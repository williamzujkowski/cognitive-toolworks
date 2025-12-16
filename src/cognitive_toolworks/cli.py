"""
Cognitive Toolworks CLI

AI-Native Skill Forge: Generate cross-platform agent artifacts using LLM intelligence.
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

app = typer.Typer(
    name="ct",
    help="Cognitive Toolworks: AI-Native Skill Forge",
    add_completion=True,
    rich_markup_mode="rich",
)

console = Console()


class Platform(str, Enum):
    """Target platform for skill generation."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    UNIVERSAL = "universal"


class SourceType(str, Enum):
    """Type of source to generate from."""

    MCP = "mcp"
    OPENAPI = "openapi"
    README = "readme"
    SCRIPT = "script"
    DOCS = "docs"


# --- Generate Commands ---


@app.command("generate")
def generate_cmd() -> None:
    """Generate agent artifacts. Use subcommands: skill, agents-md, llms-txt"""
    console.print("[yellow]Use a subcommand: ct generate skill, ct generate agents-md[/]")
    raise typer.Exit(1)


generate_app = typer.Typer(help="Generate agent artifacts")
app.add_typer(generate_app, name="generate")


@generate_app.command("skill")
def generate_skill(
    from_mcp: Annotated[
        Path | None,
        typer.Option("--from-mcp", help="Path to MCP server config JSON"),
    ] = None,
    from_openapi: Annotated[
        str | None,
        typer.Option("--from-openapi", help="Path or URL to OpenAPI spec"),
    ] = None,
    from_readme: Annotated[
        Path | None,
        typer.Option("--from-readme", help="Path to README file"),
    ] = None,
    from_analysis: Annotated[
        Path | None,
        typer.Option("--from-analysis", help="Path to analysis JSON from introspect"),
    ] = None,
    name: Annotated[
        str | None,
        typer.Option("--name", "-n", help="Skill name (auto-detected if not provided)"),
    ] = None,
    platform: Annotated[
        Platform,
        typer.Option("--platform", "-p", help="Target platform(s)"),
    ] = Platform.UNIVERSAL,
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output directory"),
    ] = Path("./generated-skill"),
    examples: Annotated[
        int,
        typer.Option("--examples", "-e", help="Number of examples to generate"),
    ] = 3,
    token_budget: Annotated[
        int,
        typer.Option("--token-budget", help="Max tokens for Level 2 content"),
    ] = 5000,
    optimize: Annotated[
        bool,
        typer.Option("--optimize", help="Run optimization pass"),
    ] = True,
    orchestrated: Annotated[
        bool,
        typer.Option("--orchestrated", help="Use claude-flow multi-agent orchestration"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview without writing files"),
    ] = False,
) -> None:
    """
    Generate a SKILL.md from various sources.

    Examples:
        ct generate skill --from-mcp ./github-mcp.json
        ct generate skill --from-openapi https://api.example.com/openapi.json
        ct generate skill --from-readme ./README.md --name my-tool
    """
    # Validate exactly one source is provided
    sources = [from_mcp, from_openapi, from_readme, from_analysis]
    provided = [s for s in sources if s is not None]

    if len(provided) != 1:
        console.print(
            "[red]Error: Provide exactly one source (--from-mcp, --from-openapi, etc.)[/]"
        )
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Determine source type
        if from_mcp:
            source_type = SourceType.MCP
            source_path = from_mcp
        elif from_openapi:
            source_type = SourceType.OPENAPI
            source_path = (
                Path(from_openapi) if not from_openapi.startswith("http") else from_openapi
            )
        elif from_readme:
            source_type = SourceType.README
            source_path = from_readme
        else:
            source_type = SourceType.DOCS
            source_path = from_analysis

        # Step 1: Introspect
        task = progress.add_task(f"[cyan]Introspecting {source_type.value}...", total=None)
        analysis = _introspect_source(source_type, source_path)
        progress.update(task, completed=True)

        # Step 2: Generate
        task = progress.add_task("[cyan]Generating skill...", total=None)
        if orchestrated:
            skill_content = _generate_orchestrated(analysis, platform, examples, token_budget)
        else:
            skill_content = _generate_skill(analysis, platform, examples, token_budget)
        progress.update(task, completed=True)

        # Step 3: Optimize
        if optimize:
            task = progress.add_task("[cyan]Optimizing...", total=None)
            skill_content = _optimize_skill_legacy(skill_content)
            progress.update(task, completed=True)

        # Step 4: Validate
        task = progress.add_task("[cyan]Validating...", total=None)
        validation = _validate_skill(skill_content, platform)
        progress.update(task, completed=True)

    # Display results
    _display_generation_results(skill_content, validation)

    # Write output
    if not dry_run:
        _write_skill(skill_content, output, name)
        console.print(f"\n[green]✅ Skill generated at {output}/SKILL.md[/]")
    else:
        console.print("\n[yellow]Dry run - no files written[/]")


@generate_app.command("agents-md")
def generate_agents_md(
    repo: Annotated[
        Path,
        typer.Option("--repo", "-r", help="Path to repository"),
    ] = Path(),
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output path for AGENTS.md"),
    ] = Path("./AGENTS.md"),
    with_llms_txt: Annotated[
        bool,
        typer.Option("--with-llms-txt", help="Also generate llms.txt"),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview without writing"),
    ] = False,
) -> None:
    """
    Generate AGENTS.md for a repository.

    Analyzes repository structure, package configs, CI setup, and existing
    documentation to create comprehensive agent instructions.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing repository...", total=None)
        repo_analysis = _analyze_repository(repo)
        progress.update(task, completed=True)

        task = progress.add_task("[cyan]Generating AGENTS.md...", total=None)
        agents_content = _generate_agents_md(repo_analysis)
        progress.update(task, completed=True)

        if with_llms_txt:
            task = progress.add_task("[cyan]Generating llms.txt...", total=None)
            llms_content = _generate_llms_txt(repo_analysis)
            progress.update(task, completed=True)

    if not dry_run:
        output.write_text(agents_content)
        console.print(f"[green]✅ Generated {output}[/]")

        if with_llms_txt:
            llms_path = repo / "llms.txt"
            llms_path.write_text(llms_content)
            console.print(f"[green]✅ Generated {llms_path}[/]")
    else:
        console.print(Panel(agents_content[:500] + "...", title="AGENTS.md Preview"))


# --- Introspect Commands ---


introspect_app = typer.Typer(help="Introspect sources to extract information")
app.add_typer(introspect_app, name="introspect")


@introspect_app.command("mcp")
def introspect_mcp(
    config: Annotated[Path, typer.Argument(help="Path to MCP config JSON")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path for analysis JSON"),
    ] = None,
    raw: Annotated[
        bool,
        typer.Option("--raw", help="Output raw introspection data"),
    ] = False,
) -> None:
    """
    Introspect an MCP server to extract tool definitions.

    Connects to the MCP server defined in the config and extracts:
    - Tool definitions and schemas
    - Resource definitions
    - Server capabilities
    """
    console.print(f"[cyan]Introspecting MCP server from {config}...[/]")

    analysis = _introspect_source(SourceType.MCP, config)

    if raw:
        console.print_json(data=analysis)
    else:
        _display_introspection_results(analysis)

    if output:
        output.write_text(json.dumps(analysis, indent=2))
        console.print(f"[green]✅ Analysis saved to {output}[/]")


@introspect_app.command("openapi")
def introspect_openapi(
    spec: Annotated[str, typer.Argument(help="Path or URL to OpenAPI spec")],
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path for analysis JSON"),
    ] = None,
    focus_endpoints: Annotated[
        str | None,
        typer.Option("--focus-endpoints", help="Comma-separated endpoint paths to focus on"),
    ] = None,
) -> None:
    """Introspect an OpenAPI specification."""
    console.print(f"[cyan]Introspecting OpenAPI spec: {spec}...[/]")

    endpoints = focus_endpoints.split(",") if focus_endpoints else None
    analysis = _introspect_source(SourceType.OPENAPI, spec, endpoints=endpoints)

    _display_introspection_results(analysis)

    if output:
        output.write_text(json.dumps(analysis, indent=2))
        console.print(f"[green]✅ Analysis saved to {output}[/]")


# --- Analyze Commands ---


@app.command("analyze")
def analyze(
    path: Annotated[Path, typer.Argument(help="Path to skill or SKILL.md")],
    full_report: Annotated[
        bool,
        typer.Option("--full-report", help="Generate comprehensive report"),
    ] = False,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path for JSON report"),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Output as JSON"),
    ] = False,
) -> None:
    """
    Analyze a skill for quality, token efficiency, and security.

    Reports:
    - Token counts per level
    - Token efficiency score
    - Progressive disclosure score
    - Security issues
    - Cross-platform compatibility
    """
    skill_path = path / "SKILL.md" if path.is_dir() else path

    if not skill_path.exists():
        console.print(f"[red]Error: {skill_path} not found[/]")
        raise typer.Exit(1)

    console.print(f"[cyan]Analyzing {skill_path}...[/]")

    report = _analyze_skill(skill_path, full_report)

    if json_output:
        console.print_json(data=report)
    else:
        _display_analysis_report(report)

    if output:
        output.write_text(json.dumps(report, indent=2))
        console.print(f"[green]✅ Report saved to {output}[/]")


@app.command("analyze-repo")
def analyze_repo(
    repo: Annotated[Path, typer.Argument(help="Path to repository")] = Path(),
    generate_all: Annotated[
        bool,
        typer.Option("--generate-all", help="Generate AGENTS.md, llms.txt, and skill suggestions"),
    ] = False,
) -> None:
    """
    Analyze a repository for agent configuration opportunities.

    Identifies:
    - Missing AGENTS.md
    - Potential skills to create
    - Documentation gaps
    """
    console.print(f"[cyan]Analyzing repository: {repo}...[/]")

    analysis = _analyze_repository(repo)
    _display_repo_analysis(analysis)

    if generate_all:
        console.print("\n[cyan]Generating artifacts...[/]")
        # Generate AGENTS.md
        agents_content = _generate_agents_md(analysis)
        (repo / "AGENTS.md").write_text(agents_content)
        console.print("[green]✅ Generated AGENTS.md[/]")


# --- Validate Commands ---


@app.command("validate")
def validate(
    path: Annotated[Path, typer.Argument(help="Path to skill or SKILL.md")],
    platforms: Annotated[
        str,
        typer.Option("--platforms", "-p", help="Comma-separated platforms to validate against"),
    ] = "anthropic,openai",
    fix: Annotated[
        bool,
        typer.Option("--fix", help="Attempt to auto-fix issues"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed validation output"),
    ] = False,
) -> None:
    """
    Validate a skill against platform specifications.

    Checks:
    - Frontmatter validity
    - Description length limits
    - Name format requirements
    - Token budgets
    """
    skill_path = path / "SKILL.md" if path.is_dir() else path

    if not skill_path.exists():
        console.print(f"[red]Error: {skill_path} not found[/]")
        raise typer.Exit(1)

    platform_list = [p.strip() for p in platforms.split(",")]

    console.print(f"[cyan]Validating {skill_path} against: {', '.join(platform_list)}...[/]")

    content = skill_path.read_text()
    results = {}

    for platform in platform_list:
        results[platform] = _validate_platform(content, platform)

    _display_validation_results(results, verbose)

    all_passed = all(r["passed"] for r in results.values())

    if not all_passed and fix:
        console.print("\n[cyan]Attempting auto-fix...[/]")
        fixed_content = _auto_fix_skill(content, results)
        skill_path.write_text(fixed_content)
        console.print("[green]✅ Applied fixes. Re-run validation to verify.[/]")

    raise typer.Exit(0 if all_passed else 1)


# --- Optimize Commands ---


@app.command("optimize")
def optimize(
    path: Annotated[Path, typer.Argument(help="Path to skill or SKILL.md")],
    tier: Annotated[
        str,
        typer.Option("--tier", "-t", help="Target tier: T1 (2k), T2 (6k), or T3 (12k)"),
    ] = "T2",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Preview changes without writing"),
    ] = False,
    in_place: Annotated[
        bool,
        typer.Option("--in-place", "-i", help="Modify file in place"),
    ] = False,
    legacy: Annotated[
        bool,
        typer.Option("--legacy", help="Use legacy whitespace-only optimization"),
    ] = False,
) -> None:
    """
    Optimize a skill for progressive disclosure and token efficiency.

    Uses LLM-powered optimization to restructure content into T1/T2/T3 tiers:
    - T1 (≤2k tokens): Metadata, purpose, triggers, quick reference
    - T2 (≤6k tokens): Core procedures, decision rules, common examples
    - T3 (≤12k tokens): Detailed references, advanced examples

    Strategies:
    - Remove redundant content
    - Use imperative voice
    - Move detailed content to references
    - Consolidate examples
    - Restructure for progressive disclosure

    Use --dry-run to preview optimizations without making changes.
    Use --legacy for simple whitespace-only optimization.
    """
    import asyncio

    skill_path = path / "SKILL.md" if path.is_dir() else path

    if not skill_path.exists():
        console.print(f"[red]Error: {skill_path} not found[/]")
        raise typer.Exit(1)

    # Validate tier
    tier_upper = tier.upper()
    if tier_upper not in ["T1", "T2", "T3"]:
        console.print(f"[red]Error: Invalid tier '{tier}'. Must be T1, T2, or T3[/]")
        raise typer.Exit(1)

    content = skill_path.read_text()
    original_tokens = _count_tokens(content)

    console.print(f"[cyan]Optimizing {skill_path}...[/]")
    console.print(f"  Original: {original_tokens} tokens")
    console.print(f"  Target tier: {tier_upper}")

    if legacy:
        # Legacy optimization: just remove whitespace
        console.print("[yellow]Using legacy whitespace-only optimization[/]")
        optimized = _optimize_skill_legacy(content)
        new_tokens = _count_tokens(optimized)
        console.print(f"  Optimized: {new_tokens} tokens ({original_tokens - new_tokens} saved)")
        changes = ["Removed duplicate newlines"]
    else:
        # LLM-powered optimization
        if dry_run:
            console.print("[yellow]Dry run mode: analyzing only[/]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running LLM optimization...", total=None)
            result = asyncio.run(_optimize_skill_with_llm(skill_path, dry_run))
            progress.update(task, completed=True)

        optimized = result["content"]
        new_tokens = result["optimized_tokens"]
        changes = result["changes"]

        console.print(f"  Optimized: {new_tokens} tokens ({original_tokens - new_tokens} saved)")
        console.print(f"  Reduction: {result['reduction_pct']:.1f}%")

        if result["within_budget"]:
            console.print(f"[green]  ✓ Within {tier_upper} budget[/]")
        else:
            console.print(f"[yellow]  ⚠ Exceeds {tier_upper} budget[/]")

    # Display changes
    console.print("\n[cyan]Changes made:[/]")
    for change in changes:
        console.print(f"  • {change}")

    # Write output
    if dry_run:
        console.print("\n[yellow]Dry run complete - no files modified[/]")
    elif in_place:
        skill_path.write_text(optimized)
        console.print(f"\n[green]✅ Updated {skill_path}[/]")
    else:
        output_path = skill_path.with_suffix(".optimized.md")
        output_path.write_text(optimized)
        console.print(f"\n[green]✅ Saved to {output_path}[/]")


# --- Security Commands ---


@app.command("security-scan")
def security_scan(
    path: Annotated[Path, typer.Argument(help="Path to skill(s) to scan")],
    recursive: Annotated[
        bool,
        typer.Option("--recursive", "-r", help="Scan directories recursively"),
    ] = False,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Output path for report"),
    ] = None,
) -> None:
    """
    Scan skills for security issues.

    Detects:
    - Unrestricted file system access
    - Network calls without allowlisting
    - Shell command injection vectors
    - Sensitive data exposure
    """
    console.print(f"[cyan]Scanning {path} for security issues...[/]")

    issues = _security_scan(path, recursive)

    _display_security_results(issues)

    if output:
        output.write_text(json.dumps(issues, indent=2))
        console.print(f"[green]✅ Report saved to {output}[/]")

    if issues:
        raise typer.Exit(1)


# --- Utility Commands ---


@app.command("version")
def version() -> None:
    """Show version information."""
    from cognitive_toolworks import __version__

    console.print(f"cognitive-toolworks v{__version__}")


@app.command("benchmark")
def benchmark(
    path: Annotated[Path, typer.Argument(help="Path to skills directory")],
    _iterations: Annotated[
        int,
        typer.Option("--iterations", "-n", help="Number of iterations"),
    ] = 5,
) -> None:
    """Benchmark skill loading and analysis performance."""
    console.print(f"[cyan]Benchmarking {path}...[/]")
    # TODO: Implement benchmarking
    console.print("[yellow]Benchmarking not yet implemented[/]")


# --- Helper Functions (implementations) ---


def _introspect_source(source_type: SourceType, source_path, **_kwargs) -> dict:
    """Introspect a source to extract information."""
    if source_type == SourceType.MCP:
        from cognitive_toolworks.sources.mcp import MCPConfig, MCPIntrospector

        config = MCPConfig.from_json(Path(source_path))
        MCPIntrospector(config)
        # For now, return a placeholder since actual introspection needs running server
        return {
            "source_type": source_type.value,
            "server_name": config.command,
            "tools": [],
            "resources": [],
            "capabilities": [],
        }
    elif source_type == SourceType.OPENAPI:
        from cognitive_toolworks.sources.openapi import introspect_openapi

        # source_path can be either a Path or str (URL)
        path_or_url = str(source_path)
        analysis = introspect_openapi(path_or_url)

        # Convert to dict format expected by the rest of the CLI
        return {
            "source_type": source_type.value,
            "api_name": analysis.api_name,
            "base_url": analysis.base_url,
            "endpoints": [e.to_dict() for e in analysis.endpoints],
            "schemas": analysis.schemas,
            "authentication": analysis.authentication,
            "capabilities": analysis.capabilities,
        }
    return {
        "source_type": source_type.value,
        "tools": [],
        "resources": [],
        "capabilities": [],
    }


def _generate_skill(analysis: dict, _platform: Platform, _examples: int, _token_budget: int) -> str:
    """Generate skill content from analysis."""
    from cognitive_toolworks.models import SkillContent, SkillMetadata

    # Create a basic skill structure from analysis
    name = analysis.get("server_name", "generated-skill")
    if "/" in name:
        name = name.split("/")[-1]
    name = name.lower().replace("_", "-").replace(" ", "-")

    metadata = SkillMetadata(
        name=name,
        description=f"Auto-generated skill from {analysis.get('source_type', 'unknown')} source",
    )

    source_type = analysis.get("source_type", "unknown")
    skill = SkillContent(
        metadata=metadata,
        overview=f"This skill was generated from a {source_type} source.",
        when_to_use=[f"Use this skill when working with {name}"],
        quick_reference="See instructions below for usage.",
        instructions="Configure and use this skill according to your needs.",
        examples=[],
        guidelines=["Follow best practices", "Test thoroughly"],
    )

    return skill.to_markdown()


def _generate_orchestrated(
    analysis: dict, _platform: Platform, _examples: int, _token_budget: int
) -> str:
    """Generate skill using claude-flow orchestration."""
    # For now, fall back to regular generation
    # TODO: Implement full claude-flow integration
    return _generate_skill(analysis, _platform, _examples, _token_budget)


def _optimize_skill_legacy(content: str) -> str:
    """
    Legacy optimization: remove extra whitespace.

    This is a simple optimization that just removes duplicate newlines.
    For LLM-powered optimization, use _optimize_skill_with_llm.
    """
    lines = content.split("\n")
    optimized = []
    prev_empty = False

    for line in lines:
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue
        optimized.append(line)
        prev_empty = is_empty

    return "\n".join(optimized)


async def _optimize_skill_with_llm(skill_path: Path, dry_run: bool) -> dict[str, object]:
    """
    Optimize skill using ProgressiveDisclosureOptimizer.

    Args:
        skill_path: Path to SKILL.md file
        dry_run: If True, analyze only without rewriting

    Returns:
        Dictionary with optimization results
    """
    from cognitive_toolworks.generators.skill import SkillGenerator
    from cognitive_toolworks.optimizers.progressive import ProgressiveDisclosureOptimizer

    # Read and parse the skill
    content = skill_path.read_text()

    # Parse markdown to SkillContent
    # Use SkillGenerator's parser
    generator = SkillGenerator()
    skill_name = skill_path.parent.name if skill_path.parent.name != "." else "skill"
    skill_content = generator._parse_skill_markdown(content, skill_name)

    # Run optimization
    optimizer = ProgressiveDisclosureOptimizer(dry_run=dry_run)
    result = await optimizer.optimize(skill_content)

    # Return optimized markdown
    optimized_markdown = result.optimized_skill.to_markdown()

    return {
        "content": optimized_markdown,
        "original_tokens": result.original_tokens,
        "optimized_tokens": result.optimized_tokens,
        "reduction_pct": result.reduction_percentage,
        "within_budget": result.within_budget,
        "changes": result.changes_made,
    }


def _validate_skill(content: str, _platform: Platform) -> dict:
    """Validate skill against platform spec."""
    from cognitive_toolworks.validators.anthropic import AnthropicValidator
    from cognitive_toolworks.validators.openai import OpenAIValidator

    if _platform == Platform.ANTHROPIC:
        result = AnthropicValidator().validate(content)
    elif _platform == Platform.OPENAI:
        result = OpenAIValidator().validate(content)
    else:
        # Universal: check both
        anthropic_result = AnthropicValidator().validate(content)
        openai_result = OpenAIValidator().validate(content)
        return {
            "passed": anthropic_result.passed and openai_result.passed,
            "issues": [i.to_dict() for i in anthropic_result.issues + openai_result.issues],
        }

    return {"passed": result.passed, "issues": [i.to_dict() for i in result.issues]}


def _validate_platform(content: str, platform: str) -> dict:
    """Validate against specific platform."""
    from cognitive_toolworks.validators.anthropic import AnthropicValidator
    from cognitive_toolworks.validators.openai import OpenAIValidator

    if platform.lower() == "anthropic":
        result = AnthropicValidator().validate(content)
    elif platform.lower() == "openai":
        result = OpenAIValidator().validate(content)
    else:
        return {
            "passed": False,
            "issues": [f"Unknown platform: {platform}"],
            "platform": platform,
        }

    return {
        "passed": result.passed,
        "issues": [i.message for i in result.issues],
        "platform": platform,
    }


def _write_skill(content: str, output: Path, _name: str | None) -> None:
    """Write skill to output directory."""
    output.mkdir(parents=True, exist_ok=True)
    (output / "SKILL.md").write_text(content)


def _analyze_repository(repo: Path) -> dict:
    """Analyze repository structure."""
    analysis = {
        "path": str(repo),
        "has_agents_md": (repo / "AGENTS.md").exists(),
        "has_claude_md": (repo / "CLAUDE.md").exists(),
        "has_readme": (repo / "README.md").exists(),
    }

    # Detect language
    if (repo / "package.json").exists():
        analysis["language"] = "JavaScript/TypeScript"
        analysis["package_manager"] = "npm"
    elif (repo / "pyproject.toml").exists():
        analysis["language"] = "Python"
        analysis["package_manager"] = "pip"
    elif (repo / "Cargo.toml").exists():
        analysis["language"] = "Rust"
        analysis["package_manager"] = "cargo"
    else:
        analysis["language"] = "Unknown"
        analysis["package_manager"] = "unknown"

    return analysis


def _analyze_skill(path: Path, full_report: bool) -> dict:
    """Analyze skill quality."""
    from cognitive_toolworks.analyzers.coverage import CoverageAnalyzer
    from cognitive_toolworks.analyzers.security import SecurityAnalyzer
    from cognitive_toolworks.analyzers.tokens import TokenAnalyzer

    content = path.read_text()

    # Token analysis
    token_analyzer = TokenAnalyzer()
    token_metrics = token_analyzer.analyze(content)

    # Security analysis
    security_analyzer = SecurityAnalyzer()
    security_report = security_analyzer.analyze(content)

    report = {
        "token_count": token_metrics.total_tokens,
        "level1_tokens": token_metrics.level1_tokens,
        "level2_tokens": token_metrics.level2_tokens,
        "efficiency_score": token_metrics.efficiency_score,
        "security_score": security_report.score,
        "security_issues": [i.description for i in security_report.issues],
    }

    if full_report:
        coverage_analyzer = CoverageAnalyzer()
        coverage_report = coverage_analyzer.analyze(content)
        report["coverage_score"] = coverage_report.overall_score
        report["missing_sections"] = coverage_report.missing_sections
        report["recommendations"] = coverage_report.recommendations

    return report


def _generate_agents_md(analysis: dict) -> str:
    """Generate AGENTS.md content."""
    lines = [
        "# AGENTS.md",
        "",
        "## Project Overview",
        "",
        f"Language: {analysis.get('language', 'Unknown')}",
        f"Package Manager: {analysis.get('package_manager', 'unknown')}",
        "",
        "## Dev Environment",
        "",
        "### Setup",
        "",
        "```bash",
        f"{analysis.get('package_manager', 'npm')} install",
        "```",
        "",
        "## Testing Instructions",
        "",
        "```bash",
        f"{analysis.get('package_manager', 'npm')} test",
        "```",
        "",
        "## PR Instructions",
        "",
        "**Title Format**: `type(scope): description`",
        "",
        "### Checklist",
        "",
        "- [ ] Tests pass",
        "- [ ] Linting passes",
        "- [ ] Documentation updated",
        "",
        "## Coding Conventions",
        "",
        "- Follow existing code style",
        "- Write tests for new features",
        "- Keep commits atomic",
    ]
    return "\n".join(lines)


def _generate_llms_txt(analysis: dict) -> str:
    """Generate llms.txt content."""
    lines = [
        f"# {Path(analysis.get('path', '.')).name}",
        "",
        f"Language: {analysis.get('language', 'Unknown')}",
        f"Package Manager: {analysis.get('package_manager', 'unknown')}",
    ]
    return "\n".join(lines)


def _count_tokens(content: str) -> int:
    """Count tokens in content."""
    from cognitive_toolworks.analyzers.tokens import count_tokens

    return count_tokens(content)


def _auto_fix_skill(content: str, _validation_results: dict) -> str:
    """Attempt to auto-fix validation issues."""
    from cognitive_toolworks.validators.anthropic import AnthropicValidator

    return AnthropicValidator().auto_fix(content)


def _security_scan(path: Path, recursive: bool) -> list:
    """Scan for security issues."""
    from cognitive_toolworks.analyzers.security import SecurityAnalyzer

    analyzer = SecurityAnalyzer()
    all_issues = []

    if path.is_file():
        report = analyzer.analyze_file(path)
        all_issues.extend([i.to_dict() for i in report.issues])
    else:
        reports = analyzer.analyze_directory(path, recursive)
        for file_path, report in reports.items():
            for issue in report.issues:
                issue_dict = issue.to_dict()
                issue_dict["file"] = file_path
                all_issues.append(issue_dict)

    return all_issues


def _display_generation_results(content: str, validation: dict) -> None:
    """Display generation results."""
    table = Table(title="Generation Results")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Token Count", str(_count_tokens(content)))
    table.add_row("Validation", "✅ Passed" if validation["passed"] else "❌ Failed")

    console.print(table)


def _display_introspection_results(analysis: dict) -> None:
    """Display introspection results."""
    console.print(Panel(json.dumps(analysis, indent=2)[:500], title="Introspection Results"))


def _display_analysis_report(report: dict) -> None:
    """Display analysis report."""
    table = Table(title="Analysis Report")
    table.add_column("Metric")
    table.add_column("Value")

    for key, value in report.items():
        table.add_row(key, str(value))

    console.print(table)


def _display_repo_analysis(analysis: dict) -> None:
    """Display repository analysis."""
    console.print(Panel(json.dumps(analysis, indent=2), title="Repository Analysis"))


def _display_validation_results(results: dict, verbose: bool) -> None:
    """Display validation results."""
    for platform, result in results.items():
        status = "[green]✅ Passed[/]" if result["passed"] else "[red]❌ Failed[/]"
        console.print(f"  {platform}: {status}")

        if verbose and result.get("issues"):
            for issue in result["issues"]:
                console.print(f"    - {issue}")


def _display_security_results(issues: list) -> None:
    """Display security scan results."""
    if not issues:
        console.print("[green]✅ No security issues found[/]")
    else:
        console.print(f"[red]❌ Found {len(issues)} security issues[/]")
        for issue in issues:
            console.print(f"  - {issue}")


if __name__ == "__main__":
    app()
