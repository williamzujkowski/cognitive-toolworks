# Changelog - container-security-checker

All notable changes to this skill will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release extracted from security-assessment-framework skill
- CIS Docker and Kubernetes benchmark validation
- Pod Security Standards enforcement checking (Baseline, Restricted)
- Kubernetes RBAC configuration review
- Container image security verification (trusted registries, non-root execution)
- Network policies and admission controller validation
- Support for docker, kubernetes, and both platforms
- Token budget enforcement: T1 ≤2k, T2 ≤6k
- Kubernetes YAML and Dockerfile remediation snippets

### Notes
- Focused single-domain skill following CLAUDE.md ≤2 step principle
- All CIS Benchmark and Kubernetes references updated with 2025-10-26 access dates
