"""Tests for documentation site parser."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from cognitive_toolworks.sources.docs import DocsParser, parse_docs


class TestDocsParser:
    """Tests for DocsParser class."""

    def test_parse_single_markdown_file(self) -> None:
        """Test parsing a single markdown file."""
        content = """# Test Documentation

This is a test documentation page.

## Installation

```bash
pip install test-package
```

## Usage

```python
import test_package
test_package.run()
```

## API Reference

### function_name(param1, param2)

Does something useful.
"""
        with TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "test.md"
            temp_path.write_text(content)

            parser = DocsParser()
            result = parser.parse_markdown_file(temp_path)

            assert result.site_name == "Test Documentation"
            assert len(result.pages) == 1
            assert result.pages[0].title == "Test Documentation"
            assert len(result.code_examples) > 0
            assert any(ex["language"] == "bash" for ex in result.code_examples)
            assert any(ex["language"] == "python" for ex in result.code_examples)

    def test_parse_markdown_directory(self) -> None:
        """Test parsing a directory of markdown files."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)

            # Create multiple markdown files
            (temp_dir / "index.md").write_text("# Main Documentation\n\nWelcome!")
            (temp_dir / "installation.md").write_text(
                "# Installation\n\n```bash\npip install pkg\n```"
            )
            (temp_dir / "usage.md").write_text(
                "# Usage\n\n```python\nimport pkg\npkg.run()\n```"
            )

            parser = DocsParser()
            result = parser.parse_directory(temp_dir)

            assert len(result.pages) == 3
            assert result.site_name in ("Main Documentation", str(temp_dir.name))
            assert len(result.code_examples) >= 2

    def test_parse_html_directory(self) -> None:
        """Test parsing a directory of HTML files."""
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Documentation</title>
</head>
<body>
    <h1>Test Page</h1>
    <p>This is a test page.</p>
    <pre><code>pip install test</code></pre>
</body>
</html>
"""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            (temp_dir / "index.html").write_text(html_content)

            parser = DocsParser()
            result = parser.parse_html_directory(temp_dir)

            assert len(result.pages) >= 1
            assert result.pages[0].title == "Test Documentation"

    def test_extract_title_from_markdown(self) -> None:
        """Test extracting title from markdown content."""
        content = """# My Documentation

Content here.
"""
        parser = DocsParser()
        title = parser._extract_title_from_markdown(content)

        assert title == "My Documentation"

    def test_extract_title_from_markdown_no_header(self) -> None:
        """Test extracting title when no header exists."""
        content = "Just some text without headers."
        parser = DocsParser()
        title = parser._extract_title_from_markdown(content)

        assert title == "Untitled"

    def test_extract_title_from_html(self) -> None:
        """Test extracting title from HTML content."""
        content = """<html>
<head><title>HTML Page Title</title></head>
<body><h1>Header</h1></body>
</html>
"""
        parser = DocsParser()
        title = parser._extract_title_from_html(content)

        assert title == "HTML Page Title"

    def test_extract_title_from_html_h1_fallback(self) -> None:
        """Test extracting title from HTML h1 when no title tag."""
        content = """<html>
<body><h1>Main Header</h1></body>
</html>
"""
        parser = DocsParser()
        title = parser._extract_title_from_html(content)

        assert title == "Main Header"

    def test_extract_text_from_html(self) -> None:
        """Test extracting text content from HTML."""
        content = """<html>
<head><style>body { color: red; }</style></head>
<body>
    <script>alert('test');</script>
    <p>This is visible text.</p>
    <div>More text &amp; symbols.</div>
</body>
</html>
"""
        parser = DocsParser()
        text = parser._extract_text_from_html(content)

        assert "This is visible text" in text
        assert "More text & symbols" in text
        assert "alert" not in text
        assert "color: red" not in text

    def test_extract_code_examples(self) -> None:
        """Test extracting code examples from markdown."""
        content = """# Documentation

Example 1:

```python
print("Hello")
```

Example 2:

```bash
echo "World"
```
"""
        parser = DocsParser()
        examples = parser._extract_code_examples(content)

        assert len(examples) == 2
        assert examples[0]["language"] == "python"
        assert "print" in examples[0]["code"]
        assert examples[1]["language"] == "bash"
        assert "echo" in examples[1]["code"]

    def test_extract_code_examples_no_language(self) -> None:
        """Test extracting code examples without language specification."""
        content = """# Docs

```
generic code
```
"""
        parser = DocsParser()
        examples = parser._extract_code_examples(content)

        assert len(examples) == 1
        assert examples[0]["language"] == "text"
        assert "generic code" in examples[0]["code"]

    def test_extract_api_references(self) -> None:
        """Test extracting API references."""
        content = """# API Reference

## Functions

def calculate_sum(a, b)

Returns the sum of a and b.

## Classes

class DataProcessor(BaseProcessor)

Processes data.
"""
        parser = DocsParser()
        refs = parser._extract_api_references(content)

        assert len(refs) >= 1
        # Check for function reference
        func_refs = [r for r in refs if r["type"] == "function"]
        assert len(func_refs) >= 1
        assert any(r["name"] == "calculate_sum" for r in func_refs)

        # Check for class reference
        class_refs = [r for r in refs if r["type"] == "class"]
        assert len(class_refs) >= 1
        assert any(r["name"] == "DataProcessor" for r in class_refs)

    def test_extract_installation_instructions(self) -> None:
        """Test extracting installation instructions."""
        content = """# Installation

Install via pip:

```bash
pip install my-package
```

Or via npm:

```bash
npm install my-package
```
"""
        parser = DocsParser()
        instructions = parser._extract_installation_instructions(content)

        assert len(instructions) >= 2
        assert any("pip install" in inst for inst in instructions)
        assert any("npm install" in inst for inst in instructions)

    def test_extract_installation_various_package_managers(self) -> None:
        """Test extracting installation for various package managers."""
        content = """
pip install pkg1
npm install pkg2
yarn add pkg3
gem install pkg4
go get pkg5
cargo install pkg6
"""
        parser = DocsParser()
        instructions = parser._extract_installation_instructions(content)

        assert len(instructions) >= 6
        assert any("pip" in inst for inst in instructions)
        assert any("npm" in inst for inst in instructions)
        assert any("yarn" in inst for inst in instructions)
        assert any("gem" in inst for inst in instructions)
        assert any("go get" in inst for inst in instructions)
        assert any("cargo" in inst for inst in instructions)

    def test_extract_usage_patterns(self) -> None:
        """Test extracting usage patterns."""
        content = """# Usage

Basic usage:

```python
import mylib
mylib.run()
```

Advanced usage:

```python
from mylib import advanced
advanced.process()
```
"""
        parser = DocsParser()
        patterns = parser._extract_usage_patterns(content)

        assert len(patterns) == 2
        assert all(p["language"] == "python" for p in patterns)
        assert "import mylib" in patterns[0]["code"]
        assert "Basic usage:" in patterns[0]["description"]

    def test_is_api_page(self) -> None:
        """Test API page detection."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()

        api_page = PageInfo(title="API Reference", url="api.md", content="")
        assert parser._is_api_page(api_page) is True

        regular_page = PageInfo(title="Getting Started", url="start.md", content="")
        assert parser._is_api_page(regular_page) is False

    def test_is_installation_page(self) -> None:
        """Test installation page detection."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()

        install_page = PageInfo(
            title="Installation Guide", url="install.md", content=""
        )
        assert parser._is_installation_page(install_page) is True

        other_page = PageInfo(title="Tutorial", url="tutorial.md", content="")
        assert parser._is_installation_page(other_page) is False

    def test_is_usage_page(self) -> None:
        """Test usage page detection."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()

        usage_page = PageInfo(title="Usage Examples", url="usage.md", content="")
        assert parser._is_usage_page(usage_page) is True

        other_page = PageInfo(title="FAQ", url="faq.md", content="")
        assert parser._is_usage_page(other_page) is False

    def test_build_hierarchy(self) -> None:
        """Test building page hierarchy."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()
        parser.pages = [
            PageInfo(title="Index", url="index.md", content="", parent=None),
            PageInfo(title="Page 1", url="page1.md", content="", parent="index.md"),
            PageInfo(title="Page 2", url="page2.md", content="", parent="index.md"),
            PageInfo(title="Sub Page", url="sub.md", content="", parent="page1.md"),
        ]

        hierarchy = parser._build_hierarchy()

        assert "root" in hierarchy
        assert "index.md" in hierarchy
        assert "page1.md" in hierarchy
        assert len(hierarchy["root"]) == 1
        assert len(hierarchy["index.md"]) == 2

    def test_build_search_index(self) -> None:
        """Test building search index."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()
        parser.pages = [
            PageInfo(title="Getting Started Guide", url="start.md", content=""),
            PageInfo(title="API Reference", url="api.md", content=""),
        ]

        index = parser._build_search_index()

        assert "getting started guide" in index
        assert index["getting started guide"] == "start.md"
        assert "api reference" in index
        assert index["api reference"] == "api.md"

    def test_detect_site_name_from_mkdocs(self) -> None:
        """Test detecting site name from mkdocs.yml."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            mkdocs_config = temp_dir / "mkdocs.yml"
            mkdocs_config.write_text("site_name: My Documentation Site\n")

            parser = DocsParser()
            site_name = parser._detect_site_name(temp_dir)

            assert site_name == "My Documentation Site"

    def test_detect_site_name_from_sphinx_conf(self) -> None:
        """Test detecting site name from Sphinx conf.py."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            conf_py = temp_dir / "conf.py"
            conf_py.write_text('project = "Sphinx Project"\n')

            parser = DocsParser()
            site_name = parser._detect_site_name(temp_dir)

            assert site_name == "Sphinx Project"

    def test_detect_site_name_from_readme(self) -> None:
        """Test detecting site name from README."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            readme = temp_dir / "README.md"
            readme.write_text("# Project Name\n\nDescription here.")

            parser = DocsParser()
            site_name = parser._detect_site_name(temp_dir)

            assert site_name == "Project Name"

    def test_detect_site_name_fallback_to_directory(self) -> None:
        """Test falling back to directory name."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)

            parser = DocsParser()
            site_name = parser._detect_site_name(temp_dir)

            assert site_name == temp_dir.name

    def test_parse_directory_with_subdirectories(self) -> None:
        """Test parsing directory with subdirectories."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)

            # Create nested structure
            (temp_dir / "index.md").write_text("# Main\n")
            subdir = temp_dir / "guides"
            subdir.mkdir()
            (subdir / "guide1.md").write_text("# Guide 1\n")
            (subdir / "guide2.md").write_text("# Guide 2\n")

            parser = DocsParser()
            result = parser.parse_directory(temp_dir)

            assert len(result.pages) == 3
            assert any(p.title == "Main" for p in result.pages)
            assert any(p.title == "Guide 1" for p in result.pages)
            assert any(p.title == "Guide 2" for p in result.pages)

    def test_parse_directory_invalid_path(self) -> None:
        """Test parsing with invalid directory path."""
        parser = DocsParser()

        with pytest.raises(ValueError, match="does not exist"):
            parser.parse_directory(Path("/nonexistent/path"))

    def test_parse_directory_file_instead_of_directory(self) -> None:
        """Test parsing when path is a file instead of directory."""
        with TemporaryDirectory() as tmpdir:
            temp_file = Path(tmpdir) / "file.md"
            temp_file.write_text("# Content\n")

            parser = DocsParser()

            with pytest.raises(ValueError, match="not a directory"):
                parser.parse_directory(temp_file)

    def test_parse_html_directory_invalid_path(self) -> None:
        """Test parsing HTML with invalid directory path."""
        parser = DocsParser()

        with pytest.raises(ValueError, match="does not exist"):
            parser.parse_html_directory(Path("/nonexistent/path"))

    def test_extract_all_code_examples(self) -> None:
        """Test extracting all code examples from multiple pages."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()
        parser.pages = [
            PageInfo(
                title="Page 1",
                url="page1.md",
                content="```python\nprint('hello')\n```",
            ),
            PageInfo(
                title="Page 2",
                url="page2.md",
                content="```bash\necho world\n```",
            ),
        ]

        examples = parser._extract_all_code_examples()

        assert len(examples) == 2
        assert examples[0]["source_page"] == "Page 1"
        assert examples[1]["source_page"] == "Page 2"
        assert examples[0]["language"] == "python"
        assert examples[1]["language"] == "bash"

    def test_extract_all_api_references(self) -> None:
        """Test extracting all API references from multiple pages."""
        from cognitive_toolworks.models import PageInfo

        parser = DocsParser()
        parser.pages = [
            PageInfo(
                title="API Reference",
                url="api.md",
                content="def my_function(arg1, arg2)",
            ),
            PageInfo(
                title="Not API",
                url="guide.md",
                content="def another_function()",
            ),
        ]

        refs = parser._extract_all_api_references()

        # Only API pages should be extracted - check that API page refs exist
        api_refs = [r for r in refs if r.get("source_page") == "API Reference"]
        assert len(api_refs) >= 1
        # Verify the function was extracted from API page
        assert any(r["name"] == "my_function" for r in api_refs)

    def test_parse_docs_function_markdown_file(self) -> None:
        """Test parse_docs convenience function with markdown file."""
        with TemporaryDirectory() as tmpdir:
            temp_file = Path(tmpdir) / "test.md"
            temp_file.write_text("# Test\n\nContent here.")

            result = parse_docs(temp_file)

            assert result.site_name == "Test"
            assert len(result.pages) == 1

    def test_parse_docs_function_markdown_directory(self) -> None:
        """Test parse_docs convenience function with markdown directory."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            (temp_dir / "index.md").write_text("# Index\n")
            (temp_dir / "page.md").write_text("# Page\n")

            result = parse_docs(temp_dir)

            assert len(result.pages) == 2

    def test_parse_docs_function_html_directory(self) -> None:
        """Test parse_docs convenience function with HTML directory."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            (temp_dir / "index.html").write_text(
                "<html><head><title>Test</title></head></html>"
            )

            result = parse_docs(temp_dir)

            assert len(result.pages) >= 1

    def test_parse_docs_function_auto_detect_format(self) -> None:
        """Test parse_docs with auto format detection."""
        with TemporaryDirectory() as tmpdir:
            # Test markdown auto-detection
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Test\n")
            result = parse_docs(md_file, format_type="auto")
            assert len(result.pages) == 1

    def test_parse_docs_function_explicit_format(self) -> None:
        """Test parse_docs with explicit format type."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            (temp_dir / "test.md").write_text("# Test\n")

            result = parse_docs(temp_dir, format_type="markdown")

            assert len(result.pages) == 1

    def test_parse_docs_function_invalid_format(self) -> None:
        """Test parse_docs with invalid format type."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)

            with pytest.raises(ValueError, match="Unsupported format"):
                parse_docs(temp_dir, format_type="invalid")

    def test_parse_docs_function_no_files_found(self) -> None:
        """Test parse_docs when no markdown or HTML files found."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)
            (temp_dir / "test.txt").write_text("Not markdown or HTML")

            with pytest.raises(ValueError, match="No markdown or HTML files found"):
                parse_docs(temp_dir, format_type="auto")

    def test_parse_docs_function_unsupported_file_extension(self) -> None:
        """Test parse_docs with unsupported file extension."""
        with TemporaryDirectory() as tmpdir:
            temp_file = Path(tmpdir) / "test.txt"
            temp_file.write_text("Content")

            with pytest.raises(ValueError, match="Cannot auto-detect format"):
                parse_docs(temp_file, format_type="auto")

    def test_parse_docs_function_with_base_url(self) -> None:
        """Test parse_docs with base URL parameter."""
        with TemporaryDirectory() as tmpdir:
            temp_file = Path(tmpdir) / "test.md"
            temp_file.write_text("# Test\n")

            result = parse_docs(temp_file, base_url="https://example.com/docs")

            assert result.base_url == "https://example.com/docs"

    def test_comprehensive_real_world_pattern(self) -> None:
        """Test parsing a realistic documentation structure."""
        with TemporaryDirectory() as tmpdir:
            temp_dir = Path(tmpdir)

            # Create realistic doc structure
            (temp_dir / "mkdocs.yml").write_text("site_name: My Project Docs\n")
            (temp_dir / "index.md").write_text(
                """# My Project

Welcome to My Project documentation.

## Quick Start

```bash
pip install myproject
```
"""
            )

            guides_dir = temp_dir / "guides"
            guides_dir.mkdir()
            (guides_dir / "installation.md").write_text(
                """# Installation

Install via pip:

```bash
pip install myproject
```

Or via conda:

```bash
conda install myproject
```
"""
            )

            (guides_dir / "usage.md").write_text(
                """# Usage

Basic usage:

```python
from myproject import MyClass

obj = MyClass()
obj.run()
```

Advanced usage:

```python
from myproject import advanced

advanced.process(data)
```
"""
            )

            api_dir = temp_dir / "api"
            api_dir.mkdir()
            (api_dir / "reference.md").write_text(
                """# API Reference

## Classes

class MyClass(BaseClass)

Main class for the library.

## Functions

def process_data(data, options)

Processes the input data.
"""
            )

            parser = DocsParser()
            result = parser.parse_directory(temp_dir)

            # Verify structure
            assert result.site_name == "My Project Docs"
            assert len(result.pages) >= 4

            # Verify code examples
            assert len(result.code_examples) >= 4
            bash_examples = [
                ex for ex in result.code_examples if ex["language"] == "bash"
            ]
            python_examples = [
                ex for ex in result.code_examples if ex["language"] == "python"
            ]
            assert len(bash_examples) >= 2
            assert len(python_examples) >= 2

            # Verify installation instructions
            assert len(result.installation_instructions) >= 1
            assert any(
                "pip install" in inst for inst in result.installation_instructions
            )

            # Verify API references
            assert len(result.api_references) >= 1

            # Verify hierarchy
            assert len(result.page_hierarchy) >= 1

            # Verify search index
            assert len(result.search_index) >= 1


class TestDocsAnalysisModel:
    """Tests for DocsAnalysis dataclass."""

    def test_docs_analysis_to_dict(self) -> None:
        """Test converting DocsAnalysis to dictionary."""
        from cognitive_toolworks.models import DocsAnalysis, PageInfo

        page = PageInfo(title="Test", url="test.md", content="Content")
        analysis = DocsAnalysis(
            site_name="Test Site",
            base_url="https://example.com",
            pages=[page],
            code_examples=[{"language": "python", "code": "print('hi')"}],
        )

        result = analysis.to_dict()

        assert result["site_name"] == "Test Site"
        assert result["base_url"] == "https://example.com"
        assert len(result["pages"]) == 1
        assert result["pages"][0]["title"] == "Test"
        assert len(result["code_examples"]) == 1


class TestPageInfoModel:
    """Tests for PageInfo dataclass."""

    def test_page_info_to_dict(self) -> None:
        """Test converting PageInfo to dictionary."""
        from cognitive_toolworks.models import PageInfo

        page = PageInfo(
            title="Test Page",
            url="test.md",
            content="Test content",
            parent="index.md",
            children=["child1.md", "child2.md"],
            level=1,
        )

        result = page.to_dict()

        assert result["title"] == "Test Page"
        assert result["url"] == "test.md"
        assert result["content"] == "Test content"
        assert result["parent"] == "index.md"
        assert len(result["children"]) == 2
        assert result["level"] == 1
