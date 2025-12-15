"""Tests for README parser."""

from pathlib import Path
from tempfile import NamedTemporaryFile

from cognitive_toolworks.sources.readme import ReadmeParser, parse_readme


class TestReadmeParser:
    """Tests for ReadmeParser class."""

    def test_basic_parsing(self) -> None:
        """Test basic README parsing."""
        content = """# Test Project

This is a test project description.

## Installation

```bash
pip install test-project
```

## Usage

```python
import test_project
test_project.run()
```

## Features

- Feature 1
- Feature 2
- Feature 3
"""
        parser = ReadmeParser(content)
        result = parser.parse()

        assert result.project_name == "Test Project"
        assert "test project description" in result.description
        assert result.installation is not None
        assert "pip install test-project" in result.installation
        assert len(result.usage_examples) > 0
        assert len(result.features) == 3
        assert "Feature 1" in result.features

    def test_extract_sections(self) -> None:
        """Test section extraction."""
        content = """# Main Title

Content here.

## Section 1

Section 1 content.

## Section 2

Section 2 content.
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()

        assert "Main Title" in sections
        assert "Section 1" in sections
        assert "Section 2" in sections
        assert "Section 1 content" in sections["Section 1"]

    def test_extract_badges(self) -> None:
        """Test badge extraction."""
        content = """# Project

[![CI](https://img.shields.io/badge/ci-passing-green)](https://ci.example.com)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://example.com)

Description here.
"""
        parser = ReadmeParser(content)
        badges = parser._extract_badges()

        assert len(badges) >= 2
        assert any(b["alt"] == "CI" for b in badges)
        assert any("img.shields.io" in b.get("image_url", "") for b in badges)

    def test_extract_code_blocks(self) -> None:
        """Test code block extraction."""
        content = """# Project

Install:

```bash
npm install project
```

Usage:

```javascript
const project = require('project');
project.run();
```
"""
        parser = ReadmeParser(content)
        code_blocks = parser._extract_code_blocks()

        assert len(code_blocks) == 2
        assert code_blocks[0]["language"] == "bash"
        assert "npm install" in code_blocks[0]["content"]
        assert code_blocks[1]["language"] == "javascript"
        assert "require" in code_blocks[1]["content"]

    def test_extract_usage_examples(self) -> None:
        """Test usage examples extraction."""
        content = """# Project

## Usage

Basic usage:

```python
import mylib
mylib.hello()
```

Advanced usage:

```python
import mylib
mylib.advanced_feature()
```
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()
        examples = parser._extract_usage_examples(sections)

        assert len(examples) == 2
        assert all(ex["language"] == "python" for ex in examples)
        assert "import mylib" in examples[0]["code"]

    def test_extract_features(self) -> None:
        """Test feature list extraction."""
        content = """# Project

## Features

- Fast performance
- Easy to use
- Well documented
- Extensible architecture
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()
        features = parser._extract_features(sections)

        assert len(features) == 4
        assert "Fast performance" in features
        assert "Easy to use" in features

    def test_extract_dependencies_pip(self) -> None:
        """Test dependency extraction from pip install."""
        content = """## Installation

```bash
pip install requests numpy pandas
```
"""
        parser = ReadmeParser(content)
        deps = parser._extract_dependencies(content)

        assert "requests" in deps
        assert "numpy" in deps
        assert "pandas" in deps

    def test_extract_dependencies_npm(self) -> None:
        """Test dependency extraction from npm install."""
        content = """## Installation

```bash
npm install express lodash axios
```
"""
        parser = ReadmeParser(content)
        deps = parser._extract_dependencies(content)

        assert "express" in deps
        assert "lodash" in deps
        assert "axios" in deps

    def test_extract_dependencies_with_flags(self) -> None:
        """Test dependency extraction ignores flags."""
        content = """## Setup

```bash
pip install --upgrade requests
npm install -D jest
```
"""
        parser = ReadmeParser(content)
        deps = parser._extract_dependencies(content)

        assert "requests" in deps
        assert "jest" in deps
        # Flags should not be included
        assert "--upgrade" not in deps
        assert "-D" not in deps

    def test_extract_project_name(self) -> None:
        """Test project name extraction."""
        content = """# My Awesome Project

Description here.
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()
        name = parser._extract_project_name(sections)

        assert name == "My Awesome Project"

    def test_extract_description(self) -> None:
        """Test description extraction."""
        content = """# Project

This is the project description.
It spans multiple lines.

## Installation

Install instructions.
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()
        description = parser._extract_description(sections)

        assert "project description" in description.lower()

    def test_real_world_readme_pattern_1(self) -> None:
        """Test parsing a real-world README pattern (Python project)."""
        content = """# cognitive-toolworks

[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](https://github.com/user/repo)
[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://pypi.org/project/cognitive-toolworks/)

Generate AI agent skills from various sources.

## Features

- Parse MCP servers
- Parse OpenAPI specs
- Parse README files
- Generate SKILL.md files

## Installation

```bash
pip install cognitive-toolworks
```

## Usage

```python
from cognitive_toolworks import ReadmeParser

parser = ReadmeParser(content)
result = parser.parse()
```

## API Reference

See the full API documentation at [docs](https://example.com/docs).
"""
        parser = ReadmeParser(content)
        result = parser.parse()

        assert result.project_name == "cognitive-toolworks"
        assert "AI agent skills" in result.description
        assert result.installation is not None
        assert "pip install" in result.installation
        assert len(result.features) == 4
        assert "Parse MCP servers" in result.features
        assert len(result.usage_examples) > 0
        assert result.usage_examples[0]["language"] == "python"
        assert len(result.badges) >= 2
        assert result.api_reference is not None
        assert len(result.dependencies) > 0

    def test_real_world_readme_pattern_2(self) -> None:
        """Test parsing a real-world README pattern (Node.js project)."""
        content = """# express-api

A lightweight Express.js API framework.

## Quick Start

```bash
npm install express-api
```

## Example

Create an API in seconds:

```javascript
const api = require('express-api');

api.get('/hello', (req, res) => {
  res.json({ message: 'Hello World' });
});

api.start(3000);
```

## Features

* Automatic routing
* Built-in validation
* TypeScript support
"""
        parser = ReadmeParser(content)
        result = parser.parse()

        assert result.project_name == "express-api"
        assert "Express.js API" in result.description
        assert result.installation is not None
        assert "npm install" in result.installation
        assert len(result.features) == 3
        assert "Automatic routing" in result.features
        assert len(result.usage_examples) > 0

    def test_parse_readme_function(self) -> None:
        """Test convenience parse_readme function."""
        content = """# Test

Test description.

## Install

```bash
pip install test
```
"""
        with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            result = parse_readme(temp_path)
            assert result.project_name == "Test"
            assert result.description == "Test description."
        finally:
            temp_path.unlink()

    def test_empty_sections(self) -> None:
        """Test handling of README with minimal content."""
        content = """# Minimal Project

Just a title.
"""
        parser = ReadmeParser(content)
        result = parser.parse()

        assert result.project_name == "Minimal Project"
        assert result.description == "Just a title."
        assert result.installation is None
        assert len(result.usage_examples) == 0
        assert len(result.features) == 0

    def test_nested_headers(self) -> None:
        """Test handling of nested header levels."""
        content = """# Main

## Section 1

Content 1.

### Subsection 1.1

Sub-content.

## Section 2

Content 2.
"""
        parser = ReadmeParser(content)
        sections = parser._extract_sections()

        assert "Section 1" in sections
        assert "Section 2" in sections
        # Subsections should be included in parent section
        assert "Subsection 1.1" in sections["Section 1"]

    def test_multiple_code_blocks_same_section(self) -> None:
        """Test multiple code blocks in the same section."""
        content = """# Project

## Examples

First example:

```python
print("Hello")
```

Second example:

```python
print("World")
```
"""
        parser = ReadmeParser(content)
        code_blocks = parser._extract_code_blocks()

        assert len(code_blocks) == 2
        assert all(cb["language"] == "python" for cb in code_blocks)

    def test_code_block_without_language(self) -> None:
        """Test code blocks without language specification."""
        content = """# Project

```
generic code
without language
```
"""
        parser = ReadmeParser(content)
        code_blocks = parser._extract_code_blocks()

        assert len(code_blocks) == 1
        assert code_blocks[0]["language"] == "text"
        assert "generic code" in code_blocks[0]["content"]
