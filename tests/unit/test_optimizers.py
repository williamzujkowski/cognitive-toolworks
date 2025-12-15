"""
Tests for LLM-powered skill optimizers.

Tests both ProgressiveDisclosureOptimizer and StructureOptimizer
with mocked LLM calls.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from cognitive_toolworks.llm.client import LLMResponse
from cognitive_toolworks.models import SkillContent, SkillMetadata
from cognitive_toolworks.optimizers import (
    OptimizationResult,
    ProgressiveDisclosureOptimizer,
    StructureOptimizer,
)
from cognitive_toolworks.optimizers.progressive import T1_BUDGET, T2_BUDGET, T3_BUDGET


@pytest.fixture
def sample_skill() -> SkillContent:
    """Create a sample skill for testing."""
    metadata = SkillMetadata(
        name="test-skill",
        description="A test skill for optimizer testing",
        category="testing",
        version="1.0.0",
    )

    return SkillContent(
        metadata=metadata,
        overview="This is a test skill used for testing the optimizer functionality.",
        when_to_use=[
            "When you need to test optimizers",
            "When validating LLM-powered restructuring",
        ],
        quick_reference="Run `test-command` to test.",
        instructions="Step 1: Do this.\nStep 2: Do that.\nStep 3: Complete the task.",
        examples=[
            {
                "title": "Basic Example",
                "description": "A simple test example",
                "code": "test-command --flag",
                "language": "bash",
            }
        ],
        guidelines=["Always test thoroughly", "Follow best practices"],
        troubleshooting=[{"issue": "Command fails", "solution": "Check your inputs"}],
        references=["https://example.com/docs"],
    )


@pytest.fixture
def large_skill() -> SkillContent:
    """Create a large skill that exceeds T2 budget."""
    metadata = SkillMetadata(
        name="large-test-skill",
        description="A large test skill that exceeds token budgets",
        category="testing",
        version="1.0.0",
    )

    # Create verbose content that will exceed T2_BUDGET
    verbose_instructions = "\n\n".join(
        [
            f"Step {i}: " + " ".join(["This is verbose content."] * 50)
            for i in range(1, 100)
        ]
    )

    return SkillContent(
        metadata=metadata,
        overview="This is a large test skill with verbose content. " * 20,
        when_to_use=[f"Use case {i}" for i in range(1, 50)],
        quick_reference="Lots of commands here. " * 100,
        instructions=verbose_instructions,
        examples=[
            {
                "title": f"Example {i}",
                "description": "A verbose example " * 20,
                "code": "test-command " * 50,
                "language": "bash",
            }
            for i in range(1, 20)
        ],
        guidelines=[f"Guideline {i}: " + "Follow this. " * 10 for i in range(1, 30)],
        troubleshooting=[
            {"issue": f"Issue {i}", "solution": "Long solution. " * 20}
            for i in range(1, 20)
        ],
    )


class TestOptimizationResult:
    """Tests for OptimizationResult dataclass."""

    def test_reduction_percentage(self) -> None:
        """Test reduction percentage calculation."""
        result = OptimizationResult(
            original_tokens=1000,
            optimized_tokens=750,
            changes_made=["Reduced content"],
            optimized_skill=MagicMock(),
        )

        assert result.reduction_percentage == 25.0

    def test_reduction_percentage_zero_original(self) -> None:
        """Test reduction percentage with zero original tokens."""
        result = OptimizationResult(
            original_tokens=0,
            optimized_tokens=0,
            changes_made=[],
            optimized_skill=MagicMock(),
        )

        assert result.reduction_percentage == 0.0

    def test_within_budget_true(self) -> None:
        """Test within_budget when optimized tokens are within T2 budget."""
        result = OptimizationResult(
            original_tokens=10000,
            optimized_tokens=5000,
            changes_made=["Optimized"],
            optimized_skill=MagicMock(),
        )

        assert result.within_budget is True

    def test_within_budget_false(self) -> None:
        """Test within_budget when optimized tokens exceed T2 budget."""
        result = OptimizationResult(
            original_tokens=10000,
            optimized_tokens=8000,
            changes_made=["Attempted optimization"],
            optimized_skill=MagicMock(),
        )

        assert result.within_budget is False


class TestProgressiveDisclosureOptimizer:
    """Tests for ProgressiveDisclosureOptimizer."""

    @pytest.mark.asyncio
    async def test_optimize_already_under_budget(
        self, sample_skill: SkillContent
    ) -> None:
        """Test optimization when skill is already under budget."""
        optimizer = ProgressiveDisclosureOptimizer()

        result = await optimizer.optimize(sample_skill)

        assert result.original_tokens <= T2_BUDGET
        assert result.optimized_tokens == result.original_tokens
        assert result.within_budget
        assert any(
            "already within T2 budget" in change for change in result.changes_made
        )

    @pytest.mark.asyncio
    async def test_optimize_large_skill_dry_run(
        self, large_skill: SkillContent
    ) -> None:
        """Test dry run optimization of large skill."""
        import json

        # Mock LLM response
        mock_analysis = {
            "tier_assignments": {
                "frontmatter": "T1",
                "purpose": "T1",
                "examples": "T2",
            },
            "content_to_move": [
                {
                    "section": "advanced_examples",
                    "reason": "Verbose",
                    "target": "advanced.md",
                }
            ],
            "content_to_condense": [],
            "content_to_remove": [],
            "recommended_changes": ["Remove filler words", "Use imperative voice"],
            "estimated_tokens_after": 4800,
        }

        mock_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client.generate = AsyncMock(return_value=mock_response)

        optimizer = ProgressiveDisclosureOptimizer(client=mock_client, dry_run=True)
        result = await optimizer.optimize(large_skill)

        assert "Dry run" in " ".join(result.changes_made)
        assert result.optimized_tokens < result.original_tokens
        assert any("Recommended" in change for change in result.changes_made)

    @pytest.mark.asyncio
    async def test_optimize_with_rewrite(self, large_skill: SkillContent) -> None:
        """Test full optimization with rewrite."""
        import json

        # Mock LLM responses
        mock_analysis = {
            "tier_assignments": {"frontmatter": "T1"},
            "content_to_move": [],
            "content_to_condense": [
                {
                    "section": "instructions",
                    "current_tokens": 2000,
                    "target_tokens": 1000,
                    "strategy": "Use imperative voice",
                }
            ],
            "content_to_remove": [],
            "recommended_changes": ["Condense instructions"],
            "estimated_tokens_after": 5000,
        }

        optimized_markdown = """---
name: large-test-skill
description: "A large test skill that exceeds token budgets"
---

# Optimized Skill

Condensed overview.

## When to Use This Skill

- Use case 1
- Use case 2

## Instructions

Step 1: Do this.
Step 2: Do that.
"""

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        # First call for analysis
        analysis_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        # Second call for rewrite
        rewrite_response = LLMResponse(
            content=optimized_markdown,
            model="claude-test",
            tokens_used=200,
            stop_reason="end_turn",
        )

        mock_client.generate = AsyncMock(
            side_effect=[analysis_response, rewrite_response]
        )

        optimizer = ProgressiveDisclosureOptimizer(client=mock_client, dry_run=False)
        result = await optimizer.optimize(large_skill)

        # Verify calls were made
        assert mock_client.generate.call_count == 2
        assert "Rewriting skill with optimizations" in result.changes_made
        assert result.optimized_tokens < result.original_tokens

    @pytest.mark.asyncio
    async def test_analyze_only(self, large_skill: SkillContent) -> None:
        """Test analyze_only method."""
        import json

        mock_analysis = {
            "tier_assignments": {"frontmatter": "T1"},
            "content_to_move": [],
            "content_to_condense": [],
            "content_to_remove": [],
            "recommended_changes": [],
            "estimated_tokens_after": 5000,
        }

        mock_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client.generate = AsyncMock(return_value=mock_response)

        optimizer = ProgressiveDisclosureOptimizer(client=mock_client)
        analysis = await optimizer.analyze_only(large_skill)

        assert "original_tokens" in analysis
        assert "analysis" in analysis
        assert "over_budget" in analysis
        assert analysis["over_budget"] is True


class TestStructureOptimizer:
    """Tests for StructureOptimizer."""

    @pytest.mark.asyncio
    async def test_optimize_dry_run(self, sample_skill: SkillContent) -> None:
        """Test dry run structure optimization."""
        import json

        mock_analysis = {
            "structure_issues": [
                {
                    "issue": "Examples before instructions",
                    "severity": "medium",
                    "fix": "Reorder sections",
                }
            ],
            "readability_issues": [],
            "llm_optimization_issues": [],
            "recommended_restructuring": [],
            "formatting_improvements": [],
            "voice_corrections": [],
            "estimated_improvement": "10% better",
        }

        mock_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client.generate = AsyncMock(return_value=mock_response)

        optimizer = StructureOptimizer(client=mock_client, dry_run=True)
        result = await optimizer.optimize(sample_skill)

        assert "Dry run" in " ".join(result.changes_made)
        assert "Structure issue" in " ".join(result.changes_made)

    @pytest.mark.asyncio
    async def test_optimize_with_restructure(self, sample_skill: SkillContent) -> None:
        """Test full structure optimization with restructuring."""
        import json

        mock_analysis = {
            "structure_issues": [
                {"issue": "Poor organization", "severity": "high", "fix": "Reorder"}
            ],
            "readability_issues": [
                {"issue": "Long paragraphs", "severity": "low", "fix": "Break up"}
            ],
            "llm_optimization_issues": [
                {
                    "issue": "Missing triggers",
                    "severity": "high",
                    "fix": "Add trigger phrases",
                }
            ],
            "recommended_restructuring": [],
            "formatting_improvements": [],
            "voice_corrections": [],
            "estimated_improvement": "30% better",
        }

        restructured_markdown = """---
name: test-skill
description: "A test skill for optimizer testing"
---

# Test Skill

Improved overview.

## When to Use This Skill

- Clear trigger: test optimization
- Clear trigger: validate LLM

## Quick Reference

Run `test-command`.

## Instructions

1. Do this.
2. Do that.
3. Complete the task.
"""

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()

        # First call for analysis
        analysis_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        # Second call for restructure
        restructure_response = LLMResponse(
            content=restructured_markdown,
            model="claude-test",
            tokens_used=200,
            stop_reason="end_turn",
        )

        mock_client.generate = AsyncMock(
            side_effect=[analysis_response, restructure_response]
        )

        optimizer = StructureOptimizer(client=mock_client, dry_run=False)
        result = await optimizer.optimize(sample_skill)

        # Verify calls were made
        assert mock_client.generate.call_count == 2
        assert "Restructuring skill with optimizations" in result.changes_made
        assert any("Structure issue" in change for change in result.changes_made)
        assert any("Readability issue" in change for change in result.changes_made)
        assert any("LLM optimization" in change for change in result.changes_made)

    @pytest.mark.asyncio
    async def test_analyze_only(self, sample_skill: SkillContent) -> None:
        """Test analyze_only method."""
        import json

        mock_analysis = {
            "structure_issues": [{"issue": "Test issue", "severity": "low"}],
            "readability_issues": [{"issue": "Test readability", "severity": "low"}],
            "llm_optimization_issues": [],
            "recommended_restructuring": [],
            "formatting_improvements": [],
            "voice_corrections": [],
            "estimated_improvement": "5% better",
        }

        mock_response = LLMResponse(
            content=json.dumps(mock_analysis),
            model="claude-test",
            tokens_used=100,
            stop_reason="end_turn",
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock()
        mock_client.generate = AsyncMock(return_value=mock_response)

        optimizer = StructureOptimizer(client=mock_client)
        analysis = await optimizer.analyze_only(sample_skill)

        assert "original_tokens" in analysis
        assert "analysis" in analysis
        assert "total_issues" in analysis
        assert analysis["total_issues"] == 2  # 1 structure + 1 readability


class TestOptimizerBudgets:
    """Tests for budget constants."""

    def test_budget_hierarchy(self) -> None:
        """Test that budget tiers are in correct order."""
        assert T1_BUDGET < T2_BUDGET < T3_BUDGET
        assert T1_BUDGET == 2000
        assert T2_BUDGET == 6000
        assert T3_BUDGET == 12000
