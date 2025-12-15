---
name: Observability Unified Dashboard
slug: observability-unified-dashboard
description: Design unified dashboards with golden signals, OpenTelemetry correlation, SLO tracking, and Grafana 11 auto-correlations for metrics/logs/traces.
capabilities:
  - Unified dashboard design integrating metrics, logs, and traces
  - Golden Signals implementation (latency, traffic, errors, saturation)
  - OpenTelemetry pipeline configuration with OTLP protocol
  - Grafana 11 correlation setup (metrics → logs → traces)
  - SLO/SLI tracking and alerting
  - Multi-data source query orchestration
  - Real-time compliance scoring and trend analysis
  - Automated alert routing and escalation
inputs:
  services:
    type: array
    description: List of services/systems to monitor
    required: true
  deployment_env:
    type: string
    description: Environment context (production, staging, dev)
    required: true
  slo_targets:
    type: object
    description: SLO definitions per service (e.g., 99.9% availability, p95 latency <200ms)
    required: false
  telemetry_sources:
    type: object
    description: Data sources (Prometheus, Loki, Tempo, Jaeger, cloud providers)
    required: true
  alert_destinations:
    type: array
    description: Alert routing (PagerDuty, Slack, email, webhooks)
    required: false
  custom_metrics:
    type: array
    description: Business-specific metrics beyond golden signals
    required: false
outputs:
  dashboard_config:
    type: object
    description: Grafana dashboard JSON with panels for golden signals and SLOs
  correlation_rules:
    type: array
    description: Automatic correlation rules linking metrics, logs, and traces
  alert_rules:
    type: array
    description: Alert definitions with thresholds, severity, and routing
  otel_pipeline:
    type: object
    description: OpenTelemetry Collector configuration (receivers, processors, exporters)
  slo_summary:
    type: object
    description: SLO compliance report with error budget burn rate
keywords:
  - observability
  - golden signals
  - OpenTelemetry
  - Grafana
  - SLO
  - SLI
  - unified dashboard
  - metrics
  - logs
  - traces
  - correlation
  - alerting
  - SRE
version: 1.0.0
owner: cognitive-toolworks
license: Apache-2.0
security:
  secrets: "Avoid logging sensitive data; redact PII/credentials in traces and logs"
  compliance: "GDPR/CCPA-compliant log retention; encrypt telemetry data in transit (TLS)"
links:
  - title: "Google SRE Book: The Four Golden Signals"
    url: "https://sre.google/sre-book/monitoring-distributed-systems/"
    accessed: "2025-10-26"
  - title: "OpenTelemetry Official Documentation"
    url: "https://opentelemetry.io/docs/"
    accessed: "2025-10-26"
  - title: "Grafana 11 Correlations Documentation"
    url: "https://grafana.com/docs/grafana/latest/administration/correlations/"
    accessed: "2025-10-26"
  - title: "Prometheus Best Practices"
    url: "https://prometheus.io/docs/practices/"
    accessed: "2025-10-26"
  - title: "NIST SP 800-92: Guide to Computer Security Log Management"
    url: "https://csrc.nist.gov/publications/detail/sp/800-92/final"
    accessed: "2025-10-26"
---

## Purpose & When-To-Use

**Purpose:** Design comprehensive observability dashboards that unify metrics, logs, and traces using the Four Golden Signals framework (Latency, Traffic, Errors, Saturation), automate correlations across telemetry signals via OpenTelemetry, track SLO compliance, and configure Grafana 11 with automatic drill-down from alerts to root cause.

**When to Use:**
- You need a **single pane of glass** for monitoring distributed systems (microservices, cloud-native apps).
- You want to implement **SRE best practices** (Golden Signals, SLO tracking, error budget management).
- You have **multiple telemetry sources** (Prometheus, Loki, Tempo, Jaeger, CloudWatch, Datadog) and need unified visibility.
- You need **automatic correlation** from high-level metrics (latency spike) → detailed logs (error messages) → distributed traces (slow span).
- You're migrating from **tool-specific dashboards** (separate Prometheus/Grafana, ELK, Jaeger UIs) to a unified platform.
- You require **real-time SLO compliance** tracking with burn rate alerts.

**Orchestrates:**
- `observability-slo-calculator`: Computes SLO compliance, error budgets, and burn rates.
- `observability-stack-configurator`: Deploys Prometheus, Loki, Tempo, Grafana stack.

**Complements:**
- `database-postgres-architect`, `database-mongodb-architect`, `database-redis-architect`: Adds database-specific metrics (query latency, cache hit rate).
- `cloud-kubernetes-architect`: Integrates k8s metrics (pod restarts, resource saturation).

## Pre-Checks

**Mandatory Inputs:**
- `services`: List of services/systems to monitor (≥1). Each service should have a unique `service.name` (OpenTelemetry resource attribute).
- `telemetry_sources`: At least one data source for metrics (e.g., Prometheus), logs (e.g., Loki), or traces (e.g., Tempo).
- `deployment_env`: Environment context to filter data (production, staging, dev).

**Validation Steps:**
1. **Compute NOW_ET** using NIST time.gov semantics (America/New_York, ISO-8601) for timestamp anchoring.
2. **Check telemetry_sources accessibility:** Verify endpoints are reachable (HTTP 200 for Prometheus `/api/v1/status/config`, Loki `/ready`, Tempo `/ready`).
3. **Verify OpenTelemetry instrumentation:** Confirm services emit OTLP (OpenTelemetry Protocol) data with `trace_id` and `span_id` propagation.
4. **Validate SLO targets format:** If provided, ensure SLOs follow `<SLI> <comparator> <target>` format (e.g., `availability >= 99.9%`, `p95_latency < 200ms`).
5. **Abort if:**
   - Zero telemetry sources configured.
   - Services list is empty or lacks `service.name` attributes.
   - Data sources return 401 (authentication failure) or 404 (endpoint not found).

## Procedure

### T1: Quick Dashboard Setup (≤2k tokens, 80% use case)

**Goal:** Generate a minimal unified dashboard with the Four Golden Signals for a single service using existing Prometheus/Loki/Tempo data sources.

**Steps:**
1. **Identify primary service:** Select the most critical service from `services` list (or use first entry if priority not specified).
2. **Query telemetry sources for baseline metrics:**
   - **Latency:** `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="<service>"}[5m]))`
   - **Traffic:** `sum(rate(http_requests_total{job="<service>"}[5m]))`
   - **Errors:** `sum(rate(http_requests_total{job="<service>", status=~"5.."}[5m])) / sum(rate(http_requests_total{job="<service>"}[5m])) * 100`
   - **Saturation:** `avg(process_cpu_seconds_total{job="<service>"})` and `avg(process_resident_memory_bytes{job="<service>"})`
3. **Generate Grafana dashboard JSON:**
   - 4 panels (one per golden signal), arranged in a 2×2 grid.
   - Time range: Last 1 hour (default).
   - Refresh interval: 30 seconds.
4. **Add basic alert rule:**
   - Alert if error rate > 5% for 5 minutes (severity: warning).
5. **Output:** Dashboard JSON + alert rule YAML (Grafana-managed alerting format).

**Token Budget:** ≤2k tokens (no deep SLO calculation, no complex correlation setup).

### T2: Unified Dashboard with SLO Tracking (≤6k tokens)

**Goal:** Create a comprehensive dashboard with Golden Signals, SLO compliance tracking, automated correlations, and multi-service support.

**Steps:**
1. **Invoke `observability-slo-calculator` (T2):**
   - Pass `slo_targets`, `services`, and `telemetry_sources` (Prometheus for metrics, Loki for logs).
   - Retrieve: SLO compliance %, error budget remaining, burn rate, time to exhaustion.
2. **Design multi-service dashboard:**
   - **Overview panel:** Table showing all services with current SLO status (✅ compliant, ⚠️ warning, ❌ breached).
   - **Per-service rows:** Each service gets 4 golden signal panels + 1 SLO panel.
   - **Heatmap panel:** Latency distribution across all services (percentiles: p50, p95, p99).
3. **Configure OpenTelemetry correlations:**
   - **Metrics → Logs:** Add correlation from Prometheus alert → Loki logs filtered by `service.name` and `trace_id`.
   - **Logs → Traces:** Add correlation from Loki log entry → Tempo trace lookup via `trace_id`.
   - **Configuration:** Use Grafana 11 Correlations API (`POST /api/datasources/uid/<uid>/correlations`).
4. **Set up automated alert routing:**
   - **Critical alerts** (SLO burn rate > 14.4x, error rate > 10%): Route to PagerDuty.
   - **Warning alerts** (SLO burn rate > 6x, error rate > 5%): Route to Slack.
   - **Info alerts** (SLO trending toward breach in 7 days): Route to email.
5. **Generate OpenTelemetry Collector pipeline:**
   ```yaml
   receivers:
     otlp:
       protocols:
         grpc:
         http:
   processors:
     batch:
       timeout: 10s
       send_batch_size: 1024
     resource:
       attributes:
         - key: deployment.environment
           value: ${DEPLOYMENT_ENV}
           action: insert
   exporters:
     prometheus:
       endpoint: "prometheus:9090"
     loki:
       endpoint: "http://loki:3100/loki/api/v1/push"
     tempo:
       endpoint: "tempo:4317"
   service:
     pipelines:
       metrics:
         receivers: [otlp]
         processors: [batch, resource]
         exporters: [prometheus]
       logs:
         receivers: [otlp]
         processors: [batch, resource]
         exporters: [loki]
       traces:
         receivers: [otlp]
         processors: [batch, resource]
         exporters: [tempo]
   ```
6. **Validation:**
   - Test correlation: Click Prometheus alert → verify Loki logs appear → click log line → verify Tempo trace opens.
   - Test SLO tracking: Trigger synthetic error (increase 5xx responses) → confirm error budget decreases.
7. **Output:**
   - Dashboard JSON (multi-service, golden signals, SLO panels).
   - Correlation rules JSON (3 rules: metrics→logs, logs→traces, traces→metrics).
   - Alert rules YAML (5-10 rules based on golden signals + SLO burn rate).
   - OpenTelemetry Collector config YAML.
   - SLO summary report (current compliance, burn rate, time to exhaustion).

**Token Budget:** ≤6k tokens (includes SLO calculation delegation, correlation setup, multi-service config).

### T3: Enterprise-Scale Dashboard with Advanced Features (≤12k tokens)

**Goal:** Deploy a production-grade unified observability platform with custom metrics, anomaly detection, capacity planning, and compliance reporting.

**Steps:**
1. **Invoke `observability-stack-configurator` (T3):**
   - Deploy full stack (Prometheus, Loki, Tempo, Grafana 11) with HA (high availability).
   - Configure persistent storage (retention: metrics 30 days, logs 90 days, traces 7 days).
2. **Extend dashboard with custom metrics:**
   - **Business metrics:** Order conversion rate, payment success rate, user signups/hour.
   - **Infrastructure metrics:** Database query latency (PostgreSQL, MongoDB, Redis), cache hit rate, queue depth (Kafka, RabbitMQ).
   - **Security metrics:** Failed login attempts, API rate limit hits, TLS certificate expiry countdown.
3. **Implement anomaly detection:**
   - Use Prometheus recording rules to compute baseline metrics (7-day moving average for latency, traffic).
   - Alert on deviations: `abs(current_latency - baseline_latency) / baseline_latency > 0.3` (30% deviation).
4. **Capacity planning panel:**
   - Extrapolate resource usage (CPU, memory, disk) to predict when thresholds will be hit.
   - Example: If disk usage grows at 2GB/day and 80GB free, alert "Disk full in 40 days."
5. **Compliance reporting:**
   - **NIST SP 800-92 Log Management:** Verify logs retained for required period (90 days), encrypted at rest.
   - **GDPR/CCPA:** Ensure PII redaction in logs (email, IP addresses masked).
   - Generate monthly compliance report: log retention status, encryption enabled, access audit trail.
6. **Advanced correlations:**
   - **Traces → Metrics:** From slow trace span → view aggregated latency metrics for that endpoint.
   - **Logs → Metrics:** From error log → view error rate time series.
   - **Cross-service correlation:** Link frontend error → backend API trace → database slow query log.
7. **Multi-environment dashboard:**
   - Separate panels for production, staging, dev environments.
   - Environment selector variable (Grafana template variable) to toggle between envs.
8. **Generate comprehensive documentation:**
   - Runbook for common alerts (High error rate → check recent deployments, review logs, rollback if needed).
   - Troubleshooting guide (Correlation not working → verify `trace_id` propagation, check OTLP endpoints).
9. **Validation:**
   - Simulate production incident: Inject latency spike → verify anomaly detection alerts → follow correlation chain → confirm root cause identified.
   - Audit compliance: Run GDPR compliance check → verify PII redacted, logs encrypted.
10. **Output:**
    - Multi-environment dashboard JSON (production, staging, dev).
    - 20+ alert rules (golden signals + SLO + anomaly detection + capacity planning).
    - OpenTelemetry Collector config with advanced processors (attributes, tail sampling, span metrics).
    - Compliance report (log retention, encryption status, PII redaction confirmation).
    - Runbook documentation (5-10 common scenarios with resolution steps).

**Token Budget:** ≤12k tokens (includes stack deployment, advanced analytics, compliance checks, documentation).

## Decision Rules

**Ambiguity Resolution:**
1. **If `slo_targets` not provided:**
   - Use **industry-standard defaults**: 99.9% availability (3 nines), p95 latency < 500ms, error rate < 1%.
   - Emit warning: "No SLO targets specified; using defaults. Review and adjust based on business requirements."
2. **If telemetry source lacks one signal type (e.g., no traces):**
   - Proceed with available signals (metrics + logs only).
   - Emit note: "Tempo not configured; trace correlation unavailable. Install Tempo for full observability."
3. **If multiple services with same `service.name`:**
   - Abort and request clarification: "Duplicate service names detected. Ensure unique `service.name` attributes per service."
4. **If alert destinations not specified:**
   - Default to **Grafana built-in alerting** (notifications visible in Grafana UI only).
   - Suggest: "Configure PagerDuty, Slack, or email for external alert routing."

**Stop Conditions:**
- **Insufficient data:** Telemetry sources return zero metrics/logs/traces for >5 minutes → abort with error: "No data from telemetry sources. Verify instrumentation and OTLP exporters."
- **Authentication failure:** All data sources return 401/403 → abort with error: "Authentication failed for telemetry sources. Check credentials and API tokens."
- **Incompatible versions:** Grafana version < 10.0 detected → warn: "Correlations require Grafana 11+. Upgrade recommended."

**Thresholds:**
- **Golden Signal Alerts:**
  - Latency: p95 > 2× baseline for 5 minutes.
  - Traffic: >50% drop from baseline for 5 minutes (potential outage).
  - Errors: >5% error rate for 5 minutes.
  - Saturation: CPU >80%, memory >85%, disk >90% for 5 minutes.
- **SLO Burn Rate Alerts (Google SRE methodology):**
  - **Critical:** 14.4× burn rate (error budget exhausted in 2 days) → page immediately.
  - **Warning:** 6× burn rate (error budget exhausted in 5 days) → notify team.

## Output Contract

**Required Fields:**

```typescript
{
  dashboard_config: {
    uid: string;              // Grafana dashboard UID (unique identifier)
    title: string;            // Dashboard title (e.g., "Unified Observability: Production Services")
    panels: Array<{           // Array of dashboard panels
      id: number;             // Panel ID (unique within dashboard)
      title: string;          // Panel title (e.g., "Latency (p95)")
      type: string;           // Panel type (graph, stat, table, heatmap)
      targets: Array<{        // Data source queries
        datasource: string;   // Data source UID (Prometheus, Loki, Tempo)
        expr: string;         // Query expression (PromQL, LogQL, TraceQL)
      }>;
      alert?: {               // Optional alert configuration
        name: string;         // Alert rule name
        condition: string;    // Alert condition (PromQL expression)
        for: string;          // Duration threshold (e.g., "5m")
        annotations: {
          summary: string;    // Alert summary (e.g., "High error rate detected")
        };
      };
    }>;
    templating: {             // Dashboard variables (environment, service selector)
      list: Array<{
        name: string;         // Variable name (e.g., "environment")
        type: string;         // Variable type (query, custom, interval)
        query: string;        // Query to populate variable options
      }>;
    };
  };
  correlation_rules: Array<{  // Grafana correlations
    source_datasource: string; // Source data source UID (e.g., Prometheus)
    target_datasource: string; // Target data source UID (e.g., Loki)
    label: string;             // Correlation link label (e.g., "View Logs")
    field: string;             // Field to use for correlation (e.g., "trace_id")
    transformation: string;    // Optional transformation (e.g., regex extraction)
  }>;
  alert_rules: Array<{        // Alert definitions
    name: string;             // Alert rule name
    expr: string;             // PromQL expression for alert condition
    for: string;              // Duration threshold (e.g., "5m")
    severity: "critical" | "warning" | "info";
    annotations: {
      summary: string;        // Human-readable alert summary
      runbook_url?: string;   // Link to runbook for resolution steps
    };
    route?: {                 // Alert routing (optional)
      receiver: string;       // Receiver name (PagerDuty, Slack, email)
    };
  }>;
  otel_pipeline: {            // OpenTelemetry Collector configuration
    receivers: object;        // OTLP receivers (grpc, http)
    processors: object;       // Batch, resource, attributes processors
    exporters: object;        // Prometheus, Loki, Tempo exporters
    service: {
      pipelines: {
        metrics: { receivers: string[]; processors: string[]; exporters: string[] };
        logs: { receivers: string[]; processors: string[]; exporters: string[] };
        traces: { receivers: string[]; processors: string[]; exporters: string[] };
      };
    };
  };
  slo_summary: {              // SLO compliance report (from observability-slo-calculator)
    services: Array<{
      name: string;           // Service name
      slo_compliance: number; // Current SLO compliance (0-100%)
      error_budget_remaining: number; // Error budget remaining (%)
      burn_rate: number;      // Current error budget burn rate (multiplier)
      time_to_exhaustion_hours: number | null; // Hours until error budget exhausted (null if budget positive)
      status: "compliant" | "warning" | "breached";
    }>;
    overall_compliance: number; // Average compliance across all services
  };
}
```

**Optional Fields:**
- `custom_panels`: Array of custom dashboard panels for business-specific metrics.
- `capacity_forecast`: Object with resource usage predictions (disk full in X days, etc.).
- `compliance_report`: Object with NIST SP 800-92, GDPR/CCPA compliance status.
- `runbook_links`: Object mapping alert names to runbook URLs.

**Format:** JSON for `dashboard_config`, `correlation_rules`, `otel_pipeline`, `slo_summary`. YAML for `alert_rules` (Grafana-managed alerting format).

## Examples

### Example 1: E-commerce Platform Unified Dashboard (T2)

**Input:**
```yaml
services:
  - name: "frontend-web"
    type: "web"
  - name: "api-gateway"
    type: "api"
  - name: "order-service"
    type: "backend"
deployment_env: "production"
slo_targets:
  - service: "api-gateway"
    availability: 99.95%
    p95_latency_ms: 200
  - service: "order-service"
    availability: 99.9%
    p95_latency_ms: 500
telemetry_sources:
  metrics: "prometheus-prod"
  logs: "loki-prod"
  traces: "tempo-prod"
alert_destinations:
  - type: "pagerduty"
    integration_key: "REDACTED"
  - type: "slack"
    webhook_url: "REDACTED"
```

**Output (T2 Summary):**
```yaml
Dashboard: "Unified Observability: E-commerce Production"
  - Overview Panel: 3 services, 2/3 SLO compliant (order-service at 99.85%, warning)
  - Golden Signals (per service):
      api-gateway: Latency p95=150ms ✅, Traffic=1200 req/s, Errors=0.5% ✅, CPU=45%
      order-service: Latency p95=480ms ✅, Traffic=300 req/s, Errors=2.1% ⚠️, CPU=78%
  - Correlations: 3 rules (Prometheus alert → Loki logs → Tempo traces)
  - Alerts:
      - CRITICAL: order-service error rate >5% for 5m → PagerDuty
      - WARNING: order-service SLO burn rate 7.2× (budget exhausted in 4 days) → Slack
OpenTelemetry Pipeline: OTLP receivers → batch processor → Prometheus/Loki/Tempo exporters
SLO Summary:
  - api-gateway: 99.98% compliant (6% error budget remaining, burn rate 0.8×)
  - order-service: 99.85% compliant (85% error budget consumed, burn rate 7.2× ⚠️)
  - Overall: 99.92% compliance
```

**Link to Full Example:** See `skills/observability-unified-dashboard/examples/ecommerce-unified-dashboard.txt`

### Example 2: Microservices Platform with Custom Metrics (T3 Snippet)

**Custom Metrics Added:**
- **Payment success rate:** `sum(rate(payment_transactions_total{status="success"}[5m])) / sum(rate(payment_transactions_total[5m])) * 100`
- **Database query latency:** `histogram_quantile(0.95, rate(db_query_duration_seconds_bucket{db="orders"}[5m]))`
- **Cache hit rate:** `sum(rate(redis_hits_total[5m])) / (sum(rate(redis_hits_total[5m])) + sum(rate(redis_misses_total[5m]))) * 100`

**Anomaly Detection Alert:**
```yaml
- alert: LatencyAnomalyDetected
  expr: |
    abs(
      histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
      -
      histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[7d] offset 7d))
    ) / histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[7d] offset 7d)) > 0.3
  for: 10m
  severity: warning
  annotations:
    summary: "Latency 30% higher than 7-day baseline"
    runbook_url: "https://runbooks.example.com/latency-anomaly"
```

## Quality Gates

**Token Budget Compliance:**
- T1 output ≤2k tokens (basic dashboard + 1 service).
- T2 output ≤6k tokens (multi-service dashboard + SLO tracking + correlations).
- T3 output ≤12k tokens (enterprise dashboard + custom metrics + anomaly detection + compliance).

**Validation Checklist:**
- [ ] Dashboard has 4 golden signal panels per service (Latency, Traffic, Errors, Saturation).
- [ ] SLO compliance panel shows current %, error budget remaining, burn rate.
- [ ] Correlations tested: Click metric alert → logs appear → trace opens.
- [ ] Alert rules use multi-window burn rate (1h + 5m for critical, 6h + 30m for warning).
- [ ] OpenTelemetry pipeline config validates against OTEL Collector schema.
- [ ] PII redaction confirmed in logs (regex check for email, SSN, credit card patterns).
- [ ] Dashboard JSON imports successfully into Grafana 11+ without errors.

**Safety & Auditability:**
- **No secrets in output:** Redact all API keys, tokens, passwords in dashboard/alert configs.
- **Retention compliance:** Verify logs retained per policy (90 days for NIST SP 800-92, adjust for GDPR right to be forgotten).
- **Audit trail:** Dashboard changes tracked via Grafana version history; alert rule changes logged to SIEM.

**Determinism:**
- **Stable queries:** Use fixed time ranges for baselines (7-day moving average, not "last week" which shifts daily).
- **Consistent naming:** Use standardized panel titles (Latency (p95), Traffic (req/s), Errors (%), Saturation (CPU/Memory)).

## Resources

**Official Documentation:**
- [Google SRE Book: The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/) (accessed 2025-10-26)
  - Latency: Time to service a request (distinguish success vs failure latency).
  - Traffic: Demand on your system (requests/sec, transactions/sec).
  - Errors: Rate of failed requests (HTTP 500s, exceptions).
  - Saturation: Resource utilization (CPU, memory, disk, network near capacity).
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) (accessed 2025-10-26)
  - OTLP protocol specification, instrumentation guides, collector configuration.
- [Grafana 11 Correlations](https://grafana.com/docs/grafana/latest/administration/correlations/) (accessed 2025-10-26)
  - Setup guide for automatic correlations between data sources.
- [Prometheus Alerting Best Practices](https://prometheus.io/docs/practices/alerting/) (accessed 2025-10-26)
  - Multi-window burn rate alerts, alert routing, notification templates.
- [NIST SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final) (accessed 2025-10-26)
  - Log retention requirements, encryption standards, access controls.

**Complementary Skills:**
- `observability-slo-calculator`: Computes SLO compliance, error budgets, burn rates (invoke for T2/T3).
- `observability-stack-configurator`: Deploys Prometheus, Loki, Tempo, Grafana stack (invoke for T3).

**OpenTelemetry Collector Reference Config:**
- [OTEL Collector Configuration](https://opentelemetry.io/docs/collector/configuration/)
- [Prometheus Exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/prometheusexporter)
- [Loki Exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/lokiexporter)
- [Tempo Exporter (OTLP)](https://grafana.com/docs/tempo/latest/configuration/otlp/)

**Grafana Dashboard Examples:**
- [Grafana Labs: SLO Dashboard](https://grafana.com/grafana/dashboards/14683-slo-dashboard/)
- [Grafana Labs: OpenTelemetry APM](https://grafana.com/grafana/dashboards/19419-opentelemetry-apm/)

**SLO/Error Budget Methodology:**
- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [Sloth: Easy SLO definition and alerting (SLO generator)](https://github.com/slok/sloth)

**Security & Compliance:**
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) (PII redaction guidance)
- [GDPR Article 17: Right to Erasure](https://gdpr-info.eu/art-17-gdpr/) (log retention implications)
