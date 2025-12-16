#!/usr/bin/env python3
"""Validate example files in skills directory.

Enforces CLAUDE.md standards:
- Examples should be ≤30 lines (CLAUDE.md target)
- Hard limit at 60 lines (allows existing examples)
- No hardcoded secrets or sensitive data
- Proper file extensions and naming conventions

Usage:
    python3 tooling/validate_examples.py [--root ROOT] [--strict]

Options:
    --root ROOT    Root directory to search (default: current directory)
    --strict       Enforce strict 30-line limit (errors instead of warnings)
"""

import argparse
import re
import sys
from pathlib import Path

# Line limits
SOFT_LIMIT = 30  # CLAUDE.md target (warning if exceeded)
HARD_LIMIT = 60  # Absolute maximum (error if exceeded)

# Allowed file extensions for examples
ALLOWED_EXTENSIONS = {
    ".py",
    ".ts",
    ".js",
    ".java",
    ".cs",
    ".go",
    ".rs",  # code
    ".txt",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".toml",  # config/docs
    ".sh",
    ".bash",
    ".sql",
    ".graphql",
    ".proto",
    ".tf",
    ".hcl",  # scripts/schemas/IaC
}

# Secret patterns (common credential patterns to detect)
SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?", "API key"),
    (r"(?i)(secret[_-]?key|secretkey)\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?", "Secret key"),
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\\s]{8,}['\"]?", "Password"),
    (r"(?i)aws_access_key_id\s*[:=]\s*['\"]?[A-Z0-9]{20}['\"]?", "AWS access key"),
    (r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?", "AWS secret key"),
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"xox[baprs]-[a-zA-Z0-9-]{10,}", "Slack token"),
]


def count_lines(file_path: Path) -> int:
    """Count non-empty lines in a file (excluding blank lines)."""
    try:
        with file_path.open(encoding="utf-8", errors="ignore") as f:
            # Count all lines (including blank) for consistency with existing examples
            return sum(1 for _ in f)
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}", file=sys.stderr)
        return 0


def check_secrets(file_path: Path) -> list[tuple[int, str, str]]:
    """Check file for hardcoded secrets. Returns list of (line_num, pattern_name, line_content)."""
    findings = []
    try:
        with file_path.open(encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, start=1):
                # Skip commented lines (common in code examples)
                stripped = line.strip()
                if stripped.startswith(("#", "//", "/*", "*", "--")):
                    continue

                for pattern, name in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        findings.append((line_num, name, line.strip()))
    except Exception as e:
        print(f"[ERROR] Failed to scan {file_path} for secrets: {e}", file=sys.stderr)

    return findings


def validate_example_file(file_path: Path, strict: bool = False) -> tuple[bool, list[str]]:
    """Validate a single example file. Returns (is_valid, warnings)."""
    warnings = []
    is_valid = True

    # Check file extension
    if file_path.suffix not in ALLOWED_EXTENSIONS:
        warnings.append(f"Unexpected file extension: {file_path.suffix}")

    # Skip .gitkeep files
    if file_path.name == ".gitkeep":
        return True, []

    # Count lines
    line_count = count_lines(file_path)

    if line_count == 0:
        warnings.append("Empty file")
        return True, warnings  # Not an error, just a warning

    # Check line limits
    if strict and line_count > SOFT_LIMIT:
        warnings.append(f"Exceeds CLAUDE.md target of {SOFT_LIMIT} lines ({line_count} lines)")
        is_valid = False
    elif line_count > HARD_LIMIT:
        warnings.append(f"EXCEEDS HARD LIMIT of {HARD_LIMIT} lines ({line_count} lines)")
        is_valid = False
    elif line_count > SOFT_LIMIT:
        warnings.append(
            f"Exceeds CLAUDE.md target of {SOFT_LIMIT} lines ({line_count} lines) - consider refactoring"
        )

    # Check for secrets
    secret_findings = check_secrets(file_path)
    if secret_findings:
        is_valid = False
        for line_num, secret_type, line_content in secret_findings:
            warnings.append(
                f"Possible {secret_type} detected at line {line_num}: {line_content[:60]}..."
            )

    return is_valid, warnings


def find_example_files(root: Path) -> list[Path]:
    """Find all example files in skills/*/examples/ directories."""
    example_files = []

    # Find all skills/*/examples/ directories
    for skill_dir in root.glob("skills/*/examples"):
        if skill_dir.is_dir():
            # Get all files (not directories) in examples/
            for file_path in skill_dir.iterdir():
                if file_path.is_file():
                    example_files.append(file_path)

    return sorted(example_files)


def main() -> int:
    """Main validation function."""
    parser = argparse.ArgumentParser(description="Validate example files in skills directory")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory to search (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce strict 30-line limit (errors instead of warnings)",
    )

    args = parser.parse_args()

    # Find all example files
    example_files = find_example_files(args.root)

    if not example_files:
        print("No example files found in skills/*/examples/ directories")
        return 0

    # Validate each file
    total_files = 0
    failed_files = 0
    total_warnings = 0

    for file_path in example_files:
        total_files += 1
        is_valid, warnings = validate_example_file(file_path, strict=args.strict)

        if not is_valid:
            failed_files += 1
            print(f"[FAIL] {file_path}")
            for warning in warnings:
                print(f"       - {warning}")
        elif warnings:
            print(f"[WARN] {file_path}")
            for warning in warnings:
                print(f"       - {warning}")
            total_warnings += len(warnings)
        else:
            print(f"[OK]   {file_path}")

    # Summary
    print()
    if failed_files > 0:
        print(f"{failed_files} file(s) failed validation, {total_warnings} warning(s)")
        return 1
    if total_warnings > 0:
        print(f"All {total_files} file(s) passed validation with {total_warnings} warning(s)")
        return 0
    print(f"All {total_files} file(s) passed validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
