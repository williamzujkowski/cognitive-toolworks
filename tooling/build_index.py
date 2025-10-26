#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FRONT_MATTER_DELIM = re.compile(r"^---\s*$")

META_FIELDS = [
    "slug",
    "name",
    "description",
    "keywords",
    "owner",
    "version",
]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_front_matter(md_text: str) -> dict[str, Any]:
    lines = md_text.splitlines()
    if not lines or not FRONT_MATTER_DELIM.match(lines[0]):
        msg = "Missing starting '---' for front matter"
        raise ValueError(msg)
    end_idx = None
    for i in range(1, len(lines)):
        if FRONT_MATTER_DELIM.match(lines[i]):
            end_idx = i
            break
    if end_idx is None:
        msg = "Missing closing '---' for front matter"
        raise ValueError(msg)

    fm_text = "\n".join(lines[1:end_idx])
    if yaml is None:
        msg = "PyYAML not installed. Please add 'pyyaml'."
        raise RuntimeError(msg)
    meta = yaml.safe_load(fm_text) or {}
    if not isinstance(meta, dict):
        msg = "Front matter must be a YAML mapping"
        raise ValueError(msg)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="Build skills-index.json from SKILL.md files")
    ap.add_argument("--root", type=Path, default=Path("."), help="Repo root")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path (default: <root>/index/skills-index.json)",
    )
    ap.add_argument(
        "--with-embeddings",
        action="store_true",
        help="Also rebuild embeddings after building index",
    )
    args = ap.parse_args()

    root: Path = args.root.resolve()
    skills_dir = root / "skills"
    index_dir = root / "index"
    out = args.out or (index_dir / "skills-index.json")

    if not skills_dir.exists():
        print(f"ERROR: skills dir not found: {skills_dir}", file=sys.stderr)
        return 2
    index_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        meta = extract_front_matter(read_text(skill_md))
        missing = [k for k in META_FIELDS if k not in meta]
        if missing:
            print(f"WARN: {skill_md} missing fields: {', '.join(missing)}", file=sys.stderr)
        entry = {
            "slug": meta.get("slug"),
            "name": meta.get("name"),
            "summary": (meta.get("description") or "").strip()[:160],
            "keywords": meta.get("keywords", []),
            "owner": meta.get("owner"),
            "version": meta.get("version"),
            "entry": str(skill_md.as_posix()),
        }
        entries.append(entry)

    # Deterministic order
    entries = sorted(entries, key=lambda e: (e.get("slug") or ""))

    # Basic sanity
    slugs = [e.get("slug") for e in entries]
    if len(slugs) != len(set(slugs)):
        print("ERROR: duplicate slugs in skills", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} with {len(entries)} entr(y/ies)")

    # Optionally rebuild embeddings
    if args.with_embeddings:
        print("\nRebuilding embeddings...")
        embeddings_script = Path(__file__).parent / "build_embeddings.py"
        # S603: Subprocess call is safe - controlled script path and executable
        result = subprocess.run(  # noqa: S603
            [sys.executable, str(embeddings_script)], cwd=root, check=False
        )
        if result.returncode != 0:
            msg = "Failed to build embeddings"
            print(f"ERROR: {msg}", file=sys.stderr)
            return result.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
