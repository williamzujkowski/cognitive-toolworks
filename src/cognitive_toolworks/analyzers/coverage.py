"""
Instruction coverage analysis for skills.

Analyzes how well a skill covers its stated purpose by checking:
- Required sections present
- Tool documentation completeness
- Example coverage
- Error handling documentation
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


class CoverageLevel(str, Enum):
    """Coverage completeness levels."""

    COMPLETE = "complete"
    GOOD = "good"
    PARTIAL = "partial"
    MINIMAL = "minimal"
    MISSING = "missing"


@dataclass
class SectionCoverage:
    """Coverage analysis for a section."""

    name: str
    present: bool
    completeness: CoverageLevel
    issues: list[str] = field(default_factory=list)


@dataclass
class CoverageReport:
    """Full coverage analysis report."""

    sections: list[SectionCoverage]
    overall_score: float  # 0-1
    overall_level: CoverageLevel
    missing_sections: list[str]
    recommendations: list[str]

    @property
    def passed(self) -> bool:
        """Check if coverage is acceptable."""
        return self.overall_score >= 0.7

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "sections": [
                {
                    "name": s.name,
                    "present": s.present,
                    "completeness": s.completeness.value,
                    "issues": s.issues,
                }
                for s in self.sections
            ],
            "overall_score": self.overall_score,
            "overall_level": self.overall_level.value,
            "missing_sections": self.missing_sections,
            "recommendations": self.recommendations,
        }


class CoverageAnalyzer:
    """
    Analyzes instruction coverage in skills.

    Checks for presence and completeness of:
    - Required sections (overview, when to use, instructions)
    - Optional but important sections (examples, troubleshooting)
    - Tool/command documentation
    - Error handling
    """

    # Required sections for a complete skill
    REQUIRED_SECTIONS: ClassVar[list[tuple[str, list[str]]]] = [
        ("metadata", ["---", "name:", "description:"]),
        ("overview", ["# ", "## Overview"]),
        ("when_to_use", ["## When to Use", "## When To Use"]),
        ("instructions", ["## Instructions", "## Workflows", "## Quick Reference"]),
    ]

    # Optional but recommended sections
    RECOMMENDED_SECTIONS: ClassVar[list[tuple[str, list[str]]]] = [
        ("examples", ["## Example", "### Example"]),
        ("troubleshooting", ["## Troubleshoot"]),
        ("guidelines", ["## Guideline", "## Best Practice"]),
        ("references", ["## Reference", "## See Also"]),
    ]

    def analyze(self, content: str) -> CoverageReport:
        """
        Analyze coverage of a skill.

        Args:
            content: The SKILL.md content.

        Returns:
            CoverageReport with section analysis and recommendations.
        """
        sections: list[SectionCoverage] = []
        missing_sections: list[str] = []

        # Check required sections
        for name, markers in self.REQUIRED_SECTIONS:
            coverage = self._check_section(content, name, markers, required=True)
            sections.append(coverage)
            if not coverage.present:
                missing_sections.append(name)

        # Check recommended sections
        for name, markers in self.RECOMMENDED_SECTIONS:
            coverage = self._check_section(content, name, markers, required=False)
            sections.append(coverage)

        # Additional quality checks
        sections.extend(self._check_examples(content))
        sections.extend(self._check_commands(content))

        # Calculate overall score
        overall_score = self._calculate_score(sections)
        overall_level = self._score_to_level(overall_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(sections, content)

        return CoverageReport(
            sections=sections,
            overall_score=overall_score,
            overall_level=overall_level,
            missing_sections=missing_sections,
            recommendations=recommendations,
        )

    def _check_section(
        self,
        content: str,
        name: str,
        markers: list[str],
        required: bool,
    ) -> SectionCoverage:
        """Check if a section is present and assess its completeness."""
        content_lower = content.lower()
        present = any(marker.lower() in content_lower for marker in markers)

        if not present:
            return SectionCoverage(
                name=name,
                present=False,
                completeness=CoverageLevel.MISSING,
                issues=[f"{'Required' if required else 'Recommended'} section '{name}' is missing"],
            )

        # Assess completeness based on content length
        section_content = self._extract_section(content, markers)
        completeness = self._assess_completeness(section_content, name)
        issues = self._find_section_issues(section_content, name)

        return SectionCoverage(
            name=name,
            present=True,
            completeness=completeness,
            issues=issues,
        )

    def _extract_section(self, content: str, markers: list[str]) -> str:
        """Extract content of a section."""
        lines = content.split("\n")
        in_section = False
        section_lines: list[str] = []

        for line in lines:
            # Check if we're starting a new section
            line_lower = line.lower()
            if any(marker.lower() in line_lower for marker in markers):
                in_section = True
                continue

            # Check if we've hit a new major section
            if in_section and line.startswith("## "):
                break

            if in_section:
                section_lines.append(line)

        return "\n".join(section_lines)

    def _assess_completeness(self, section_content: str, section_name: str) -> CoverageLevel:
        """Assess completeness of a section's content."""
        if not section_content.strip():
            return CoverageLevel.MISSING

        # Count meaningful lines
        lines = [line for line in section_content.split("\n") if line.strip()]
        word_count = len(section_content.split())

        # Section-specific thresholds
        thresholds = {
            "metadata": {"complete": 3, "good": 2, "partial": 1},
            "overview": {"complete": 50, "good": 30, "partial": 10},
            "when_to_use": {"complete": 5, "good": 3, "partial": 1},
            "instructions": {"complete": 100, "good": 50, "partial": 20},
            "examples": {"complete": 3, "good": 2, "partial": 1},
            "troubleshooting": {"complete": 3, "good": 2, "partial": 1},
        }

        thresh = thresholds.get(section_name, {"complete": 50, "good": 20, "partial": 5})

        # Use line count for lists, word count for prose
        if section_name in ["when_to_use", "examples", "troubleshooting"]:
            metric = len(lines)
        else:
            metric = word_count

        if metric >= thresh["complete"]:
            return CoverageLevel.COMPLETE
        elif metric >= thresh["good"]:
            return CoverageLevel.GOOD
        elif metric >= thresh["partial"]:
            return CoverageLevel.PARTIAL
        else:
            return CoverageLevel.MINIMAL

    def _find_section_issues(self, section_content: str, section_name: str) -> list[str]:
        """Find specific issues with a section."""
        issues: list[str] = []

        if section_name == "when_to_use":
            # Should have bullet points
            if "-" not in section_content and "*" not in section_content:
                issues.append("When to Use should include bullet points")

        elif section_name == "instructions":
            # Should have code blocks or commands
            if "```" not in section_content and "$" not in section_content:
                issues.append("Instructions should include code examples or commands")

        elif section_name == "examples":
            # Should have multiple examples
            example_count = section_content.lower().count("example")
            if example_count < 2:
                issues.append("Should include at least 2-3 examples")

        return issues

    def _check_examples(self, content: str) -> list[SectionCoverage]:
        """Check example quality and coverage."""
        sections: list[SectionCoverage] = []

        # Count code blocks
        code_blocks = content.count("```")
        if code_blocks == 0:
            sections.append(
                SectionCoverage(
                    name="code_examples",
                    present=False,
                    completeness=CoverageLevel.MISSING,
                    issues=["No code examples found"],
                )
            )
        elif code_blocks < 3:
            sections.append(
                SectionCoverage(
                    name="code_examples",
                    present=True,
                    completeness=CoverageLevel.PARTIAL,
                    issues=[f"Only {code_blocks} code blocks; recommend 3+"],
                )
            )
        else:
            sections.append(
                SectionCoverage(
                    name="code_examples",
                    present=True,
                    completeness=CoverageLevel.COMPLETE,
                )
            )

        return sections

    def _check_commands(self, content: str) -> list[SectionCoverage]:
        """Check command documentation coverage."""
        sections: list[SectionCoverage] = []

        # Look for command patterns
        command_pattern = r"\$\s+\w+"
        commands = re.findall(command_pattern, content)

        if not commands:
            sections.append(
                SectionCoverage(
                    name="commands",
                    present=False,
                    completeness=CoverageLevel.MISSING,
                    issues=["No CLI commands documented"],
                )
            )
        else:
            # Check if commands have descriptions
            completeness = CoverageLevel.COMPLETE if len(commands) >= 3 else CoverageLevel.PARTIAL
            sections.append(
                SectionCoverage(
                    name="commands",
                    present=True,
                    completeness=completeness,
                )
            )

        return sections

    def _calculate_score(self, sections: list[SectionCoverage]) -> float:
        """Calculate overall coverage score."""
        if not sections:
            return 0.0

        level_scores = {
            CoverageLevel.COMPLETE: 1.0,
            CoverageLevel.GOOD: 0.8,
            CoverageLevel.PARTIAL: 0.5,
            CoverageLevel.MINIMAL: 0.3,
            CoverageLevel.MISSING: 0.0,
        }

        # Weight required sections more heavily
        weights = {
            "metadata": 1.5,
            "overview": 1.2,
            "when_to_use": 1.0,
            "instructions": 1.5,
            "examples": 1.0,
            "troubleshooting": 0.5,
            "guidelines": 0.5,
            "references": 0.3,
            "code_examples": 1.0,
            "commands": 0.8,
        }

        total_weight = 0.0
        total_score = 0.0

        for section in sections:
            weight = weights.get(section.name, 0.5)
            score = level_scores.get(section.completeness, 0.0)
            total_weight += weight
            total_score += score * weight

        return total_score / total_weight if total_weight > 0 else 0.0

    def _score_to_level(self, score: float) -> CoverageLevel:
        """Convert score to coverage level."""
        if score >= 0.9:
            return CoverageLevel.COMPLETE
        elif score >= 0.7:
            return CoverageLevel.GOOD
        elif score >= 0.5:
            return CoverageLevel.PARTIAL
        elif score >= 0.3:
            return CoverageLevel.MINIMAL
        else:
            return CoverageLevel.MISSING

    def _generate_recommendations(
        self,
        sections: list[SectionCoverage],
        content: str,
    ) -> list[str]:
        """Generate recommendations based on analysis."""
        recommendations: list[str] = []

        for section in sections:
            if section.completeness == CoverageLevel.MISSING:
                recommendations.append(f"Add '{section.name}' section")
            elif section.completeness in (CoverageLevel.MINIMAL, CoverageLevel.PARTIAL):
                recommendations.append(f"Expand '{section.name}' section with more detail")

            for issue in section.issues:
                if issue not in recommendations:
                    recommendations.append(issue)

        # Content-specific recommendations
        if "```" not in content:
            recommendations.append("Add code examples with proper syntax highlighting")

        if "error" not in content.lower() and "troubleshoot" not in content.lower():
            recommendations.append("Add error handling or troubleshooting section")

        return recommendations[:10]  # Limit to top 10
