# Changelog

All notable changes to the Microservices Pattern Architect skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of Microservices Pattern Architect skill
- T1 tier: Pattern recommendation with quick template links (≤2k tokens)
- T2 tier: Extended implementation guidance with monitoring strategy (≤6k tokens)
- Support for 6 core microservices patterns:
  - Saga (choreography and orchestration variants)
  - CQRS (Command Query Responsibility Segregation)
  - Event Sourcing with event store design
  - Circuit Breaker for fault tolerance
  - API Gateway with BFF (Backend for Frontend) variant
  - Service Discovery (client-side and server-side)
- Pattern composition recommendations for complex scenarios
- Anti-pattern detection and remediation guidance
- Framework-specific templates for Spring Boot, Node.js, .NET, Go, Python
- Event schema design with versioning strategies
- Observability and monitoring strategy per pattern
- Integration guidance with cloud-native-deployment-orchestrator
- Decision tree for pattern selection based on scenario
- Comprehensive resource templates in resources/ folder
- Example implementations and code scaffolding

### Research Sources
- Microservices.io Patterns (Chris Richardson, accessed 2025-10-25)
- Martin Fowler Microservices Guide (accessed 2025-10-25)
- Microsoft Azure Architecture Patterns (updated September 2025, accessed 2025-10-25)
- Pattern-specific references for Saga, CQRS, Event Sourcing, Circuit Breaker, API Gateway, Service Discovery

### Dependencies
- Requires: cloud-native-deployment-orchestrator (for deployment integration)
- Optional integration: architecture-decision-framework (for ADR generation)

### Quality Gates
- Token budgets enforced: T1 ≤2k, T2 ≤6k
- All sources cited with access dates (NOW_ET: 2025-10-25T21:30:36-04:00)
- No secrets or PII in templates
- Example ≤30 lines (microservices-example.txt)
- 5 evaluation scenarios in tests/evals_microservices-pattern-architect.yaml
