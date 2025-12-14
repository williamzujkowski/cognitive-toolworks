"""
Security pattern detection for skills.

Detects potential security issues including:
- Unrestricted file system access
- Network calls without allowlisting
- Shell command injection vectors
- Sensitive data exposure patterns
- Tool permission escalation
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from pathlib import Path


class Severity(str, Enum):
    """Security issue severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueType(str, Enum):
    """Types of security issues."""

    FILE_SYSTEM = "file_system"
    NETWORK = "network"
    SHELL_INJECTION = "shell_injection"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    PERMISSION_ESCALATION = "permission_escalation"
    UNSAFE_PATTERN = "unsafe_pattern"


@dataclass
class SecurityIssue:
    """A detected security issue."""

    severity: Severity
    issue_type: IssueType
    description: str
    line_number: int | None = None
    line_content: str | None = None
    recommendation: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "severity": self.severity.value,
            "type": self.issue_type.value,
            "description": self.description,
            "line": self.line_number,
            "content": self.line_content,
            "recommendation": self.recommendation,
        }


@dataclass
class SecurityReport:
    """Security scan report."""

    issues: list[SecurityIssue] = field(default_factory=list)
    score: float = 1.0  # 0-1, higher is better
    summary: str = ""

    @property
    def passed(self) -> bool:
        """Check if security scan passed (no high/critical issues)."""
        return not any(
            issue.severity in (Severity.CRITICAL, Severity.HIGH)
            for issue in self.issues
        )

    @property
    def critical_count(self) -> int:
        """Count of critical issues."""
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        """Count of high severity issues."""
        return sum(1 for i in self.issues if i.severity == Severity.HIGH)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "issues": [i.to_dict() for i in self.issues],
            "score": self.score,
            "summary": self.summary,
            "passed": self.passed,
            "counts": {
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": sum(1 for i in self.issues if i.severity == Severity.MEDIUM),
                "low": sum(1 for i in self.issues if i.severity == Severity.LOW),
            },
        }


class SecurityAnalyzer:
    """
    Analyzes skills for security vulnerabilities.

    Scans for dangerous patterns that could lead to:
    - Data exfiltration
    - System compromise
    - Credential theft
    - Unauthorized access
    """

    # Patterns for file system access
    FILE_PATTERNS: ClassVar[list[tuple[str, Severity, str]]] = [
        (r"/etc/passwd", Severity.HIGH, "Access to system password file"),
        (r"/etc/shadow", Severity.CRITICAL, "Access to shadow password file"),
        (r"~/.ssh/", Severity.CRITICAL, "Access to SSH keys"),
        (r"~/.aws/", Severity.CRITICAL, "Access to AWS credentials"),
        (r"/root/", Severity.HIGH, "Access to root home directory"),
        (r"rm\s+-rf\s+/", Severity.CRITICAL, "Recursive deletion from root"),
        (r"chmod\s+777", Severity.HIGH, "World-writable permissions"),
        (r"\.\./\.\./\.\./", Severity.HIGH, "Path traversal attempt"),
    ]

    # Patterns for network access
    NETWORK_PATTERNS: ClassVar[list[tuple[str, Severity, str]]] = [
        (r"curl\s+[^|]+\|\s*sh", Severity.CRITICAL, "Piping curl to shell"),
        (r"wget\s+[^|]+\|\s*sh", Severity.CRITICAL, "Piping wget to shell"),
        (r"curl\s+-o\s+/tmp/", Severity.MEDIUM, "Downloading to tmp directory"),
        (r"requests\.get\([^)]*\)", Severity.LOW, "HTTP request (verify allowlist)"),
        (r"fetch\([^)]*\)", Severity.LOW, "Fetch request (verify allowlist)"),
    ]

    # Patterns for shell injection
    SHELL_PATTERNS: ClassVar[list[tuple[str, Severity, str]]] = [
        (r"\$\{[^}]*\}", Severity.MEDIUM, "Shell variable expansion"),
        (r"\$\([^)]*\)", Severity.MEDIUM, "Command substitution"),
        (r"`[^`]*`", Severity.MEDIUM, "Backtick command substitution"),
        (r"eval\s+", Severity.HIGH, "Eval usage"),
        (r"exec\s+", Severity.HIGH, "Exec usage"),
        (r"\|\s*bash", Severity.HIGH, "Piping to bash"),
        (r"\|\s*sh\b", Severity.HIGH, "Piping to sh"),
    ]

    # Patterns for credential exposure
    CREDENTIAL_PATTERNS: ClassVar[list[tuple[str, Severity, str]]] = [
        (
            r'api[_-]?key\s*[=:]\s*["\'][^"\']+["\']',
            Severity.CRITICAL,
            "Hardcoded API key",
        ),
        (
            r'password\s*[=:]\s*["\'][^"\']+["\']',
            Severity.CRITICAL,
            "Hardcoded password",
        ),
        (r'secret\s*[=:]\s*["\'][^"\']+["\']', Severity.CRITICAL, "Hardcoded secret"),
        (r'token\s*[=:]\s*["\'][^"\']+["\']', Severity.HIGH, "Hardcoded token"),
        (r"ANTHROPIC_API_KEY\s*=", Severity.MEDIUM, "API key in code (use env var)"),
        (r"sk-[a-zA-Z0-9]{48}", Severity.CRITICAL, "OpenAI API key pattern"),
        (r"sk-ant-[a-zA-Z0-9-]+", Severity.CRITICAL, "Anthropic API key pattern"),
    ]

    # Unsafe patterns
    UNSAFE_PATTERNS: ClassVar[list[tuple[str, Severity, str]]] = [
        (r"sudo\s+", Severity.HIGH, "Sudo usage"),
        (r"--no-verify", Severity.MEDIUM, "Skipping verification"),
        (r"--insecure", Severity.HIGH, "Insecure flag"),
        (r"-k\s+", Severity.MEDIUM, "Skipping SSL verification"),
        (r"allowAllHosts", Severity.HIGH, "Allowing all hosts"),
        (r"\*\.\*", Severity.MEDIUM, "Wildcard pattern"),
    ]

    def __init__(self) -> None:
        self._compiled_patterns: list[tuple[re.Pattern, Severity, str, IssueType]] = []
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Pre-compile regex patterns for performance."""
        pattern_groups = [
            (self.FILE_PATTERNS, IssueType.FILE_SYSTEM),
            (self.NETWORK_PATTERNS, IssueType.NETWORK),
            (self.SHELL_PATTERNS, IssueType.SHELL_INJECTION),
            (self.CREDENTIAL_PATTERNS, IssueType.CREDENTIAL_EXPOSURE),
            (self.UNSAFE_PATTERNS, IssueType.UNSAFE_PATTERN),
        ]

        for patterns, issue_type in pattern_groups:
            for pattern, severity, description in patterns:
                compiled = re.compile(pattern, re.IGNORECASE)
                self._compiled_patterns.append(
                    (compiled, severity, description, issue_type)
                )

    def analyze(self, content: str) -> SecurityReport:
        """
        Analyze content for security issues.

        Args:
            content: The skill content to analyze.

        Returns:
            SecurityReport with detected issues and score.
        """
        issues: list[SecurityIssue] = []
        lines = content.split("\n")

        # Check each line against all patterns
        for line_num, line in enumerate(lines, 1):
            for pattern, severity, description, issue_type in self._compiled_patterns:
                if pattern.search(line):
                    issues.append(
                        SecurityIssue(
                            severity=severity,
                            issue_type=issue_type,
                            description=description,
                            line_number=line_num,
                            line_content=line.strip()[:100],
                            recommendation=self._get_recommendation(issue_type),
                        )
                    )

        # Additional semantic checks
        issues.extend(self._check_tool_permissions(content))
        issues.extend(self._check_allowed_tools(content))

        # Calculate score
        score = self._calculate_score(issues)

        # Generate summary
        summary = self._generate_summary(issues)

        return SecurityReport(issues=issues, score=score, summary=summary)

    def analyze_file(self, path: Path) -> SecurityReport:
        """Analyze a file for security issues."""
        content = path.read_text()
        return self.analyze(content)

    def analyze_directory(
        self, path: Path, recursive: bool = False
    ) -> dict[str, SecurityReport]:
        """Analyze all skills in a directory."""
        reports: dict[str, SecurityReport] = {}

        pattern = "**/*.md" if recursive else "*.md"
        for md_file in path.glob(pattern):
            reports[str(md_file)] = self.analyze_file(md_file)

        return reports

    def _check_tool_permissions(self, content: str) -> list[SecurityIssue]:
        """Check for overly permissive tool access."""
        issues: list[SecurityIssue] = []

        # Check for dangerous tool combinations
        dangerous_tools = ["Bash", "Write", "Edit"]
        has_dangerous = sum(
            1 for tool in dangerous_tools if tool.lower() in content.lower()
        )

        if has_dangerous >= 3 and "allowed-tools" not in content.lower():
            issues.append(
                SecurityIssue(
                    severity=Severity.MEDIUM,
                    issue_type=IssueType.PERMISSION_ESCALATION,
                    description="Multiple powerful tools without explicit allowed-tools restriction",
                    recommendation="Add 'allowed-tools' frontmatter to restrict tool access",
                )
            )

        return issues

    def _check_allowed_tools(self, content: str) -> list[SecurityIssue]:
        """Check allowed-tools configuration."""
        issues: list[SecurityIssue] = []

        # Look for allowed-tools in frontmatter
        if "allowed-tools:" in content.lower():
            # Check for overly permissive patterns
            if "*" in content and "allowed-tools" in content.lower():
                issues.append(
                    SecurityIssue(
                        severity=Severity.HIGH,
                        issue_type=IssueType.PERMISSION_ESCALATION,
                        description="Wildcard in allowed-tools grants excessive permissions",
                        recommendation="Explicitly list required tools instead of using wildcards",
                    )
                )

        return issues

    def _get_recommendation(self, issue_type: IssueType) -> str:
        """Get recommendation for issue type."""
        recommendations = {
            IssueType.FILE_SYSTEM: "Restrict file access to specific paths using allowlists",
            IssueType.NETWORK: "Use domain allowlists for network access",
            IssueType.SHELL_INJECTION: "Avoid dynamic command construction; use parameterized calls",
            IssueType.CREDENTIAL_EXPOSURE: "Use environment variables for credentials",
            IssueType.PERMISSION_ESCALATION: "Apply principle of least privilege",
            IssueType.UNSAFE_PATTERN: "Remove unsafe flags and verify security implications",
        }
        return recommendations.get(
            issue_type, "Review and address the security concern"
        )

    def _calculate_score(self, issues: list[SecurityIssue]) -> float:
        """Calculate security score (0-1, higher is better)."""
        if not issues:
            return 1.0

        # Weight by severity
        weights = {
            Severity.CRITICAL: 0.3,
            Severity.HIGH: 0.2,
            Severity.MEDIUM: 0.1,
            Severity.LOW: 0.05,
            Severity.INFO: 0.01,
        }

        total_penalty = sum(weights.get(issue.severity, 0) for issue in issues)
        return max(0.0, 1.0 - total_penalty)

    def _generate_summary(self, issues: list[SecurityIssue]) -> str:
        """Generate human-readable summary."""
        if not issues:
            return "No security issues detected."

        critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        high = sum(1 for i in issues if i.severity == Severity.HIGH)
        medium = sum(1 for i in issues if i.severity == Severity.MEDIUM)
        low = sum(1 for i in issues if i.severity == Severity.LOW)

        parts = []
        if critical:
            parts.append(f"{critical} critical")
        if high:
            parts.append(f"{high} high")
        if medium:
            parts.append(f"{medium} medium")
        if low:
            parts.append(f"{low} low")

        return f"Found {len(issues)} issues: " + ", ".join(parts)
