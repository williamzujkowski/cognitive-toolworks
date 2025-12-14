"""
SKILL.md Generator.

LLM-powered generation of skill files with progressive disclosure,
token budget enforcement, and cross-platform support.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, PackageLoader, select_autoescape

from cognitive_toolworks.llm.client import LLMClient
from cognitive_toolworks.llm.prompts import get_prompt
from cognitive_toolworks.models import (
    MCPAnalysis,
    Platform,
    SemanticAnalysis,
    SkillContent,
    SkillMetadata,
)

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class GenerationConfig:
    """Configuration for skill generation."""

    platform: Platform = Platform.UNIVERSAL
    level1_token_budget: int = 100  # Metadata only
    level2_token_budget: int = 5000  # Main SKILL.md body
    num_examples: int = 3
    optimize: bool = True
    include_troubleshooting: bool = True


class SkillGenerator:
    """
    Generates SKILL.md files from source analysis.

    Supports:
    - MCP server analysis
    - OpenAPI spec analysis
    - README analysis
    - Direct semantic analysis

    Uses LLM for intelligent content generation with progressive disclosure.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        config: GenerationConfig | None = None,
    ) -> None:
        self.llm = llm_client or LLMClient()
        self.config = config or GenerationConfig()

        # Setup Jinja2 environment
        self._jinja_env = Environment(
            loader=PackageLoader("cognitive_toolworks", "templates"),
            autoescape=select_autoescape(default=False),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    async def generate_from_mcp(
        self,
        analysis: MCPAnalysis,
        name: str | None = None,
    ) -> SkillContent:
        """
        Generate a skill from MCP server analysis.

        Args:
            analysis: MCPAnalysis from introspection.
            name: Optional skill name (auto-generated if not provided).

        Returns:
            SkillContent with full skill structure.
        """
        # First, perform semantic analysis
        semantic = await self._semantic_analysis(analysis)

        # Generate skill content
        skill = await self._generate_skill(
            semantic=semantic,
            name=name or self._derive_name(analysis.server_name),
            source_type="mcp",
            source_data=analysis.to_dict(),
        )

        return skill

    async def generate_from_semantic(
        self,
        semantic: SemanticAnalysis,
        name: str,
        source_type: str = "custom",
    ) -> SkillContent:
        """
        Generate a skill from pre-computed semantic analysis.

        Args:
            semantic: SemanticAnalysis with purpose, workflows, etc.
            name: Skill name.
            source_type: Type of source this came from.

        Returns:
            SkillContent with full skill structure.
        """
        return await self._generate_skill(
            semantic=semantic,
            name=name,
            source_type=source_type,
            source_data={},
        )

    async def _semantic_analysis(self, analysis: MCPAnalysis) -> SemanticAnalysis:
        """Perform LLM-powered semantic analysis of MCP server."""
        prompt = get_prompt("semantic_analysis").format(
            tools_json=json.dumps([t.to_dict() for t in analysis.tools], indent=2),
            resources_json=json.dumps(analysis.resources, indent=2),
        )
        system = get_prompt("semantic_analysis_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system, json_output=True)

        data = response.as_json

        return SemanticAnalysis(
            purpose=data.get("purpose", ""),
            tool_categories=data.get("tool_categories", {}),
            workflows=data.get("workflows", []),
            error_scenarios=data.get("error_scenarios", []),
            security_considerations=data.get("security_considerations", []),
            recommended_use_cases=data.get("recommended_use_cases", []),
        )

    async def _generate_skill(
        self,
        semantic: SemanticAnalysis,
        name: str,
        _source_type: str,
        _source_data: dict[str, Any],
    ) -> SkillContent:
        """Generate skill content using LLM."""
        prompt = get_prompt("skill_generation").format(
            analysis_json=json.dumps(semantic.to_dict(), indent=2),
            platform=self.config.platform.value,
            level2_budget=self.config.level2_token_budget,
        )
        system = get_prompt("skill_generation_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system)

        # Parse the generated markdown into SkillContent
        skill = self._parse_skill_markdown(response.content, name)

        # Generate examples if needed
        if len(skill.examples) < self.config.num_examples:
            examples = await self._generate_examples(semantic, skill)
            skill.examples.extend(examples)

        return skill

    async def _generate_examples(
        self,
        semantic: SemanticAnalysis,
        skill: SkillContent,
    ) -> list[dict[str, Any]]:
        """Generate additional examples using LLM."""
        prompt = get_prompt("example_generation").format(
            count=self.config.num_examples - len(skill.examples),
            skill_overview=skill.overview,
            tools_json=json.dumps(list(semantic.tool_categories.keys()), indent=2),
            workflows_json=json.dumps(semantic.workflows, indent=2),
        )
        system = get_prompt("example_generation_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system, json_output=True)

        return response.as_json

    def _parse_skill_markdown(self, content: str, name: str) -> SkillContent:
        """Parse generated markdown into SkillContent structure."""
        # Extract frontmatter
        lines = content.split("\n")
        metadata = self._extract_frontmatter(lines)

        # If no metadata in generated content, create default
        if not metadata:
            metadata = SkillMetadata(
                name=name,
                description=f"Auto-generated skill for {name}",
            )

        # Extract sections
        overview = self._extract_section(content, ["# ", "## Overview"])
        when_to_use = self._extract_list_section(content, "When to Use")
        quick_ref = self._extract_section(content, "Quick Reference")
        instructions = self._extract_section(
            content, ["Instructions", "Workflows", "Detailed"]
        )
        examples = self._extract_examples(content)
        guidelines = self._extract_list_section(content, "Guidelines")
        troubleshooting = self._extract_troubleshooting(content)

        return SkillContent(
            metadata=metadata,
            overview=overview or f"{name} skill for intelligent automation.",
            when_to_use=when_to_use or [f"Use {name} for automation tasks"],
            quick_reference=quick_ref or "",
            instructions=instructions or "",
            examples=examples,
            guidelines=guidelines or [],
            troubleshooting=troubleshooting,
        )

    def _extract_frontmatter(self, lines: list[str]) -> SkillMetadata | None:
        """Extract YAML frontmatter from lines."""
        if not lines or lines[0].strip() != "---":
            return None

        frontmatter_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            frontmatter_lines.append(line)

        if not frontmatter_lines:
            return None

        # Parse simple YAML
        data: dict[str, Any] = {}
        for line in frontmatter_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip().strip('"').strip("'")

        return SkillMetadata(
            name=data.get("name", "unnamed-skill"),
            description=data.get("description", ""),
            allowed_tools=(
                data.get("allowed-tools", "").split(", ")
                if data.get("allowed-tools")
                else None
            ),
        )

    def _extract_section(self, content: str, headers: str | list[str]) -> str:
        """Extract content under a section header."""
        if isinstance(headers, str):
            headers = [headers]

        lines = content.split("\n")
        in_section = False
        section_lines: list[str] = []

        for line in lines:
            # Check if we've hit a new section
            if line.startswith("## ") or line.startswith("# "):
                if in_section:
                    break  # End of our section
                # Check if this is our section
                for header in headers:
                    if header.lower() in line.lower():
                        in_section = True
                        break
            elif in_section:
                section_lines.append(line)

        return "\n".join(section_lines).strip()

    def _extract_list_section(self, content: str, header: str) -> list[str]:
        """Extract a bulleted list section."""
        section = self._extract_section(content, header)
        items = []

        for line in section.split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                items.append(line[2:])

        return items

    def _extract_examples(self, content: str) -> list[dict[str, Any]]:
        """Extract examples from content."""
        examples: list[dict[str, Any]] = []
        section = self._extract_section(content, "Example")

        if not section:
            return examples

        # Split by ### headers
        current_example: dict[str, Any] = {}
        current_code = []
        in_code_block = False
        code_language = ""

        for line in section.split("\n"):
            if line.startswith("### "):
                if current_example:
                    if current_code:
                        current_example["code"] = "\n".join(current_code)
                        current_example["language"] = code_language or "bash"
                    examples.append(current_example)
                current_example = {"title": line[4:].strip()}
                current_code = []
                in_code_block = False
            elif line.startswith("```"):
                if in_code_block:
                    in_code_block = False
                else:
                    in_code_block = True
                    code_language = line[3:].strip()
            elif in_code_block:
                current_code.append(line)
            elif current_example and not current_example.get("description"):
                if line.strip():
                    current_example["description"] = line.strip()

        if current_example:
            if current_code:
                current_example["code"] = "\n".join(current_code)
                current_example["language"] = code_language or "bash"
            examples.append(current_example)

        return examples

    def _extract_troubleshooting(self, content: str) -> list[dict[str, str]]:
        """Extract troubleshooting items."""
        items: list[dict[str, str]] = []
        section = self._extract_section(content, "Troubleshooting")

        if not section:
            return items

        current_item: dict[str, str] = {}

        for line in section.split("\n"):
            if line.startswith("### "):
                if current_item:
                    items.append(current_item)
                current_item = {"issue": line[4:].strip(), "solution": ""}
            elif current_item and line.strip():
                current_item["solution"] += line + "\n"

        if current_item:
            current_item["solution"] = current_item["solution"].strip()
            items.append(current_item)

        return items

    def _derive_name(self, server_name: str) -> str:
        """Derive a skill name from server name."""
        # Clean up common prefixes
        name = server_name.lower()
        for prefix in ["@modelcontextprotocol/server-", "server-", "mcp-"]:
            if name.startswith(prefix):
                name = name[len(prefix) :]

        # Convert to kebab-case
        name = name.replace("_", "-").replace(" ", "-")

        return name

    def render_skill(self, skill: SkillContent) -> str:
        """Render SkillContent to markdown string."""
        return skill.to_markdown()

    def save_skill(self, skill: SkillContent, output_dir: Path) -> Path:
        """Save skill to output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_path = output_dir / "SKILL.md"
        skill_path.write_text(self.render_skill(skill))

        # Create examples directory if needed
        if skill.examples:
            examples_dir = output_dir / "examples"
            examples_dir.mkdir(exist_ok=True)

        return skill_path
