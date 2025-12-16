"""
README/Documentation Parser Module.

Extracts structured information from README files and documentation.
Supports markdown parsing and section extraction.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar

from cognitive_toolworks.models import ReadmeAnalysis

if TYPE_CHECKING:
    from pathlib import Path


class ReadmeParser:
    """
    Parses README and documentation files to extract structured information.

    Analyzes markdown structure, extracts sections, code blocks, badges,
    and other metadata useful for skill generation.
    """

    # Common section header patterns (case-insensitive)
    INSTALLATION_HEADERS: ClassVar[set[str]] = {
        "installation",
        "install",
        "setup",
        "getting started",
        "quickstart",
        "quick start",
    }
    USAGE_HEADERS: ClassVar[set[str]] = {
        "usage",
        "examples",
        "example",
        "getting started",
        "quickstart",
    }
    FEATURES_HEADERS: ClassVar[set[str]] = {
        "features",
        "capabilities",
        "what's included",
    }
    API_HEADERS: ClassVar[set[str]] = {
        "api",
        "api reference",
        "reference",
        "documentation",
    }

    def __init__(self, content: str) -> None:
        """
        Initialize parser with README content.

        Args:
            content: Raw markdown content of the README file.
        """
        self.content = content
        self.lines = content.split("\n")

    def parse(self) -> ReadmeAnalysis:
        """
        Parse the README and extract structured information.

        Returns:
            ReadmeAnalysis containing extracted sections and metadata.
        """
        sections = self._extract_sections()
        badges = self._extract_badges()

        # Extract key information
        project_name = self._extract_project_name(sections)
        description = self._extract_description(sections)
        installation = self._find_section_content(sections, self.INSTALLATION_HEADERS)
        usage_examples = self._extract_usage_examples(sections)
        features = self._extract_features(sections)
        api_reference = self._find_section_content(sections, self.API_HEADERS)
        dependencies = self._extract_dependencies(installation or "")

        return ReadmeAnalysis(
            project_name=project_name,
            description=description,
            installation=installation,
            usage_examples=usage_examples,
            features=features,
            api_reference=api_reference,
            dependencies=dependencies,
            badges=badges,
            sections=sections,
        )

    def _extract_sections(self) -> dict[str, str]:
        """
        Extract sections by markdown headers.

        Returns:
            Dictionary mapping section titles to their content.
        """
        sections: dict[str, str] = {}
        current_section: str | None = None
        current_content: list[str] = []

        for line in self.lines:
            # Check if line is a header
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line)

            if header_match:
                # Save previous section if exists
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                # Only track top-level and second-level headers
                if level <= 2:
                    current_section = title
                    current_content = []
                else:
                    # Sub-sections are part of current section
                    if current_section:
                        current_content.append(line)
            else:
                if current_section:
                    current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _extract_badges(self) -> list[dict[str, str]]:
        """
        Extract badges from markdown image links.

        Returns:
            List of badge dictionaries with 'alt', 'url', and 'link' keys.
        """
        badges = []

        # Pattern: [![alt](image_url)](link_url)
        badge_pattern = r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)"

        for match in re.finditer(badge_pattern, self.content):
            badges.append(
                {
                    "alt": match.group(1),
                    "image_url": match.group(2),
                    "link": match.group(3),
                }
            )

        # Also match simple image syntax: ![alt](url)
        simple_image_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"

        for match in re.finditer(simple_image_pattern, self.content):
            # Avoid duplicates from badge pattern
            alt = match.group(1)
            url = match.group(2)

            # Check if this looks like a badge (shields.io, badge URLs, etc.)
            if any(badge_host in url for badge_host in ["shields.io", "badge", "img.shields.io"]):
                # Check if not already added
                if not any(b.get("image_url") == url for b in badges):
                    badges.append({"alt": alt, "image_url": url, "link": ""})

        return badges

    def _extract_code_blocks(self) -> list[dict[str, str]]:
        """
        Extract code blocks with their language and content.

        Returns:
            List of dictionaries with 'language' and 'content' keys.
        """
        code_blocks = []
        in_code_block = False
        current_language = ""
        current_content: list[str] = []

        for line in self.lines:
            # Check for code block start
            if line.startswith("```"):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    current_language = line[3:].strip() or "text"
                    current_content = []
                else:
                    # Ending a code block
                    in_code_block = False
                    code_blocks.append(
                        {
                            "language": current_language,
                            "content": "\n".join(current_content),
                        }
                    )
            elif in_code_block:
                current_content.append(line)

        return code_blocks

    def _extract_project_name(self, sections: dict[str, str]) -> str:
        """
        Extract project name from the first header or document title.

        Args:
            sections: Extracted sections dictionary.

        Returns:
            Project name string.
        """
        # Try first header
        for line in self.lines:
            if line.startswith("# "):
                return line[2:].strip()

        # Fallback to first section title
        if sections:
            return next(iter(sections.keys()))

        return "Unknown Project"

    def _extract_description(self, sections: dict[str, str]) -> str:
        """
        Extract project description.

        Args:
            sections: Extracted sections dictionary.

        Returns:
            Project description string.
        """
        # Look for content after the first header but before second section
        first_section_key = next(iter(sections.keys())) if sections else None

        if first_section_key:
            content = sections[first_section_key]

            # Extract first paragraph
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

            if paragraphs:
                # Filter out badge lines and get first real paragraph
                for para in paragraphs:
                    if not para.startswith("![") and not para.startswith("[!["):
                        return para

        return ""

    def _find_section_content(
        self,
        sections: dict[str, str],
        header_keywords: set[str],
    ) -> str | None:
        """
        Find section content by matching header keywords.

        Args:
            sections: Extracted sections dictionary.
            header_keywords: Set of keywords to match against section titles.

        Returns:
            Section content if found, None otherwise.
        """
        for title, content in sections.items():
            title_lower = title.lower()
            if any(keyword in title_lower for keyword in header_keywords):
                return content

        return None

    def _extract_usage_examples(self, sections: dict[str, str]) -> list[dict[str, str]]:
        """
        Extract usage examples from usage/examples sections.

        Args:
            sections: Extracted sections dictionary.

        Returns:
            List of usage example dictionaries.
        """
        examples = []

        # Find usage/examples section
        usage_content = self._find_section_content(sections, self.USAGE_HEADERS)

        if usage_content:
            # Extract code blocks from usage section
            in_code_block = False
            current_language = ""
            current_content: list[str] = []
            description = ""

            for line in usage_content.split("\n"):
                if line.startswith("```"):
                    if not in_code_block:
                        in_code_block = True
                        current_language = line[3:].strip() or "text"
                        current_content = []
                    else:
                        in_code_block = False
                        examples.append(
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
                    if line.strip():
                        description += line + " "

        return examples

    def _extract_features(self, sections: dict[str, str]) -> list[str]:
        """
        Extract feature list from features section.

        Args:
            sections: Extracted sections dictionary.

        Returns:
            List of feature strings.
        """
        features = []

        # Find features section
        features_content = self._find_section_content(sections, self.FEATURES_HEADERS)

        if features_content:
            # Extract bullet points
            for line in features_content.split("\n"):
                line = line.strip()
                # Match markdown list items (-, *, +)
                if re.match(r"^[-*+]\s+", line):
                    feature = re.sub(r"^[-*+]\s+", "", line).strip()
                    features.append(feature)

        return features

    def _extract_dependencies(self, installation_content: str) -> list[str]:
        """
        Extract dependencies from installation instructions.

        Args:
            installation_content: Content of installation section.

        Returns:
            List of dependency strings.
        """
        dependencies: list[str] = []

        if not installation_content:
            return dependencies

        # Look for common package manager commands
        patterns = [
            r"pip install\s+([^\n]+)",
            r"npm install\s+([^\n]+)",
            r"yarn add\s+([^\n]+)",
            r"gem install\s+([^\n]+)",
            r"go get\s+([^\n]+)",
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, installation_content)
            for match in matches:
                # Parse package names
                packages = match.group(1).strip()

                # Split into tokens
                tokens = packages.split()

                # Filter out flags and options (anything starting with -)
                for token in tokens:
                    token = token.strip()
                    # Skip flags
                    if token.startswith("-"):
                        continue
                    # Add valid package names
                    if token and token not in dependencies:
                        dependencies.append(token)

        return dependencies


def parse_readme(path: Path) -> ReadmeAnalysis:
    """
    Convenience function to parse a README file.

    Args:
        path: Path to README file.

    Returns:
        ReadmeAnalysis with extracted information.
    """
    content = path.read_text(encoding="utf-8")
    parser = ReadmeParser(content)
    return parser.parse()
