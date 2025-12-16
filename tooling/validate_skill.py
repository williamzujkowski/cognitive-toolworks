#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped,unused-ignore]
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

try:
    from urllib.parse import urlparse
    from urllib.request import Request, urlopen
except Exception:  # pragma: no cover
    urlparse = None  # type: ignore[assignment]
    urlopen = None  # type: ignore[assignment]

FRONT_MATTER_DELIM = re.compile(r"^---\s*$")
REQ_META_KEYS = {
    "name",
    "slug",
    "description",
    "capabilities",
    "inputs",
    "outputs",
    "keywords",
    "version",
    "owner",
    "license",
    "security",
    "links",
}
REQ_BODY_SECTIONS = [
    "## Purpose & When-To-Use",
    "## Pre-Checks",
    "## Procedure",
    "## Decision Rules",
    "## Output Contract",
    "## Quality Gates",
    "## Resources",
]
MAX_DESCRIPTION_LEN = 160
MAX_EXAMPLE_LINES = 30
MAX_CODEBLOCK_LINES = 200

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key id
    re.compile(r"BEGIN (?:RSA |EC |)PRIVATE KEY"),
    re.compile(r"ssh-rsa "),
    re.compile(r"(?i)password\s*[:=]\s*[^\s]{6,}"),
    re.compile(r"(?i)secret\s*[:=]\s*[^\s]{6,}"),
]


@dataclass
class SkillValidationIssue:
    path: Path
    message: str
    severity: str = "error"  # error or warning


@dataclass
class FrontMatter:
    meta: dict[str, Any]
    body: str


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_front_matter(md_text: str) -> FrontMatter:
    """Extract YAML front matter delimited by '---' at the top of the file."""
    lines = md_text.splitlines()
    if not lines or not FRONT_MATTER_DELIM.match(lines[0]):
        msg = "Missing starting '---' for front matter"
        raise ValueError(msg)
    # find closing '---'
    end_idx = None
    for i in range(1, len(lines)):
        if FRONT_MATTER_DELIM.match(lines[i]):
            end_idx = i
            break
    if end_idx is None:
        msg = "Missing closing '---' for front matter"
        raise ValueError(msg)

    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])

    if yaml is None:
        msg = "PyYAML not installed. Please add 'pyyaml' and re-run validator."
        raise RuntimeError(msg)
    try:
        meta = yaml.safe_load(fm_text) or {}
    except Exception as e:  # pragma: no cover
        msg = f"Failed to parse front matter YAML: {e}"
        raise ValueError(msg) from e

    if not isinstance(meta, dict):
        msg = "Front matter must be a YAML mapping (object)"
        raise ValueError(msg)

    return FrontMatter(meta=meta, body=body)


def find_code_blocks(text: str) -> list[tuple[int, int]]:
    """Return list of (start_line_idx, end_line_idx) for fenced code blocks."""
    blocks: list[tuple[int, int]] = []
    fence = re.compile(r"^```")
    lines = text.splitlines()
    open_idx: int | None = None
    for i, ln in enumerate(lines):
        if fence.match(ln):
            if open_idx is None:
                open_idx = i
            else:
                blocks.append((open_idx, i))
                open_idx = None
    return blocks


def first_examples_block_len(text: str) -> int | None:
    """Return line count of the first code block under '## Examples'."""
    parts = re.split(r"^## Examples\s*$", text, flags=re.M)
    if len(parts) < 2:
        return None
    examples = parts[1]
    blocks = find_code_blocks(examples)
    if not blocks:
        return None
    start, end = blocks[0]
    return max(0, end - start - 1)  # exclude fence lines


def has_token_budgets(text: str) -> bool:
    # simple check for presence of T1/T2/T3 in the Quality Gates or anywhere
    return bool(
        re.search(r"\bT1\b", text) and re.search(r"\bT2\b", text) and re.search(r"\bT3\b", text)
    )


def scan_secrets(text: str) -> str | None:
    for pat in SECRET_PATTERNS:
        m = pat.search(text)
        if m:
            return f"Potential secret matched pattern: {pat.pattern}"
    return None


def extract_urls(text: str) -> list[str]:
    """Extract all HTTP/HTTPS URLs from text."""
    url_pattern = re.compile(r"https?://[^\s\)\]\"'<>]+")
    return url_pattern.findall(text)


def validate_url(url: str, timeout: int = 5) -> tuple[bool, str]:
    """Check if URL is accessible. Returns (is_valid, message)."""
    if urlopen is None:
        return False, "URL validation unavailable (urllib not found)"

    try:
        # Clean up URL (remove trailing punctuation)
        url = url.rstrip(".,;:!?")

        # Basic URL structure check
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False, f"Invalid URL structure: {url}"

        # Try to fetch with a HEAD request first (faster)
        req = Request(url, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0 (SkillValidator/1.0)")

        with urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                return True, "OK"
            return False, f"HTTP {response.status}"
    except Exception as e:
        # Return as warning, not error - links might be temporarily down
        return False, str(e)


def extract_code_blocks_with_lang(text: str) -> list[tuple[str, str]]:
    """Extract code blocks with their language tags. Returns [(lang, code), ...]."""
    blocks: list[tuple[str, str]] = []
    pattern = re.compile(r"^```(\w+)?\s*$", re.MULTILINE)
    lines = text.splitlines()

    i = 0
    while i < len(lines):
        match = pattern.match(lines[i])
        if match:
            lang = match.group(1) or ""
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append((lang, "\n".join(code_lines)))
        i += 1

    return blocks


def validate_code_syntax(lang: str, code: str) -> tuple[bool, str]:
    """Validate code syntax for supported languages. Returns (is_valid, message)."""
    lang = lang.lower()

    if lang in ("python", "py"):
        try:
            ast.parse(code)
            return True, "Valid Python"
        except SyntaxError as e:
            return False, f"Python syntax error: {e.msg} at line {e.lineno}"

    # Add more languages as needed
    # For now, other languages pass validation
    return True, f"Syntax check not implemented for {lang}"


def check_todo_markers(text: str) -> list[str]:
    """Find TODO markers that should not be in committed skills."""
    todo_pattern = re.compile(r"\[TODO:([^\]]+)\]")
    matches = todo_pattern.findall(text)
    return matches


def validate_skill_file(
    path: Path,
    check_links: bool = False,
    check_syntax: bool = False,
    check_todos: bool = False,
) -> list[SkillValidationIssue]:
    issues: list[SkillValidationIssue] = []
    try:
        fm = extract_front_matter(read_text(path))
    except Exception as e:
        issues.append(SkillValidationIssue(path, f"Front matter error: {e}"))
        return issues

    meta = fm.meta
    body = fm.body
    full_text = read_text(path)

    # Required metadata keys
    missing = sorted(k for k in REQ_META_KEYS if k not in meta)
    if missing:
        issues.append(SkillValidationIssue(path, f"Missing metadata keys: {', '.join(missing)}"))

    # Types & simple constraints
    desc = str(meta.get("description", ""))
    if len(desc) == 0:
        issues.append(SkillValidationIssue(path, "description must be non-empty"))
    elif len(desc) > MAX_DESCRIPTION_LEN:
        issues.append(
            SkillValidationIssue(
                path,
                f"description too long ({len(desc)} > {MAX_DESCRIPTION_LEN})",
            )
        )

    if not isinstance(meta.get("keywords", []), list) or not meta.get("keywords"):
        issues.append(SkillValidationIssue(path, "keywords must be a non-empty list"))

    # Body sections present
    for sect in REQ_BODY_SECTIONS:
        if re.search(rf"^{re.escape(sect)}\s*$", body, flags=re.M) is None:
            issues.append(SkillValidationIssue(path, f"Missing required section heading: {sect}"))

    # Token budgets present
    if not has_token_budgets(body):
        issues.append(SkillValidationIssue(path, "Token budgets (T1/T2/T3) not found"))

    # Examples block sanity
    ex_len = first_examples_block_len(body)
    if ex_len is None:
        issues.append(SkillValidationIssue(path, "No code example found under '## Examples'"))
    else:
        if ex_len > MAX_EXAMPLE_LINES:
            issues.append(
                SkillValidationIssue(
                    path,
                    f"Example too long: {ex_len} lines (max {MAX_EXAMPLE_LINES})",
                )
            )

    # Oversized code blocks
    for start, end in find_code_blocks(body):
        n = max(0, end - start - 1)
        if n > MAX_CODEBLOCK_LINES:
            issues.append(
                SkillValidationIssue(
                    path,
                    f"Code block too long: {n} lines (max {MAX_CODEBLOCK_LINES})",
                )
            )

    # Secret scanning
    sec = scan_secrets(body)
    if sec:
        issues.append(SkillValidationIssue(path, sec))

    # Quality gates (optional, enabled via flags)

    # Check for TODO markers (strict mode)
    if check_todos:
        todos = check_todo_markers(full_text)
        if todos:
            for todo in todos:
                issues.append(
                    SkillValidationIssue(
                        path,
                        f"TODO marker found (not allowed in committed skills): {todo}",
                        severity="error",
                    )
                )

    # Validate URLs (strict mode)
    if check_links:
        urls = extract_urls(full_text)
        for url in urls:
            is_valid, msg = validate_url(url)
            if not is_valid:
                issues.append(
                    SkillValidationIssue(
                        path,
                        f"Link validation failed for {url}: {msg}",
                        severity="warning",  # Warning not error - links can be temporarily down
                    )
                )

    # Validate code syntax in examples (strict mode)
    if check_syntax:
        code_blocks = extract_code_blocks_with_lang(body)
        for lang, code in code_blocks:
            if lang:  # Only check blocks with language tags
                is_valid, msg = validate_code_syntax(lang, code)
                if not is_valid:
                    issues.append(
                        SkillValidationIssue(
                            path,
                            f"Code syntax validation failed: {msg}",
                            severity="error",
                        )
                    )

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Anthropic SKILL.md files")
    ap.add_argument(
        "--root",
        type=Path,
        default=Path(),
        help="Repo root (default: .)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict mode: check links, syntax, and fail on warnings",
    )
    ap.add_argument(
        "--check-links",
        action="store_true",
        help="Validate all HTTP/HTTPS URLs (implies warnings)",
    )
    ap.add_argument(
        "--check-syntax",
        action="store_true",
        help="Validate code syntax in examples",
    )
    ap.add_argument(
        "--check-todos",
        action="store_true",
        help="Fail on TODO markers in committed skills",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON for CI parsing",
    )
    args = ap.parse_args()

    # Strict mode enables all checks and fails on warnings
    check_links = args.strict or args.check_links
    check_syntax = args.strict or args.check_syntax
    check_todos = args.strict or args.check_todos
    fail_on_warnings = args.strict

    root: Path = args.root.resolve()
    skills_dir = root / "skills"
    if not skills_dir.exists():
        if not args.json:
            print(f"ERROR: skills dir not found: {skills_dir}", file=sys.stderr)
        return 2

    md_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not md_files:
        if args.json:
            print(json.dumps({"status": "success", "skills": 0, "issues": []}))
        else:
            print("No skills found.")
        return 0

    total_issues: list[SkillValidationIssue] = []
    results_by_file: dict[str, list[dict[str, str]]] = {}

    for p in md_files:
        issues = validate_skill_file(
            p,
            check_links=check_links,
            check_syntax=check_syntax,
            check_todos=check_todos,
        )
        if issues:
            results_by_file[str(p)] = [
                {"severity": isue.severity, "message": isue.message} for isue in issues
            ]
            if not args.json:
                for isue in issues:
                    severity_label = "WARN" if isue.severity == "warning" else "FAIL"
                    print(f"[{severity_label}] {isue.path}: {isue.message}")
            total_issues.extend(issues)
        else:
            if not args.json:
                print(f"[OK]   {p}")

    # Separate errors and warnings
    errors = [i for i in total_issues if i.severity == "error"]
    warnings = [i for i in total_issues if i.severity == "warning"]

    if args.json:
        output = {
            "status": "failed" if (errors or (fail_on_warnings and warnings)) else "success",
            "skills_checked": len(md_files),
            "errors": len(errors),
            "warnings": len(warnings),
            "files": results_by_file,
        }
        print(json.dumps(output, indent=2))
    else:
        if errors or warnings:
            print(
                f"\n{len(errors)} error(s), {len(warnings)} warning(s) found across {len(md_files)} file(s).",
                file=sys.stderr,
            )
        else:
            print(f"\nAll {len(md_files)} skill(s) passed validation.")

    # Exit codes: 0 = success, 1 = errors found, 2 = system error
    # In strict mode, warnings also cause failure
    if errors or (fail_on_warnings and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
