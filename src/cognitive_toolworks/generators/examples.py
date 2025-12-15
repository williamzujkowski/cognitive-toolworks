"""
Example Generator Module.

LLM-powered generation of skill examples with quality validation
and platform-specific formatting.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

from cognitive_toolworks.llm.client import LLMClient
from cognitive_toolworks.llm.prompts import get_prompt

if TYPE_CHECKING:
    from cognitive_toolworks.models import SemanticAnalysis, SkillContent


class ExampleComplexity(str, Enum):
    """Complexity level for generated examples."""

    SIMPLE = "simple"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EDGE_CASE = "edge_case"


@dataclass
class Example:
    """A single skill example."""

    title: str
    description: str
    code: str
    language: str = "bash"
    user_intent: str = ""
    expected_output: str = ""
    complexity: ExampleComplexity = ExampleComplexity.SIMPLE
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "code": self.code,
            "language": self.language,
            "user_intent": self.user_intent,
            "expected_output": self.expected_output,
            "complexity": self.complexity.value,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Example:
        """Create from dictionary."""
        complexity = data.get("complexity", "simple")
        if isinstance(complexity, str):
            complexity = ExampleComplexity(complexity)

        return cls(
            title=data.get("title", "Untitled Example"),
            description=data.get("description", ""),
            code=data.get("code", ""),
            language=data.get("language", "bash"),
            user_intent=data.get("user_intent", ""),
            expected_output=data.get("expected_output", ""),
            complexity=complexity,
            tags=data.get("tags", []),
        )

    def is_valid(self) -> bool:
        """Check if example has minimum required fields."""
        return bool(self.title and self.code)

    def token_estimate(self) -> int:
        """Estimate token count for this example."""
        # Rough estimate: 1 token per 4 characters
        total_chars = (
            len(self.title)
            + len(self.description)
            + len(self.code)
            + len(self.user_intent)
            + len(self.expected_output)
        )
        return total_chars // 4


@dataclass
class ExampleSet:
    """A collection of examples with metadata."""

    examples: list[Example] = field(default_factory=list)
    skill_name: str = ""
    total_tokens: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_name": self.skill_name,
            "examples": [e.to_dict() for e in self.examples],
            "total_tokens": self.total_tokens,
        }

    def add_example(self, example: Example) -> None:
        """Add an example to the set."""
        self.examples.append(example)
        self.total_tokens += example.token_estimate()

    def filter_by_complexity(self, complexity: ExampleComplexity) -> list[Example]:
        """Filter examples by complexity level."""
        return [e for e in self.examples if e.complexity == complexity]

    def validate_all(self) -> tuple[bool, list[str]]:
        """Validate all examples and return issues."""
        issues = []
        for i, example in enumerate(self.examples):
            if not example.is_valid():
                issues.append(
                    f"Example {i + 1} ({example.title}): missing required fields"
                )
            if len(example.code) < 10:
                issues.append(f"Example {i + 1} ({example.title}): code too short")
            if not example.description:
                issues.append(f"Example {i + 1} ({example.title}): missing description")

        return len(issues) == 0, issues


@dataclass
class ExampleGenerationConfig:
    """Configuration for example generation."""

    num_examples: int = 3
    include_simple: bool = True
    include_intermediate: bool = True
    include_advanced: bool = False
    include_edge_case: bool = True
    max_tokens_per_example: int = 200
    default_language: str = "bash"


class ExampleGenerator:
    """
    Generates skill examples using LLM.

    Supports:
    - Generation from semantic analysis
    - Generation from existing skill content
    - Quality validation
    - Platform-specific formatting
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        config: ExampleGenerationConfig | None = None,
    ) -> None:
        self.llm = llm_client or LLMClient()
        self.config = config or ExampleGenerationConfig()

    async def generate_from_semantic(
        self,
        semantic: SemanticAnalysis,
        skill_overview: str = "",
    ) -> ExampleSet:
        """
        Generate examples from semantic analysis.

        Args:
            semantic: SemanticAnalysis with purpose, workflows, etc.
            skill_overview: Optional skill overview for context.

        Returns:
            ExampleSet with generated examples.
        """
        prompt = get_prompt("example_generation").format(
            count=self.config.num_examples,
            skill_overview=skill_overview or semantic.purpose,
            tools_json=json.dumps(list(semantic.tool_categories.keys()), indent=2),
            workflows_json=json.dumps(
                [
                    w if isinstance(w, dict) else {"name": str(w)}
                    for w in semantic.workflows
                ],
                indent=2,
            ),
        )
        system = get_prompt("example_generation_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system, json_output=True)

        examples = self._parse_examples(response.as_json)

        example_set = ExampleSet(skill_name=skill_overview)
        for example in examples:
            example_set.add_example(example)

        return example_set

    async def generate_from_skill(
        self,
        skill: SkillContent,
    ) -> ExampleSet:
        """
        Generate additional examples for an existing skill.

        Args:
            skill: SkillContent to generate examples for.

        Returns:
            ExampleSet with generated examples.
        """
        # Build context from skill content
        context = f"""
Skill Name: {skill.metadata.name}
Description: {skill.metadata.description}
Overview: {skill.overview}

When to Use:
{chr(10).join('- ' + item for item in skill.when_to_use)}

Existing Examples: {len(skill.examples)}
"""

        prompt = f"""Generate {self.config.num_examples} new examples for this skill.

{context}

Requirements:
- Examples should be different from any existing ones
- Cover diverse use cases
- Include at least one edge case
- Keep each example under {self.config.max_tokens_per_example} tokens

Output as JSON array of example objects with:
- title: Example title
- description: What this demonstrates
- code: The command/code
- language: Programming language
- user_intent: What user wants to accomplish
- expected_output: Expected result
- complexity: simple|intermediate|advanced|edge_case
"""

        system = get_prompt("example_generation_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system, json_output=True)

        examples = self._parse_examples(response.as_json)

        example_set = ExampleSet(skill_name=skill.metadata.name)
        for example in examples:
            example_set.add_example(example)

        return example_set

    async def enhance_example(
        self,
        example: Example,
        add_output: bool = True,
        add_explanation: bool = True,
    ) -> Example:
        """
        Enhance an existing example with more details.

        Args:
            example: Example to enhance.
            add_output: Add expected output if missing.
            add_explanation: Add detailed description.

        Returns:
            Enhanced Example.
        """
        enhancements_needed = []
        if add_output and not example.expected_output:
            enhancements_needed.append("expected output")
        if add_explanation and len(example.description) < 50:
            enhancements_needed.append("detailed explanation")

        if not enhancements_needed:
            return example

        prompt = f"""Enhance this skill example by adding: {', '.join(enhancements_needed)}

Title: {example.title}
Code:
```{example.language}
{example.code}
```
Current Description: {example.description}

Output as JSON with all fields including the enhancements."""

        async with self.llm:
            response = await self.llm.generate(
                prompt,
                system="You are an expert at writing clear, educational code examples.",
                json_output=True,
            )

        data = response.as_json
        if isinstance(data, dict):
            return Example(
                title=data.get("title", example.title),
                description=data.get("description", example.description),
                code=data.get("code", example.code),
                language=data.get("language", example.language),
                user_intent=data.get("user_intent", example.user_intent),
                expected_output=data.get("expected_output", example.expected_output),
                complexity=example.complexity,
                tags=data.get("tags", example.tags),
            )

        return example

    def validate_examples(
        self,
        examples: list[Example] | ExampleSet,
    ) -> tuple[bool, list[str]]:
        """
        Validate a list of examples.

        Args:
            examples: Examples to validate.

        Returns:
            Tuple of (all_valid, list_of_issues).
        """
        if isinstance(examples, ExampleSet):
            return examples.validate_all()

        issues: list[str] = []
        for i, example in enumerate(examples):
            if not example.is_valid():
                issues.append(
                    f"Example {i + 1} ({example.title}): missing required fields"
                )
            if len(example.code) < 10:
                issues.append(f"Example {i + 1} ({example.title}): code too short")
            if not example.description:
                issues.append(f"Example {i + 1} ({example.title}): missing description")

        return len(issues) == 0, issues

    def format_for_skill_md(
        self,
        examples: list[Example] | ExampleSet,
    ) -> str:
        """
        Format examples for inclusion in SKILL.md.

        Args:
            examples: Examples to format.

        Returns:
            Markdown-formatted examples section.
        """
        example_list = (
            examples.examples if isinstance(examples, ExampleSet) else examples
        )

        if not example_list:
            return ""

        lines = ["## Examples", ""]

        for example in example_list:
            lines.append(f"### {example.title}")
            lines.append("")
            if example.description:
                lines.append(example.description)
                lines.append("")
            lines.append(f"```{example.language}")
            lines.append(example.code)
            lines.append("```")
            if example.expected_output:
                lines.append("")
                lines.append("**Expected output:**")
                lines.append("```")
                lines.append(example.expected_output)
                lines.append("```")
            lines.append("")

        return "\n".join(lines)

    def _parse_examples(self, data: Any) -> list[Example]:
        """Parse LLM response into Example objects."""
        examples: list[Example] = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    examples.append(Example.from_dict(item))
        elif isinstance(data, dict):
            # Single example
            examples.append(Example.from_dict(data))

        # Assign complexity based on index if not set
        complexities = [
            ExampleComplexity.SIMPLE,
            ExampleComplexity.INTERMEDIATE,
            ExampleComplexity.ADVANCED,
            ExampleComplexity.EDGE_CASE,
        ]
        for i, example in enumerate(examples):
            if example.complexity == ExampleComplexity.SIMPLE and i > 0:
                example.complexity = complexities[min(i, len(complexities) - 1)]

        return examples


def create_example(
    title: str,
    code: str,
    description: str = "",
    language: str = "bash",
    **kwargs: Any,
) -> Example:
    """
    Convenience function to create an example.

    Args:
        title: Example title.
        code: The code/command.
        description: What this demonstrates.
        language: Programming language.
        **kwargs: Additional Example fields.

    Returns:
        Example instance.
    """
    return Example(
        title=title,
        description=description,
        code=code,
        language=language,
        user_intent=kwargs.get("user_intent", ""),
        expected_output=kwargs.get("expected_output", ""),
        complexity=kwargs.get("complexity", ExampleComplexity.SIMPLE),
        tags=kwargs.get("tags", []),
    )
