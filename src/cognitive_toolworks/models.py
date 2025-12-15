"""
Data models for Cognitive Toolworks.

These models define the structure of skills, analysis reports, and configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Platform(str, Enum):
    """Target platform for skill generation."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    UNIVERSAL = "universal"  # Compatible with both

    def __str__(self) -> str:
        return self.value


class SourceType(str, Enum):
    """Type of source to generate from."""

    MCP_SERVER = "mcp"
    OPENAPI = "openapi"
    README = "readme"
    SCRIPT = "script"
    DOCUMENTATION = "docs"

    def __str__(self) -> str:
        return self.value


@dataclass
class SkillMetadata:
    """
    YAML frontmatter for SKILL.md.

    Follows Anthropic's Agent Skills specification:
    - name: max 64 chars, lowercase + hyphens
    - description: max 200 chars for Anthropic, 1024 for internal
    """

    name: str
    description: str
    category: str | None = None
    allowed_tools: list[str] | None = None
    dependencies: list[str] | None = None
    version: str = "1.0.0"
    license: str | None = None

    def validate_anthropic(self) -> list[str]:
        """Validate against Anthropic spec, returning list of issues."""
        issues = []

        # Name validation
        if len(self.name) > 64:
            issues.append(f"name exceeds 64 chars: {len(self.name)}")
        if not self.name.replace("-", "").replace("_", "").isalnum():
            issues.append("name must be lowercase letters, numbers, and hyphens")
        if self.name != self.name.lower():
            issues.append("name must be lowercase")

        # Description validation
        if len(self.description) > 200:
            issues.append(f"description exceeds 200 chars: {len(self.description)}")
        if "<" in self.description or ">" in self.description:
            issues.append("description cannot contain XML tags")

        return issues

    def validate_openai(self) -> list[str]:
        """Validate against OpenAI Codex CLI spec."""
        issues = []

        if len(self.name) > 64:
            issues.append(f"name exceeds 64 chars: {len(self.name)}")

        if len(self.description) > 1024:
            issues.append(f"description exceeds 1024 chars: {len(self.description)}")

        return issues

    def to_yaml(self) -> str:
        """Convert to YAML frontmatter string."""
        lines = ["---"]
        lines.append(f"name: {self.name}")
        lines.append(f'description: "{self.description}"')

        if self.allowed_tools:
            lines.append(f"allowed-tools: {', '.join(self.allowed_tools)}")

        if self.dependencies:
            lines.append("dependencies:")
            for dep in self.dependencies:
                lines.append(f"  - {dep}")

        if self.license:
            lines.append(f"license: {self.license}")

        lines.append("---")
        return "\n".join(lines)


@dataclass
class SkillContent:
    """
    Full skill content structure.

    Represents all levels of progressive disclosure:
    - Level 1: metadata (frontmatter)
    - Level 2: main content (SKILL.md body)
    - Level 3: references (separate files)
    """

    metadata: SkillMetadata
    overview: str
    when_to_use: list[str]
    quick_reference: str
    instructions: str
    examples: list[dict[str, Any]]
    guidelines: list[str]
    troubleshooting: list[dict[str, str]] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Convert to full SKILL.md content."""
        lines = [self.metadata.to_yaml(), ""]

        # Title and overview
        lines.append(f"# {self.metadata.name.replace('-', ' ').title()}")
        lines.append("")
        lines.append(self.overview)
        lines.append("")

        # When to use
        lines.append("## When to Use This Skill")
        lines.append("")
        for item in self.when_to_use:
            lines.append(f"- {item}")
        lines.append("")

        # Quick reference
        lines.append("## Quick Reference")
        lines.append("")
        lines.append(self.quick_reference)
        lines.append("")

        # Main instructions
        lines.append("## Instructions")
        lines.append("")
        lines.append(self.instructions)
        lines.append("")

        # Examples
        if self.examples:
            lines.append("## Examples")
            lines.append("")
            for i, example in enumerate(self.examples, 1):
                lines.append(f"### Example {i}: {example.get('title', 'Example')}")
                lines.append("")
                if "description" in example:
                    lines.append(example["description"])
                    lines.append("")
                if "code" in example:
                    lines.append("```" + example.get("language", "bash"))
                    lines.append(example["code"])
                    lines.append("```")
                    lines.append("")

        # Guidelines
        if self.guidelines:
            lines.append("## Guidelines")
            lines.append("")
            for guideline in self.guidelines:
                lines.append(f"- {guideline}")
            lines.append("")

        # Troubleshooting
        if self.troubleshooting:
            lines.append("## Troubleshooting")
            lines.append("")
            for item in self.troubleshooting:
                lines.append(f"### {item.get('issue', 'Issue')}")
                lines.append(item.get("solution", ""))
                lines.append("")

        # References
        if self.references:
            lines.append("## See Also")
            lines.append("")
            for ref in self.references:
                lines.append(f"- {ref}")
            lines.append("")

        return "\n".join(lines)


@dataclass
class AgentsConfig:
    """
    AGENTS.md structure.

    Follows the AGENTS.md specification from OpenAI/AAIF.
    """

    project_overview: str
    dev_environment: dict[str, Any]
    testing_instructions: dict[str, Any]
    pr_instructions: dict[str, Any]
    coding_conventions: dict[str, Any]
    project_specific: dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Convert to AGENTS.md content."""
        lines = ["# AGENTS.md", ""]

        # Overview
        lines.append("## Project Overview")
        lines.append("")
        lines.append(self.project_overview)
        lines.append("")

        # Dev environment
        lines.append("## Dev Environment")
        lines.append("")
        if "setup" in self.dev_environment:
            lines.append("### Setup")
            lines.append("```bash")
            lines.append(self.dev_environment["setup"])
            lines.append("```")
            lines.append("")
        if "directories" in self.dev_environment:
            lines.append("### Key Directories")
            for path, desc in self.dev_environment["directories"].items():
                lines.append(f"- `{path}` - {desc}")
            lines.append("")

        # Testing
        lines.append("## Testing Instructions")
        lines.append("")
        if "commands" in self.testing_instructions:
            lines.append("```bash")
            for cmd in self.testing_instructions["commands"]:
                lines.append(cmd)
            lines.append("```")
            lines.append("")
        if "requirements" in self.testing_instructions:
            lines.append("### Requirements")
            for req in self.testing_instructions["requirements"]:
                lines.append(f"- {req}")
            lines.append("")

        # PR instructions
        lines.append("## PR Instructions")
        lines.append("")
        if "title_format" in self.pr_instructions:
            lines.append(f"**Title Format**: `{self.pr_instructions['title_format']}`")
            lines.append("")
        if "checklist" in self.pr_instructions:
            lines.append("### Checklist")
            for item in self.pr_instructions["checklist"]:
                lines.append(f"- [ ] {item}")
            lines.append("")

        # Coding conventions
        lines.append("## Coding Conventions")
        lines.append("")
        for key, value in self.coding_conventions.items():
            if isinstance(value, list):
                lines.append(f"### {key.replace('_', ' ').title()}")
                for item in value:
                    lines.append(f"- {item}")
                lines.append("")
            else:
                lines.append(f"- **{key}**: {value}")
        lines.append("")

        return "\n".join(lines)


@dataclass
class AnalysisReport:
    """
    Quality analysis output.

    Contains metrics and recommendations for skill improvement.
    """

    # Token metrics
    total_tokens: int
    level1_tokens: int  # Metadata
    level2_tokens: int  # Main body
    level3_tokens: int  # References

    # Quality scores (0-1)
    token_efficiency: float
    progressive_disclosure_score: float
    coverage_score: float

    # Security
    security_issues: list[str]
    security_score: float

    # Compatibility
    anthropic_compatible: bool
    anthropic_issues: list[str]
    openai_compatible: bool
    openai_issues: list[str]

    # Recommendations
    recommendations: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "tokens": {
                "total": self.total_tokens,
                "level1": self.level1_tokens,
                "level2": self.level2_tokens,
                "level3": self.level3_tokens,
            },
            "scores": {
                "token_efficiency": self.token_efficiency,
                "progressive_disclosure": self.progressive_disclosure_score,
                "coverage": self.coverage_score,
                "security": self.security_score,
            },
            "security": {
                "issues": self.security_issues,
                "score": self.security_score,
            },
            "compatibility": {
                "anthropic": {
                    "compatible": self.anthropic_compatible,
                    "issues": self.anthropic_issues,
                },
                "openai": {
                    "compatible": self.openai_compatible,
                    "issues": self.openai_issues,
                },
            },
            "recommendations": self.recommendations,
        }

    @property
    def passed(self) -> bool:
        """Check if skill passes all validations."""
        return (
            self.anthropic_compatible
            and self.openai_compatible
            and len(self.security_issues) == 0
            and self.token_efficiency >= 0.7
        )


@dataclass
class MCPToolDefinition:
    """Definition of an MCP tool from introspection."""

    name: str
    description: str
    input_schema: dict[str, Any]
    required_params: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "required_params": self.required_params,
        }


@dataclass
class MCPAnalysis:
    """Analysis result from MCP server introspection."""

    server_name: str
    tools: list[MCPToolDefinition]
    resources: list[dict[str, Any]]
    capabilities: list[str]
    semantic_analysis: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "server_name": self.server_name,
            "tools": [t.to_dict() for t in self.tools],
            "resources": self.resources,
            "capabilities": self.capabilities,
            "semantic_analysis": self.semantic_analysis,
        }


@dataclass
class SemanticAnalysis:
    """Semantic analysis of source material."""

    purpose: str
    tool_categories: dict[str, list[str]]
    workflows: list[dict[str, Any]]
    error_scenarios: list[str]
    security_considerations: list[str]
    recommended_use_cases: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "purpose": self.purpose,
            "tool_categories": self.tool_categories,
            "workflows": self.workflows,
            "error_scenarios": self.error_scenarios,
            "security_considerations": self.security_considerations,
            "recommended_use_cases": self.recommended_use_cases,
        }
