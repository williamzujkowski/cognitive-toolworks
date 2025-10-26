# Common Query Anti-Patterns and Fixes

## SQL Anti-Patterns

### 1. SELECT * (Column Over-Fetching)
**Bad**: `SELECT * FROM users WHERE id = 123;`
**Good**: `SELECT id, name, email FROM users WHERE id = 123;`
**Rationale**: Reduces network overhead and enables covering indexes.

### 2. Leading Wildcard in LIKE
**Bad**: `SELECT * FROM products WHERE name LIKE '%phone%';`
**Good**: `SELECT * FROM products WHERE name LIKE 'phone%';` OR use full-text search
**Rationale**: Leading wildcard prevents index usage, forces full table scan.

### 3. Functions on Indexed Columns
**Bad**: `SELECT * FROM orders WHERE YEAR(created_at) = 2025;`
**Good**: `SELECT * FROM orders WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01';`
**Rationale**: Function on column prevents index usage (index on created_at unusable).

### 4. OR Conditions on Different Columns
**Bad**: `SELECT * FROM users WHERE email = 'x' OR phone = 'y';`
**Good**: Use UNION or separate queries, or create indexes on both columns
**Rationale**: Database may not use index merge efficiently.

### 5. Implicit Type Conversion
**Bad**: `SELECT * FROM orders WHERE customer_id = '12345';` (customer_id is INT)
**Good**: `SELECT * FROM orders WHERE customer_id = 12345;`
**Rationale**: Type mismatch prevents index usage.

## MongoDB Anti-Patterns

### 1. Large Skip() Operations
**Bad**: `db.products.find().skip(10000).limit(10);`
**Good**: Use range queries with _id or indexed field for pagination
**Rationale**: skip() scans and discards all skipped documents.

### 2. Regex Without Anchors
**Bad**: `db.users.find({name: /john/i});`
**Good**: `db.users.find({name: /^john/i});` (anchored at start)
**Rationale**: Unanchored regex prevents efficient index usage.

### 3. $where Operator
**Bad**: `db.orders.find({$where: "this.total > 100"});`
**Good**: `db.orders.find({total: {$gt: 100}});`
**Rationale**: $where executes JavaScript for each document, no index usage.

## Redis Anti-Patterns

### 1. KEYS Command in Production
**Bad**: `KEYS user:*` (blocks Redis for large keyspaces)
**Good**: `SCAN 0 MATCH user:* COUNT 100` (cursor-based iteration)
**Rationale**: KEYS is O(N) and blocks other operations.

### 2. Large VALUES in Strings
**Bad**: Storing entire JSON object as single STRING
**Good**: Use HASH for structured data with field-level access
**Rationale**: HASHes allow partial updates, reduce network overhead.

### 3. Missing TTL on Ephemeral Data
**Bad**: `SET session:abc123 "data"` (no expiration)
**Good**: `SETEX session:abc123 3600 "data"` (1 hour TTL)
**Rationale**: Prevents memory exhaustion from stale data.
