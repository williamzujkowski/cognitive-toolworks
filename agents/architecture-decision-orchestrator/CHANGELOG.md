# Changelog - Architecture Decision Orchestrator

All notable changes to this agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of Architecture Decision Orchestrator agent
- 4-step workflow: Discovery → Analysis → Synthesis → Documentation
- Integration with architecture-decision-framework skill
- Support for Nygard, MADR, and Y-statement ADR formats
- C4 diagram generation (Context, Container, Component levels)
- ATAM trade-off analysis for complex decisions
- Pattern evaluation for Layered, Hexagonal, Event-Driven, CQRS architectures
- Progressive disclosure with T1/T2/T3 tiers
- Migration strategy recommendations (greenfield, strangler, big-bang, phased)
- Quality gates with syntax validation for PlantUML/Mermaid diagrams
- Comprehensive examples for microservices and monolith scenarios

### Technical Details
- System prompt: 1487 tokens (under 1500 token limit)
- 8 required sections per CLAUDE.md standards
- NOW_ET timestamp normalization (NIST time.gov semantics)
- All sources cited with access dates
- No secrets, PII, or fabricated benchmarks
