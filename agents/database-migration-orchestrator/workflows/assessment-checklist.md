# Database Migration Assessment Checklist

## Source Database Analysis

### Schema Inventory
- [ ] Table count and schemas identified
- [ ] Column types and constraints documented
- [ ] Index strategy analyzed (primary, unique, composite)
- [ ] Foreign key relationships mapped
- [ ] Stored procedures/functions cataloged
- [ ] Triggers and views documented
- [ ] Partitioning strategy noted (if any)

### Data Profile
- [ ] Total data volume (GB) measured
- [ ] Row count per table captured
- [ ] Growth rate calculated (GB/month)
- [ ] Data distribution analyzed (hot vs cold data)
- [ ] Large objects identified (BLOB, TEXT >1MB)

### Query Analysis
- [ ] Slow query log reviewed
- [ ] Top 20 queries by frequency identified
- [ ] Query patterns categorized (OLTP vs OLAP)
- [ ] Application query dependencies mapped

### Performance Baseline
- [ ] Avg query latency (p50, p95, p99) captured
- [ ] Throughput (QPS) measured
- [ ] Connection pool metrics recorded
- [ ] Resource utilization (CPU, RAM, IOPS) noted

## Target Database Compatibility

### Feature Parity
- [ ] Data type mappings verified
- [ ] SQL dialect differences identified
- [ ] Stored procedure migration feasibility assessed
- [ ] Extension/plugin compatibility checked

### Breaking Changes
- [ ] Version-specific deprecations noted
- [ ] Syntax changes documented
- [ ] Configuration parameter changes identified

## Migration Complexity Assessment

### Risk Rating
- [ ] Schema complexity: Low / Medium / High
- [ ] Data volume risk: Low / Medium / High
- [ ] Application coupling: Low / Medium / High
- [ ] Business criticality: Low / Medium / High

### Effort Estimate
- Schema migration: ___ hours
- Data migration tooling: ___ hours
- Application changes: ___ hours
- Testing and validation: ___ hours
- **Total**: ___ hours
