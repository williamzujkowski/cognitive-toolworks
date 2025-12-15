"""
AAIF (AI Agent Infrastructure Foundation) standards validator.

Validates skills against AAIF ecosystem conventions:
- Progressive disclosure (T1/T2/T3 tiers)
- Token budgets enforcement
- Inter-skill compatibility
- Security constraints
- Required sections and structure
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

import yaml

from cognitive_toolworks.analyzers.tokens import count_tokens
from cognitive_toolworks.validators.anthropic import (
    ValidationIssue,
    ValidationSeverity,
)

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class AAIFValidationResult:
    """Result of AAIF validation."""

    valid: bool
    tier_compliance: dict[str, bool] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)
    score: float = 0.0

    @property
    def errors(self) -> list[ValidationIssue]:
        """Get only error-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Get only warning-level issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "valid": self.valid,
            "tier_compliance": self.tier_compliance,
            "issues": [i.to_dict() for i in self.issues],
            "score": self.score,
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "info": len(
                    [i for i in self.issues if i.severity == ValidationSeverity.INFO]
                ),
            },
        }


class AAIFValidator:
    """
    Validates skills against AAIF standards.

    AAIF requirements:
    - T1 tier: ≤2k tokens (fast path, 80% of requests)
    - T2 tier: ≤6k tokens (extended validation)
    - T3 tier: ≤12k tokens (deep research)
    - Progressive disclosure structure
    - Required sections in specific order
    - Inter-skill references must be valid
    - Security constraints declared
    """

    # AAIF token budgets
    T1_TOKEN_BUDGET = 2000
    T2_TOKEN_BUDGET = 6000
    T3_TOKEN_BUDGET = 12000

    # Required frontmatter fields per CLAUDE.md
    REQUIRED_FIELDS: ClassVar[list[str]] = [
        "name",
        "slug",
        "description",
        "capabilities",
        "inputs",
        "outputs",
        "keywords",
        "version",
        "owner",
        "license",
        "security",
        "links",
    ]

    # Required sections in order per CLAUDE.md Section 3
    REQUIRED_SECTIONS: ClassVar[list[str]] = [
        "Purpose & When-To-Use",
        "Pre-Checks",
        "Procedure",
        "Decision Rules",
        "Output Contract",
        "Examples",
        "Quality Gates",
        "Resources",
    ]

    # Naming convention pattern
    SLUG_PATTERN = re.compile(r"^(?:core-|[a-z]+-[a-z]+-)[a-z]+$")

    def validate(self, content: str) -> AAIFValidationResult:
        """
        Validate skill content against AAIF standards.

        Args:
            content: The SKILL.md content.

        Returns:
            AAIFValidationResult with compliance details.
        """
        issues: list[ValidationIssue] = []
        tier_compliance: dict[str, bool] = {}

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)

        if frontmatter is None:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="frontmatter",
                    message="Missing or invalid YAML frontmatter",
                    fix_suggestion="Add frontmatter starting with --- and ending with ---",
                )
            )
            return AAIFValidationResult(
                valid=False, issues=issues, tier_compliance={}, score=0.0
            )

        # Validate frontmatter fields
        issues.extend(self._validate_frontmatter(frontmatter))

        # Validate naming convention
        issues.extend(self._validate_naming_convention(frontmatter))

        # Validate required sections
        issues.extend(self._validate_sections(content))

        # Validate token budgets and tier compliance
        tier_issues, tier_compliance = self._validate_token_budgets(content)
        issues.extend(tier_issues)

        # Validate progressive disclosure structure
        issues.extend(self._validate_progressive_disclosure(content))

        # Validate inter-skill references
        issues.extend(self._validate_skill_references(content))

        # Validate security constraints
        issues.extend(self._validate_security(frontmatter, content))

        # Calculate compliance score
        score = self._calculate_compliance_score(issues, tier_compliance)

        # Determine overall validity
        valid = not any(i.severity == ValidationSeverity.ERROR for i in issues)

        return AAIFValidationResult(
            valid=valid,
            tier_compliance=tier_compliance,
            issues=issues,
            score=score,
        )

    def validate_file(self, path: Path) -> AAIFValidationResult:
        """Validate a SKILL.md file."""
        content = path.read_text()
        return self.validate(content)

    def _extract_frontmatter(self, content: str) -> dict[str, Any] | None:
        """Extract YAML frontmatter from content."""
        lines = content.split("\n")

        if not lines or lines[0].strip() != "---":
            return None

        frontmatter_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            frontmatter_lines.append(line)

        if not frontmatter_lines:
            return None

        try:
            result: dict[str, Any] | None = yaml.safe_load("\n".join(frontmatter_lines))
            return result if isinstance(result, dict) else None
        except yaml.YAMLError:
            return None

    def _validate_frontmatter(
        self, frontmatter: dict[str, Any]
    ) -> list[ValidationIssue]:
        """Validate required frontmatter fields."""
        issues: list[ValidationIssue] = []

        for field_name in self.REQUIRED_FIELDS:
            if field_name not in frontmatter:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field=field_name,
                        message=f"{field_name} is required in frontmatter",
                        fix_suggestion=f"Add {field_name} to frontmatter",
                    )
                )
            elif not frontmatter[field_name]:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field=field_name,
                        message=f"{field_name} cannot be empty",
                        fix_suggestion=f"Provide a value for {field_name}",
                    )
                )

        # Validate description length (≤160 per CLAUDE.md)
        if "description" in frontmatter:
            desc = frontmatter["description"]
            if isinstance(desc, str) and len(desc) > 160:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field="description",
                        message=f"description exceeds 160 chars ({len(desc)})",
                        fix_suggestion="Shorten description to 160 characters or less",
                    )
                )

        # Validate security field declares constraints
        if "security" in frontmatter:
            sec = frontmatter["security"]
            if isinstance(sec, str) and len(sec) < 10:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        field="security",
                        message="security field should explicitly declare constraints",
                        fix_suggestion='Use format like "Public; no secrets or PII; safe for open repositories"',
                    )
                )

        return issues

    def _validate_naming_convention(
        self, frontmatter: dict[str, Any]
    ) -> list[ValidationIssue]:
        """Validate naming convention follows AAIF standards."""
        issues: list[ValidationIssue] = []

        slug = frontmatter.get("slug", "")
        if not slug:
            return issues  # Already caught by required fields check

        # Validate slug format
        if not self.SLUG_PATTERN.match(slug):
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="slug",
                    message="slug should follow AAIF naming convention: {domain}-{scope}-{action}",
                    fix_suggestion="Use format: core-*, {domain}-{scope}-{action}, or {tech}-{scope}-{action}",
                )
            )

        # Validate name matches slug pattern
        name = frontmatter.get("name", "")
        if name and slug:
            # Name should be lowercase, alphanumeric + hyphens
            if not re.match(r"^[a-z0-9-\s]+$", name.lower()):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.INFO,
                        field="name",
                        message="name should use lowercase letters, numbers, hyphens, and spaces",
                    )
                )

        return issues

    def _validate_sections(self, content: str) -> list[ValidationIssue]:
        """Validate required sections are present in correct order."""
        issues: list[ValidationIssue] = []

        # Find all section headers
        section_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
        sections_found = section_pattern.findall(content)

        # Check for required sections
        for required_section in self.REQUIRED_SECTIONS:
            found = any(
                required_section.lower() in section.lower()
                for section in sections_found
            )
            if not found:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field="sections",
                        message=f"Missing required section: {required_section}",
                        fix_suggestion=f"Add ## {required_section} section",
                    )
                )

        # Check section order (optional but recommended)
        section_order = []
        for section in sections_found:
            for i, required in enumerate(self.REQUIRED_SECTIONS):
                if required.lower() in section.lower():
                    section_order.append((i, required))
                    break

        # Verify order is ascending
        if section_order:
            for i in range(len(section_order) - 1):
                if section_order[i][0] > section_order[i + 1][0]:
                    issues.append(
                        ValidationIssue(
                            severity=ValidationSeverity.WARNING,
                            field="sections",
                            message=f"Sections out of order: {section_order[i][1]} appears before {section_order[i + 1][1]}",
                            fix_suggestion="Reorder sections per AAIF standards",
                        )
                    )
                    break

        return issues

    def _validate_token_budgets(
        self, content: str
    ) -> tuple[list[ValidationIssue], dict[str, bool]]:
        """Validate token budgets for each tier."""
        issues: list[ValidationIssue] = []
        tier_compliance: dict[str, bool] = {}

        # Extract body (after frontmatter)
        lines = content.split("\n")
        body_start = 0
        in_frontmatter = False

        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    body_start = i + 1
                    break

        body = "\n".join(lines[body_start:])

        # Count tokens for T1 tier (frontmatter + Purpose + Pre-Checks + T1 Procedure + Output Contract)
        t1_content = self._extract_t1_content(content)
        t1_tokens = count_tokens(t1_content)
        tier_compliance["T1"] = t1_tokens <= self.T1_TOKEN_BUDGET

        if t1_tokens > self.T1_TOKEN_BUDGET:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="tokens",
                    message=f"T1 tier exceeds {self.T1_TOKEN_BUDGET} tokens ({t1_tokens})",
                    fix_suggestion="Move detailed content to T2/T3 sections or reference files",
                )
            )
        elif t1_tokens > self.T1_TOKEN_BUDGET * 0.9:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="tokens",
                    message=f"T1 tier approaching token budget ({t1_tokens}/{self.T1_TOKEN_BUDGET})",
                )
            )

        # Count tokens for T2 tier (T1 + T2 Procedure + Decision Rules + Quality Gates + one example)
        t2_content = self._extract_t2_content(content)
        t2_tokens = count_tokens(t2_content)
        tier_compliance["T2"] = t2_tokens <= self.T2_TOKEN_BUDGET

        if t2_tokens > self.T2_TOKEN_BUDGET:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="tokens",
                    message=f"T2 tier exceeds {self.T2_TOKEN_BUDGET} tokens ({t2_tokens})",
                    fix_suggestion="Move heavy content to T3 or reference files",
                )
            )
        elif t2_tokens > self.T2_TOKEN_BUDGET * 0.9:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="tokens",
                    message=f"T2 tier approaching token budget ({t2_tokens}/{self.T2_TOKEN_BUDGET})",
                )
            )

        # Count tokens for T3 tier (all content)
        t3_tokens = count_tokens(body)
        tier_compliance["T3"] = t3_tokens <= self.T3_TOKEN_BUDGET

        if t3_tokens > self.T3_TOKEN_BUDGET:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="tokens",
                    message=f"T3 tier exceeds {self.T3_TOKEN_BUDGET} tokens ({t3_tokens})",
                    fix_suggestion="Move detailed content to reference files",
                )
            )

        # Check if token budgets are mentioned in Quality Gates
        if "quality gates" in content.lower():
            has_budget_mention = (
                "token" in content.lower() and "budget" in content.lower()
            )
            if not has_budget_mention:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        field="quality-gates",
                        message="Token budgets should be explicitly mentioned in Quality Gates section",
                        fix_suggestion="Add token budget constraints (T1/T2/T3) to Quality Gates",
                    )
                )

        return issues, tier_compliance

    def _extract_t1_content(self, content: str) -> str:
        """Extract T1 tier content."""
        # T1: Front-matter, Purpose, Pre-Checks, T1 Procedure, Output Contract
        sections_to_include = [
            "purpose",
            "when-to-use",
            "pre-checks",
            "output contract",
        ]

        lines = content.split("\n")
        result_lines: list[str] = []
        in_section = False

        for line in lines:
            # Include frontmatter
            if line.strip() == "---":
                result_lines.append(line)
                continue

            # Check for section headers
            if line.startswith("##"):
                section_name = line[2:].strip().lower()
                in_section = any(sect in section_name for sect in sections_to_include)
                if in_section:
                    result_lines.append(line)
            elif in_section:
                # Stop at T2/T3 procedure subsections
                if "###" in line and (
                    "tier 2" in line.lower() or "tier 3" in line.lower()
                ):
                    in_section = False
                else:
                    result_lines.append(line)

        return "\n".join(result_lines)

    def _extract_t2_content(self, content: str) -> str:
        """Extract T2 tier content (T1 + additional sections)."""
        # T2: All T1 + T2 Procedure, Decision Rules, Quality Gates, one example
        sections_to_exclude = ["resources"]

        lines = content.split("\n")
        result_lines: list[str] = []
        in_excluded = False

        for line in lines:
            if line.startswith("##"):
                section_name = line[2:].strip().lower()
                in_excluded = any(sect in section_name for sect in sections_to_exclude)
                if not in_excluded:
                    result_lines.append(line)
            elif not in_excluded:
                result_lines.append(line)

        # Limit examples to first one only
        result = "\n".join(result_lines)
        example_pattern = re.compile(r"(###\s+Example\s+\d)", re.IGNORECASE)
        matches = list(example_pattern.finditer(result))
        if len(matches) > 1:
            # Truncate after first example
            second_example_pos = matches[1].start()
            result = result[:second_example_pos]

        return result

    def _validate_progressive_disclosure(self, content: str) -> list[ValidationIssue]:
        """Validate progressive disclosure structure."""
        issues: list[ValidationIssue] = []

        # Check for tiered procedure sections
        has_t1_procedure = (
            "### step 1" in content.lower() or "t1 procedure" in content.lower()
        )
        has_procedure_section = "## procedure" in content.lower()

        if has_procedure_section and not has_t1_procedure:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    field="procedure",
                    message="Procedure section should be organized by steps or tiers (T1/T2/T3)",
                    fix_suggestion="Use ### Step N subsections to organize procedure",
                )
            )

        # Check that examples are not too verbose (≤30 lines per CLAUDE.md)
        example_sections = re.findall(
            r"###\s+Example.*?(?=###|##|\Z)", content, re.DOTALL | re.IGNORECASE
        )
        for i, example in enumerate(example_sections, 1):
            lines = [line for line in example.split("\n") if line.strip()]
            if len(lines) > 30:
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        field="examples",
                        message=f"Example {i} exceeds 30 lines ({len(lines)})",
                        fix_suggestion="Keep examples ≤30 lines; move longer examples to examples/ directory",
                    )
                )

        return issues

    def _validate_skill_references(self, content: str) -> list[ValidationIssue]:
        """Validate inter-skill references."""
        issues: list[ValidationIssue] = []

        # Look for skill references in format: skill-name or [skill-name]
        skill_ref_pattern = re.compile(r"\b([a-z]+-[a-z]+-[a-z]+)\b")
        references = skill_ref_pattern.findall(content)

        # Look for explicit "see also" or "related skills" sections
        has_related_section = (
            "see also" in content.lower() or "related skills" in content.lower()
        )

        if references and not has_related_section:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    field="references",
                    message="Consider adding a 'See Also' section for skill references",
                    fix_suggestion="Add skill references to Resources section",
                )
            )

        # Check for [TODO: ...] markers (not allowed per CLAUDE.md)
        todo_pattern = re.compile(r"\[TODO:.*?\]", re.IGNORECASE)
        todos = todo_pattern.findall(content)
        if todos:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="todos",
                    message=f"Found {len(todos)} TODO markers - must be resolved before commit",
                    fix_suggestion="Resolve or remove all [TODO: ...] markers",
                )
            )

        return issues

    def _validate_security(
        self, frontmatter: dict[str, Any], content: str
    ) -> list[ValidationIssue]:
        """Validate security constraints."""
        issues: list[ValidationIssue] = []

        # Check for common secret patterns
        secret_patterns = [
            (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}", "API key"),
            (r"(?i)(secret|password)\s*[:=]\s*['\"]?[^\s\"']{8,}", "Secret/Password"),
            (r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*", "Bearer token"),
            (r"(?i)token\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}", "Token"),
        ]

        for pattern, secret_type in secret_patterns:
            if re.search(pattern, content):
                issues.append(
                    ValidationIssue(
                        severity=ValidationSeverity.ERROR,
                        field="security",
                        message=f"Potential {secret_type} detected in content",
                        fix_suggestion="Remove all secrets and credentials from skill",
                    )
                )

        # Check that security field exists and is meaningful
        security = frontmatter.get("security", "")
        if not security:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    field="security",
                    message="security field is required",
                    fix_suggestion='Add security: "Public; no secrets or PII; safe for open repositories"',
                )
            )

        return issues

    def _calculate_compliance_score(
        self, issues: list[ValidationIssue], tier_compliance: dict[str, bool]
    ) -> float:
        """Calculate overall compliance score (0-1)."""
        # Start with perfect score
        score = 1.0

        # Deduct for errors
        error_count = len([i for i in issues if i.severity == ValidationSeverity.ERROR])
        score -= error_count * 0.15

        # Deduct for warnings
        warning_count = len(
            [i for i in issues if i.severity == ValidationSeverity.WARNING]
        )
        score -= warning_count * 0.05

        # Deduct for info issues
        info_count = len([i for i in issues if i.severity == ValidationSeverity.INFO])
        score -= info_count * 0.02

        # Bonus for tier compliance
        if tier_compliance.get("T1", False):
            score += 0.05
        if tier_compliance.get("T2", False):
            score += 0.05
        if tier_compliance.get("T3", False):
            score += 0.05

        return max(0.0, min(1.0, score))
