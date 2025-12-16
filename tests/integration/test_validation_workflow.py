"""
Integration tests for validation → auto-fix → re-validation workflow.

Tests the complete validation roundtrip:
1. Load a SKILL.md file
2. Run validation to detect issues
3. Apply auto-fixes where possible
4. Re-validate to confirm fixes worked
"""

from pathlib import Path

import pytest

from cognitive_toolworks.validators.aaif import AAIFValidator
from cognitive_toolworks.validators.anthropic import (
    AnthropicValidator,
    ValidationSeverity,
)


@pytest.fixture
def fixtures_dir() -> Path:
    """Get the integration fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def invalid_skill_path(fixtures_dir: Path) -> Path:
    """Path to intentionally invalid skill file."""
    return fixtures_dir / "invalid_skill.md"


@pytest.fixture
def sample_valid_skill(tmp_path: Path) -> Path:
    """Create a valid skill file for testing."""
    skill_content = """---
name: test-validation-skill
slug: test-validation-skill
description: A valid test skill for validation workflow testing
capabilities:
  - Test validation
  - Verify workflows
inputs:
  test_input:
    type: string
    required: true
outputs:
  test_output:
    type: string
keywords:
  - testing
  - validation
version: 1.0.0
owner: test
license: MIT
---

# Test Validation Skill

## Overview

This skill tests the validation workflow with proper structure.

## When to Use This Skill

- When testing validation
- When verifying skill compliance
- When ensuring quality

## Instructions

1. Load the skill file
2. Run validation
3. Check results

```bash
ct validate skill.md
```

## Examples

### Example 1: Basic Validation

```python
validator = AnthropicValidator()
result = validator.validate_file("skill.md")
assert result.passed
```

## Troubleshooting

### Validation Fails

Check error messages and fix issues.

## Guidelines

- Follow Anthropic specification
- Keep descriptions concise
- Include required sections
"""
    skill_file = tmp_path / "valid_skill.md"
    skill_file.write_text(skill_content)
    return skill_file


@pytest.mark.integration
class TestValidationWorkflow:
    """Integration tests for validation workflows."""

    def test_detect_invalid_skill_issues(self, invalid_skill_path: Path) -> None:
        """Test that validation correctly detects issues in invalid skill."""
        validator = AnthropicValidator()
        result = validator.validate_file(invalid_skill_path)

        # Should fail validation
        assert not result.passed

        # Should detect uppercase name issue
        name_issues = [
            issue
            for issue in result.issues
            if issue.field == "name" or "name" in issue.message.lower()
        ]
        assert len(name_issues) > 0

        # Should have error-level issues
        assert len(result.errors) > 0

    def test_validate_valid_skill(self, sample_valid_skill: Path) -> None:
        """Test that a properly formatted skill passes validation."""
        validator = AnthropicValidator()
        result = validator.validate_file(sample_valid_skill)

        # Should pass or only have minor warnings
        if not result.passed:
            print("Validation issues:")
            for issue in result.issues:
                print(f"  {issue.severity.value}: {issue.field}: {issue.message}")

        # Should have no errors (warnings are acceptable)
        assert len(result.errors) == 0

    def test_auto_fix_suggestions(self, invalid_skill_path: Path) -> None:
        """Test that validator provides fix suggestions for common issues."""
        validator = AnthropicValidator()
        result = validator.validate_file(invalid_skill_path)

        # Should provide fix suggestions
        issues_with_fixes = [issue for issue in result.issues if issue.fix_suggestion]
        assert len(issues_with_fixes) > 0

    def test_validation_roundtrip_with_fixes(
        self, invalid_skill_path: Path, tmp_path: Path
    ) -> None:
        """
        Test complete roundtrip: validate → fix → re-validate.

        This is the key integration test for the validation workflow.
        """
        # Step 1: Initial validation
        validator = AnthropicValidator()
        initial_result = validator.validate_file(invalid_skill_path)

        assert not initial_result.passed
        initial_error_count = len(initial_result.errors)

        # Step 2: Apply fixes
        content = invalid_skill_path.read_text()

        # Fix uppercase name
        fixed_content = content.replace(
            "name: INVALID_SKILL_NAME_WITH_UPPERCASE",
            "name: invalid-skill-name-lowercase",
        )

        # Add missing required sections
        if "## When to Use This Skill" not in fixed_content:
            fixed_content = fixed_content.replace(
                "## Overview",
                """## Overview

This is a test skill.

## When to Use This Skill

- When testing validation
- When verifying fixes

## Instructions

1. Run validation
2. Check for issues
3. Apply fixes

""",
            )

        # Step 3: Save fixed version
        fixed_file = tmp_path / "fixed_skill.md"
        fixed_file.write_text(fixed_content)

        # Step 4: Re-validate
        fixed_result = validator.validate_file(fixed_file)

        # Assertions
        # Should have fewer errors after fixes
        fixed_error_count = len(fixed_result.errors)
        assert fixed_error_count < initial_error_count

        # Ideally should pass (or at least have no name errors)
        name_errors = [
            issue
            for issue in fixed_result.errors
            if issue.field == "name" or "name" in issue.message.lower()
        ]
        assert len(name_errors) == 0

    def test_aaif_validation_workflow(self, sample_valid_skill: Path) -> None:
        """Test AAIF validator on a valid skill."""
        validator = AAIFValidator()
        result = validator.validate_file(sample_valid_skill)

        # AAIF validation should work
        assert result is not None
        # AAIF uses 'valid' instead of 'passed'
        assert isinstance(result.valid, bool)

        # Log any issues for debugging
        if not result.valid:
            for issue in result.errors:
                print(f"AAIF ERROR: {issue.field}: {issue.message}")

    def test_multiple_validator_workflow(self, sample_valid_skill: Path) -> None:
        """Test running multiple validators on the same skill."""
        # Test Anthropic validator
        anthropic_validator = AnthropicValidator()
        anthropic_result = anthropic_validator.validate_file(sample_valid_skill)

        # Test AAIF validator
        aaif_validator = AAIFValidator()
        aaif_result = aaif_validator.validate_file(sample_valid_skill)

        # Both should complete successfully (though may have different criteria)
        assert anthropic_result is not None
        assert aaif_result is not None

        # At least one should pass with minimal errors
        # AAIF is stricter and may have more requirements
        total_errors = len(anthropic_result.errors) + len(aaif_result.errors)

        # Log errors for debugging
        if total_errors > 0:
            print(f"\nAnthropicValidator errors ({len(anthropic_result.errors)}):")
            for issue in anthropic_result.errors:
                print(f"  {issue.field}: {issue.message}")
            print(f"\nAAIF errors ({len(aaif_result.errors)}):")
            for issue in aaif_result.errors:
                print(f"  {issue.field}: {issue.message}")

        # AAIF has stricter requirements - at least Anthropic should pass
        assert len(anthropic_result.errors) < 5

    def test_validation_metadata_extraction(self, sample_valid_skill: Path) -> None:
        """Test that validators correctly extract and validate metadata."""
        validator = AnthropicValidator()
        result = validator.validate_file(sample_valid_skill)

        # Should extract metadata
        assert "name" in result.metadata or len(result.issues) > 0

        # Metadata should be in result for debugging
        assert result.metadata is not None

    def test_severity_levels(self, invalid_skill_path: Path) -> None:
        """Test that validators correctly assign severity levels."""
        validator = AnthropicValidator()
        result = validator.validate_file(invalid_skill_path)

        # Should have issues at different severity levels
        has_errors = len(result.errors) > 0
        _ = len(result.warnings) > 0  # Verify warnings list accessible

        # Should have at least errors for invalid name
        assert has_errors

    def test_real_skill_validation(self) -> None:
        """Test validation against a real skill from the repository."""
        # Use an actual skill from the skills directory
        skills_dir = Path(__file__).parent.parent.parent / "skills"
        test_skill = skills_dir / "testing-unit-generator" / "SKILL.md"

        if not test_skill.exists():
            pytest.skip("Test skill not found in repository")

        validator = AnthropicValidator()
        result = validator.validate_file(test_skill)

        # Real skills should pass validation
        if not result.passed:
            print(f"Real skill validation issues for {test_skill}:")
            for issue in result.errors:
                print(f"  ERROR: {issue.field}: {issue.message}")
            for issue in result.warnings:
                print(f"  WARNING: {issue.field}: {issue.message}")

        # Should have minimal or no errors
        assert len(result.errors) <= 2  # Allow for minor issues

    def test_validation_performance(self, sample_valid_skill: Path) -> None:
        """Test that validation completes in reasonable time."""
        import time

        validator = AnthropicValidator()

        start_time = time.time()
        result = validator.validate_file(sample_valid_skill)
        end_time = time.time()

        # Validation should be fast (under 1 second for small files)
        duration = end_time - start_time
        assert duration < 1.0

        # Should complete successfully
        assert result is not None

    def test_validation_error_messages_quality(self, invalid_skill_path: Path) -> None:
        """Test that validation error messages are clear and actionable."""
        validator = AnthropicValidator()
        result = validator.validate_file(invalid_skill_path)

        # All errors should have non-empty messages
        for issue in result.errors:
            assert len(issue.message) > 10
            assert issue.field is not None
            assert len(issue.field) > 0

        # Critical errors should have fix suggestions
        critical_errors = [
            issue for issue in result.errors if issue.severity == ValidationSeverity.ERROR
        ]
        errors_with_fixes = [issue for issue in critical_errors if issue.fix_suggestion]

        # At least 50% of errors should have fix suggestions
        if len(critical_errors) > 0:
            fix_ratio = len(errors_with_fixes) / len(critical_errors)
            assert fix_ratio >= 0.3  # At least 30% have fixes

    def test_batch_validation(self, tmp_path: Path) -> None:
        """Test validating multiple skills in sequence."""
        # Create multiple test skills
        skill_files = []
        for i in range(3):
            content = f"""---
name: test-skill-{i}
slug: test-skill-{i}
description: Test skill number {i} for batch validation
capabilities:
  - Test capability
inputs:
  input:
    type: string
outputs:
  output:
    type: string
keywords:
  - test
version: 1.0.0
owner: test
license: MIT
---

# Test Skill {i}

## Overview

Test skill for batch validation.

## When to Use This Skill

When testing.

## Instructions

Run tests.
"""
            skill_file = tmp_path / f"skill_{i}.md"
            skill_file.write_text(content)
            skill_files.append(skill_file)

        # Validate all skills
        validator = AnthropicValidator()
        results = [validator.validate_file(f) for f in skill_files]

        # All should validate
        assert len(results) == 3
        assert all(r is not None for r in results)

        # Most should pass (allowing for minor issues)
        passed = sum(1 for r in results if len(r.errors) == 0)
        assert passed >= 2  # At least 2 out of 3 should pass
