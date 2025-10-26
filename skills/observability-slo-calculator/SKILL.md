---
name: "SRE SLO/SLI Calculator"
slug: observability-slo-calculator
description: "Define and calculate SLIs, SLOs, SLAs, and error budgets with monitoring integration for site reliability engineering."
capabilities:
  - define_slis_from_user_journey
  - calculate_slo_thresholds
  - compute_error_budgets
  - generate_monitoring_queries
  - design_alerting_policies
inputs:
  service_type:
    type: string
    description: "Service category: api, frontend, batch, streaming, storage, or database"
    required: true
  user_journey:
    type: array
    description: "Critical user paths or workflows that define service success"
    required: true
  availability_target:
    type: number
    description: "Desired availability percentage (e.g., 99.9, 99.95, 99.99)"
    required: false
  monitoring_platform:
    type: string
    description: "Target platform: prometheus, datadog, cloudwatch, newrelic, or generic"
    required: false
outputs:
  sli_definitions:
    type: json
    description: "Service Level Indicators with measurement methods and data sources"
  slo_targets:
    type: json
    description: "Service Level Objectives with thresholds and time windows"
  error_budget:
    type: json
    description: "Error budget calculations with burn rate and remaining budget"
  monitoring_queries:
    type: code
    description: "Platform-specific queries for SLI measurement"
  alerting_policy:
    type: json
    description: "Alert rules based on error budget consumption"
keywords:
  - sre
  - slo
  - sli
  - sla
  - error-budget
  - reliability
  - monitoring
  - prometheus
  - observability
  - availability
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: not_required
links:
  - https://sre.google/sre-book/service-level-objectives/
  - https://sre.google/workbook/implementing-slos/
  - https://landing.google.com/sre/workbook/chapters/alerting-on-slos/
  - https://prometheus.io/docs/practices/alerting/
---

## Purpose & When-To-Use

**Trigger conditions:**

- New service needs reliability targets and SLO definition
- Existing service requires error budget calculation and tracking
- Stakeholders demand SLA commitments with measurable guarantees
- Incident postmortem reveals need for better reliability metrics
- Service experiences reliability issues; need objective measurement
- DevOps team adopting SRE practices and needs SLO framework
- Monitoring alerts are noisy; need error budget-based alerting

**Use this skill when** you need to establish measurable reliability targets (SLIs/SLOs), calculate error budgets, and integrate with monitoring platforms to track service reliability against user expectations.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-25T21:30:36-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `service_type` is one of: `api`, `frontend`, `batch`, `streaming`, `storage`, `database`
   - `user_journey` is non-empty array describing critical user workflows
   - `availability_target` (if provided) is between 90.0 and 100.0
   - `monitoring_platform` is one of: `prometheus`, `datadog`, `cloudwatch`, `newrelic`, `generic`
3. **Source freshness**: All cited sources (Google SRE books, monitoring docs) accessed on `NOW_ET`
4. **Baseline data**: Historical service metrics available for realistic SLO calibration

**Abort conditions:**

- Service has no measurable user-facing behavior (cannot define meaningful SLIs)
- No monitoring/observability infrastructure exists (cannot measure SLIs)
- Availability target >99.999% without justification (unrealistic for most services)
- User journey description is vague or non-specific

---

## Procedure

### Tier 1 (Fast Path)

**Token budget**: T1 ≤2k tokens

**Scope**: Common 80% case - standard service with typical reliability requirements.

**Steps:**

1. **Identify service golden signals** based on `service_type` (accessed 2025-10-25T21:30:36-04:00: https://sre.google/sre-book/monitoring-distributed-systems/):
   - **API/Frontend**: Request latency, error rate, throughput
   - **Batch**: Job completion rate, processing time, data quality
   - **Streaming**: Event processing lag, throughput, data loss rate
   - **Storage**: Read/write latency, availability, durability
   - **Database**: Query latency, connection availability, replication lag

2. **Map user journey to SLIs**:
   - For each critical path in `user_journey`, identify primary golden signal
   - Define measurement window (rolling 30-day default per SRE Workbook, accessed 2025-10-25T21:30:36-04:00: https://sre.google/workbook/implementing-slos/)
   - Specify aggregation method (e.g., 99th percentile latency, error ratio)

3. **Calculate SLO thresholds**:
   - Use `availability_target` or default to 99.9% for user-facing services
   - Convert availability to error budget: `error_budget = (1 - availability_target) * measurement_window`
   - Example: 99.9% over 30 days = 43.2 minutes downtime allowed

4. **Generate basic monitoring query** (Prometheus example):
   ```promql
   # Availability SLI
   sum(rate(http_requests_total{status!~"5.."}[5m]))
   /
   sum(rate(http_requests_total[5m]))
   ```

5. **Output**: SLI definitions, SLO targets, error budget, and sample query

---

### Tier 2 (Extended Design)

**Token budget**: T2 ≤6k tokens

**Scope**: Production services requiring comprehensive SRE implementation with alerting and error budget policies.

**Steps:**

1. **Detailed SLI specification** (accessed 2025-10-25T21:30:36-04:00: https://sre.google/workbook/implementing-slos/):
   - **Availability SLI**: Ratio of successful requests to total requests
   - **Latency SLI**: Proportion of requests faster than threshold (e.g., 95% <200ms)
   - **Freshness SLI**: For batch/streaming - data staleness acceptable threshold
   - **Correctness SLI**: Data quality or functional correctness metric
   - **Throughput SLI**: Minimum requests/events processed per time window

2. **Multi-window SLO definition**:
   - **30-day rolling window**: Primary SLO for long-term reliability trends
   - **7-day rolling window**: Short-term health indicator
   - **28-day sliding window**: Monthly reporting alignment
   - Specify different thresholds per window if needed (looser short-term, stricter long-term)

3. **Error budget calculation with burn rate** (accessed 2025-10-25T21:30:36-04:00: https://landing.google.com/sre/workbook/chapters/alerting-on-slos/):
   - Calculate total error budget for each time window
   - Define burn rate thresholds:
     - **Fast burn** (2% budget consumed in 1 hour): Page immediately
     - **Moderate burn** (5% budget consumed in 6 hours): Alert on-call
     - **Slow burn** (10% budget consumed in 3 days): Ticket for review
   - Generate burn rate queries:
     ```promql
     # 1-hour burn rate (fast burn)
     (1 - (sum(rate(http_requests_total{status!~"5.."}[1h]))
           / sum(rate(http_requests_total[1h]))))
     > (14.4 * (1 - 0.999))  # 14.4x faster than budget allows
     ```

4. **Platform-specific query generation**:
   - **Prometheus**: PromQL with recording rules for SLI components
   - **Datadog**: Datadog Query Language with monitors
   - **CloudWatch**: CloudWatch Metrics Math expressions
   - **New Relic**: NRQL queries with baseline
   - Include both SLI measurement and error budget consumption queries

5. **Alerting policy design**:
   - Define alert severity levels (page, alert, ticket)
   - Map burn rate to severity:
     - **Critical**: >2% error budget consumed in 1 hour
     - **Warning**: >5% error budget consumed in 6 hours
     - **Info**: >10% error budget consumed in 3 days
   - Include alert content: current error rate, time to budget exhaustion, remediation guidance

6. **SLA derivation** (if customer-facing):
   - SLA = SLO - safety margin (typically 0.1-0.5%)
   - Example: Internal SLO 99.95%, external SLA 99.9%
   - Include consequences for SLA breach (credits, penalties)

7. **Error budget policy**:
   - Define feature freeze conditions: when error budget <10% remaining in 30-day window
   - Escalation path: SRE team → Engineering manager → VP Engineering
   - Recovery actions: halt risky deploys, prioritize reliability work

8. **Comprehensive output**:
   - Detailed SLI definitions with measurement methodology
   - Multi-window SLO targets
   - Error budget calculations with burn rates
   - Complete monitoring queries for chosen platform
   - Alerting policy with severity mapping
   - Error budget policy document
   - (Optional) SLA terms if customer-facing

**Sources cited** (accessed 2025-10-25T21:30:36-04:00):
- **Google SRE Book Ch. 4**: https://sre.google/sre-book/service-level-objectives/
- **Google SRE Workbook Ch. 2**: https://sre.google/workbook/implementing-slos/
- **Google SRE Workbook Ch. 5**: https://landing.google.com/sre/workbook/chapters/alerting-on-slos/
- **Prometheus Best Practices**: https://prometheus.io/docs/practices/alerting/

---

### Tier 3 (Deep Dive, not implemented)

**Token budget**: T3 not implemented for this skill

**Rationale**: T2 tier provides comprehensive SRE implementation with multi-window SLOs, error budget policies, and platform-specific monitoring integration. T3 would potentially cover highly specialized scenarios (custom SLI aggregation algorithms, multi-cluster federation, advanced anomaly detection) that are better handled through expert SRE consultation or custom tooling development.

---

## Decision Rules

**SLI selection criteria:**

- **Choose availability SLI** if user journey depends on service being reachable (most common)
- **Choose latency SLI** if user experience degrades with slow responses (interactive services)
- **Choose freshness SLI** if data staleness impacts user decisions (analytics, dashboards)
- **Choose correctness SLI** if wrong data is worse than no data (financial, healthcare)

**SLO threshold selection:**

- **99.9% (three nines)**: Standard for most user-facing services; 43.2 min downtime/month
- **99.95% (three nines five)**: High-value services; 21.6 min downtime/month
- **99.99% (four nines)**: Mission-critical services; 4.32 min downtime/month
- **<99.9%**: Internal tools, non-critical batch jobs
- **>99.99%**: Rarely justified; requires significant investment and architectural complexity

**Ambiguity thresholds:**

- If `user_journey` contains >10 critical paths → ask user to prioritize top 3-5
- If `availability_target` not specified → default to 99.9% for user-facing, 99.5% for internal
- If service has multiple user types (free vs paid) → ask if different SLOs needed per tier
- If no historical data available → start with conservative SLO (99.0%), iterate after 1 month

**Abort/stop conditions:**

- User cannot articulate what "service working" means → SLI definition impossible
- Requested SLO (e.g., 99.999%) exceeds architectural capabilities → warn and recommend realistic target
- Monitoring platform cannot measure proposed SLI → suggest alternative SLI or platform upgrade

---

## Output Contract

**Required fields:**

```json
{
  "sli_definitions": [
    {
      "name": "string (e.g., 'API Availability')",
      "type": "availability | latency | freshness | correctness | throughput",
      "description": "string (what this SLI measures)",
      "measurement_method": "string (how to calculate)",
      "data_source": "string (metrics endpoint, logs, traces)",
      "good_events": "string (numerator definition)",
      "total_events": "string (denominator definition)",
      "threshold": "number (for latency/freshness SLIs)",
      "unit": "string (ms, %, count)"
    }
  ],
  "slo_targets": [
    {
      "sli_name": "string (references SLI above)",
      "target": "number (e.g., 99.9)",
      "window": "string (30d, 7d, 28d)",
      "window_type": "rolling | calendar",
      "budget_threshold": "number (alert threshold %)"
    }
  ],
  "error_budget": {
    "total_minutes_30d": "number (allowable downtime)",
    "burn_rate_thresholds": {
      "critical_1h": "number (14.4x for 99.9%)",
      "warning_6h": "number (6x for 99.9%)",
      "info_3d": "number (1x for 99.9%)"
    },
    "current_consumption": "number | null (if historical data available)"
  },
  "monitoring_queries": {
    "platform": "string (prometheus, datadog, etc.)",
    "sli_queries": ["array of query strings"],
    "error_budget_queries": ["array of query strings"]
  },
  "alerting_policy": [
    {
      "severity": "critical | warning | info",
      "condition": "string (burn rate threshold)",
      "notification": "string (page, email, ticket)",
      "duration": "string (alert evaluation window)"
    }
  ]
}
```

**Optional fields:**

- `sla_terms`: Customer-facing SLA commitments (if applicable)
- `error_budget_policy`: Freeze/escalation procedures
- `dashboard_config`: Monitoring dashboard layout recommendations

**Validation:**

- All SLI names must be unique
- SLO targets must reference defined SLIs
- Error budget calculations must align with SLO targets
- Monitoring queries must be syntactically valid for target platform

---

## Examples

**Input:**

```json
{
  "service_type": "api",
  "user_journey": [
    "User searches products",
    "User adds item to cart",
    "User completes checkout"
  ],
  "availability_target": 99.9,
  "monitoring_platform": "prometheus"
}
```

**Output (abbreviated):**

```json
{
  "sli_definitions": [
    {
      "name": "API Availability",
      "type": "availability",
      "measurement_method": "ratio of successful HTTP responses (2xx/3xx) to total requests",
      "good_events": "http_requests_total{status=~\"2..|3..\"}",
      "total_events": "http_requests_total"
    }
  ],
  "slo_targets": [{"sli_name": "API Availability", "target": 99.9, "window": "30d"}],
  "error_budget": {"total_minutes_30d": 43.2},
  "monitoring_queries": {
    "platform": "prometheus",
    "sli_queries": [
      "sum(rate(http_requests_total{status=~\"2..|3..\"}[5m])) / sum(rate(http_requests_total[5m]))"
    ]
  }
}
```

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens for simple SLI/SLO definition with basic monitoring
- **T2**: ≤6k tokens for comprehensive SRE implementation with error budget policies

**Safety requirements:**

- Validate SLO targets are achievable given current architecture
- Warn if SLO >99.99% (requires significant investment)
- Ensure error budget policies prevent excessive risk-taking

**Auditability:**

- All SLI definitions include explicit measurement methodology
- Monitoring queries are reproducible and version-controlled
- Error budget calculations show math and assumptions

**Determinism:**

- Same inputs produce same SLI definitions
- Error budget formulas are consistent with SRE literature
- Burn rate thresholds use standard multipliers (1x, 6x, 14.4x)

---

## Resources

**Primary sources:**

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- Google SRE Workbook: https://sre.google/workbook/table-of-contents/
- Prometheus Documentation: https://prometheus.io/docs/
- Datadog SLO Monitoring: https://docs.datadoghq.com/monitors/service_level_objectives/

**Reference implementations:**

- [Prometheus SLO Recording Rules](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-slo-exporter) (accessed 2025-10-25T21:30:36-04:00)
- [Sloth SLO Generator](https://github.com/slok/sloth) (accessed 2025-10-25T21:30:36-04:00)
- [OpenSLO Specification](https://github.com/OpenSLO/OpenSLO) (accessed 2025-10-25T21:30:36-04:00)

**Additional reading:**

- The Art of SLOs (book): https://www.alex-hidalgo.com/the-art-of-slos
- SLO Workshop: https://www.usenix.org/conference/srecon19americas/presentation/fong-jones
