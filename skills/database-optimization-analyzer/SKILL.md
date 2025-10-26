---
name: Database Optimization Analyzer
slug: database-optimization-analyzer
description: Optimize SQL and NoSQL databases with schema design, query performance tuning, and indexing strategies.
capabilities:
  - Analyze query execution plans (EXPLAIN/EXPLAIN ANALYZE)
  - Recommend indexes for SQL and NoSQL databases
  - Identify N+1 queries and query anti-patterns
  - Suggest denormalization strategies for NoSQL
  - Optimize schema design for performance
  - Detect missing indexes and unused indexes
  - Analyze database-specific optimization opportunities
inputs:
  - query: SQL or NoSQL query text
  - database_type: postgresql, mysql, mongodb, redis, or other
  - execution_plan: optional EXPLAIN output
  - schema: optional table/collection schema definition
  - performance_metrics: optional query execution time, rows scanned
outputs:
  - optimization_recommendations: array of actionable improvements
  - index_suggestions: specific index definitions
  - query_rewrites: optimized query alternatives
  - estimated_impact: performance improvement estimates
  - implementation_priority: high/medium/low
keywords:
  - database
  - performance
  - optimization
  - indexing
  - query-tuning
  - SQL
  - NoSQL
  - PostgreSQL
  - MySQL
  - MongoDB
  - Redis
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: No credentials required; analyzes query patterns only
links:
  - https://www.postgresql.org/docs/current/performance-tips.html
  - https://dev.mysql.com/doc/refman/8.0/en/optimization.html
  - https://www.mongodb.com/docs/manual/core/query-optimization/
  - https://redis.io/docs/latest/develop/use/patterns/
  - https://use-the-index-luke.com/
---

## Purpose & When-To-Use

Use this skill when:
- Slow query identified (execution time >100ms for OLTP, >5s for OLAP)
- Database performance degradation observed
- Schema design review needed before production deployment
- Query optimization required for scalability
- Index strategy needs validation
- Database migration planning (SQL to NoSQL or vice versa)
- Performance regression analysis after schema changes

Do not use for:
- Database administration tasks (backup, replication, failover)
- Database installation or configuration
- Security hardening (use security-assessment-framework)
- Data modeling or ER diagram generation

## Pre-Checks

1. **Time Normalization**: `NOW_ET = 2025-10-25T22:10:45-04:00` (NIST/time.gov semantics)
2. **Input Validation**:
   - Database type must be one of: postgresql, mysql, mongodb, redis, or specify 'other'
   - Query text must be non-empty string
   - If execution_plan provided, must match database type format
3. **Source Freshness**:
   - PostgreSQL docs accessed: 2025-10-25T22:10:45-04:00
   - MySQL docs accessed: 2025-10-25T22:10:45-04:00
   - MongoDB docs accessed: 2025-10-25T22:10:45-04:00
   - Redis docs accessed: 2025-10-25T22:10:45-04:00
   - use-the-index-luke.com accessed: 2025-10-25T22:10:45-04:00

## Procedure

### T1: Fast Path (≤2k tokens, 80% common cases)

**Scope**: Quick wins for common query anti-patterns without deep execution plan analysis.

**Steps**:
1. **Detect Database Type**: Parse query syntax or use provided database_type
2. **Quick Pattern Scan**:
   - SELECT * usage (recommend explicit columns)
   - Missing WHERE clause on large tables
   - LIKE with leading wildcard (%pattern)
   - Functions on indexed columns (e.g., WHERE YEAR(date_col) = 2025)
   - Cartesian joins (missing JOIN conditions)
   - Subqueries that could be JOINs
3. **Index Hints** (generic):
   - Columns in WHERE, JOIN ON, ORDER BY, GROUP BY clauses
   - Composite index recommendations based on query predicates
4. **Output**: 3-5 actionable quick wins with implementation code

**Abort Conditions**:
- Query syntax invalid for specified database type
- Performance metrics contradict issue (query already fast)

### T2: Extended Analysis (≤6k tokens, deep optimization)

**Scope**: Detailed execution plan analysis, schema review, and database-specific optimizations.

**Steps**:
1. **Execution Plan Analysis** (if provided):
   - **PostgreSQL**: Parse EXPLAIN ANALYZE output
     - Identify Seq Scan on large tables → recommend index
     - Nested Loop with high row estimates → consider Hash Join
     - Sort operations → evaluate index for ORDER BY
     - High cost nodes → focus optimization effort
   - **MySQL**: Parse EXPLAIN output
     - type=ALL (full table scan) → add index
     - Extra='Using filesort' → index for ORDER BY
     - Extra='Using temporary' → optimize GROUP BY
     - rows examined vs rows returned ratio
   - **MongoDB**: Parse explain() output
     - COLLSCAN (collection scan) → create index
     - IXSCAN with high nReturned/totalKeysExamined → index selectivity issue
     - SORT stage → compound index with sort fields
   - **Redis**: Analyze command patterns
     - KEYS command → use SCAN for large keyspaces
     - Large SET/LIST operations → consider pipelining
     - Missing TTL on ephemeral data

2. **Schema Design Review**:
   - **Normalization Issues**:
     - Over-normalization causing excessive JOINs → selective denormalization
     - Under-normalization causing data redundancy → normalize
   - **Data Types**:
     - Oversized VARCHAR → right-size
     - Using TEXT for short strings → use VARCHAR
     - Numeric precision mismatches
   - **Partitioning Opportunities**:
     - Tables >10M rows → consider partitioning by date/range
     - Time-series data → partition by month/quarter

3. **Database-Specific Optimizations**:
   - **PostgreSQL**:
     - Partial indexes for filtered queries
     - GIN/GiST indexes for full-text search, JSON
     - Covering indexes to avoid table lookups
     - Materialized views for complex aggregations
     - (Source: https://www.postgresql.org/docs/current/indexes-types.html, accessed 2025-10-25T22:10:45-04:00)
   - **MySQL**:
     - InnoDB buffer pool sizing
     - Query cache considerations (deprecated in 8.0)
     - Index merge optimization
     - (Source: https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html, accessed 2025-10-25T22:10:45-04:00)
   - **MongoDB**:
     - ESR rule (Equality, Sort, Range) for compound indexes
     - Index intersection vs compound index trade-offs
     - Aggregation pipeline optimization ($match early, $project to reduce data)
     - (Source: https://www.mongodb.com/docs/manual/core/index-compound/, accessed 2025-10-25T22:10:45-04:00)
   - **Redis**:
     - Hash vs String for structured data
     - Sorted Sets for ranking/leaderboards
     - Pub/Sub vs Streams for messaging
     - (Source: https://redis.io/docs/latest/develop/data-types/, accessed 2025-10-25T22:10:45-04:00)

4. **N+1 Query Detection**:
   - Identify repeated queries with different parameters in application logs
   - Recommend batch loading (IN clause, JOIN, or eager loading)

5. **Output**: Detailed optimization report with:
   - Prioritized recommendations (high/medium/low impact)
   - Specific DDL statements for indexes
   - Query rewrites with before/after comparison
   - Estimated performance improvement (based on row reduction, index usage)

**Decision Rules**:
- If execution plan shows >80% time in Seq Scan → HIGH priority index recommendation
- If query returns <10% of scanned rows → index selectivity issue or missing predicate
- If schema has >5 levels of normalization → evaluate denormalization candidates
- If MongoDB query scans >10k documents to return <100 → create compound index

### T3: Deep Dive (≤12k tokens, comprehensive analysis)

**Scope**: Multi-query optimization, workload analysis, and migration recommendations.

**Steps**:
1. **Workload Pattern Analysis**:
   - Analyze multiple queries as a workload
   - Identify overlapping index opportunities
   - Detect conflicting index requirements (OLTP vs OLAP)
   - Recommend read replicas or caching for read-heavy workloads

2. **Advanced Index Strategies**:
   - Covering indexes to eliminate table lookups
   - Partial/filtered indexes to reduce index size
   - Index-only scans (PostgreSQL) or loose index scans (MySQL)
   - Multi-column index order optimization

3. **Migration Guidance**:
   - SQL to NoSQL candidates (high read/write ratio, flexible schema)
   - NoSQL to SQL candidates (complex transactions, strong consistency)
   - Polyglot persistence recommendations (right database for right use case)

4. **Benchmarking Recommendations**:
   - Generate pgbench (PostgreSQL), sysbench (MySQL), or YCSB (NoSQL) test scenarios
   - Define success metrics (latency p95, throughput)

5. **Output**: Comprehensive optimization strategy with implementation roadmap

**Abort Conditions**:
- Workload too diverse to analyze coherently (>10 distinct query patterns)
- Insufficient data to make reliable recommendations

## Decision Rules

1. **Index Creation Threshold**:
   - Recommend index if query scans >1000 rows to return <100 rows
   - Skip index if table <10k rows (full scan acceptable)
   - Avoid index if column cardinality <5% (low selectivity)

2. **Denormalization Threshold**:
   - Consider if query requires >3 JOINs
   - Evaluate if read:write ratio >10:1
   - Reject if data consistency critical (financial transactions)

3. **Database Type Recommendations**:
   - PostgreSQL: Complex queries, JSONB, full-text search, geospatial
   - MySQL: Simple OLTP, strong ecosystem, MariaDB compatibility
   - MongoDB: Flexible schema, horizontal scaling, document model
   - Redis: Caching, session store, real-time analytics, pub/sub

4. **Ambiguity Handling**:
   - If execution plan unclear → request EXPLAIN ANALYZE (PostgreSQL) or EXPLAIN FORMAT=JSON (MySQL)
   - If schema unknown → request schema dump or information_schema query
   - If performance acceptable despite anti-patterns → note improvement potential but low priority

## Output Contract

**Schema** (JSON):
```json
{
  "analysis_timestamp": "ISO-8601 datetime",
  "database_type": "string (postgresql|mysql|mongodb|redis|other)",
  "query_analyzed": "string",
  "findings": [
    {
      "type": "string (index|query_rewrite|schema_change|configuration)",
      "severity": "string (high|medium|low)",
      "description": "string",
      "recommendation": "string",
      "implementation_code": "string (DDL or config)",
      "estimated_impact": "string (e.g., '80% reduction in rows scanned')"
    }
  ],
  "index_recommendations": [
    {
      "table_or_collection": "string",
      "index_definition": "string (CREATE INDEX ... or db.collection.createIndex(...))",
      "rationale": "string",
      "estimated_size_mb": "number (optional)"
    }
  ],
  "query_rewrites": [
    {
      "original_query": "string",
      "optimized_query": "string",
      "improvement_rationale": "string"
    }
  ],
  "next_steps": ["string array of actionable items"],
  "sources_consulted": ["string array of URLs with access dates"]
}
```

**Required Fields**:
- `analysis_timestamp`, `database_type`, `findings` (must have ≥1 finding or explain why no issues found)
- If T2/T3: `sources_consulted` must include 2-4 authoritative sources

## Examples

**Example: PostgreSQL Slow Query Optimization**

Input:
```json
{
  "database_type": "postgresql",
  "query": "SELECT * FROM orders WHERE customer_id = 12345 AND status = 'pending' ORDER BY created_at DESC",
  "performance_metrics": {
    "execution_time_ms": 2300,
    "rows_scanned": 450000,
    "rows_returned": 15
  }
}
```

Output (T1):
```json
{
  "findings": [
    {"type": "query_rewrite", "severity": "medium", "description": "SELECT * loads unnecessary columns", "recommendation": "Use explicit column list"},
    {"type": "index", "severity": "high", "description": "Seq Scan on orders (450k rows scanned for 15 returned)", "recommendation": "Create composite index on (customer_id, status, created_at)"}
  ],
  "index_recommendations": [
    {"table_or_collection": "orders", "index_definition": "CREATE INDEX idx_orders_customer_status_created ON orders(customer_id, status, created_at DESC);", "rationale": "Covers WHERE predicates and ORDER BY"}
  ]
}
```

## Quality Gates

1. **Token Budget**:
   - T1: ≤2000 tokens (quick pattern scan, generic index hints)
   - T2: ≤6000 tokens (execution plan analysis, database-specific optimizations)
   - T3: ≤12000 tokens (workload analysis, migration guidance)
   - Abort if approaching limit without actionable output

2. **Safety**:
   - Never recommend DROP INDEX without analyzing query workload impact
   - Warn about locking implications of CREATE INDEX on large tables (suggest CONCURRENTLY for PostgreSQL)
   - Flag irreversible operations (denormalization, data type changes)

3. **Auditability**:
   - Every index recommendation must cite specific query pattern
   - Execution plan findings must reference specific nodes/stages
   - Estimated impact must show calculation method

4. **Determinism**:
   - Same query + execution plan → same recommendations
   - Randomness only in example data generation, not analysis logic

5. **Source Quality**:
   - T2+ must cite 2-4 official database documentation URLs with access dates
   - use-the-index-luke.com for general indexing principles (accessed 2025-10-25T22:10:45-04:00): https://use-the-index-luke.com/

## Resources

**PostgreSQL**:
- Official Performance Tips: https://www.postgresql.org/docs/current/performance-tips.html
- Index Types: https://www.postgresql.org/docs/current/indexes-types.html
- EXPLAIN Documentation: https://www.postgresql.org/docs/current/sql-explain.html

**MySQL**:
- Optimization Guide: https://dev.mysql.com/doc/refman/8.0/en/optimization.html
- Index Optimization: https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html
- EXPLAIN Format: https://dev.mysql.com/doc/refman/8.0/en/explain-output.html

**MongoDB**:
- Query Optimization: https://www.mongodb.com/docs/manual/core/query-optimization/
- Compound Indexes: https://www.mongodb.com/docs/manual/core/index-compound/
- Explain Plans: https://www.mongodb.com/docs/manual/reference/method/cursor.explain/

**Redis**:
- Data Types: https://redis.io/docs/latest/develop/data-types/
- Patterns: https://redis.io/docs/latest/develop/use/patterns/
- Best Practices: https://redis.io/docs/latest/develop/use/optimization/

**General**:
- use-the-index-luke.com: SQL indexing fundamentals (database-agnostic)
- See `resources/` directory for query templates and index strategy guides
