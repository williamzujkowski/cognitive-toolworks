"""
Documentation Site Parser Module.

Extracts structured information from documentation sites (Sphinx, MkDocs, etc.).
Supports parsing local HTML files, markdown directories, and remote documentation URLs.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from cognitive_toolworks.models import DocsAnalysis, PageInfo

if TYPE_CHECKING:
    from typing import Any


class DocsParser:
    """
    Parses documentation sites to extract structured information.

    Supports common documentation formats including Sphinx, MkDocs, and similar
    static site generators. Extracts page hierarchy, code examples, API references,
    installation instructions, and usage patterns.
    """

    # Common section header patterns for documentation
    INSTALLATION_HEADERS: ClassVar[set[str]] = {
        "installation",
        "install",
        "setup",
        "getting started",
        "quickstart",
        "quick start",
        "prerequisites",
    }

    USAGE_HEADERS: ClassVar[set[str]] = {
        "usage",
        "examples",
        "example",
        "tutorial",
        "tutorials",
        "guide",
        "guides",
        "how to",
        "how-to",
    }

    API_HEADERS: ClassVar[set[str]] = {
        "api",
        "api reference",
        "api documentation",
        "reference",
        "class reference",
        "function reference",
        "module reference",
    }

    def __init__(self, base_path: Path | None = None, base_url: str = "") -> None:
        """
        Initialize parser.

        Args:
            base_path: Base directory for local documentation files.
            base_url: Base URL for remote documentation.
        """
        self.base_path = base_path
        self.base_url = base_url
        self.pages: list[PageInfo] = []
        self.navigation: dict[str, Any] = {}

    def parse_directory(self, directory: Path) -> DocsAnalysis:
        """
        Parse a directory of markdown documentation files.

        Args:
            directory: Path to documentation directory.

        Returns:
            DocsAnalysis with extracted documentation structure.
        """
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        self.base_path = directory
        self.pages = []

        # Find all markdown files
        md_files = list(directory.rglob("*.md"))

        # Parse each markdown file
        for md_file in md_files:
            page = self._parse_markdown_file(md_file)
            if page:
                self.pages.append(page)

        # Build hierarchy
        hierarchy = self._build_hierarchy()

        # Extract cross-cutting information
        code_examples = self._extract_all_code_examples()
        api_references = self._extract_all_api_references()
        installation = self._extract_all_installation_instructions()
        usage_patterns = self._extract_all_usage_patterns()

        # Detect site name
        site_name = self._detect_site_name(directory)

        return DocsAnalysis(
            site_name=site_name,
            base_url=self.base_url,
            pages=self.pages,
            page_hierarchy=hierarchy,
            code_examples=code_examples,
            api_references=api_references,
            installation_instructions=installation,
            usage_patterns=usage_patterns,
            navigation_structure=self.navigation,
            search_index=self._build_search_index(),
        )

    def parse_html_directory(self, directory: Path) -> DocsAnalysis:
        """
        Parse a directory of HTML documentation files (e.g., Sphinx build output).

        Args:
            directory: Path to HTML documentation directory.

        Returns:
            DocsAnalysis with extracted documentation structure.
        """
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        self.base_path = directory
        self.pages = []

        # Find all HTML files
        html_files = list(directory.rglob("*.html"))

        # Parse each HTML file
        for html_file in html_files:
            page = self._parse_html_file(html_file)
            if page:
                self.pages.append(page)

        # Build hierarchy
        hierarchy = self._build_hierarchy()

        # Extract information
        code_examples = self._extract_all_code_examples()
        api_references = self._extract_all_api_references()
        installation = self._extract_all_installation_instructions()
        usage_patterns = self._extract_all_usage_patterns()

        # Detect site name
        site_name = self._detect_site_name(directory)

        return DocsAnalysis(
            site_name=site_name,
            base_url=self.base_url,
            pages=self.pages,
            page_hierarchy=hierarchy,
            code_examples=code_examples,
            api_references=api_references,
            installation_instructions=installation,
            usage_patterns=usage_patterns,
            navigation_structure=self.navigation,
            search_index=self._build_search_index(),
        )

    def parse_markdown_file(self, file_path: Path) -> DocsAnalysis:
        """
        Parse a single markdown file.

        Args:
            file_path: Path to markdown file.

        Returns:
            DocsAnalysis with single page.
        """
        page = self._parse_markdown_file(file_path)
        if not page:
            page = PageInfo(
                title="Unknown",
                url=str(file_path),
                content="",
            )

        self.pages = [page]

        return DocsAnalysis(
            site_name=page.title,
            base_url=self.base_url,
            pages=[page],
            code_examples=self._extract_code_examples(page.content),
            api_references=self._extract_api_references(page.content),
            installation_instructions=self._extract_installation_instructions(page.content),
            usage_patterns=self._extract_usage_patterns(page.content),
        )

    def _parse_markdown_file(self, file_path: Path) -> PageInfo | None:
        """Parse a single markdown file into a PageInfo object."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

        # Extract title (first # header)
        title = self._extract_title_from_markdown(content)

        # Compute relative URL
        if self.base_path:
            relative_path = file_path.relative_to(self.base_path)
            url = str(relative_path)
        else:
            url = str(file_path)

        # Compute hierarchy level based on path depth
        level = len(file_path.relative_to(self.base_path).parts) - 1 if self.base_path else 0

        # Determine parent from directory structure
        parent = None
        if self.base_path and file_path.parent != self.base_path:
            parent_index = file_path.parent / "index.md"
            if parent_index.exists():
                parent = str(parent_index.relative_to(self.base_path))

        return PageInfo(
            title=title,
            url=url,
            content=content,
            parent=parent,
            level=level,
        )

    def _parse_html_file(self, file_path: Path) -> PageInfo | None:
        """Parse a single HTML file into a PageInfo object."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

        # Extract title from HTML
        title = self._extract_title_from_html(content)

        # Extract text content from HTML (simple approach)
        text_content = self._extract_text_from_html(content)

        # Compute relative URL
        if self.base_path:
            relative_path = file_path.relative_to(self.base_path)
            url = str(relative_path)
        else:
            url = str(file_path)

        # Compute hierarchy level
        level = len(file_path.relative_to(self.base_path).parts) - 1 if self.base_path else 0

        return PageInfo(
            title=title,
            url=url,
            content=text_content,
            level=level,
        )

    def _extract_title_from_markdown(self, content: str) -> str:
        """Extract title from markdown content."""
        # Look for first # header
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()

        return "Untitled"

    def _extract_title_from_html(self, content: str) -> str:
        """Extract title from HTML content."""
        # Try <title> tag first
        title_match = re.search(r"<title>([^<]+)</title>", content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()

        # Try first <h1>
        h1_match = re.search(r"<h1[^>]*>([^<]+)</h1>", content, re.IGNORECASE)
        if h1_match:
            return h1_match.group(1).strip()

        return "Untitled"

    def _extract_text_from_html(self, content: str) -> str:
        """
        Extract text content from HTML (simplified).

        This is a basic implementation. For production use,
        consider using BeautifulSoup or similar libraries.
        """
        # Remove script and style tags
        content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL | re.IGNORECASE)

        # Remove HTML tags
        content = re.sub(r"<[^>]+>", " ", content)

        # Decode HTML entities (basic)
        content = content.replace("&nbsp;", " ")
        content = content.replace("&lt;", "<")
        content = content.replace("&gt;", ">")
        content = content.replace("&amp;", "&")
        content = content.replace("&quot;", '"')

        # Normalize whitespace
        content = re.sub(r"\s+", " ", content)

        return content.strip()

    def _build_hierarchy(self) -> dict[str, list[str]]:
        """Build page hierarchy from parsed pages."""
        hierarchy: dict[str, list[str]] = {}

        for page in self.pages:
            # Group by parent
            parent_key = page.parent or "root"
            if parent_key not in hierarchy:
                hierarchy[parent_key] = []
            hierarchy[parent_key].append(page.url)

        return hierarchy

    def _extract_all_code_examples(self) -> list[dict[str, str]]:
        """Extract all code examples from all pages."""
        examples = []
        for page in self.pages:
            page_examples = self._extract_code_examples(page.content)
            for example in page_examples:
                example["source_page"] = page.title
                example["source_url"] = page.url
                examples.append(example)
        return examples

    def _extract_code_examples(self, content: str) -> list[dict[str, str]]:
        """Extract code examples from markdown content."""
        examples = []
        in_code_block = False
        current_language = ""
        current_content: list[str] = []

        for line in content.split("\n"):
            if line.startswith("```"):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    current_language = line[3:].strip() or "text"
                    current_content = []
                else:
                    # Ending a code block
                    in_code_block = False
                    examples.append(
                        {
                            "language": current_language,
                            "code": "\n".join(current_content),
                        }
                    )
            elif in_code_block:
                current_content.append(line)

        return examples

    def _extract_all_api_references(self) -> list[dict[str, Any]]:
        """Extract all API references from all pages."""
        api_refs = []
        for page in self.pages:
            # Check if this is an API reference page
            if self._is_api_page(page):
                refs = self._extract_api_references(page.content)
                for ref in refs:
                    ref["source_page"] = page.title
                    ref["source_url"] = page.url
                    api_refs.append(ref)
        return api_refs

    def _extract_api_references(self, content: str) -> list[dict[str, Any]]:
        """Extract API reference information from content."""
        refs = []

        # Look for function/method signatures
        # Pattern: def function_name(params) or function_name(params)
        func_pattern = r"(?:def\s+)?(\w+)\s*\(([^)]*)\)"
        for match in re.finditer(func_pattern, content):
            name = match.group(1)
            params = match.group(2)
            refs.append(
                {
                    "type": "function",
                    "name": name,
                    "signature": match.group(0),
                    "parameters": params,
                }
            )

        # Look for class definitions
        # Pattern: class ClassName or class ClassName(Base)
        class_pattern = r"class\s+(\w+)(?:\(([^)]*)\))?"
        for match in re.finditer(class_pattern, content):
            name = match.group(1)
            bases = match.group(2) or ""
            refs.append(
                {
                    "type": "class",
                    "name": name,
                    "bases": bases,
                }
            )

        return refs

    def _is_api_page(self, page: PageInfo) -> bool:
        """Check if a page is an API reference page."""
        title_lower = page.title.lower()
        return any(keyword in title_lower for keyword in self.API_HEADERS)

    def _extract_all_installation_instructions(self) -> list[str]:
        """Extract installation instructions from all pages."""
        instructions = []
        for page in self.pages:
            if self._is_installation_page(page):
                page_instructions = self._extract_installation_instructions(page.content)
                instructions.extend(page_instructions)
        return instructions

    def _extract_installation_instructions(self, content: str) -> list[str]:
        """Extract installation instructions from content."""
        instructions = []

        # Look for package manager commands
        patterns = [
            r"pip install\s+([^\n]+)",
            r"npm install\s+([^\n]+)",
            r"yarn add\s+([^\n]+)",
            r"gem install\s+([^\n]+)",
            r"go get\s+([^\n]+)",
            r"cargo install\s+([^\n]+)",
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                instruction = match.group(0).strip()
                if instruction not in instructions:
                    instructions.append(instruction)

        return instructions

    def _is_installation_page(self, page: PageInfo) -> bool:
        """Check if a page contains installation instructions."""
        title_lower = page.title.lower()
        return any(keyword in title_lower for keyword in self.INSTALLATION_HEADERS)

    def _extract_all_usage_patterns(self) -> list[dict[str, str]]:
        """Extract usage patterns from all pages."""
        patterns = []
        for page in self.pages:
            if self._is_usage_page(page):
                page_patterns = self._extract_usage_patterns(page.content)
                for pattern in page_patterns:
                    pattern["source_page"] = page.title
                    pattern["source_url"] = page.url
                    patterns.append(pattern)
        return patterns

    def _extract_usage_patterns(self, content: str) -> list[dict[str, str]]:
        """Extract usage patterns from content."""
        patterns = []

        # Extract code blocks from usage sections
        in_code_block = False
        current_language = ""
        current_content: list[str] = []
        description = ""

        for line in content.split("\n"):
            if line.startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    current_language = line[3:].strip() or "text"
                    current_content = []
                else:
                    in_code_block = False
                    patterns.append(
                        {
                            "language": current_language,
                            "code": "\n".join(current_content),
                            "description": description.strip(),
                        }
                    )
                    description = ""
            elif in_code_block:
                current_content.append(line)
            else:
                # Capture description before code block
                if line.strip() and not line.startswith("#"):
                    description += line + " "

        return patterns

    def _is_usage_page(self, page: PageInfo) -> bool:
        """Check if a page contains usage information."""
        title_lower = page.title.lower()
        return any(keyword in title_lower for keyword in self.USAGE_HEADERS)

    def _detect_site_name(self, directory: Path) -> str:
        """Detect documentation site name from directory or config files."""
        # Try mkdocs.yml
        mkdocs_config = directory / "mkdocs.yml"
        if mkdocs_config.exists():
            content = mkdocs_config.read_text()
            site_name_match = re.search(r"site_name:\s*['\"]?([^'\"]+)['\"]?", content)
            if site_name_match:
                return site_name_match.group(1).strip()

        # Try conf.py (Sphinx)
        conf_py = directory / "conf.py"
        if conf_py.exists():
            content = conf_py.read_text()
            project_match = re.search(r"project\s*=\s*['\"]([^'\"]+)['\"]", content)
            if project_match:
                return project_match.group(1).strip()

        # Try README or index
        for filename in ["README.md", "index.md", "index.html"]:
            index_file = directory / filename
            if index_file.exists():
                if filename.endswith(".md"):
                    content = index_file.read_text()
                    title = self._extract_title_from_markdown(content)
                    if title != "Untitled":
                        return title
                elif filename.endswith(".html"):
                    content = index_file.read_text()
                    title = self._extract_title_from_html(content)
                    if title != "Untitled":
                        return title

        # Fall back to directory name
        return directory.name

    def _build_search_index(self) -> dict[str, str]:
        """Build a simple search index from page titles and URLs."""
        index = {}
        for page in self.pages:
            # Map title to URL
            index[page.title.lower()] = page.url

            # Also index words in title
            words = page.title.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    if word not in index:
                        index[word] = page.url
                    else:
                        # Multiple pages for same word - keep first
                        pass

        return index


def parse_docs(
    path: Path | str,
    base_url: str = "",
    format_type: str = "auto",
) -> DocsAnalysis:
    """
    Convenience function to parse documentation.

    Args:
        path: Path to documentation directory or file.
        base_url: Base URL for the documentation site.
        format_type: Format type - "auto", "markdown", or "html".

    Returns:
        DocsAnalysis with extracted documentation structure.

    Raises:
        ValueError: If path is invalid or format is unsupported.
    """
    path_obj = Path(path) if isinstance(path, str) else path

    parser = DocsParser(base_url=base_url)

    # Determine format
    if format_type == "auto":
        if path_obj.is_file():
            if path_obj.suffix == ".md":
                format_type = "markdown"
            elif path_obj.suffix == ".html":
                format_type = "html"
            else:
                raise ValueError(f"Cannot auto-detect format for: {path_obj}")
        elif path_obj.is_dir():
            # Check for markdown or HTML files
            has_md = any(path_obj.rglob("*.md"))
            has_html = any(path_obj.rglob("*.html"))
            if has_md:
                format_type = "markdown"
            elif has_html:
                format_type = "html"
            else:
                raise ValueError(f"No markdown or HTML files found in: {path_obj}")

    # Parse based on format
    if format_type == "markdown":
        if path_obj.is_file():
            return parser.parse_markdown_file(path_obj)
        else:
            return parser.parse_directory(path_obj)
    elif format_type == "html":
        if path_obj.is_file():
            raise ValueError("HTML file parsing not implemented for single files")
        else:
            return parser.parse_html_directory(path_obj)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
