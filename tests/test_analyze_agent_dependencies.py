"""Unit tests for tooling/analyze_agent_dependencies.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from analyze_agent_dependencies import (
    build_dependency_graph,
    extract_skill_references,
    generate_markdown_report,
    generate_mermaid_diagram,
    load_agents_index,
    load_skills_index,
    main,
)


class TestExtractSkillReferences:
    """Test skill reference extraction from agent markdown."""

    def test_extract_backtick_slug(self, tmp_path: Path) -> None:
        """Extract slug from backticks."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
# Agent

Uses `api-design-validator` and `security-appsec-validator` skills.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert "api-design-validator" in refs
        assert "security-appsec-validator" in refs

    def test_ignore_non_slug_backticks(self, tmp_path: Path) -> None:
        """Ignore backticked text that isn't a slug."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
# Agent

Run `npm install` and check `README.md`.
Uses `skill-with-hyphens` but not `CamelCase` or `UPPERCASE`.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert "skill-with-hyphens" in refs
        # Should exclude non-lowercase
        assert "npm" not in refs  # No hyphen
        assert "CamelCase" not in refs  # Not lowercase
        assert "UPPERCASE" not in refs  # Not lowercase
        assert "README.md" not in refs  # Has dot

    def test_require_hyphen_in_slug(self, tmp_path: Path) -> None:
        """Require at least one hyphen for slug detection."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
Uses `singleword` and `has-hyphen`.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert "has-hyphen" in refs
        assert "singleword" not in refs  # No hyphen

    def test_deduplicate_references(self, tmp_path: Path) -> None:
        """Deduplicate repeated skill references."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
Uses `test-skill` multiple times.
Also `test-skill` again.
And `test-skill` once more.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert refs.count("test-skill") == 1  # Should appear only once

    def test_return_sorted_list(self, tmp_path: Path) -> None:
        """Return alphabetically sorted list."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
Uses `zebra-skill`, `alpha-skill`, and `beta-skill`.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert refs == ["alpha-skill", "beta-skill", "zebra-skill"]

    def test_empty_file(self, tmp_path: Path) -> None:
        """Handle empty file gracefully."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text("", encoding="utf-8")

        refs = extract_skill_references(agent_md)
        assert refs == []

    def test_no_skill_references(self, tmp_path: Path) -> None:
        """Handle file with no skill references."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
# Agent with No Skills

This agent does not reference any skills.
It works independently.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        assert refs == []

    def test_complex_markdown_extraction(self, tmp_path: Path) -> None:
        """Extract skills from complex markdown structure."""
        agent_md = tmp_path / "AGENT.md"
        agent_md.write_text(
            """
# Security Auditor Agent

## Skills Orchestrated

1. `security-appsec-validator` - Application security
2. `security-cloud-analyzer` - Cloud security
3. `security-container-validator` - Container security

## Workflow

The agent uses `security-iam-reviewer` for IAM checks and
`security-network-validator` for network validation.

Also references `testing-unit-generator` in example.
""",
            encoding="utf-8",
        )

        refs = extract_skill_references(agent_md)
        # Should extract all backtick-enclosed skill references
        assert "security-appsec-validator" in refs
        assert "security-cloud-analyzer" in refs
        assert "security-container-validator" in refs
        assert "security-iam-reviewer" in refs
        assert "security-network-validator" in refs
        assert "testing-unit-generator" in refs


class TestBuildDependencyGraph:
    """Test dependency graph building."""

    def create_test_environment(
        self, tmp_path: Path
    ) -> tuple[Path, list[dict[str, Any]], list[dict[str, Any]]]:
        """Create test environment with agents and skills."""
        # Create index files
        agents_data = [
            {"slug": "test-agent", "name": "Test Agent", "entry": "agents/test-agent/AGENT.md"},
            {
                "slug": "another-agent",
                "name": "Another Agent",
                "entry": "agents/another-agent/AGENT.md",
            },
        ]

        skills_data = [
            {"slug": "skill-alpha"},
            {"slug": "skill-beta"},
            {"slug": "skill-gamma"},
        ]

        index_dir = tmp_path / "index"
        index_dir.mkdir()
        (index_dir / "agents-index.json").write_text(json.dumps(agents_data), encoding="utf-8")
        (index_dir / "skills-index.json").write_text(json.dumps(skills_data), encoding="utf-8")

        # Create agent markdown files
        agents_dir = tmp_path / "agents"

        test_agent_dir = agents_dir / "test-agent"
        test_agent_dir.mkdir(parents=True)
        (test_agent_dir / "AGENT.md").write_text(
            "Uses `skill-alpha` and `skill-beta`.", encoding="utf-8"
        )

        another_agent_dir = agents_dir / "another-agent"
        another_agent_dir.mkdir(parents=True)
        (another_agent_dir / "AGENT.md").write_text("Uses `skill-beta`.", encoding="utf-8")

        return tmp_path, agents_data, skills_data

    def test_build_graph_basic(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Build basic dependency graph."""
        repo_root, agents_data, skills_data = self.create_test_environment(tmp_path)

        # Patch loading functions
        import analyze_agent_dependencies

        def patched_load_agents() -> list[dict[str, Any]]:
            return agents_data

        def patched_load_skills() -> list[dict[str, Any]]:
            return skills_data

        monkeypatch.setattr(analyze_agent_dependencies, "load_agents_index", patched_load_agents)
        monkeypatch.setattr(analyze_agent_dependencies, "load_skills_index", patched_load_skills)
        monkeypatch.setattr(
            analyze_agent_dependencies, "__file__", str(repo_root / "tooling" / "script.py")
        )

        dependencies, skill_usage = build_dependency_graph()

        # Verify dependencies structure
        assert "test-agent" in dependencies
        assert "another-agent" in dependencies

        # Test agent uses skill-alpha and skill-beta
        assert set(dependencies["test-agent"]["skills"]) == {"skill-alpha", "skill-beta"}
        assert dependencies["test-agent"]["skill_count"] == 2

        # Another agent uses skill-beta
        assert dependencies["another-agent"]["skills"] == ["skill-beta"]
        assert dependencies["another-agent"]["skill_count"] == 1

    def test_skill_usage_reverse_mapping(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Build reverse mapping of skill usage."""
        repo_root, agents_data, skills_data = self.create_test_environment(tmp_path)

        import analyze_agent_dependencies

        monkeypatch.setattr(analyze_agent_dependencies, "load_agents_index", lambda: agents_data)
        monkeypatch.setattr(analyze_agent_dependencies, "load_skills_index", lambda: skills_data)
        monkeypatch.setattr(
            analyze_agent_dependencies, "__file__", str(repo_root / "tooling" / "script.py")
        )

        dependencies, skill_usage = build_dependency_graph()

        # skill-alpha used by test-agent
        assert skill_usage["skill-alpha"] == ["test-agent"]

        # skill-beta used by both agents
        assert set(skill_usage["skill-beta"]) == {"test-agent", "another-agent"}

        # skill-gamma not used by anyone
        assert "skill-gamma" not in skill_usage

    def test_filter_invalid_skill_references(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Filter out invalid skill references."""
        # Agent references non-existent skill
        agents_data = [{"slug": "agent", "name": "Agent", "entry": "agents/agent/AGENT.md"}]
        skills_data = [{"slug": "real-skill"}]

        index_dir = tmp_path / "index"
        index_dir.mkdir()
        (index_dir / "agents-index.json").write_text(json.dumps(agents_data), encoding="utf-8")
        (index_dir / "skills-index.json").write_text(json.dumps(skills_data), encoding="utf-8")

        agent_dir = tmp_path / "agents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "AGENT.md").write_text("Uses `real-skill` and `fake-skill`.", encoding="utf-8")

        import analyze_agent_dependencies

        monkeypatch.setattr(analyze_agent_dependencies, "load_agents_index", lambda: agents_data)
        monkeypatch.setattr(analyze_agent_dependencies, "load_skills_index", lambda: skills_data)
        monkeypatch.setattr(
            analyze_agent_dependencies, "__file__", str(tmp_path / "tooling" / "script.py")
        )

        dependencies, skill_usage = build_dependency_graph()

        # Should only include real-skill
        assert dependencies["agent"]["skills"] == ["real-skill"]
        assert "fake-skill" not in skill_usage


class TestGenerateMermaidDiagram:
    """Test Mermaid diagram generation."""

    def test_basic_diagram_structure(self) -> None:
        """Generate basic Mermaid diagram."""
        dependencies = {
            "test-agent": {
                "name": "Test Agent",
                "skills": ["skill-alpha", "skill-beta"],
                "skill_count": 2,
            }
        }

        diagram = generate_mermaid_diagram(dependencies)

        assert "```mermaid" in diagram
        assert "graph LR" in diagram
        assert "```" in diagram.split("```mermaid")[1]

    def test_style_definitions(self) -> None:
        """Include style definitions for agents and skills."""
        dependencies = {"agent": {"name": "Agent", "skills": ["skill"], "skill_count": 1}}

        diagram = generate_mermaid_diagram(dependencies)

        assert "classDef agent" in diagram
        assert "classDef skill" in diagram

    def test_agent_nodes(self) -> None:
        """Generate agent nodes with proper formatting."""
        dependencies = {
            "security-auditor": {
                "name": "Security Auditor",
                "skills": ["skill-test"],
                "skill_count": 1,
            }
        }

        diagram = generate_mermaid_diagram(dependencies)

        # Hyphens replaced with underscores for IDs
        assert "security_auditor[Security Auditor]:::agent" in diagram

    def test_skill_nodes_only_referenced(self) -> None:
        """Only create nodes for referenced skills."""
        dependencies = {
            "agent1": {"name": "Agent 1", "skills": ["skill-alpha"], "skill_count": 1},
            "agent2": {"name": "Agent 2", "skills": ["skill-beta"], "skill_count": 1},
        }

        diagram = generate_mermaid_diagram(dependencies)

        assert "skill_alpha[skill-alpha]:::skill" in diagram
        assert "skill_beta[skill-beta]:::skill" in diagram

    def test_edges_agent_to_skills(self) -> None:
        """Generate edges from agents to skills."""
        dependencies = {
            "test-agent": {"name": "Test", "skills": ["skill-a", "skill-b"], "skill_count": 2}
        }

        diagram = generate_mermaid_diagram(dependencies)

        assert "test_agent --> skill_a" in diagram
        assert "test_agent --> skill_b" in diagram

    def test_empty_dependencies(self) -> None:
        """Handle empty dependencies."""
        dependencies: dict[str, dict[str, Any]] = {}

        diagram = generate_mermaid_diagram(dependencies)

        assert "```mermaid" in diagram
        assert "graph LR" in diagram

    def test_agent_with_no_skills(self) -> None:
        """Handle agent with no skill dependencies."""
        dependencies = {"agent": {"name": "Agent", "skills": [], "skill_count": 0}}

        diagram = generate_mermaid_diagram(dependencies)

        # Agent node should exist
        assert "agent[Agent]:::agent" in diagram
        # No edges
        assert "agent -->" not in diagram


class TestGenerateMarkdownReport:
    """Test markdown report generation."""

    def create_mock_load_skills(self, skills_data: list[dict[str, Any]]) -> Any:
        """Create mock function for load_skills_index."""

        def mock_load() -> list[dict[str, Any]]:
            return skills_data

        return mock_load

    def test_report_structure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Generate report with required sections."""
        dependencies = {"agent": {"name": "Agent", "skills": ["skill"], "skill_count": 1}}
        skill_usage = {"skill": ["agent"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills([{"slug": "skill"}]),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "# Agent→Skill Dependency Graph" in report
        assert "## Summary Statistics" in report
        assert "## Agent Dependencies" in report
        assert "## Skill Usage by Agents" in report
        assert "## Insights" in report
        assert "## Dependency Graph Visualization" in report

    def test_summary_statistics(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Calculate summary statistics correctly."""
        dependencies = {
            "agent1": {"name": "A1", "skills": ["s1", "s2"], "skill_count": 2},
            "agent2": {"name": "A2", "skills": ["s2", "s3"], "skill_count": 2},
        }
        skill_usage = {"s1": ["agent1"], "s2": ["agent1", "agent2"], "s3": ["agent2"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills([{"slug": "s1"}, {"slug": "s2"}, {"slug": "s3"}]),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "- **Total Agents**: 2" in report
        assert "- **Unique Skills Referenced**: 3" in report
        assert "- **Total Skill References**: 4" in report
        assert "- **Avg Skills per Agent**: 2.0" in report

    def test_agent_dependencies_table(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Generate agent dependencies table."""
        dependencies = {
            "test-agent": {
                "name": "Test Agent",
                "skills": ["skill-a", "skill-b", "skill-c", "skill-d"],
                "skill_count": 4,
            }
        }
        skill_usage = {"skill-a": ["test-agent"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills([{"slug": "skill-a"}]),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        # Should show first 3 skills + count of remaining
        assert "| test-agent | skill-a, skill-b, skill-c, ... (+1 more) | 4 |" in report

    def test_skill_usage_table_sorted_by_count(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Sort skill usage by count (descending)."""
        dependencies = {"a1": {"name": "A1", "skills": [], "skill_count": 0}}
        skill_usage = {
            "popular-skill": ["a1", "a2", "a3"],
            "rare-skill": ["a1"],
            "medium-skill": ["a1", "a2"],
        }

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills(
                [{"slug": "popular-skill"}, {"slug": "rare-skill"}, {"slug": "medium-skill"}]
            ),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        # Find skill usage table
        lines = report.split("\n")
        skill_table_start = None
        for i, line in enumerate(lines):
            if "## Skill Usage by Agents" in line:
                skill_table_start = i
                break

        assert skill_table_start is not None
        skill_rows = [
            line
            for line in lines[skill_table_start:]
            if line.startswith("| ") and "Skill" not in line
        ]

        # First row should be popular-skill (3 agents)
        assert "popular-skill" in skill_rows[0]

    def test_orphaned_skills_detection(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Detect skills not referenced by any agent."""
        dependencies = {"agent": {"name": "Agent", "skills": ["used-skill"], "skill_count": 1}}
        skill_usage = {"used-skill": ["agent"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills(
                [{"slug": "used-skill"}, {"slug": "orphan1"}, {"slug": "orphan2"}]
            ),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "### Orphaned Skills (2)" in report
        assert "- `orphan1`" in report
        assert "- `orphan2`" in report

    def test_orphaned_skills_limit_to_20(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Limit orphaned skills display to 20."""
        # Add dummy agent to prevent division by zero in statistics
        dependencies = {"dummy-agent": {"name": "Dummy", "skills": [], "skill_count": 0}}
        skill_usage: dict[str, list[str]] = {}

        # Create 25 orphaned skills
        all_skills = [{"slug": f"orphan-{i}"} for i in range(25)]

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills(all_skills),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "### Orphaned Skills (25)" in report
        assert "- ... and 5 more" in report

    def test_heavily_referenced_skills(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Identify heavily referenced skills (2+ agents)."""
        dependencies = {"a1": {"name": "A1", "skills": [], "skill_count": 0}}
        skill_usage = {
            "common-skill": ["agent1", "agent2", "agent3"],
            "shared-skill": ["agent1", "agent2"],
            "single-use": ["agent1"],
        }

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills(
                [{"slug": "common-skill"}, {"slug": "shared-skill"}, {"slug": "single-use"}]
            ),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "### Heavily Referenced Skills (2)" in report
        assert "**common-skill** (3 agents)" in report
        assert "**shared-skill** (2 agents)" in report
        # single-use should not appear (only 1 agent)
        assert "single-use" not in report.split("Heavily Referenced")[1].split("###")[0]

    def test_agents_with_no_dependencies(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Identify agents with no skill dependencies."""
        dependencies = {
            "standalone-agent": {"name": "Standalone", "skills": [], "skill_count": 0},
            "orchestrator": {"name": "Orchestrator", "skills": ["skill"], "skill_count": 1},
        }
        skill_usage = {"skill": ["orchestrator"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills([{"slug": "skill"}]),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "### Agents with No Skill Dependencies (1)" in report
        assert "- `standalone-agent`" in report

    def test_includes_mermaid_diagram(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Include Mermaid diagram in report."""
        dependencies = {"agent": {"name": "Agent", "skills": ["skill"], "skill_count": 1}}
        skill_usage = {"skill": ["agent"]}

        import analyze_agent_dependencies

        monkeypatch.setattr(
            analyze_agent_dependencies,
            "load_skills_index",
            self.create_mock_load_skills([{"slug": "skill"}]),
        )

        report = generate_markdown_report(dependencies, skill_usage)

        assert "```mermaid" in report
        assert "graph LR" in report


class TestLoadIndices:
    """Test index loading functions."""

    def test_load_agents_index_structure(self) -> None:
        """Verify load_agents_index returns expected structure."""
        try:
            agents = load_agents_index()
            assert isinstance(agents, list)
            if agents:
                assert "slug" in agents[0]
                assert "name" in agents[0]
                assert "entry" in agents[0]
        except FileNotFoundError:
            pytest.skip("Agents index file not found (expected in test environment)")

    def test_load_skills_index_structure(self) -> None:
        """Verify load_skills_index returns expected structure."""
        try:
            skills = load_skills_index()
            assert isinstance(skills, list)
            if skills:
                assert "slug" in skills[0]
        except FileNotFoundError:
            pytest.skip("Skills index file not found (expected in test environment)")


class TestMain:
    """Test main function integration."""

    def test_main_creates_output_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Main function creates dependency graph file."""
        # Setup test environment
        agents_data = [{"slug": "agent", "name": "Agent", "entry": "agents/agent/AGENT.md"}]
        skills_data = [{"slug": "test-skill"}]

        index_dir = tmp_path / "index"
        index_dir.mkdir()
        (index_dir / "agents-index.json").write_text(json.dumps(agents_data), encoding="utf-8")
        (index_dir / "skills-index.json").write_text(json.dumps(skills_data), encoding="utf-8")

        agent_dir = tmp_path / "agents" / "agent"
        agent_dir.mkdir(parents=True)
        (agent_dir / "AGENT.md").write_text("Uses `test-skill`.", encoding="utf-8")

        docs_dir = tmp_path / "docs"
        output_file = docs_dir / "AGENT_DEPENDENCIES.md"

        # Patch functions
        import analyze_agent_dependencies

        monkeypatch.setattr(analyze_agent_dependencies, "load_agents_index", lambda: agents_data)
        monkeypatch.setattr(analyze_agent_dependencies, "load_skills_index", lambda: skills_data)
        monkeypatch.setattr(
            analyze_agent_dependencies, "__file__", str(tmp_path / "tooling" / "script.py")
        )

        main()

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert "# Agent→Skill Dependency Graph" in content

        # Check console output
        captured = capsys.readouterr()
        assert "Analyzing agent→skill dependencies" in captured.out
        assert "Dependency graph written to:" in captured.out
