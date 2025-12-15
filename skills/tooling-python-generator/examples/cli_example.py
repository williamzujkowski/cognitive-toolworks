#!/usr/bin/env python3
"""Python CLI Example: file line counter with Click.

Demonstrates: Click framework, file I/O, type hints, error handling
"""

from pathlib import Path

import click


@click.command()
@click.argument("file_path", type=click.Path(exists=True, path_type=Path))
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def count_lines(file_path: Path, verbose: bool) -> None:
    """Count lines in a file."""
    try:
        lines = file_path.read_text().splitlines()
        count = len(lines)

        if verbose:
            click.echo(f"File: {file_path}")
            click.echo(f"Lines: {count}")
        else:
            click.echo(count)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort from None


if __name__ == "__main__":
    count_lines()
