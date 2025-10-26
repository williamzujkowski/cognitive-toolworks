# Changelog

All notable changes to the data-engineering-pipeline-designer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of data-engineering-pipeline-designer skill
- T1 tier: Quick pipeline design for standard batch patterns
- T2 tier: Production-ready pipelines with quality gates and monitoring
- Support for batch, streaming, and hybrid pipeline architectures
- Airflow DAG orchestration patterns and best practices
- dbt transformation layer design with layered modeling
- Great Expectations data quality check configuration
- Kafka streaming architecture guidance
- Pipeline monitoring and SLA configuration
- Data lineage and governance controls
- Examples for e-commerce batch ELT pipeline
- Resource templates: Airflow DAG, dbt project, Great Expectations suite
- Comprehensive decision rules for batch vs streaming, incremental vs full refresh
- Integration with database-optimization-analyzer skill

### Documentation
- Complete SKILL.md with all required sections per CLAUDE.md §3
- Token budgets enforced: T1 ≤2k, T2 ≤6k tokens
- Authoritative sources cited with access dates (2025-10-25T21:30:36-04:00):
  - Apache Airflow official docs
  - dbt transformation best practices
  - Great Expectations data quality framework
  - Apache Kafka streaming architecture
- Examples limited to ≤30 lines per CLAUDE.md requirements

### Notes
- T3 tier deferred to v2.0.0 (PB-scale optimization, multi-region patterns)
- Dependencies: database-optimization-analyzer (leverages for warehouse tuning)
- Phase 2, Priority P2 per analyst-implementation-plan.json
