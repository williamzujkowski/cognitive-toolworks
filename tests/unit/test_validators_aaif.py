"""Tests for AAIF validator."""

from cognitive_toolworks.validators.aaif import AAIFValidator
from cognitive_toolworks.validators.anthropic import ValidationSeverity


class TestAAIFValidator:
    """Tests for AAIFValidator."""

    def test_valid_skill(self) -> None:
        """Test validation of valid AAIF-compliant skill."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "A valid AAIF skill for testing validation compliance"
capabilities:
  - Test validation
  - Check compliance
inputs:
  - test_input: "Input description (string, required)"
outputs:
  - test_output: "Output description"
keywords:
  - testing
  - validation
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com/docs
---

## Purpose & When-To-Use

Test skill for validation.

## Pre-Checks

Input validation checks.

## Procedure

### Step 1: Execute tests

Do the testing.

## Decision Rules

Abort if invalid.

## Output Contract

Returns validation results.

## Examples

### Example 1: Basic test

```python
result = validate()
```

## Quality Gates

Token budgets: T1 ≤ 2k, T2 ≤ 6k, T3 ≤ 12k tokens.

## Resources

See links above.
"""
        result = validator.validate(content)
        assert result.valid is True
        assert len(result.errors) == 0
        assert result.tier_compliance.get("T1", False) is True
        assert result.score > 0.8

    def test_missing_frontmatter(self) -> None:
        """Test validation catches missing frontmatter."""
        validator = AAIFValidator()
        content = """# No Frontmatter

Just content.
"""
        result = validator.validate(content)
        assert result.valid is False
        assert any("frontmatter" in i.field for i in result.issues)

    def test_missing_required_fields(self) -> None:
        """Test validation catches missing required frontmatter fields."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
description: "Missing other fields"
---

# Skill
"""
        result = validator.validate(content)
        assert result.valid is False
        # Should have errors for missing slug, capabilities, inputs, etc.
        missing_fields = [
            i for i in result.issues if i.severity == ValidationSeverity.ERROR
        ]
        assert len(missing_fields) > 5

    def test_description_too_long(self) -> None:
        """Test validation catches description over 160 chars."""
        validator = AAIFValidator()
        long_desc = "a" * 200
        content = f"""---
name: "Test Skill"
slug: "test-skill-validator"
description: "{long_desc}"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public"
links:
  - https://example.com
---

# Skill
"""
        result = validator.validate(content)
        assert result.valid is False
        assert any("160 chars" in i.message for i in result.issues)

    def test_invalid_slug_format(self) -> None:
        """Test validation catches invalid slug format."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "InvalidSlug"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

# Skill
"""
        result = validator.validate(content)
        # Should have warning about slug format
        assert any(
            "naming convention" in i.message.lower()
            and i.severity == ValidationSeverity.WARNING
            for i in result.issues
        )

    def test_missing_required_sections(self) -> None:
        """Test validation catches missing required sections."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

# Skill

Just minimal content.
"""
        result = validator.validate(content)
        assert result.valid is False
        # Should have errors for missing sections
        section_errors = [
            i
            for i in result.issues
            if i.field == "sections" and i.severity == ValidationSeverity.ERROR
        ]
        assert len(section_errors) > 0

    def test_token_budget_t1_exceeded(self) -> None:
        """Test validation catches T1 token budget violation."""
        validator = AAIFValidator()
        # Create content that exceeds T1 budget
        long_content = "\n".join([f"Line {i}: " + "word " * 50 for i in range(100)])
        content = f"""---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

{long_content}

## Pre-Checks

{long_content}

## Procedure

Content here.

## Decision Rules

Content here.

## Output Contract

Content here.

## Examples

Content here.

## Quality Gates

Content here.

## Resources

Content here.
"""
        result = validator.validate(content)
        # Should have error or warning about T1 budget
        token_issues = [i for i in result.issues if "token" in i.message.lower()]
        assert len(token_issues) > 0

    def test_example_too_long(self) -> None:
        """Test validation catches examples over 30 lines."""
        validator = AAIFValidator()
        long_example = "\n".join([f"# Line {i}" for i in range(40)])
        content = f"""---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test skill.

## Pre-Checks

Checks here.

## Procedure

Steps here.

## Decision Rules

Rules here.

## Output Contract

Contract here.

## Examples

### Example 1: Long example

{long_example}

## Quality Gates

Gates here.

## Resources

Resources here.
"""
        result = validator.validate(content)
        assert any("30 lines" in i.message for i in result.issues)

    def test_todo_markers_detected(self) -> None:
        """Test validation catches TODO markers."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

[TODO: Add purpose]

## Pre-Checks

Checks here.

## Procedure

Steps here.

## Decision Rules

Rules here.

## Output Contract

Contract here.

## Examples

Example here.

## Quality Gates

Gates here.

## Resources

Resources here.
"""
        result = validator.validate(content)
        assert result.valid is False
        assert any(
            "TODO" in i.message and i.severity == ValidationSeverity.ERROR
            for i in result.issues
        )

    def test_security_secrets_detected(self) -> None:
        """Test validation catches potential secrets."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test skill.

## Pre-Checks

API_KEY = "fake_test_key_abcdefghijklmnopqrst"

## Procedure

Steps here.

## Decision Rules

Rules here.

## Output Contract

Contract here.

## Examples

Example here.

## Quality Gates

Gates here.

## Resources

Resources here.
"""
        result = validator.validate(content)
        assert result.valid is False
        assert any(
            "API key" in i.message and i.severity == ValidationSeverity.ERROR
            for i in result.issues
        )

    def test_sections_out_of_order(self) -> None:
        """Test validation detects sections out of order."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test skill.

## Procedure

Steps here (should come after Pre-Checks).

## Pre-Checks

Checks here (should come before Procedure).

## Decision Rules

Rules here.

## Output Contract

Contract here.

## Examples

Example here.

## Quality Gates

Gates here.

## Resources

Resources here.
"""
        result = validator.validate(content)
        # Should have warning about section order
        assert any(
            "out of order" in i.message.lower()
            and i.severity == ValidationSeverity.WARNING
            for i in result.issues
        )

    def test_tier_compliance_tracking(self) -> None:
        """Test that tier compliance is properly tracked."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Short content.

## Pre-Checks

Short content.

## Procedure

Short content.

## Decision Rules

Short content.

## Output Contract

Short content.

## Examples

Short example.

## Quality Gates

Token budgets mentioned here.

## Resources

Links.
"""
        result = validator.validate(content)
        assert "T1" in result.tier_compliance
        assert "T2" in result.tier_compliance
        assert "T3" in result.tier_compliance

    def test_compliance_score_calculation(self) -> None:
        """Test compliance score is calculated correctly."""
        validator = AAIFValidator()
        # Perfect skill
        perfect_content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "A valid AAIF skill for testing"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test skill.

## Pre-Checks

Checks here.

## Procedure

### Step 1: Test

Do the test.

## Decision Rules

Rules here.

## Output Contract

Contract here.

## Examples

### Example 1: Test

```python
test()
```

## Quality Gates

Token budgets: T1 ≤ 2k, T2 ≤ 6k, T3 ≤ 12k tokens.

## Resources

See links.
"""
        result = validator.validate(perfect_content)
        assert result.score >= 0.8  # Should have high score

        # Imperfect skill
        imperfect_content = """---
name: "Test"
slug: "test"
description: "Test"
---

# Missing everything
"""
        result2 = validator.validate(imperfect_content)
        assert result2.score < 0.5  # Should have low score

    def test_validate_file(self, tmp_path) -> None:
        """Test validate_file method."""
        validator = AAIFValidator()
        skill_file = tmp_path / "SKILL.md"
        skill_file.write_text(
            """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test skill.

## Pre-Checks

Checks.

## Procedure

Steps.

## Decision Rules

Rules.

## Output Contract

Contract.

## Examples

Example.

## Quality Gates

Gates.

## Resources

Resources.
"""
        )
        result = validator.validate_file(skill_file)
        assert isinstance(result.valid, bool)
        assert isinstance(result.score, float)

    def test_to_dict(self) -> None:
        """Test AAIFValidationResult to_dict method."""
        validator = AAIFValidator()
        content = """---
name: "Test Skill"
slug: "testing-unit-validator"
description: "Valid description"
capabilities:
  - Test
inputs:
  - input1: "test"
outputs:
  - output1: "test"
keywords:
  - test
version: "1.0.0"
owner: "test"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://example.com
---

## Purpose & When-To-Use

Test.

## Pre-Checks

Test.

## Procedure

Test.

## Decision Rules

Test.

## Output Contract

Test.

## Examples

Test.

## Quality Gates

Test.

## Resources

Test.
"""
        result = validator.validate(content)
        result_dict = result.to_dict()

        assert "valid" in result_dict
        assert "tier_compliance" in result_dict
        assert "issues" in result_dict
        assert "score" in result_dict
        assert "counts" in result_dict
        assert isinstance(result_dict["issues"], list)
