# PostgreSQL 12→16 Zero-Downtime Upgrade

## Input
Source: PostgreSQL 12.8, 450GB, 87 tables
Target: PostgreSQL 16.1 on AWS RDS
Constraint: <15 min downtime

## Assessment
- Schema compatible (no breaking changes)
- 342 indexes, 15 optimization opportunities
- Effort: 40 hours

## Plan
Strategy: Blue-green + logical replication
Timeline: 14 days
Tools: pg_dump, logical replication
Rollback: DNS cutback <5 min

## Execute
Week 1: Provision + schema migration
Week 2: Data sync via replication
Day 14: Cutover (12 min downtime)

## Validate
- Rows: 2.1M verified ✓
- Performance: +23%
- Tests: 487/487 passed
