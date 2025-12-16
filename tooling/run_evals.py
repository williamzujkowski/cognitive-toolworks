#!/usr/bin/env python3
"""CLI tool to run evaluation scenarios for cognitive-toolworks skills.

Finds all eval YAML files in tests/ and validates them against expected
structure and criteria.

Usage:
    python tooling/run_evals.py
    python tooling/run_evals.py tests/evals_specific_skill.yaml
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from cognitive_toolworks.testing import EvalRunner


def main() -> int:
    """Run all evaluation scenarios and report results.

    Returns:
        Exit code: 0 if all pass, 1 if any fail
    """
    console = Console()
    runner = EvalRunner()

    # Determine which eval files to run
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"

    if len(sys.argv) > 1:
        # Run specific file(s) provided as arguments
        eval_files = [Path(arg) for arg in sys.argv[1:]]
    else:
        # Find all eval YAML files
        eval_files = sorted(tests_dir.glob("evals_*.yaml"))

    if not eval_files:
        console.print("[yellow]No eval files found in tests/[/yellow]")
        return 0

    console.print(f"\n[bold]Running {len(eval_files)} eval file(s)...[/bold]\n")

    total_scenarios = 0
    total_passed = 0
    total_failed = 0
    failed_files: list[tuple[Path, list[str]]] = []

    for eval_file in eval_files:
        if not eval_file.exists():
            console.print(f"[red]✗[/red] {eval_file.name}: File not found")
            failed_files.append((eval_file, ["File not found"]))
            continue

        try:
            results = runner.run_all(eval_file)
            total_scenarios += len(results)

            passed = sum(1 for r in results if r.passed)
            failed = len(results) - passed
            total_passed += passed
            total_failed += failed

            # Display file summary
            status = "✓" if failed == 0 else "✗"
            color = "green" if failed == 0 else "red"
            console.print(
                f"[{color}]{status}[/{color}] {eval_file.name}: "
                f"{passed}/{len(results)} scenarios passed"
            )

            # Collect failure details
            if failed > 0:
                failure_details = []
                for result in results:
                    if not result.passed:
                        errors = "; ".join(result.errors)
                        failure_details.append(f"  {result.scenario_id}: {errors}")
                failed_files.append((eval_file, failure_details))

        except Exception as e:
            console.print(f"[red]✗[/red] {eval_file.name}: {e}")
            failed_files.append((eval_file, [str(e)]))
            total_failed += 1

    # Summary table
    console.print("\n[bold]Summary:[/bold]")
    table = Table(show_header=True, header_style="bold")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right")

    table.add_row("Total eval files", str(len(eval_files)))
    table.add_row("Total scenarios", str(total_scenarios))
    table.add_row("Passed", f"[green]{total_passed}[/green]")
    table.add_row("Failed", f"[red]{total_failed}[/red]" if total_failed > 0 else "0")

    console.print(table)

    # Show failure details
    if failed_files:
        console.print("\n[bold red]Failures:[/bold red]")
        for eval_file, failure_details in failed_files:
            console.print(f"\n[red]{eval_file.name}:[/red]")
            for error in failure_details:
                console.print(f"  {error}")

    # Exit with appropriate code
    if total_failed > 0:
        console.print("\n[red]❌ Some evaluations failed[/red]")
        return 1
    else:
        console.print("\n[green]✅ All evaluations passed[/green]")
        return 0


if __name__ == "__main__":
    sys.exit(main())
