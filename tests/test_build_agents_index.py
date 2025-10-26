"""Unit tests for tooling/build_agents_index.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from textwrap import dedent
from typing import Any

import pytest

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from build_agents_index import META_FIELDS, extract_front_matter, main, read_text


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
        md = dedent(
            """\
            ---
            name: Test Agent
            slug: test-agent
            version: 1.0.0
            keywords: [test, agent]
            model: inherit
            tools: [Read, Write, Bash]
            ---
            # Body content
            """
        )
        meta = extract_front_matter(md)
        assert meta["name"] == "Test Agent"
        assert meta["slug"] == "test-agent"
        assert meta["version"] == "1.0.0"
        assert meta["keywords"] == ["test", "agent"]
        assert meta["model"] == "inherit"
        assert meta["tools"] == ["Read", "Write", "Bash"]

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
name: Complex Agent
slug: complex-agent
description: A complex agent with nested data
keywords:
  - orchestration
  - validation
  - complex
model: inherit
tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
persona: Expert orchestrator
version: 2.0.0
owner: cognitive-toolworks
---
# Content
"""
        meta = extract_front_matter(md)
        assert meta["name"] == "Complex Agent"
        assert len(meta["keywords"]) == 3
        assert "Read" in meta["tools"]
        assert meta["model"] == "inherit"
        assert meta["persona"] == "Expert orchestrator"


class TestIndexBuilding:
    """Test index building functionality."""

    def create_agent_file(self, path: Path, slug: str, **kwargs: Any) -> Path:
        """Helper to create an AGENT.md file."""
        name = kwargs.get("name", f"{slug.title()} Agent")
        description = kwargs.get("description", f"Description for {slug}")
        keywords = kwargs.get("keywords", ["test"])
        owner = kwargs.get("owner", "test-owner")
        version = kwargs.get("version", "1.0.0")
        model = kwargs.get("model", "inherit")
        tools = kwargs.get("tools", ["Read", "Write", "Bash"])

        content = f"""---
name: {name}
slug: {slug}
description: {description}
keywords: {json.dumps(keywords)}
owner: {owner}
version: {version}
model: {model}
tools: {json.dumps(tools)}
persona: Test persona
license: Apache-2.0
security:
  pii: none
  secrets: never
links:
  docs: []
---

## Purpose & Scope

Test purpose

## Orchestration Workflow

Test workflow

## Coordination Strategy

Test strategy

## Error Handling

Test error handling

## Quality Assurance

Test QA

## Usage

Test usage
"""
        agent_dir = path / slug
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_file = agent_dir / "AGENT.md"
        agent_file.write_text(content, encoding="utf-8")
        return agent_file

    def test_build_index_single_agent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Build index with single agent."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        index_dir = tmp_path / "index"

        self.create_agent_file(agents_dir, "test-agent")

        # Mock sys.argv for argparse
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "build_agents_index.py",
                "--root",
                str(tmp_path),
                "--out",
                str(index_dir / "agents-index.json"),
            ],
        )

        result = main()
        assert result == 0

        index_file = index_dir / "agents-index.json"
        assert index_file.exists()

        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index) == 1
        assert index[0]["slug"] == "test-agent"
        assert index[0]["name"] == "Test-Agent Agent"
        assert "Test purpose" not in index[0]["description"]  # Description is from frontmatter

    def test_build_index_multiple_agents(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Build index with multiple agents in deterministic order."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        index_dir = tmp_path / "index"

        # Create agents in non-alphabetical order
        self.create_agent_file(agents_dir, "zebra-agent", name="Zebra")
        self.create_agent_file(agents_dir, "alpha-agent", name="Alpha")
        self.create_agent_file(agents_dir, "beta-agent", name="Beta")

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = index_dir / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index) == 3
        # Should be sorted alphabetically by slug
        assert index[0]["slug"] == "alpha-agent"
        assert index[1]["slug"] == "beta-agent"
        assert index[2]["slug"] == "zebra-agent"

    def test_truncate_long_description(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Truncate description to 160 characters."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        long_desc = "x" * 200
        self.create_agent_file(agents_dir, "long-desc", description=long_desc)

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert len(index[0]["description"]) == 160

    def test_preserve_all_metadata_fields(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Include all required metadata fields in index entry."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        self.create_agent_file(
            agents_dir,
            "full-metadata",
            name="Full Metadata Agent",
            description="Complete metadata test",
            keywords=["keyword1", "keyword2", "keyword3"],
            owner="test-owner",
            version="2.1.0",
            model="claude-3-5-sonnet-20241022",
            tools=["Read", "Write", "Bash", "Grep", "Glob", "Task"],
        )

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        entry = index[0]
        # Verify all required fields are present
        assert "slug" in entry
        assert "name" in entry
        assert "description" in entry
        assert "keywords" in entry
        assert "owner" in entry
        assert "version" in entry
        assert "model" in entry
        assert "tools" in entry
        assert "entry" in entry

        assert entry["slug"] == "full-metadata"
        assert entry["name"] == "Full Metadata Agent"
        assert entry["description"] == "Complete metadata test"
        assert entry["keywords"] == ["keyword1", "keyword2", "keyword3"]
        assert entry["owner"] == "test-owner"
        assert entry["version"] == "2.1.0"
        assert entry["model"] == "claude-3-5-sonnet-20241022"
        assert len(entry["tools"]) == 6
        assert "entry" in entry
        assert entry["entry"].endswith("AGENT.md")

    def test_missing_metadata_fields_warning(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Warn when required metadata fields are missing."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        agent_dir = agents_dir / "incomplete"
        agent_dir.mkdir()

        # Create agent missing some metadata
        (agent_dir / "AGENT.md").write_text(
            """---
slug: incomplete
name: Incomplete Agent
---
# Content
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0  # Still succeeds but warns

        captured = capsys.readouterr()
        assert "WARN" in captured.err
        assert "missing fields" in captured.err

    def test_duplicate_slug_detection(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Detect and reject duplicate slugs."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        # Create two agents with same slug (different dirs)
        (agents_dir / "agent1").mkdir()
        (agents_dir / "agent1" / "AGENT.md").write_text(
            """---
slug: duplicate
name: Agent One
description: First agent
keywords: [test]
owner: test
version: 1.0.0
model: inherit
tools: [Read, Write]
---
# Content
""",
            encoding="utf-8",
        )

        (agents_dir / "agent2").mkdir()
        (agents_dir / "agent2" / "AGENT.md").write_text(
            """---
slug: duplicate
name: Agent Two
description: Second agent
keywords: [test]
owner: test
version: 1.0.0
model: inherit
tools: [Read, Write]
---
# Content
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 1  # Should fail

    def test_no_agents_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle case where no agents exist."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()  # Empty directory

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert index == []

    def test_agents_dir_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return error when agents directory doesn't exist."""
        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 2  # Error code for missing agents dir

    def test_custom_output_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Write to custom output path when specified."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        custom_out = tmp_path / "custom" / "output.json"

        self.create_agent_file(agents_dir, "test-agent")

        monkeypatch.setattr(
            sys,
            "argv",
            ["build_agents_index.py", "--root", str(tmp_path), "--out", str(custom_out)],
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
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        nested_out = tmp_path / "a" / "b" / "c" / "index.json"

        self.create_agent_file(agents_dir, "test-agent")

        monkeypatch.setattr(
            sys,
            "argv",
            ["build_agents_index.py", "--root", str(tmp_path), "--out", str(nested_out)],
        )

        result = main()
        assert result == 0
        assert nested_out.exists()
        assert nested_out.parent.exists()

    def test_json_format_with_newline(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Output JSON with proper indentation and trailing newline."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        self.create_agent_file(agents_dir, "test-agent")

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        content = index_file.read_text(encoding="utf-8")

        # Check trailing newline
        assert content.endswith("\n")

        # Check indentation (2 spaces)
        assert "  " in content

        # Verify valid JSON
        json.loads(content)

    def test_malformed_agent_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle malformed AGENT.md file gracefully."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        bad_agent = agents_dir / "bad-agent"
        bad_agent.mkdir()

        # Missing closing ---
        (bad_agent / "AGENT.md").write_text(
            """---
slug: bad
name: Bad Agent
# Missing closing delimiter
""",
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        # Should raise an error during extraction
        with pytest.raises(ValueError):
            main()

    def test_entry_path_format(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Entry path uses POSIX format (forward slashes)."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        self.create_agent_file(agents_dir, "path-test")

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        entry_path = index[0]["entry"]
        # POSIX format uses forward slashes
        assert "/" in entry_path
        assert "\\" not in entry_path
        assert entry_path.endswith("/AGENT.md")

    def test_model_field_preserved(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Preserve model field in index entry."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        self.create_agent_file(agents_dir, "model-test", model="claude-3-5-sonnet-20241022")

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert index[0]["model"] == "claude-3-5-sonnet-20241022"

    def test_tools_field_preserved(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Preserve tools array in index entry."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()

        tools_list = ["Read", "Write", "Bash", "Grep", "Glob", "Task", "WebFetch"]
        self.create_agent_file(agents_dir, "tools-test", tools=tools_list)

        monkeypatch.setattr(sys, "argv", ["build_agents_index.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

        index_file = tmp_path / "index" / "agents-index.json"
        with index_file.open(encoding="utf-8") as f:
            index = json.load(f)

        assert index[0]["tools"] == tools_list
        assert len(index[0]["tools"]) == 7


class TestMetaFieldsConstant:
    """Test META_FIELDS constant."""

    def test_meta_fields_complete(self) -> None:
        """META_FIELDS includes all required fields."""
        expected = ["slug", "name", "description", "model", "tools", "keywords", "version", "owner"]
        assert expected == META_FIELDS

    def test_meta_fields_order(self) -> None:
        """META_FIELDS in expected order."""
        assert META_FIELDS[0] == "slug"
        assert META_FIELDS[1] == "name"
        assert META_FIELDS[2] == "description"
        assert META_FIELDS[3] == "model"
        assert META_FIELDS[4] == "tools"
