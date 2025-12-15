"""
Cross-platform compatibility checking for skills.

Analyzes skills for compatibility across Anthropic and OpenAI platforms.
Checks for:
- Description length limits (Anthropic: 200 chars, OpenAI: 1024 chars)
- Name format requirements
- Allowed tools format differences
- YAML frontmatter compatibility
- Instruction formatting differences
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import yaml

from cognitive_toolworks.models import (
    CompatibilityIssue,
    CompatibilityReport,
    CompatibilitySeverity,
    Platform,
    SkillContent,
    SkillMetadata,
)

if TYPE_CHECKING:
    from pathlib import Path


class CompatibilityChecker:
    """
    Analyzes skills for cross-platform compatibility.

    Checks compatibility between Anthropic Agent Skills and OpenAI Codex CLI
    skill formats.
    """

    # Platform limits
    ANTHROPIC_NAME_MAX = 64
    ANTHROPIC_DESCRIPTION_MAX = 200
    OPENAI_NAME_MAX = 64
    OPENAI_DESCRIPTION_MAX = 1024

    def __init__(self) -> None:
        """Initialize compatibility checker."""
        pass

    def analyze(
        self, content: str | SkillContent | SkillMetadata
    ) -> CompatibilityReport:
        """
        Analyze content for cross-platform compatibility.

        Args:
            content: SKILL.md content, SkillContent, or SkillMetadata.

        Returns:
            CompatibilityReport with compatibility status and issues.
        """
        if isinstance(content, str):
            # Parse from markdown string
            metadata = self._extract_metadata(content)
            body = content
        elif isinstance(content, SkillContent):
            # Extract from SkillContent
            metadata = content.metadata
            body = content.to_markdown()
        elif isinstance(content, SkillMetadata):
            # Use metadata directly
            metadata = content
            body = ""
        else:
            raise TypeError(f"Unsupported content type: {type(content)}")

        issues: list[CompatibilityIssue] = []
        recommendations: list[str] = []

        # Check Anthropic compatibility
        anthropic_issues = self._check_anthropic_compatibility(metadata, body)
        issues.extend(anthropic_issues)

        # Check OpenAI compatibility
        openai_issues = self._check_openai_compatibility(metadata, body)
        issues.extend(openai_issues)

        # Determine compatibility status
        is_anthropic_compatible = not any(
            i.platform == Platform.ANTHROPIC
            and i.severity == CompatibilitySeverity.ERROR
            for i in issues
        )

        is_openai_compatible = not any(
            i.platform == Platform.OPENAI and i.severity == CompatibilitySeverity.ERROR
            for i in issues
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            issues, is_anthropic_compatible, is_openai_compatible
        )

        return CompatibilityReport(
            is_anthropic_compatible=is_anthropic_compatible,
            is_openai_compatible=is_openai_compatible,
            issues=issues,
            recommendations=recommendations,
        )

    def analyze_file(self, path: Path) -> CompatibilityReport:
        """
        Analyze a SKILL.md file for compatibility.

        Args:
            path: Path to SKILL.md file.

        Returns:
            CompatibilityReport.
        """
        content = path.read_text()
        return self.analyze(content)

    def _extract_metadata(self, content: str) -> SkillMetadata:
        """Extract metadata from SKILL.md content."""
        lines = content.split("\n")

        if not lines or lines[0].strip() != "---":
            # No frontmatter, create minimal metadata
            return SkillMetadata(name="unknown", description="")

        frontmatter_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            frontmatter_lines.append(line)

        if not frontmatter_lines:
            return SkillMetadata(name="unknown", description="")

        try:
            fm = yaml.safe_load("\n".join(frontmatter_lines))
            if not isinstance(fm, dict):
                return SkillMetadata(name="unknown", description="")

            # Parse allowed-tools (can be string or list)
            allowed_tools = fm.get("allowed-tools")
            if isinstance(allowed_tools, str):
                allowed_tools = [t.strip() for t in allowed_tools.split(",")]
            elif not isinstance(allowed_tools, list):
                allowed_tools = None

            return SkillMetadata(
                name=fm.get("name", "unknown"),
                description=fm.get("description", ""),
                category=fm.get("category"),
                allowed_tools=allowed_tools,
                dependencies=fm.get("dependencies"),
                version=fm.get("version", "1.0.0"),
                license=fm.get("license"),
            )
        except yaml.YAMLError:
            return SkillMetadata(name="unknown", description="")

    def _check_anthropic_compatibility(
        self, metadata: SkillMetadata, body: str  # noqa: ARG002
    ) -> list[CompatibilityIssue]:
        """Check compatibility with Anthropic Agent Skills spec."""
        issues: list[CompatibilityIssue] = []

        # Check name length
        if len(metadata.name) > self.ANTHROPIC_NAME_MAX:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.ANTHROPIC,
                    field="name",
                    message=f"Name exceeds Anthropic limit of {self.ANTHROPIC_NAME_MAX} chars ({len(metadata.name)})",
                    fix_suggestion=f"Shorten name to {self.ANTHROPIC_NAME_MAX} characters or less",
                )
            )

        # Check name format (lowercase, alphanumeric, hyphens)
        if not re.match(r"^[a-z0-9-]+$", metadata.name):
            fixed_name = self._fix_name(metadata.name)
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.ANTHROPIC,
                    field="name",
                    message="Name must be lowercase letters, numbers, and hyphens only",
                    fix_suggestion=f"Use: {fixed_name}",
                )
            )

        # Check description length
        if len(metadata.description) > self.ANTHROPIC_DESCRIPTION_MAX:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.ANTHROPIC,
                    field="description",
                    message=f"Description exceeds Anthropic limit of {self.ANTHROPIC_DESCRIPTION_MAX} chars ({len(metadata.description)})",
                    fix_suggestion=f"Shorten description to {self.ANTHROPIC_DESCRIPTION_MAX} characters or less",
                )
            )

        # Check for XML tags in description (not allowed by Anthropic)
        if "<" in metadata.description or ">" in metadata.description:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.ANTHROPIC,
                    field="description",
                    message="Description cannot contain XML/HTML tags (Anthropic requirement)",
                    fix_suggestion="Remove < and > characters from description",
                )
            )

        # Check for consecutive hyphens in name
        if "--" in metadata.name:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.WARNING,
                    platform=Platform.ANTHROPIC,
                    field="name",
                    message="Name should not contain consecutive hyphens",
                    fix_suggestion=metadata.name.replace("--", "-"),
                )
            )

        # Check allowed-tools format (Anthropic prefers explicit list)
        if metadata.allowed_tools and "*" in str(metadata.allowed_tools):
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.WARNING,
                    platform=Platform.ANTHROPIC,
                    field="allowed-tools",
                    message="Wildcards in allowed-tools may grant excessive permissions",
                    fix_suggestion="Explicitly list required tools instead of using wildcards",
                )
            )

        return issues

    def _check_openai_compatibility(
        self, metadata: SkillMetadata, body: str  # noqa: ARG002
    ) -> list[CompatibilityIssue]:
        """Check compatibility with OpenAI Codex CLI spec."""
        issues: list[CompatibilityIssue] = []

        # Check name length
        if len(metadata.name) > self.OPENAI_NAME_MAX:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.OPENAI,
                    field="name",
                    message=f"Name exceeds OpenAI limit of {self.OPENAI_NAME_MAX} chars ({len(metadata.name)})",
                    fix_suggestion=f"Shorten name to {self.OPENAI_NAME_MAX} characters or less",
                )
            )

        # Check description length
        if len(metadata.description) > self.OPENAI_DESCRIPTION_MAX:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.ERROR,
                    platform=Platform.OPENAI,
                    field="description",
                    message=f"Description exceeds OpenAI limit of {self.OPENAI_DESCRIPTION_MAX} chars ({len(metadata.description)})",
                    fix_suggestion=f"Shorten description to {self.OPENAI_DESCRIPTION_MAX} characters or less",
                )
            )

        # OpenAI recommends category field
        if not metadata.category:
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.INFO,
                    platform=Platform.OPENAI,
                    field="category",
                    message="OpenAI Codex CLI recommends including a category field",
                    fix_suggestion="Add category field (e.g., 'development', 'data', 'security')",
                )
            )

        # OpenAI includes version in frontmatter
        if not metadata.version or metadata.version == "1.0.0":
            issues.append(
                CompatibilityIssue(
                    severity=CompatibilitySeverity.INFO,
                    platform=Platform.OPENAI,
                    field="version",
                    message="OpenAI format typically includes explicit version",
                    fix_suggestion="Add or update version field in frontmatter",
                )
            )

        return issues

    def _generate_recommendations(
        self,
        issues: list[CompatibilityIssue],
        is_anthropic_compatible: bool,
        is_openai_compatible: bool,
    ) -> list[str]:
        """Generate actionable recommendations based on issues."""
        recommendations: list[str] = []

        # If already universal, add confirmation message
        if is_anthropic_compatible and is_openai_compatible:
            recommendations.append(
                "Skill is compatible with both Anthropic and OpenAI platforms"
            )
            # Still return any INFO-level suggestions
            return recommendations

        # Platform-specific recommendations
        if not is_anthropic_compatible:
            # Check for description length issue
            desc_issues = [
                i
                for i in issues
                if i.platform == Platform.ANTHROPIC
                and i.field == "description"
                and i.severity == CompatibilitySeverity.ERROR
            ]
            if desc_issues:
                recommendations.append(
                    f"Shorten description to {self.ANTHROPIC_DESCRIPTION_MAX} characters for Anthropic compatibility"
                )

            # Check for name format issues
            name_issues = [
                i
                for i in issues
                if i.platform == Platform.ANTHROPIC
                and i.field == "name"
                and i.severity == CompatibilitySeverity.ERROR
            ]
            if name_issues:
                recommendations.append(
                    "Use lowercase letters, numbers, and hyphens only in skill name"
                )

        if not is_openai_compatible:
            # Check for OpenAI-specific issues
            desc_issues = [
                i
                for i in issues
                if i.platform == Platform.OPENAI
                and i.field == "description"
                and i.severity == CompatibilitySeverity.ERROR
            ]
            if desc_issues:
                recommendations.append(
                    f"Shorten description to {self.OPENAI_DESCRIPTION_MAX} characters for OpenAI compatibility"
                )

        # Generic recommendations based on warnings
        warning_count = len(
            [i for i in issues if i.severity == CompatibilitySeverity.WARNING]
        )
        if warning_count > 0:
            recommendations.append(
                f"Address {warning_count} warning(s) to improve cross-platform compatibility"
            )

        # Recommendation for universal compatibility
        if is_anthropic_compatible and not is_openai_compatible:
            recommendations.append(
                "Skill is Anthropic-compatible; address OpenAI issues for universal compatibility"
            )
        elif is_openai_compatible and not is_anthropic_compatible:
            recommendations.append(
                "Skill is OpenAI-compatible; address Anthropic issues for universal compatibility"
            )
        elif not is_anthropic_compatible and not is_openai_compatible:
            recommendations.append(
                "Skill has compatibility issues with both platforms; address errors first"
            )

        return recommendations

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
        if len(fixed) > self.ANTHROPIC_NAME_MAX:
            fixed = fixed[: self.ANTHROPIC_NAME_MAX].rstrip("-")
        return fixed
