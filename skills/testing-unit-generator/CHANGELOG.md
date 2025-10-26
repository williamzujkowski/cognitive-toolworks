# Changelog - Unit Testing Generator

## [1.0.0] - 2025-10-26

### Added
- Initial skill creation following CLAUDE.md standards
- Support for 5 testing frameworks: Jest, PyTest, Go testing, JUnit, RSpec
- Three-tier progressive disclosure (T1: scaffolding, T2: mocks+coverage, T3: advanced patterns)
- Token budgets: T1≤2k, T2≤6k, T3≤12k
- Example PyTest file with mocking (≤30 lines)
- 5 evaluation scenarios covering all supported frameworks
- Official documentation sources with access timestamps (2025-10-26T02:31:24Z)
- Output contract with test files, config, and coverage setup
- Decision rules for framework detection and abort conditions
- Quality gates for safety, auditability, and determinism

### Documentation
- SKILL.md with all required sections per CLAUDE.md §3
- pytest-example.py demonstrating mocking patterns
- evals_unit-testing-generator.yaml with T1/T2/T3 test cases
- Citations for Jest, PyTest, Go, JUnit, RSpec official docs
