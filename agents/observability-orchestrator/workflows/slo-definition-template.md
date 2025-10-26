# SLO Definition Worksheet

## Service Information

- **Service name**: [e.g., checkout-service]
- **Business criticality**: [Critical | Important | Standard]
- **Service type**: [User-facing | Internal API | Data processing | Background job]
- **Owner/team**: [Team responsible]

## SLA Commitments (if applicable)

- **Availability SLA**: [e.g., 99.9%]
- **Latency SLA**: [e.g., P95 < 300ms]
- **Other commitments**: [Throughput, freshness, etc.]

## SLI Definition

### Availability SLI

- **Measurement**: [PromQL/CloudWatch query]
- **Calculation**: [Good requests / Total requests]
- **Exclusions**: [Planned maintenance, client errors (4xx)]

### Latency SLI

- **Percentile**: [P50 | P95 | P99]
- **Measurement**: [PromQL/CloudWatch query]
- **Target**: [e.g., P95 < 200ms]

### Error Rate SLI

- **Definition**: [Server errors (5xx) / Total requests]
- **Measurement**: [PromQL/CloudWatch query]
- **Target**: [e.g., <0.1%]

## SLO Targets (derived from SLA - error budget)

- **Availability SLO**: [e.g., 99.5% from 99.9% SLA]
- **Error budget**: [e.g., 0.4% = 40.32 min/month]
- **Measurement window**: [28-day rolling | Calendar month]

## Burn Rate Alerts

### Fast Burn Alert (1-hour window)
- **Threshold**: [2% of monthly budget consumed in 1 hour]
- **Severity**: Critical
- **Notification**: PagerDuty

### Slow Burn Alert (6-hour window)
- **Threshold**: [5% of monthly budget consumed in 6 hours]
- **Severity**: Warning
- **Notification**: Slack

## Error Budget Policy

- **>50% budget remaining**: Normal change velocity
- **20-50% budget remaining**: Caution; increase monitoring
- **<20% budget remaining**: Freeze non-critical changes
- **Budget exhausted**: Emergency change freeze; focus on reliability

## Review Cadence

- **Weekly**: Error budget status review
- **Monthly**: SLO target adjustment based on business needs
- **Quarterly**: SLI relevance validation
