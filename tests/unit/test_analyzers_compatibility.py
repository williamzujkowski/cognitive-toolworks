"""Tests for compatibility analyzer."""

from cognitive_toolworks.analyzers.compatibility import CompatibilityChecker
from cognitive_toolworks.models import (
    CompatibilityIssue,
    CompatibilityReport,
    CompatibilitySeverity,
    Platform,
    SkillContent,
    SkillMetadata,
)


class TestCompatibilityChecker:
    """Tests for CompatibilityChecker."""

    def test_universal_compatible_skill(self) -> None:
        """Test skill compatible with both platforms."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="test-skill",
            description="A test skill for compatibility checking",
            allowed_tools=["Bash", "Read"],
            version="1.0.0",
            category="testing",
        )

        report = checker.analyze(metadata)

        assert report.is_anthropic_compatible is True
        assert report.is_openai_compatible is True
        assert report.is_universal is True
        assert len(report.anthropic_issues) == 0
        # OpenAI may have INFO-level suggestions but no errors
        assert all(i.severity != CompatibilitySeverity.ERROR for i in report.openai_issues)

    def test_anthropic_description_too_long(self) -> None:
        """Test Anthropic description length limit (200 chars)."""
        checker = CompatibilityChecker()
        long_desc = "x" * 201  # Exceeds Anthropic limit
        metadata = SkillMetadata(name="test-skill", description=long_desc)

        report = checker.analyze(metadata)

        assert report.is_anthropic_compatible is False
        assert report.is_openai_compatible is True  # OpenAI allows 1024 chars
        assert len(report.anthropic_issues) > 0

        # Check for specific error
        desc_errors = [i for i in report.anthropic_issues if i.field == "description"]
        assert len(desc_errors) > 0
        assert desc_errors[0].severity == CompatibilitySeverity.ERROR
        assert "200 chars" in desc_errors[0].message

    def test_openai_description_too_long(self) -> None:
        """Test OpenAI description length limit (1024 chars)."""
        checker = CompatibilityChecker()
        long_desc = "x" * 1025  # Exceeds OpenAI limit
        metadata = SkillMetadata(name="test-skill", description=long_desc)

        report = checker.analyze(metadata)

        assert report.is_anthropic_compatible is False  # Also fails Anthropic
        assert report.is_openai_compatible is False
        assert len(report.openai_issues) > 0

        # Check for specific error
        desc_errors = [i for i in report.openai_issues if i.field == "description"]
        assert len(desc_errors) > 0
        assert desc_errors[0].severity == CompatibilitySeverity.ERROR
        assert "1024 chars" in desc_errors[0].message

    def test_anthropic_name_invalid_format(self) -> None:
        """Test Anthropic name format requirements."""
        checker = CompatibilityChecker()

        # Test uppercase (not allowed)
        metadata = SkillMetadata(name="TestSkill", description="Test")
        report = checker.analyze(metadata)
        assert report.is_anthropic_compatible is False
        name_errors = [i for i in report.anthropic_issues if i.field == "name"]
        assert len(name_errors) > 0

        # Test spaces (not allowed)
        metadata = SkillMetadata(name="test skill", description="Test")
        report = checker.analyze(metadata)
        assert report.is_anthropic_compatible is False

        # Test special characters (not allowed)
        metadata = SkillMetadata(name="test_skill!", description="Test")
        report = checker.analyze(metadata)
        assert report.is_anthropic_compatible is False

    def test_anthropic_name_too_long(self) -> None:
        """Test Anthropic name length limit (64 chars)."""
        checker = CompatibilityChecker()
        long_name = "x" * 65
        metadata = SkillMetadata(name=long_name, description="Test")

        report = checker.analyze(metadata)

        assert report.is_anthropic_compatible is False
        name_errors = [i for i in report.anthropic_issues if i.field == "name"]
        assert len(name_errors) > 0
        assert any("64 chars" in e.message for e in name_errors)

    def test_anthropic_description_xml_tags(self) -> None:
        """Test Anthropic prohibition of XML tags in description."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(name="test-skill", description="Use <tool> to process data")

        report = checker.analyze(metadata)

        assert report.is_anthropic_compatible is False
        desc_errors = [
            i for i in report.anthropic_issues if i.field == "description" and "XML" in i.message
        ]
        assert len(desc_errors) > 0
        assert desc_errors[0].severity == CompatibilitySeverity.ERROR

    def test_anthropic_consecutive_hyphens_warning(self) -> None:
        """Test warning for consecutive hyphens in name."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(name="test--skill", description="Test skill")

        report = checker.analyze(metadata)

        # Should still be compatible but have a warning
        warning_issues = [
            i for i in report.anthropic_issues if i.severity == CompatibilitySeverity.WARNING
        ]
        assert len(warning_issues) > 0
        assert any("consecutive hyphens" in w.message for w in warning_issues)

    def test_anthropic_wildcard_tools_warning(self) -> None:
        """Test warning for wildcard in allowed-tools."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="test-skill",
            description="Test skill",
            allowed_tools=["*"],
        )

        report = checker.analyze(metadata)

        warning_issues = [i for i in report.anthropic_issues if i.field == "allowed-tools"]
        assert len(warning_issues) > 0
        assert warning_issues[0].severity == CompatibilitySeverity.WARNING
        assert "Wildcards" in warning_issues[0].message

    def test_openai_category_recommendation(self) -> None:
        """Test OpenAI recommendation for category field."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="test-skill",
            description="Test skill",
            category=None,  # No category
        )

        report = checker.analyze(metadata)

        # Should be compatible but have INFO suggestion
        assert report.is_openai_compatible is True
        info_issues = [i for i in report.openai_issues if i.severity == CompatibilitySeverity.INFO]
        assert any(i.field == "category" for i in info_issues)

    def test_openai_version_recommendation(self) -> None:
        """Test OpenAI recommendation for version field."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="test-skill",
            description="Test skill",
            version="1.0.0",  # Default version
        )

        report = checker.analyze(metadata)

        # Should have INFO suggestion about version
        info_issues = [i for i in report.openai_issues if i.severity == CompatibilitySeverity.INFO]
        assert any(i.field == "version" for i in info_issues)

    def test_analyze_from_markdown_string(self) -> None:
        """Test analyzing from markdown string."""
        checker = CompatibilityChecker()
        content = """---
name: test-skill
description: "A test skill for compatibility"
allowed-tools: Bash, Read
---

# Test Skill

This is a test skill.
"""

        report = checker.analyze(content)

        assert report.is_anthropic_compatible is True
        assert report.is_openai_compatible is True

    def test_analyze_from_skill_content(self) -> None:
        """Test analyzing from SkillContent object."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="test-skill",
            description="Test skill",
            category="testing",
        )
        content = SkillContent(
            metadata=metadata,
            overview="Test overview",
            when_to_use=["When testing"],
            quick_reference="Quick ref",
            instructions="Do the thing",
            examples=[],
            guidelines=["Be thorough"],
        )

        report = checker.analyze(content)

        assert report.is_anthropic_compatible is True
        assert report.is_openai_compatible is True

    def test_analyze_invalid_yaml_frontmatter(self) -> None:
        """Test handling of invalid YAML frontmatter."""
        checker = CompatibilityChecker()
        content = """---
name: test-skill
description: "Unclosed quote
---

# Test Skill
"""

        report = checker.analyze(content)

        # Should handle gracefully and create minimal metadata
        assert report is not None

    def test_analyze_missing_frontmatter(self) -> None:
        """Test handling of missing frontmatter."""
        checker = CompatibilityChecker()
        content = """# Test Skill

No frontmatter here.
"""

        report = checker.analyze(content)

        # Should handle gracefully
        assert report is not None
        # Missing frontmatter creates minimal metadata which may be compatible
        # but will have an empty description (which is technically valid but not useful)
        # The checker should still work without crashing
        assert isinstance(report, CompatibilityReport)

    def test_recommendations_generation(self) -> None:
        """Test recommendation generation."""
        checker = CompatibilityChecker()

        # Test universal compatibility
        good_metadata = SkillMetadata(
            name="test-skill",
            description="Test",
            category="testing",
        )
        report = checker.analyze(good_metadata)
        assert "compatible with both" in " ".join(report.recommendations).lower()

        # Test Anthropic-only compatibility
        long_desc = "x" * 250  # Too long for Anthropic, ok for OpenAI
        metadata = SkillMetadata(name="test-skill", description=long_desc)
        report = checker.analyze(metadata)
        assert any("anthropic" in r.lower() for r in report.recommendations)

    def test_compatibility_report_properties(self) -> None:
        """Test CompatibilityReport property methods."""
        checker = CompatibilityChecker()
        metadata = SkillMetadata(
            name="TestSkill",  # Invalid for Anthropic
            description="x" * 1025,  # Invalid for OpenAI
        )

        report = checker.analyze(metadata)

        # Test properties
        assert len(report.anthropic_issues) > 0
        assert len(report.openai_issues) > 0
        assert report.is_universal is False

        # Test to_dict
        report_dict = report.to_dict()
        assert "is_anthropic_compatible" in report_dict
        assert "is_openai_compatible" in report_dict
        assert "is_universal" in report_dict
        assert "issues" in report_dict
        assert "recommendations" in report_dict
        assert "counts" in report_dict

        # Check counts
        assert report_dict["counts"]["anthropic"] == len(report.anthropic_issues)
        assert report_dict["counts"]["openai"] == len(report.openai_issues)
        assert report_dict["counts"]["total"] == len(report.issues)

    def test_compatibility_issue_to_dict(self) -> None:
        """Test CompatibilityIssue to_dict method."""
        issue = CompatibilityIssue(
            severity=CompatibilitySeverity.ERROR,
            platform=Platform.ANTHROPIC,
            field="description",
            message="Description too long",
            fix_suggestion="Shorten to 200 chars",
        )

        issue_dict = issue.to_dict()
        assert issue_dict["severity"] == "error"
        assert issue_dict["platform"] == "anthropic"
        assert issue_dict["field"] == "description"
        assert issue_dict["message"] == "Description too long"
        assert issue_dict["fix"] == "Shorten to 200 chars"

    def test_name_fixing_suggestion(self) -> None:
        """Test name fixing suggestions."""
        checker = CompatibilityChecker()

        # Test uppercase to lowercase
        metadata = SkillMetadata(name="TestSkill", description="Test")
        report = checker.analyze(metadata)
        name_issues = [i for i in report.anthropic_issues if i.field == "name"]
        assert any(
            i.fix_suggestion and "testskill" in i.fix_suggestion.lower() for i in name_issues
        )

        # Test with actual hyphens to verify they're preserved
        metadata2 = SkillMetadata(name="Test-Skill", description="Test")
        report2 = checker.analyze(metadata2)
        name_issues2 = [i for i in report2.anthropic_issues if i.field == "name"]
        assert any(i.fix_suggestion and "test-skill" in i.fix_suggestion for i in name_issues2)

    def test_allowed_tools_string_format(self) -> None:
        """Test parsing of allowed-tools as comma-separated string."""
        checker = CompatibilityChecker()
        content = """---
name: test-skill
description: "Test skill"
allowed-tools: "Bash, Read, Write"
---

# Test Skill
"""

        report = checker.analyze(content)
        # Should parse correctly and not cause errors
        assert report is not None

    def test_edge_case_exact_limits(self) -> None:
        """Test edge cases at exact limit boundaries."""
        checker = CompatibilityChecker()

        # Anthropic description at exactly 200 chars
        desc_200 = "x" * 200
        metadata = SkillMetadata(name="test-skill", description=desc_200)
        report = checker.analyze(metadata)
        assert report.is_anthropic_compatible is True

        # Anthropic description at 201 chars
        desc_201 = "x" * 201
        metadata = SkillMetadata(name="test-skill", description=desc_201)
        report = checker.analyze(metadata)
        assert report.is_anthropic_compatible is False

        # OpenAI description at exactly 1024 chars
        desc_1024 = "x" * 1024
        metadata = SkillMetadata(name="test-skill", description=desc_1024)
        report = checker.analyze(metadata)
        assert report.is_openai_compatible is True

        # OpenAI description at 1025 chars
        desc_1025 = "x" * 1025
        metadata = SkillMetadata(name="test-skill", description=desc_1025)
        report = checker.analyze(metadata)
        assert report.is_openai_compatible is False
