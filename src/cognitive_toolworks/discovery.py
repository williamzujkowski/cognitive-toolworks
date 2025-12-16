"""
Discovery module for browsing and searching skills.

Provides fast, local-only discovery of skills from the skills index.
No LLM calls - just text search and filtering.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SkillIndexEntry:
    """Single entry from skills-index.json."""

    slug: str
    name: str
    summary: str
    keywords: list[str]
    owner: str
    version: str
    entry: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SkillIndexEntry:
        """Create from index JSON entry."""
        return cls(
            slug=data["slug"],
            name=data["name"],
            summary=data["summary"],
            keywords=data.get("keywords", []),
            owner=data.get("owner", "unknown"),
            version=data.get("version", "1.0.0"),
            entry=data["entry"],
        )

    def matches_query(self, query: str) -> bool:
        """Check if entry matches search query (case-insensitive)."""
        query_lower = query.lower()
        return (
            query_lower in self.name.lower()
            or query_lower in self.summary.lower()
            or any(query_lower in kw.lower() for kw in self.keywords)
            or query_lower in self.slug.lower()
        )

    def matches_domain(self, domain: str) -> bool:
        """Check if slug matches domain prefix."""
        return self.slug.startswith(domain.lower())


class SkillIndex:
    """
    Cached loader for skills-index.json.

    Provides fast filtering and searching without loading full SKILL.md files.
    """

    def __init__(self, index_path: Path | None = None):
        """
        Initialize skill index.

        Args:
            index_path: Path to skills-index.json. If None, auto-detects from repo root.
        """
        if index_path is None:
            # Auto-detect from repo root
            # Try common locations
            candidates = [
                Path.cwd() / "index" / "skills-index.json",
                Path.cwd() / "skills-index.json",
                Path(__file__).parent.parent.parent / "index" / "skills-index.json",
            ]
            for candidate in candidates:
                if candidate.exists():
                    index_path = candidate
                    break
            else:
                msg = f"Could not find skills-index.json. Tried: {[str(p) for p in candidates]}"
                raise FileNotFoundError(msg)

        self.index_path = index_path
        self._entries: list[SkillIndexEntry] | None = None

    def _load(self) -> list[SkillIndexEntry]:
        """Load and cache index entries."""
        if self._entries is None:
            with self.index_path.open() as f:
                data = json.load(f)
            self._entries = [SkillIndexEntry.from_dict(entry) for entry in data]
        return self._entries

    def list_skills(self, domain: str | None = None) -> list[SkillIndexEntry]:
        """
        List all skills, optionally filtered by domain.

        Args:
            domain: Domain prefix to filter by (e.g., "security", "cloud", "testing")

        Returns:
            List of matching skill entries, sorted by slug
        """
        entries = self._load()

        if domain:
            entries = [e for e in entries if e.matches_domain(domain)]

        return sorted(entries, key=lambda e: e.slug)

    def search_skills(self, query: str) -> list[SkillIndexEntry]:
        """
        Search skills by keyword in name, summary, keywords, or slug.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching skills, sorted by relevance (exact slug match first)
        """
        entries = self._load()
        matches = [e for e in entries if e.matches_query(query)]

        # Sort by relevance: exact slug match > name match > summary match > keyword match
        def relevance_key(entry: SkillIndexEntry) -> tuple[int, str]:
            query_lower = query.lower()
            if entry.slug.lower() == query_lower:
                return (0, entry.slug)
            if query_lower in entry.name.lower():
                return (1, entry.slug)
            if query_lower in entry.summary.lower():
                return (2, entry.slug)
            return (3, entry.slug)

        return sorted(matches, key=relevance_key)

    def get_skill(self, slug: str) -> SkillIndexEntry | None:
        """
        Get skill by exact slug.

        Args:
            slug: Skill slug

        Returns:
            Skill entry if found, None otherwise
        """
        entries = self._load()
        for entry in entries:
            if entry.slug == slug:
                return entry
        return None

    def get_domains(self) -> list[str]:
        """
        Get list of unique domain prefixes from all skills.

        Returns:
            Sorted list of domain prefixes (part before first hyphen)
        """
        entries = self._load()
        domains = set()
        for entry in entries:
            # Extract domain from slug (part before first hyphen)
            parts = entry.slug.split("-")
            if parts:
                domains.add(parts[0])
        return sorted(domains)

    def count(self) -> int:
        """Get total number of skills in index."""
        return len(self._load())
