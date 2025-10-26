# Post-Mortem Report Template

**Incident ID:** [INC-YYYY-MM-DD-###]
**Incident Type:** [security | outage | disaster-recovery | data-breach | ransomware | ddos | service-degradation]
**Severity:** [P0 | P1 | P2 | P3]
**Date/Time:** [YYYY-MM-DD HH:MM UTC] to [YYYY-MM-DD HH:MM UTC]
**Duration:** [HH:MM total]
**Incident Commander:** [Name/Role]
**Report Author:** [Name]
**Report Date:** [YYYY-MM-DD]

---

## Executive Summary

[2-3 paragraph summary of incident: what happened, customer impact, resolution, key lessons learned]

**Impact Metrics:**
- Customers Affected: [number or percentage]
- Services Impacted: [list]
- Revenue Impact: [$amount or "none"]
- MTTD (Mean Time to Detect): [HH:MM]
- MTTR (Mean Time to Resolve): [HH:MM]
- Data Loss: [yes/no, amount if applicable]

---

## Timeline (All Times UTC)

| Time | Event | Actor | Notes |
|------|-------|-------|-------|
| 14:32 | Initial alert triggered: "API error rate > 10%" | Datadog | Alert sent to PagerDuty |
| 14:35 | On-call engineer acknowledged alert | Jane Doe | Began investigation |
| 14:40 | Identified root cause: database connection pool exhausted | Jane Doe | Logs confirmed max connections hit |
| 14:45 | Containment: Restarted app servers to reset connection pools | Jane Doe | Temporary mitigation |
| 14:50 | Applied fix: Increased database max_connections from 100 to 200 | John Smith (DBA) | Postgres config update |
| 14:55 | Validated recovery: Error rate returned to normal (<0.1%) | Jane Doe | Monitoring confirmed |
| 15:10 | Incident closed | Jane Doe | Post-mortem scheduled |

---

## Root Cause Analysis (5 Whys)

**Problem Statement:** API error rate spiked to 15%, causing customer request failures.

1. **Why did API requests fail?**
   - Database connection pool was exhausted (all 100 connections in use).

2. **Why was the connection pool exhausted?**
   - Application leaked database connections during long-running transactions.

3. **Why did the application leak connections?**
   - Code did not properly close connections in error paths (missing `defer db.Close()` in Go).

4. **Why was this not caught in testing?**
   - Unit tests did not stress-test connection pool under high load or error scenarios.

5. **Why was there no monitoring alert for connection pool exhaustion?**
   - No alert configured for `pg_stat_database.numbackends` metric approaching max_connections.

**Root Cause:** Application code leaked database connections in error paths, combined with insufficient connection pool monitoring, leading to connection exhaustion under load.

---

## Detection

**How was the incident detected?**
- [ ] Automated monitoring alert (specify: Datadog error rate threshold)
- [ ] Customer report (ticket/support channel)
- [ ] Internal user report
- [ ] Security scan/audit
- [ ] Other: ___

**Detection Delay:** [time between incident start and detection]
**Improvements Needed:** [e.g., "Earlier detection via connection pool monitoring"]

---

## Containment & Resolution

**Containment Actions:**
1. Restarted application servers to reset connection pools (temporary fix)
2. Increased database max_connections from 100 to 200 (short-term capacity increase)

**Eradication Actions:**
1. Fixed Go code to properly close DB connections in all error paths (`defer db.Close()`)
2. Added connection pool monitoring alerts (PagerDuty alert when >80% pool utilization)
3. Implemented connection leak detection in CI/CD pipeline (static analysis)

**Recovery Actions:**
1. Deployed code fix to production via canary deployment (5% → 25% → 100%)
2. Validated fix with load testing (simulated 2x peak traffic)
3. Monitored for 24 hours post-deployment (no recurrence)

---

## Impact Assessment

**Customer Impact:**
- Total customers affected: 12,000 (15% of active users)
- Symptoms: API request failures, timeout errors, "Database connection error" messages
- Duration: 23 minutes (14:32 - 14:55 UTC)
- Severity: P1 (high impact, short duration)

**Business Impact:**
- Revenue loss: Estimated $5,000 (failed transactions during outage)
- SLA breach: Yes (99.9% uptime SLA, monthly budget consumed)
- Reputational: Minor (resolved quickly, transparent communication via status page)

**Data Impact:**
- Data loss: None
- Data breach: No
- Compliance impact: None

---

## Action Items

| ID | Description | Owner | Priority | Due Date | Status |
|----|-------------|-------|----------|----------|--------|
| AI-1 | Fix database connection leak in error paths (all services) | Jane Doe | P0 | 2025-10-27 | Completed |
| AI-2 | Add connection pool monitoring alerts (>80% utilization) | John Smith | P0 | 2025-10-28 | In Progress |
| AI-3 | Implement connection leak detection in CI/CD (static analysis) | Security Team | P1 | 2025-11-03 | Planned |
| AI-4 | Load test all services under 2x peak traffic | SRE Team | P1 | 2025-11-10 | Planned |
| AI-5 | Document database connection best practices for dev team | Jane Doe | P2 | 2025-11-15 | Planned |
| AI-6 | Review and tune database connection pool settings (all DBs) | DBA Team | P2 | 2025-11-20 | Planned |

---

## Lessons Learned

**What Went Well:**
- Fast detection via automated monitoring (3 minutes from incident to alert)
- Clear escalation path and rapid DBA engagement
- Effective temporary mitigation (restarted app servers) allowed time for proper fix
- Transparent customer communication via status page
- No-blame post-mortem culture encouraged honest discussion

**What Went Wrong:**
- Connection pool exhaustion was preventable (known anti-pattern)
- No proactive monitoring for connection pool metrics
- Load testing did not simulate error path scenarios
- Code review missed missing connection cleanup in error paths

**Where We Got Lucky:**
- Incident occurred during business hours (fast response)
- DBA was available immediately (no escalation delay)
- Fix was simple (config change + code fix)
- No data loss or security impact

**Opportunities for Improvement:**
1. Implement connection pool monitoring across all databases (proactive alerting)
2. Enhance load testing to include error injection and connection leak scenarios
3. Add static analysis to CI/CD to detect resource leaks (connections, file handles, goroutines)
4. Create database connection best practices guide for developers
5. Conduct quarterly chaos engineering exercises to test incident response

---

## Compliance & Reporting

**Regulatory Reporting Required:**
- [ ] HIPAA breach notification (60 days) - **N/A** (no PHI affected)
- [ ] PCI-DSS incident report - **N/A** (no payment data affected)
- [ ] SOC2 CC7.3 documentation - **Required** (incident communications documented)
- [ ] FedRAMP IR-6 reporting to Agency - **N/A** (not FedRAMP environment)
- [ ] GDPR breach notification (72 hours) - **N/A** (no personal data breach)

**Internal Reporting:**
- [x] Engineering leadership notified
- [x] Customer success team briefed
- [x] Incident retrospective scheduled (2025-10-26)
- [x] Status page updated with post-mortem summary

---

## Appendices

**Appendix A: Relevant Logs**
[Link to log aggregation query or attach sanitized log excerpts]

**Appendix B: Metrics & Graphs**
[Embed or link to monitoring dashboards showing error rates, connection pool usage, latency]

**Appendix C: Code Changes**
[Link to GitHub PR or commit SHA for code fixes]

**Appendix D: Related Incidents**
[List similar past incidents, if any, and their resolutions]

---

**Approval:**
- Incident Commander: ___________________________ Date: ___________
- Engineering Manager: _________________________ Date: ___________
- CISO (if security incident): _________________ Date: ___________
