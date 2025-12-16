"""Tests for skill discovery module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cognitive_toolworks.discovery import SkillIndex, SkillIndexEntry


@pytest.fixture
def sample_index_data() -> list[dict]:
    """Sample skills index data for testing."""
    return [
        {
            "slug": "security-appsec-validator",
            "name": "Application Security Validator",
            "summary": "Validate application security with OWASP checks",
            "keywords": ["security", "owasp", "validation", "appsec"],
            "owner": "cognitive-toolworks",
            "version": "1.0.0",
            "entry": "/path/to/skill.md",
        },
        {
            "slug": "cloud-aws-architect",
            "name": "AWS Cloud Architect",
            "summary": "Design AWS cloud architectures",
            "keywords": ["cloud", "aws", "architecture", "design"],
            "owner": "cognitive-toolworks",
            "version": "1.1.0",
            "entry": "/path/to/skill2.md",
        },
        {
            "slug": "testing-unit-generator",
            "name": "Unit Test Generator",
            "summary": "Generate unit tests for various frameworks",
            "keywords": ["testing", "unit-tests", "generator"],
            "owner": "cognitive-toolworks",
            "version": "1.0.0",
            "entry": "/path/to/skill3.md",
        },
        {
            "slug": "api-graphql-designer",
            "name": "GraphQL API Designer",
            "summary": "Design GraphQL schemas and APIs",
            "keywords": ["api", "graphql", "schema", "design"],
            "owner": "cognitive-toolworks",
            "version": "1.2.0",
            "entry": "/path/to/skill4.md",
        },
    ]


@pytest.fixture
def temp_index(tmp_path: Path, sample_index_data: list[dict]) -> Path:
    """Create temporary skills index file."""
    index_path = tmp_path / "skills-index.json"
    with index_path.open("w") as f:
        json.dump(sample_index_data, f, indent=2)
    return index_path


class TestSkillIndexEntry:
    """Test SkillIndexEntry dataclass."""

    def test_from_dict(self, sample_index_data: list[dict]):
        """Test creating entry from dict."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.slug == "security-appsec-validator"
        assert entry.name == "Application Security Validator"
        assert entry.summary == "Validate application security with OWASP checks"
        assert "security" in entry.keywords
        assert entry.version == "1.0.0"

    def test_matches_query_name(self, sample_index_data: list[dict]):
        """Test query matching in name."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.matches_query("security")
        assert entry.matches_query("SECURITY")  # Case insensitive
        assert entry.matches_query("validator")
        assert not entry.matches_query("kubernetes")

    def test_matches_query_summary(self, sample_index_data: list[dict]):
        """Test query matching in summary."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.matches_query("owasp")
        assert entry.matches_query("OWASP")
        assert entry.matches_query("validate")

    def test_matches_query_keywords(self, sample_index_data: list[dict]):
        """Test query matching in keywords."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.matches_query("appsec")
        assert entry.matches_query("validation")

    def test_matches_query_slug(self, sample_index_data: list[dict]):
        """Test query matching in slug."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.matches_query("security-appsec")
        assert entry.matches_query("appsec-validator")

    def test_matches_domain(self, sample_index_data: list[dict]):
        """Test domain matching."""
        entry = SkillIndexEntry.from_dict(sample_index_data[0])
        assert entry.matches_domain("security")
        assert entry.matches_domain("SECURITY")  # Case insensitive
        assert not entry.matches_domain("cloud")
        assert not entry.matches_domain("testing")


class TestSkillIndex:
    """Test SkillIndex class."""

    def test_init_with_path(self, temp_index: Path):
        """Test initialization with explicit path."""
        index = SkillIndex(index_path=temp_index)
        assert index.index_path == temp_index
        assert index._entries is None  # Not loaded yet

    def test_init_with_nonexistent_path(self):
        """Test initialization with non-existent path."""
        # Creating index with non-existent path doesn't fail until loading
        index = SkillIndex(index_path=Path("/nonexistent/skills-index.json"))
        # Should fail when trying to load
        with pytest.raises(FileNotFoundError):
            index.list_skills()

    def test_list_skills_all(self, temp_index: Path):
        """Test listing all skills."""
        index = SkillIndex(index_path=temp_index)
        skills = index.list_skills()

        assert len(skills) == 4
        # Should be sorted by slug
        assert skills[0].slug == "api-graphql-designer"
        assert skills[1].slug == "cloud-aws-architect"
        assert skills[2].slug == "security-appsec-validator"
        assert skills[3].slug == "testing-unit-generator"

    def test_list_skills_by_domain(self, temp_index: Path):
        """Test filtering skills by domain."""
        index = SkillIndex(index_path=temp_index)

        # Filter by security
        security_skills = index.list_skills(domain="security")
        assert len(security_skills) == 1
        assert security_skills[0].slug == "security-appsec-validator"

        # Filter by cloud
        cloud_skills = index.list_skills(domain="cloud")
        assert len(cloud_skills) == 1
        assert cloud_skills[0].slug == "cloud-aws-architect"

        # Filter by non-existent domain
        none_skills = index.list_skills(domain="nonexistent")
        assert len(none_skills) == 0

    def test_search_skills(self, temp_index: Path):
        """Test searching skills."""
        index = SkillIndex(index_path=temp_index)

        # Search by keyword
        results = index.search_skills("graphql")
        assert len(results) == 1
        assert results[0].slug == "api-graphql-designer"

        # Search by partial name
        results = index.search_skills("test")
        assert len(results) == 1
        assert results[0].slug == "testing-unit-generator"

        # Search by common keyword
        results = index.search_skills("design")
        assert len(results) == 2
        # Exact slug match or name match should come first
        slugs = [r.slug for r in results]
        assert "cloud-aws-architect" in slugs
        assert "api-graphql-designer" in slugs

    def test_search_skills_case_insensitive(self, temp_index: Path):
        """Test case-insensitive search."""
        index = SkillIndex(index_path=temp_index)

        results = index.search_skills("AWS")
        assert len(results) == 1
        assert results[0].slug == "cloud-aws-architect"

        results = index.search_skills("GraphQL")
        assert len(results) == 1
        assert results[0].slug == "api-graphql-designer"

    def test_search_skills_relevance_sorting(self, temp_index: Path):
        """Test search results are sorted by relevance."""
        index = SkillIndex(index_path=temp_index)

        # Search for "security" - should prioritize exact slug match
        results = index.search_skills("security")
        # security-appsec-validator should come first (slug match)
        assert results[0].slug == "security-appsec-validator"

    def test_get_skill_by_slug(self, temp_index: Path):
        """Test getting skill by exact slug."""
        index = SkillIndex(index_path=temp_index)

        skill = index.get_skill("cloud-aws-architect")
        assert skill is not None
        assert skill.slug == "cloud-aws-architect"
        assert skill.name == "AWS Cloud Architect"

        # Non-existent slug
        skill = index.get_skill("nonexistent-skill")
        assert skill is None

    def test_get_domains(self, temp_index: Path):
        """Test extracting unique domains."""
        index = SkillIndex(index_path=temp_index)

        domains = index.get_domains()
        assert len(domains) == 4
        assert "api" in domains
        assert "cloud" in domains
        assert "security" in domains
        assert "testing" in domains
        # Should be sorted
        assert domains == ["api", "cloud", "security", "testing"]

    def test_count(self, temp_index: Path):
        """Test counting total skills."""
        index = SkillIndex(index_path=temp_index)
        assert index.count() == 4

    def test_caching(self, temp_index: Path):
        """Test that index is cached after first load."""
        index = SkillIndex(index_path=temp_index)

        # First call loads
        _ = index.list_skills()
        assert index._entries is not None

        # Second call uses cache (check internal cache, not return value)
        entries1 = index._entries
        _ = index.list_skills()
        entries2 = index._entries
        assert entries1 is entries2  # Same cached object


class TestIntegration:
    """Integration tests with real index if available."""

    def test_real_index_if_exists(self):
        """Test with real skills-index.json if it exists."""
        try:
            # Try to auto-detect real index
            index = SkillIndex()
            skills = index.list_skills()
            assert len(skills) > 0
            assert all(isinstance(s, SkillIndexEntry) for s in skills)

            # Test search works
            results = index.search_skills("test")
            assert all(isinstance(r, SkillIndexEntry) for r in results)

            # Test domains work
            domains = index.get_domains()
            assert len(domains) > 0
            assert all(isinstance(d, str) for d in domains)

        except FileNotFoundError:
            # Real index not available, skip
            pytest.skip("Real skills-index.json not available")
