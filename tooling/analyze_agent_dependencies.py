#!/usr/bin/env python3
"""
Agent→Skill Dependency Graph Analyzer
Extracts skill references from agents and visualizes relationships
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_agents_index() -> list[dict[str, Any]]:
    """Load agents index"""
    index_path = Path(__file__).parent.parent / "index" / "agents-index.json"
    with open(index_path) as f:
        result: list[dict[str, Any]] = json.load(f)
        return result


def load_skills_index() -> list[dict[str, Any]]:
    """Load skills index"""
    index_path = Path(__file__).parent.parent / "index" / "skills-index.json"
    with open(index_path) as f:
        result: list[dict[str, Any]] = json.load(f)
        return result


def extract_skill_references(agent_md_path: Path) -> list[str]:
    """Extract skill slug references from agent AGENT.md"""
    content = agent_md_path.read_text()

    # Pattern 1: Backtick-enclosed slugs (e.g., `skill-slug`)
    backtick_pattern = r"`([a-z0-9-]+)`"

    # Pattern 2: Explicit skill list format: "1. `slug` - description"
    # Pattern 3: References in prose

    skills = set()
    for match in re.finditer(backtick_pattern, content):
        slug = match.group(1)
        # Filter to likely skill slugs (contains at least one hyphen, lowercase)
        if "-" in slug and slug.islower():
            skills.add(slug)

    return sorted(skills)


def build_dependency_graph() -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    """Build agent→skill dependency graph"""
    agents = load_agents_index()
    skills_set = {s["slug"] for s in load_skills_index()}

    dependencies: dict[str, dict[str, Any]] = {}
    skill_usage: dict[str, list[str]] = defaultdict(list)  # skill → list of agents using it

    repo_root = Path(__file__).parent.parent

    for agent in agents:
        agent_slug = agent["slug"]
        # entry is a relative path from repo root
        agent_path = repo_root / agent["entry"]

        # Extract skill references
        referenced_skills = extract_skill_references(agent_path)

        # Filter to only actual skills (not agent slugs or other references)
        valid_skills = [s for s in referenced_skills if s in skills_set]

        dependencies[agent_slug] = {
            "name": agent["name"],
            "skills": valid_skills,
            "skill_count": len(valid_skills),
        }

        # Track reverse mapping
        for skill in valid_skills:
            skill_usage[skill].append(agent_slug)

    return dependencies, skill_usage


def generate_mermaid_diagram(dependencies: dict[str, dict[str, Any]]) -> str:
    """Generate Mermaid flowchart for agent→skill dependencies"""
    lines = ["```mermaid", "graph LR"]

    # Style definitions
    lines.append("  classDef agent fill:#e1f5ff,stroke:#01579b,stroke-width:2px")
    lines.append("  classDef skill fill:#fff3e0,stroke:#e65100,stroke-width:1px")
    lines.append("")

    # Nodes
    for agent_slug, data in sorted(dependencies.items()):
        agent_id = agent_slug.replace("-", "_")
        lines.append(f"  {agent_id}[{data['name']}]:::agent")

    lines.append("")

    # Skill nodes (only for skills that are referenced)
    all_referenced_skills = set()
    for data in dependencies.values():
        all_referenced_skills.update(data["skills"])

    for skill_slug in sorted(all_referenced_skills):
        skill_id = skill_slug.replace("-", "_")
        lines.append(f"  {skill_id}[{skill_slug}]:::skill")

    lines.append("")

    # Edges
    for agent_slug, data in sorted(dependencies.items()):
        agent_id = agent_slug.replace("-", "_")
        for skill_slug in sorted(data["skills"]):
            skill_id = skill_slug.replace("-", "_")
            lines.append(f"  {agent_id} --> {skill_id}")

    lines.append("```")
    return "\n".join(lines)


def generate_markdown_report(
    dependencies: dict[str, dict[str, Any]], skill_usage: dict[str, list[str]]
) -> str:
    """Generate markdown dependency report"""
    md = ["# Agent→Skill Dependency Graph", ""]

    # Summary stats
    total_agents = len(dependencies)
    total_unique_skills = len(skill_usage)
    total_references = sum(d["skill_count"] for d in dependencies.values())

    md.append("## Summary Statistics")
    md.append("")
    md.append(f"- **Total Agents**: {total_agents}")
    md.append(f"- **Unique Skills Referenced**: {total_unique_skills}")
    md.append(f"- **Total Skill References**: {total_references}")
    md.append(f"- **Avg Skills per Agent**: {total_references / total_agents:.1f}")
    md.append("")

    # Agent breakdown
    md.append("## Agent Dependencies")
    md.append("")
    md.append("| Agent | Skills Referenced | Count |")
    md.append("|-------|-------------------|-------|")

    for agent_slug in sorted(dependencies.keys()):
        data = dependencies[agent_slug]
        skills_preview = ", ".join(data["skills"][:3])
        if data["skill_count"] > 3:
            skills_preview += f", ... (+{data['skill_count'] - 3} more)"
        md.append(f"| {agent_slug} | {skills_preview} | {data['skill_count']} |")

    md.append("")

    # Skill usage (reverse mapping)
    md.append("## Skill Usage by Agents")
    md.append("")
    md.append("| Skill | Used By Agents | Count |")
    md.append("|-------|----------------|-------|")

    for skill_slug in sorted(skill_usage.keys(), key=lambda s: len(skill_usage[s]), reverse=True):
        agents_list = skill_usage[skill_slug]
        count = len(agents_list)
        agents_preview = ", ".join(agents_list[:2])
        if count > 2:
            agents_preview += f", ... (+{count - 2} more)"
        md.append(f"| {skill_slug} | {agents_preview} | {count} |")

    md.append("")

    # Insights
    md.append("## Insights")
    md.append("")

    # Orphaned skills (not referenced by any agent)
    all_skills = {s["slug"] for s in load_skills_index()}
    orphaned_skills = all_skills - skill_usage.keys()

    md.append(f"### Orphaned Skills ({len(orphaned_skills)})")
    md.append("")
    md.append("Skills not referenced by any agent (directly user-invoked or routing-based):")
    md.append("")
    for skill in sorted(orphaned_skills)[:20]:  # Show first 20
        md.append(f"- `{skill}`")
    if len(orphaned_skills) > 20:
        md.append(f"- ... and {len(orphaned_skills) - 20} more")
    md.append("")

    # Heavily used skills
    heavily_used = [(s, len(agents)) for s, agents in skill_usage.items() if len(agents) >= 2]
    if heavily_used:
        md.append(f"### Heavily Referenced Skills ({len(heavily_used)})")
        md.append("")
        md.append("Skills used by multiple agents:")
        md.append("")
        for skill, count in sorted(heavily_used, key=lambda x: x[1], reverse=True):
            agents_str = ", ".join(skill_usage[skill])
            md.append(f"- **{skill}** ({count} agents): {agents_str}")
        md.append("")

    # Agents with no skill dependencies
    no_deps = [a for a, d in dependencies.items() if d["skill_count"] == 0]
    if no_deps:
        md.append(f"### Agents with No Skill Dependencies ({len(no_deps)})")
        md.append("")
        for agent in no_deps:
            md.append(f"- `{agent}`")
        md.append("")

    # Dependency graph visualization
    md.append("## Dependency Graph Visualization")
    md.append("")
    md.append(generate_mermaid_diagram(dependencies))
    md.append("")

    return "\n".join(md)


def main() -> None:
    print("Analyzing agent→skill dependencies...")

    dependencies, skill_usage = build_dependency_graph()

    print(f"Found {len(dependencies)} agents")
    print(f"Found {len(skill_usage)} unique skill references")

    # Generate report
    report = generate_markdown_report(dependencies, skill_usage)

    output_path = Path(__file__).parent.parent / "docs" / "AGENT_DEPENDENCIES.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report)

    print(f"Dependency graph written to: {output_path}")

    # Quick summary
    print("\nQuick Summary:")
    print(f"  Total agents: {len(dependencies)}")
    print(f"  Skills referenced: {len(skill_usage)}")
    print(
        f"  Orphaned skills: {len({s['slug'] for s in load_skills_index()} - skill_usage.keys())}"
    )


if __name__ == "__main__":
    main()
