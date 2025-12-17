#!/usr/bin/env python3
"""Validate instruction file consistency and sync status.

This script checks that CLAUDE.md, AGENTS.md, and GEMINI.md stay consistent
where content overlaps and validates their structure.

Usage:
    python tooling/validate_instructions.py [--check-tokens] [--check-sync] [--check-imports]
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import tiktoken

    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


def count_tokens(content: str) -> int:
    """Count tokens using tiktoken cl100k_base encoding."""
    if not HAS_TIKTOKEN:
        # Fallback: rough estimate of 4 chars per token
        return len(content) // 4

    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(content))


def check_file_exists(filepath: Path) -> bool:
    """Check if an instruction file exists."""
    return filepath.exists() and filepath.is_file()


def validate_token_budgets(root: Path) -> list[str]:
    """Validate instruction files stay within token limits."""
    errors = []
    limits = {
        "CLAUDE.md": 7000,  # Allow some buffer over 6000 self-declared limit
        "AGENTS.md": 3000,
        "GEMINI.md": 1000,
    }

    for filename, limit in limits.items():
        filepath = root / filename
        if not check_file_exists(filepath):
            continue

        content = filepath.read_text()
        tokens = count_tokens(content)

        if tokens > limit:
            errors.append(
                f"{filename}: {tokens} tokens exceeds limit of {limit} "
                f"(over by {tokens - limit})"
            )
        else:
            print(f"  {filename}: {tokens} tokens (limit: {limit})")

    return errors


def validate_gemini_imports(root: Path) -> list[str]:
    """Validate GEMINI.md imports resolve correctly."""
    errors: list[str] = []
    gemini_path = root / "GEMINI.md"

    if not check_file_exists(gemini_path):
        return errors

    content = gemini_path.read_text()

    # Find all @file.md imports (supports @./file.md, @../file.md, @file.md)
    import_pattern = re.compile(r"^@(\.{0,2}/[^\s]+\.md|[^\s]+\.md)$", re.MULTILINE)
    imports = import_pattern.findall(content)

    for import_path in imports:
        # Resolve relative path
        if import_path.startswith("./"):
            resolved = root / import_path[2:]
        elif import_path.startswith("../"):
            resolved = root.parent / import_path[3:]
        elif import_path.startswith("/"):
            resolved = Path(import_path)
        else:
            resolved = root / import_path

        if not check_file_exists(resolved):
            errors.append(f"GEMINI.md: Import '@{import_path}' not found at {resolved}")
        else:
            print(f"  Import @{import_path} -> {resolved}")

    return errors


def validate_shared_concepts(root: Path) -> list[str]:
    """Check that shared concepts are consistent across files."""
    errors: list[str] = []
    warnings: list[str] = []

    claude_path = root / "CLAUDE.md"
    agents_path = root / "AGENTS.md"

    if not check_file_exists(claude_path) or not check_file_exists(agents_path):
        return errors

    claude_content = claude_path.read_text().lower()
    agents_content = agents_path.read_text().lower()

    # Shared concepts that should appear in both files
    shared_concepts = {
        "testing": ["pytest", "coverage"],
        "code_quality": ["ruff", "black", "mypy"],
        "security": ["gitleaks", "pre-commit"],
        "python_version": ["python 3.11", "3.11+"],
    }

    for concept, keywords in shared_concepts.items():
        claude_has = any(kw in claude_content for kw in keywords)
        agents_has = any(kw in agents_content for kw in keywords)

        if claude_has and agents_has:
            print(f"  {concept}: Present in both files")
        elif claude_has and not agents_has:
            warnings.append(f"{concept}: Found in CLAUDE.md but not AGENTS.md")
        elif agents_has and not claude_has:
            warnings.append(f"{concept}: Found in AGENTS.md but not CLAUDE.md")

    # Warnings are informational, not errors (files serve different purposes)
    for warning in warnings:
        print(f"  [INFO] {warning}")

    return errors


def validate_structure(root: Path) -> list[str]:
    """Validate basic structure of instruction files."""
    errors = []

    # CLAUDE.md should have numbered sections
    claude_path = root / "CLAUDE.md"
    if check_file_exists(claude_path):
        content = claude_path.read_text()
        if not re.search(r"^## \d+\)", content, re.MULTILINE):
            errors.append("CLAUDE.md: Missing numbered sections (## 0), ## 1), etc.)")
        if "STATUS: AUTHORITATIVE" not in content:
            errors.append("CLAUDE.md: Missing STATUS: AUTHORITATIVE marker")

    # AGENTS.md should have standard sections
    agents_path = root / "AGENTS.md"
    if check_file_exists(agents_path):
        content = agents_path.read_text()
        required_sections = ["Dev Environment", "Testing", "PR"]
        for section in required_sections:
            if section.lower() not in content.lower():
                errors.append(f"AGENTS.md: Missing expected section containing '{section}'")

    # GEMINI.md should import AGENTS.md
    gemini_path = root / "GEMINI.md"
    if check_file_exists(gemini_path):
        content = gemini_path.read_text()
        if "@./AGENTS.md" not in content and "@AGENTS.md" not in content:
            errors.append("GEMINI.md: Should import AGENTS.md using @./AGENTS.md")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate instruction file consistency")
    parser.add_argument(
        "--check-tokens",
        action="store_true",
        help="Check token budgets for each file",
    )
    parser.add_argument(
        "--check-sync",
        action="store_true",
        help="Check shared concepts are consistent",
    )
    parser.add_argument(
        "--check-imports",
        action="store_true",
        help="Check GEMINI.md imports resolve",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all checks",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root directory",
    )

    args = parser.parse_args()

    # Default to all checks if none specified
    if not any([args.check_tokens, args.check_sync, args.check_imports]):
        args.all = True

    root = args.root
    all_errors = []

    print(f"Validating instruction files in: {root}\n")

    # Check files exist
    print("Checking file existence...")
    for filename in ["CLAUDE.md", "AGENTS.md", "GEMINI.md"]:
        filepath = root / filename
        status = "exists" if check_file_exists(filepath) else "MISSING"
        print(f"  {filename}: {status}")
    print()

    # Structure validation (always run)
    print("Validating structure...")
    errors = validate_structure(root)
    all_errors.extend(errors)
    if not errors:
        print("  All structure checks passed")
    print()

    # Token budget check
    if args.all or args.check_tokens:
        print("Checking token budgets...")
        if not HAS_TIKTOKEN:
            print("  [WARN] tiktoken not installed, using estimate")
        errors = validate_token_budgets(root)
        all_errors.extend(errors)
        print()

    # Import validation
    if args.all or args.check_imports:
        print("Validating GEMINI.md imports...")
        errors = validate_gemini_imports(root)
        all_errors.extend(errors)
        if not errors:
            print("  All imports valid")
        print()

    # Shared concept sync
    if args.all or args.check_sync:
        print("Checking shared concept consistency...")
        errors = validate_shared_concepts(root)
        all_errors.extend(errors)
        print()

    # Summary
    if all_errors:
        print("ERRORS FOUND:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("All validation checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
