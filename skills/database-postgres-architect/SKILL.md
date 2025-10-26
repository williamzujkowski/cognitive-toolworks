---
name: PostgreSQL Database Architect
slug: database-postgres-architect
description: Design high-performance PostgreSQL databases with schema optimization, indexing strategies, partitioning, replication, and PostgreSQL 17 tuning.
capabilities:
  - Schema design with normalization and denormalization strategies
  - Index strategy (B-tree, GIN, BRIN, GiST, partial, covering indexes)
  - Table partitioning (range, list, hash) for scalability
  - Query performance optimization and EXPLAIN ANALYZE interpretation
  - PostgreSQL 17 vectored I/O and parallelism configuration
  - Replication architecture (streaming, logical replication)
  - High availability with failover and connection pooling
inputs:
  - Application requirements (workload type, scale, latency targets)
  - Data model (entities, relationships, access patterns)
  - Performance constraints (queries per second, data volume, growth rate)
  - Availability requirements (uptime SLA, RPO, RTO)
  - Deployment environment (cloud provider, managed vs self-hosted)
outputs:
  - Optimized schema design with DDL scripts
  - Index recommendations with CREATE INDEX statements
  - Performance tuning configuration (postgresql.conf parameters)
  - Partitioning strategy with partition definitions
  - High availability architecture diagram and setup scripts
keywords:
  - postgresql
  - database architecture
  - schema design
  - indexing
  - partitioning
  - query optimization
  - replication
  - high availability
  - performance tuning
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  - Read-only schema analysis, no data access
  - Configuration review only, no production changes without approval
  - Audit logging of all tuning recommendations
links:
  - https://www.postgresql.org/docs/current/
  - https://www.postgresql.org/docs/current/performance-tips.html
  - https://www.postgresql.org/docs/current/indexes.html
  - https://www.mydbops.com/blog/postgresql-parameter-tuning-best-practices
---

## Purpose & When-To-Use

**Primary trigger conditions:**

- Designing new PostgreSQL database for production application
- Performance issues with existing PostgreSQL deployment (slow queries, high latency)
- Scaling PostgreSQL beyond 100GB or 10k QPS
- High availability requirement (99.9%+ uptime SLA)
- Migration to PostgreSQL from other databases (MySQL, Oracle, SQL Server)
- PostgreSQL version upgrade planning (to PostgreSQL 17)
- Cloud migration (AWS RDS/Aurora, GCP Cloud SQL, Azure Database for PostgreSQL)

**When NOT to use this skill:**

- Database-agnostic schema design → use database-schema-designer
- Query-level optimization only → use database-optimization-analyzer
- Data migration/ETL → use database-migration-generator
- NoSQL databases (MongoDB, Cassandra) → use database-mongodb-architect (future)

**Value proposition:** Optimizes PostgreSQL schema, indexes, and configuration for 2-10x performance improvement. PostgreSQL 17 delivers 2x write throughput in high-concurrency workloads and 20x vacuum memory reduction compared to PostgreSQL 16 (PostgreSQL.org 2025).

## Pre-Checks

**Required inputs validation:**

```python
NOW_ET = "2025-10-26T18:30:00-04:00"

assert workload_type in ["oltp", "olap", "htap", "time-series"], "Valid workload type required"
assert data_volume_estimate is not None, "Data volume estimate required (GB or row count)"
assert queries_per_second_target > 0, "QPS target required"

# Version check
if postgresql_version < 17:
    warn("PostgreSQL 17+ recommended for vectored I/O and improved parallelism")

# Cloud vs self-hosted
if deployment_environment in ["aws-rds", "gcp-cloudsql", "azure-postgres"]:
    note("Managed service constraints apply (limited postgresql.conf access)")
```

**Authority checks:**

- Read access to existing schema (if analyzing existing DB)
- PostgreSQL EXPLAIN permissions for query analysis
- superuser or elevated privileges for configuration recommendations (not required for read-only analysis)

**Source citations (accessed 2025-10-26T18:30:00-04:00):**

- PostgreSQL 17 Performance Improvements: https://www.pgedge.com/blog/postgresql-17-a-major-step-forward-in-performance-logical-replication-and-more
- PostgreSQL Tuning Best Practices 2025: https://www.mydbops.com/blog/postgresql-parameter-tuning-best-practices
- PostgreSQL Indexing Strategies: https://www.freecodecamp.org/news/postgresql-indexing-strategies/
- PostgreSQL Documentation: https://www.postgresql.org/docs/current/

## Procedure

### Tier 1 (≤2k tokens): Quick PostgreSQL Health Check

**Goal:** Identify top 3 performance bottlenecks and provide immediate tuning recommendations in <10 minutes.

**Steps:**

1. **Analyze workload characteristics**
   - OLTP (high concurrency, small transactions) → prioritize indexing, connection pooling
   - OLAP (analytical queries, large scans) → prioritize parallelism, partitioning
   - HTAP (hybrid) → balance both strategies
   - Time-series (append-heavy, time-based queries) → prioritize BRIN indexes, time-based partitioning

2. **Quick schema review**
   - Identify missing indexes on foreign keys (common oversight)
   - Check for tables >1M rows without partitioning
   - Flag SERIAL vs IDENTITY (prefer IDENTITY in PG 10+)
   - Detect overuse of TEXT when VARCHAR(n) or specific types appropriate

3. **Memory configuration quick scan**
   - **shared_buffers:** Should be 25-40% of total RAM (accessed 2025-10-26T18:30:00-04:00)
     - If <25% → recommend increase (reduces disk I/O)
     - If >40% → may cause OS cache duplication, recommend 25-40% range
   - **effective_cache_size:** Should be 50-75% of total RAM
     - Used by query planner to estimate index vs seq scan cost
   - **work_mem:** Should be 4-16MB per connection
     - Too low → disk-based sorts (slow)
     - Too high → memory exhaustion with many connections

4. **Output quick wins** (top 3 highest-impact fixes)
   - Example: "Add B-tree index on users(email) for login queries → 50x speedup"
   - Example: "Increase shared_buffers from 128MB to 8GB (25% of 32GB RAM) → reduce disk reads 60%"
   - Example: "Partition orders table by created_at (monthly) → reduce scan time from 45s to 2s"

**Token budget checkpoint:** ~1.8k tokens for workload analysis, schema scan, config review, quick wins output.

### Tier 2 (≤6k tokens): Comprehensive PostgreSQL Architecture Design

**Goal:** Generate production-ready PostgreSQL architecture with optimized schema, indexes, partitioning, and configuration.

**Extends T1 with:**

5. **Detailed schema design**

   **Normalization strategy:**
   - **3NF (Third Normal Form):** Default for OLTP workloads requiring data consistency
   - **Denormalization:** Strategic for read-heavy workloads (e.g., pre-join user + profile into single table)
   - **Materialized views:** For complex aggregations (refresh strategies: CONCURRENTLY or scheduled)

   **Data type optimization:**
   - Use **SMALLINT** (2 bytes) vs **INTEGER** (4 bytes) vs **BIGINT** (8 bytes) appropriately
   - Prefer **TIMESTAMPTZ** (timezone-aware) over **TIMESTAMP** for UTC storage
   - Use **JSONB** (binary JSON, indexable) over **JSON** (text-based)
   - Leverage **UUID v4** for distributed ID generation or **IDENTITY** for centralized

   **Constraints and validation:**
   - **PRIMARY KEY** with appropriate type (BIGSERIAL for high-volume tables)
   - **FOREIGN KEY** with ON DELETE CASCADE/SET NULL (avoid orphans)
   - **CHECK constraints** for data validation
   - **UNIQUE constraints** with partial indexes for conditional uniqueness

6. **Advanced indexing strategies**

   **Index types and use cases:**

   | Index Type | Use Case | Example |
   |------------|----------|---------|
   | **B-tree** (default) | Equality, range queries | `CREATE INDEX idx_users_email ON users(email);` |
   | **Hash** | Equality only (faster than B-tree for exact match) | `CREATE INDEX idx_sessions_hash ON sessions USING HASH(session_id);` |
   | **GIN** (Generalized Inverted) | Full-text search, JSONB, arrays | `CREATE INDEX idx_posts_fts ON posts USING GIN(to_tsvector('english', content));` |
   | **GiST** (Generalized Search Tree) | Geometric data, full-text, range types | `CREATE INDEX idx_locations_gist ON locations USING GIST(coordinates);` |
   | **BRIN** (Block Range Index) | Large tables with natural ordering (time-series) | `CREATE INDEX idx_logs_brin ON logs USING BRIN(created_at);` |
   | **Partial** | Index subset of rows | `CREATE INDEX idx_active_users ON users(last_login) WHERE active = true;` |
   | **Covering** (INCLUDE) | Include non-key columns | `CREATE INDEX idx_orders_cover ON orders(user_id) INCLUDE (total_amount, status);` |

   **Index maintenance:**
   - **REINDEX** for bloated indexes (track with pg_stat_user_indexes)
   - **CONCURRENTLY** for zero-downtime index creation: `CREATE INDEX CONCURRENTLY idx_name ON table(column);`
   - Monitor index usage with `pg_stat_user_indexes.idx_scan` (drop unused indexes)

7. **Table partitioning for scalability**

   **Partitioning strategies (PostgreSQL 10+ declarative partitioning):**

   **Range partitioning** (most common, time-based):
   ```sql
   CREATE TABLE orders (
     id BIGSERIAL,
     user_id BIGINT,
     created_at TIMESTAMPTZ NOT NULL,
     total_amount NUMERIC(10,2)
   ) PARTITION BY RANGE (created_at);

   CREATE TABLE orders_2025_01 PARTITION OF orders
     FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
   CREATE TABLE orders_2025_02 PARTITION OF orders
     FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
   ```

   **List partitioning** (categorical data):
   ```sql
   CREATE TABLE users PARTITION BY LIST (country_code);
   CREATE TABLE users_us PARTITION OF users FOR VALUES IN ('US');
   CREATE TABLE users_eu PARTITION OF users FOR VALUES IN ('DE', 'FR', 'UK');
   ```

   **Hash partitioning** (distribute evenly when no natural partition key):
   ```sql
   CREATE TABLE sessions PARTITION BY HASH (session_id);
   CREATE TABLE sessions_0 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 0);
   CREATE TABLE sessions_1 PARTITION OF sessions FOR VALUES WITH (MODULUS 4, REMAINDER 1);
   ```

   **Partition pruning (PostgreSQL 17 improvement):**
   - Query planner automatically skips irrelevant partitions
   - Example: `SELECT * FROM orders WHERE created_at >= '2025-10-01'` only scans Oct 2025 partition
   - Monitor with `EXPLAIN ANALYZE` to verify pruning: look for "Partitions pruned: N"

8. **Query optimization and EXPLAIN ANALYZE**

   **Reading EXPLAIN ANALYZE output:**
   ```sql
   EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'user@example.com';
   ```

   **Key metrics:**
   - **Seq Scan** (sequential scan) → full table scan, usually bad for large tables
   - **Index Scan** → good, using index
   - **Index Only Scan** → best, all data from index (covering index)
   - **Bitmap Heap Scan** → combines multiple indexes
   - **Parallel Seq Scan** → multi-core scan (PostgreSQL 9.6+, improved in 17)

   **Common optimization patterns:**
   - Replace `SELECT *` with specific columns (especially with large TEXT/JSONB)
   - Use `LIMIT` to reduce result set size
   - Rewrite subqueries as JOINs or CTEs (Common Table Expressions)
   - Leverage `LATERAL JOIN` for row-dependent subqueries

9. **PostgreSQL 17 specific optimizations**

   **Vectored I/O (accessed 2025-10-26T18:30:00-04:00):**
   - Reduces I/O operations by batching multiple block reads
   - Configure `io_combine_limit` (default: 128kB)
   - **2x write throughput** in high-concurrency workloads

   **Vacuum performance:**
   - **20x memory reduction** in vacuum process
   - Configure `autovacuum_work_mem` (default: -1, inherits maintenance_work_mem)
   - Monitor vacuum with `pg_stat_progress_vacuum`

   **Parallelism improvements:**
   - Expanded parallelism for `FULL OUTER JOIN` and aggregates
   - Configure `max_parallel_workers_per_gather` (default: 2, recommend 4-8 for OLAP)
   - Configure `max_parallel_workers` (total parallel workers across queries)

   **Incremental sort optimization:**
   - Handles larger datasets with minimal memory
   - Automatically used when appropriate (no config needed)

10. **Performance tuning configuration**

    **Memory parameters (postgresql.conf):**
    ```ini
    # For 32GB RAM server (OLTP workload)
    shared_buffers = 8GB           # 25% of RAM
    effective_cache_size = 20GB    # 60% of RAM
    work_mem = 16MB                # per operation (scale down if many connections)
    maintenance_work_mem = 1GB     # for VACUUM, CREATE INDEX
    autovacuum_work_mem = 1GB      # vacuum memory
    ```

    **Connection pooling:**
    - Use **PgBouncer** or **pgpool-II** for connection pooling
    - PostgreSQL connections are heavy (each fork costs ~10MB memory)
    - Recommended: `max_connections = 100` (or lower), pool at application layer

    **Checkpointing:**
    ```ini
    checkpoint_timeout = 15min     # reduce for faster crash recovery
    checkpoint_completion_target = 0.9  # spread writes over 90% of checkpoint interval
    ```

    **Write-Ahead Log (WAL):**
    ```ini
    wal_level = replica            # for streaming replication
    max_wal_size = 4GB             # allow larger WAL before checkpoint
    min_wal_size = 1GB
    ```

11. **High availability architecture**

    **Streaming replication (synchronous vs asynchronous):**
    - **Asynchronous:** Default, minimal performance impact, potential data loss on primary failure
    - **Synchronous:** Zero data loss, higher latency (wait for standby ACK)
    - Configure `synchronous_commit = on` and `synchronous_standby_names`

    **Logical replication (PostgreSQL 10+):**
    - Replicate specific tables/databases (not entire cluster)
    - Supports cross-version replication (e.g., PG 16 → PG 17)
    - Use for multi-region deployments or selective replication

    **Failover strategies:**
    - **Automatic failover:** Use **Patroni** + **etcd/Consul** for distributed consensus
    - **Manual failover:** `pg_ctl promote` on standby
    - **Cloud-managed:** AWS RDS Multi-AZ, GCP Cloud SQL HA, Azure Flexible Server HA

**Authority sources (accessed 2025-10-26T18:30:00-04:00):**

- PostgreSQL 17 Features: https://www.pgedge.com/blog/postgresql-17-a-major-step-forward-in-performance-logical-replication-and-more
- PostgreSQL Performance Tips: https://www.postgresql.org/docs/current/performance-tips.html
- PostgreSQL Tuning 2025: https://dbadataverse.com/tech/postgresql/2025/02/postgresql-configuration-parameters-best-practices-for-performance-tuning
- Index Types: https://www.postgresql.org/docs/current/indexes-types.html

**Output:** Complete PostgreSQL architecture including schema DDL, index definitions, partitioning strategy, postgresql.conf tuning parameters, and HA architecture diagram.

**Token budget checkpoint:** ~5.5k tokens (includes T1 + comprehensive schema design + indexing + partitioning + tuning).

### T3: Enterprise PostgreSQL Architecture (≤12k tokens)

**Goal:** Advanced multi-region, disaster recovery, and large-scale PostgreSQL deployment for >1TB data or >100k QPS.

**Extends T2 with:**

12. **Multi-region architecture**
    - **Cross-region read replicas:** Reduce latency for global users
    - **Geo-partitioning:** Store EU users in EU region (GDPR compliance)
    - **Conflict resolution:** For multi-master setups (Postgres-BDR or Citus)

13. **Sharding strategies**
    - **Citus extension:** Horizontal scaling across multiple PostgreSQL nodes
    - **Application-level sharding:** Partition data by tenant ID or user ID
    - **FDW (Foreign Data Wrappers):** Access remote PostgreSQL databases transparently

14. **Backup and disaster recovery**
    - **pg_basebackup:** Physical backup (binary copy)
    - **pg_dump/pg_restore:** Logical backup (SQL dump)
    - **Point-in-Time Recovery (PITR):** Restore to specific timestamp using WAL archives
    - **RPO/RTO targets:** Design backup frequency and restore testing cadence

15. **Monitoring and observability**
    - **pg_stat_statements:** Track slow queries
    - **pg_stat_activity:** Monitor active connections and queries
    - **pg_stat_bgwriter:** Background writer statistics
    - **Third-party tools:** pgAdmin, Datadog, Prometheus + Grafana

16. **Security hardening**
    - **SSL/TLS:** Encrypt connections (`ssl = on` in postgresql.conf)
    - **pg_hba.conf:** Configure host-based authentication (restrict by IP, require SSL)
    - **Row-level security (RLS):** Fine-grained access control
    - **Encryption at rest:** Use LUKS or cloud-native encryption (AWS RDS encryption, GCP CMEK)

**Authority sources (accessed 2025-10-26T18:30:00-04:00):**

- PostgreSQL Replication: https://www.postgresql.org/docs/current/high-availability.html
- Backup and Recovery: https://www.postgresql.org/docs/current/backup.html
- Security: https://www.postgresql.org/docs/current/runtime-config-connection.html#RUNTIME-CONFIG-CONNECTION-SSL

**Output:** Full enterprise-grade PostgreSQL architecture including multi-region replication, sharding design, backup/DR plan, monitoring dashboard, and security configuration.

**Token budget checkpoint:** ~11k tokens (includes T1 + T2 + enterprise architecture).

## Decision Rules

**When to abort:**

- PostgreSQL version not supported (<9.6 EOL) → recommend upgrade path
- Insufficient input data (no schema, no workload characteristics) → request data model and access patterns
- Contradictory requirements (e.g., "sub-millisecond latency" + "10TB OLAP queries") → clarify priorities

**Ambiguity thresholds:**

- **Index selection:** Only recommend index if >10% query acceleration (avoid index bloat)
- **Partitioning threshold:** Only partition tables >1M rows or >1GB size
- **Replication:** Require explicit availability SLA (99%, 99.9%, 99.99%) to recommend synchronous vs asynchronous

**Prioritization logic:**

1. **Correctness first:** Schema normalization for data integrity (unless denormalization justified)
2. **Quick wins:** Missing indexes on foreign keys (common 10-100x speedup)
3. **Scalability:** Partitioning for large tables before they become unmanageable
4. **High availability:** Replication setup only after performance baseline established

**PostgreSQL principle application:**

- **"Optimize for reads":** 80% of workloads are read-heavy, prioritize indexes and caching
- **"Normalize then denormalize":** Start with 3NF, selectively denormalize based on query patterns
- **"Monitor before tuning":** Use EXPLAIN ANALYZE and pg_stat_statements to identify actual bottlenecks

## Output Contract

**Schema (JSON):**

```json
{
  "schema_design": {
    "tables": [
      {
        "name": "users",
        "columns": [
          {"name": "id", "type": "BIGSERIAL", "constraints": ["PRIMARY KEY"]},
          {"name": "email", "type": "VARCHAR(255)", "constraints": ["NOT NULL", "UNIQUE"]},
          {"name": "created_at", "type": "TIMESTAMPTZ", "default": "NOW()"}
        ],
        "indexes": [
          {"name": "idx_users_email", "type": "B-tree", "columns": ["email"], "unique": true}
        ],
        "partitioning": null
      }
    ],
    "normalization_level": "3NF",
    "estimated_size_gb": 50
  },
  "index_recommendations": [
    {
      "table": "orders",
      "index_name": "idx_orders_user_created",
      "type": "B-tree",
      "columns": ["user_id", "created_at"],
      "rationale": "Covers 80% of queries filtering by user and time range",
      "estimated_speedup": "25x (seq scan 450ms → index scan 18ms)",
      "create_statement": "CREATE INDEX CONCURRENTLY idx_orders_user_created ON orders(user_id, created_at);"
    }
  ],
  "partitioning_strategy": {
    "table": "orders",
    "partition_by": "RANGE",
    "partition_key": "created_at",
    "partition_interval": "monthly",
    "retention_policy": "drop partitions older than 2 years",
    "estimated_query_speedup": "20x (table scan 45s → partition scan 2s)"
  },
  "performance_tuning": {
    "postgresql_conf": {
      "shared_buffers": "8GB",
      "effective_cache_size": "20GB",
      "work_mem": "16MB",
      "maintenance_work_mem": "1GB",
      "max_connections": 100
    },
    "expected_improvement": "60% reduction in disk I/O, 2x query throughput"
  },
  "high_availability": {
    "architecture": "primary + 2 read replicas (async)",
    "failover_strategy": "automatic (Patroni + etcd)",
    "rto": "< 60 seconds",
    "rpo": "< 5 seconds (async replication lag)"
  }
}
```

**Required fields:** schema_design (tables with columns and indexes), performance_tuning (postgresql_conf parameters).

**Optional fields:** partitioning_strategy (only if tables >1M rows), high_availability (only if HA requirement specified).

## Examples

```yaml
# Example: E-commerce platform (OLTP workload)
input:
  workload_type: oltp
  data_volume: "500GB (5M users, 50M orders)"
  queries_per_second: 5000
  availability_sla: 99.95%
  deployment: aws-rds-postgres-17

output:
  schema_design:
    users: 3NF normalized, BIGSERIAL id, VARCHAR email (indexed)
    orders: partitioned by created_at (monthly), indexed on user_id + status
  indexes:
    - users(email) B-tree UNIQUE → login queries 50x faster
    - orders(user_id, created_at) B-tree → user history 25x faster
    - orders(status) partial WHERE status != 'completed' → active orders
  partitioning:
    orders: RANGE by created_at, monthly, 24 partitions (2 years)
  performance_tuning:
    shared_buffers: 16GB (25% of 64GB), work_mem: 8MB, max_connections: 200
  high_availability:
    primary + 2 read replicas (async), Patroni failover, RTO <60s
```

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - quick health check with top 3 optimization recommendations
- **T2**: ≤6,000 tokens - comprehensive architecture with schema, indexes, partitioning, tuning, and HA design
- **T3**: ≤12,000 tokens - enterprise architecture with multi-region, sharding, DR, monitoring, and security hardening

**Accuracy requirements:**

- All DDL statements must be valid PostgreSQL 17 syntax
- Memory configuration calculations verified against server RAM
- Index recommendations validated with EXPLAIN ANALYZE cost estimates

**Safety constraints:**

- **No DROP statements** without explicit approval
- **No ALTER TABLE** on production without maintenance window
- **No synchronous replication** without understanding latency impact

**Auditability:**

- Cite PostgreSQL documentation version for all recommendations
- Include EXPLAIN ANALYZE output for index justification
- Document performance improvement estimates with methodology

**Determinism:**

- Same workload + same data model → same schema design
- Configurable thresholds (index selectivity, partitioning size, memory percentages)

## Resources

**Official PostgreSQL documentation:**

- PostgreSQL 18 Documentation (latest): https://www.postgresql.org/docs/current/
- Performance Tips: https://www.postgresql.org/docs/current/performance-tips.html
- Indexes: https://www.postgresql.org/docs/current/indexes.html
- Partitioning: https://www.postgresql.org/docs/current/ddl-partitioning.html
- High Availability: https://www.postgresql.org/docs/current/high-availability.html

**PostgreSQL 17 features and tuning:**

- PostgreSQL 17 Performance: https://www.pgedge.com/blog/postgresql-17-a-major-step-forward-in-performance-logical-replication-and-more
- Tuning Best Practices 2025: https://www.mydbops.com/blog/postgresql-parameter-tuning-best-practices
- Configuration Guide 2025: https://dbadataverse.com/tech/postgresql/2025/02/postgresql-configuration-parameters-best-practices-for-performance-tuning

**Schema design and indexing:**

- Database Schema Best Practices: https://www.bytebase.com/blog/top-database-schema-design-best-practices/
- Advanced Indexing Strategies: https://www.freecodecamp.org/news/postgresql-indexing-strategies/
- Index Best Practices: https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide

**Tools and extensions:**

- pgAdmin: https://www.pgadmin.org/
- PgBouncer (connection pooling): https://www.pgbouncer.org/
- Patroni (HA): https://patroni.readthedocs.io/
- Citus (sharding): https://www.citusdata.com/

**Related skills:**

- `database-schema-designer`: Database-agnostic schema design
- `database-optimization-analyzer`: Query-level performance tuning
- `database-migration-generator`: Data migration and ETL
- `cloud-aws-architect`: AWS RDS/Aurora PostgreSQL deployment
- `cloud-gcp-architect`: GCP Cloud SQL PostgreSQL deployment
- `cloud-azure-architect`: Azure Database for PostgreSQL deployment
