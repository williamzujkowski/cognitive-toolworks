"""
OpenAI Skills (Codex CLI) specification validator.

Validates skills against OpenAI's format:
- Name format (max 64 chars)
- Description length (max 1024 chars)
- Required sections
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

import yaml

from cognitive_toolworks.validators.anthropic import (
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)

if TYPE_CHECKING:
    from pathlib import Path


class OpenAIValidator:
    """
    Validates skills against OpenAI Codex CLI specification.

    Spec requirements:
    - name: max 64 chars
    - description: max 1024 chars
    - Stored in ~/.codex/skills/
    """

    # OpenAI spec limits (more permissive than Anthropic)
    NAME_MAX_LENGTH = 64
    DESCRIPTION_MAX_LENGTH = 1024

    # Required frontmatter fields
    REQUIRED_FIELDS: ClassVar[list[str]] = ["name", "description"]

    def validate(self, content: str) -> ValidationResult:
        """
        Validate skill content against OpenAI spec.

        Args:
            content: The SKILL.md content.

        Returns:
            ValidationResult with pass/fail and issues.
        """
        issues: list[ValidationIssue] = []
        metadata: dict = {}

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)

        if frontmatter is None:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="frontmatter",
                    message="Missing or invalid YAML frontmatter",
                )
            )
            return ValidationResult(passed=False, issues=issues)

        metadata["frontmatter"] = frontmatter

        # Validate name
        issues.extend(self._validate_name(frontmatter.get("name")))

        # Validate description
        issues.extend(self._validate_description(frontmatter.get("description")))

        # Check for category (recommended for Codex)
        if not frontmatter.get("category"):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="category",
                    message="Consider adding a category for better organization in Codex",
                )
            )

        # Determine pass/fail
        passed = not any(i.severity == ValidationSeverity.ERROR for i in issues)

        return ValidationResult(passed=passed, issues=issues, metadata=metadata)

    def validate_file(self, path: Path) -> ValidationResult:
        """Validate a SKILL.md file."""
        content = path.read_text()
        return self.validate(content)

    def _extract_frontmatter(self, content: str) -> dict | None:
        """Extract YAML frontmatter from content."""
        lines = content.split("\n")

        if not lines or lines[0].strip() != "---":
            return None

        frontmatter_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            frontmatter_lines.append(line)

        if not frontmatter_lines:
            return None

        try:
            return yaml.safe_load("\n".join(frontmatter_lines))
        except yaml.YAMLError:
            return None

    def _validate_name(self, name: str | None) -> list[ValidationIssue]:
        """Validate the skill name."""
        issues: list[ValidationIssue] = []

        if not name:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="name",
                    message="name is required",
                )
            )
            return issues

        # Length check
        if len(name) > self.NAME_MAX_LENGTH:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="name",
                    message=f"name exceeds {self.NAME_MAX_LENGTH} chars ({len(name)})",
                )
            )

        # OpenAI is more permissive but still recommend lowercase
        if name != name.lower():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="name",
                    message="Consider using lowercase name for cross-platform compatibility",
                )
            )

        return issues

    def _validate_description(self, description: str | None) -> list[ValidationIssue]:
        """Validate the skill description."""
        issues: list[ValidationIssue] = []

        if not description:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="description",
                    message="description is required",
                )
            )
            return issues

        # Length check (OpenAI allows longer)
        if len(description) > self.DESCRIPTION_MAX_LENGTH:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="description",
                    message=f"description exceeds {self.DESCRIPTION_MAX_LENGTH} chars ({len(description)})",
                )
            )

        return issues


def validate_cross_platform(content: str) -> dict[str, ValidationResult]:
    """
    Validate skill against both Anthropic and OpenAI specs.

    Args:
        content: The SKILL.md content.

    Returns:
        Dictionary with results for each platform.
    """
    from cognitive_toolworks.validators.anthropic import AnthropicValidator

    return {
        "anthropic": AnthropicValidator().validate(content),
        "openai": OpenAIValidator().validate(content),
    }
