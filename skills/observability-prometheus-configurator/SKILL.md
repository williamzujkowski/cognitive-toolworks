---
name: Prometheus Configuration Specialist
slug: observability-prometheus-configurator
description: Configure Prometheus with alerting, recording rules, service discovery (K8s, Consul, EC2), federation, PromQL optimization, and Alertmanager.
capabilities:
  - Prometheus scrape configuration with service discovery
  - Alerting rules with multi-window burn rate patterns
  - Recording rules for pre-computing expensive queries
  - Relabeling for metric filtering and label transformation
  - Federation for multi-DC and cross-service monitoring
  - PromQL query optimization and cardinality management
  - Alertmanager routing and notification configuration
  - Prometheus 3.0+ features (UTF-8, OTLP, Remote Write 2.0)
inputs:
  - Service topology and scrape targets
  - Service discovery mechanism (Kubernetes, Consul, EC2, file_sd)
  - Alert definitions with severity levels
  - Recording rule requirements
  - Alertmanager notification channels (PagerDuty, Slack, email)
  - Federation topology (if multi-DC or cross-service)
  - Cardinality constraints and retention requirements
outputs:
  - prometheus.yml configuration file
  - Alerting rules YAML files
  - Recording rules YAML files
  - Alertmanager configuration
  - Relabeling strategies for cardinality management
  - PromQL query optimization recommendations
  - Federation endpoint configuration
  - Service discovery relabel configs
keywords:
  - prometheus
  - monitoring
  - observability
  - alerting
  - recording-rules
  - service-discovery
  - kubernetes-sd
  - promql
  - federation
  - alertmanager
  - metrics
  - relabeling
  - cardinality
  - burn-rate
  - slo
version: "1.0.0"
owner: cognitive-toolworks
license: MIT
security: "No sensitive data allowed in metric labels. Use relabeling to drop secrets. Avoid high-cardinality labels (user IDs, request IDs)."
links:
  - title: "Prometheus 3.0 Release (November 2024)"
    url: "https://prometheus.io/blog/2024/11/14/prometheus-3-0/"
    accessed: "2025-10-26"
  - title: "Prometheus Configuration Documentation"
    url: "https://prometheus.io/docs/prometheus/latest/configuration/configuration/"
    accessed: "2025-10-26"
  - title: "Prometheus Alerting Best Practices"
    url: "https://prometheus.io/docs/practices/alerting/"
    accessed: "2025-10-26"
  - title: "Prometheus Recording Rules"
    url: "https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/"
    accessed: "2025-10-26"
  - title: "Prometheus Naming Conventions"
    url: "https://prometheus.io/docs/practices/naming/"
    accessed: "2025-10-26"
---

# Prometheus Configuration Specialist

## Purpose & When-To-Use

**Trigger conditions:**

* You need to configure Prometheus for metrics collection from Kubernetes, Consul, EC2, or static targets
* You need to create alerting rules with burn rate calculations or multi-window patterns
* You need to optimize PromQL queries or reduce cardinality for high-volume metrics
* You need to set up federation for multi-datacenter or cross-service monitoring
* You need to configure Alertmanager routing with grouping, inhibition, or multiple receivers
* You need to pre-compute expensive queries using recording rules

**Complements:**

* `observability-stack-configurator`: For overall observability stack design
* `observability-unified-dashboard`: For Grafana dashboard design with Prometheus datasources
* `observability-slo-calculator`: For SLO/error budget definitions that drive alerting rules

**Out of scope:**

* Application instrumentation (use language-specific Prometheus client libraries)
* Long-term metrics storage (use Thanos, Cortex, or Mimir)
* Log aggregation (use Loki or ELK)
* Distributed tracing (use Tempo, Jaeger, or Zipkin)

---

## Pre-Checks

**Time normalization:**

* Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
* Use `NOW_ET` for all access dates in citations

**Verify inputs:**

* ✅ **Required:** At least one scrape target specification (service discovery config or static targets)
* ✅ **Required:** Prometheus version specified (recommend 3.0+ for UTF-8, OTLP, Remote Write 2.0)
* ⚠️ **Optional:** Alert definitions (if alerting is needed)
* ⚠️ **Optional:** Recording rule definitions (if query optimization is needed)
* ⚠️ **Optional:** Alertmanager receivers (PagerDuty, Slack, email, webhook)
* ⚠️ **Optional:** Federation topology (if multi-DC or cross-service monitoring is required)

**Validate service discovery:**

* If `kubernetes_sd_config`: Verify Kubernetes API access and RBAC permissions
* If `consul_sd_config`: Verify Consul agent accessibility and service catalog
* If `ec2_sd_config`: Verify AWS credentials and EC2 instance tags
* If `file_sd_config`: Verify JSON/YAML file path and refresh interval

**Check cardinality constraints:**

* Every unique combination of label key-value pairs creates a new time series
* High-cardinality labels (user IDs, request IDs, timestamps) cause memory/storage issues
* Recommended: <10M active time series per Prometheus instance
* Use `metric_relabel_configs` to drop high-cardinality labels

**Source freshness:**

* Prometheus 3.0 released November 14, 2024 (accessed `NOW_ET`)
* Prometheus 3.5 (upcoming LTS release, 2025)
* Alerting best practices and recording rule conventions stable across versions

**Abort if:**

* No scrape targets specified → **EMIT TODO:** "Specify at least one scrape target (kubernetes_sd, consul_sd, ec2_sd, static_configs)"
* Service discovery config incomplete → **EMIT TODO:** "Provide complete service discovery configuration (API endpoints, credentials, filters)"
* Alert definitions lack severity or description → **EMIT TODO:** "Add severity label and description annotation to all alerts"

---

## Procedure

### T1: Basic Prometheus Setup (≤2k tokens, 80% use case)

**Scenario:** Single service with static targets or file-based service discovery, basic alerting, no recording rules.

**Steps:**

1. **Global Configuration:**
   * Set `scrape_interval: 15s` (balance between data freshness and storage)
   * Set `evaluation_interval: 15s` (how often to evaluate alerting/recording rules)
   * Set `external_labels` for federation or remote write (e.g., `datacenter: us-east-1`)

2. **Scrape Configuration:**
   * Define `job_name` (logical grouping, e.g., `api-service`, `postgres-exporter`)
   * Choose service discovery:
     * **Static:** `static_configs` with `targets: ['localhost:9090']`
     * **File-based:** `file_sd_configs` with `files: ['/etc/prometheus/targets/*.json']`
   * Set `scrape_interval` override if different from global

3. **Basic Alerting Rules:**
   * Create `alerts.yml` with groups
   * Alert on symptoms (high latency, error rate) not causes (CPU, disk)
   * Include severity label (`severity: critical|warning|info`)
   * Add description and summary annotations

4. **Alertmanager Integration:**
   * Configure `alertmanager_config` with `static_configs` pointing to Alertmanager instance
   * Set `send_resolved: true` to notify when alert resolves

**Output:**

* `prometheus.yml` with global config, single scrape job, alerting rules file reference
* `alerts.yml` with 2-5 basic alerts
* No recording rules (not needed for T1 simplicity)

**Token budget:** ≤2000 tokens

---

### T2: Multi-Service Discovery + Recording Rules (≤6k tokens)

**Scenario:** Multiple services with Kubernetes/Consul/EC2 service discovery, recording rules for expensive queries, Alertmanager routing with grouping.

**Steps:**

1. **Service Discovery Configuration:**

   **Kubernetes Service Discovery:**
   * Use `kubernetes_sd_configs` with `role: pod` (discover all pods with `prometheus.io/scrape: "true"` annotation)
   * Relabeling pattern:
     ```yaml
     relabel_configs:
       - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
         action: keep
         regex: true
       - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
         action: replace
         target_label: __metrics_path__
         regex: (.+)
       - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
         action: replace
         target_label: __address__
         regex: ([^:]+)(?::\d+)?;(\d+)
         replacement: $1:$2
       - source_labels: [__meta_kubernetes_namespace]
         action: replace
         target_label: kubernetes_namespace
       - source_labels: [__meta_kubernetes_pod_name]
         action: replace
         target_label: kubernetes_pod_name
     ```
   * Supported roles: `node`, `pod`, `service`, `endpoints`, `ingress` (accessed `NOW_ET`: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)

   **Consul Service Discovery:**
   * Use `consul_sd_configs` with `server: 'consul.service.consul:8500'`
   * Filter by service tags: `tags: ['production', 'monitoring-enabled']`

   **EC2 Service Discovery:**
   * Use `ec2_sd_configs` with AWS region and filters
   * Relabel based on EC2 tags: `__meta_ec2_tag_<tagkey>`

2. **Recording Rules:**

   * **Naming convention:** `level:metric:operations` (accessed `NOW_ET`: https://prometheus.io/docs/practices/naming/)
   * **Level:** Aggregation level (`job`, `instance`, `cluster`)
   * **Metric:** Base metric name
   * **Operations:** Aggregation operations (`sum`, `avg`, `rate`)
   * **Example:**
     ```yaml
     groups:
       - name: api_recording_rules
         interval: 30s
         rules:
           - record: job:http_requests_total:rate5m
             expr: sum(rate(http_requests_total[5m])) by (job)
           - record: job:http_request_duration_seconds:p95
             expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
     ```
   * **Use cases:** Pre-compute dashboard queries, optimize slow PromQL queries, aggregate high-cardinality metrics

3. **Relabeling Strategies:**

   **Metric Relabeling (`metric_relabel_configs`):**
   * Drop high-cardinality labels:
     ```yaml
     metric_relabel_configs:
       - source_labels: [user_id]
         action: labeldrop
         regex: .*
       - source_labels: [__name__]
         action: drop
         regex: 'expensive_metric_.*'
     ```

   **Target Relabeling (`relabel_configs`):**
   * Modify labels before scraping (transform service discovery metadata)

4. **Alerting Rules (Advanced):**

   **Multi-Window Burn Rate Alerts:**
   * Detect fast SLO burn (error budget exhausted in days instead of weeks)
   * Example: 14.4× burn rate (exhaust 30-day budget in 2 days) for critical, 6× for warning
   * **Pattern:**
     ```yaml
     groups:
       - name: slo_alerts
         rules:
           - alert: ErrorBudgetBurn_Critical
             expr: |
               (
                 sum(rate(http_requests_total{status=~"5.."}[1h]))
                 /
                 sum(rate(http_requests_total[1h]))
               ) > (14.4 * 0.001)
             for: 2m
             labels:
               severity: critical
             annotations:
               summary: "Error budget burning 14.4× faster than allowed"
               description: "{{ $labels.job }} has {{ $value | humanizePercentage }} error rate (SLO: 99.9%, budget exhausted in 2 days)"
     ```

   **Symptom-Based Alerts:**
   * Alert on latency, error rate, saturation (not CPU/memory directly)
   * **Golden Signals:** Latency, Traffic, Errors, Saturation
   * Example:
     ```yaml
     - alert: HighLatency
       expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)) > 0.5
       for: 5m
       labels:
         severity: warning
       annotations:
         summary: "High latency on {{ $labels.job }}"
         description: "p95 latency is {{ $value }}s (threshold: 0.5s)"
     ```

5. **Alertmanager Routing:**

   * **Routing tree:** Group alerts by `cluster` + `alertname`, wait 30s for batch
   * **Receivers:** PagerDuty (critical), Slack (warning/info), email (all)
   * **Inhibition:** Suppress lower-severity alerts when higher-severity alerts are firing
   * **Example:**
     ```yaml
     route:
       receiver: 'default-email'
       group_by: ['cluster', 'alertname']
       group_wait: 30s
       group_interval: 5m
       repeat_interval: 4h
       routes:
         - match:
             severity: critical
           receiver: 'pagerduty'
         - match:
             severity: warning
           receiver: 'slack'

     receivers:
       - name: 'pagerduty'
         pagerduty_configs:
           - service_key: '<PD_SERVICE_KEY>'
       - name: 'slack'
         slack_configs:
           - api_url: '<SLACK_WEBHOOK_URL>'
             channel: '#alerts'
             title: '{{ .GroupLabels.alertname }}'
             text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
       - name: 'default-email'
         email_configs:
           - to: 'ops@example.com'

     inhibit_rules:
       - source_match:
           severity: critical
         target_match:
           severity: warning
         equal: ['cluster', 'alertname']
     ```

**Output:**

* `prometheus.yml` with Kubernetes/Consul/EC2 service discovery, relabeling configs
* `recording_rules.yml` with 5-10 recording rules (level:metric:operations naming)
* `alerts.yml` with multi-window burn rate alerts and symptom-based alerts
* `alertmanager.yml` with routing tree, receivers, inhibition rules

**Token budget:** ≤6000 tokens

---

### T3: Enterprise Federation + PromQL Optimization (≤12k tokens)

**Scenario:** Multi-datacenter federation, cardinality management, PromQL query optimization, Prometheus 3.0+ features (UTF-8, OTLP, Remote Write 2.0).

**Steps:**

1. **Federation Configuration:**

   **Hierarchical Federation (Multi-DC):**
   * **Pattern:** Per-datacenter Prometheus servers scrape local services, global Prometheus server federates aggregated metrics
   * **Benefits:** Scales to tens of datacenters and millions of nodes (accessed `NOW_ET`: https://prometheus.io/docs/prometheus/latest/federation/)
   * **Global server config:**
     ```yaml
     scrape_configs:
       - job_name: 'federate-us-east-1'
         scrape_interval: 30s
         honor_labels: true
         metrics_path: '/federate'
         params:
           'match[]':
             - '{job="prometheus"}'
             - '{__name__=~"job:.*"}'  # Only federate aggregated recording rules
         static_configs:
           - targets:
             - 'prometheus-us-east-1:9090'
             - 'prometheus-us-west-2:9090'
     ```

   **Cross-Service Federation:**
   * **Pattern:** Service A Prometheus federates metrics from Service B Prometheus to correlate cross-service metrics
   * **Use case:** Cluster scheduler federating resource usage from multiple service Prometheus servers

2. **PromQL Optimization:**

   **Query Performance Best Practices:**
   * **Filter early:** Use label matchers to narrow time series before aggregation
     * ❌ **Slow:** `sum(http_requests_total)` (aggregates 10k+ time series)
     * ✅ **Fast:** `sum(http_requests_total{job="api-service", status=~"5.."})` (aggregates 10-50 time series)
   * **Avoid broad selectors:** Never use bare metric names (`api_http_requests_total`) without labels
   * **Use recording rules:** Pre-compute expensive queries (accessed `NOW_ET`: https://prometheus.io/docs/prometheus/latest/querying/basics/)
   * **Limit time ranges:** Avoid queries over >24h without recording rules
   * **Example optimized query:**
     ```promql
     # Compute error rate using pre-recorded job-level metrics (fast)
     job:http_requests_total:rate5m{job="api-service", status=~"5.."}
     /
     job:http_requests_total:rate5m{job="api-service"}
     ```

   **Cardinality Management:**
   * **Problem:** High-cardinality labels (user IDs, request IDs) create millions of time series → memory/disk explosion
   * **Detection:** Query `topk(10, count by (__name__)({__name__=~".+"}))` to find high-cardinality metrics
   * **Solutions:**
     1. **Drop labels:** Use `metric_relabel_configs` to remove high-cardinality labels
     2. **Aggregate:** Use recording rules to pre-aggregate high-cardinality metrics
     3. **Sample:** Use `metric_relabel_configs` with `action: drop` to sample metrics
   * **Example cardinality reduction:**
     ```yaml
     metric_relabel_configs:
       # Drop user_id label (high cardinality)
       - source_labels: [user_id]
         action: labeldrop
         regex: .*
       # Keep only 5xx errors (reduce cardinality of status label)
       - source_labels: [status]
         action: keep
         regex: '5..'
     ```

3. **Prometheus 3.0+ Features:**

   **UTF-8 Support (Prometheus 3.0+):**
   * **Feature:** Allows all valid UTF-8 characters in metric and label names (accessed `NOW_ET`: https://prometheus.io/blog/2024/11/14/prometheus-3-0/)
   * **Example:** `http_requests_total{endpoint="用户登录"}` (Chinese characters now valid)
   * **Migration:** UTF-8 mode enabled by default in Prometheus 3.0

   **OpenTelemetry OTLP Receiver (Prometheus 3.0+):**
   * **Feature:** Prometheus can receive OTLP metrics natively
   * **Endpoint:** `/api/v1/otlp/v1/metrics`
   * **Configuration:**
     ```yaml
     otlp:
       protocols:
         http:
           endpoint: 0.0.0.0:9090
     ```
   * **Use case:** Consolidate Prometheus and OpenTelemetry pipelines

   **Remote Write 2.0 (Prometheus 3.0+):**
   * **Feature:** Native support for metadata, exemplars, created timestamps, native histograms
   * **Benefits:** Better interoperability with long-term storage (Thanos, Cortex, Mimir)

4. **Advanced Relabeling Patterns:**

   **Extract Kubernetes Annotations into Labels:**
   ```yaml
   relabel_configs:
     - source_labels: [__meta_kubernetes_pod_annotation_app_version]
       action: replace
       target_label: version
     - source_labels: [__meta_kubernetes_pod_annotation_team]
       action: replace
       target_label: team
   ```

   **Drop Expensive Metrics Based on Name Pattern:**
   ```yaml
   metric_relabel_configs:
     - source_labels: [__name__]
       action: drop
       regex: 'go_.*|process_.*'  # Drop Go runtime metrics to save storage
   ```

5. **Recording Rules for Aggregation:**

   **Multi-Level Aggregation:**
   ```yaml
   groups:
     - name: instance_aggregation
       interval: 30s
       rules:
         # Level 1: Instance-level
         - record: instance:http_requests_total:rate5m
           expr: sum(rate(http_requests_total[5m])) by (instance, job, status)

         # Level 2: Job-level (aggregates Level 1)
         - record: job:http_requests_total:rate5m
           expr: sum(instance:http_requests_total:rate5m) by (job, status)

         # Level 3: Cluster-level (aggregates Level 2)
         - record: cluster:http_requests_total:rate5m
           expr: sum(job:http_requests_total:rate5m) by (status)
   ```

6. **Alertmanager Advanced Features:**

   **Time-Based Routing (Mute Alerts During Maintenance):**
   ```yaml
   route:
     routes:
       - match:
           severity: warning
         mute_time_intervals:
           - weekends
           - maintenance_window

   mute_time_intervals:
     - name: weekends
       time_intervals:
         - weekdays: ['saturday', 'sunday']
     - name: maintenance_window
       time_intervals:
         - times:
           - start_time: '23:00'
             end_time: '01:00'
   ```

   **Grouping by Multiple Labels:**
   ```yaml
   route:
     group_by: ['cluster', 'namespace', 'alertname']
     group_wait: 30s
     group_interval: 5m
     repeat_interval: 12h
   ```

**Output:**

* `prometheus.yml` with federation endpoints, OTLP receiver, Remote Write 2.0
* Multi-level recording rules (instance → job → cluster aggregation)
* Cardinality management relabeling configs
* PromQL optimization recommendations with query examples
* Alertmanager advanced routing (time-based muting, multi-label grouping)

**Token budget:** ≤12000 tokens

---

## Decision Rules

**When to use federation vs remote write:**

* **Federation:** Multi-DC with global aggregation, <10 Prometheus servers
* **Remote Write:** Long-term storage, >10 Prometheus servers, different retention policies

**When to create recording rules:**

* Query execution time >5s on Grafana dashboard
* Query used in multiple dashboards or alerts
* High-cardinality metric needs pre-aggregation (e.g., >100k time series)

**Alert severity assignment:**

* **Critical:** User-impacting outage, page on-call engineer immediately (e.g., API error rate >5%)
* **Warning:** Potential issue, notify Slack, no page (e.g., API latency p95 >500ms)
* **Info:** FYI notification, email only (e.g., deployment completed)

**Service discovery selection:**

* **Kubernetes:** Use `kubernetes_sd_configs` with `role: pod` for dynamic pod discovery
* **Consul:** Use `consul_sd_configs` for VM-based infrastructure with Consul service catalog
* **EC2:** Use `ec2_sd_configs` for AWS instances with consistent tagging
* **File-based:** Use `file_sd_configs` for static infrastructure or external service discovery

**Cardinality limits:**

* **Target:** <10M active time series per Prometheus instance
* **Alert:** If `prometheus_tsdb_symbol_table_size_bytes` >1GB or `prometheus_tsdb_head_series` >10M
* **Action:** Drop high-cardinality labels or aggregate with recording rules

**Abort conditions:**

* Prometheus memory usage >80% of available → reduce cardinality or add recording rules
* Scrape duration >scrape interval → increase interval or optimize exporters
* Alert fatigue (>50 alerts firing) → review alert thresholds and use inhibition rules

---

## Output Contract

**prometheus.yml schema:**

```yaml
global:
  scrape_interval: <duration>
  evaluation_interval: <duration>
  external_labels:
    <label_name>: <label_value>

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['<alertmanager_host>:<port>']

rule_files:
  - 'alerts.yml'
  - 'recording_rules.yml'

scrape_configs:
  - job_name: '<job_name>'
    kubernetes_sd_configs: [...]  # OR consul_sd_configs, ec2_sd_configs, static_configs
    relabel_configs: [...]
    metric_relabel_configs: [...]
```

**alerts.yml schema:**

```yaml
groups:
  - name: <group_name>
    rules:
      - alert: <alert_name>
        expr: <promql_expression>
        for: <duration>
        labels:
          severity: critical|warning|info
        annotations:
          summary: <short_description>
          description: <detailed_description_with_templating>
```

**recording_rules.yml schema:**

```yaml
groups:
  - name: <group_name>
    interval: <duration>
    rules:
      - record: <level>:<metric>:<operations>
        expr: <promql_expression>
        labels:
          <label_name>: <label_value>
```

**alertmanager.yml schema:**

```yaml
route:
  receiver: <default_receiver>
  group_by: [<label_name>, ...]
  group_wait: <duration>
  group_interval: <duration>
  repeat_interval: <duration>
  routes:
    - match:
        <label_name>: <label_value>
      receiver: <receiver_name>

receivers:
  - name: <receiver_name>
    pagerduty_configs: [...]
    slack_configs: [...]
    email_configs: [...]

inhibit_rules:
  - source_match:
      <label_name>: <label_value>
    target_match:
      <label_name>: <label_value>
    equal: [<label_name>, ...]
```

**Required fields:**

* `prometheus.yml`: `global.scrape_interval`, `scrape_configs[].job_name`
* `alerts.yml`: `alert`, `expr`, `labels.severity`, `annotations.summary`
* `recording_rules.yml`: `record`, `expr`
* `alertmanager.yml`: `route.receiver`, `receivers[].name`

**Validation:**

* All PromQL expressions syntactically valid: `promtool check rules <file.yml>`
* Prometheus config valid: `promtool check config prometheus.yml`
* Alertmanager config valid: `amtool check-config alertmanager.yml`

---

## Examples

### Example 1: Kubernetes Service Discovery with Recording Rules

**Scenario:** Scrape all pods with `prometheus.io/scrape: "true"` annotation, create recording rules for API latency.

**prometheus.yml:**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

**recording_rules.yml:**

```yaml
groups:
  - name: api_latency
    interval: 30s
    rules:
      - record: job:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
      - record: job:http_request_duration_seconds:p99
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))
```

---

## Quality Gates

**Token budgets:**

* **T1:** ≤2000 tokens (basic scrape + alerting)
* **T2:** ≤6000 tokens (service discovery + recording rules + Alertmanager routing)
* **T3:** ≤12000 tokens (federation + PromQL optimization + cardinality management)

**Safety:**

* ❌ **Never:** Include secrets in metric labels (passwords, API keys, tokens)
* ❌ **Never:** Use high-cardinality labels (user IDs, request IDs, UUIDs) without aggregation
* ✅ **Always:** Validate PromQL expressions with `promtool check rules`
* ✅ **Always:** Use `metric_relabel_configs` to drop secrets if accidentally exposed

**Auditability:**

* All Prometheus configs in version control (Git)
* Recording rule naming follows `level:metric:operations` convention
* Alert annotations include `summary` and `description` with templating
* Alertmanager routing documented with receiver purposes

**Determinism:**

* Same scrape targets + same relabeling = same time series
* Recording rules evaluated at fixed intervals (deterministic)
* Alert grouping by `cluster` + `alertname` produces predictable batches

**Performance:**

* Scrape duration <80% of scrape interval (avoid missed scrapes)
* PromQL query execution time <5s (use recording rules if slower)
* Cardinality <10M active time series per Prometheus instance
* Alert evaluation time <1s (use recording rules to pre-aggregate)

---

## Resources

**Official Documentation:**

* Prometheus 3.0 announcement (UTF-8, OTLP, Remote Write 2.0): https://prometheus.io/blog/2024/11/14/prometheus-3-0/ (accessed `NOW_ET`)
* Configuration reference: https://prometheus.io/docs/prometheus/latest/configuration/configuration/ (accessed `NOW_ET`)
* Alerting best practices: https://prometheus.io/docs/practices/alerting/ (accessed `NOW_ET`)
* Recording rules: https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/ (accessed `NOW_ET`)
* Naming conventions: https://prometheus.io/docs/practices/naming/ (accessed `NOW_ET`)
* Federation: https://prometheus.io/docs/prometheus/latest/federation/ (accessed `NOW_ET`)

**Tooling:**

* `promtool`: Validate Prometheus configs and PromQL queries
* `amtool`: Validate Alertmanager configs and manage silences
* Prometheus exporters: Node Exporter, Blackbox Exporter, PostgreSQL Exporter, etc.

**Related Skills:**

* `observability-stack-configurator`: Overall observability stack design
* `observability-unified-dashboard`: Grafana dashboard design with Prometheus datasources
* `observability-slo-calculator`: SLO/error budget definitions for alerting rules
* `kubernetes-manifest-generator`: Kubernetes deployment manifests for Prometheus + Alertmanager
