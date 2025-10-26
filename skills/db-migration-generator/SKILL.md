---
name: "Database Migration Script Generator"
slug: "db-migration-generator"
description: "Generate database migration scripts for Liquibase, Flyway, Alembic with rollback safety, data preservation, and zero-downtime patterns"
capabilities:
  - Schema migrations (DDL: tables, columns, indexes, constraints)
  - Data migrations with backfill and transformation logic
  - Zero-downtime deployment patterns (expand/contract, online DDL)
  - Rollback script generation with safety validation
  - Migration testing and validation scripts
  - Database-specific optimization (PostgreSQL, MySQL, SQL Server, Oracle)
inputs:
  - migration_tool: "liquibase | flyway | alembic (string)"
  - database: "postgresql | mysql | sqlserver | oracle (string)"
  - migration_type: "schema | data | hybrid (string)"
  - downtime_allowed: "true | false (boolean)"
  - migration_description: "Human-readable description of migration intent (string)"
outputs:
  - migration_script: "Forward migration code in tool-specific format (string)"
  - rollback_script: "Reverse migration code with safety checks (string)"
  - validation_tests: "Test queries to validate migration success (array)"
  - deployment_guide: "Step-by-step rollout instructions (string)"
keywords:
  - database-migration
  - liquibase
  - flyway
  - alembic
  - schema-migration
  - zero-downtime
  - rollback
  - ddl
  - postgresql
  - mysql
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://docs.liquibase.com/
  - https://flywaydb.org/documentation/
  - https://alembic.sqlalchemy.org/
  - https://www.postgresql.org/docs/current/sql-altertable.html
  - https://dev.mysql.com/doc/refman/8.0/en/online-ddl.html
---

## Purpose & When-To-Use

**Trigger conditions:**
- Evolving database schema for application updates
- Performing data migrations with business logic transformations
- Implementing zero-downtime deployments requiring schema changes
- Standardizing migration workflows across teams
- Migrating between database versions or platforms
- Adding indexes, constraints, or partitioning to existing tables

**Not for:**
- Initial database schema creation (use ORM models or DDL scripts)
- One-off data fixes (use direct SQL with transaction safety)
- Database backups or recovery operations
- Cross-database data replication (use ETL tools)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `migration_tool` must be one of: liquibase, flyway, alembic
- `database` must be one of: postgresql, mysql, sqlserver, oracle
- `migration_type` must be one of: schema, data, hybrid
- `downtime_allowed` must be boolean (true/false)
- `migration_description` must be non-empty and descriptive

**Source freshness:**
- Liquibase docs must be accessible [accessed 2025-10-26T03:51:54-04:00](https://docs.liquibase.com/change-types/home.html)
- Flyway docs must be accessible [accessed 2025-10-26T03:51:54-04:00](https://flywaydb.org/documentation/concepts/migrations)
- Alembic docs must be accessible [accessed 2025-10-26T03:51:54-04:00](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- PostgreSQL online DDL docs must be accessible [accessed 2025-10-26T03:51:54-04:00](https://www.postgresql.org/docs/current/sql-altertable.html)
- MySQL online DDL docs must be accessible [accessed 2025-10-26T03:51:54-04:00](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl.html)

---

## Procedure

### T1: Basic Schema Migration (≤2k tokens)

**Fast path for simple DDL changes:**

1. **Schema Change Identification**
   - Add/drop columns (with default values to avoid table rewrites)
   - Create/drop tables
   - Add/drop simple indexes (non-unique, single column)
   - Add/drop NOT NULL constraints (with validation)

2. **Tool-Specific Migration Format**

   **Liquibase (XML/YAML)** [accessed 2025-10-26T03:51:54-04:00](https://docs.liquibase.com/change-types/add-column.html)
   ```xml
   <changeSet id="add-email-column" author="migration-generator">
     <addColumn tableName="users">
       <column name="email" type="VARCHAR(255)"/>
     </addColumn>
     <rollback>
       <dropColumn tableName="users" columnName="email"/>
     </rollback>
   </changeSet>
   ```

   **Flyway (SQL)** [accessed 2025-10-26T03:51:54-04:00](https://flywaydb.org/documentation/concepts/migrations#sql-based-migrations)
   ```sql
   -- V1__add_email_column.sql
   ALTER TABLE users ADD COLUMN email VARCHAR(255);
   ```

   **Alembic (Python)** [accessed 2025-10-26T03:51:54-04:00](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.add_column)
   ```python
   def upgrade():
       op.add_column('users', sa.Column('email', sa.String(255)))

   def downgrade():
       op.drop_column('users', 'email')
   ```

3. **Basic Rollback Script**
   - Generate inverse operation for each forward change
   - Add rollback validation comments
   - Include manual rollback steps if auto-rollback unsafe

**Decision:** If simple schema change without data → STOP at T1; otherwise proceed to T2.

---

### T2: Data Migrations with Rollback (≤6k tokens)

**Extended migrations with data transformations:**

1. **Data Migration Patterns** [accessed 2025-10-26T03:51:54-04:00](https://docs.liquibase.com/change-types/update.html)

   **Backfill Existing Data**
   ```python
   # Alembic: Backfill default values for new column
   def upgrade():
       op.add_column('users', sa.Column('status', sa.String(20), nullable=True))
       # Backfill existing rows
       op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")
       # Make NOT NULL after backfill
       op.alter_column('users', 'status', nullable=False)
   ```

   **Data Transformation**
   ```python
   # Alembic: Split full_name into first_name and last_name
   def upgrade():
       op.add_column('users', sa.Column('first_name', sa.String(100)))
       op.add_column('users', sa.Column('last_name', sa.String(100)))
       # Transform data
       connection = op.get_bind()
       users = connection.execute("SELECT id, full_name FROM users").fetchall()
       for user_id, full_name in users:
           parts = full_name.split(' ', 1)
           first = parts[0]
           last = parts[1] if len(parts) > 1 else ''
           connection.execute(
               "UPDATE users SET first_name = %s, last_name = %s WHERE id = %s",
               (first, last, user_id)
           )
       op.drop_column('users', 'full_name')
   ```

2. **Rollback Safety Patterns**
   - **Idempotency:** Ensure migrations can run multiple times safely
   - **Checkpointing:** Add validation queries before destructive operations
   - **Backup Triggers:** Create temporary backup tables for data migrations
   - **Dry-Run Mode:** Include commented-out SELECT statements to preview changes

3. **Validation Tests** [accessed 2025-10-26T03:51:54-04:00](https://flywaydb.org/documentation/concepts/callbacks)
   ```sql
   -- Post-migration validation
   SELECT COUNT(*) FROM users WHERE email IS NULL; -- Should be 0
   SELECT COUNT(*) FROM users WHERE status NOT IN ('active', 'inactive'); -- Should be 0
   ```

4. **Database-Specific Considerations**

   **PostgreSQL** [accessed 2025-10-26T03:51:54-04:00](https://www.postgresql.org/docs/current/ddl-alter.html)
   - Use `ALTER TABLE ... SET NOT NULL` with `CHECK` constraint first
   - Prefer `CONCURRENTLY` for index creation (zero-downtime)
   - Use `pg_stat_progress_create_index` to monitor long operations

   **MySQL** [accessed 2025-10-26T03:51:54-04:00](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)
   - Check online DDL support: `ALGORITHM=INPLACE, LOCK=NONE`
   - Avoid `ALTER TABLE` that requires table copy (pre-8.0)
   - Use `pt-online-schema-change` for large tables (Percona Toolkit)

   **SQL Server**
   - Use `WITH (ONLINE = ON)` for index operations
   - Leverage `SSMS` execution plan analysis
   - Consider `SCHEMA_ONLY` copies for large data migrations

---

### T3: Zero-Downtime Patterns (≤12k tokens)

**Advanced patterns for production systems:**

1. **Expand/Contract Pattern** [accessed 2025-10-26T03:51:54-04:00](https://www.liquibase.com/blog/expand-contract-pattern)

   **Phase 1: Expand (Add new schema)**
   ```python
   # Migration 001: Add new column, keep old column
   def upgrade():
       op.add_column('users', sa.Column('email_new', sa.String(255)))
       # Trigger to sync old → new during transition
       op.execute("""
           CREATE TRIGGER sync_email_new
           BEFORE UPDATE ON users
           FOR EACH ROW
           BEGIN
               SET NEW.email_new = NEW.email;
           END;
       """)
   ```

   **Phase 2: Migrate Data**
   ```python
   # Migration 002: Backfill new column
   def upgrade():
       op.execute("UPDATE users SET email_new = email WHERE email_new IS NULL")
   ```

   **Phase 3: Contract (Remove old schema)**
   ```python
   # Migration 003: Drop old column (after application updated)
   def upgrade():
       op.execute("DROP TRIGGER IF EXISTS sync_email_new")
       op.drop_column('users', 'email')
       op.alter_column('users', 'email_new', new_column_name='email')
   ```

2. **Online Index Creation** [accessed 2025-10-26T03:51:54-04:00](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)

   **PostgreSQL CONCURRENTLY**
   ```sql
   -- Flyway: V5__add_email_index.sql
   CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

   -- Validation
   SELECT schemaname, tablename, indexname, indexdef
   FROM pg_indexes
   WHERE indexname = 'idx_users_email';
   ```

   **MySQL Online DDL**
   ```sql
   -- Flyway: V6__add_composite_index.sql
   ALTER TABLE users
   ADD INDEX idx_email_status (email, status)
   ALGORITHM=INPLACE, LOCK=NONE;
   ```

3. **Shadow Table Pattern** (for complex transformations)
   ```python
   # Migration 010: Create shadow table with new schema
   def upgrade():
       op.create_table(
           'users_new',
           sa.Column('id', sa.Integer, primary_key=True),
           sa.Column('email', sa.String(255), nullable=False, index=True),
           sa.Column('status', sa.String(20), nullable=False)
       )
       # Stream data from old → new table
       op.execute("""
           INSERT INTO users_new (id, email, status)
           SELECT id, email, COALESCE(status, 'active')
           FROM users
       """)
       # Atomic rename (downtime: milliseconds)
       op.rename_table('users', 'users_old')
       op.rename_table('users_new', 'users')
   ```

4. **Deployment Guide Template**
   ```markdown
   ## Deployment Steps

   ### Pre-Migration
   1. Verify database backup completed (last 24h)
   2. Check application connection pool settings (timeout ≥ 30s)
   3. Review query performance baseline (pg_stat_statements)

   ### Migration Execution
   1. Run migration in transaction (if supported)
   2. Monitor lock waits: `SELECT * FROM pg_locks WHERE NOT granted`
   3. Validate row counts: `SELECT COUNT(*) FROM users`

   ### Post-Migration
   1. Run ANALYZE to update statistics
   2. Verify application logs (no constraint violations)
   3. Monitor query performance (compare to baseline)

   ### Rollback Procedure (if needed)
   1. Stop application traffic (or use feature flag)
   2. Run rollback script: `flyway undo` or `alembic downgrade -1`
   3. Verify data integrity: `SELECT * FROM users LIMIT 10`
   4. Restore from backup if rollback fails
   ```

5. **Blue-Green Database Migrations** [accessed 2025-10-26T03:51:54-04:00](https://martinfowler.com/bliki/BlueGreenDeployment.html)
   - Duplicate database instance (Blue = old schema, Green = new schema)
   - Run migrations on Green instance
   - Dual-write pattern during transition (application writes to both)
   - Cutover: Update connection string to Green
   - Validation period: Keep Blue online for 24-48h

---

## Decision Rules

**Migration Tool Selection:**
- **Liquibase:** Best for multi-database support, XML/YAML declarative changes, complex rollback
- **Flyway:** Best for SQL-first teams, simple versioning, Java/Spring ecosystems
- **Alembic:** Best for Python applications using SQLAlchemy, programmatic migrations

**Migration Strategy by Downtime Allowance:**
- **downtime_allowed = true:** Use direct ALTER TABLE, faster execution, simpler scripts
- **downtime_allowed = false:** Use expand/contract, CONCURRENTLY, shadow tables, longer timeline

**Database-Specific Patterns:**
- **PostgreSQL:** Prefer CONCURRENTLY for indexes, use CHECK constraints before NOT NULL
- **MySQL:** Validate ALGORITHM=INPLACE support, use pt-online-schema-change for InnoDB
- **SQL Server:** Use ONLINE=ON, consider columnstore indexes for analytics workloads
- **Oracle:** Use Oracle Data Redefinition (DBMS_REDEFINITION) for zero-downtime

**Abort Conditions:**
- Invalid tool/database combination → error "Tool X does not support database Y"
- Destructive operation without rollback → error "Cannot generate safe rollback for DROP TABLE"
- Zero-downtime requested for non-supported operation → error "Zero-downtime not possible for operation X"

**Data Preservation Checks:**
- Dropping columns: Warn if column contains non-NULL data
- Changing types: Validate data fits in new type (VARCHAR(50) → VARCHAR(20))
- Adding NOT NULL: Require default value or backfill strategy

---

## Output Contract

**Schema (JSON):**

```json
{
  "migration_tool": "liquibase | flyway | alembic",
  "database": "postgresql | mysql | sqlserver | oracle",
  "migration_type": "schema | data | hybrid",
  "downtime_allowed": "boolean",
  "migration_script": {
    "filename": "string (e.g., V5__add_email_column.sql)",
    "content": "string (tool-specific migration code)"
  },
  "rollback_script": {
    "filename": "string (e.g., U5__undo_email_column.sql)",
    "content": "string (inverse migration code)",
    "manual_steps": ["string (if auto-rollback unsafe)"]
  },
  "validation_tests": [
    {
      "description": "string",
      "query": "string (SQL validation query)",
      "expected_result": "string"
    }
  ],
  "deployment_guide": {
    "pre_migration_steps": ["string"],
    "execution_steps": ["string"],
    "post_migration_steps": ["string"],
    "rollback_procedure": ["string"],
    "estimated_duration": "string (e.g., '5 minutes', '2 hours')"
  },
  "warnings": ["string (potential issues or breaking changes)"],
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- `migration_tool`, `database`, `migration_type`, `downtime_allowed`, `migration_script`, `rollback_script`, `validation_tests`, `deployment_guide`, `timestamp`

**Safety Guarantees:**
- All DDL changes must have explicit rollback (or manual rollback steps)
- Data migrations must include row count validation
- Zero-downtime migrations must specify lock duration estimates

---

## Examples

**Example 1: Simple Column Addition (Alembic + PostgreSQL)**

```python
"""Add email column to users table with NOT NULL constraint

Revision ID: a1b2c3d4e5f6
Revises: previous_revision
Create Date: 2025-10-26 03:51:54.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add column as nullable first
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

    # Backfill with placeholder (application will update)
    op.execute("UPDATE users SET email = CONCAT('user', id, '@example.com') WHERE email IS NULL")

    # Add NOT NULL constraint
    op.alter_column('users', 'email', nullable=False)

    # Add index for performance
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
    op.drop_column('users', 'email')
```

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (simple schema change, basic rollback)
- **T2:** ≤6k tokens (data migration, validation tests, database-specific optimizations)
- **T3:** ≤12k tokens (zero-downtime patterns, deployment guide, multi-phase migrations)

**Safety:**
- No plaintext credentials in migration scripts (use environment variables)
- All destructive operations require explicit confirmation comments
- Rollback scripts tested against sample data

**Auditability:**
- Migration IDs/versions follow tool conventions (Flyway: V1__description.sql, Alembic: revision IDs)
- All migrations include author, timestamp, and description
- Database-specific syntax validated against official documentation

**Determinism:**
- Same inputs → identical migration scripts
- Idempotent migrations (can run multiple times safely)
- Predictable rollback behavior

**Performance:**
- Estimate lock duration for DDL operations
- Include EXPLAIN ANALYZE for data migrations affecting >10k rows
- Recommend batch size for large table transformations (e.g., 1000 rows/batch)

---

## Resources

**Official Documentation (accessed 2025-10-26T03:51:54-04:00):**
1. [Liquibase Change Types](https://docs.liquibase.com/change-types/home.html) - DDL/DML operations
2. [Flyway SQL Migrations](https://flywaydb.org/documentation/concepts/migrations) - Versioned migrations
3. [Alembic Operations Reference](https://alembic.sqlalchemy.org/en/latest/ops.html) - Python migration API
4. [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) - DDL syntax
5. [MySQL Online DDL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl.html) - Zero-downtime operations
6. [SQL Server Online Index Operations](https://learn.microsoft.com/en-us/sql/relational-databases/indexes/perform-index-operations-online) - Online DDL

**Migration Patterns:**
- [Expand/Contract Pattern](https://www.liquibase.com/blog/expand-contract-pattern) - Zero-downtime schema evolution
- [Blue-Green Deployments](https://martinfowler.com/bliki/BlueGreenDeployment.html) - Database migration strategies
- [Database Refactoring](https://databaserefactoring.com/) - Catalog of database refactoring patterns

**Best Practices:**
- [Flyway Best Practices](https://flywaydb.org/documentation/usage/bestpractices) - Migration versioning and naming
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) - Auto-generate vs manual migrations
- [PostgreSQL Wiki: Don't Do This](https://wiki.postgresql.org/wiki/Don%27t_Do_This) - Anti-patterns to avoid

**Tool Comparisons:**
- [Liquibase vs Flyway](https://www.liquibase.com/liquibase-vs-flyway) - Feature comparison
- [Schema Migration Tools Comparison](https://db-migrations.github.io/) - Multi-tool benchmarks
