---
name: Data Engineering Pipeline Designer
slug: data-engineering-pipeline-designer
description: Design data pipelines with quality checks, orchestration, and governance using modern data stack patterns for robust ELT/ETL workflows.
capabilities:
  - Design DAGs for batch and streaming pipelines
  - Embed data quality checks with Great Expectations
  - Configure Airflow orchestration best practices
  - Model transformations with dbt patterns
  - Implement Kafka streaming architectures
  - Define data lineage and governance controls
inputs:
  - pipeline_type: batch | streaming | hybrid
  - source_systems: array of data sources (databases, APIs, files, streams)
  - transformation_requirements: business logic, aggregations, joins
  - quality_requirements: data validation rules, SLAs, monitoring needs
  - orchestration_platform: Airflow | Prefect | Dagster | custom
  - target_systems: data warehouse, lake, lakehouse destinations
outputs:
  - pipeline_architecture: JSON schema with components and flow
  - dag_template: orchestration code (Airflow DAG, dbt project)
  - quality_checks: Great Expectations suite configuration
  - monitoring_config: alerts, SLAs, data lineage tracking
  - implementation_guide: step-by-step deployment instructions
keywords:
  - data-engineering
  - airflow
  - dbt
  - great-expectations
  - kafka
  - data-quality
  - orchestration
  - ETL
  - ELT
  - data-pipeline
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: No secrets or PII in examples; use environment variables for credentials
links:
  - https://airflow.apache.org/docs/
  - https://docs.getdbt.com/
  - https://greatexpectations.io/
  - https://kafka.apache.org/documentation/
---

## Purpose & When-To-Use

**Trigger this skill when:**

- Designing a new data pipeline (batch, streaming, or hybrid)
- Migrating from ETL to modern ELT patterns
- Implementing data quality checks in existing pipelines
- Troubleshooting data quality issues or pipeline failures
- Establishing data orchestration best practices
- Configuring real-time streaming data architectures
- Setting up data lineage and governance controls

**Do NOT use for:**

- Simple one-off data exports (use SQL directly)
- BI tool configuration (separate concern)
- ML model training pipelines (use mlops-lifecycle-manager skill)
- Database schema design only (use database-optimization-analyzer)

## Pre-Checks

**Time normalization:**

- Compute `NOW_ET` = 2025-10-25T21:30:36-04:00 (NIST/time.gov, America/New_York)

**Input validation:**

1. `pipeline_type` must be one of: batch, streaming, hybrid
2. `source_systems` must contain at least one valid source
3. `transformation_requirements` must specify business logic or be empty for raw ingestion
4. `quality_requirements` must define at least one validation rule or SLA
5. `orchestration_platform` must be specified (default: Airflow if omitted)
6. `target_systems` must contain at least one destination

**Abort conditions:**

- If source and target are identical (no transformation needed)
- If pipeline_type=streaming but no stream source specified
- If quality_requirements reference non-existent fields
- If orchestration_platform is unsupported (emit TODO list)

## Procedure

### Tier 1 (≤2k tokens): Quick Pipeline Design

**Use when:** 80% of cases; standard batch pipeline with known patterns

**Steps:**

1. **Analyze inputs** and classify pipeline pattern:
   - Batch: scheduled ETL/ELT (daily, hourly)
   - Streaming: real-time event processing (Kafka, Kinesis)
   - Hybrid: batch + streaming (lambda architecture)

2. **Select orchestration approach:**
   - Airflow DAG for batch/hybrid (de facto standard, accessed 2025-10-25T21:30:36-04:00: https://www.astronomer.io/airflow/)
   - Kafka + ksqlDB for streaming (accessed 2025-10-25T21:30:36-04:00: https://kafka.apache.org/documentation/)
   - dbt for transformation layer (accessed 2025-10-25T21:30:36-04:00: https://docs.getdbt.com/)

3. **Generate pipeline architecture JSON:**
   ```json
   {
     "pipeline_id": "<slug>",
     "type": "batch|streaming|hybrid",
     "orchestration": "airflow|kafka",
     "layers": {
       "ingestion": {"sources": [], "method": "full|incremental"},
       "transformation": {"tool": "dbt", "models": []},
       "quality": {"framework": "great_expectations", "checkpoints": []},
       "storage": {"targets": [], "format": "parquet|delta"}
     },
     "schedule": "cron|event-driven"
   }
   ```

4. **Output quick-start template:**
   - Airflow DAG skeleton with TaskGroups
   - dbt project structure (staging → intermediate → marts)
   - Great Expectations basic suite (nullity, uniqueness, ranges)

5. **Define monitoring:**
   - SLA alerts (Airflow SLAs or custom)
   - Data quality thresholds (fail fast on critical checks)
   - Lineage tracking (dbt docs, OpenLineage)

**Token budget: T1 ≤ 2000 tokens**

### Tier 2 (≤6k tokens): Production-Ready Pipeline with Quality Gates

**Use when:** Production deployment, complex transformations, strict SLAs

**Prerequisites:** T1 completed OR inputs indicate production requirements

**Steps:**

1. **Deep-dive on data quality** (accessed 2025-10-25T21:30:36-04:00: https://greatexpectations.io/):
   - Profiling: auto-generate Expectations from sample data
   - Critical validations: PK uniqueness, FK integrity, business rules
   - Checkpoint strategy: pre-ingestion, post-transformation, pre-load
   - Action on failure: block pipeline, alert, quarantine bad records

2. **Optimize Airflow DAG design** (accessed 2025-10-25T21:30:36-04:00: https://medium.com/@datasmiles/mastering-apache-airflow-myessential-best-practices-for-robust-data-orchestration-095460505843):
   - Idempotent tasks: same input → same output (critical for backfills)
   - Atomic tasks: one task = one action (fine-grained retry)
   - Dynamic task generation: use TaskGroups for parallel sources
   - XCom for state passing: avoid large payloads (use external state store)
   - Connection management: use Airflow Connections, never hardcode credentials
   - Resource optimization: pools, queues, executor type (LocalExecutor vs CeleryExecutor)

3. **Implement dbt best practices** (accessed 2025-10-25T21:30:36-04:00: https://www.getdbt.com/blog/data-transformation-best-practices):
   - Layer pattern: staging (raw + minimal cleaning) → intermediate (business logic) → marts (denormalized for analytics)
   - One model = one logical transformation (no mega-models with 50 joins)
   - Materialization strategy:
     - Views: lightweight, always fresh, slow queries
     - Tables: fast queries, stale until rebuild
     - Incremental: append-only or merge, handle late-arriving data
   - Testing: not_null, unique, accepted_values, relationships
   - Documentation: schema.yml with descriptions, dbt docs generate
   - Macros for DRY: reusable SQL snippets (date ranges, common filters)

4. **Configure streaming (if applicable):**
   - Kafka architecture: producers → topics (partitioned) → consumers (accessed 2025-10-25T21:30:36-04:00: https://kafka.apache.org/)
   - Partition strategy: by key (user_id, order_id) for ordering guarantees
   - Consumer groups: parallel processing, fault tolerance
   - Schema registry: Avro/Protobuf for schema evolution (accessed 2025-10-25T21:30:36-04:00: https://www.confluent.io/blog/streaming-data-pipeline-with-apache-kafka-and-ksqldb/)
   - ksqlDB for stream transformations: joins, aggregations, windowing
   - Exactly-once semantics: idempotent producers + transactional consumers

5. **Data lineage and governance:**
   - OpenLineage integration: capture lineage from Airflow and dbt
   - Data catalog: tag PII, set retention policies
   - RBAC: column-level access controls in warehouse
   - Audit logs: who accessed what data, when

6. **Monitoring and alerting:**
   - Pipeline health: Airflow UI, metrics to Prometheus/Datadog
   - Data quality dashboards: Great Expectations Data Docs
   - SLA violations: PagerDuty/Slack integration
   - Cost tracking: warehouse query costs, Airflow compute

**Token budget: T2 ≤ 6000 tokens**

### Tier 3 (≤12k tokens): Advanced Patterns and Optimization

**Use when:** Handling PB-scale data, multi-region, complex event-driven patterns

**Note:** This skill is scoped to T2. For T3 scenarios:

- **TODO:** Consult mlops-lifecycle-manager for ML feature pipelines
- **TODO:** Consult database-optimization-analyzer for warehouse tuning
- **TODO:** Consult cloud-native-deployment-orchestrator for Kubernetes-based orchestration

**Not implemented in v1.0.0.**

## Decision Rules

**When to choose batch vs streaming:**

- Batch if: data arrives in bulk, latency tolerance >1 hour, simpler to maintain
- Streaming if: sub-second latency required, event-driven triggers, real-time analytics
- Hybrid if: both real-time dashboards AND overnight batch reporting needed

**When to use incremental vs full refresh:**

- Full refresh: small tables (<10M rows), idempotent, no history tracking
- Incremental: large tables (>100M rows), append-only or merge strategy, track watermarks

**When to fail vs warn on data quality issues:**

- Fail (block pipeline): critical business rules (revenue calculations, PK violations)
- Warn (continue with alert): non-critical outliers, minor formatting issues
- Quarantine: isolate bad records, process good records, manual review queue

**Orchestration platform selection:**

- Airflow: if need Python flexibility, complex dependencies, mature ecosystem
- Prefect: if want modern UI, easier local development, Pythonic
- Dagster: if want software-defined assets, testing-first approach
- Cloud-native (Step Functions, Cloud Composer): if locked into cloud vendor

**Abort conditions:**

- No clear transformation logic defined → emit TODO: "Specify business rules"
- Source schema unknown → emit TODO: "Profile source data first"
- Target warehouse not provisioned → emit TODO: "Setup destination infra"

## Output Contract

**Required fields:**

```json
{
  "pipeline_architecture": {
    "pipeline_id": "string (slug format)",
    "type": "batch|streaming|hybrid",
    "orchestration": {
      "platform": "airflow|prefect|dagster|kafka",
      "schedule": "cron expression | event-driven",
      "parallelism": "integer (max concurrent tasks)"
    },
    "layers": {
      "ingestion": {
        "sources": ["array of source configs"],
        "method": "full|incremental",
        "connector": "native|fivetran|airbyte|custom"
      },
      "transformation": {
        "tool": "dbt|spark|custom",
        "models": ["array of model names"],
        "materialization": "view|table|incremental"
      },
      "quality": {
        "framework": "great_expectations|dbt_tests|custom",
        "checkpoints": ["array of checkpoint configs"],
        "action_on_failure": "block|warn|quarantine"
      },
      "storage": {
        "targets": ["array of target configs"],
        "format": "parquet|delta|iceberg|avro"
      }
    },
    "monitoring": {
      "slas": ["array of SLA definitions"],
      "alerts": ["array of alert configs"],
      "lineage": "openlineage|datahub|custom"
    }
  },
  "dag_template": "string (executable code or path to resource)",
  "quality_checks": "string (Great Expectations suite YAML or dbt test SQL)",
  "monitoring_config": "string (alert rules, dashboard JSON)",
  "implementation_guide": "array of step-by-step instructions"
}
```

**Optional fields:**

- `cost_estimate`: projected monthly cost (warehouse + orchestration + storage)
- `performance_benchmarks`: expected throughput, latency targets
- `rollback_plan`: how to revert if pipeline fails in production

**Validation:**

- `pipeline_id` must be unique, slug format (lowercase, hyphens)
- `schedule` must be valid cron OR event trigger definition
- `sources` and `targets` must have valid connection info (no credentials in output)
- All referenced `models` must exist in transformation layer

## Examples

**Example 1: Batch ELT Pipeline (E-commerce Orders)**

```yaml
# Input
pipeline_type: batch
source_systems: [{type: postgres, name: orders_db, tables: [orders, customers]}]
transformation_requirements: [Join orders+customers, Calculate daily revenue]
quality_requirements: [order_id unique, order_total > 0]
orchestration_platform: airflow
target_systems: [{type: snowflake, schema: analytics}]
schedule: 0 2 * * *

# Output (abbreviated)
pipeline_architecture:
  pipeline_id: ecommerce-orders-elt
  type: batch
  orchestration: {platform: airflow, schedule: "0 2 * * *"}
  layers:
    ingestion:
      sources: [orders_db.orders, orders_db.customers]
      method: incremental
    transformation:
      tool: dbt
      models: [stg_orders, int_order_metrics, fct_daily_revenue]
    quality:
      framework: great_expectations
      checkpoints: [staging_check, marts_check]
```

## Quality Gates

**Token budgets (enforced):**

- T1: ≤2000 tokens (quick design, standard patterns)
- T2: ≤6000 tokens (production-ready, quality gates, monitoring)
- T3: Not implemented in v1.0.0

**Safety checks:**

- Never emit credentials or API keys in outputs
- Always use environment variables or secret managers (Airflow Connections, AWS Secrets Manager)
- Validate that quality checks don't reference PII columns without encryption

**Auditability:**

- All architecture decisions logged in `implementation_guide`
- Source links with access dates for claims (Airflow docs, dbt docs, etc.)
- Version transformations with dbt git tags or Airflow DAG versions

**Determinism:**

- Same inputs → same pipeline architecture JSON
- Idempotent DAG designs (safe to re-run)
- Incremental models handle late-arriving data gracefully

## Resources

**Official documentation (accessed 2025-10-25T21:30:36-04:00):**

- Apache Airflow: https://airflow.apache.org/docs/
- dbt (data build tool): https://docs.getdbt.com/
- Great Expectations: https://greatexpectations.io/
- Apache Kafka: https://kafka.apache.org/documentation/

**Best practices guides:**

- Airflow orchestration patterns: https://www.astronomer.io/airflow/
- dbt transformation best practices: https://www.getdbt.com/blog/data-transformation-best-practices
- Modern data stack architecture: https://www.getdbt.com/blog/data-integration

**Templates and examples:**

- Located in `/skills/data-engineering-pipeline-designer/resources/`
- `airflow-dag-template.py`: Production-ready DAG with TaskGroups and SLAs
- `dbt-project-structure.yml`: Layered dbt project (staging → marts)
- `great-expectations-suite.yml`: Common data quality checks
- `kafka-streaming-config.json`: Schema registry + consumer group setup

**Related skills:**

- `database-optimization-analyzer`: For warehouse query tuning and indexing
- `devops-pipeline-architect`: For CI/CD of pipeline code
- `cloud-native-deployment-orchestrator`: For Kubernetes-based Airflow deployments
