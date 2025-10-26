---
name: "Incident Response Playbook Generator"
slug: "resilience-incident-generator"
description: "Generate incident response playbooks for security incidents, outages, and disaster recovery with NIST SP 800-61 compliance and escalation paths."
capabilities:
  - Security incident response playbook generation
  - Production outage runbook creation
  - Disaster recovery scenario planning
  - Escalation matrix design
  - Post-mortem template generation
  - NIST SP 800-61 lifecycle compliance
  - On-call rotation and paging integration
  - Communication plan templates
inputs:
  - incident_type: "security | outage | disaster-recovery | data-breach | ransomware | ddos | service-degradation (string)"
  - severity_level: "P0 (critical) | P1 (high) | P2 (medium) | P3 (low) (string, default: P1)"
  - service_context: "service name, architecture, dependencies (object, optional)"
  - compliance_requirements: "NIST, SOC2, HIPAA, PCI-DSS (array, optional)"
  - tier: "T1 (template) | T2 (detailed playbook) (string, default: T1)"
outputs:
  - playbook: "NIST SP 800-61 structured playbook with phases"
  - escalation_matrix: "contact list with escalation thresholds"
  - runbook: "step-by-step remediation procedures"
  - post_mortem_template: "structured incident report template"
  - communication_plan: "stakeholder notification templates"
keywords:
  - incident-response
  - disaster-recovery
  - playbook
  - runbook
  - nist-800-61
  - security-incident
  - outage
  - escalation
  - post-mortem
  - on-call
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final
  - https://www.atlassian.com/incident-management/incident-response
  - https://response.pagerduty.com/
  - https://www.sans.org/white-papers/33901/
  - https://cloud.google.com/architecture/incident-response
  - https://incidentresponse.com/playbooks/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Security incident detected (malware, data breach, unauthorized access, ransomware, DDoS)
- Production outage or service degradation impacting customers
- Disaster recovery event (data center failure, regional outage, natural disaster)
- Post-incident review requiring playbook formalization
- Compliance requirement to document incident response procedures (SOC2, FedRAMP, HIPAA, PCI-DSS)
- New service launch requiring incident runbooks
- On-call rotation setup needing escalation paths

**Not for:**
- Real-time incident coordination (use incident management platforms)
- Automated incident detection (use monitoring/alerting systems)
- Forensic analysis execution (provides methodology only)
- Legal incident disclosure decisions (consult legal counsel)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `incident_type` must be: security, outage, disaster-recovery, data-breach, ransomware, ddos, service-degradation
- `severity_level` must be: P0, P1, P2, or P3
- `service_context` (if provided) must include: service_name, team_owner, dependencies
- `compliance_requirements` must be valid framework identifiers
- `tier` must be: T1 or T2

**Source freshness:**
- NIST SP 800-61 Rev 2 (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final - Computer Security Incident Handling Guide
- Atlassian Incident Management (accessed 2025-10-25T21:30:36-04:00): https://www.atlassian.com/incident-management/incident-response
- PagerDuty Incident Response (accessed 2025-10-25T21:30:36-04:00): https://response.pagerduty.com/
- SANS Incident Handler's Handbook (accessed 2025-10-25T21:30:36-04:00): https://www.sans.org/white-papers/33901/

**Dependency validation:**
- Security incidents leverage: security-assessment-framework (for threat context)
- No hard dependencies for T1 (template generation)

---

## Procedure

### T1: Playbook Template (≤2k tokens)

**Fast path for 80% of standard playbook needs:**

1. **Incident classification:**
   - Map `incident_type` to NIST SP 800-61 category
   - Assign severity level based on `severity_level` input
   - Identify compliance requirements (if any)

2. **Generate playbook structure:**
   - **Phase 1: Preparation** - Pre-incident setup (tools, contacts, access)
   - **Phase 2: Detection & Analysis** - Incident identification and scoping
   - **Phase 3: Containment** - Short-term and long-term containment steps
   - **Phase 4: Eradication** - Root cause removal
   - **Phase 5: Recovery** - Service restoration and validation
   - **Phase 6: Post-Incident Activity** - Lessons learned and documentation

3. **Create escalation matrix:**
   - Define escalation thresholds by severity (P0 ≤15min, P1 ≤30min, P2 ≤2hr, P3 ≤1day)
   - Template contact roles: Incident Commander, Tech Lead, Communications Lead, Executive Sponsor
   - Include paging instructions (PagerDuty, Opsgenie, custom)

4. **Output deliverables:**
   - Playbook markdown document (NIST SP 800-61 aligned)
   - Escalation matrix CSV/JSON
   - Post-mortem template with 5 Whys framework

**Token budget:** T1 ≤2k tokens (template only, no deep context)

---

### T2: Detailed Playbook with Service Context (≤6k tokens)

**Extended path for service-specific, compliance-driven playbooks:**

1. **Enhanced incident analysis (extends T1):**
   - Analyze `service_context` to identify critical dependencies
   - Map service architecture to failure modes (single points of failure, cascading failures)
   - Identify compliance-specific requirements (HIPAA breach notification timelines, PCI-DSS forensic preservation)

2. **Service-specific runbook generation:**
   - Create detailed remediation steps for common failure scenarios
   - Include rollback procedures and health check validation
   - Add monitoring query examples (Prometheus, Datadog, CloudWatch)
   - Document safe restart procedures and dependency startup order

3. **Compliance integration:**
   - NIST SP 800-61: Map playbook phases to incident handling lifecycle
   - SOC2 CC7.3: Document incident response communications
   - HIPAA: Add breach notification timelines (60-day requirement)
   - PCI-DSS 12.10: Include forensic evidence preservation steps
   - FedRAMP: Reference IR-4 and IR-6 controls from NIST SP 800-53

4. **Communication plan generation:**
   - Internal stakeholder notification templates (engineering, support, executives)
   - External communication templates (customer status page, regulatory notifications)
   - Severity-based communication cadence (P0: every 30min, P1: hourly, P2: daily)

5. **Post-mortem template customization:**
   - Include service-specific incident timeline
   - Root cause analysis framework (5 Whys, Fishbone diagram)
   - Action items with owners and due dates
   - Metrics: MTTD (Mean Time to Detect), MTTR (Mean Time to Resolve), customer impact

6. **Decision rules for escalation:**
   - Auto-escalate if incident duration exceeds: P0=30min, P1=2hr, P2=8hr
   - Auto-escalate if customer impact exceeds: P0=any, P1=10%, P2=25%
   - Invoke disaster recovery if: data center failure, regional outage, ransomware with data encryption

**Token budget:** T2 ≤6k tokens (includes service context, compliance, and communication plans)

---

## Decision Rules

**Incident type routing:**
- `security | data-breach | ransomware` → Include forensic preservation steps, consider invoking security-assessment-framework
- `outage | service-degradation` → Focus on MTTR reduction, rollback procedures, health checks
- `disaster-recovery` → Invoke DR site failover procedures, RTO/RPO validation
- `ddos` → Include traffic analysis, rate limiting, upstream provider coordination

**Severity thresholds (auto-escalation triggers):**
- **P0 (critical):** Customer-facing impact, data breach, ransomware → Escalate to VP/C-level within 15 minutes
- **P1 (high):** Partial service degradation, security incident contained → Escalate to Director within 30 minutes
- **P2 (medium):** Internal systems impacted, no customer impact → Escalate to Manager within 2 hours
- **P3 (low):** Minor issues, no service impact → Standard on-call escalation

**Compliance-driven requirements:**
- HIPAA data breach → Invoke 60-day breach notification requirement, add HHS reporting steps
- PCI-DSS incident → Add forensic investigation and PCI QSA notification
- SOC2 incident → Document communications per CC7.3 requirement
- FedRAMP incident → Report to Agency within 1 hour for P0 incidents per IR-6(1)

**Abort conditions:**
- If `incident_type` is unknown/invalid → Request clarification
- If `service_context` missing for T2 → Downgrade to T1 or request architecture details
- If compliance requirements conflict → Flag for manual review and legal consultation

---

## Output Contract

**Required fields (all tiers):**

```yaml
playbook:
  incident_type: string
  severity: "P0" | "P1" | "P2" | "P3"
  nist_phases:
    - phase: "Preparation" | "Detection & Analysis" | "Containment" | "Eradication" | "Recovery" | "Post-Incident"
      steps: array[string]
      duration_estimate: string
      success_criteria: string
  escalation_matrix:
    - role: string
      contact_method: string
      escalation_threshold: string
  post_mortem_template:
    incident_summary: string
    timeline: array[{timestamp, event, actor}]
    root_cause: string
    impact: {customers_affected, duration, revenue_impact}
    action_items: array[{owner, description, due_date, priority}]

runbook: # T2 only
  service_name: string
  failure_modes: array[{scenario, symptoms, remediation_steps}]
  rollback_procedure: array[string]
  health_checks: array[{name, command, expected_result}]
  dependencies: array[{service, startup_order, health_endpoint}]

communication_plan: # T2 only
  internal_stakeholders: array[{role, notification_threshold, channel}]
  external_communication: array[{audience, template, approval_required}]
  status_page_updates: {cadence, template}
```

**Format:** JSON or YAML (consumer specifies)

**Guarantees:**
- All playbooks follow NIST SP 800-61 Rev 2 incident handling lifecycle
- Escalation thresholds are severity-appropriate and time-bounded
- Post-mortem templates include 5 Whys or equivalent root cause analysis
- Compliance requirements mapped to specific playbook steps

---

## Examples

**Input:**
```json
{
  "incident_type": "data-breach",
  "severity_level": "P0",
  "compliance_requirements": ["HIPAA", "SOC2"],
  "tier": "T1"
}
```

**Output (abbreviated):**
```yaml
playbook:
  incident_type: data-breach
  severity: P0
  nist_phases:
    - phase: Containment
      steps:
        - Isolate affected systems from network
        - Preserve forensic evidence (logs, memory dumps)
        - Revoke compromised credentials
      duration_estimate: 30-60 minutes
    - phase: Post-Incident
      steps:
        - HIPAA breach notification to HHS within 60 days
        - SOC2 CC7.3 communication documentation
  escalation_matrix:
    - {role: CISO, contact: PagerDuty, threshold: "15 min"}
    - {role: Legal, contact: Email, threshold: "30 min"}
```

---

## Quality Gates

**Token budgets:**
- **T1 ≤2k tokens:** Template-based playbook generation, no deep service context
- **T2 ≤6k tokens:** Service-specific runbooks with compliance integration
- **T3:** Not implemented (incident response is sufficiently covered by T1/T2 tiers)

**Safety:**
- No embedded credentials or API keys in playbooks
- No PII in example scenarios
- Compliance requirements are technical controls only (not legal advice)

**Auditability:**
- All NIST SP 800-61 citations include access date = NOW_ET
- Compliance mappings traceable to source frameworks
- Escalation thresholds based on industry standards (PagerDuty, Atlassian)

**Determinism:**
- Same inputs → same playbook structure
- Escalation thresholds are severity-based and predictable
- NIST phases always in lifecycle order: Preparation → Detection → Containment → Eradication → Recovery → Post-Incident

**Validation:**
- Playbook must include all 6 NIST SP 800-61 phases
- Escalation matrix must define contact methods and thresholds
- Post-mortem template must include timeline, root cause, and action items

---

## Resources

**Primary sources (NIST SP 800-61 compliance):**
- NIST SP 800-61 Rev 2: Computer Security Incident Handling Guide (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final
- NIST SP 800-53 Rev 5: IR-4 (Incident Handling), IR-6 (Incident Reporting) (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

**Industry best practices:**
- Atlassian Incident Management Handbook (accessed 2025-10-25T21:30:36-04:00): https://www.atlassian.com/incident-management/incident-response
- PagerDuty Incident Response Documentation (accessed 2025-10-25T21:30:36-04:00): https://response.pagerduty.com/
- Google SRE Book: Managing Incidents (accessed 2025-10-25T21:30:36-04:00): https://sre.google/sre-book/managing-incidents/
- SANS Incident Handler's Handbook (accessed 2025-10-25T21:30:36-04:00): https://www.sans.org/white-papers/33901/

**Compliance frameworks:**
- HIPAA Breach Notification Rule (accessed 2025-10-25T21:30:36-04:00): https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html
- PCI DSS v4.0 Requirement 12.10 (accessed 2025-10-25T21:30:36-04:00): https://www.pcisecuritystandards.org/document_library
- SOC2 Trust Services Criteria CC7.3 (accessed 2025-10-25T21:30:36-04:00): https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html

**Templates and tools:**
- See `/skills/resilience-incident-generator/resources/` for:
  - `playbook-template.md` - NIST SP 800-61 aligned playbook structure
  - `escalation-matrix.csv` - Contact escalation template
  - `post-mortem-template.md` - 5 Whys root cause analysis template
  - `runbook-template.md` - Service-specific runbook structure
