#!/usr/bin/env python3
"""
Initialize Anthropic Skills repo structure with .gitkeep files.

- Creates the standard directories for a skills repository
  (index/, skills/, tests/, tooling/, .github/workflows/).
- Adds .gitkeep in every created directory (idempotent).
- Optionally pre-creates skill skeleton folders under skills/<slug> with
  examples/, resources/, scripts/ and .gitkeep files.
- Optionally adds arbitrary extra directories (relative, safe-checked).
- Supports dry-run mode.

Designed to pass common linting and security scans:
- Standard library only (no subprocess or eval).
- Type hints; deterministic behavior; no network calls.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List


DEFAULT_DIRS: List[str] = [
    "index",
    "index/embeddings",
    "skills",
    "tests",
    "tooling",
    ".github",
    ".github/workflows",
]

SKILL_SUBDIRS: List[str] = [
    "examples",
    "resources",
    "scripts",
]


def _safe_join(root: Path, rel: str) -> Path:
    """
    Join a relative path safely under root, preventing escape via '..' or absolute paths.
    """
    if rel.strip() == "":
        raise ValueError("Empty relative path is not allowed.")
    p = Path(rel)
    if p.is_absolute():
        raise ValueError(f"Absolute paths are not allowed: {rel}")
    # Normalize and ensure it's within root
    target = (root / p).resolve()
    root_resolved = root.resolve()
    if root_resolved not in target.parents and target != root_resolved:
        # If target isn't the root or inside it, reject.
        raise ValueError(f"Unsafe path outside repo root: {rel}")
    return target


def _ensure_dir(path: Path, dry_run: bool) -> None:
    """
    Create a directory (parents=True) and place a .gitkeep inside.
    """
    if dry_run:
        print(f"[DRY] mkdir -p {path}")
        print(f"[DRY] touch {path/'.gitkeep'}")
        return
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    # Always create/touch to ensure presence (idempotent).
    gitkeep.touch(exist_ok=True)


def _create_skill_skeleton(root: Path, slug: str, dry_run: bool) -> None:
    """
    Create skills/<slug>/ with subfolders and .gitkeep files.
    Only structure; does not create SKILL.md (separate generator handles that).
    """
    if not slug or slug.strip() == "":
        raise ValueError("Skill slug cannot be empty.")
    if any(c in slug for c in r"\/:<>|*?\""):
        raise ValueError(f"Skill slug contains invalid characters: {slug}")

    base = _safe_join(root, f"skills/{slug}")
    _ensure_dir(base, dry_run)
    for sub in SKILL_SUBDIRS:
        _ensure_dir(base / sub, dry_run)


def _create_structure(root: Path, dirs: Iterable[str], skills: Iterable[str], dry_run: bool) -> None:
    for d in dirs:
        target = _safe_join(root, d)
        _ensure_dir(target, dry_run)

    for slug in skills:
        normalized = slug.strip()
        if normalized:
            _create_skill_skeleton(root, normalized, dry_run)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize Skills repository folder structure with .gitkeep files."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Root of the repository (default: current directory).",
    )
    parser.add_argument(
        "--extra-dir",
        action="append",
        default=[],
        help="Additional relative directories to create (can be passed multiple times).",
    )
    parser.add_argument(
        "--skills",
        default="",
        help="Comma-separated list of skill slugs to precreate under skills/<slug>/.",
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="If set, do not create the default directory set; use only --extra-dir and --skills.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing to disk.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    try:
        root = args.repo_root.resolve()
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: Could not resolve repo root: {exc}", file=sys.stderr)
        return 2

    if not root.exists():
        if args.dry_run:
            print(f"[DRY] mkdir -p {root}")
        else:
            try:
                root.mkdir(parents=True, exist_ok=True)
            except Exception as exc:  # pragma: no cover
                print(f"ERROR: Could not create repo root: {exc}", file=sys.stderr)
                return 2

    dirs: List[str] = []
    if not args.no_defaults:
        dirs.extend(DEFAULT_DIRS)

    # Deduplicate while preserving order
    for ed in args.extra_dir:
        if ed not in dirs:
            dirs.append(ed)

    skills_list: List[str] = [s.strip() for s in args.skills.split(",") if s.strip()]

    # Always ensure top-level root gets a .gitkeep if requested structure is empty
    # (We won’t create .gitkeep directly under root to avoid clutter; only inside directories.)

    try:
        _create_structure(root, dirs, skills_list, args.dry_run)
    except ValueError as ve:
        print(f"ERROR: {ve}", file=sys.stderr)
        return 1
    except OSError as oe:  # pragma: no cover
        print(f"ERROR: OS error while creating structure: {oe}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("\n[DRY] Completed dry run. No files were written.")
    else:
        print("Repository structure initialized successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
