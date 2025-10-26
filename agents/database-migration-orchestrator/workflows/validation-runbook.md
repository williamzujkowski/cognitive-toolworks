# Database Migration Validation Runbook

## Pre-Migration Validation

### 1. Backup Verification
```bash
# Verify backup exists and is restorable
pg_dump source_db > backup.sql
psql test_db < backup.sql
# Confirm row counts match
```

### 2. Replication Setup (if zero-downtime)
```sql
-- Source: Create publication
CREATE PUBLICATION migration_pub FOR ALL TABLES;

-- Target: Create subscription
CREATE SUBSCRIPTION migration_sub
CONNECTION 'host=source dbname=db'
PUBLICATION migration_pub;

-- Monitor lag
SELECT * FROM pg_stat_subscription;
```

## Post-Migration Validation

### 1. Schema Validation
```sql
-- Compare table counts
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema');

-- Compare column definitions
SELECT table_name, column_name, data_type
FROM information_schema.columns
ORDER BY table_name, ordinal_position;
```

### 2. Data Reconciliation

#### Row Count Validation
```sql
-- Source
SELECT schemaname, tablename, n_live_tup
FROM pg_stat_user_tables;

-- Target (compare counts)
SELECT schemaname, tablename, n_live_tup
FROM pg_stat_user_tables;
```

#### Checksum Validation (PostgreSQL)
```sql
-- Create checksums for critical tables
SELECT md5(string_agg(md5(t::text), '' ORDER BY id))
FROM orders t;
```

#### Sample Comparison
```sql
-- Random sample validation (1000 rows)
SELECT * FROM orders
ORDER BY RANDOM() LIMIT 1000;
-- Compare with source
```

### 3. Performance Benchmarking

#### Query Performance Test
```sql
-- Run top 10 queries and measure execution time
EXPLAIN ANALYZE
SELECT ... [critical query];
-- Compare with baseline
```

#### Load Test
```bash
# Using pgbench or equivalent
pgbench -c 10 -j 2 -t 1000 target_db
# Compare TPS with baseline
```

### 4. Application Validation

#### Connection Test
```bash
# Verify application can connect
psql -h target_host -U app_user -d target_db -c "SELECT 1"
```

#### Smoke Tests
- [ ] User authentication works
- [ ] Critical read operations succeed
- [ ] Critical write operations succeed
- [ ] Scheduled jobs execute successfully

### 5. Monitoring Validation
```bash
# Verify metrics collection
curl http://prometheus:9090/api/v1/query?query=pg_up

# Check alerting rules
curl http://alertmanager:9093/api/v1/alerts
```

## Validation Checklist

### Data Integrity
- [ ] Row counts match for all tables (±0.1%)
- [ ] Primary key constraints validated
- [ ] Foreign key relationships intact
- [ ] Checksums match for critical tables
- [ ] Sample comparison shows no discrepancies

### Performance
- [ ] Query latency ≤ baseline (p95)
- [ ] Throughput (QPS) ≥ baseline
- [ ] Resource utilization within limits
- [ ] No connection pool exhaustion

### Functional
- [ ] All application tests pass
- [ ] Scheduled jobs running
- [ ] Integrations functioning
- [ ] No error spikes in logs

### Operational
- [ ] Monitoring dashboards active
- [ ] Alerting rules firing correctly
- [ ] Backup jobs configured
- [ ] Runbooks updated

## Sign-Off Template

**Migration validated by**: [Name]
**Date**: [ISO-8601]
**Validation results**: [Pass/Fail]
**Notes**: [Any observations or concerns]
**Approved for production**: [Yes/No]
