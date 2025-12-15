"""Unit tests for tooling/analyze_coverage.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from analyze_coverage import (
    analyze_coverage,
    categorize_skill,
    generate_markdown_report,
    load_skills_index,
    main,
)


class TestCategorizeSkill:
    """Test skill categorization logic."""

    def test_core_skills(self) -> None:
        """Categorize core-* skills as Core tier."""
        tier, domain = categorize_skill("core-agent-authoring")
        assert tier == "Core"
        assert domain == "Core"

        tier, domain = categorize_skill("core-skill-authoring")
        assert tier == "Core"
        assert domain == "Core"

    def test_domain_skills(self) -> None:
        """Categorize regular domain skills as Domain tier."""
        tier, domain = categorize_skill("api-design-validator")
        assert tier == "Domain"
        assert domain == "Api"

        tier, domain = categorize_skill("security-appsec-validator")
        assert tier == "Domain"
        assert domain == "Security"

    def test_kubernetes_specialized(self) -> None:
        """Kubernetes skills categorized as Specialized."""
        tier, domain = categorize_skill("kubernetes-manifest-generator")
        assert tier == "Specialized"
        assert domain == "Kubernetes"

    def test_terraform_specialized(self) -> None:
        """Terraform skills categorized as Specialized."""
        tier, domain = categorize_skill("terraform-module-patterns")
        assert tier == "Specialized"
        assert domain == "Terraform"

    def test_rust_specialized(self) -> None:
        """Rust skills categorized as Specialized."""
        tier, domain = categorize_skill("rust-analyzer")
        assert tier == "Specialized"
        assert domain == "Rust"

    def test_go_specialized(self) -> None:
        """Go skills categorized as Specialized."""
        tier, domain = categorize_skill("go-project-scaffolder")
        assert tier == "Specialized"
        assert domain == "Go"

    def test_mobile_specialized(self) -> None:
        """Mobile skills categorized as Specialized."""
        tier, domain = categorize_skill("mobile-cicd-generator")
        assert tier == "Specialized"
        assert domain == "Mobile"

    def test_compliance_specialized(self) -> None:
        """Compliance skills categorized as Specialized."""
        tier, domain = categorize_skill("compliance-fedramp-validator")
        assert tier == "Specialized"
        assert domain == "Compliance"

    def test_slo_specialized(self) -> None:
        """SLO skills categorized as Specialized."""
        tier, domain = categorize_skill("slo-validator")
        assert tier == "Specialized"
        assert domain == "Slo"

    def test_e2e_specialized(self) -> None:
        """E2E skills categorized as Specialized."""
        tier, domain = categorize_skill("e2e-testing-generator")
        assert tier == "Specialized"
        assert domain == "E2e"

    def test_tech_in_second_part_specialized(self) -> None:
        """Skills with tech keyword in second part are Specialized."""
        tier, domain = categorize_skill("cloud-kubernetes-integrator")
        assert tier == "Specialized"
        assert domain == "Cloud"

    def test_domain_capitalization(self) -> None:
        """Domain names are capitalized."""
        tier, domain = categorize_skill("database-schema-designer")
        assert domain == "Database"

        tier, domain = categorize_skill("testing-unit-generator")
        assert domain == "Testing"

    def test_uncategorized_skill(self) -> None:
        """Skills without hyphens are uncategorized."""
        tier, domain = categorize_skill("singlenamesku")
        assert tier == "Uncategorized"
        assert domain == "Other"

    def test_single_hyphen_skill(self) -> None:
        """Skills with single hyphen return domain from first part."""
        tier, domain = categorize_skill("api-validator")
        assert tier == "Domain"
        assert domain == "Api"


class TestAnalyzeCoverage:
    """Test coverage analysis."""

    def test_empty_skills_list(self) -> None:
        """Handle empty skills list."""
        by_tier, by_domain, domain_tier_map = analyze_coverage([])

        assert by_tier["Core"] == []
        assert by_tier["Domain"] == []
        assert by_tier["Specialized"] == []
        assert len(by_domain) == 0

    def test_single_core_skill(self) -> None:
        """Analyze single core skill."""
        skills = [{"slug": "core-agent-authoring"}]
        by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

        assert len(by_tier["Core"]) == 1
        assert "core-agent-authoring" in by_tier["Core"]
        assert by_domain["Core"] == 1
        assert "core-agent-authoring" in domain_tier_map["Core"]["Core"]

    def test_mixed_tier_skills(self) -> None:
        """Analyze skills across different tiers."""
        skills = [
            {"slug": "core-skill-authoring"},
            {"slug": "api-design-validator"},
            {"slug": "kubernetes-manifest-generator"},
        ]
        by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

        assert len(by_tier["Core"]) == 1
        assert len(by_tier["Domain"]) == 1
        assert len(by_tier["Specialized"]) == 1

    def test_domain_counting(self) -> None:
        """Count skills per domain correctly."""
        skills = [
            {"slug": "security-appsec-validator"},
            {"slug": "security-cloud-analyzer"},
            {"slug": "security-container-validator"},
            {"slug": "api-design-validator"},
            {"slug": "api-contract-testing"},
        ]
        by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

        assert by_domain["Security"] == 3
        assert by_domain["Api"] == 2

    def test_domain_tier_mapping(self) -> None:
        """Map domains to tiers correctly."""
        skills = [
            {"slug": "testing-unit-generator"},
            {"slug": "testing-integration-designer"},
            {"slug": "e2e-testing-generator"},
        ]
        by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

        # First two are Domain tier
        assert len(domain_tier_map["Domain"]["Testing"]) == 2
        # E2E is Specialized tier
        assert len(domain_tier_map["Specialized"]["E2e"]) == 1

    def test_multiple_domains_same_tier(self) -> None:
        """Handle multiple domains within same tier."""
        skills = [
            {"slug": "api-design-validator"},
            {"slug": "database-schema-designer"},
            {"slug": "testing-unit-generator"},
        ]
        by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

        assert len(by_tier["Domain"]) == 3
        assert len(domain_tier_map["Domain"]) == 3
        assert "Api" in domain_tier_map["Domain"]
        assert "Database" in domain_tier_map["Domain"]
        assert "Testing" in domain_tier_map["Domain"]


class TestGenerateMarkdownReport:
    """Test markdown report generation."""

    def test_basic_report_structure(self) -> None:
        """Generate report with required sections."""
        by_tier = {"Core": ["core-test"], "Domain": ["api-test"], "Specialized": ["k8s-test"]}
        by_domain = {"Core": 1, "Api": 1, "K8s": 1}
        domain_tier_map = {
            "Core": {"Core": ["core-test"]},
            "Domain": {"Api": ["api-test"]},
            "Specialized": {"K8s": ["k8s-test"]},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 3)

        # Check required sections
        assert "# Skill Coverage Matrix Analysis" in report
        assert "## Coverage by Tier" in report
        assert "## Coverage by Domain (Top 10)" in report
        assert "## Detailed Tier Breakdown" in report
        assert "## Gap Analysis" in report
        assert "## Domain Coverage Heat Map" in report

    def test_total_skills_count(self) -> None:
        """Include total skills count."""
        by_tier = {"Core": [], "Domain": [], "Specialized": []}
        by_domain: dict[str, int] = {}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 42)

        assert "**Total Skills**: 42" in report

    def test_tier_percentages(self) -> None:
        """Calculate tier percentages correctly."""
        by_tier = {
            "Core": ["c1", "c2"],
            "Domain": ["d1", "d2", "d3", "d4"],
            "Specialized": ["s1", "s2", "s3", "s4"],
        }
        by_domain = {"Core": 2, "Domain": 4, "Specialized": 4}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {"Core": by_tier["Core"]},
            "Domain": {"Domain": by_tier["Domain"]},
            "Specialized": {"Specialized": by_tier["Specialized"]},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 10)

        # Core: 2/10 = 20%
        assert "| Core | 2 | 20.0% |" in report
        # Domain: 4/10 = 40%
        assert "| Domain | 4 | 40.0% |" in report
        # Specialized: 4/10 = 40%
        assert "| Specialized | 4 | 40.0% |" in report

    def test_zero_division_protection(self) -> None:
        """Handle zero total skills gracefully."""
        by_tier = {"Core": [], "Domain": [], "Specialized": []}
        by_domain: dict[str, int] = {}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 0)

        # Should not raise division by zero
        assert "0.0%" in report

    def test_top_domains_limit(self) -> None:
        """Limit domain list to top 10."""
        by_tier = {"Core": [], "Domain": [], "Specialized": []}
        by_domain = {f"Domain{i}": i for i in range(1, 16)}  # 15 domains
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 100)

        # Check that top domains appear (higher counts should be in report)
        assert "Domain15" in report
        assert "Domain14" in report
        # Count domain rows in the table (should be exactly 10, not including header/separator)
        lines = report.split("\n")
        in_domain_section = False
        domain_rows = 0
        for line in lines:
            if "## Coverage by Domain (Top 10)" in line:
                in_domain_section = True
            elif in_domain_section and line.startswith("| Domain"):
                if "Count" not in line:  # Skip header
                    domain_rows += 1
            elif in_domain_section and line.startswith("##"):
                break
        assert domain_rows == 10  # Exactly 10 domain rows

    def test_skills_preview_truncation(self) -> None:
        """Truncate skills preview to 3 items."""
        by_tier = {"Core": [], "Domain": ["s1", "s2", "s3", "s4", "s5"], "Specialized": []}
        by_domain = {"Test": 5}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {"Test": ["s1", "s2", "s3", "s4", "s5"]},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 5)

        # Should show first 3 skills + "..."
        assert "s1, s2, s3, ..." in report

    def test_detailed_breakdown_core_list(self) -> None:
        """List core skills individually."""
        by_tier = {"Core": ["core-alpha", "core-beta"], "Domain": [], "Specialized": []}
        by_domain = {"Core": 2}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {"Core": ["core-alpha", "core-beta"]},
            "Domain": {},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 2)

        assert "### Core (2 skills)" in report
        assert "- `core-alpha`" in report
        assert "- `core-beta`" in report

    def test_detailed_breakdown_domain_grouping(self) -> None:
        """Group domain skills by domain."""
        by_tier = {
            "Core": [],
            "Domain": ["api-design", "api-contract", "database-schema"],
            "Specialized": [],
        }
        by_domain = {"Api": 2, "Database": 1}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {"Api": ["api-design", "api-contract"], "Database": ["database-schema"]},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 3)

        assert "### Domain (3 skills)" in report
        assert "**Api** (2):" in report
        assert "**Database** (1):" in report

    def test_gap_analysis_sections(self) -> None:
        """Include gap analysis recommendations."""
        by_tier = {"Core": [], "Domain": [], "Specialized": []}
        by_domain: dict[str, int] = {}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 0)

        # Check gap analysis sections exist
        assert "**Cloud Providers:**" in report
        assert "**Language-Specific Tooling:**" in report
        assert "**Testing:**" in report
        assert "**Observability:**" in report
        assert "### Recommendations" in report

    def test_heat_map_visualization(self) -> None:
        """Generate ASCII heat map."""
        by_tier = {"Core": [], "Domain": ["d1", "d2", "d3"], "Specialized": []}
        by_domain = {"TestDomain": 3, "Core": 0}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {},
            "Domain": {"TestDomain": ["d1", "d2", "d3"]},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 3)

        # Heat map should have bars (█ characters)
        assert "█" in report
        # Should show TestDomain with count
        assert "TestDomain" in report
        assert "[ 3]" in report or "[3]" in report

    def test_heat_map_excludes_core(self) -> None:
        """Heat map excludes Core domain."""
        by_tier = {"Core": ["c1", "c2"], "Domain": ["d1"], "Specialized": []}
        by_domain = {"Core": 2, "Test": 1}
        domain_tier_map: dict[str, dict[str, list[str]]] = {
            "Core": {"Core": ["c1", "c2"]},
            "Domain": {"Test": ["d1"]},
            "Specialized": {},
        }

        report = generate_markdown_report(by_tier, by_domain, domain_tier_map, 3)

        # Find heat map section
        lines = report.split("\n")
        in_heat_map = False
        heat_map_lines = []
        for line in lines:
            if "## Domain Coverage Heat Map" in line:
                in_heat_map = True
            elif in_heat_map:
                if line.strip() == "```" and heat_map_lines:
                    break
                if line.strip() and line.strip() != "```":
                    heat_map_lines.append(line)

        # Core should not appear in heat map data
        # "Core" might appear as domain name, but shouldn't have visualization bar
        # Let's check more specifically - Core with bracket count shouldn't be there
        assert not any("Core" in line and "[" in line for line in heat_map_lines)


class TestLoadSkillsIndex:
    """Test skills index loading.

    Note: load_skills_index() uses Path(__file__) which is difficult to mock.
    Testing is done via integration tests in TestMain instead.
    """

    def test_load_index_structure(self) -> None:
        """Verify load_skills_index returns expected structure."""
        # This tests the actual repository index file exists
        # Skipping if in test environment without real index
        try:
            skills = load_skills_index()
            # Verify it returns a list
            assert isinstance(skills, list)
            # If there are skills, verify structure
            if skills:
                assert "slug" in skills[0]
        except FileNotFoundError:
            # Index file doesn't exist in test environment - skip
            pytest.skip("Skills index file not found (expected in test environment)")


class TestMain:
    """Test main function integration."""

    def test_main_creates_output_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Main function creates coverage matrix file."""
        # Create mock index
        index_data = [
            {"slug": "core-test-skill"},
            {"slug": "api-design-validator"},
            {"slug": "kubernetes-manifest-generator"},
        ]

        index_dir = tmp_path / "index"
        index_dir.mkdir()
        index_file = index_dir / "skills-index.json"
        index_file.write_text(json.dumps(index_data), encoding="utf-8")

        docs_dir = tmp_path / "docs"
        output_file = docs_dir / "COVERAGE_MATRIX.md"

        # Patch load_skills_index
        import analyze_coverage

        def patched_load() -> list[dict[str, Any]]:
            with index_file.open() as f:
                result: list[dict[str, Any]] = json.load(f)
                return result

        monkeypatch.setattr(analyze_coverage, "load_skills_index", patched_load)

        # Patch output path
        mock_script_path = tmp_path / "tooling" / "analyze_coverage.py"
        monkeypatch.setattr(analyze_coverage, "__file__", str(mock_script_path))

        main()

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Skill Coverage Matrix Analysis" in content
        assert "**Total Skills**: 3" in content

    def test_main_prints_summary(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Main function prints summary to stdout."""
        index_data = [
            {"slug": "core-test"},
            {"slug": "api-test"},
        ]

        index_dir = tmp_path / "index"
        index_dir.mkdir()
        index_file = index_dir / "skills-index.json"
        index_file.write_text(json.dumps(index_data), encoding="utf-8")

        import analyze_coverage

        def patched_load() -> list[dict[str, Any]]:
            with index_file.open() as f:
                result: list[dict[str, Any]] = json.load(f)
                return result

        monkeypatch.setattr(analyze_coverage, "load_skills_index", patched_load)

        mock_script_path = tmp_path / "tooling" / "analyze_coverage.py"
        monkeypatch.setattr(analyze_coverage, "__file__", str(mock_script_path))

        main()

        captured = capsys.readouterr()
        assert "Coverage matrix written to:" in captured.out
        assert "Quick Summary:" in captured.out
        assert "Total Skills: 2" in captured.out
