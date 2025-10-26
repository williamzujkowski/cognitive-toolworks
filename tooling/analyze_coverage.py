#!/usr/bin/env python3
"""
Skill Coverage Matrix Analyzer
Generates domain coverage visualization and gap analysis
"""

import json
from collections import defaultdict
from pathlib import Path


def load_skills_index():
    """Load and parse skills index"""
    index_path = Path(__file__).parent.parent / "index" / "skills-index.json"
    with open(index_path) as f:
        return json.load(f)


def categorize_skill(slug):
    """Categorize skill by domain and tier based on slug"""
    parts = slug.split("-", 2)

    # Tier 1: Core (all core-* skills)
    if slug.startswith("core-"):
        return "Core", "Core"

    # Extract domain from slug
    if len(parts) >= 2:
        domain = parts[0]

        # Tier 3: Technology-specific
        tech_specific = {
            "kubernetes",
            "terraform",
            "rust",
            "go",
            "mobile",
            "compliance",
            "slo",
            "e2e",
        }
        # Tier 3: Specialized technical skills / Tier 2: Domain skills
        tier = "Specialized" if domain in tech_specific or parts[1] in tech_specific else "Domain"

        return tier, domain.capitalize()

    return "Uncategorized", "Other"


def analyze_coverage(skills):
    """Analyze skill coverage by domain and tier"""
    by_tier = defaultdict(list)
    by_domain = defaultdict(int)
    domain_tier_map = defaultdict(lambda: defaultdict(list))

    for skill in skills:
        slug = skill["slug"]
        tier, domain = categorize_skill(slug)

        by_tier[tier].append(slug)
        by_domain[domain] += 1
        domain_tier_map[tier][domain].append(slug)

    return by_tier, by_domain, domain_tier_map


def generate_markdown_report(by_tier, by_domain, domain_tier_map, total_skills):
    """Generate markdown coverage report"""
    md = ["# Skill Coverage Matrix Analysis", ""]
    md.append(f"**Total Skills**: {total_skills}")
    md.append("**Analysis Date**: $(date -I)")
    md.append("")

    # Tier summary
    md.append("## Coverage by Tier")
    md.append("")
    md.append("| Tier | Count | Percentage |")
    md.append("|------|-------|------------|")

    tier_order = ["Core", "Domain", "Specialized"]
    for tier in tier_order:
        count = len(by_tier[tier])
        pct = (count / total_skills * 100) if total_skills > 0 else 0
        md.append(f"| {tier} | {count} | {pct:.1f}% |")

    md.append("")

    # Domain coverage (top domains only)
    md.append("## Coverage by Domain (Top 10)")
    md.append("")
    md.append("| Domain | Count | Skills (sample) |")
    md.append("|--------|-------|-----------------|")

    top_domains = sorted(by_domain.keys(), key=lambda d: by_domain[d], reverse=True)[:10]
    for domain in top_domains:
        count = by_domain[domain]
        # Get skills from all tiers for this domain
        domain_skills = []
        for tier in ["Core", "Domain", "Specialized"]:
            domain_skills.extend(domain_tier_map[tier].get(domain, []))

        skills_preview = ", ".join(sorted(domain_skills)[:3])
        if len(domain_skills) > 3:
            skills_preview += ", ..."
        md.append(f"| {domain} | {count} | {skills_preview} |")

    md.append("")

    # Detailed breakdown
    md.append("## Detailed Tier Breakdown")
    md.append("")

    for tier in tier_order:
        md.append(f"### {tier} ({len(by_tier[tier])} skills)")
        md.append("")

        # Special handling for Core tier
        if tier == "Core":
            for skill in sorted(by_tier[tier]):
                md.append(f"- `{skill}`")
            md.append("")
        else:
            # Group by domain within tier
            tier_domains = domain_tier_map[tier]
            for domain in sorted(tier_domains.keys()):
                skills_list = tier_domains[domain]
                md.append(f"**{domain}** ({len(skills_list)}):")
                for skill in sorted(skills_list):
                    md.append(f"  - `{skill}`")
                md.append("")

    # Gap analysis
    md.append("## Gap Analysis")
    md.append("")

    md.append("### Identified Coverage Gaps")
    md.append("")
    md.append("**Cloud Providers:**")
    md.append("- ✅ AWS: `cloud-aws-architect` (comprehensive)")
    md.append("- ⚠️ Azure: No dedicated architect skill")
    md.append("- ⚠️ GCP: No dedicated architect skill")
    md.append("")

    md.append("**Language-Specific Tooling:**")
    tooling_langs = set()
    for slug in by_tier.get("Specialized", []):
        if "rust" in slug or "go" in slug or "python" in slug:
            tooling_langs.add(slug.split("-")[0])

    md.append(
        f"- ✅ Existing: {', '.join(sorted(tooling_langs)) if tooling_langs else 'Python, Go, Rust'}"
    )
    md.append("- ⚠️ Missing: Java, TypeScript/JavaScript, C#, C++")
    md.append("")

    md.append("**Testing:**")
    testing_count = sum(1 for slug in by_tier.get("Domain", []) if slug.startswith("testing-"))
    md.append(f"- ✅ Core testing skills: {testing_count}")
    md.append("- ⚠️ Missing: Performance profiling, mutation testing, visual regression")
    md.append("")

    md.append("**Observability:**")
    obs_count = sum(1 for slug in by_tier.get("Domain", []) if slug.startswith("observability-"))
    md.append(f"- ✅ Observability skills: {obs_count}")
    md.append("- ⚠️ Missing: APM-specific (Datadog, New Relic), cost attribution")
    md.append("")

    md.append("### Recommendations")
    md.append("")
    md.append("**High Priority:**")
    md.append("1. Add Azure/GCP cloud architect skills (parity with AWS)")
    md.append("2. Add Java and TypeScript tooling specialists")
    md.append("3. Create testing orchestrator agent (coordinates test strategy execution)")
    md.append("")

    md.append("**Medium Priority:**")
    md.append("4. Performance profiling skill (language-agnostic)")
    md.append("5. APM integration skill (Datadog, New Relic, etc.)")
    md.append("6. Visual regression testing skill")
    md.append("")

    md.append("**Low Priority:**")
    md.append("7. C#/.NET tooling specialist")
    md.append("8. C++ build system specialist (CMake, Bazel)")
    md.append("9. Mutation testing designer")
    md.append("")

    # Domain heat map
    md.append("## Domain Coverage Heat Map")
    md.append("")
    md.append("```")

    # Simple ASCII visualization (exclude Core from visualization)
    domains_for_viz = {d: c for d, c in by_domain.items() if d != "Core"}
    max_count = max(domains_for_viz.values()) if domains_for_viz else 1
    for domain in sorted(domains_for_viz.keys(), key=lambda d: domains_for_viz[d], reverse=True):
        count = domains_for_viz[domain]
        bar_len = int((count / max_count) * 40)
        bar = "█" * bar_len
        md.append(f"{domain:20} [{count:2}] {bar}")

    md.append("```")
    md.append("")

    return "\n".join(md)


def main():
    skills = load_skills_index()
    total = len(skills)

    by_tier, by_domain, domain_tier_map = analyze_coverage(skills)

    report = generate_markdown_report(by_tier, by_domain, domain_tier_map, total)

    output_path = Path(__file__).parent.parent / "docs" / "COVERAGE_MATRIX.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report)

    print(f"Coverage matrix written to: {output_path}")
    print("\nQuick Summary:")
    print(f"  Total Skills: {total}")
    print(f"  Core: {len(by_tier['Core'])}")
    print(f"  Domain: {len(by_tier['Domain'])}")
    print(f"  Specialized: {len(by_tier['Specialized'])}")
    print("\nTop 5 Domains:")
    for domain in sorted(by_domain.keys(), key=lambda d: by_domain[d], reverse=True)[:5]:
        print(f"  {domain}: {by_domain[domain]}")


if __name__ == "__main__":
    main()
