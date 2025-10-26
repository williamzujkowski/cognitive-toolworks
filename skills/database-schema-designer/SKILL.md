---
name: Database Schema Designer
slug: database-schema-designer
description: Design normalized database schemas with ERDs, migration plans, and indexing strategies for relational and document databases
capabilities:
  - Entity-relationship modeling and normalization (1NF-3NF, BCNF)
  - Schema migration planning with rollback strategies
  - Index design and query optimization patterns
  - Constraint modeling (FK, unique, check, triggers)
  - Multi-database support (PostgreSQL, MySQL, MongoDB, DynamoDB)
inputs:
  - business_requirements: Domain entities, relationships, and access patterns
  - existing_schema: Optional current schema for evolution/refactoring
  - database_type: Target database system (postgres, mysql, mongo, etc.)
  - scale_requirements: Expected data volume and query patterns
outputs:
  - erd_diagram: Mermaid ER diagram with entities and relationships
  - ddl_scripts: CREATE TABLE statements with constraints and indexes
  - migration_plan: Ordered migration steps with rollback procedures
  - optimization_notes: Indexing strategy and query pattern recommendations
keywords:
  - database
  - schema
  - ERD
  - normalization
  - migration
  - SQL
  - DDL
  - indexes
  - constraints
  - data-modeling
version: 1.0.0
owner: cloud.gov OCS
license: Apache-2.0
security: Safe for design work; no credentials or production data
links:
  - https://www.postgresql.org/docs/current/ddl.html
  - https://dev.mysql.com/doc/refman/8.0/en/data-types.html
  - https://docs.mongodb.com/manual/data-modeling/
---

## Purpose & When-To-Use

Use this skill when you need to:
- Design a new database schema from business requirements
- Refactor an existing schema for better normalization or performance
- Plan a migration strategy between schema versions
- Optimize database structure for specific access patterns
- Choose appropriate data types, indexes, and constraints

**Skip this skill** if you only need query optimization (use `database-optimization-analyzer`) or simple CRUD operations.

## Pre-Checks

1. **Verify time context**: Compute `NOW_ET` = 2025-10-26T12:00:00-04:00 (accessed via NIST/time.gov semantics)
2. **Validate inputs**:
   - Business requirements describe entities, relationships, and cardinality
   - Database type is specified (default: PostgreSQL)
   - Scale requirements include estimated row counts and query frequency
3. **Check database documentation** is current (accessed NOW_ET):
   - PostgreSQL 16+ docs (https://www.postgresql.org/docs/current/, accessed 2025-10-26)
   - MySQL 8.0+ docs (https://dev.mysql.com/doc/, accessed 2025-10-26)
   - MongoDB 7.0+ docs (https://docs.mongodb.com/, accessed 2025-10-26)

## Procedure

### T1: Fast Path (≤2k tokens) - Simple Schema Design

For straightforward domains with 3-8 entities and clear relationships:

1. **Entity extraction** (100 tokens):
   - Identify nouns from requirements → entities
   - List attributes with data types
   - Note primary keys (natural vs surrogate)

2. **Relationship modeling** (200 tokens):
   - Identify entity relationships (1:1, 1:N, N:M)
   - Resolve N:M with junction tables
   - Add foreign key constraints

3. **Quick normalization** (150 tokens):
   - Check 1NF: Atomic values, no repeating groups
   - Check 2NF: No partial dependencies
   - Check 3NF: No transitive dependencies

4. **Basic indexes** (100 tokens):
   - Primary key indexes (automatic)
   - Foreign key indexes (recommended)
   - Common query column indexes

5. **Output** (≤1.5k tokens):
   - Mermaid ERD
   - DDL CREATE TABLE statements
   - Basic index creation statements

### T2: Standard Path (≤6k tokens) - Production-Ready Schema

For complex domains requiring optimization and migration planning:

1. **All T1 steps** (550 tokens)

2. **Advanced normalization** (300 tokens):
   - Evaluate BCNF for complex functional dependencies
   - Consider controlled denormalization for read performance
   - Document normalization decisions and trade-offs

3. **Constraint design** (400 tokens):
   - Check constraints for data validation
   - Unique constraints for business rules
   - Triggers for complex integrity rules
   - Cascade rules for foreign keys (ON DELETE, ON UPDATE)

4. **Index optimization** (500 tokens):
   - Composite indexes for multi-column queries
   - Covering indexes for SELECT performance
   - Partial indexes for filtered queries
   - Full-text search indexes if applicable

5. **Migration planning** (800 tokens):
   - Version N → N+1 migration steps
   - Data backfill scripts for new columns
   - Rollback procedures for each step
   - Zero-downtime migration strategy (if required)

6. **Documentation** (≤3.5k tokens):
   - ERD with cardinality notation
   - Complete DDL with comments
   - Migration plan with ordering
   - Index justification and query patterns

### T3: Deep Dive (≤12k tokens) - Enterprise Schema with Partitioning

For large-scale systems requiring partitioning, sharding, or cross-database design:

1. **All T2 steps** (≤6k tokens)

2. **Scalability design** (1.5k tokens):
   - Table partitioning strategy (range, list, hash)
   - Sharding key selection and distribution
   - Archive table design for historical data
   - Read replicas and query routing

3. **Performance analysis** (1k tokens):
   - Query pattern analysis and index coverage
   - EXPLAIN plan review for common queries
   - Cardinality estimation and statistics
   - Partition pruning verification

4. **Data lifecycle** (800 tokens):
   - Retention policies and TTL implementation
   - Archive and purge procedures
   - GDPR/compliance considerations (anonymization, deletion)

5. **Comprehensive documentation** (≤2.7k tokens):
   - Full ERD with physical and logical views
   - DDL with partitioning and sharding
   - Complete migration plan with testing steps
   - Performance baseline and monitoring queries

## Decision Rules

**When to escalate complexity tier:**
- T1 → T2: More than 10 entities, OR migration from existing schema, OR explicit performance requirements
- T2 → T3: More than 50 tables, OR partitioning needed, OR multi-region deployment, OR >100M rows expected

**When to recommend denormalization:**
- Read:write ratio > 100:1 AND query joins >3 tables
- Real-time analytics dashboards requiring <100ms response
- Document explicitly: "Controlled denormalization for performance: [justification]"

**When to abort:**
- Requirements lack entity definitions or relationships
- Database type unsupported (emit TODO: "Add support for [database]")
- Conflicting constraints detected (e.g., circular foreign keys)

## Output Contract

**Required fields:**
```yaml
erd_diagram: string  # Mermaid ER diagram syntax
ddl_scripts: string  # Complete DDL (CREATE TABLE, indexes, constraints)
migration_plan: array  # Ordered steps with up/down scripts
optimization_notes: string  # Index strategy and query patterns
```

**Optional fields:**
```yaml
normalization_analysis: string  # 1NF-3NF evaluation
partitioning_strategy: string  # If T3 used
test_data_generator: string  # Sample INSERT statements
```

**Format:** JSON or YAML document, optionally with embedded SQL code blocks

## Examples

```sql
-- E-commerce schema: User, Product, Order, OrderItem (T1 example)
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock INTEGER DEFAULT 0 CHECK (stock >= 0)
);
CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
  total DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE order_items (
  order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES products(product_id) ON DELETE RESTRICT,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  price_snapshot DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (order_id, product_id)
);
CREATE INDEX idx_orders_user ON orders(user_id, created_at DESC);
CREATE INDEX idx_products_price ON products(price) WHERE stock > 0;
```

## Quality Gates

**Token budgets:**
- T1: ≤2k tokens (simple 3-8 entity schemas)
- T2: ≤6k tokens (production schemas with migrations)
- T3: ≤12k tokens (enterprise with partitioning/sharding)

**Safety checks:**
- [ ] No hardcoded credentials or sensitive data in examples
- [ ] All foreign keys have ON DELETE/ON UPDATE clauses specified
- [ ] Indexes justified by query patterns (not speculative)
- [ ] Migration steps are reversible (rollback provided)

**Validation:**
- [ ] DDL is syntactically valid for target database
- [ ] ERD entities match DDL tables 1:1
- [ ] All 3NF violations documented with justification
- [ ] Examples use sample/synthetic data only

**Determinism:**
- Use SERIAL/BIGSERIAL for PostgreSQL auto-increment
- Use AUTO_INCREMENT for MySQL
- Document any database-specific features used

## Resources

**Official Documentation** (accessed 2025-10-26):
- PostgreSQL DDL: https://www.postgresql.org/docs/current/ddl.html
- PostgreSQL Indexes: https://www.postgresql.org/docs/current/indexes.html
- MySQL Data Types: https://dev.mysql.com/doc/refman/8.0/en/data-types.html
- MongoDB Data Modeling: https://docs.mongodb.com/manual/data-modeling/

**Best Practices** (accessed 2025-10-26):
- Database Normalization Guide: https://www.sqlshack.com/database-normalization-process/
- Index Design Patterns: https://use-the-index-luke.com/

**Tools:**
- ERD visualization: Mermaid (https://mermaid.js.org/syntax/entityRelationshipDiagram.html)
- Schema diff tools: migra, sqldiff, liquibase
- Migration frameworks: Flyway, Alembic, Liquibase

**Related Skills:**
- `database-migration-generator` - Generate migration scripts from schema changes
- `database-optimization-analyzer` - Analyze and optimize existing schemas
- `data-pipeline-designer` - Design ETL pipelines for data movement
