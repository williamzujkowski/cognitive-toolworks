# Runbook Template

## Alert: [Alert Name]

**Severity**: [Critical | Warning | Info]
**Service**: [Service name]
**Last Updated**: [Date]
**Owner**: [Team/Person]

---

## Symptom

[Brief description of what the alert indicates]

Example: "High error rate detected in checkout-service (>5% of requests failing with 5xx errors)"

---

## Impact

**User impact**: [How does this affect end users?]
**Business impact**: [Revenue loss? SLA breach? Compliance risk?]
**Blast radius**: [Which services/features are affected?]

Example:
- Users cannot complete purchases
- Estimated revenue impact: $X/minute
- Affects 100% of checkout attempts

---

## Triage Steps (First 5 minutes)

1. **Check dashboard**: [Link to relevant Grafana/CloudWatch dashboard]
   - Verify error rate spike is real (not false positive)
   - Identify time of onset
   - Check for correlation with deployments or infrastructure changes

2. **Check recent changes**:
   - Review recent deployments: `kubectl rollout history deployment/checkout-service`
   - Check infrastructure changes: AWS console, Terraform state
   - Verify dependency health: database, cache, external APIs

3. **Initial mitigation** (if applicable):
   - Rollback recent deployment: `kubectl rollout undo deployment/checkout-service`
   - Scale up service: `kubectl scale deployment/checkout-service --replicas=10`
   - Enable circuit breaker: [Command/API call]

---

## Investigation

### Key Metrics

- **Error rate**: [Link to metric query]
- **Latency**: [Link to P95/P99 latency]
- **Throughput**: [Link to requests/sec]
- **Dependency status**: [Database, cache, APIs]

### Log Queries

```
# CloudWatch Logs Insights / Loki query
fields @timestamp, @message, trace_id, error
| filter service = "checkout-service"
| filter level = "ERROR"
| sort @timestamp desc
| limit 100
```

### Trace Analysis

- **Jaeger/X-Ray query**: [Link or search parameters]
- **Look for**: Slow database queries, timeout errors, retry storms

### Common Root Causes

1. **Database performance degradation**
   - Check: Connection pool exhaustion, slow queries, replication lag
   - Query: `SHOW PROCESSLIST;` (MySQL) or equivalent

2. **Dependency failure**
   - Check: Payment gateway availability, inventory service health
   - Verify: External API status pages

3. **Resource exhaustion**
   - Check: CPU, memory, disk, network saturation
   - Query: `kubectl top pods -n production`

4. **Configuration change**
   - Check: Recent ConfigMap/Secret updates
   - Verify: Environment variable changes

---

## Resolution

### Immediate Actions

- [ ] Identify root cause from triage/investigation
- [ ] Apply fix or rollback
- [ ] Verify error rate returns to normal (<1%)
- [ ] Confirm SLO compliance recovering

### Fix Verification

- Wait 10 minutes after fix
- Check dashboard: Error rate <1%, latency within SLO
- Sample user journey: Manually test checkout flow
- Monitor error budget consumption rate

---

## Communication

### Internal

- **Slack channel**: #incidents
- **Update frequency**: Every 15 minutes until resolved
- **Status page**: [Link to internal status dashboard]

### External (if customer-facing)

- **Status page**: [Link to public status page]
- **Update template**:
  > "We are investigating elevated error rates affecting checkout. Our team is actively working on a resolution. Updates every 15 minutes."

---

## Post-Incident

### Immediate Follow-up

- [ ] Update incident ticket: [JIRA/Linear link]
- [ ] Schedule PIR (Post-Incident Review) within 48 hours
- [ ] Capture telemetry: Logs, metrics, traces from incident window

### PIR Agenda

- Timeline reconstruction (using observability data)
- Root cause analysis (5 Whys)
- Action items: Prevention, detection improvement, response improvement
- Observability gaps identified during incident

### Prevention

- [ ] Add/improve monitoring to catch earlier
- [ ] Implement automated mitigation (auto-scaling, circuit breakers)
- [ ] Update runbook with lessons learned
- [ ] Schedule reliability improvements (tech debt)

---

## Escalation

**If issue persists after 30 minutes:**

1. **Primary on-call**: [Name] - [Phone/Slack]
2. **Secondary on-call**: [Name] - [Phone/Slack]
3. **Engineering manager**: [Name] - [Phone/Slack]
4. **Vendor support** (if applicable): [Support contact/ticket system]

---

## Related Documentation

- Architecture diagram: [Link]
- Service README: [Link]
- Deployment guide: [Link]
- Previous incidents: [Links to related PIRs]
