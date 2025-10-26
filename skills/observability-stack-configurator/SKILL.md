---
name: "Observability Stack Configurator"
slug: observability-stack-configurator
description: "Configure comprehensive observability with metrics, logging, tracing, and alerting using Prometheus, OpenTelemetry, CloudWatch, and Grafana."
capabilities:
  - configure_metrics_collection
  - configure_logging_aggregation
  - configure_distributed_tracing
  - configure_alerting_rules
inputs:
  platform:
    type: string
    description: "Platform: kubernetes, aws, azure, gcp, on-premise"
    required: true
  tech_stack:
    type: array
    description: "Application technologies to instrument"
    required: true
  requirements:
    type: object
    description: "SLIs, alerting rules, retention policies, dashboard specifications"
    required: true
outputs:
  metrics_config:
    type: code
    description: "Prometheus, CloudWatch, or Datadog configuration"
  logging_config:
    type: code
    description: "Logging stack configuration (ELK, Loki, CloudWatch Logs)"
  tracing_config:
    type: code
    description: "OpenTelemetry or X-Ray instrumentation"
  dashboards:
    type: array
    description: "Grafana or CloudWatch dashboard definitions"
keywords:
  - observability
  - prometheus
  - opentelemetry
  - grafana
  - cloudwatch
  - logging
  - tracing
  - metrics
  - alerting
  - monitoring
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: required
links:
  - https://prometheus.io/docs/
  - https://opentelemetry.io/docs/
  - https://grafana.com/docs/
  - https://aws.amazon.com/cloudwatch/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Production incidents reveal lack of visibility into system behavior
- Application deployment without monitoring or alerting
- Troubleshooting requires distributed tracing across microservices
- SLO/SLA commitments require metrics and alerting
- Compliance or audit requires centralized logging
- Performance optimization needs detailed metrics

**Use this skill when** you need a complete observability stack with metrics collection, log aggregation, distributed tracing, and intelligent alerting.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T01:33:56-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `platform` is one of: `kubernetes`, `aws`, `azure`, `gcp`, `on-premise`
   - `tech_stack` contains instrumentable technologies
   - `requirements.slis` defines key service level indicators
   - `requirements.alerting_rules` specifies conditions and thresholds
   - `requirements.retention_policies` defines data retention periods
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Platform compatibility**: Confirm observability tools available on target platform

**Abort conditions:**

- Platform doesn't support required observability tools
- Tech stack cannot be instrumented (proprietary, closed-source without metrics endpoint)
- Conflicting requirements (e.g., "zero cost" with "15-second granularity metrics")
- Retention requirements violate regulatory constraints

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Basic observability with essential metrics, logs, and simple alerting.

**Steps:**

1. **Design observability architecture** (500 tokens):
   - Select observability stack based on platform:
     - **Kubernetes**: Prometheus + Grafana + Loki
     - **AWS**: CloudWatch Metrics + Logs + X-Ray
     - **Azure**: Azure Monitor + Application Insights
     - **GCP**: Cloud Monitoring + Cloud Logging + Cloud Trace
   - Identify instrumentation points in application code
   - Define essential metrics (RED: Rate, Errors, Duration; USE: Utilization, Saturation, Errors)

2. **Generate observability configurations** (1500 tokens):
   - **Metrics**:
     - Prometheus scrape configs or CloudWatch metric filters
     - Application instrumentation snippets (client libraries)
     - Essential metrics: request rate, error rate, latency percentiles (p50, p95, p99)
   - **Logging**:
     - Log aggregation configuration (Loki, CloudWatch Logs, ELK)
     - Structured logging format (JSON)
     - Log retention policies (7-30 days for development)
   - **Basic alerting**:
     - Critical alerts: service down, error rate >5%, latency >1s
     - Alert routing configuration (email, Slack, PagerDuty)
   - **Simple dashboards**:
     - Service health overview (uptime, request rate, error rate, latency)
     - Infrastructure metrics (CPU, memory, disk, network)

**Decision point**: If requirements include distributed tracing, SLO tracking, advanced analytics, or multi-cluster → escalate to T2.

---

### Tier 2 (Extended Analysis, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Comprehensive observability with distributed tracing, SLO tracking, advanced alerting, and correlation.

**Steps:**

1. **Design comprehensive observability** (2000 tokens):
   - **Distributed tracing** (accessed 2025-10-26T01:33:56-04:00):
     - **OpenTelemetry**: Language-agnostic instrumentation for metrics, logs, traces
     - Trace context propagation across service boundaries (W3C Trace Context)
     - Sampling strategies (head-based, tail-based) for cost optimization
     - Integration with Jaeger, Zipkin, or cloud-native solutions (X-Ray, Cloud Trace)
   - **SLO tracking**:
     - Define SLIs from requirements (availability, latency, error rate)
     - Calculate SLO compliance and error budgets
     - Configure SLO dashboards with burn rate alerts
   - **Advanced metrics**:
     - Business metrics (conversion rate, transaction volume)
     - Application performance monitoring (APM) with detailed breakdowns
     - Custom metrics for domain-specific monitoring
   - **Log correlation**:
     - Trace ID injection into logs for correlation
     - Structured logging with consistent fields
     - Log-based metrics for pattern detection

2. **Generate comprehensive configurations** (4000 tokens):
   - **Prometheus/CloudWatch advanced**:
     - Recording rules for precomputed aggregations
     - Federation for multi-cluster metrics
     - Long-term storage (Thanos, Cortex, or cloud-native)
     - Service discovery for dynamic targets
   - **OpenTelemetry instrumentation**:
     - Auto-instrumentation for common frameworks
     - Custom spans for business-critical operations
     - Baggage propagation for cross-service context
     - Collector configuration with processors and exporters
   - **Advanced alerting**:
     - Multi-condition alerts with logical operators
     - Anomaly detection for dynamic thresholds
     - Alert grouping and deduplication
     - Escalation policies and on-call schedules
     - Runbook links in alert descriptions
   - **Comprehensive dashboards**:
     - Service dependency maps
     - SLO compliance tracking
     - Cost attribution and optimization
     - Capacity planning metrics
   - **Log analytics**:
     - Full-text search and filtering
     - Log-based alerting
     - Anomaly detection in logs
     - Compliance audit trails

**Sources cited** (accessed 2025-10-26T01:33:56-04:00):

- **Prometheus Best Practices**: https://prometheus.io/docs/practices/
- **OpenTelemetry**: https://opentelemetry.io/docs/concepts/
- **Grafana Dashboards**: https://grafana.com/docs/grafana/latest/dashboards/
- **Google SRE Monitoring**: https://sre.google/sre-book/monitoring-distributed-systems/

---

### Tier 3 (Deep Dive, ≤12k tokens)

**Token budget**: ≤12k tokens

**Scope**: Enterprise observability with AI/ML insights, cost optimization, and security monitoring.

**Steps:**

1. **AI/ML-enhanced observability** (4000 tokens):
   - Anomaly detection with machine learning models
   - Predictive alerting based on historical patterns
   - Root cause analysis automation
   - Capacity forecasting with time-series prediction
   - Automated incident triage and correlation

2. **Advanced analytics and optimization** (4000 tokens):
   - Observability data lake for long-term analysis
   - Cost optimization through sampling and aggregation strategies
   - Multi-tenancy with namespace isolation
   - Cardinality management for high-dimensional metrics
   - Query optimization and performance tuning
   - Data retention tiering (hot/warm/cold storage)

3. **Security and compliance monitoring** (4000 tokens):
   - Security event logging and SIEM integration
   - Audit trail generation for compliance (SOC2, HIPAA, PCI-DSS)
   - Sensitive data masking in logs
   - Access control and authentication for observability tools
   - Encryption at rest and in transit for telemetry data
   - Compliance reporting and evidence collection

**Additional sources** (accessed 2025-10-26T01:33:56-04:00):

- **OpenTelemetry Collector**: https://opentelemetry.io/docs/collector/
- **Thanos**: https://thanos.io/tip/thanos/quick-tutorial.md
- **AWS Observability Best Practices**: https://aws-observability.github.io/observability-best-practices/

---

## Decision Rules

**Observability stack selection:**

- **Prometheus + Grafana**: Open-source, Kubernetes-native, vendor-neutral
- **CloudWatch**: AWS-native, tight integration, managed service
- **Datadog/New Relic**: Comprehensive SaaS, fast setup, higher cost
- **Elastic Stack (ELK)**: Powerful log analytics, full-text search
- **OpenTelemetry**: Vendor-agnostic instrumentation, future-proof

**Metric collection strategy:**

- **Pull-based (Prometheus)**: Good for dynamic environments, service discovery
- **Push-based (CloudWatch)**: Good for ephemeral workloads (Lambda, batch jobs)
- **Hybrid**: Use both based on workload characteristics

**Retention policies:**

- **Metrics**: 15 days high-resolution, 90 days aggregated, 1 year downsampled
- **Logs**: 7-30 days searchable, longer for compliance (1-7 years)
- **Traces**: 7-14 days with sampling (1-10% of traces)

**Escalation conditions:**

- Novel platform without established observability patterns
- Requirements exceed T3 scope (custom data pipeline, ML model training)
- Compliance requirements need specialized tools (SIEM, DLP)

**Abort conditions:**

- Platform restrictions prevent telemetry export
- Conflicting requirements (e.g., "no network egress" with "SaaS monitoring")
- Cost constraints incompatible with retention/granularity requirements

---

## Output Contract

**Required outputs:**

```json
{
  "metrics_config": {
    "type": "object",
    "properties": {
      "platform": "string (prometheus|cloudwatch|datadog)",
      "scrape_configs": "string (YAML configuration)",
      "recording_rules": "string (optional aggregation rules)",
      "retention": "string (duration)"
    }
  },
  "logging_config": {
    "type": "object",
    "properties": {
      "platform": "string (loki|cloudwatch-logs|elasticsearch)",
      "aggregation_config": "string (configuration)",
      "retention_policy": "string (duration or storage class)",
      "structured_format": "string (JSON schema)"
    }
  },
  "tracing_config": {
    "type": "object",
    "properties": {
      "platform": "string (opentelemetry|jaeger|x-ray)",
      "instrumentation": "string (language-specific code)",
      "sampling_rate": "number (0.0 to 1.0)",
      "exporter_config": "string (backend configuration)"
    }
  },
  "dashboards": {
    "type": "array",
    "items": {
      "name": "string",
      "platform": "string (grafana|cloudwatch)",
      "definition": "string (JSON or YAML)"
    }
  },
  "alerting_rules": {
    "type": "array",
    "items": {
      "name": "string",
      "condition": "string (PromQL or equivalent)",
      "severity": "string (critical|warning|info)",
      "notification_channel": "string"
    }
  }
}
```

**Quality guarantees:**

- Metrics cover RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) methods
- Logs are structured with consistent fields (timestamp, level, message, trace_id)
- Traces propagate context across service boundaries
- Alerting rules avoid false positives with appropriate thresholds
- Dashboards provide actionable insights (not vanity metrics)

---

## Examples

**Example: Prometheus scrape config with OpenTelemetry**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'api-service'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['production']
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: api
        action: keep

alerting_rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
```

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens (basic metrics, logs, alerting)
- **T2**: ≤6k tokens (distributed tracing, SLO tracking, advanced alerting)
- **T3**: ≤12k tokens (AI/ML insights, security monitoring, compliance)

**Safety checks:**

- No sensitive data (PII, credentials) in logs or metrics
- Encryption configured for telemetry data in transit and at rest
- Access controls on observability dashboards and data
- Cost controls to prevent runaway metric cardinality

**Auditability:**

- All configuration changes version-controlled
- Alert history retained for incident retrospectives
- Compliance logs immutable and tamper-evident

**Determinism:**

- Same inputs produce identical observability configurations
- Alerting thresholds based on data-driven baselines
- Dashboard definitions reproducible from code

---

## Resources

**Official Documentation** (accessed 2025-10-26T01:33:56-04:00):

- Prometheus: https://prometheus.io/docs/
- OpenTelemetry: https://opentelemetry.io/docs/
- Grafana: https://grafana.com/docs/
- AWS CloudWatch: https://docs.aws.amazon.com/cloudwatch/

**Best Practices** (accessed 2025-10-26T01:33:56-04:00):

- Google SRE Book - Monitoring: https://sre.google/sre-book/monitoring-distributed-systems/
- RED Method: https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/
- USE Method: https://www.brendangregg.com/usemethod.html

**Templates** (in repository `/resources/`):

- Prometheus configurations for common platforms
- OpenTelemetry instrumentation examples
- Grafana dashboard templates
- CloudWatch alarm and dashboard definitions
