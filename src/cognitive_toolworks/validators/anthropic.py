"""
Anthropic SKILL.md specification validator.

Validates skills against Anthropic's Agent Skills specification:
- Name format (lowercase, hyphens, max 64 chars)
- Description length (max 200 chars)
- Required sections
- Token budgets
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

import yaml

from cognitive_toolworks.analyzers.tokens import count_tokens

if TYPE_CHECKING:
    from pathlib import Path


class ValidationSeverity(str, Enum):
    """Severity of validation issues."""

    ERROR = "error"  # Blocks compliance
    WARNING = "warning"  # Should fix
    INFO = "info"  # Suggestion


@dataclass
class ValidationIssue:
    """A validation issue found in a skill."""

    severity: ValidationSeverity
    field: str
    message: str
    fix_suggestion: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "severity": self.severity.value,
            "field": self.field,
            "message": self.message,
            "fix": self.fix_suggestion,
        }


@dataclass
class ValidationResult:
    """Result of validation."""

    passed: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def errors(self) -> list[ValidationIssue]:
        """Get only error-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Get only warning-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "passed": self.passed,
            "issues": [i.to_dict() for i in self.issues],
            "metadata": self.metadata,
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "info": len(
                    [i for i in self.issues if i.severity == ValidationSeverity.INFO]
                ),
            },
        }


class AnthropicValidator:
    """
    Validates skills against Anthropic's specification.

    Spec requirements:
    - name: max 64 chars, lowercase, alphanumeric + hyphens
    - description: max 200 chars, no XML tags
    - allowed-tools: optional but recommended
    - Level 2 tokens: recommended < 5000
    """

    # Anthropic spec limits
    NAME_MAX_LENGTH = 64
    DESCRIPTION_MAX_LENGTH = 200
    LEVEL2_TOKEN_BUDGET = 5000

    # Required frontmatter fields
    REQUIRED_FIELDS: ClassVar[list[str]] = ["name", "description"]

    # Recommended frontmatter fields
    RECOMMENDED_FIELDS: ClassVar[list[str]] = ["allowed-tools"]

    def validate(self, content: str) -> ValidationResult:
        """
        Validate skill content against Anthropic spec.

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
                    fix_suggestion="Add frontmatter starting with --- and ending with ---",
                )
            )
            return ValidationResult(passed=False, issues=issues)

        metadata["frontmatter"] = frontmatter

        # Validate name
        issues.extend(self._validate_name(frontmatter.get("name")))

        # Validate description
        issues.extend(self._validate_description(frontmatter.get("description")))

        # Validate allowed-tools
        issues.extend(self._validate_allowed_tools(frontmatter.get("allowed-tools")))

        # Validate token budget
        token_issues, token_count = self._validate_tokens(content)
        issues.extend(token_issues)
        metadata["token_count"] = token_count

        # Check for required sections
        issues.extend(self._validate_sections(content))

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
                    fix_suggestion=f"Shorten name to {self.NAME_MAX_LENGTH} characters or less",
                )
            )

        # Format check (lowercase, alphanumeric, hyphens)
        if not re.match(r"^[a-z0-9-]+$", name):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="name",
                    message="name must be lowercase letters, numbers, and hyphens only",
                    fix_suggestion=f"Use: {self._fix_name(name)}",
                )
            )

        # No consecutive hyphens
        if "--" in name:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="name",
                    message="name should not contain consecutive hyphens",
                    fix_suggestion=name.replace("--", "-"),
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

        # Length check
        if len(description) > self.DESCRIPTION_MAX_LENGTH:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="description",
                    message=f"description exceeds {self.DESCRIPTION_MAX_LENGTH} chars ({len(description)})",
                    fix_suggestion="Shorten description to include key trigger phrases only",
                )
            )

        # No XML tags
        if "<" in description or ">" in description:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="description",
                    message="description cannot contain XML/HTML tags",
                    fix_suggestion="Remove < and > characters",
                )
            )

        # Should include trigger phrases
        trigger_words = ["use when", "for", "helps", "enables", "allows"]
        has_trigger = any(word in description.lower() for word in trigger_words)
        if not has_trigger:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="description",
                    message="description should include trigger phrases (e.g., 'Use when...')",
                )
            )

        return issues

    def _validate_allowed_tools(
        self, allowed_tools: str | list | None
    ) -> list[ValidationIssue]:
        """Validate allowed-tools configuration."""
        issues: list[ValidationIssue] = []

        if not allowed_tools:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="allowed-tools",
                    message="Consider adding allowed-tools to restrict tool access",
                )
            )
            return issues

        # Parse if string
        if isinstance(allowed_tools, str):
            tools = [t.strip() for t in allowed_tools.split(",")]
        else:
            tools = allowed_tools

        # Check for wildcards
        if "*" in tools or any("*" in t for t in tools):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="allowed-tools",
                    message="Wildcards in allowed-tools may grant excessive permissions",
                )
            )

        return issues

    def _validate_tokens(self, content: str) -> tuple[list[ValidationIssue], int]:
        """Validate token budget."""
        issues: list[ValidationIssue] = []

        # Extract body (after frontmatter)
        lines = content.split("\n")
        body_start = 0
        in_frontmatter = False

        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    body_start = i + 1
                    break

        body = "\n".join(lines[body_start:])
        token_count = count_tokens(body)

        if token_count > self.LEVEL2_TOKEN_BUDGET:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="tokens",
                    message=f"Level 2 content exceeds recommended {self.LEVEL2_TOKEN_BUDGET} tokens ({token_count})",
                    fix_suggestion="Move detailed content to reference files",
                )
            )
        elif token_count > self.LEVEL2_TOKEN_BUDGET * 0.9:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="tokens",
                    message=f"Level 2 content approaching token budget ({token_count}/{self.LEVEL2_TOKEN_BUDGET})",
                )
            )

        return issues, token_count

    def _validate_sections(self, content: str) -> list[ValidationIssue]:
        """Validate required sections are present."""
        issues: list[ValidationIssue] = []
        content_lower = content.lower()

        # Check for overview/purpose
        if "## overview" not in content_lower and "# " not in content[:500].lower():
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="sections",
                    message="Missing Overview section",
                    fix_suggestion="Add ## Overview section after frontmatter",
                )
            )

        # Check for when to use
        if "when to use" not in content_lower:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="sections",
                    message="Missing 'When to Use' section",
                    fix_suggestion="Add ## When to Use This Skill section with trigger conditions",
                )
            )

        # Check for examples
        if "## example" not in content_lower and "### example" not in content_lower:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="sections",
                    message="No Examples section found",
                    fix_suggestion="Add 2-3 concrete examples",
                )
            )

        return issues

    def _fix_name(self, name: str) -> str:
        """Attempt to fix an invalid name."""
        # Convert to lowercase
        fixed = name.lower()
        # Replace spaces and underscores with hyphens
        fixed = re.sub(r"[\s_]+", "-", fixed)
        # Remove invalid characters
        fixed = re.sub(r"[^a-z0-9-]", "", fixed)
        # Remove consecutive hyphens
        fixed = re.sub(r"-+", "-", fixed)
        # Trim hyphens from ends
        fixed = fixed.strip("-")
        # Truncate if needed
        if len(fixed) > self.NAME_MAX_LENGTH:
            fixed = fixed[: self.NAME_MAX_LENGTH].rstrip("-")
        return fixed

    def auto_fix(self, content: str) -> str:
        """
        Attempt to auto-fix common validation issues.

        Args:
            content: The SKILL.md content.

        Returns:
            Fixed content (best effort).
        """
        lines = content.split("\n")
        fixed_lines: list[str] = []
        in_frontmatter = False
        frontmatter_done = False

        for line in lines:
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    frontmatter_done = True
                fixed_lines.append(line)
                continue

            if in_frontmatter and not frontmatter_done:
                # Fix name line
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                    fixed_name = self._fix_name(name)
                    fixed_lines.append(f"name: {fixed_name}")
                    continue

                # Fix description line
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                    # Remove XML tags
                    desc = re.sub(r"<[^>]+>", "", desc)
                    # Truncate if needed
                    if len(desc) > self.DESCRIPTION_MAX_LENGTH:
                        desc = desc[: self.DESCRIPTION_MAX_LENGTH - 3] + "..."
                    fixed_lines.append(f'description: "{desc}"')
                    continue

            fixed_lines.append(line)

        return "\n".join(fixed_lines)
