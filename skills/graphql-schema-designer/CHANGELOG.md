# Changelog - GraphQL Schema Designer

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of GraphQL Schema Designer skill
- Support for standalone, federated, and stitched schema types
- Apollo Federation v2 configuration with @key, @shareable, @external directives
- DataLoader patterns for n+1 query prevention
- Cursor-based and offset pagination implementations
- GraphQL subscription design patterns
- Custom scalar type definitions
- Authorization directive patterns
- Query complexity analysis and depth limiting
- Schema stitching guidance for legacy integration
- T1 (≤2k), T2 (≤6k), T3 (≤12k) tiered implementation
- Comprehensive examples and evals (5 scenarios)
- Source citations from GraphQL spec, Apollo Federation, DataLoader

### Token Budgets
- T1: Basic schema design (≤2k tokens)
- T2: Production optimization with federation (≤6k tokens)
- T3: Advanced patterns with subscriptions (≤12k tokens)

### Quality Gates
- SDL syntax validation
- Federation directive compliance
- DataLoader configuration for relationship fields
- Query complexity and depth limiting
- Security directive coverage
