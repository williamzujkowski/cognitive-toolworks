"""
Structure optimizer.

Improves skill organization, readability, and LLM consumption
using LLM-powered analysis and restructuring.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cognitive_toolworks.analyzers.tokens import count_tokens
from cognitive_toolworks.llm.client import LLMClient
from cognitive_toolworks.optimizers.progressive import OptimizationResult

if TYPE_CHECKING:
    from cognitive_toolworks.models import SkillContent


class StructureOptimizer:
    """
    Optimizer for skill structure and readability.

    Uses LLM to:
    1. Improve section organization
    2. Enhance readability (headings, lists, code blocks)
    3. Optimize for LLM consumption (clear triggers, imperative voice)
    4. Ensure consistent formatting
    """

    SYSTEM_PROMPT = """You are an expert at optimizing technical documentation structure
for both human readability and LLM consumption. Your goal is to:

1. Organize sections logically (general to specific)
2. Use clear, descriptive headings
3. Employ imperative voice for instructions
4. Optimize formatting (lists, tables, code blocks)
5. Ensure progressive disclosure (quick reference before details)
6. Add clear trigger phrases for LLM routing

Maintain technical accuracy while improving clarity and structure."""

    ANALYSIS_PROMPT = """# Structure Analysis

Analyze this skill's structure and recommend improvements.

## Current Skill Content
{content}

## Evaluation Criteria

1. **Section Organization**: Logical flow, proper ordering
2. **Readability**: Clear headings, appropriate formatting
3. **LLM Optimization**: Trigger phrases, imperative voice, scannable structure
4. **Consistency**: Uniform formatting, consistent style
5. **Progressive Disclosure**: Quick reference before detailed content

## Task

Provide a JSON response with:

1. **structure_issues**: Problems with current organization
2. **readability_issues**: Formatting or clarity problems
3. **llm_optimization_issues**: Things that hinder LLM consumption
4. **recommended_restructuring**: How to reorganize sections
5. **formatting_improvements**: Specific formatting changes
6. **voice_corrections**: Passive to imperative conversions

Output format:
```json
{{
  "structure_issues": [
    {{"issue": "Examples appear before procedure", "severity": "medium", "fix": "Move examples after instructions"}}
  ],
  "readability_issues": [
    {{"issue": "Long paragraphs in instructions", "severity": "low", "fix": "Break into numbered steps or bullet points"}}
  ],
  "llm_optimization_issues": [
    {{"issue": "Missing clear trigger phrases in When to Use", "severity": "high", "fix": "Add explicit trigger patterns"}}
  ],
  "recommended_restructuring": [
    {{"current_order": ["Overview", "Examples", "Instructions"], "recommended_order": ["Overview", "When to Use", "Quick Reference", "Instructions", "Examples"]}},
    {{"action": "split", "section": "Long Instructions", "into": ["Basic Workflow", "Advanced Options"]}}
  ],
  "formatting_improvements": [
    {{"section": "Instructions", "change": "Convert paragraph to numbered steps"}},
    {{"section": "Commands", "change": "Use code blocks with syntax highlighting"}},
    {{"section": "Options", "change": "Convert to table for scanability"}}
  ],
  "voice_corrections": [
    {{"original": "You can run this command", "corrected": "Run this command"}},
    {{"original": "This will create a file", "corrected": "Creates a file"}}
  ],
  "estimated_improvement": "30% better LLM routing, 25% faster human comprehension"
}}
```"""

    RESTRUCTURE_PROMPT = """# Skill Restructuring

Restructure this skill following the optimization plan.

## Original Skill
{original_content}

## Structure Plan
{structure_plan}

## Requirements

1. **Organization**: Follow recommended section order
2. **Formatting**: Apply all formatting improvements
3. **Voice**: Use imperative voice throughout instructions
4. **Clarity**: Clear headings, scannable structure
5. **Triggers**: Explicit trigger phrases in "When to Use"
6. **Code Blocks**: Syntax highlighting, clear examples
7. **Lists**: Use bullets for options, numbers for steps
8. **Tables**: Use for parameter references, comparisons

## Style Guide

- Headings: Descriptive, action-oriented (e.g., "When to Use This Skill")
- Instructions: Imperative voice (e.g., "Run command", "Set variable")
- Lists: Parallel structure, consistent formatting
- Code: Syntax highlighting, comments for complex parts
- Examples: Title, description, code, expected output

Output the restructured SKILL.md content in markdown format."""

    def __init__(self, client: LLMClient | None = None, dry_run: bool = False) -> None:
        """
        Initialize the optimizer.

        Args:
            client: LLM client for analysis. If None, creates default client.
            dry_run: If True, analyze but don't modify content.
        """
        self.client = client or LLMClient()
        self.dry_run = dry_run

    async def optimize(self, skill: SkillContent) -> OptimizationResult:
        """
        Optimize a skill's structure and readability.

        Args:
            skill: The skill to optimize.

        Returns:
            OptimizationResult with metrics and optimized skill.
        """
        # Get original content and token count
        original_content = skill.to_markdown()
        original_tokens = count_tokens(original_content)

        changes_made: list[str] = []

        # Step 1: Analyze the structure
        changes_made.append("Analyzing skill structure with LLM")
        analysis_prompt = self.ANALYSIS_PROMPT.format(content=original_content)

        async with self.client as client:
            analysis_response = await client.generate(
                prompt=analysis_prompt,
                system=self.SYSTEM_PROMPT,
                json_output=True,
            )

            structure_plan = analysis_response.as_json

            # Log identified issues
            for issue in structure_plan.get("structure_issues", []):
                changes_made.append(f"Structure issue: {issue.get('issue')}")

            for issue in structure_plan.get("readability_issues", []):
                changes_made.append(f"Readability issue: {issue.get('issue')}")

            for issue in structure_plan.get("llm_optimization_issues", []):
                changes_made.append(f"LLM optimization: {issue.get('issue')}")

            # Step 2: Restructure the skill if not dry run
            if self.dry_run:
                changes_made.append(
                    "Dry run - analysis only, no restructuring performed"
                )
                return OptimizationResult(
                    original_tokens=original_tokens,
                    optimized_tokens=original_tokens,
                    changes_made=changes_made,
                    optimized_skill=skill,
                )

            # Perform the restructuring
            changes_made.append("Restructuring skill with optimizations")
            restructure_prompt = self.RESTRUCTURE_PROMPT.format(
                original_content=original_content,
                structure_plan=str(structure_plan),
            )

            restructure_response = await client.generate(
                prompt=restructure_prompt,
                system=self.SYSTEM_PROMPT,
            )

            optimized_content = restructure_response.content
            optimized_tokens = count_tokens(optimized_content)

            # Parse the optimized markdown back into SkillContent
            optimized_skill = self._parse_optimized_skill(optimized_content, skill)

            # Calculate token change
            token_diff = optimized_tokens - original_tokens
            if token_diff > 0:
                changes_made.append(
                    f"Restructuring added {token_diff} tokens for clarity "
                    f"(from {original_tokens} to {optimized_tokens})"
                )
            elif token_diff < 0:
                changes_made.append(
                    f"Restructuring reduced {-token_diff} tokens "
                    f"(from {original_tokens} to {optimized_tokens})"
                )
            else:
                changes_made.append("Restructuring maintained token count")

            return OptimizationResult(
                original_tokens=original_tokens,
                optimized_tokens=optimized_tokens,
                changes_made=changes_made,
                optimized_skill=optimized_skill,
            )

    def _parse_optimized_skill(
        self, optimized_content: str, original_skill: SkillContent
    ) -> SkillContent:
        """
        Parse optimized markdown back into SkillContent.

        This is a simplified parser. In production, use a proper markdown parser.

        Args:
            optimized_content: The optimized markdown content.
            original_skill: The original skill (for fallback values).

        Returns:
            Updated SkillContent.
        """
        # For now, preserve the original structure but update key fields
        # A real implementation would parse the markdown properly
        # This is a placeholder that maintains type safety

        from cognitive_toolworks.models import SkillContent

        # Split into sections
        sections = optimized_content.split("\n## ")

        # Extract overview (text before first section)
        parts = sections[0].split("\n# ")
        overview = parts[-1].strip() if len(parts) > 1 else original_skill.overview

        # Update the skill content (simplified)
        return SkillContent(
            metadata=original_skill.metadata,
            overview=overview,
            when_to_use=original_skill.when_to_use,
            quick_reference=original_skill.quick_reference,
            instructions=original_skill.instructions,
            examples=original_skill.examples,
            guidelines=original_skill.guidelines,
            troubleshooting=original_skill.troubleshooting,
            references=original_skill.references,
            scripts=original_skill.scripts,
        )

    async def analyze_only(self, skill: SkillContent) -> dict[str, object]:
        """
        Analyze a skill's structure without optimizing it.

        Args:
            skill: The skill to analyze.

        Returns:
            Dictionary with analysis results.
        """
        original_content = skill.to_markdown()
        original_tokens = count_tokens(original_content)

        analysis_prompt = self.ANALYSIS_PROMPT.format(content=original_content)

        async with self.client as client:
            analysis_response = await client.generate(
                prompt=analysis_prompt,
                system=self.SYSTEM_PROMPT,
                json_output=True,
            )

            return {
                "original_tokens": original_tokens,
                "analysis": analysis_response.as_json,
                "total_issues": len(
                    analysis_response.as_json.get("structure_issues", [])
                )
                + len(analysis_response.as_json.get("readability_issues", []))
                + len(analysis_response.as_json.get("llm_optimization_issues", [])),
            }
