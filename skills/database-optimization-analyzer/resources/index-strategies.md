# Index Design Strategies by Database

## PostgreSQL Index Strategies

### Composite Index Column Order
**Rule**: Equality → Range → Sort (E-R-S)
```sql
-- Query: WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY priority DESC
-- Optimal index:
CREATE INDEX idx_status_created_priority ON tasks(status, created_at, priority DESC);
```

### Covering Indexes (Index-Only Scans)
```sql
-- Include frequently accessed columns to avoid table lookup
CREATE INDEX idx_orders_covering ON orders(customer_id, status) INCLUDE (total, created_at);
```

### Partial Indexes
```sql
-- Index only active records
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
-- Reduces index size by ~90% if only 10% of users are active
```

### GIN/GiST Indexes for Special Data Types
```sql
-- Full-text search
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- JSONB queries
CREATE INDEX idx_metadata_tags ON products USING GIN(metadata jsonb_path_ops);
```

## MySQL Index Strategies

### Index Merge Optimization
```sql
-- MySQL can merge multiple indexes
CREATE INDEX idx_status ON orders(status);
CREATE INDEX idx_priority ON orders(priority);
-- Query: WHERE status = 'pending' OR priority = 'high'
-- MySQL may use index_merge(idx_status, idx_priority)
```

### Prefix Indexes for Long Strings
```sql
-- Index first 10 characters only
CREATE INDEX idx_email_prefix ON users(email(10));
-- Reduces index size, may require additional table lookup for exact match
```

### Index Condition Pushdown (ICP)
```sql
-- MySQL 5.6+ pushes WHERE conditions to storage engine
CREATE INDEX idx_composite ON orders(customer_id, status);
-- Query: WHERE customer_id = 123 AND status = 'shipped' AND total > 100
-- Index used for customer_id, status; total filtered via ICP
```

## MongoDB Index Strategies

### ESR Rule (Equality, Sort, Range)
```javascript
// Query: db.orders.find({status: 'shipped', total: {$gt: 100}}).sort({created_at: -1})
// Optimal index:
db.orders.createIndex({status: 1, created_at: -1, total: 1});
// Equality first (status), then sort (created_at), then range (total)
```

### Compound Index vs Index Intersection
```javascript
// Compound index (preferred for frequent query):
db.users.createIndex({status: 1, age: 1});

// Index intersection (flexible but slower):
db.users.createIndex({status: 1});
db.users.createIndex({age: 1});
// MongoDB may intersect both indexes, but compound is faster
```

### Covered Queries
```javascript
// Query projects only indexed fields (no document fetch)
db.users.createIndex({email: 1, name: 1});
db.users.find({email: 'user@example.com'}, {_id: 0, email: 1, name: 1});
// explain() shows 'PROJECTION_COVERED'
```

### Sparse Indexes
```javascript
// Index only documents with specific field
db.users.createIndex({phone: 1}, {sparse: true});
// Reduces index size if many documents lack phone field
```

## Redis Data Structure Selection

### Hash vs String for Objects
```redis
# Bad: Storing JSON as STRING
SET user:123 '{"name":"John","email":"john@example.com"}'

# Good: Using HASH for structured data
HSET user:123 name "John" email "john@example.com"
# Allows: HGET user:123 name (fetch single field)
```

### Sorted Sets for Rankings
```redis
# Leaderboard with scores
ZADD leaderboard 1500 "player1" 1200 "player2"
ZREVRANGE leaderboard 0 9 WITHSCORES  # Top 10 players
```

### Geospatial Indexes
```redis
# Store locations with GEO commands
GEOADD locations 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
GEORADIUS locations 15 37 100 km WITHDIST
```

## General Indexing Principles

1. **Selectivity**: Index high-cardinality columns (many distinct values)
   - Email (high selectivity) vs Gender (low selectivity)
   - Cardinality = Distinct values / Total rows

2. **Index Size**: Balance coverage vs size
   - Too many indexes slow writes (INSERT/UPDATE must update all indexes)
   - Rule of thumb: ≤5 indexes per table for OLTP

3. **Index Maintenance**:
   - PostgreSQL: REINDEX CONCURRENTLY to rebuild bloated indexes
   - MySQL: OPTIMIZE TABLE to defragment indexes
   - MongoDB: db.collection.reIndex() (use sparingly, locks collection)

4. **Monitoring**:
   - PostgreSQL: pg_stat_user_indexes (identify unused indexes)
   - MySQL: INFORMATION_SCHEMA.INDEX_STATISTICS
   - MongoDB: $indexStats aggregation stage
