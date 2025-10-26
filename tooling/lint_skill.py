#!/usr/bin/env python3
"""Lint SKILL.md files for style consistency.

Checks:
- Heading order matches CLAUDE.md §3 specification
- Code fences are properly closed
- External links are valid (HTTP status check)
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

FRONT_MATTER_DELIM = re.compile(r"^---\s*$")

# Required body sections in exact order per CLAUDE.md §3
REQUIRED_SECTIONS_ORDER = [
    "## Purpose & When-To-Use",
    "## Pre-Checks",
    "## Procedure",
    "## Decision Rules",
    "## Output Contract",
    "## Examples",
    "## Quality Gates",
    "## Resources",
]


@dataclass
class LintIssue:
    path: Path
    message: str
    severity: str = "ERROR"  # ERROR or WARN


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_body(md_text: str) -> str:
    """Extract body text after front matter."""
    lines = md_text.splitlines()
    if not lines or not FRONT_MATTER_DELIM.match(lines[0]):
        return md_text  # No front matter, return as-is

    # Find closing '---'
    end_idx = None
    for i in range(1, len(lines)):
        if FRONT_MATTER_DELIM.match(lines[i]):
            end_idx = i
            break

    if end_idx is None:
        return md_text

    return "\n".join(lines[end_idx + 1:])


def check_heading_order(body: str, path: Path) -> List[LintIssue]:
    """Verify required sections appear in the correct order."""
    issues: List[LintIssue] = []

    # Find all h2 headings
    h2_pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    found_headings = [m.group(0) for m in h2_pattern.finditer(body)]

    # Extract only the required headings in order they appear
    required_found = [h for h in found_headings if h in REQUIRED_SECTIONS_ORDER]

    # Check if they appear in the correct order
    expected_idx = 0
    for heading in required_found:
        try:
            actual_idx = REQUIRED_SECTIONS_ORDER.index(heading)
            if actual_idx < expected_idx:
                issues.append(
                    LintIssue(
                        path,
                        f"Heading '{heading}' appears out of order (expected after '{REQUIRED_SECTIONS_ORDER[expected_idx - 1] if expected_idx > 0 else 'start'}')",
                    )
                )
            expected_idx = max(expected_idx, actual_idx + 1)
        except ValueError:
            pass  # Heading not in required list, skip

    # Check for missing required sections
    for required in REQUIRED_SECTIONS_ORDER:
        if required not in found_headings:
            issues.append(
                LintIssue(
                    path,
                    f"Missing required section: {required}",
                    severity="WARN",
                )
            )

    return issues


def check_code_fences(body: str, path: Path) -> List[LintIssue]:
    """Verify all code fences are properly closed."""
    issues: List[LintIssue] = []
    fence_pattern = re.compile(r"^```")
    lines = body.splitlines()

    open_line: Optional[int] = None
    for i, line in enumerate(lines, start=1):
        if fence_pattern.match(line):
            if open_line is None:
                open_line = i
            else:
                open_line = None  # Close the fence

    if open_line is not None:
        issues.append(
            LintIssue(
                path,
                f"Unclosed code fence starting at line {open_line}",
            )
        )

    return issues


def extract_links(body: str) -> List[str]:
    """Extract all HTTP(S) URLs from markdown."""
    # Match markdown links [text](url) and bare URLs
    md_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    bare_url_pattern = re.compile(r'https?://[^\s<>"\)]+')

    urls = []

    # Extract from markdown links
    for match in md_link_pattern.finditer(body):
        url = match.group(2)
        if url.startswith(('http://', 'https://')):
            urls.append(url)

    # Extract bare URLs (not already in markdown links)
    body_no_md = md_link_pattern.sub('', body)
    for match in bare_url_pattern.finditer(body_no_md):
        urls.append(match.group(0))

    return list(set(urls))  # Deduplicate


def check_link_validity(url: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """Check if URL is accessible. Returns (is_valid, error_message)."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False, "Invalid URL format"

        # Skip fragment-only or anchor links
        if url.startswith('#'):
            return True, None

        # Make HEAD request to check accessibility
        req = Request(url, method='HEAD')
        req.add_header('User-Agent', 'SkillLinter/1.0')

        with urlopen(req, timeout=timeout) as response:
            if response.status < 400:
                return True, None
            else:
                return False, f"HTTP {response.status}"

    except HTTPError as e:
        return False, f"HTTP {e.code}"
    except URLError as e:
        return False, f"URL error: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def check_links(body: str, path: Path, validate: bool = False) -> List[LintIssue]:
    """Check external links. If validate=True, perform HTTP checks."""
    issues: List[LintIssue] = []
    urls = extract_links(body)

    if not urls:
        return issues

    if validate:
        for url in urls:
            is_valid, error = check_link_validity(url)
            if not is_valid:
                issues.append(
                    LintIssue(
                        path,
                        f"Broken link '{url}': {error}",
                        severity="WARN",
                    )
                )

    return issues


def lint_skill_file(path: Path, validate_links: bool = False) -> List[LintIssue]:
    """Run all lint checks on a SKILL.md file."""
    issues: List[LintIssue] = []

    try:
        content = read_text(path)
        body = extract_body(content)
    except Exception as e:
        issues.append(LintIssue(path, f"Failed to read file: {e}"))
        return issues

    # Run checks
    issues.extend(check_heading_order(body, path))
    issues.extend(check_code_fences(body, path))
    issues.extend(check_links(body, path, validate=validate_links))

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Lint SKILL.md files for style consistency"
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repo root (default: .)",
    )
    ap.add_argument(
        "--validate-links",
        action="store_true",
        help="Perform HTTP validation of external links (slow)",
    )
    args = ap.parse_args()

    root: Path = args.root.resolve()
    skills_dir = root / "skills"

    if not skills_dir.exists():
        print(f"ERROR: skills dir not found: {skills_dir}", file=sys.stderr)
        return 2

    md_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not md_files:
        print("No skills found.")
        return 0

    total_issues: List[LintIssue] = []
    for p in md_files:
        issues = lint_skill_file(p, validate_links=args.validate_links)
        if issues:
            for issue in issues:
                prefix = "[WARN]" if issue.severity == "WARN" else "[FAIL]"
                print(f"{prefix} {issue.path}: {issue.message}")
            total_issues.extend(issues)
        else:
            print(f"[OK]   {p}")

    # Count errors vs warnings
    errors = [i for i in total_issues if i.severity == "ERROR"]
    warnings = [i for i in total_issues if i.severity == "WARN"]

    if total_issues:
        print(
            f"\n{len(errors)} error(s), {len(warnings)} warning(s) across {len(md_files)} file(s).",
            file=sys.stderr,
        )
        # Only fail on errors, not warnings
        return 1 if errors else 0

    print(f"\nAll {len(md_files)} skill(s) passed linting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
