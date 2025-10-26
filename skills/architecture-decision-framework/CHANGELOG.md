# Changelog - Architecture Decision Framework

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial skill implementation for architecture decision framework
- Support for four core architectural patterns: Layered, Hexagonal, Event-Driven, CQRS
- Three ADR formats: Nygard, MADR, Y-statements
- ATAM (Architecture Tradeoff Analysis Method) integration
- C4 model diagram generation (Context, Container, Component, Code levels)
- Three-tier procedure (T1 ≤2k, T2 ≤6k, T3 ≤12k tokens)
- Pattern evaluation matrix with quality attributes scoring
- Trade-off analysis with sensitivity and tradeoff points
- Migration strategy recommendations (greenfield, strangler, big-bang, phased)
- Authoritative source citations (ADR.github.io, Martin Fowler, C4model.com, SEI/CMU)
- Example ADR in Y-statement format for microservices migration
- Resource links with access dates (2025-10-25T21:30:36-04:00)

### Documentation
- Pre-checks for input validation and source freshness
- Decision rules for pattern selection thresholds
- Output contract with JSON schema
- Quality gates for token budgets and validation
- Examples for T2 tier microservices API gateway decision
