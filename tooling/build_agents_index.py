#!/usr/bin/env python3
"""Build agents-index.json from AGENT.md files"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped,unused-ignore]
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FRONT_MATTER_DELIM = re.compile(r"^---\s*$")

# Required metadata fields for agents
META_FIELDS = [
    "slug",
    "name",
    "description",
    "model",
    "tools",
    "keywords",
    "version",
    "owner",
]


def read_text(p: Path) -> str:
    """Read file as UTF-8 text"""
    return p.read_text(encoding="utf-8")


def extract_front_matter(md_text: str) -> dict[str, Any]:
    """Extract YAML front matter from markdown"""
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
    """Build agents-index.json from all AGENT.md files"""
    ap = argparse.ArgumentParser(description="Build agents-index.json from AGENT.md files")
    ap.add_argument("--root", type=Path, default=Path("."), help="Repo root")
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path (default: <root>/index/agents-index.json)",
    )
    args = ap.parse_args()

    root: Path = args.root.resolve()
    agents_dir = root / "agents"
    index_dir = root / "index"
    out = args.out or (index_dir / "agents-index.json")

    if not agents_dir.exists():
        print(f"ERROR: agents dir not found: {agents_dir}", file=sys.stderr)
        return 2
    index_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    for agent_md in sorted(agents_dir.glob("*/AGENT.md")):
        meta = extract_front_matter(read_text(agent_md))
        missing = [k for k in META_FIELDS if k not in meta]
        if missing:
            print(f"WARN: {agent_md} missing fields: {', '.join(missing)}", file=sys.stderr)

        entry = {
            "slug": meta.get("slug"),
            "name": meta.get("name"),
            "description": (meta.get("description") or "").strip()[:160],
            "keywords": meta.get("keywords", []),
            "model": meta.get("model"),
            "tools": meta.get("tools", []),
            "version": meta.get("version"),
            "owner": meta.get("owner"),
            "entry": str(agent_md.as_posix()),
        }
        entries.append(entry)

    # Deterministic alphabetical order by slug
    entries = sorted(entries, key=lambda e: (e.get("slug") or ""))

    # Sanity check: no duplicate slugs
    slugs = [e.get("slug") for e in entries]
    if len(slugs) != len(set(slugs)):
        print("ERROR: duplicate slugs in agents", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} with {len(entries)} entr(y/ies)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
