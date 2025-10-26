# Changelog

All notable changes to the Database Migration Script Generator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of Database Migration Script Generator skill
- Support for Liquibase (XML/YAML), Flyway (SQL), and Alembic (Python) migration tools
- Support for PostgreSQL, MySQL, SQL Server, and Oracle databases
- T1 tier: Basic schema migrations (add/drop columns, tables, indexes)
- T2 tier: Data migrations with backfill, transformation logic, and database-specific optimizations
- T3 tier: Zero-downtime patterns (expand/contract, online DDL, shadow tables)
- Rollback script generation with safety validation
- Migration validation tests and deployment guides
- Comprehensive examples for all migration patterns
- 5 evaluation scenarios covering common migration use cases
