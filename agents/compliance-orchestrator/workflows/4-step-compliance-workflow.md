# 4-Step Compliance Workflow — Detailed Procedures

**Agent**: compliance-orchestrator
**Version**: 1.0.0
**Last Updated**: 2025-10-26T01:33:55-04:00

---

## Overview

The compliance orchestrator executes a standardized 4-step workflow for all compliance assessments, regardless of framework or tier. This document provides detailed step-by-step procedures for each workflow phase.

## Workflow Steps

### Step 1: Discovery & Requirements

**Objective**: Validate inputs, load control catalogs, scan evidence, determine assessment scope

**Pre-conditions**:
- User has provided framework identifier
- Evidence path exists (or assessment will proceed as gap-only)
- System context available (minimum: system_name, system_id, boundary)

**Procedure**:

1. **Input Validation**
   - Verify framework identifier against valid list: nist-csf, nist-800-53, fedramp, fisma, gdpr, hipaa, pci-dss
   - Check control_baseline required for NIST/FedRAMP: low, moderate, high
   - Validate evidence_path accessibility (warn if inaccessible, continue)
   - Parse system_context JSON for required fields
   - Default validation_mode to "standard" (T2) if not specified

2. **Control Catalog Loading**
   - For FedRAMP:
     - Low: 125 controls
     - Moderate: 325 controls
     - High: 421 controls
   - For NIST 800-53 Rev 5: Load all 20 families, apply baseline overlay
   - For GDPR: Load Articles 5, 25, 32 requirements
   - For HIPAA: Load Security Rule (45 CFR 164.308-316)
   - Source: NIST SP 800-53 Rev 5 catalog (https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

3. **Evidence Discovery**
   - Scan evidence_path for files matching naming conventions
   - Look for evidence manifest (evidence_manifest.json or evidence_manifest.yaml)
   - Count evidence files by type: policy, procedure, config, log, test, screenshot
   - Map files to controls using:
     - Filename patterns (e.g., AC-2_implementation.pdf → AC-2 control)
     - Manifest entries (explicit control-to-evidence mapping)
   - Flag controls with zero evidence as critical gaps

4. **Cloud Inheritance Analysis** (if applicable)
   - Detect cloud provider from system_context (AWS, Azure, GCP)
   - Load inherited controls:
     - AWS GovCloud FedRAMP High: 160+ inherited controls
     - Azure Government: similar coverage
   - Document customer responsibility matrix
   - Verify provider compliance documentation is current (<12 months)

5. **Tier Determination**
   - validation_mode = "quick" → T1 (quick report, no OSCAL)
   - validation_mode = "standard" → T2 (OSCAL SSP generation)
   - validation_mode = "comprehensive" → T3 (full artifact suite)

**Outputs**:
- Validated input parameters
- Control catalog loaded (count: total controls)
- Evidence file count and mapping
- Assessment tier selected
- Inherited controls documented (if cloud-hosted)

**Error Handling**:
- Framework unrecognized → emit valid framework list and stop
- system_context missing required fields → emit TODO list and stop
- Evidence path inaccessible → warn, proceed with gap-only analysis
- Control catalog unavailable → attempt download from NIST, fallback to embedded baseline

---

### Step 2: Assessment & Analysis

**Objective**: Map evidence to controls, validate completeness, analyze gaps, calculate coverage metrics

**Pre-conditions**:
- Control catalog loaded from Step 1
- Evidence file list available (may be empty)
- Control-to-evidence mapping established

**Procedure**:

1. **Evidence-to-Control Mapping**
   - For each control in catalog:
     - Check if evidence exists via filename pattern or manifest
     - Validate evidence type matches control requirements:
       - Policy controls (PL, PS families) → require policy documents
       - Technical controls (AC, IA, SC families) → require config + test results
       - Operational controls (AU, CM, IR families) → require logs + procedures
     - Assign evidence quality score:
       - Specificity: Does evidence directly address control requirement? (0-3 points)
       - Timeliness: Is evidence current? (0-3 points)
       - Completeness: Does evidence cover entire scope? (0-3 points)
       - Total: 0-9 quality score per control

2. **Evidence Freshness Validation**
   - For each evidence file:
     - Extract modification timestamp
     - Calculate age (NOW_ET - file_mtime)
     - Flag if >90 days (warning - refresh recommended)
     - Flag if >365 days (error - refresh required)
     - Categorize evidence by freshness: current (<90d), aging (90-365d), stale (>365d)

3. **Control Status Determination**
   - For each control:
     - If evidence quality ≥7 and freshness current → "implemented"
     - If evidence quality 4-6 or freshness aging → "partially-implemented"
     - If evidence exists but quality <4 or freshness stale → "planned"
     - If no evidence → "not-started"
     - If control not applicable (e.g., physical controls in cloud) → "not-applicable"

4. **Coverage Calculation**
   - total_controls = count of all controls in baseline
   - implemented = count of "implemented" controls
   - partially_implemented = count of "partially-implemented" controls
   - planned = count of "planned" controls
   - not_started = count of "not-started" controls
   - not_applicable = count of "not-applicable" controls
   - coverage_pct = ((implemented + partially_implemented) / (total_controls - not_applicable)) * 100

5. **Gap Analysis**
   - Identify controls lacking sufficient evidence
   - Categorize gaps by severity:
     - **Critical**: High-impact controls (AC-1, AC-2, IA-2, IA-5, SC-7, SC-8) with zero evidence
     - **High**: Moderate-impact controls missing required evidence types
     - **Medium**: Minor evidence gaps or outdated artifacts
     - **Low**: Documentation formatting issues
   - Apply risk scoring:
     - Likelihood (Low=1, Moderate=2, High=3)
     - Impact (Low=10, Moderate=50, High=100) per FIPS 199
     - Risk = Likelihood × Impact

6. **Cross-Framework Mapping** (if multi-framework)
   - Use NIST CSF as pivot for control alignment
   - Example: NIST CSF PR.AC-1 maps to:
     - NIST 800-53 Rev 5: AC-2, AC-3, AC-5, AC-6
     - FedRAMP Moderate: AC-2, AC-3 (subset)
     - HIPAA: 164.308(a)(3), 164.308(a)(4)
     - GDPR: Article 32(1)(b) - access control
   - Identify overlapping controls to avoid duplicate effort

**Outputs**:
- Control status map (implemented, partially-implemented, planned, not-started, not-applicable)
- Coverage metrics (total, implemented count, coverage percentage)
- Gap list with severity ratings (critical, high, medium, low)
- Risk scores per gap
- Cross-framework control mapping (if multi-framework assessment)

**Quality Checks**:
- Coverage warning if <80%
- Coverage error if <70%
- Critical gap alert if AC/IA/SC families missing evidence
- Evidence freshness alerts per file

---

### Step 3: Synthesis & Generation

**Objective**: Generate compliance reports, OSCAL artifacts, remediation plans, monitoring dashboards

**Pre-conditions**:
- Control status map from Step 2
- Gap analysis complete
- Assessment tier determined (T1/T2/T3)

**Procedure**:

1. **Compliance Report Generation** (all tiers)
   - Construct JSON structure:
     ```json
     {
       "metadata": {
         "timestamp": "NOW_ET",
         "framework": "framework_id",
         "system_id": "system_id",
         "system_name": "system_name",
         "assessment_tier": "T1|T2|T3"
       },
       "summary": {
         "total_controls": count,
         "implemented": count,
         "partially_implemented": count,
         "planned": count,
         "not_started": count,
         "not_applicable": count,
         "coverage_pct": percentage,
         "status": "ready|ready-with-findings|gaps-identified|not-ready"
       },
       "gaps": [/* array of gap objects with severity, remediation */],
       "metrics": {/* control family breakdown, evidence counts */}
     }
     ```

2. **OSCAL SSP Generation** (T2+)
   - Construct OSCAL 1.1.2 compliant System Security Plan JSON:
     - `metadata`: system info, responsible parties, publication timestamp (NOW_ET)
     - `import-profile`: reference to applied baseline (e.g., FedRAMP Moderate)
     - `system-characteristics`: boundary, data flows, components, status
     - `system-implementation`: components, users, inventory, interconnections
     - `control-implementation`: per-control implementation statements and evidence references
     - `back-matter`: evidence artifacts as resources with UUIDs
   - Validate against OSCAL SSP schema: https://github.com/usnistgov/OSCAL/blob/main/json/schema/oscal_ssp_schema.json

3. **OSCAL Artifact Suite** (T3 only)
   - **SAP (Security Assessment Plan)**:
     - Assessment objectives per control
     - Assessment methods: examine, interview, test (per NIST 800-53A)
     - Assessment team roles and responsibilities
     - Assessment schedule with milestones
   - **SAR (Security Assessment Report)**:
     - Assessment findings per control
     - Risk ratings (low/moderate/high)
     - Identified deficiencies with evidence
     - Recommended remediation actions
   - **POA&M (Plan of Action & Milestones)**:
     - Open findings from assessment
     - Remediation plan with specific milestones
     - Risk acceptance decisions (if applicable)
     - Deviation requests per FedRAMP template

4. **Remediation Plan** (T2+)
   - Generate prioritized markdown document:
     ```markdown
     # Remediation Plan — System Name

     ## Priority 1 (Critical - Required for ATO)
     ### AC-2(1): Account Management | Automated Account Management
     - **Gap**: No evidence of automated account provisioning/deprovisioning
     - **Risk Score**: 300 (High likelihood × High impact)
     - **Recommendation**: Implement SCIM with IdP; document in AC-2 policy
     - **Effort**: 2-4 weeks
     - **Owner**: IAM Team
     - **Target Date**: [calculated from NOW_ET + effort]

     ## Priority 2 (High - Required for full compliance)
     ### AU-6(1): Audit Review, Analysis, and Reporting | Automated Process Integration
     ...
     ```

5. **Dashboard Schema** (T3 only)
   - Design continuous monitoring dashboard:
     ```json
     {
       "metrics": [
         {"control": "AC-2", "metric": "failed_login_attempts", "threshold": 5, "period": "15min"},
         {"control": "AU-6", "metric": "unreviewed_audit_records", "threshold": 1000, "period": "24h"},
         {"control": "CM-3", "metric": "unapproved_config_changes", "threshold": 0, "period": "1h"}
       ],
       "alerting": {
         "critical": ["AC-*", "IA-*", "SC-*"],
         "high": ["AU-*", "CM-*", "IR-*"],
         "medium": ["CA-*", "RA-*", "SA-*"]
       },
       "frequency": {
         "realtime": ["AC", "AU", "SI"],
         "daily": ["CM", "IA"],
         "weekly": ["RA", "CA"],
         "monthly": ["PL", "SA"]
       }
     }
     ```

**Outputs**:
- compliance_report.json (all tiers)
- oscal_ssp.json (T2+)
- oscal_sap.json (T3)
- oscal_sar.json (T3)
- oscal_poam.json (T3, if gaps exist)
- remediation_plan.md (T2+)
- dashboard_schema.json (T3)

**Quality Checks**:
- All JSON validates against schemas
- All timestamps use NOW_ET format
- All UUIDs are valid UUID v4
- No secrets or PII embedded
- File sizes reasonable (<50MB per artifact)

---

### Step 4: Validation & Finalization

**Objective**: Validate OSCAL schemas, verify cross-references, run safety scans, generate audit trail

**Pre-conditions**:
- Artifacts generated in Step 3
- OSCAL CLI tools available (or delegate to oscal-ssp-validate skill)

**Procedure**:

1. **OSCAL Schema Validation**
   - For each OSCAL artifact (SSP, SAP, SAR, POA&M):
     - Run schema validation against OSCAL 1.1.2+ schemas
     - Check required fields present (metadata, UUID fields)
     - Validate UUID format (v4)
     - Verify timestamp format (ISO-8601)
   - Delegation option: Use Task to invoke `oscal-ssp-validate` skill
     ```
     Task: "Use oscal-ssp-validate skill to validate SSP artifact"
     Input: {ssp_path: "/output/oscal_ssp.json", profile: "fedramp-moderate", strict: true}
     ```

2. **Cross-Reference Integrity**
   - Verify all component UUIDs referenced in control-implementation exist in system-implementation
   - Check all responsible-role UUIDs referenced exist in metadata/roles
   - Validate all resource UUIDs in back-matter are referenced in control-implementation
   - Ensure no orphaned UUIDs or dangling references

3. **Profile Alignment** (if profile specified)
   - Verify import-profile references valid OSCAL profile (e.g., FedRAMP Moderate baseline)
   - Check all controls in control-implementation match controls in imported profile
   - Validate parameter settings align with profile requirements
   - Flag any controls in SSP not in profile (may indicate error)

4. **Safety Scans**
   - Pattern scan for secrets:
     - API keys: `(api[_-]?key|apikey)[\s:=]+['\"]?[a-zA-Z0-9]{20,}`
     - Tokens: `(token|bearer)[\s:=]+['\"]?[a-zA-Z0-9._-]{20,}`
     - Passwords: `(password|passwd|pwd)[\s:=]+['\"]?[^\s'\"]+`
   - Pattern scan for PII:
     - SSN: `\d{3}-\d{2}-\d{4}`
     - Email (if not official contacts): `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Flag any matches for manual review

5. **Audit Trail Generation**
   - Append to compliance_report.json:
     ```json
     "audit_trail": {
       "discovery_timestamp": "2025-10-26T01:33:55-04:00",
       "assessment_timestamp": "2025-10-26T01:35:12-04:00",
       "synthesis_timestamp": "2025-10-26T01:37:48-04:00",
       "validation_timestamp": "2025-10-26T01:39:22-04:00",
       "total_duration_seconds": 327,
       "validation_results": {
         "oscal_ssp_valid": true,
         "oscal_sap_valid": true,
         "oscal_sar_valid": true,
         "oscal_poam_valid": true,
         "cross_references_valid": true,
         "profile_aligned": true,
         "secrets_detected": false,
         "pii_detected": false
       }
     }
     ```

6. **Final Quality Assessment**
   - Calculate ATO readiness score:
     - Coverage ≥95% + no critical gaps = "ready"
     - Coverage 80-94% + minor gaps = "ready-with-findings"
     - Coverage 70-79% + gaps = "gaps-identified"
     - Coverage <70% = "not-ready"
   - Estimate time-to-ATO:
     - If ready: 2-4 weeks (submission + review)
     - If ready-with-findings: 4-8 weeks (remediation + submission)
     - If gaps-identified: 8-16 weeks (significant remediation)
     - If not-ready: 16+ weeks (major remediation)

**Outputs**:
- validation_report.json (schema check results, cross-ref status, safety scan results)
- Updated compliance_report.json with audit_trail
- Final ATO readiness assessment
- Time-to-ATO estimate

**Error Handling**:
- If OSCAL schema validation fails → report errors, halt artifact delivery, suggest fixes
- If cross-references invalid → flag specific UUIDs, suggest corrections
- If secrets detected → halt delivery, warn user, recommend sanitization
- If PII detected → warn user, recommend review/redaction

---

## Decision Points

### Tier Escalation
- User requests OSCAL generation → escalate to T2 minimum
- User requests full artifact suite → escalate to T3
- Multi-framework assessment → escalate to T3
- Continuous monitoring design → escalate to T3

### Abort Conditions
- Framework unrecognized → emit valid framework list and stop
- System context missing required fields → emit TODO list and stop
- OSCAL schema validation fails → report errors and halt artifact generation
- Token budget exceeded → recommend splitting by control family

### Quality Thresholds
- Coverage warning: <80% (recommend improvement)
- Coverage error: <70% (defer formal assessment)
- Evidence age warning: >90 days (refresh recommended)
- Evidence age error: >365 days (refresh required)
- Critical gap threshold: AC-1, AC-2, IA-2, IA-5, SC-7, SC-8 with zero evidence = ATO blocker

---

## References

- NIST SP 800-37 Rev 2 (Risk Management Framework): https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final
- NIST SP 800-53 Rev 5 (Security Controls): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- NIST SP 800-53A Rev 5 (Assessment Procedures): https://csrc.nist.gov/publications/detail/sp/800-53a/rev-5/final
- OSCAL Documentation: https://pages.nist.gov/OSCAL/
- FedRAMP Authorization Process: https://www.fedramp.gov/assets/resources/documents/Agency_Authorization_Playbook.pdf
