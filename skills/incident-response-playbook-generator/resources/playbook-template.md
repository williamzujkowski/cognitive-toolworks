# Incident Response Playbook Template

**Incident Type:** [security | outage | disaster-recovery | data-breach | ransomware | ddos | service-degradation]
**Severity:** [P0 | P1 | P2 | P3]
**Last Updated:** [YYYY-MM-DD]
**Owner:** [Team/Role]

---

## Phase 1: Preparation (Pre-Incident)

**Objective:** Ensure tools, access, and team readiness before incidents occur.

**Actions:**
- [ ] Verify on-call rotation configured (PagerDuty/Opsgenie)
- [ ] Confirm access to logging/monitoring systems (Datadog, Splunk, CloudWatch)
- [ ] Test incident communication channels (#incidents Slack, status page)
- [ ] Validate backup/DR procedures (RTO: ___, RPO: ___)
- [ ] Review escalation matrix and contact list
- [ ] Ensure forensic tools available (if security incident)

**Tools Required:**
- Monitoring: [Datadog, Prometheus, CloudWatch, etc.]
- Communication: [Slack, Zoom, PagerDuty, status page]
- Access: [VPN, SSH keys, admin credentials in vault]

---

## Phase 2: Detection & Analysis

**Objective:** Identify and scope the incident rapidly.

**Detection Triggers:**
- Alert: [Specific alert name/condition]
- Symptoms: [User reports, metrics, error rates]
- Monitoring query: [Example: `error_rate{service="api"} > 5%`]

**Analysis Steps:**
1. [ ] Verify alert is not false positive
2. [ ] Determine scope: affected services, users, regions
3. [ ] Check recent changes: deployments, config changes, infrastructure updates
4. [ ] Gather evidence: logs, metrics, traces, screenshots
5. [ ] Classify incident type and assign severity (P0/P1/P2/P3)

**Duration Estimate:** 5-15 minutes (P0), 15-30 minutes (P1/P2)

---

## Phase 3: Containment

**Objective:** Stop the incident from spreading while preserving evidence.

**Short-Term Containment (minutes to hours):**
- [ ] Isolate affected systems (network segmentation, firewall rules)
- [ ] Disable compromised accounts/credentials (if security incident)
- [ ] Implement rate limiting or traffic shaping (if DDoS/overload)
- [ ] Fail over to backup/DR site (if outage)
- [ ] Preserve forensic evidence (logs, memory dumps, disk snapshots)

**Long-Term Containment (hours to days):**
- [ ] Apply temporary patches or workarounds
- [ ] Monitor for incident recurrence or lateral movement
- [ ] Maintain service availability via degraded mode if necessary

**Rollback Decision:** If recent deployment suspected, execute rollback procedure (see runbook)

---

## Phase 4: Eradication

**Objective:** Remove root cause and prevent recurrence.

**Actions:**
- [ ] Identify root cause (5 Whys, Fishbone diagram)
- [ ] Remove malicious code, backdoors, or vulnerabilities (if security)
- [ ] Patch software, update configurations, fix infrastructure issues
- [ ] Rebuild compromised systems from clean baseline
- [ ] Validate fix in staging environment before production deployment

**Validation:**
- [ ] Root cause confirmed through testing
- [ ] No residual malicious activity detected
- [ ] Monitoring shows normal service behavior

---

## Phase 5: Recovery

**Objective:** Restore full service operation and validate health.

**Actions:**
- [ ] Restore services from backups (if data loss occurred)
- [ ] Re-enable disabled accounts/features incrementally
- [ ] Monitor for abnormal behavior during recovery
- [ ] Perform health checks: [list service-specific checks]
- [ ] Validate data integrity and consistency
- [ ] Gradually increase traffic to restored services (canary deployment)

**Success Criteria:**
- [ ] All services operating at normal capacity
- [ ] Error rates within SLO thresholds
- [ ] Customer impact eliminated
- [ ] Monitoring alerts cleared

---

## Phase 6: Post-Incident Activity

**Objective:** Learn from incident and improve processes.

**Actions:**
- [ ] Conduct post-mortem within 48 hours (no-blame culture)
- [ ] Document timeline: detection, containment, recovery milestones
- [ ] Perform root cause analysis (5 Whys, RCA template)
- [ ] Calculate metrics: MTTD, MTTR, customer impact, revenue impact
- [ ] Create action items with owners and due dates
- [ ] Update playbooks/runbooks based on lessons learned
- [ ] Share findings with team and stakeholders

**Compliance Reporting (if applicable):**
- [ ] HIPAA breach notification to HHS (within 60 days if PHI affected)
- [ ] PCI-DSS incident report to acquiring bank and card brands
- [ ] SOC2 documentation per CC7.3 requirement
- [ ] FedRAMP incident report to Agency within 1 hour (P0/P1)

---

## Escalation Matrix

| Severity | Initial Contact | Escalation Time | Escalation Contact |
|----------|----------------|-----------------|-------------------|
| P0       | On-call Engineer (PagerDuty) | 15 minutes | VP Engineering, CISO (if security) |
| P1       | On-call Engineer | 30 minutes | Engineering Manager, Security Lead |
| P2       | On-call Engineer | 2 hours | Team Lead |
| P3       | Ticket to team queue | Next business day | N/A |

**Contact Methods:**
- PagerDuty: [integration URL]
- Slack: #incidents channel
- Email: incidents@company.com
- Phone: [on-call hotline]

---

## Communication Plan

**Internal Stakeholders:**
- Engineering: Real-time updates in #incidents Slack
- Support: Incident summary and customer-facing talking points
- Executives: Email summary at incident start, resolution, post-mortem

**External Communication:**
- Status Page: Update within 15 minutes of P0/P1 detection
- Customer Notifications: Email/in-app if data breach or extended outage
- Regulatory: As required by HIPAA, PCI-DSS, FedRAMP

**Update Cadence:**
- P0: Every 15-30 minutes until resolved
- P1: Hourly
- P2: Every 4 hours or daily
- P3: Daily or upon resolution
