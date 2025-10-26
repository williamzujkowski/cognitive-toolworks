# Changelog - Testing Strategy Composer

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-25

### Added
- Initial release of Testing Strategy Composer skill
- T1 tier: Fast path for test distribution recommendations (≤2k tokens)
- T2 tier: Extended analysis with scaffolding and execution plans (≤6k tokens)
- Support for unit, integration, E2E, and performance test strategies
- Framework-specific scaffolding templates (Jest, pytest, JUnit, etc.)
- Coverage gap identification with risk prioritization
- Phased execution plan generation with effort estimates
- Test pyramid heuristics based on architecture patterns (monolith, microservices, API-only, mobile)
- Decision rules for test distribution adjustments
- Example workflow for e-commerce REST API
- Test pyramid Markdown template resource
- 5 evaluation scenarios (microservices, monolith, API-only, mobile, ML pipeline)
- Citations from Google Testing Blog, Martin Fowler, Microsoft Patterns, ISTQB Foundation

### Sources Cited (accessed 2025-10-25T21:30:36-04:00)
- https://testing.googleblog.com/
- https://martinfowler.com/testing/
- https://martinfowler.com/articles/practical-test-pyramid.html
- https://learn.microsoft.com/en-us/dotnet/core/testing/
- https://www.istqb.org/certifications/certified-tester-foundation-level

### Security
- No PII or secrets included
- Test templates use placeholder data only
- Sandboxed execution recommended for generated test scaffolding

---

## [Unreleased]

### Planned
- T3 tier for deep-dive test effectiveness analysis (mutation testing)
- Performance test benchmarking templates
- Flaky test detection heuristics
- Contract testing guidance for microservices
- Visual regression testing strategies for UI-heavy systems

---

**Maintained by**: william@cognitive-toolworks
**License**: MIT
