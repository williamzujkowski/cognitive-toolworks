"""Unit tests for tooling/build_index.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from build_index import META_FIELDS, extract_front_matter, main, read_text


class TestReadText:
    """Test file reading utility."""

    def test_read_utf8_file(self, tmp_path: Path) -> None:
        """Read UTF-8 encoded file successfully."""
        test_file = tmp_path / "test.txt"
        content = "Hello, 世界! 🌍"
        test_file.write_text(content, encoding="utf-8")
        result = read_text(test_file)
        assert result == content


class TestFrontMatterExtraction:
    """Test YAML front matter extraction."""

    def test_valid_front_matter(self) -> None:
        """Extract valid front matter successfully."""
        md = dedent("""\
            ---
            name: Test Skill
            slug: test-skill
            version: 1.0.0
            keywords: [test, skill]
            ---
            # Body content
            """)
        meta = extract_front_matter(md)
        assert meta["name"] == "Test Skill"
        assert meta["slug"] == "test-skill"
        assert meta["version"] == "1.0.0"
        assert meta["keywords"] == ["test", "skill"]

    def test_missing_starting_delimiter(self) -> None:
        """Raise error when starting --- is missing."""
        md = "name: Test\n---\n# Content"
        with pytest.raises(ValueError, match="Missing starting '---'"):
            extract_front_matter(md)

    def test_missing_closing_delimiter(self) -> None:
        """Raise error when closing --- is missing."""
        md = "---\nname: Test\n# No closing delimiter"
        with pytest.raises(ValueError, match="Missing closing '---'"):
            extract_front_matter(md)

    def test_empty_front_matter(self) -> None:
        """Handle empty front matter (returns empty dict)."""
        md = "---\n---\n# Content"
        meta = extract_front_matter(md)
        assert meta == {}

    def test_non_dict_front_matter(self) -> None:
        """Raise error if front matter is not a mapping."""
        md = "---\n- item1\n- item2\n---\n# Content"
        with pytest.raises(ValueError, match="Front matter must be a YAML mapping"):
            extract_front_matter(md)

    def test_complex_metadata(self) -> None:
        """Extract complex nested metadata."""
        md = """---
name: Complex Skill
slug: complex-skill
description: A complex skill with nested data
keywords:
  - testing
  - validation
  - complex
capabilities:
  - feature1
  - feature2
inputs:
  param1: string
  param2: number
version: 2.0.0
---
# Content
"""
        meta = extract_front_matter(md)
        assert meta["name"] == "Complex Skill"
        assert len(meta["keywords"]) == 3
        assert "feature1" in meta["capabilities"]
        assert isinstance(meta["inputs"], dict)


class TestIndexBuilding:
    """Test index building functionality."""

    def create_skill_file(self, path: Path, slug: str, **kwargs: Any) -> Path:
        """Helper to create a SKILL.md file."""
        name = kwargs.get("name", f"{slug.title()} Skill")
        description = kwargs.get("description", f"Description for {slug}")
        keywords = kwargs.get("keywords", ["test"])
        owner = kwargs.get("owner", "test-owner")
        version = kwargs.get("version", "1.0.0")

        content = f"""---
name: {name}
slug: {slug}
description: {description}
keywords: {json.dumps(keywords)}
owner: {owner}
version: {version}
capabilities: [test]
inputs: {{}}
outputs: {{}}
license: Apache-2.0
security: standard
links: []
---

## Purpose & When-To-Use
Test purpose

## Pre-Checks
Test checks

## Procedure
Test procedure

## Decision Rules
Test rules

## Output Contract
Test output

## Quality Gates
Test gates

## Resources
Test resources

## Examples
```
example
```
"""
        skill_dir = path / slug
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(content, encoding="utf-8")
        return skill_file

    def test_build_index_single_skill(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Build index with single skill."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        index_dir = tmp_path / "index"

        self.create_skill_file(skills_dir, "test-skill")

        # Mock sys.argv for argparse
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "build_index.py",
                "--root",
                str(tmp_path),
                "--out",
                str(index_dir / "skills-index.json"),
            ],
        )

        result = main()
        assert result == 0

        index_file = index_dir / "skills-index.json"
        assert index_file.exists()

        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index) == 1
        assert index[0]["slug"] == "test-skill"
        assert index[0]["name"] == "Test-Skill Skill"
        assert "Test purpose" not in index[0]["summary"]  # Summary is description, not body

    def test_build_index_multiple_skills(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Build index with multiple skills in deterministic order."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        index_dir = tmp_path / "index"

        # Create skills in non-alphabetical order
        self.create_skill_file(skills_dir, "zebra-skill", name="Zebra")
        self.create_skill_file(skills_dir, "alpha-skill", name="Alpha")
        self.create_skill_file(skills_dir, "beta-skill", name="Beta")

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = index_dir / "skills-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index) == 3
        # Should be sorted alphabetically by slug
        assert index[0]["slug"] == "alpha-skill"
        assert index[1]["slug"] == "beta-skill"
        assert index[2]["slug"] == "zebra-skill"

    def test_truncate_long_description(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Truncate description to 160 characters."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        long_desc = "x" * 200
        self.create_skill_file(skills_dir, "long-desc", description=long_desc)

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "skills-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index[0]["summary"]) == 160

    def test_preserve_all_metadata_fields(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Include all required metadata fields in index entry."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        self.create_skill_file(
            skills_dir,
            "full-metadata",
            name="Full Metadata Skill",
            description="Complete metadata test",
            keywords=["keyword1", "keyword2", "keyword3"],
            owner="test-owner",
            version="2.1.0",
        )

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "skills-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        entry = index[0]
        # Verify all required fields are present (note: description becomes summary in index)
        assert "slug" in entry
        assert "name" in entry
        assert "summary" in entry  # description is renamed to summary
        assert "keywords" in entry
        assert "owner" in entry
        assert "version" in entry
        assert "entry" in entry

        assert entry["slug"] == "full-metadata"
        assert entry["name"] == "Full Metadata Skill"
        assert entry["summary"] == "Complete metadata test"
        assert entry["keywords"] == ["keyword1", "keyword2", "keyword3"]
        assert entry["owner"] == "test-owner"
        assert entry["version"] == "2.1.0"
        assert "entry" in entry
        assert entry["entry"].endswith("SKILL.md")

    def test_missing_metadata_fields_warning(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Warn when required metadata fields are missing."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        skill_dir = skills_dir / "incomplete"
        skill_dir.mkdir()

        # Create skill missing some metadata
        (skill_dir / "SKILL.md").write_text(
            """---
slug: incomplete
name: Incomplete Skill
---
# Content
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0  # Still succeeds but warns

        captured = capsys.readouterr()
        assert "WARN" in captured.err
        assert "missing fields" in captured.err

    def test_duplicate_slug_detection(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Detect and reject duplicate slugs."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        # Create two skills with same slug (different dirs)
        (skills_dir / "skill1").mkdir()
        (skills_dir / "skill1" / "SKILL.md").write_text(
            """---
slug: duplicate
name: Skill One
description: First skill
keywords: [test]
owner: test
version: 1.0.0
---
# Content
""",
            encoding="utf-8",
        )

        (skills_dir / "skill2").mkdir()
        (skills_dir / "skill2" / "SKILL.md").write_text(
            """---
slug: duplicate
name: Skill Two
description: Second skill
keywords: [test]
owner: test
version: 1.0.0
---
# Content
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 1  # Should fail

    def test_no_skills_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle case where no skills exist."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()  # Empty directory

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "skills-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert index == []

    def test_skills_dir_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return error when skills directory doesn't exist."""
        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 2  # Error code for missing skills dir

    def test_custom_output_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Write to custom output path when specified."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        custom_out = tmp_path / "custom" / "output.json"

        self.create_skill_file(skills_dir, "test-skill")

        monkeypatch.setattr(
            sys, "argv", ["build_index.py", "--root", str(tmp_path), "--out", str(custom_out)]
        )

        result = main()
        assert result == 0
        assert custom_out.exists()

        with custom_out.open(encoding="utf-8") as f:
            index = json.load(f)
        assert len(index) == 1

    def test_index_creates_parent_directories(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Create parent directories for output if they don't exist."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        nested_out = tmp_path / "a" / "b" / "c" / "index.json"

        self.create_skill_file(skills_dir, "test-skill")

        monkeypatch.setattr(
            sys, "argv", ["build_index.py", "--root", str(tmp_path), "--out", str(nested_out)]
        )

        result = main()
        assert result == 0
        assert nested_out.exists()
        assert nested_out.parent.exists()

    def test_json_format_with_newline(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Output JSON with proper indentation and trailing newline."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        self.create_skill_file(skills_dir, "test-skill")

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "skills-index.json"
        content = index_file.read_text(encoding="utf-8")

        # Check trailing newline
        assert content.endswith("\n")

        # Check indentation (2 spaces)
        assert "  " in content

        # Verify valid JSON
        json.loads(content)

    def test_malformed_skill_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle malformed SKILL.md file gracefully."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        bad_skill = skills_dir / "bad-skill"
        bad_skill.mkdir()

        # Missing closing ---
        (bad_skill / "SKILL.md").write_text(
            """---
slug: bad
name: Bad Skill
# Missing closing delimiter
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        # Should raise an error during extraction
        with pytest.raises(ValueError):
            main()

    def test_entry_path_format(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Entry path uses POSIX format (forward slashes)."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        self.create_skill_file(skills_dir, "path-test")

        monkeypatch.setattr(sys, "argv", ["build_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "skills-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        entry_path = index[0]["entry"]
        # POSIX format uses forward slashes
        assert "/" in entry_path
        assert "\\" not in entry_path
        assert entry_path.endswith("/SKILL.md")


class TestMetaFieldsConstant:
    """Test META_FIELDS constant."""

    def test_meta_fields_complete(self) -> None:
        """META_FIELDS includes all required fields."""
        expected = ["slug", "name", "description", "keywords", "owner", "version"]
        assert expected == META_FIELDS

    def test_meta_fields_order(self) -> None:
        """META_FIELDS in expected order."""
        assert META_FIELDS[0] == "slug"
        assert META_FIELDS[1] == "name"
