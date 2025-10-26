---
name: Compliance Automation Engine
slug: compliance-automation-engine
description: Automate compliance checks for NIST, FedRAMP, FISMA, GDPR, HIPAA, and fintech regulations with OSCAL artifact generation and evidence validation.
capabilities:
  - Cross-framework control mapping (NIST CSF, 800-53, FedRAMP, FISMA, GDPR, HIPAA)
  - OSCAL artifact generation (SSP, SAP, SAR, POA&M)
  - Automated evidence collection and validation
  - Gap analysis and remediation planning
  - Continuous compliance monitoring
  - ATO (Authority to Operate) preparation support
inputs:
  - framework: compliance framework identifier (nist-csf, nist-800-53, fedramp, fisma, gdpr, hipaa, pci-dss)
  - control_baseline: baseline level (low, moderate, high for NIST/FedRAMP)
  - evidence_path: directory path containing compliance evidence artifacts
  - system_context: JSON describing system boundaries, data flows, components
  - validation_mode: quick, standard, comprehensive (maps to T1/T2/T3)
outputs:
  - compliance_report: structured JSON with control status, gaps, evidence mapping
  - oscal_artifacts: generated OSCAL documents (format depends on framework)
  - remediation_plan: prioritized list of gaps with recommended actions
  - dashboard_data: metrics for continuous compliance monitoring
keywords:
  - compliance
  - automation
  - nist
  - fedramp
  - fisma
  - oscal
  - gdpr
  - hipaa
  - controls
  - ato
  - security
  - governance
version: 1.0.0
owner: cognitive-toolworks
license: CC0-1.0
security: public; no secrets or PII; handles compliance metadata only
links:
  - https://www.nist.gov/cyberframework
  - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
  - https://www.fedramp.gov/
  - https://pages.nist.gov/OSCAL/
  - https://gdpr.eu/
  - https://www.hhs.gov/hipaa/
  - https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final
  - https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.xlsx
---

## Purpose & When-To-Use

**Trigger conditions:**

* Preparing for Authority to Operate (ATO) or certification under FedRAMP, FISMA, HIPAA, GDPR, or other frameworks
* Conducting compliance audit or assessment requiring control mapping and evidence validation
* Implementing continuous compliance monitoring for regulatory requirements
* Generating OSCAL artifacts (SSP, SAP, SAR, POA&M) for submission or review
* Performing gap analysis between current state and required control baseline
* Responding to audit findings or compliance violations requiring remediation tracking
* Migrating between compliance frameworks (e.g., NIST 800-53 to FedRAMP baseline)

**Use this skill when:**

* System requires compliance certification under one or more federal/industry regulations
* Organization needs automated control mapping across multiple frameworks
* Manual compliance tracking has become error-prone or resource-intensive
* Auditors or assessors require standardized OSCAL-formatted documentation
* Continuous monitoring is required for ongoing ATO maintenance
* Control inheritance from cloud providers (AWS, Azure, GCP) needs mapping

**Do NOT use this skill for:**

* Legal interpretation of regulations (requires qualified counsel)
* Privacy impact assessments requiring human judgment
* First-time framework selection (use architecture decision framework instead)
* Systems not subject to regulatory compliance requirements

## Pre-Checks

**Time normalization:**
```
NOW_ET = <NIST time.gov semantics, America/New_York, ISO-8601>
Example: 2025-10-25T21:30:36-04:00
```

**Input validation:**

* `framework` must be one of: `nist-csf`, `nist-800-53`, `fedramp`, `fisma`, `gdpr`, `hipaa`, `pci-dss`, `sox`, `fintech-composite`
* `control_baseline` required for NIST/FedRAMP frameworks: `low`, `moderate`, `high`
  * FedRAMP Low: 125 controls (accessed 2025-10-25T21:30:36-04:00, [source](https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.xlsx))
  * FedRAMP Moderate: 325 controls
  * FedRAMP High: 421 controls
* `evidence_path` must exist and be readable; skip if empty (report as gap)
* `system_context` must include at minimum: `system_name`, `system_id`, `boundary_description`, `authorization_boundary`
* `validation_mode` defaults to `standard` (T2) if not specified

**Framework version checks:**

* NIST SP 800-53 current version: Rev 5 (September 2020, accessed 2025-10-25T21:30:36-04:00, [source](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final))
* OSCAL current version: 1.1.2 (accessed 2025-10-25T21:30:36-04:00, [source](https://pages.nist.gov/OSCAL/reference/latest/complete/))
* FedRAMP baseline version: Rev 5 baseline (2022, accessed 2025-10-25T21:30:36-04:00)
* GDPR: effective May 25, 2018; no version changes (accessed 2025-10-25T21:30:36-04:00)
* HIPAA Security Rule: 45 CFR Parts 160, 162, 164 (accessed 2025-10-25T21:30:36-04:00, [source](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html))

**Dependency checks:**

* If OSCAL generation requested: validate OSCAL schema availability
* If FedRAMP: verify access to FedRAMP template repository
* If evidence validation: check for supported evidence formats (PDF, JSON, YAML, logs)

## Procedure

### Tier 1: Quick Compliance Check (≤2k tokens)

**Goal:** Rapid assessment of control coverage and critical gaps for 80% use cases

**Target scenarios:**
* Quick readiness check before formal assessment
* Dashboard updates for continuous monitoring
* High-level gap identification

**Steps:**

1. **Load control baseline**
   * Fetch applicable controls for `framework` + `control_baseline`
   * Example: FedRAMP Moderate = 325 controls from AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PS, RA, SA, SC, SI, SR families
   * Source: NIST SP 800-53 Rev 5 catalog (accessed 2025-10-25T21:30:36-04:00)

2. **Scan evidence directory**
   * Count evidence files mapped to controls (via naming convention or manifest)
   * Flag controls with zero evidence as critical gaps

3. **Calculate coverage metrics**
   * `coverage_pct = (controls_with_evidence / total_controls) * 100`
   * `critical_gaps = controls with family priority 1 and zero evidence`
   * `status = "ready" if coverage_pct >= 95 else "gaps-identified"`

4. **Generate quick report**
   ```json
   {
     "framework": "fedramp-moderate",
     "total_controls": 325,
     "implemented": 310,
     "in_progress": 10,
     "not_started": 5,
     "coverage_pct": 95.4,
     "critical_gaps": ["AC-2(1)", "AU-6(1)", "IR-4"],
     "status": "gaps-identified",
     "next_action": "address critical gaps before full assessment"
   }
   ```

**Token budget:** ~1800 tokens (control list loading + basic logic)

### Tier 2: Standard Compliance Assessment (≤6k tokens)

**Goal:** Detailed control-by-control validation with evidence mapping and OSCAL SSP generation

**Target scenarios:**
* Pre-audit readiness assessment
* OSCAL SSP document generation for submission
* Detailed gap analysis with remediation recommendations

**Steps:**

1. **Load and normalize controls**
   * Fetch full control catalog for framework
   * Apply control baseline overlay (low/moderate/high)
   * Cross-reference with framework-specific requirements (e.g., FedRAMP parameters)

2. **Evidence collection and mapping**
   * Scan `evidence_path` for artifacts
   * Parse evidence manifests (JSON/YAML) linking evidence to controls
   * Validate evidence freshness (warn if >90 days old)
   * Map evidence types: policies, procedures, configurations, logs, screenshots, test results

3. **Control status assessment**
   * For each control:
     * Check evidence existence and quality
     * Validate against control implementation requirements
     * Determine status: `implemented`, `partially-implemented`, `planned`, `not-applicable`
     * Document inheritance (e.g., from AWS GovCloud, Azure Government)

4. **Gap analysis**
   * Identify controls lacking sufficient evidence
   * Categorize gaps by severity:
     * **Critical:** High-impact controls (AC, IA, SC families) with zero evidence
     * **High:** Moderate-impact controls missing required evidence types
     * **Medium:** Minor evidence gaps or outdated artifacts
     * **Low:** Documentation formatting issues

5. **Generate OSCAL SSP (if requested)**
   * Construct OSCAL 1.1.2 compliant SSP JSON
   * Include sections:
     * `metadata`: system info, responsible parties, publication timestamp (NOW_ET)
     * `import-profile`: reference to applied baseline (e.g., FedRAMP Moderate)
     * `system-characteristics`: boundary, data flows, components
     * `system-implementation`: components, users, inventory
     * `control-implementation`: per-control implementation statements and evidence references
     * `back-matter`: evidence artifacts as resources
   * Validate against OSCAL SSP schema (accessed 2025-10-25T21:30:36-04:00, [source](https://github.com/usnistgov/OSCAL/blob/main/json/schema/oscal_ssp_schema.json))

6. **Remediation planning**
   * Generate prioritized remediation plan:
     ```
     Priority 1 (Critical - Required for ATO):
     - AC-2(1): Account Management | Automated Account Management
       Gap: No evidence of automated account provisioning/deprovisioning
       Recommendation: Implement SCIM with IdP; document in AC-2 policy
       Effort: 2-4 weeks | Owner: IAM team

     Priority 2 (High - Required for full compliance):
     - AU-6(1): Audit Review, Analysis, and Reporting | Automated Process Integration
       Gap: Logs collected but no automated analysis/alerting
       Recommendation: Deploy SIEM with correlation rules; reference in AU-6 procedure
       Effort: 4-6 weeks | Owner: SecOps team
     ```

7. **Output structured report**
   * Compliance report JSON (see Output Contract)
   * OSCAL SSP artifact (if applicable)
   * Remediation plan markdown
   * Dashboard metrics for tracking

**Token budget:** ~5500 tokens (detailed control iteration + OSCAL generation)

**Key decision points:**
* If coverage < 70%: recommend deferring formal assessment
* If critical gaps in AC, IA, SC families: flag as ATO blockers
* If evidence > 180 days old: require refresh

### Tier 3: Comprehensive Compliance Audit (≤12k tokens)

**Goal:** Deep-dive multi-framework analysis with cross-framework mapping, continuous monitoring design, and full OSCAL artifact suite generation

**Target scenarios:**
* Initial ATO package preparation requiring SSP, SAP, SAR, POA&M
* Multi-framework compliance (e.g., FedRAMP + HIPAA for healthcare SaaS)
* Continuous monitoring implementation
* Post-incident compliance impact assessment

**Steps:**

1. **Multi-framework control mapping**
   * Load controls for all applicable frameworks
   * Build mapping table using NIST Cybersecurity Framework (CSF) as pivot
     * Example: NIST CSF PR.AC-1 maps to:
       * NIST 800-53 Rev 5: AC-2, AC-3, AC-5, AC-6
       * FedRAMP Moderate: AC-2, AC-3 (subset)
       * HIPAA: 164.308(a)(3), 164.308(a)(4)
       * GDPR: Article 32(1)(b) - access control
   * Source: NIST CSF Framework Crosswalk (accessed 2025-10-25T21:30:36-04:00, [source](https://www.nist.gov/cyberframework/framework-crosswalks))
   * Identify overlapping controls to avoid duplicate effort

2. **Deep evidence validation**
   * For each control implementation:
     * Validate evidence completeness against control requirements
     * Check evidence chain: policy → procedure → configuration → test result
     * Verify evidence authenticity (digital signatures, audit trails)
     * Assess evidence quality using criteria:
       * Specificity: does evidence directly address control requirement?
       * Timeliness: is evidence current (< 90 days for operational evidence)?
       * Consistency: do multiple evidence sources corroborate?
       * Scope: does evidence cover entire system boundary?

3. **Control inheritance analysis**
   * For cloud-hosted systems, analyze inherited controls:
     * AWS: 160+ inherited controls for FedRAMP High GovCloud (accessed 2025-10-25T21:30:36-04:00, [source](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/))
     * Azure Government: similar coverage for FedRAMP High (accessed 2025-10-25T21:30:36-04:00)
     * Document customer responsibility matrix (shared vs. inherited)
   * Validate cloud provider compliance documentation is current

4. **Generate complete OSCAL artifact suite**

   **SSP (System Security Plan):**
   * Full implementation details per control
   * Responsible parties and roles
   * System diagrams (reference from `system_context`)
   * Authorization boundary definition

   **SAP (Security Assessment Plan):**
   * Assessment objectives per control
   * Assessment methods: examine, interview, test
   * Assessment team roles
   * Assessment schedule
   * NIST SP 800-53A assessment procedures (accessed 2025-10-25T21:30:36-04:00, [source](https://csrc.nist.gov/publications/detail/sp/800-53a/rev-5/final))

   **SAR (Security Assessment Report):**
   * Assessment findings per control
   * Risk ratings (low/moderate/high)
   * Identified deficiencies
   * Recommended remediation actions

   **POA&M (Plan of Action & Milestones):**
   * Open findings from assessment
   * Remediation plan with milestones
   * Risk acceptance decisions
   * Deviation requests (if applicable)
   * Per FedRAMP POA&M template requirements (accessed 2025-10-25T21:30:36-04:00, [source](https://www.fedramp.gov/assets/resources/templates/FedRAMP-POAM-Template.xlsm))

5. **Continuous monitoring design**
   * Identify controls requiring continuous monitoring (CM controls)
   * Recommend monitoring frequency per control family:
     * Real-time: AC (access), AU (audit), SI (incident)
     * Daily: CM (configuration), IA (identification)
     * Weekly: RA (risk assessment), CA (assessment)
     * Monthly: PL (planning), SA (acquisition)
   * Generate monitoring dashboard schema:
     ```json
     {
       "metrics": [
         {"control": "AC-2", "metric": "failed_login_attempts", "threshold": 5, "period": "15min"},
         {"control": "AU-6", "metric": "unreviewed_audit_records", "threshold": 1000, "period": "24h"},
         {"control": "CM-3", "metric": "unapproved_config_changes", "threshold": 0, "period": "1h"}
       ],
       "alerting": {
         "critical": ["AC-*", "IA-*", "SC-*"],
         "high": ["AU-*", "CM-*", "IR-*"]
       }
     }
     ```

6. **Risk-based prioritization**
   * Apply NIST RMF Risk Assessment Framework (accessed 2025-10-25T21:30:36-04:00, [source](https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final))
   * Calculate risk scores per gap:
     * Likelihood (Low=1, Moderate=2, High=3)
     * Impact (Low=10, Moderate=50, High=100) per FIPS 199
     * Risk = Likelihood × Impact
   * Prioritize remediation by risk score descending

7. **Compliance dashboard generation**
   * Output metrics suitable for executive dashboards:
     * Overall compliance score (%)
     * Controls by status (pie chart data)
     * Top 5 risk items
     * Remediation velocity (gaps closed per sprint/month)
     * Time-to-ATO estimate based on current velocity
     * Trend analysis (if historical data available)

8. **Cross-framework compliance report**
   * Unified view showing compliance across multiple frameworks
   * Identify efficiency opportunities (one control satisfying multiple requirements)
   * Highlight framework-specific gaps requiring additional evidence

**Token budget:** ~11500 tokens (multi-framework mapping + full OSCAL suite + monitoring design)

**Key decision points:**
* If POA&M items > 50: recommend phased remediation approach
* If high-risk gaps in authorization boundary: recommend boundary re-scoping
* If continuous monitoring not feasible: document risk acceptance rationale
* If multi-framework conflicts detected: escalate for policy decision

## Decision Rules

**Ambiguity resolution:**

* **Framework version conflicts:** Default to latest published version; warn if document specifies older version
* **Missing control parameters:** Use baseline defaults per NIST 800-53B (accessed 2025-10-25T21:30:36-04:00, [source](https://csrc.nist.gov/publications/detail/sp/800-53b/final)); flag for manual review
* **Evidence interpretation:** If evidence format unclear, attempt automated parse; fall back to manual review flag
* **Control status uncertainty:** Default to `partially-implemented` with justification; require manual adjudication

**Abort conditions:**

* `framework` not recognized → emit error and list valid frameworks
* `system_context` missing required fields → emit TODO list of missing fields
* Evidence path inaccessible → warn and proceed with gap analysis
* OSCAL schema validation fails → report errors and halt artifact generation
* Control baseline exceeds token budget → recommend splitting into multiple assessments

**Tier escalation triggers:**

* T1→T2: User requests OSCAL generation or detailed gap analysis
* T2→T3: Multiple frameworks specified, or continuous monitoring design requested, or full artifact suite needed

**Quality thresholds:**

* Evidence age warning: > 90 days
* Evidence age error: > 365 days
* Coverage warning: < 80%
* Coverage error: < 70%
* Critical gap threshold: any control in AC-1, AC-2, IA-2, IA-5, SC-7, SC-8 families

## Output Contract

**compliance_report (JSON):**

```json
{
  "metadata": {
    "timestamp": "2025-10-25T21:30:36-04:00",
    "framework": "fedramp-moderate",
    "system_id": "SYS-001",
    "system_name": "Example SaaS Platform",
    "assessment_tier": "T3"
  },
  "summary": {
    "total_controls": 325,
    "implemented": 310,
    "partially_implemented": 10,
    "planned": 3,
    "not_applicable": 2,
    "coverage_pct": 95.4,
    "status": "ready-with-findings",
    "estimated_ato_date": "2025-12-15"
  },
  "gaps": [
    {
      "control_id": "AC-2(1)",
      "title": "Account Management | Automated Account Management",
      "severity": "critical",
      "gap_description": "No evidence of automated account provisioning",
      "risk_score": 300,
      "remediation": {
        "recommendation": "Implement SCIM with IdP",
        "effort_weeks": 4,
        "owner": "IAM Team",
        "target_date": "2025-11-22"
      }
    }
  ],
  "metrics": {
    "controls_by_family": {"AC": 25, "AU": 18, "...": "..."},
    "evidence_count": 847,
    "evidence_types": {"policy": 45, "procedure": 68, "config": 312, "test": 422}
  }
}
```

**oscal_artifacts (object):**

```json
{
  "ssp": "<OSCAL 1.1.2 compliant SSP JSON>",
  "sap": "<OSCAL SAP JSON if T3>",
  "sar": "<OSCAL SAR JSON if T3>",
  "poam": "<OSCAL POA&M JSON if gaps exist>"
}
```

**remediation_plan (markdown):**

Prioritized list with:
* Priority level (1=Critical, 2=High, 3=Medium, 4=Low)
* Control ID and title
* Gap description
* Recommended action
* Effort estimate
* Responsible party
* Target completion date

**dashboard_data (JSON):**

Time-series compatible metrics for visualization:
* Compliance score over time
* Gap count by severity
* Remediation velocity
* Control family coverage heatmap

**Required fields (all tiers):**
* `metadata.timestamp` (NOW_ET)
* `summary.total_controls`
* `summary.coverage_pct`
* `summary.status`

**Optional fields (T2+):**
* `oscal_artifacts.ssp`
* `remediation_plan`

**Optional fields (T3 only):**
* `oscal_artifacts.sap`, `.sar`, `.poam`
* `dashboard_data`
* `multi_framework_mapping`

## Examples

**Example 1: T2 FedRAMP Moderate Assessment**

```yaml
# Input
framework: fedramp-moderate
control_baseline: moderate
evidence_path: /compliance/evidence/fedramp-mod
system_context:
  system_name: "Cloud SaaS Platform"
  system_id: "CSP-001"
  boundary_description: "AWS GovCloud VPC with web/app/db tiers"
  authorization_boundary: "All components in VPC vpc-abc123"
validation_mode: standard

# Processing (excerpt)
# Loaded 325 controls from FedRAMP Moderate baseline
# Scanned 847 evidence files
# Identified 10 gaps (3 critical, 5 high, 2 medium)
# Generated OSCAL SSP (245KB JSON)

# Output (summary)
coverage: 96.9%
status: ready-with-findings
critical_gaps: ["AC-2(1)", "AU-6(1)", "IR-4(1)"]
oscal_ssp_generated: true
remediation_priority: "Address 3 critical gaps in 4-6 weeks"
```

## Quality Gates

**Token budgets (enforced):**
* T1 ≤ 2000 tokens — quick coverage check, control list loading only
* T2 ≤ 6000 tokens — detailed assessment with OSCAL SSP generation
* T3 ≤ 12000 tokens — multi-framework analysis with full artifact suite

**Safety checks:**
* No credentials or API keys in evidence files (pattern scan)
* No PII in generated artifacts (GDPR/HIPAA compliance)
* All external links use HTTPS
* Evidence file sizes reasonable (< 50MB per file; warn if larger)

**Auditability:**
* All control assessments include justification and evidence references
* OSCAL artifacts include metadata/publication timestamp (NOW_ET)
* Remediation plans include responsible parties and target dates
* Audit trail in compliance_report.metadata

**Determinism:**
* Same inputs + evidence → same compliance_report (idempotent)
* Control status deterministic based on evidence availability and quality
* Gap prioritization algorithmic (risk score calculation)

**Validation requirements:**
* OSCAL artifacts validate against official schemas (1.1.2)
* Control IDs match official NIST SP 800-53 Rev 5 catalog
* FedRAMP templates match current published versions
* Framework crosswalks use authoritative NIST sources

## Resources

**NIST Publications:**
* NIST Cybersecurity Framework (CSF): https://www.nist.gov/cyberframework (accessed 2025-10-25T21:30:36-04:00)
* NIST SP 800-53 Rev 5 (Security and Privacy Controls): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (accessed 2025-10-25T21:30:36-04:00)
* NIST SP 800-53A Rev 5 (Assessment Procedures): https://csrc.nist.gov/publications/detail/sp/800-53a/rev-5/final (accessed 2025-10-25T21:30:36-04:00)
* NIST SP 800-53B (Control Baselines): https://csrc.nist.gov/publications/detail/sp/800-53b/final (accessed 2025-10-25T21:30:36-04:00)
* NIST SP 800-37 Rev 2 (Risk Management Framework): https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final (accessed 2025-10-25T21:30:36-04:00)

**OSCAL Resources:**
* OSCAL Project Homepage: https://pages.nist.gov/OSCAL/ (accessed 2025-10-25T21:30:36-04:00)
* OSCAL Schema Repository: https://github.com/usnistgov/OSCAL (accessed 2025-10-25T21:30:36-04:00)
* OSCAL Content Repository (controls, catalogs, profiles): https://github.com/usnistgov/oscal-content (accessed 2025-10-25T21:30:36-04:00)

**FedRAMP Resources:**
* FedRAMP Homepage: https://www.fedramp.gov/ (accessed 2025-10-25T21:30:36-04:00)
* FedRAMP Security Controls Baseline: https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.xlsx (accessed 2025-10-25T21:30:36-04:00)
* FedRAMP Templates: https://www.fedramp.gov/assets/resources/templates/ (accessed 2025-10-25T21:30:36-04:00)

**Regulatory Resources:**
* GDPR Official Text: https://gdpr.eu/ (accessed 2025-10-25T21:30:36-04:00)
* HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html (accessed 2025-10-25T21:30:36-04:00)
* FISMA Implementation: https://csrc.nist.gov/projects/risk-management/fisma-background (accessed 2025-10-25T21:30:36-04:00)

**Cloud Provider Compliance:**
* AWS GovCloud FedRAMP: https://aws.amazon.com/compliance/services-in-scope/FedRAMP/ (accessed 2025-10-25T21:30:36-04:00)
* Azure Government Compliance: https://docs.microsoft.com/azure/azure-government/compliance/azure-services-in-fedramp-auditscope (accessed 2025-10-25T21:30:36-04:00)

**Tools and Validation:**
* OSCAL CLI Tools: https://github.com/usnistgov/oscal-cli (accessed 2025-10-25T21:30:36-04:00)
* NIST CSF Framework Crosswalks: https://www.nist.gov/cyberframework/framework-crosswalks (accessed 2025-10-25T21:30:36-04:00)
