"""
Progressive disclosure optimizer.

Restructures skill content into T1/T2/T3 tiers using LLM intelligence
to identify what belongs in each tier and move verbose content to references.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from cognitive_toolworks.analyzers.tokens import count_tokens
from cognitive_toolworks.llm.client import LLMClient

if TYPE_CHECKING:
    from cognitive_toolworks.models import SkillContent


# Token budgets per tier (from CLAUDE.md)
T1_BUDGET = 2000  # Fast path, 80% of requests
T2_BUDGET = 6000  # Extended validation
T3_BUDGET = 12000  # Deep research


@dataclass
class OptimizationResult:
    """
    Result of skill optimization.

    Contains metrics and the optimized skill content.
    """

    original_tokens: int
    optimized_tokens: int
    changes_made: list[str]
    optimized_skill: SkillContent

    @property
    def reduction_percentage(self) -> float:
        """Calculate percentage reduction in tokens."""
        if self.original_tokens == 0:
            return 0.0
        reduction = self.original_tokens - self.optimized_tokens
        return (reduction / self.original_tokens) * 100

    @property
    def within_budget(self) -> bool:
        """Check if optimized skill is within T2 budget."""
        return self.optimized_tokens <= T2_BUDGET


class ProgressiveDisclosureOptimizer:
    """
    Optimizer for progressive disclosure structure.

    Uses LLM to:
    1. Identify content that should be in T1 (frontmatter + triggers)
    2. Identify content that should be in T2 (core procedures)
    3. Move verbose content to T3 (references)
    """

    # LLM prompts for optimization
    SYSTEM_PROMPT = """You are an expert at optimizing agent skills for progressive disclosure.
Your goal is to restructure skills into three tiers:

T1 (≤2k tokens): Metadata, purpose, triggers, quick reference
T2 (≤6k tokens): Core procedures, decision rules, common examples
T3 (≤12k tokens): Detailed references, advanced examples, deep dive content

Analyze the skill and identify:
1. What stays in main SKILL.md (T1+T2)
2. What moves to reference files (T3)
3. Redundant or verbose content to remove
4. How to make the content more concise

Always preserve accuracy and technical correctness."""

    ANALYSIS_PROMPT = """# Progressive Disclosure Analysis

Analyze this skill and recommend how to structure it into T1/T2/T3 tiers.

## Current Skill Content
{content}

## Current Token Count
{current_tokens} tokens

## Target Budget
T1+T2 combined: ≤6000 tokens (ideally ≤5000)

## Task
Provide a JSON response with:

1. **tier_assignments**: For each section, specify T1, T2, or T3
2. **content_to_move**: List of content blocks to move to reference files
3. **content_to_condense**: List of sections that can be made more concise
4. **content_to_remove**: List of redundant/unnecessary content
5. **recommended_changes**: Specific actionable changes

Output format:
```json
{{
  "tier_assignments": {{
    "frontmatter": "T1",
    "purpose": "T1",
    "when_to_use": "T1",
    "quick_reference": "T1",
    "procedure": "T2",
    "examples": "T2",
    "advanced_examples": "T3",
    "detailed_reference": "T3"
  }},
  "content_to_move": [
    {{"section": "advanced_examples", "reason": "Complex edge cases", "target": "advanced.md"}},
    {{"section": "detailed_api_reference", "reason": "Verbose specs", "target": "api-reference.md"}}
  ],
  "content_to_condense": [
    {{"section": "instructions", "current_tokens": 2000, "target_tokens": 1000, "strategy": "Remove filler, use imperative voice, consolidate examples"}}
  ],
  "content_to_remove": [
    {{"section": "obvious_troubleshooting", "reason": "Redundant with examples"}}
  ],
  "recommended_changes": [
    "Convert passive voice to imperative in instructions",
    "Merge similar examples 2 and 3",
    "Move detailed API schemas to reference file",
    "Remove 'Introduction' section - covered in Purpose",
    "Use table format for command options instead of verbose list"
  ],
  "estimated_tokens_after": 4800
}}
```"""

    REWRITE_PROMPT = """# Skill Rewrite for Progressive Disclosure

Rewrite this skill following the optimization plan.

## Original Skill
{original_content}

## Optimization Plan
{optimization_plan}

## Requirements
1. Apply all recommended changes
2. Maintain technical accuracy
3. Keep T1+T2 sections under 6000 tokens
4. Use concise, imperative language
5. Preserve all critical information
6. Move verbose content to references (indicate with "[See reference.md]")

Output the optimized SKILL.md content in markdown format."""

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
        Optimize a skill for progressive disclosure.

        Args:
            skill: The skill to optimize.

        Returns:
            OptimizationResult with metrics and optimized skill.
        """
        # Get original content and token count
        original_content = skill.to_markdown()
        original_tokens = count_tokens(original_content)

        changes_made: list[str] = []

        # If already under budget, return as-is
        if original_tokens <= T2_BUDGET:
            changes_made.append(f"Skill already within T2 budget ({original_tokens} tokens)")
            return OptimizationResult(
                original_tokens=original_tokens,
                optimized_tokens=original_tokens,
                changes_made=changes_made,
                optimized_skill=skill,
            )

        # Step 1: Analyze the skill
        changes_made.append("Analyzing skill structure with LLM")
        analysis_prompt = self.ANALYSIS_PROMPT.format(
            content=original_content,
            current_tokens=original_tokens,
        )

        async with self.client as client:
            analysis_response = await client.generate(
                prompt=analysis_prompt,
                system=self.SYSTEM_PROMPT,
                json_output=True,
            )

            optimization_plan = analysis_response.as_json

            # Log recommended changes
            for change in optimization_plan.get("recommended_changes", []):
                changes_made.append(f"Recommended: {change}")

            # Step 2: Rewrite the skill if not dry run
            if self.dry_run:
                changes_made.append("Dry run - analysis only, no rewrite performed")
                return OptimizationResult(
                    original_tokens=original_tokens,
                    optimized_tokens=optimization_plan.get(
                        "estimated_tokens_after", original_tokens
                    ),
                    changes_made=changes_made,
                    optimized_skill=skill,
                )

            # Perform the rewrite
            changes_made.append("Rewriting skill with optimizations")
            rewrite_prompt = self.REWRITE_PROMPT.format(
                original_content=original_content,
                optimization_plan=str(optimization_plan),
            )

            rewrite_response = await client.generate(
                prompt=rewrite_prompt,
                system=self.SYSTEM_PROMPT,
            )

            optimized_content = rewrite_response.content
            optimized_tokens = count_tokens(optimized_content)

            # Parse the optimized markdown back into SkillContent
            # For now, we'll create a simplified version
            # In production, you'd want a proper markdown parser
            optimized_skill = self._parse_optimized_skill(optimized_content, skill)

            changes_made.append(
                f"Reduced from {original_tokens} to {optimized_tokens} tokens "
                f"({((original_tokens - optimized_tokens) / original_tokens * 100):.1f}% reduction)"
            )

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
        from cognitive_toolworks.models import SkillContent

        # For now, preserve the original structure but update key fields
        # A real implementation would parse the markdown properly
        # This is a placeholder that maintains type safety

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
        Analyze a skill without optimizing it.

        Args:
            skill: The skill to analyze.

        Returns:
            Dictionary with analysis results.
        """
        original_content = skill.to_markdown()
        original_tokens = count_tokens(original_content)

        analysis_prompt = self.ANALYSIS_PROMPT.format(
            content=original_content,
            current_tokens=original_tokens,
        )

        async with self.client as client:
            analysis_response = await client.generate(
                prompt=analysis_prompt,
                system=self.SYSTEM_PROMPT,
                json_output=True,
            )

            return {
                "original_tokens": original_tokens,
                "analysis": analysis_response.as_json,
                "over_budget": original_tokens > T2_BUDGET,
                "budget_difference": original_tokens - T2_BUDGET,
            }
