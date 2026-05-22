"""Unit tests for tooling/validate_skill.py"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import pytest

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from validate_skill import (
    MAX_CODEBLOCK_LINES,
    MAX_DESCRIPTION_LEN,
    MAX_EXAMPLE_LINES,
    FrontMatter,
    SkillValidationIssue,
    extract_front_matter,
    find_code_blocks,
    first_examples_block_len,
    has_token_budgets,
    scan_secrets,
    validate_skill_file,
)


class TestFrontMatterExtraction:
    """Test YAML front matter extraction from markdown."""

    def test_valid_front_matter(self) -> None:
        """Extract valid front matter successfully."""
        md = dedent("""\
            ---
            name: Test Skill
            slug: test-skill
            version: 1.0.0
            ---
            # Content here
            """)
        fm = extract_front_matter(md)
        assert isinstance(fm, FrontMatter)
        assert fm.meta["name"] == "Test Skill"
        assert fm.meta["slug"] == "test-skill"
        assert "# Content here" in fm.body

    def test_missing_starting_delimiter(self) -> None:
        """Raise error when starting --- is missing."""
        md = "name: Test\n---\n# Content"
        with pytest.raises(ValueError, match="Missing starting '---'"):
            extract_front_matter(md)

    def test_missing_closing_delimiter(self) -> None:
        """Raise error when closing --- is missing."""
        md = "---\nname: Test\n# Content"
        with pytest.raises(ValueError, match="Missing closing '---'"):
            extract_front_matter(md)

    def test_invalid_yaml(self) -> None:
        """Raise error for invalid YAML syntax."""
        md = "---\nname: Test\n  invalid: : yaml\n---\n# Content"
        with pytest.raises(ValueError, match="Failed to parse front matter YAML"):
            extract_front_matter(md)

    def test_non_dict_front_matter(self) -> None:
        """Raise error if front matter is not a mapping."""
        md = "---\n- item1\n- item2\n---\n# Content"
        with pytest.raises(ValueError, match="Front matter must be a YAML mapping"):
            extract_front_matter(md)

    def test_empty_front_matter(self) -> None:
        """Handle empty front matter (returns empty dict)."""
        md = "---\n---\n# Content"
        fm = extract_front_matter(md)
        assert fm.meta == {}
        assert "# Content" in fm.body


class TestCodeBlockDetection:
    """Test fenced code block detection."""

    def test_single_code_block(self) -> None:
        """Detect single code block."""
        text = dedent("""\
            Some text
            ```python
            print("hello")
            ```
            More text
            """)
        blocks = find_code_blocks(text)
        assert len(blocks) == 1
        assert blocks[0] == (1, 3)  # Line indices

    def test_multiple_code_blocks(self) -> None:
        """Detect multiple code blocks."""
        text = dedent("""\
            ```
            code1
            ```
            Text between
            ```
            code2
            ```
            """)
        blocks = find_code_blocks(text)
        assert len(blocks) == 2

    def test_no_code_blocks(self) -> None:
        """Return empty list when no code blocks present."""
        text = "Just plain text"
        blocks = find_code_blocks(text)
        assert blocks == []

    def test_unclosed_code_block(self) -> None:
        """Handle unclosed code block (returns no blocks)."""
        text = "```\ncode\n"
        blocks = find_code_blocks(text)
        assert blocks == []


class TestExampleBlockLength:
    """Test example block length calculation."""

    def test_example_with_code_block(self) -> None:
        """Calculate length of example code block."""
        text = dedent("""\
            ## Examples

            ```python
            line1
            line2
            line3
            ```
            """)
        length = first_examples_block_len(text)
        assert length == 3

    def test_no_examples_section(self) -> None:
        """Return None when ## Examples section missing."""
        text = "## Other Section\nContent"
        length = first_examples_block_len(text)
        assert length is None

    def test_examples_without_code_block(self) -> None:
        """Return None when Examples has no code block."""
        text = "## Examples\n\nJust text"
        length = first_examples_block_len(text)
        assert length is None

    def test_multiple_code_blocks_uses_first(self) -> None:
        """Use first code block in Examples section."""
        text = dedent("""\
            ## Examples

            ```
            first
            ```

            ```
            second
            second2
            ```
            """)
        length = first_examples_block_len(text)
        assert length == 1  # First block has 1 line


class TestTokenBudgetDetection:
    """Test token budget (T1/T2/T3) detection."""

    def test_all_budgets_present(self) -> None:
        """Return True when T1, T2, T3 all present."""
        text = "T1 budget, T2 extended, T3 deep"
        assert has_token_budgets(text) is True

    def test_missing_t1(self) -> None:
        """Return False when T1 missing."""
        text = "T2 and T3 present"
        assert has_token_budgets(text) is False

    def test_missing_t2(self) -> None:
        """Return False when T2 missing."""
        text = "T1 and T3 present"
        assert has_token_budgets(text) is False

    def test_missing_t3(self) -> None:
        """Return False when T3 missing."""
        text = "T1 and T2 present"
        assert has_token_budgets(text) is False

    def test_no_budgets(self) -> None:
        """Return False when no budgets present."""
        text = "Just regular text"
        assert has_token_budgets(text) is False


class TestSecretScanning:
    """Test secret pattern detection."""

    def test_aws_access_key(self) -> None:
        """Detect AWS access key pattern."""
        text = "AKIAIOSFODNN7EXAMPLE"  # gitleaks:allow
        result = scan_secrets(text)
        assert result is not None
        assert "AKIA" in result

    def test_private_key(self) -> None:
        """Detect private key pattern."""
        text = "-----BEGIN RSA PRIVATE KEY-----"
        result = scan_secrets(text)
        assert result is not None
        assert "PRIVATE KEY" in result

    def test_ssh_key(self) -> None:
        """Detect SSH key pattern."""
        text = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB"
        result = scan_secrets(text)
        assert result is not None

    def test_password_pattern(self) -> None:
        """Detect password assignment."""
        text = "password: mysecretpass123"
        result = scan_secrets(text)
        assert result is not None

    def test_secret_pattern(self) -> None:
        """Detect secret assignment."""
        text = "SECRET=topsecret123456"  # gitleaks:allow
        result = scan_secrets(text)
        assert result is not None

    def test_no_secrets(self) -> None:
        """Return None when no secrets detected."""
        text = "Just normal text with no secrets"
        result = scan_secrets(text)
        assert result is None


class TestSkillFileValidation:
    """Test complete skill file validation."""

    def test_minimal_valid_skill(self, tmp_path: Path) -> None:
        """Validate minimal valid SKILL.md file."""
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent("""\
                ---
                name: Test Skill
                slug: test-skill
                description: A test skill for validation
                capabilities: [test]
                inputs: {test: string}
                outputs: {result: string}
                keywords: [test, validation]
                version: 1.0.0
                owner: test
                license: Apache-2.0
                security: standard
                links: [http://example.com]
                ---

                ## Purpose & When-To-Use
                Test purpose

                ## Pre-Checks
                Test checks

                ## Procedure
                T1 fast path
                T2 extended
                T3 deep

                ## Decision Rules
                Test rules

                ## Output Contract
                Test output

                ## Quality Gates
                Test gates with T1 T2 T3

                ## Resources
                Test resources

                ## Examples

                ```python
                print("example")
                ```
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        assert issues == []

    def test_missing_required_metadata(self, tmp_path: Path) -> None:
        """Detect missing required metadata keys."""
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent("""\
                ---
                name: Test
                slug: test
                ---
                # Content
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        assert len(issues) > 0
        assert any("Missing metadata keys" in i.message for i in issues)

    def test_description_too_long(self, tmp_path: Path) -> None:
        """Detect description exceeding max length."""
        long_desc = "x" * (MAX_DESCRIPTION_LEN + 1)
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent(f"""\
                ---
                name: Test
                slug: test
                description: {long_desc}
                capabilities: [test]
                inputs: {{}}
                outputs: {{}}
                keywords: [test]
                version: 1.0.0
                owner: test
                license: Apache-2.0
                security: standard
                links: []
                ---
                # Content
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        assert any("description too long" in i.message for i in issues)

    def test_missing_required_sections(self, tmp_path: Path) -> None:
        """Detect missing required body sections."""
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent("""\
                ---
                name: Test
                slug: test
                description: Test
                capabilities: [test]
                inputs: {}
                outputs: {}
                keywords: [test]
                version: 1.0.0
                owner: test
                license: Apache-2.0
                security: standard
                links: []
                ---

                ## Purpose & When-To-Use
                Only one section
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        # Should find multiple missing sections
        missing_section_issues = [i for i in issues if "Missing required section" in i.message]
        assert len(missing_section_issues) > 0

    def test_missing_token_budgets(self, tmp_path: Path) -> None:
        """Detect missing token budgets."""
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent("""\
                ---
                name: Test
                slug: test
                description: Test
                capabilities: [test]
                inputs: {}
                outputs: {}
                keywords: [test]
                version: 1.0.0
                owner: test
                license: Apache-2.0
                security: standard
                links: []
                ---

                ## Purpose & When-To-Use
                Purpose

                ## Pre-Checks
                Checks

                ## Procedure
                No budgets here

                ## Decision Rules
                Rules

                ## Output Contract
                Output

                ## Quality Gates
                Gates

                ## Resources
                Resources

                ## Examples
                ```
                example
                ```
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        assert any("Token budgets" in i.message for i in issues)

    def test_example_too_long(self, tmp_path: Path) -> None:
        """Detect example exceeding max lines."""
        long_example = "\n".join([f"line{i}" for i in range(MAX_EXAMPLE_LINES + 5)])
        skill = tmp_path / "SKILL.md"
        content = f"""---
name: Test
slug: test
description: Test
capabilities: [test]
inputs: {{}}
outputs: {{}}
keywords: [test]
version: 1.0.0
owner: test
license: Apache-2.0
security: standard
links: []
---

## Purpose & When-To-Use
Purpose

## Pre-Checks
Checks

## Procedure
T1 T2 T3

## Decision Rules
Rules

## Output Contract
Output

## Quality Gates
Gates

## Resources
Resources

## Examples

```python
{long_example}
```
"""
        skill.write_text(content, encoding="utf-8")
        issues = validate_skill_file(skill)
        assert any("Example too long" in i.message for i in issues)

    def test_code_block_too_long(self, tmp_path: Path) -> None:
        """Detect code block exceeding max lines."""
        huge_code = "\n".join([f"line{i}" for i in range(MAX_CODEBLOCK_LINES + 5)])
        skill = tmp_path / "SKILL.md"
        content = f"""---
name: Test
slug: test
description: Test
capabilities: [test]
inputs: {{}}
outputs: {{}}
keywords: [test]
version: 1.0.0
owner: test
license: Apache-2.0
security: standard
links: []
---

## Purpose & When-To-Use
Purpose

## Pre-Checks
Checks

## Procedure
T1 T2 T3

## Decision Rules
Rules

## Output Contract
Output

## Quality Gates
Gates

## Resources

```
{huge_code}
```

## Examples
```
small example
```
"""
        skill.write_text(content, encoding="utf-8")
        issues = validate_skill_file(skill)
        assert any("Code block too long" in i.message for i in issues)

    def test_secret_detection(self, tmp_path: Path) -> None:
        """Detect secrets in skill file."""
        skill = tmp_path / "SKILL.md"
        skill.write_text(
            dedent("""\
                ---
                name: Test
                slug: test
                description: Test
                capabilities: [test]
                inputs: {}
                outputs: {}
                keywords: [test]
                version: 1.0.0
                owner: test
                license: Apache-2.0
                security: standard
                links: []
                ---

                ## Purpose & When-To-Use
                Don't include AKIAIOSFODNN7EXAMPLE in docs  # gitleaks:allow

                ## Pre-Checks
                Checks

                ## Procedure
                T1 T2 T3

                ## Decision Rules
                Rules

                ## Output Contract
                Output

                ## Quality Gates
                Gates

                ## Resources
                Resources

                ## Examples
                ```
                example
                ```
                """),
            encoding="utf-8",
        )
        issues = validate_skill_file(skill)
        assert any("secret" in i.message.lower() for i in issues)


class TestSkillValidationIssue:
    """Test SkillValidationIssue dataclass."""

    def test_issue_creation(self) -> None:
        """Create validation issue with path and message."""
        path = Path("/test/SKILL.md")
        message = "Test error"
        issue = SkillValidationIssue(path, message)
        assert issue.path == path
        assert issue.message == message
