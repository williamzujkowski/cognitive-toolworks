# Changelog - Polyglot Coding Standards Analyzer

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of polyglot coding standards analyzer
- Support for 8 languages: Go, JavaScript, Kotlin, Python, Rust, Shell, Swift, TypeScript
- Universal principle validation (DRY, SOLID, naming conventions, magic numbers)
- Language-specific style guide enforcement
- Automated fix suggestions for mechanical issues
- Quality scoring system (0-100 scale)
- T1 fast path (≤2k tokens) for universal rules
- T2 extended analysis (≤6k tokens) for language-specific rules
- JSON output schema with severity-categorized issues
- Markdown fix suggestions with code snippets
- Language auto-detection via file extensions and syntax patterns
- Rule severity filtering (error/warning/info thresholds)
- Comprehensive language rules mapping (resources/language-rules.json)
- Citations for 6 official style guides with access dates

### Documentation
- Complete SKILL.md with all 8 required sections
- Example usage (≤30 lines) demonstrating Python analysis
- Token budgets clearly specified (T1≤2k, T2≤6k)
- Front-matter with all required keys
- Resource links to official style guides

### Security
- Public repository safe; no secrets or PII
- Static analysis only (no code execution)
- File read sandboxing enforced

### Testing
- 5 evaluation scenarios covering multiple languages and edge cases
- Pass/fail criteria defined for each scenario
