"""Tests for template rendering and platform selection."""

from cognitive_toolworks.generators.skill import GenerationConfig, SkillGenerator
from cognitive_toolworks.models import Platform, SkillContent, SkillMetadata


class TestSkillMetadataYAML:
    """Tests for SkillMetadata YAML generation."""

    def test_to_yaml_basic(self) -> None:
        """Test basic Anthropic YAML generation."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill",
        )
        yaml = meta.to_yaml()

        assert "---" in yaml
        assert "name: test-skill" in yaml
        assert 'description: "A test skill"' in yaml
        assert yaml.count("---") == 2

    def test_to_yaml_with_tools(self) -> None:
        """Test YAML generation with allowed tools."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill",
            allowed_tools=["Bash", "Read", "Write"],
        )
        yaml = meta.to_yaml()

        assert "allowed-tools: Bash, Read, Write" in yaml

    def test_to_yaml_with_dependencies(self) -> None:
        """Test YAML generation with dependencies."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill",
            dependencies=["other-skill", "another-skill"],
        )
        yaml = meta.to_yaml()

        assert "dependencies:" in yaml
        assert "  - other-skill" in yaml
        assert "  - another-skill" in yaml

    def test_to_openai_yaml_basic(self) -> None:
        """Test basic OpenAI YAML generation."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill for OpenAI",
        )
        yaml = meta.to_openai_yaml()

        assert "---" in yaml
        assert "name: test-skill" in yaml
        assert 'description: "A test skill for OpenAI"' in yaml

    def test_to_openai_yaml_with_category(self) -> None:
        """Test OpenAI YAML includes category field."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill",
            category="automation",
        )
        yaml = meta.to_openai_yaml()

        assert "category: automation" in yaml

    def test_to_openai_yaml_with_version(self) -> None:
        """Test OpenAI YAML includes version field."""
        meta = SkillMetadata(
            name="test-skill",
            description="A test skill",
            version="2.1.0",
        )
        yaml = meta.to_openai_yaml()

        assert "version: 2.1.0" in yaml

    def test_to_openai_yaml_longer_description(self) -> None:
        """Test OpenAI YAML supports longer descriptions."""
        # 500 chars - too long for Anthropic, OK for OpenAI
        long_desc = "a" * 500
        meta = SkillMetadata(
            name="test-skill",
            description=long_desc,
        )

        # Should validate fine for OpenAI
        issues = meta.validate_openai()
        assert len(issues) == 0

        # Should render without issues
        yaml = meta.to_openai_yaml()
        assert long_desc in yaml


class TestSkillGeneratorTemplateSelection:
    """Tests for platform-based template selection in SkillGenerator."""

    def test_default_platform_universal(self) -> None:
        """Test default platform is UNIVERSAL."""
        config = GenerationConfig()
        assert config.platform == Platform.UNIVERSAL

    def test_render_skill_anthropic(self) -> None:
        """Test rendering with Anthropic template."""
        config = GenerationConfig(platform=Platform.ANTHROPIC)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(
            name="test-skill",
            description="Test skill for Anthropic",
        )
        skill = SkillContent(
            metadata=meta,
            overview="This is a test skill",
            when_to_use=["When you need to test", "When testing is required"],
            quick_reference="Run the test",
            instructions="Execute the test command",
            examples=[
                {
                    "title": "Basic Test",
                    "description": "Run a basic test",
                    "code": "test --run",
                    "language": "bash",
                }
            ],
            guidelines=["Follow best practices", "Test thoroughly"],
        )

        rendered = generator.render_skill(skill, platform=Platform.ANTHROPIC)

        # Check frontmatter
        assert "---" in rendered
        assert "name: test-skill" in rendered
        assert "# Test Skill" in rendered

        # Check sections
        assert "## When to Use This Skill" in rendered
        assert "- When you need to test" in rendered
        assert "## Quick Reference" in rendered
        assert "## Instructions" in rendered
        assert "## Examples" in rendered
        assert "### Example 1: Basic Test" in rendered
        assert "## Guidelines" in rendered
        assert "```bash" in rendered

    def test_render_skill_openai(self) -> None:
        """Test rendering with OpenAI template."""
        config = GenerationConfig(platform=Platform.OPENAI)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(
            name="openai-test-skill",
            description="Test skill for OpenAI Codex CLI",
            category="testing",
            version="1.2.0",
        )
        skill = SkillContent(
            metadata=meta,
            overview="This is an OpenAI test skill",
            when_to_use=["When using Codex CLI"],
            quick_reference="codex test",
            instructions="Run codex test command",
            examples=[],
            guidelines=["Use best practices"],
        )

        rendered = generator.render_skill(skill, platform=Platform.OPENAI)

        # Check OpenAI-specific frontmatter
        assert "name: openai-test-skill" in rendered
        assert "category: testing" in rendered
        assert "version: 1.2.0" in rendered

        # Check structure
        assert "# Openai Test Skill" in rendered
        assert "## When to Use This Skill" in rendered

    def test_render_skill_universal_uses_anthropic(self) -> None:
        """Test UNIVERSAL platform uses Anthropic template (more restrictive)."""
        config = GenerationConfig(platform=Platform.UNIVERSAL)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(
            name="universal-skill",
            description="Universal skill",
        )
        skill = SkillContent(
            metadata=meta,
            overview="Universal skill overview",
            when_to_use=["Always"],
            quick_reference="run",
            instructions="Execute",
            examples=[],
            guidelines=[],
        )

        # UNIVERSAL should use Anthropic template as it's more restrictive
        rendered = generator.render_skill(skill, platform=Platform.UNIVERSAL)

        # Should look like Anthropic format
        assert "name: universal-skill" in rendered
        assert "# Universal Skill" in rendered

    def test_render_skill_with_troubleshooting(self) -> None:
        """Test rendering with troubleshooting section."""
        config = GenerationConfig(platform=Platform.ANTHROPIC)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(name="test-skill", description="Test")
        skill = SkillContent(
            metadata=meta,
            overview="Test",
            when_to_use=["Test"],
            quick_reference="test",
            instructions="Test",
            examples=[],
            guidelines=[],
            troubleshooting=[
                {"issue": "Command fails", "solution": "Check permissions"},
                {"issue": "Timeout error", "solution": "Increase timeout value"},
            ],
        )

        rendered = generator.render_skill(skill)

        assert "## Troubleshooting" in rendered
        assert "### Command fails" in rendered
        assert "Check permissions" in rendered
        assert "### Timeout error" in rendered

    def test_render_skill_with_references(self) -> None:
        """Test rendering with references section."""
        config = GenerationConfig(platform=Platform.OPENAI)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(name="test-skill", description="Test")
        skill = SkillContent(
            metadata=meta,
            overview="Test",
            when_to_use=["Test"],
            quick_reference="test",
            instructions="Test",
            examples=[],
            guidelines=[],
            references=[
                "[Official Docs](https://example.com/docs)",
                "[GitHub](https://github.com/example)",
            ],
        )

        rendered = generator.render_skill(skill)

        assert "## See Also" in rendered
        assert "[Official Docs](https://example.com/docs)" in rendered
        assert "[GitHub](https://github.com/example)" in rendered

    def test_platform_override(self) -> None:
        """Test platform override in render_skill."""
        # Generator configured for ANTHROPIC
        config = GenerationConfig(platform=Platform.ANTHROPIC)
        generator = SkillGenerator(config=config)

        meta = SkillMetadata(
            name="test-skill",
            description="Test",
            category="test",
        )
        skill = SkillContent(
            metadata=meta,
            overview="Test",
            when_to_use=["Test"],
            quick_reference="test",
            instructions="Test",
            examples=[],
            guidelines=[],
        )

        # Override to use OpenAI template
        rendered = generator.render_skill(skill, platform=Platform.OPENAI)

        # Should use OpenAI format (includes category)
        assert "category: test" in rendered


class TestPlatformValidation:
    """Tests for platform-specific validation."""

    def test_anthropic_description_limit(self) -> None:
        """Test Anthropic enforces 200 char description limit."""
        meta = SkillMetadata(
            name="test-skill",
            description="a" * 250,  # Too long
        )
        issues = meta.validate_anthropic()
        assert len(issues) > 0
        assert any("200 chars" in issue for issue in issues)

    def test_openai_description_limit(self) -> None:
        """Test OpenAI allows 1024 char descriptions."""
        meta = SkillMetadata(
            name="test-skill",
            description="a" * 500,  # OK for OpenAI
        )
        issues = meta.validate_openai()
        assert len(issues) == 0

    def test_openai_description_too_long(self) -> None:
        """Test OpenAI enforces 1024 char limit."""
        meta = SkillMetadata(
            name="test-skill",
            description="a" * 1100,  # Too long
        )
        issues = meta.validate_openai()
        assert len(issues) > 0
        assert any("1024 chars" in issue for issue in issues)

    def test_universal_should_use_stricter_limits(self) -> None:
        """Test that UNIVERSAL platform should use Anthropic's stricter limits."""
        # This is a design choice - UNIVERSAL should be compatible with both,
        # so it should use the more restrictive limits (Anthropic's 200 chars)
        meta = SkillMetadata(
            name="test-skill",
            description="a" * 250,
        )

        # For UNIVERSAL, validate against Anthropic limits
        anthropic_issues = meta.validate_anthropic()
        assert len(anthropic_issues) > 0
