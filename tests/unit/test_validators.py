"""Tests for validator modules."""

from cognitive_toolworks.validators.anthropic import (
    AnthropicValidator,
    ValidationSeverity,
)
from cognitive_toolworks.validators.openai import (
    OpenAIValidator,
    validate_cross_platform,
)


class TestAnthropicValidator:
    """Tests for AnthropicValidator."""

    def test_valid_skill(self) -> None:
        """Test validation of valid skill."""
        validator = AnthropicValidator()
        content = """---
name: valid-skill
description: A valid skill for testing validation
---

# Valid Skill

## Overview

This is a valid skill.

## When to Use This Skill

- When testing
- When validating

## Instructions

Do the thing.
"""
        result = validator.validate(content)
        assert result.passed is True
        assert len(result.errors) == 0

    def test_missing_frontmatter(self) -> None:
        """Test validation catches missing frontmatter."""
        validator = AnthropicValidator()
        content = """# No Frontmatter

Just content.
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("frontmatter" in i.field for i in result.issues)

    def test_name_too_long(self) -> None:
        """Test validation catches long name."""
        validator = AnthropicValidator()
        content = f"""---
name: {"a" * 100}
description: Valid description
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("64 chars" in i.message for i in result.issues)

    def test_name_uppercase(self) -> None:
        """Test validation catches uppercase name."""
        validator = AnthropicValidator()
        content = """---
name: MySkill
description: Valid description
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("lowercase" in i.message for i in result.issues)

    def test_description_too_long(self) -> None:
        """Test validation catches long description."""
        validator = AnthropicValidator()
        content = f"""---
name: valid-name
description: {"a" * 250}
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("200 chars" in i.message for i in result.issues)

    def test_description_xml_tags(self) -> None:
        """Test validation catches XML tags in description."""
        validator = AnthropicValidator()
        content = """---
name: valid-name
description: Description with <tag>content</tag>
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("XML" in i.message for i in result.issues)

    def test_missing_name(self) -> None:
        """Test validation catches missing name."""
        validator = AnthropicValidator()
        content = """---
description: Has description but no name
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("name is required" in i.message for i in result.issues)

    def test_missing_description(self) -> None:
        """Test validation catches missing description."""
        validator = AnthropicValidator()
        content = """---
name: valid-name
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("description is required" in i.message for i in result.issues)

    def test_auto_fix_name(self) -> None:
        """Test auto-fix corrects name."""
        validator = AnthropicValidator()
        content = """---
name: My_Invalid Name!
description: Valid description
---

# Skill
"""
        fixed = validator.auto_fix(content)
        assert "my-invalid-name" in fixed
        assert "My_Invalid Name!" not in fixed

    def test_auto_fix_description(self) -> None:
        """Test auto-fix handles XML tags."""
        validator = AnthropicValidator()
        content = """---
name: valid-name
description: Has <tag>XML</tag> content
---

# Skill
"""
        fixed = validator.auto_fix(content)
        assert "<tag>" not in fixed
        assert "Has  content" in fixed or "Has XML content" in fixed

    def test_severity_levels(self) -> None:
        """Test severity level classification."""
        validator = AnthropicValidator()

        # Missing required field = error
        content_error = """---
description: No name
---
"""
        result = validator.validate(content_error)
        assert any(i.severity == ValidationSeverity.ERROR for i in result.issues)

        # Missing recommended section = warning or info
        content_warning = """---
name: valid-name
description: Valid description
---

# No sections
"""
        result = validator.validate(content_warning)
        assert any(
            i.severity in (ValidationSeverity.WARNING, ValidationSeverity.INFO)
            for i in result.issues
        )


class TestOpenAIValidator:
    """Tests for OpenAIValidator."""

    def test_valid_skill(self) -> None:
        """Test validation of valid skill."""
        validator = OpenAIValidator()
        content = """---
name: valid-skill
description: A valid skill for OpenAI Codex
---

# Valid Skill

Content here.
"""
        result = validator.validate(content)
        assert result.passed is True

    def test_longer_description_allowed(self) -> None:
        """Test OpenAI allows longer descriptions."""
        validator = OpenAIValidator()
        # 500 chars is OK for OpenAI (limit is 1024)
        content = f"""---
name: valid-name
description: {"a" * 500}
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is True

    def test_description_too_long(self) -> None:
        """Test OpenAI catches descriptions over 1024."""
        validator = OpenAIValidator()
        content = f"""---
name: valid-name
description: {"a" * 1100}
---

# Skill
"""
        result = validator.validate(content)
        assert result.passed is False
        assert any("1024 chars" in i.message for i in result.issues)


class TestCrossPlatformValidation:
    """Tests for cross-platform validation."""

    def test_both_pass(self) -> None:
        """Test skill that passes both platforms."""
        content = """---
name: universal-skill
description: Works on both platforms
---

# Universal Skill

## Overview

This skill works everywhere.

## When to Use

- Always
"""
        results = validate_cross_platform(content)

        assert "anthropic" in results
        assert "openai" in results
        assert results["anthropic"].passed is True
        assert results["openai"].passed is True

    def test_anthropic_only_fail(self) -> None:
        """Test skill that fails only Anthropic validation."""
        # Long description passes OpenAI but fails Anthropic
        content = f"""---
name: anthropic-fail
description: {"a" * 250}
---

# Skill
"""
        results = validate_cross_platform(content)

        assert results["anthropic"].passed is False
        assert results["openai"].passed is True
