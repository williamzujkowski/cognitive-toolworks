---
name: "Service Level Objective Validator"
slug: slo-validator
description: "Validate SLO definitions against actual metrics, generate alerting rules, and design error budget policies with burn rate calculations."
capabilities:
  - validate_slo_against_metrics
  - calculate_error_budget_burn_rate
  - generate_multi_window_alerts
  - audit_slo_compliance
  - generate_slo_dashboards
inputs:
  slo_definition:
    type: json
    description: "SLO specification (YAML/JSON) with targets, windows, and SLI queries"
    required: true
  metrics_source:
    type: string
    description: "Metrics platform: prometheus, cloudwatch, datadog, newrelic"
    required: true
  time_window:
    type: string
    description: "Validation period: 7d, 28d, 90d (default: 28d)"
    required: false
  error_budget_policy:
    type: string
    description: "Policy strictness: strict, moderate, flexible (default: moderate)"
    required: false
outputs:
  validation_report:
    type: json
    description: "SLO compliance vs actual metrics with breach timeline"
  alerting_rules:
    type: code
    description: "Platform-specific alert definitions (Prometheus rules, CloudWatch alarms)"
  error_budget_status:
    type: json
    description: "Current burn rate, remaining budget, time-to-exhaustion"
  dashboard_config:
    type: json
    description: "Grafana/CloudWatch dashboard configuration for SLO tracking"
keywords:
  - slo
  - validation
  - error-budget
  - burn-rate
  - alerting
  - prometheus
  - sre
  - observability
  - compliance
  - monitoring
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: not_required
links:
  - https://sre.google/workbook/implementing-slos/
  - https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
  - https://github.com/slok/sloth
  - https://docs.datadoghq.com/monitors/service_level_objectives/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Existing SLO definition needs validation against actual service performance
- SRE team requires automated alerting on error budget consumption
- Compliance audit demands proof of SLO adherence over time period
- Incident postmortem reveals SLO was breached but no alerts fired
- Service migration requires SLO re-validation with new infrastructure
- Multi-window burn rate alerts needed (fast/slow burn detection)
- Dashboard generation needed for executive SLO reporting

**Use this skill when** you have an existing SLO definition and need to validate it against real metrics, generate appropriate alerting rules with burn rate thresholds, and create compliance reports or monitoring dashboards.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T03:51:54-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `slo_definition` contains `target`, `window`, and `sli_query` fields
   - `metrics_source` is one of: `prometheus`, `cloudwatch`, `datadog`, `newrelic`
   - `time_window` is valid duration: `7d`, `28d`, or `90d` (default: `28d`)
   - `error_budget_policy` is one of: `strict`, `moderate`, `flexible` (default: `moderate`)
3. **Source freshness**: All cited sources (Google SRE Workbook, Prometheus docs, Sloth) accessed on `NOW_ET`
4. **Metrics availability**: Target metrics platform is accessible and contains historical data for `time_window`

**Abort conditions:**

- SLO definition missing required fields (`target`, `window`, `sli_query`)
- Metrics source unavailable or lacks data for validation period
- SLI query syntax invalid for specified metrics platform
- Historical data gap >10% of validation window (insufficient for accurate validation)

---

## Procedure

### Tier 1 (Fast Path)

**Token budget**: T1 ≤2k tokens

**Scope**: Basic SLO validation for common availability/latency targets with simple alerting.

**Steps:**

1. **Parse SLO definition**:
   - Extract `target` (e.g., 99.9%), `window` (e.g., 30d), `sli_query` (metrics query)
   - Validate query syntax for `metrics_source` platform
   - Calculate error budget: `error_budget = (1 - target) * window`
   - Example: 99.9% over 30d = 43.2 minutes allowed downtime

2. **Query metrics platform** (accessed 2025-10-26T03:51:54-04:00: https://prometheus.io/docs/prometheus/latest/querying/basics/):
   - Execute `sli_query` over `time_window` (default 28d)
   - Calculate actual SLO achievement: `actual_slo = avg(sli_results)`
   - Identify breach periods: timestamps where SLI < target

3. **Compute error budget status**:
   - `consumed_budget = (1 - actual_slo) * window`
   - `remaining_budget = error_budget - consumed_budget`
   - `compliance = (consumed_budget <= error_budget) ? "PASS" : "FAIL"`

4. **Generate basic alert rule** (Prometheus example):
   ```yaml
   - alert: SLOBudgetExhausted
     expr: (1 - sli_query) > (1 - 0.999)
     for: 5m
     labels:
       severity: critical
     annotations:
       summary: "Error budget exhausted"
   ```

5. **Output**: Validation report (pass/fail), current budget status, basic alert rule

---

### Tier 2 (Extended Validation)

**Token budget**: T2 ≤6k tokens

**Scope**: Production SLO validation with multi-window burn rate alerts and compliance reporting.

**Steps:**

1. **Multi-window SLO validation** (accessed 2025-10-26T03:51:54-04:00: https://sre.google/workbook/implementing-slos/):
   - Validate SLO over multiple time windows: 7d, 28d, 90d
   - Calculate compliance for each window independently
   - Identify short-term degradation (7d breach) vs long-term trends (90d)
   - Generate breach timeline: all periods where SLI fell below target

2. **Burn rate calculation** (accessed 2025-10-26T03:51:54-04:00: https://sre.google/workbook/alerting-on-slos/):
   - **Fast burn** (1-hour window): Detects rapid error budget consumption
     - Threshold: 14.4x normal burn rate for 99.9% SLO
     - Formula: `(1 - sli_1h) > 14.4 * (1 - target)`
   - **Medium burn** (6-hour window): Detects moderate degradation
     - Threshold: 6x normal burn rate
     - Formula: `(1 - sli_6h) > 6 * (1 - target)`
   - **Slow burn** (3-day window): Detects gradual degradation
     - Threshold: 1x normal burn rate (budget exhaustion in 30 days)
     - Formula: `(1 - sli_3d) > 1 * (1 - target)`

3. **Error budget policy enforcement** (based on `error_budget_policy` parameter):
   - **Strict**: Alert when >75% budget consumed, freeze deploys at >90%
   - **Moderate**: Alert when >85% budget consumed, freeze deploys at >95%
   - **Flexible**: Alert when >90% budget consumed, no automatic freeze

4. **Platform-specific alerting rules generation**:

   **Prometheus** (accessed 2025-10-26T03:51:54-04:00: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/):
   ```yaml
   groups:
     - name: slo_alerts
       interval: 30s
       rules:
         - alert: SLOFastBurn
           expr: |
             (1 - (sum(rate(http_requests_total{status!~"5.."}[1h]))
                   / sum(rate(http_requests_total[1h]))))
             > (14.4 * (1 - 0.999))
           for: 2m
           labels:
             severity: critical
           annotations:
             summary: "Fast burn: error budget will exhaust in 2 hours"

         - alert: SLOSlowBurn
           expr: |
             (1 - (sum(rate(http_requests_total{status!~"5.."}[3d]))
                   / sum(rate(http_requests_total[3d]))))
             > (1 * (1 - 0.999))
           for: 15m
           labels:
             severity: warning
           annotations:
             summary: "Slow burn: error budget will exhaust in 30 days"
   ```

   **CloudWatch**:
   ```json
   {
     "AlarmName": "SLO-FastBurn-API",
     "ComparisonOperator": "GreaterThanThreshold",
     "EvaluationPeriods": 2,
     "MetricName": "ErrorRate",
     "Namespace": "AWS/ApplicationELB",
     "Period": 3600,
     "Statistic": "Average",
     "Threshold": 0.0144,
     "ActionsEnabled": true,
     "AlarmActions": ["arn:aws:sns:us-east-1:123456789:critical-alerts"]
   }
   ```

5. **Dashboard configuration** (accessed 2025-10-26T03:51:54-04:00: https://github.com/slok/sloth):
   - **Panel 1**: SLO compliance gauge (current achievement vs target)
   - **Panel 2**: Error budget remaining (time-series graph)
   - **Panel 3**: Burn rate by window (1h, 6h, 3d stacked graph)
   - **Panel 4**: Breach timeline (heatmap showing SLO violations)
   - **Panel 5**: Time to budget exhaustion (calculated metric)

   Grafana example (using Sloth format):
   ```yaml
   version: "prometheus/v1"
   service: "api-service"
   slos:
     - name: "availability"
       objective: 99.9
       sli:
         events:
           error_query: sum(rate(http_requests_total{status=~"5.."}[{{.window}}]))
           total_query: sum(rate(http_requests_total[{{.window}}]))
       alerting:
         name: "API SLO"
         page_alert:
           labels:
             severity: critical
         ticket_alert:
           labels:
             severity: warning
   ```

6. **Compliance audit report**:
   - **Summary**: Overall SLO compliance (PASS/FAIL) for each time window
   - **Breach details**: Start/end timestamps, duration, root cause (if known)
   - **Budget consumption**: Total consumed, remaining, projected exhaustion date
   - **Alerting effectiveness**: Were alerts fired during breach periods?
   - **Recommendations**: SLO adjustment suggestions based on historical performance

7. **Comprehensive output**:
   - Multi-window validation report with breach timeline
   - Platform-specific alerting rules (Prometheus/CloudWatch/Datadog)
   - Error budget status with burn rate metrics
   - Dashboard configuration (Grafana/CloudWatch JSON)
   - Compliance audit report

**Sources cited** (accessed 2025-10-26T03:51:54-04:00):
- **Google SRE Workbook - Implementing SLOs**: https://sre.google/workbook/implementing-slos/
- **Google SRE Workbook - Alerting on SLOs**: https://sre.google/workbook/alerting-on-slos/
- **Prometheus Alerting Rules**: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- **Sloth SLO Generator**: https://github.com/slok/sloth

---

### Tier 3 (Deep Analysis)

**Token budget**: T3 ≤12k tokens

**Scope**: Advanced SLO validation with anomaly detection, trend analysis, and automated remediation recommendations.

**Steps:**

1. **Historical trend analysis**:
   - Analyze SLO performance over extended period (90d, 180d, 1y)
   - Identify seasonality patterns (weekday/weekend, business hours, holidays)
   - Calculate baseline SLO achievement by time period
   - Detect anomalous degradation periods (statistical outliers)

2. **SLO sensitivity analysis**:
   - Simulate impact of SLO target adjustments (e.g., 99.9% → 99.95%)
   - Calculate required infrastructure improvements to meet tighter SLOs
   - Estimate cost of achieving higher reliability (additional resources, redundancy)

3. **Multi-service dependency analysis**:
   - Identify upstream/downstream service dependencies
   - Calculate composite SLO (product of dependent service SLOs)
   - Example: If Service A (99.9%) depends on Service B (99.95%), composite = 99.85%
   - Recommend SLO targets for dependencies to achieve overall target

4. **Automated remediation recommendations**:
   - Analyze breach root causes from incident reports/logs
   - Generate prioritized backlog of reliability improvements
   - Estimate error budget recovery timeline for each improvement
   - Link to related runbooks/playbooks for common failure modes

5. **Advanced alerting strategies**:
   - **Adaptive thresholds**: Adjust burn rate thresholds based on time-of-day/day-of-week patterns
   - **Multi-burn-rate windows**: Combine multiple windows (e.g., 1h AND 6h) to reduce false positives
   - **Budget forecasting**: Predict budget exhaustion based on current burn rate trends

6. **Comprehensive SLO evaluation**:
   - Generate executive summary report with visualizations
   - Provide SLO tuning recommendations (target too strict/loose?)
   - Include cost/benefit analysis of SLO improvements
   - Export results to common formats (PDF, Excel, JSON)

---

## Decision Rules

**SLO compliance determination:**

- **PASS**: Actual SLO ≥ target for all evaluated time windows
- **FAIL**: Actual SLO < target for any evaluated time window
- **WARNING**: Within 5% of error budget exhaustion (trigger proactive review)

**Burn rate alert severity mapping:**

- **Critical (page)**: Fast burn (1h) consuming >2% of 30-day budget
- **Warning (ticket)**: Medium burn (6h) consuming >5% of 30-day budget
- **Info (notification)**: Slow burn (3d) consuming >10% of 30-day budget

**Dashboard generation strategy:**

- **Prometheus metrics**: Use Grafana with Sloth-generated dashboards
- **CloudWatch metrics**: Use native CloudWatch dashboards
- **Datadog metrics**: Use Datadog SLO UI with custom widgets
- **Multi-platform**: Generate platform-agnostic JSON schema, manual import required

**Ambiguity thresholds:**

- If `slo_definition` lacks `window` → default to 30d (SRE standard)
- If `error_budget_policy` not specified → default to `moderate`
- If metrics have >10% data gaps → issue warning, proceed with available data
- If SLO target >99.99% → issue warning about feasibility

**Abort/stop conditions:**

- Metrics query returns zero results (invalid query or no data)
- SLO definition malformed (missing required fields)
- Metrics platform authentication/access fails
- Historical data coverage <50% of validation window

---

## Output Contract

**Required fields:**

```json
{
  "validation_report": {
    "slo_name": "string",
    "target": "number (e.g., 99.9)",
    "windows": [
      {
        "period": "string (7d, 28d, 90d)",
        "actual_slo": "number (achieved %)",
        "compliance": "PASS | FAIL | WARNING",
        "error_budget_total": "number (minutes)",
        "error_budget_consumed": "number (minutes)",
        "error_budget_remaining": "number (minutes)",
        "breach_count": "number",
        "breach_timeline": [
          {
            "start": "ISO8601 timestamp",
            "end": "ISO8601 timestamp",
            "duration_minutes": "number",
            "severity": "critical | warning"
          }
        ]
      }
    ],
    "overall_compliance": "PASS | FAIL"
  },
  "alerting_rules": {
    "platform": "string (prometheus | cloudwatch | datadog)",
    "format": "yaml | json",
    "rules": "string (platform-specific alert definitions)"
  },
  "error_budget_status": {
    "current_burn_rate_1h": "number (multiplier, e.g., 14.4x)",
    "current_burn_rate_6h": "number",
    "current_burn_rate_3d": "number",
    "time_to_exhaustion": "string (e.g., '2 hours' | '15 days' | 'N/A')",
    "budget_policy_triggered": "boolean",
    "recommended_action": "freeze_deploys | monitor_closely | continue_normal_operations"
  },
  "dashboard_config": {
    "platform": "string (grafana | cloudwatch | datadog)",
    "format": "json | yaml",
    "config": "object (platform-specific dashboard definition)"
  }
}
```

**Optional fields:**

- `trend_analysis`: Historical SLO performance trends (T3 only)
- `remediation_recommendations`: Prioritized reliability improvements (T3 only)
- `compliance_audit`: Detailed audit report with breach analysis

**Validation:**

- All time windows must have `compliance` status
- Burn rate calculations must use correct multipliers for target SLO
- Dashboard config must be valid JSON/YAML for target platform
- Alert rules must be syntactically correct for metrics platform

---

## Examples

**Input:**

```json
{
  "slo_definition": {
    "name": "API Availability",
    "target": 99.9,
    "window": "30d",
    "sli_query": "sum(rate(http_requests_total{status!~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))"
  },
  "metrics_source": "prometheus",
  "time_window": "28d",
  "error_budget_policy": "moderate"
}
```

**Output (abbreviated):**

```json
{
  "validation_report": {
    "slo_name": "API Availability",
    "target": 99.9,
    "windows": [{
      "period": "28d",
      "actual_slo": 99.87,
      "compliance": "FAIL",
      "error_budget_consumed": 52.4,
      "error_budget_remaining": -12.2,
      "breach_count": 3
    }],
    "overall_compliance": "FAIL"
  },
  "error_budget_status": {
    "current_burn_rate_1h": 2.1,
    "time_to_exhaustion": "N/A (budget exhausted)"
  }
}
```

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens for basic SLO validation with simple alerting
- **T2**: ≤6k tokens for multi-window validation with burn rate alerts and dashboards
- **T3**: ≤12k tokens for trend analysis, remediation recommendations, and advanced reporting

**Safety requirements:**

- Validate metrics queries are read-only (no writes to metrics platform)
- Warn if SLO breach detected but no historical incidents recorded
- Ensure alert rules don't create excessive notification volume (>10 alerts/day = review needed)

**Auditability:**

- All validation results include query timestamps and data sources
- Breach timeline provides exact start/end times for compliance review
- Alert rules are version-controlled and reproducible

**Determinism:**

- Same SLO definition + metrics data produces identical validation report
- Burn rate calculations use standard formulas from Google SRE literature
- Error budget math is transparent and auditable

---

## Resources

**Primary sources:**

- Google SRE Workbook - Implementing SLOs: https://sre.google/workbook/implementing-slos/
- Google SRE Workbook - Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Prometheus Alerting Rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
- Datadog SLO Monitoring: https://docs.datadoghq.com/monitors/service_level_objectives/

**Reference implementations:**

- Sloth (SLO generator): https://github.com/slok/sloth
- OpenSLO Specification: https://github.com/OpenSLO/OpenSLO
- Pyrra (SLO framework): https://github.com/pyrra-dev/pyrra

**Additional reading:**

- The Art of SLOs: https://www.alex-hidalgo.com/the-art-of-slos
- SLI/SLO Workshop: https://www.usenix.org/conference/srecon19americas/presentation/fong-jones
