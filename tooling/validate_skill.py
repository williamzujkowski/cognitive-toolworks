#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

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


@dataclass
class FrontMatter:
    meta: dict
    body: str


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_front_matter(md_text: str) -> FrontMatter:
    """Extract YAML front matter delimited by '---' at the top of the file."""
    lines = md_text.splitlines()
    if not lines or not FRONT_MATTER_DELIM.match(lines[0]):
        raise ValueError("Missing starting '---' for front matter")
    # find closing '---'
    end_idx = None
    for i in range(1, len(lines)):
        if FRONT_MATTER_DELIM.match(lines[i]):
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("Missing closing '---' for front matter")

    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])

    if yaml is None:
        raise RuntimeError("PyYAML not installed. Please add 'pyyaml' and re-run validator.")
    try:
        meta = yaml.safe_load(fm_text) or {}
    except Exception as e:  # pragma: no cover
        raise ValueError(f"Failed to parse front matter YAML: {e}")

    if not isinstance(meta, dict):
        raise ValueError("Front matter must be a YAML mapping (object)")

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


def validate_skill_file(path: Path) -> list[SkillValidationIssue]:
    issues: list[SkillValidationIssue] = []
    try:
        fm = extract_front_matter(read_text(path))
    except Exception as e:
        issues.append(SkillValidationIssue(path, f"Front matter error: {e}"))
        return issues

    meta = fm.meta
    body = fm.body

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

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Anthropic SKILL.md files")
    ap.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repo root (default: .)",
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

    total_issues: list[SkillValidationIssue] = []
    for p in md_files:
        issues = validate_skill_file(p)
        if issues:
            for isue in issues:
                print(f"[FAIL] {isue.path}: {isue.message}")
            total_issues.extend(issues)
        else:
            print(f"[OK]   {p}")

    if total_issues:
        print(
            f"\n{len(total_issues)} issue(s) found across {len(md_files)} file(s).", file=sys.stderr
        )
        return 1
    print(f"\nAll {len(md_files)} skill(s) passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
