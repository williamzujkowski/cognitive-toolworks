---
name: MongoDB Database Architect
slug: database-mongodb-architect
description: Design MongoDB architectures with document modeling, indexing (ESR rule), sharding, aggregation pipelines, replica sets, and WiredTiger tuning.
capabilities:
  - Document schema design (embedding vs referencing, schema validation)
  - Advanced indexing (single, compound, multikey, text, geospatial, hashed, wildcard)
  - Sharding strategy (hashed vs ranged shard keys, chunk balancing)
  - Aggregation pipeline optimization ($match, $group, $project, $lookup)
  - Replica set configuration (read preferences, write concerns)
  - WiredTiger cache and connection pool tuning
  - MongoDB 8.0 specific optimizations (embedded config servers, queryable encryption)
  - Query profiling and performance troubleshooting with explain()
inputs:
  - Workload type (OLTP, OLAP, time-series, content management, real-time analytics)
  - Data volume and growth rate (documents, collections, total size)
  - Access patterns (query types, read/write ratio, cardinality)
  - Availability requirements (SLA, RTO, RPO)
  - Deployment environment (Atlas, self-hosted, cloud provider)
  - MongoDB version (default: 8.0)
outputs:
  - Document schema design with embedding/referencing decisions
  - Index recommendations with ESR rule application
  - Sharding strategy with shard key selection and justification
  - Aggregation pipeline examples with optimization techniques
  - Replica set configuration (primary, secondary, arbiter)
  - WiredTiger cache sizing and connection pool settings
  - Performance tuning recommendations with estimated improvements
  - Migration plan if upgrading from older MongoDB versions
keywords:
  - mongodb
  - nosql
  - document-database
  - schema-design
  - indexing
  - sharding
  - aggregation
  - replica-set
  - wiredtiger
  - performance-tuning
  - mongodb-8
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: public
links:
  - title: "MongoDB 8.0 Performance Improvements"
    url: "https://www.infoq.com/news/2024/10/mongodb-80-performances/"
    accessed: "2025-10-26T18:17:22-0400"
  - title: "MongoDB Indexing Best Practices"
    url: "https://www.mongodb.com/company/blog/performance-best-practices-indexing"
    accessed: "2025-10-26T18:17:22-0400"
  - title: "MongoDB Sharding Best Practices"
    url: "https://www.mongodb.com/company/blog/mongodb/performance-best-practices-sharding"
    accessed: "2025-10-26T18:17:22-0400"
  - title: "MongoDB Data Modeling - Embedding vs References"
    url: "https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/"
    accessed: "2025-10-26T18:17:22-0400"
---

## Purpose & When-To-Use

Invoke this skill when designing, reviewing, or optimizing MongoDB database architectures for applications requiring flexible schema, document-based data models, horizontal scalability, or high availability.

**Trigger Conditions:**
- "Design a MongoDB architecture for [use case]"
- "How should I model [entity relationships] in MongoDB?"
- "My MongoDB queries are slow, need indexing recommendations"
- "Plan a sharding strategy for [data volume] with [growth rate]"
- "Optimize MongoDB aggregation pipeline for [query pattern]"
- "Configure replica set for [availability SLA]"
- "Migrate from MongoDB [old version] to 8.0"

**Out of Scope:**
- SQL database design (use database-postgres-architect)
- Redis caching (use database-redis-architect when available)
- General database migration (use database-migration-generator)

---

## Pre-Checks

1. **Time Normalization:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601).
2. **Input Validation:**
   - Workload type specified (OLTP, OLAP, time-series, content, analytics)
   - Data volume estimates available (documents, collections, size)
   - Access patterns described (query types, read/write ratio)
3. **Version Check:** MongoDB version specified (default to 8.0 if not provided).
4. **Deployment Context:** Cloud provider or self-hosted, resource constraints (RAM, CPU, storage).
5. **Existing Schema:** If optimizing existing database, request sample documents and query patterns.

**Abort Conditions:**
- No workload type or access patterns provided → emit TODO list with required inputs.
- Data volume completely unknown → warn that sizing recommendations will be generic.

---

## Procedure

### T1: Quick Schema Review & Index Recommendations (≤2k tokens)

**Use Case:** Fast path for common scenarios (80% of requests).

**Steps:**
1. **Analyze Access Patterns:** Identify top 3-5 most frequent queries.
2. **Document Modeling Decision:**
   - **Embed** if 1-to-1 or 1-to-many relationships, low cardinality, read-heavy, atomic updates needed.
   - **Reference** if many-to-many, frequently changing data, high cardinality, document size >16 MB risk.
3. **Index Recommendations (ESR Rule):**
   - **E**quality fields first (exact match filters: `{status: "active"}`)
   - **S**ort fields next (sort order: `.sort({created_at: -1})`)
   - **R**ange fields last (range queries: `{age: {$gt: 18}}`)
   - Example: `db.users.createIndex({status: 1, created_at: -1, age: 1})`
4. **Top 3 Bottlenecks:** Identify missing indexes, sequential scans, document size issues.
5. **Quick Wins:** Provide 1-3 immediate optimizations with estimated speedup (e.g., "Add index on email → 100x faster login").

**Output:** Schema design decision, 3-5 index recommendations with ESR justification, top 3 bottlenecks.

---

### T2: Complete Architecture Design (≤6k tokens)

**Use Case:** Comprehensive architecture for production deployments.

**Steps:**

#### 1. Document Schema Design

**Embedding vs Referencing Table:**

| Criteria | Embed | Reference |
|----------|-------|-----------|
| Relationship | 1-to-1, 1-to-many (low cardinality) | many-to-many, 1-to-many (high cardinality) |
| Access Pattern | Always queried together | Often queried independently |
| Update Frequency | Infrequent updates | Frequent updates to related data |
| Data Growth | Bounded, predictable | Unbounded, grows over time |
| Document Size | <16 MB total | Risk of exceeding 16 MB limit |
| Atomic Writes | Need atomicity across related data | Atomicity not required |

**Schema Validation (MongoDB 8.0):**
```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "created_at"],
      properties: {
        email: {bsonType: "string", pattern: "^.+@.+$"},
        age: {bsonType: "int", minimum: 0, maximum: 150},
        created_at: {bsonType: "date"}
      }
    }
  }
})
```

#### 2. Advanced Indexing Strategy

**Index Types and Use Cases:**

| Index Type | Use Case | Example |
|------------|----------|---------|
| Single Field | Equality or range on one field | `db.users.createIndex({email: 1})` |
| Compound (ESR) | Multi-field queries (Equality, Sort, Range) | `db.orders.createIndex({status: 1, created_at: -1, total: 1})` |
| Multikey | Arrays (e.g., tags, categories) | `db.products.createIndex({tags: 1})` |
| Text | Full-text search | `db.posts.createIndex({content: "text"})` |
| Geospatial | Location-based queries (2dsphere) | `db.locations.createIndex({coordinates: "2dsphere"})` |
| Hashed | Sharding, equality-only queries | `db.sessions.createIndex({session_id: "hashed"})` |
| Wildcard | Flexible schema with many fields | `db.events.createIndex({"metadata.$**": 1})` |
| Partial | Index subset of documents | `db.users.createIndex({last_login: 1}, {partialFilterExpression: {active: true}})` |

**Covered Query Optimization:**
```javascript
// Covered query: all fields in index, no document access
db.orders.createIndex({user_id: 1, status: 1, total: 1})
db.orders.find({user_id: 12345, status: "shipped"}, {_id: 0, user_id: 1, status: 1, total: 1})
// explain() shows: totalDocsExamined: 0 (covered by index)
```

**ESR Rule Application:**
```javascript
// Query: Find active users, sort by created_at descending, filter age > 18
db.users.find({status: "active", age: {$gt: 18}}).sort({created_at: -1})

// Correct index (ESR):
// Equality: status (exact match)
// Sort: created_at (sort field)
// Range: age (range filter)
db.users.createIndex({status: 1, created_at: -1, age: 1})
```

#### 3. Sharding Strategy

**Shard Key Selection (MongoDB 8.0):**

| Shard Key Type | Use Case | Pros | Cons |
|----------------|----------|------|------|
| Hashed | Monotonically increasing IDs, even distribution | Uniform write distribution, no hotspots | Cannot use range queries efficiently on shard key |
| Ranged | Time-series data, natural ordering | Efficient range queries, targeted reads | Risk of hotspots if monotonic (e.g., timestamp) |
| Compound | Multi-tenant apps, complex access patterns | Balances distribution and query targeting | More complex to design |

**Hashed Sharding Example:**
```javascript
// Enable sharding on database
sh.enableSharding("myapp")

// Shard collection with hashed shard key
sh.shardCollection("myapp.users", {user_id: "hashed"})

// MongoDB 8.0: Move unsharded collection to specific shard
db.adminCommand({moveCollection: "myapp.analytics", toShard: "shard02"})
```

**Ranged Sharding Example (Time-Series):**
```javascript
// Shard by timestamp for time-series data
sh.shardCollection("myapp.events", {timestamp: 1})

// Zone sharding (MongoDB 8.0): Route data by date ranges to specific shards
sh.addShardToZone("shard01", "recent")
sh.updateZoneKeyRange("myapp.events", {timestamp: ISODate("2025-01-01")}, {timestamp: MaxKey}, "recent")
```

**Avoid Scatter-Gather Queries:**
- Include shard key in queries: `db.users.find({user_id: 12345})` → targets single shard
- Without shard key: `db.users.find({email: "test@example.com"})` → scatter-gather across all shards (slow)
- Exception: Large aggregations benefit from parallelism across shards

#### 4. Aggregation Pipeline Optimization

**Pipeline Stages (Execution Order Matters):**

```javascript
// Optimized aggregation: $match early, $project late, use indexes
db.orders.aggregate([
  // Stage 1: $match FIRST (uses index, reduces documents)
  {$match: {status: "shipped", created_at: {$gte: ISODate("2025-01-01")}}},

  // Stage 2: $sort (uses index if compound index exists)
  {$sort: {created_at: -1}},

  // Stage 3: $lookup (join with users collection)
  {$lookup: {
    from: "users",
    localField: "user_id",
    foreignField: "_id",
    as: "user_details"
  }},

  // Stage 4: $group (aggregation after filtering)
  {$group: {
    _id: "$user_id",
    total_spent: {$sum: "$total"},
    order_count: {$sum: 1}
  }},

  // Stage 5: $project LAST (reduce network transfer)
  {$project: {_id: 1, total_spent: 1, order_count: 1}}
])
```

**Index Sort Optimization:**
- If `{status: 1, created_at: -1}` index exists, `$match` + `$sort` uses index (no in-memory sort).
- Without index, MongoDB sorts in memory (limited by 100 MB unless `allowDiskUse: true`).

**Sharded Aggregation (MongoDB 8.0):**
- Aggregations run in parallel on each shard, then merge results.
- Use `$match` early to enable shard targeting.
- MongoDB 8.0: 32% overall performance improvement in aggregations.

#### 5. Replica Set Configuration

**Standard 3-Member Replica Set:**

```javascript
rs.initiate({
  _id: "myReplicaSet",
  members: [
    {_id: 0, host: "mongo1.example.com:27017", priority: 2},  // Primary (high priority)
    {_id: 1, host: "mongo2.example.com:27017", priority: 1},  // Secondary
    {_id: 2, host: "mongo3.example.com:27017", arbiterOnly: true}  // Arbiter (no data)
  ]
})
```

**Read Preferences:**
- `primary` (default): All reads from primary (strong consistency).
- `primaryPreferred`: Read from primary, fallback to secondary if unavailable.
- `secondary`: Read from secondary (may read stale data).
- `secondaryPreferred`: Read from secondary, fallback to primary.
- `nearest`: Read from lowest-latency member.

**Write Concerns:**
- `w: 1` (default): Acknowledge after primary write (fast, risk of data loss on primary failure).
- `w: "majority"`: Acknowledge after majority of replica set members (slower, durable).
- `w: 3`: Acknowledge after 3 members (explicit count).
- `j: true`: Wait for write to journal (disk) before acknowledging.

**MongoDB 8.0 Replica Set Enhancements:**
- Faster concurrent writes during replication.
- Disable "majority" read concern for PSA (Primary-Secondary-Arbiter) to avoid cache pressure.

#### 6. WiredTiger Cache & Connection Pool Tuning

**WiredTiger Cache Sizing (MongoDB 8.0):**

```yaml
# Default: 50% of RAM - 1 GB
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 32  # For 64 GB RAM server (50%)
```

**Guidelines:**
- **Production:** 50-62.5% of available RAM (balance with filesystem cache).
- **Cache should hold working set** (frequently accessed data).
- **Monitor:** `db.serverStatus().wiredTiger.cache` (bytes in cache, eviction activity).
- **Too large:** Starves OS filesystem cache, degrades performance.
- **Too small:** High eviction rate, poor query performance.

**Connection Pool Configuration:**

```javascript
// Application connection string
mongodb://mongo1.example.com:27017,mongo2.example.com:27017,mongo3.example.com:27017/?replicaSet=myReplicaSet&maxPoolSize=50&minPoolSize=10&maxIdleTimeMS=60000
```

**Settings:**
- `maxPoolSize`: Maximum connections (default 100). Each connection ~1 MB RAM.
- `minPoolSize`: Minimum connections (default 0). Pre-warm pool for faster queries.
- `maxIdleTimeMS`: Close idle connections after timeout (default: no timeout).
- **Rule of Thumb:** maxPoolSize ≈ (expected concurrent operations) + 10-20% buffer.

#### 7. Performance Tuning (MongoDB 8.0)

**Configuration Parameters:**

```yaml
# For 64 GB RAM server (OLTP workload)
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 32                    # 50% of RAM
    collectionConfig:
      blockCompressor: snappy             # Default compression
    indexConfig:
      prefixCompression: true             # Index prefix compression

net:
  maxIncomingConnections: 65536           # Max client connections
  compression:
    compressors: snappy                   # Network compression

operationProfiling:
  mode: slowOp                            # Profile slow queries
  slowOpThresholdMs: 100                  # Log queries >100ms

replication:
  replSetName: myReplicaSet
  enableMajorityReadConcern: true         # Disable for PSA if cache pressure
```

**MongoDB 8.0 Performance Improvements:**
- **36% faster reads** (vectored I/O, reduced memory usage).
- **56% faster bulk inserts** (batch processing optimizations).
- **75% query latency reduction** (internal benchmarks).
- **Embedded sharding config servers** (no separate config server replica set).
- **Move collections across shards without shard key** (MongoDB 8.0 feature).

**Output:** Complete architecture document with schema design, index definitions, sharding strategy, aggregation examples, replica set config, tuning parameters.

---

### T3: Enterprise Features & Migration Planning (≤12k tokens)

**Use Case:** Multi-region deployments, queryable encryption, sharding at scale, version migrations.

**Steps:**

#### 1. Multi-Region Replica Set (Global Deployment)

```javascript
rs.initiate({
  _id: "globalReplicaSet",
  members: [
    {_id: 0, host: "us-east-1.example.com:27017", priority: 2, tags: {region: "us-east"}},
    {_id: 1, host: "us-east-2.example.com:27017", priority: 1, tags: {region: "us-east"}},
    {_id: 2, host: "eu-west-1.example.com:27017", priority: 1, tags: {region: "eu-west"}},
    {_id: 3, host: "ap-southeast-1.example.com:27017", priority: 1, tags: {region: "ap-southeast"}},
    {_id: 4, host: "arbiter.example.com:27017", arbiterOnly: true}
  ],
  settings: {
    // Read from nearest region
    getLastErrorDefaults: {w: "majority", wtimeout: 5000}
  }
})

// Region-specific read preferences
db.users.find({region: "us-east"}).readPref("nearest", [{region: "us-east"}])
```

#### 2. Queryable Encryption (MongoDB 8.0)

**Use Case:** Encrypt sensitive fields (PII, PHI) while allowing queries.

```javascript
// Create encrypted collection (MongoDB 8.0 expanded support)
db.createCollection("patients", {
  encryptedFields: {
    fields: [
      {
        path: "ssn",
        bsonType: "string",
        queries: {queryType: "equality"}  // Allow equality queries on encrypted field
      },
      {
        path: "medical_record",
        bsonType: "string"
        // No queries specification = cannot query, only store/retrieve
      }
    ]
  }
})

// Query encrypted field
db.patients.find({ssn: "123-45-6789"})  // Allowed (queryable encryption)
```

#### 3. Cross-Shard Aggregation Optimization

**Parallel Execution on Sharded Cluster:**

```javascript
// Aggregation runs in parallel on each shard, then merges
db.orders.aggregate([
  {$match: {created_at: {$gte: ISODate("2025-01-01")}}},  // Shard targeting if sharded by created_at
  {$group: {_id: "$product_id", total_sales: {$sum: "$total"}}},
  {$sort: {total_sales: -1}},
  {$limit: 10}
], {allowDiskUse: true})  // Allow >100 MB sort for large datasets
```

**Optimization:**
- Shard by time-based field → `$match` with date range targets recent shards only.
- MongoDB 8.0: Improved parallelism for FULL OUTER JOIN and aggregations.
- Monitor with `db.currentOp()` to see query distribution across shards.

#### 4. Migration from MongoDB 6.x/7.x to 8.0

**Benefits of MongoDB 8.0:**
- 36% faster reads, 56% faster bulk inserts (accessed 2025-10-26T18:17:22-0400, [InfoQ MongoDB 8.0](https://www.infoq.com/news/2024/10/mongodb-80-performances/)).
- Embedded sharding config servers (reduce infrastructure).
- Queryable encryption enhancements.
- Move collections across shards without shard key.

**Migration Strategy (Zero-Downtime):**

1. **Set up MongoDB 8.0 replica set members** (add to existing replica set as secondaries).
2. **Replicate data** (wait for secondaries to sync).
3. **Test queries on MongoDB 8.0 secondaries** (validate compatibility, performance).
4. **Stepdown primary** (`rs.stepDown()`) → elect MongoDB 8.0 member as new primary.
5. **Upgrade remaining members** (rolling upgrade, one at a time).
6. **Set feature compatibility version:** `db.adminCommand({setFeatureCompatibilityVersion: "8.0"})`.
7. **Monitor for 24h** (rollback if issues detected).

**Risks:**
- Incompatible drivers (ensure client drivers support MongoDB 8.0).
- Deprecated features removed (check release notes).
- Configuration parameter changes.

#### 5. Monitoring & Observability

**Key Metrics:**

```javascript
// Server status
db.serverStatus()

// WiredTiger cache stats
db.serverStatus().wiredTiger.cache
// Monitor: bytes currently in cache, bytes read into cache, eviction activity

// Connection stats
db.serverStatus().connections
// Monitor: current, available, totalCreated

// Operation counters
db.serverStatus().opcounters
// Monitor: insert, query, update, delete, getmore, command

// Slow query profiling
db.system.profile.find({millis: {$gt: 100}}).sort({ts: -1}).limit(10)

// Index usage stats
db.collection.aggregate([{$indexStats: {}}])
```

**Tools:**
- MongoDB Atlas: Built-in monitoring, Performance Advisor (index recommendations).
- Self-Hosted: Percona Monitoring and Management (PMM), MongoDB Ops Manager.
- Application Performance Monitoring (APM): Datadog, New Relic, Dynatrace.

**Output:** Multi-region architecture, queryable encryption setup, cross-shard aggregation strategy, migration plan with risks, monitoring dashboards.

---

## Decision Rules

1. **Embedding vs Referencing:**
   - If relationship is 1-to-many with <100 related documents → **Embed**.
   - If related data changes frequently or queried independently → **Reference**.
   - If document size risk >16 MB or unbounded growth → **Reference**.

2. **Index Creation:**
   - Add index if query scans >1000 documents without index.
   - Use compound index (ESR rule) for multi-field queries.
   - Avoid indexes on low-cardinality fields (<10 distinct values).
   - Use partial indexes for large collections with filtered queries.

3. **Sharding Trigger:**
   - Enable sharding if data size >200 GB or growth rate >50 GB/month.
   - Use hashed shard key for monotonic IDs (avoid hotspots).
   - Use ranged shard key for time-series data with zone sharding.

4. **Replica Set Configuration:**
   - Use 3-member replica set minimum (1 primary + 2 secondaries or 1 secondary + 1 arbiter).
   - Use 5-member replica set for high availability (1 primary + 4 secondaries).
   - Set `w: "majority"` for critical writes (durability over speed).
   - Use `readPreference: "secondary"` for analytics queries (offload primary).

5. **WiredTiger Cache Sizing:**
   - Allocate 50% of RAM for WiredTiger cache (default).
   - Increase to 62.5% if working set >50% RAM and low filesystem cache usage.
   - Decrease if high OS memory pressure or filesystem cache thrashing.

6. **Aggregation Optimization:**
   - Place `$match` as early as possible (reduce documents).
   - Use indexes for `$match` and `$sort` stages.
   - Use `$project` last to reduce network transfer.
   - Enable `allowDiskUse: true` for >100 MB sorts/groups.

**Uncertainty Thresholds:**
- If access patterns unclear → request sample queries and usage statistics.
- If data volume highly uncertain → provide scalable architecture with sharding plan.
- If existing schema has >10 collections → focus on top 3 most-queried collections first.

---

## Output Contract

**Required Fields:**

```yaml
document_schema:
  - collection_name: string
    embedding_decision: "embed" | "reference"
    justification: string (why embed or reference)
    schema_validation: object (JSON schema)
    sample_document: object

indexes:
  - collection_name: string
    index_name: string
    index_definition: object ({field: 1|-1})
    index_type: "single" | "compound" | "multikey" | "text" | "geospatial" | "hashed" | "wildcard" | "partial"
    esr_justification: string (if compound index)
    estimated_speedup: string (e.g., "50x faster")

sharding_strategy:
  - enabled: boolean
    shard_key: object ({field: "hashed" | 1})
    shard_key_type: "hashed" | "ranged" | "compound"
    justification: string (why this shard key)
    target_chunk_size: string (default: "64 MB")

aggregation_examples:
  - use_case: string
    pipeline: array (aggregation stages)
    optimization_notes: string

replica_set:
  - members: integer (3, 5, etc.)
    configuration: object (rs.initiate() config)
    read_preference: "primary" | "primaryPreferred" | "secondary" | "secondaryPreferred" | "nearest"
    write_concern: object ({w: "majority", j: true})

performance_tuning:
  - wiredtiger_cache_gb: number
    max_connections: integer
    connection_pool_size: integer
    profiling_threshold_ms: integer
    estimated_improvement: string (e.g., "36% faster reads")

migration_plan:  # If upgrading versions
  - current_version: string
    target_version: string
    strategy: "rolling upgrade" | "blue-green" | "snapshot restore"
    steps: array (migration steps)
    risks: array (potential issues)
    downtime_estimate: string
```

**Token Tier Minimums:**
- T1: document_schema (embed/reference decision), indexes (top 3-5), bottlenecks (top 3).
- T2: All of T1 + sharding_strategy, aggregation_examples, replica_set, performance_tuning.
- T3: All of T2 + multi-region, queryable_encryption, migration_plan, monitoring.

---

## Examples

**ESR Rule for Compound Index:**

```javascript
// Query: Find active users, sort by created_at descending, filter age > 18
db.users.find({status: "active", age: {$gt: 18}}).sort({created_at: -1})

// Index following ESR rule:
// E (Equality): status
// S (Sort): created_at
// R (Range): age
db.users.createIndex({status: 1, created_at: -1, age: 1})
```

See `examples/content-management-mongodb-architecture.txt` for a complete architecture example.

---

## Quality Gates

1. **Token Budgets:**
   - T1 response ≤2k tokens (fast path, common scenarios).
   - T2 response ≤6k tokens (complete architecture).
   - T3 response ≤12k tokens (enterprise features, migrations).

2. **Safety Checks:**
   - No credentials or connection strings with passwords in output.
   - Schema validation rules enforce data quality (no malformed documents).
   - Audit logging enabled for sensitive collections (PII, PHI).

3. **Auditability:**
   - All index recommendations include ESR justification.
   - All sharding strategies include shard key selection reasoning.
   - All performance claims cite MongoDB 8.0 benchmarks with access dates.

4. **Determinism:**
   - Same input (workload, data volume, access patterns) → same architecture recommendations.
   - Index order deterministic (ESR rule applied consistently).

5. **Citations:**
   - MongoDB 8.0 performance improvements: 36% faster reads, 56% faster bulk inserts (accessed 2025-10-26T18:17:22-0400, [InfoQ](https://www.infoq.com/news/2024/10/mongodb-80-performances/)).
   - ESR Rule (Equality, Sort, Range) for compound indexes (accessed 2025-10-26T18:17:22-0400, [MongoDB Blog](https://www.mongodb.com/company/blog/performance-best-practices-indexing)).
   - WiredTiger cache default: 50% RAM - 1 GB (accessed 2025-10-26T18:17:22-0400, [MongoDB Docs](https://www.mongodb.com/docs/manual/faq/storage/)).

---

## Resources

**Official MongoDB Documentation:**
- [MongoDB 8.0 Release Notes](https://www.mongodb.com/docs/manual/release-notes/8.0/)
- [Data Modeling Introduction](https://www.mongodb.com/docs/manual/data-modeling/)
- [Indexing Strategies](https://www.mongodb.com/docs/manual/indexes/)
- [Sharding Reference](https://www.mongodb.com/docs/manual/sharding/)
- [Aggregation Pipeline](https://www.mongodb.com/docs/manual/aggregation/)
- [Replica Set Configuration](https://www.mongodb.com/docs/manual/replication/)

**Performance & Best Practices:**
- [Performance Best Practices: Indexing](https://www.mongodb.com/company/blog/performance-best-practices-indexing) (accessed 2025-10-26T18:17:22-0400)
- [Performance Best Practices: Sharding](https://www.mongodb.com/company/blog/mongodb/performance-best-practices-sharding) (accessed 2025-10-26T18:17:22-0400)
- [MongoDB 8.0 Performance Improvements](https://www.infoq.com/news/2024/10/mongodb-80-performances/) (accessed 2025-10-26T18:17:22-0400)
- [WiredTiger Cache Tuning](https://source.wiredtiger.com/mongodb-6.0/tune_cache.html) (accessed 2025-10-26T18:17:22-0400)

**Tools:**
- [MongoDB Compass](https://www.mongodb.com/products/compass) (GUI for schema exploration and index management)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (managed cloud database with Performance Advisor)
- [Percona Monitoring and Management (PMM)](https://www.percona.com/software/database-tools/percona-monitoring-and-management) (self-hosted monitoring)
