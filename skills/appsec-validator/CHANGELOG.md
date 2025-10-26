# Changelog - appsec-validator

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release extracted from security-assessment-framework skill
- OWASP Top 10 2021 compliance checking (A01-A10)
- OWASP API Security Top 10 2023 validation (API1-API10)
- SQL injection and XSS prevention verification
- Authentication and authorization review capabilities
- Three-tier check levels: critical-only, standard, comprehensive
- Token budget enforcement: T1 ≤2k, T2 ≤6k, T3 ≤12k
- CVSS v3.1 scoring for findings
- Support for web-app, api, and mobile-backend scopes

### Notes
- Focused single-domain skill following CLAUDE.md ≤2 step principle
- All OWASP references updated with 2025-10-26 access dates
