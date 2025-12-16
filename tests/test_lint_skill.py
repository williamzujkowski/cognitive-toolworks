"""Unit tests for tooling/lint_skill.py"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from typing import TYPE_CHECKING

from lint_skill import (
    REQUIRED_SECTIONS_ORDER,
    LintIssue,
    check_code_fences,
    check_heading_order,
    check_link_validity,
    check_links,
    extract_body,
    extract_links,
    lint_skill_file,
    main,
    read_text,
)

if TYPE_CHECKING:
    import pytest


class TestReadText:
    """Test file reading utility."""

    def test_read_utf8_file(self, tmp_path: Path) -> None:
        """Read UTF-8 encoded file successfully."""
        test_file = tmp_path / "test.md"
        content = "Hello, 世界! 🌍"
        test_file.write_text(content, encoding="utf-8")
        result = read_text(test_file)
        assert result == content


class TestExtractBody:
    """Test body extraction after front matter."""

    def test_extract_with_front_matter(self) -> None:
        """Extract body when front matter present."""
        md = dedent(
            """\
            ---
            name: Test
            slug: test
            ---
            ## Purpose & When-To-Use
            Body content
            """
        )
        body = extract_body(md)
        assert "## Purpose & When-To-Use" in body
        assert "Body content" in body
        assert "---" not in body

    def test_no_front_matter(self) -> None:
        """Return entire content when no front matter."""
        md = "## Purpose & When-To-Use\nContent"
        body = extract_body(md)
        assert body == md

    def test_unclosed_front_matter(self) -> None:
        """Return entire content when front matter unclosed."""
        md = "---\nname: Test\n## Content"
        body = extract_body(md)
        assert body == md

    def test_empty_content(self) -> None:
        """Handle empty content."""
        body = extract_body("")
        assert body == ""


class TestCheckHeadingOrder:
    """Test heading order validation."""

    def test_correct_order(self, tmp_path: Path) -> None:
        """Accept headings in correct order."""
        body = dedent(
            """\
            ## Purpose & When-To-Use
            Purpose

            ## Pre-Checks
            Checks

            ## Procedure
            Procedure

            ## Decision Rules
            Rules

            ## Output Contract
            Output

            ## Examples
            Examples

            ## Quality Gates
            Gates

            ## Resources
            Resources
            """
        )
        issues = check_heading_order(body, tmp_path / "test.md")
        # Should only have no order errors (missing sections checked elsewhere)
        order_errors = [i for i in issues if "out of order" in i.message]
        assert len(order_errors) == 0

    def test_wrong_order(self, tmp_path: Path) -> None:
        """Detect headings out of order."""
        body = dedent(
            """\
            ## Procedure
            Procedure

            ## Purpose & When-To-Use
            Purpose (should come before Procedure)
            """
        )
        issues = check_heading_order(body, tmp_path / "test.md")
        order_issues = [i for i in issues if "out of order" in i.message]
        assert len(order_issues) > 0
        assert any("Purpose" in i.message for i in order_issues)

    def test_missing_sections(self, tmp_path: Path) -> None:
        """Detect missing required sections."""
        body = "## Purpose & When-To-Use\nOnly one section"
        issues = check_heading_order(body, tmp_path / "test.md")
        missing_issues = [i for i in issues if "Missing required section" in i.message]
        # Should find 7 missing sections
        assert len(missing_issues) == 7

    def test_extra_headings_ignored(self, tmp_path: Path) -> None:
        """Ignore extra headings not in required list."""
        body = dedent(
            """\
            ## Purpose & When-To-Use
            Purpose

            ## Custom Section
            Extra content

            ## Pre-Checks
            Checks
            """
        )
        issues = check_heading_order(body, tmp_path / "test.md")
        # Custom Section should be ignored (not cause errors)
        order_errors = [i for i in issues if "Custom Section" in i.message]
        assert len(order_errors) == 0

    def test_missing_warnings_not_errors(self, tmp_path: Path) -> None:
        """Missing sections should be warnings, not errors."""
        body = "## Purpose & When-To-Use\nOnly one section"
        issues = check_heading_order(body, tmp_path / "test.md")
        missing_issues = [i for i in issues if "Missing required section" in i.message]
        assert all(i.severity == "WARN" for i in missing_issues)


class TestCheckCodeFences:
    """Test code fence validation."""

    def test_properly_closed_fences(self, tmp_path: Path) -> None:
        """Accept properly closed code fences."""
        body = dedent(
            """\
            Some text
            ```python
            code
            ```
            More text
            ```
            another block
            ```
            """
        )
        issues = check_code_fences(body, tmp_path / "test.md")
        assert len(issues) == 0

    def test_unclosed_fence(self, tmp_path: Path) -> None:
        """Detect unclosed code fence."""
        body = dedent(
            """\
            Text
            ```python
            code without closing
            """
        )
        issues = check_code_fences(body, tmp_path / "test.md")
        assert len(issues) == 1
        assert "Unclosed code fence" in issues[0].message
        assert "line 2" in issues[0].message

    def test_no_code_fences(self, tmp_path: Path) -> None:
        """Handle content with no code fences."""
        body = "Just plain text"
        issues = check_code_fences(body, tmp_path / "test.md")
        assert len(issues) == 0

    def test_multiple_unclosed(self, tmp_path: Path) -> None:
        """Detect last unclosed fence in odd number."""
        body = dedent(
            """\
            ```
            block1
            ```
            ```
            block2
            ```
            ```
            unclosed block3
            """
        )
        issues = check_code_fences(body, tmp_path / "test.md")
        assert len(issues) == 1
        assert "line 7" in issues[0].message


class TestExtractLinks:
    """Test link extraction."""

    def test_extract_markdown_links(self) -> None:
        """Extract URLs from markdown links."""
        body = "[Example](https://example.com) and [Test](http://test.org)"
        urls = extract_links(body)
        assert "https://example.com" in urls
        assert "http://test.org" in urls

    def test_extract_bare_urls(self) -> None:
        """Extract bare URLs."""
        body = "Visit https://example.com and http://test.org for details."
        urls = extract_links(body)
        assert "https://example.com" in urls
        assert "http://test.org" in urls

    def test_ignore_relative_links(self) -> None:
        """Ignore relative/internal links."""
        body = "[Internal](../other.md) and [Anchor](#section)"
        urls = extract_links(body)
        assert len(urls) == 0

    def test_deduplicate_urls(self) -> None:
        """Deduplicate repeated URLs."""
        body = "https://example.com and https://example.com again"
        urls = extract_links(body)
        assert len(urls) == 1

    def test_mixed_links(self) -> None:
        """Handle mix of markdown and bare URLs."""
        body = "See [Docs](https://docs.example.com) or https://example.com"
        urls = extract_links(body)
        assert len(urls) == 2
        assert "https://docs.example.com" in urls
        assert "https://example.com" in urls

    def test_no_links(self) -> None:
        """Handle content with no links."""
        body = "Just plain text with no URLs"
        urls = extract_links(body)
        assert len(urls) == 0


class TestCheckLinkValidity:
    """Test link validity checking."""

    def test_valid_url_format(self) -> None:
        """Accept valid URL format (without network call)."""
        # Use mock to avoid actual network call
        with patch("lint_skill.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.status = 200
            mock_urlopen.return_value = mock_response

            is_valid, error = check_link_validity("https://example.com")
            assert is_valid is True
            assert error is None

    def test_invalid_url_format(self) -> None:
        """Reject invalid URL format."""
        is_valid, error = check_link_validity("not-a-url")
        assert is_valid is False
        assert "Invalid URL format" in error

    def test_http_error_404(self) -> None:
        """Handle HTTP 404 errors."""
        with patch("lint_skill.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = HTTPError("url", 404, "Not Found", {}, None)  # type: ignore[arg-type]

            is_valid, error = check_link_validity("https://example.com/404")
            assert is_valid is False
            assert "HTTP 404" in error

    def test_url_error(self) -> None:
        """Handle URL errors (network issues)."""
        with patch("lint_skill.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = URLError("Connection refused")

            is_valid, error = check_link_validity("https://invalid.example")
            assert is_valid is False
            assert "URL error" in error

    def test_anchor_link(self) -> None:
        """Anchor-only links fail validation (not HTTP/HTTPS)."""
        # Note: extract_links() filters these out, so they shouldn't reach this function
        is_valid, error = check_link_validity("#section-anchor")
        assert is_valid is False
        assert "Invalid URL format" in error

    def test_http_status_error(self) -> None:
        """Handle non-200 HTTP status codes."""
        with patch("lint_skill.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.status = 500
            mock_urlopen.return_value = mock_response

            is_valid, error = check_link_validity("https://example.com/error")
            assert is_valid is False
            assert "HTTP 500" in error

    def test_generic_exception(self) -> None:
        """Handle generic exceptions."""
        with patch("lint_skill.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = Exception("Unexpected error occurred")

            is_valid, error = check_link_validity("https://example.com")
            assert is_valid is False
            assert "Error:" in error


class TestCheckLinks:
    """Test link checking wrapper."""

    def test_no_validation(self, tmp_path: Path) -> None:
        """Skip HTTP validation when validate=False."""
        body = "[Example](https://example.com)"
        issues = check_links(body, tmp_path / "test.md", validate=False)
        assert len(issues) == 0

    def test_with_validation_success(self, tmp_path: Path) -> None:
        """Perform HTTP validation when validate=True."""
        body = "[Example](https://example.com)"

        with patch("lint_skill.check_link_validity") as mock_check:
            mock_check.return_value = (True, None)

            issues = check_links(body, tmp_path / "test.md", validate=True)
            assert len(issues) == 0
            mock_check.assert_called_once()

    def test_with_validation_failure(self, tmp_path: Path) -> None:
        """Report broken links when validation fails."""
        body = "[Broken](https://broken.example.com)"

        with patch("lint_skill.check_link_validity") as mock_check:
            mock_check.return_value = (False, "HTTP 404")

            issues = check_links(body, tmp_path / "test.md", validate=True)
            assert len(issues) == 1
            assert "Broken link" in issues[0].message
            assert "broken.example.com" in issues[0].message
            assert issues[0].severity == "WARN"

    def test_no_links(self, tmp_path: Path) -> None:
        """Handle content with no links."""
        body = "No links here"
        issues = check_links(body, tmp_path / "test.md", validate=True)
        assert len(issues) == 0


class TestLintSkillFile:
    """Test complete skill file linting."""

    def test_valid_skill_file(self, tmp_path: Path) -> None:
        """Lint valid SKILL.md file."""
        skill_file = tmp_path / "SKILL.md"
        skill_file.write_text(
            dedent(
                """\
                ---
                name: Test
                slug: test
                ---

                ## Purpose & When-To-Use
                Purpose

                ## Pre-Checks
                Checks

                ## Procedure
                Procedure

                ## Decision Rules
                Rules

                ## Output Contract
                Output

                ## Examples
                ```
                example
                ```

                ## Quality Gates
                Gates

                ## Resources
                Resources
                """
            ),
            encoding="utf-8",
        )
        issues = lint_skill_file(skill_file, validate_links=False)
        # Should have no order errors or fence errors
        errors = [i for i in issues if i.severity == "ERROR"]
        assert len(errors) == 0

    def test_file_not_found(self, tmp_path: Path) -> None:
        """Handle missing file."""
        issues = lint_skill_file(tmp_path / "nonexistent.md")
        assert len(issues) == 1
        assert "Failed to read file" in issues[0].message

    def test_combined_issues(self, tmp_path: Path) -> None:
        """Detect multiple types of issues."""
        skill_file = tmp_path / "SKILL.md"
        skill_file.write_text(
            dedent(
                """\
                ---
                name: Test
                ---

                ## Procedure
                Wrong order

                ```
                Unclosed fence
                """
            ),
            encoding="utf-8",
        )
        issues = lint_skill_file(skill_file, validate_links=False)

        # Should have order error, unclosed fence, and missing sections
        assert len(issues) > 0
        assert any(
            "out of order" in i.message or "Missing required section" in i.message for i in issues
        )
        assert any("Unclosed code fence" in i.message for i in issues)


class TestMain:
    """Test CLI main function."""

    def create_skill_file(self, path: Path, valid: bool = True) -> Path:
        """Helper to create a test SKILL.md file."""
        if valid:
            content = dedent(
                """\
                ---
                name: Test
                slug: test
                ---

                ## Purpose & When-To-Use
                Purpose

                ## Pre-Checks
                Checks

                ## Procedure
                Procedure

                ## Decision Rules
                Rules

                ## Output Contract
                Output

                ## Examples
                ```
                example
                ```

                ## Quality Gates
                Gates

                ## Resources
                Resources
                """
            )
        else:
            content = dedent(
                """\
                ---
                name: Test
                ---

                ## Procedure
                Wrong order

                ```
                Unclosed fence
                """
            )

        skill_file = path / "SKILL.md"
        skill_file.write_text(content, encoding="utf-8")
        return skill_file

    def test_main_valid_skill(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Lint valid skill successfully."""
        skills_dir = tmp_path / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)
        self.create_skill_file(skills_dir, valid=True)

        monkeypatch.setattr(sys, "argv", ["lint_skill.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

    def test_main_invalid_skill(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Detect errors in invalid skill."""
        skills_dir = tmp_path / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)
        self.create_skill_file(skills_dir, valid=False)

        monkeypatch.setattr(sys, "argv", ["lint_skill.py", "--root", str(tmp_path)])

        result = main()
        assert result == 1  # Should fail due to errors

    def test_main_missing_skills_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Return error when skills dir missing."""
        monkeypatch.setattr(sys, "argv", ["lint_skill.py", "--root", str(tmp_path)])

        result = main()
        assert result == 2

    def test_main_no_skills_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle empty skills directory."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        monkeypatch.setattr(sys, "argv", ["lint_skill.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0

    def test_main_warnings_only(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Pass with warnings only (no errors)."""
        skills_dir = tmp_path / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)

        # Create skill with missing sections (warnings) but no errors
        skill_file = skills_dir / "SKILL.md"
        skill_file.write_text(
            dedent(
                """\
                ---
                name: Test
                ---

                ## Purpose & When-To-Use
                Only one section (will trigger warnings for missing sections)
                """
            ),
            encoding="utf-8",
        )

        monkeypatch.setattr(sys, "argv", ["lint_skill.py", "--root", str(tmp_path)])

        result = main()
        assert result == 0  # Warnings don't cause failure

    def test_main_with_link_validation(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Run with --validate-links flag."""
        skills_dir = tmp_path / "skills" / "test-skill"
        skills_dir.mkdir(parents=True)

        skill_file = skills_dir / "SKILL.md"
        skill_file.write_text(
            dedent(
                """\
                ---
                name: Test
                ---

                ## Purpose & When-To-Use
                Purpose

                [Example](https://example.com)

                ## Pre-Checks
                Checks

                ## Procedure
                Procedure

                ## Decision Rules
                Rules

                ## Output Contract
                Output

                ## Examples
                ```
                example
                ```

                ## Quality Gates
                Gates

                ## Resources
                Resources
                """
            ),
            encoding="utf-8",
        )

        monkeypatch.setattr(
            sys, "argv", ["lint_skill.py", "--root", str(tmp_path), "--validate-links"]
        )

        with patch("lint_skill.check_link_validity") as mock_check:
            mock_check.return_value = (True, None)

            result = main()
            assert result == 0
            # Should have called link validation
            mock_check.assert_called()


class TestLintIssue:
    """Test LintIssue dataclass."""

    def test_issue_creation(self) -> None:
        """Create lint issue with path and message."""
        path = Path("/test/SKILL.md")
        message = "Test error"
        issue = LintIssue(path, message)
        assert issue.path == path
        assert issue.message == message
        assert issue.severity == "ERROR"  # Default

    def test_issue_with_warning(self) -> None:
        """Create warning severity issue."""
        path = Path("/test/SKILL.md")
        issue = LintIssue(path, "Warning message", severity="WARN")
        assert issue.severity == "WARN"


class TestRequiredSectionsOrder:
    """Test REQUIRED_SECTIONS_ORDER constant."""

    def test_sections_complete(self) -> None:
        """Verify all 8 required sections present."""
        assert len(REQUIRED_SECTIONS_ORDER) == 8

    def test_sections_order(self) -> None:
        """Verify sections in expected order."""
        assert REQUIRED_SECTIONS_ORDER[0] == "## Purpose & When-To-Use"
        assert REQUIRED_SECTIONS_ORDER[1] == "## Pre-Checks"
        assert REQUIRED_SECTIONS_ORDER[2] == "## Procedure"
        assert REQUIRED_SECTIONS_ORDER[3] == "## Decision Rules"
        assert REQUIRED_SECTIONS_ORDER[4] == "## Output Contract"
        assert REQUIRED_SECTIONS_ORDER[5] == "## Examples"
        assert REQUIRED_SECTIONS_ORDER[6] == "## Quality Gates"
        assert REQUIRED_SECTIONS_ORDER[7] == "## Resources"
