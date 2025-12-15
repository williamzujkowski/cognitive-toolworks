"""
Token counting and efficiency analysis.

Uses tiktoken for accurate token counting with Claude's tokenizer.
Provides efficiency scoring based on content-to-token ratio.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import tiktoken

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class TokenMetrics:
    """Token metrics for a skill."""

    total_tokens: int
    level1_tokens: int  # Frontmatter/metadata
    level2_tokens: int  # Main body
    level3_tokens: int  # References

    # Efficiency metrics
    efficiency_score: float  # 0-1, higher is better
    content_density: float  # Useful content / total tokens

    # Budget compliance
    level1_over_budget: bool
    level2_over_budget: bool

    @property
    def passed_budget(self) -> bool:
        """Check if skill passes token budgets."""
        return not self.level1_over_budget and not self.level2_over_budget


class TokenAnalyzer:
    """
    Analyzes token usage and efficiency in skills.

    Uses tiktoken with cl100k_base encoding (Claude's tokenizer)
    to provide accurate token counts.
    """

    # Default token budgets (from Anthropic spec)
    LEVEL1_BUDGET = 100  # Metadata only
    LEVEL2_BUDGET = 5000  # Main SKILL.md body
    LEVEL3_BUDGET = float("inf")  # Unbounded for references

    def __init__(
        self,
        level1_budget: int = LEVEL1_BUDGET,
        level2_budget: int = LEVEL2_BUDGET,
    ) -> None:
        self.level1_budget = level1_budget
        self.level2_budget = level2_budget
        self._encoder = tiktoken.get_encoding("cl100k_base")

    def analyze(self, content: str, references_dir: Path | None = None) -> TokenMetrics:
        """
        Analyze token usage in a skill.

        Args:
            content: The SKILL.md content.
            references_dir: Optional path to references directory.

        Returns:
            TokenMetrics with counts and efficiency scores.
        """
        # Split content into levels
        level1, level2 = self._split_levels(content)

        level1_tokens = self._count_tokens(level1)
        level2_tokens = self._count_tokens(level2)

        # Count references if provided
        level3_tokens = 0
        if references_dir and references_dir.exists():
            for ref_file in references_dir.glob("*.md"):
                level3_tokens += self._count_tokens(ref_file.read_text())

        total_tokens = level1_tokens + level2_tokens + level3_tokens

        # Calculate efficiency
        efficiency_score = self._calculate_efficiency(content, level2_tokens)
        content_density = self._calculate_density(content, total_tokens)

        return TokenMetrics(
            total_tokens=total_tokens,
            level1_tokens=level1_tokens,
            level2_tokens=level2_tokens,
            level3_tokens=level3_tokens,
            efficiency_score=efficiency_score,
            content_density=content_density,
            level1_over_budget=level1_tokens > self.level1_budget,
            level2_over_budget=level2_tokens > self.level2_budget,
        )

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken."""
        return len(self._encoder.encode(text))

    def _split_levels(self, content: str) -> tuple[str, str]:
        """Split content into Level 1 (frontmatter) and Level 2 (body)."""
        lines = content.split("\n")

        # Find frontmatter
        if not lines or lines[0].strip() != "---":
            return "", content

        frontmatter_end = -1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                frontmatter_end = i
                break

        if frontmatter_end == -1:
            return "", content

        level1 = "\n".join(lines[: frontmatter_end + 1])
        level2 = "\n".join(lines[frontmatter_end + 1 :])

        return level1, level2

    def _calculate_efficiency(self, content: str, body_tokens: int) -> float:
        """
        Calculate token efficiency score.

        Factors:
        - Proximity to budget (closer is better, under is required)
        - Code block ratio (code is dense, good)
        - List usage (lists are efficient)
        - Redundancy detection
        """
        if body_tokens == 0:
            return 0.0

        score = 1.0

        # Budget proximity (being under budget is good, way under is wasteful)
        budget_ratio = body_tokens / self.level2_budget
        if budget_ratio > 1.0:
            # Over budget: penalize heavily
            score *= max(0.0, 1.0 - (budget_ratio - 1.0) * 2)
        elif budget_ratio < 0.3:
            # Way under budget: might be missing content
            score *= 0.8
        else:
            # Good range
            score *= 1.0

        # Code block bonus (code is information-dense)
        code_blocks = content.count("```")
        if code_blocks > 0:
            score *= min(1.1, 1.0 + code_blocks * 0.02)

        # List efficiency (lists are compact)
        list_lines = sum(
            1 for line in content.split("\n") if line.strip().startswith(("-", "*", "1."))
        )
        total_lines = len([line for line in content.split("\n") if line.strip()])
        if total_lines > 0:
            list_ratio = list_lines / total_lines
            score *= 1.0 + list_ratio * 0.1

        # Redundancy penalty
        redundancy = self._detect_redundancy(content)
        score *= 1.0 - redundancy * 0.3

        return min(1.0, max(0.0, score))

    def _calculate_density(self, content: str, total_tokens: int) -> float:
        """Calculate content density (useful content / total)."""
        if total_tokens == 0:
            return 0.0

        # Count "useful" content indicators
        useful_indicators = 0

        # Code blocks are highly useful
        useful_indicators += content.count("```") * 50

        # Commands are useful
        useful_indicators += content.count("$ ") * 20

        # Lists are useful
        useful_indicators += (
            sum(1 for line in content.split("\n") if line.strip().startswith(("-", "*"))) * 5
        )

        # Headers structure content
        useful_indicators += (
            sum(1 for line in content.split("\n") if line.strip().startswith("#")) * 10
        )

        # Normalize by total tokens
        return min(1.0, useful_indicators / total_tokens)

    def _detect_redundancy(self, content: str) -> float:
        """Detect redundant content (0-1 score, higher = more redundant)."""
        lines = [line.strip().lower() for line in content.split("\n") if line.strip()]

        if len(lines) < 2:
            return 0.0

        # Check for duplicate or near-duplicate lines
        seen = set()
        duplicates = 0

        for line in lines:
            # Skip very short lines
            if len(line) < 10:
                continue

            # Check for exact duplicates
            if line in seen:
                duplicates += 1
            seen.add(line)

        return min(1.0, duplicates / len(lines))


def count_tokens(text: str) -> int:
    """
    Quick token count utility function.

    Args:
        text: The text to count tokens in.

    Returns:
        Number of tokens.
    """
    try:
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))
    except Exception:
        # Fallback to rough estimate
        return len(text) // 4
