# Changelog - Database Optimization Analyzer

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of database-optimization-analyzer skill
- T1 tier: Fast path for common query anti-patterns (≤2k tokens)
- T2 tier: Extended analysis with execution plan parsing (≤6k tokens)
- T3 tier: Deep dive with workload analysis and migration guidance (≤12k tokens)
- Support for PostgreSQL, MySQL, MongoDB, and Redis
- Query execution plan analysis (EXPLAIN/EXPLAIN ANALYZE)
- Index recommendation engine with composite index optimization
- N+1 query detection
- Schema design review capabilities
- Database-specific optimization strategies
- Query rewrite suggestions
- Denormalization recommendations for NoSQL
- Comprehensive output contract with JSON schema
- Example optimization scenario (PostgreSQL slow query)
- Resources directory with query templates and index strategies
- 5 evaluation scenarios covering SQL, NoSQL, and edge cases

### Documentation
- Complete SKILL.md following CLAUDE.md §3 format
- Token budgets documented for all three tiers
- 6 authoritative sources cited with access dates
- Decision rules for index creation, denormalization, and database selection
- Quality gates for safety, auditability, and determinism

### Sources Referenced
- PostgreSQL Official Docs (accessed 2025-10-25T22:10:45-04:00)
- MySQL Official Docs (accessed 2025-10-25T22:10:45-04:00)
- MongoDB Official Docs (accessed 2025-10-25T22:10:45-04:00)
- Redis Official Docs (accessed 2025-10-25T22:10:45-04:00)
- use-the-index-luke.com (accessed 2025-10-25T22:10:45-04:00)
