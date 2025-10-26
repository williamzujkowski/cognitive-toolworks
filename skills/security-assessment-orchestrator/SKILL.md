---
name: Security Assessment Orchestrator
slug: security-assessment-orchestrator
description: Comprehensive security assessment across application, cloud, container, IAM, network, OS, supply chain, and zero trust using NIST CSF 2.0.
capabilities:
  - Orchestrates 10 security-* skills for unified posture assessment
  - NIST CSF 2.0 alignment (Govern, Identify, Protect, Detect, Respond, Recover)
  - Aggregated risk scoring (CVSS 4.0 + business context)
  - Cross-domain finding correlation and attack path analysis
  - Security maturity assessment (Crawl, Walk, Run)
  - Prioritized remediation roadmap with effort/impact estimates
inputs:
  - Assessment scope (application, infrastructure, cloud, full-stack)
  - Target environment (dev, staging, production, all)
  - Compliance requirements (NIST CSF, CIS, OWASP, FedRAMP, none)
  - Business context (asset criticality, data sensitivity, internet-facing)
  - Depth level (quick-scan, standard, comprehensive)
outputs:
  - Unified security findings with CVSS scores and context
  - NIST CSF 2.0 function coverage report
  - Security maturity score (0-10 per CSF function)
  - Attack path analysis with exploitability assessment
  - Prioritized remediation roadmap with timelines
keywords:
  - security assessment
  - nist csf
  - security orchestration
  - risk scoring
  - cvss
  - security posture
  - vulnerability management
  - compliance
  - security maturity
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  - Read-only assessment, no production system modification
  - Handles sensitive findings data (encrypt/restrict access)
  - Audit logging of all delegated security skill invocations
links:
  - https://www.nist.gov/cyberframework
  - https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
  - https://www.first.org/cvss/
  - https://securecontrolsframework.com/blog/nist-csf-20-assessment-guide/
---

## Purpose & When-To-Use

**Primary trigger conditions:**

- Pre-production security review required across all layers (app + infra + cloud)
- Compliance audit preparation (NIST CSF 2.0, ISO 27001, SOC 2, FedRAMP)
- Post-incident comprehensive security assessment
- Quarterly security posture review (enterprise practice)
- M&A due diligence security evaluation
- Board/executive request for unified security metrics
- Third-party security questionnaire requiring holistic assessment

**When NOT to use this skill:**

- Single-domain security check (use specific security-* skill directly)
- Real-time vulnerability scanning (use SAST/DAST/SCA tools)
- Penetration testing (requires manual testing, not framework assessment)
- Code-level security review (use security-appsec-validator alone)

**Value proposition:** Provides unified security posture across 10 security domains, correlates findings to identify attack paths, and prioritizes remediation based on CVSS 4.0 + business context. Organizations using comprehensive security orchestration reduce MTTD (Mean Time To Detect) by 62% and MTTR (Mean Time To Respond) by 74% compared to siloed assessments (IBM Security 2025).

## Pre-Checks

**Required inputs validation:**

```python
NOW_ET = "2025-10-26T16:45:00-04:00"

assert assessment_scope in ["application", "infrastructure", "cloud", "full-stack"], "Valid scopes required"
assert target_environment in ["dev", "staging", "production", "all"], "Valid environment required"
assert compliance_requirements in ["nist-csf", "cis", "owasp", "fedramp", "none"]
assert depth_level in ["quick-scan", "standard", "comprehensive"], "Valid depth required"

# Business context validation
if business_context.get("internet_facing") and target_environment == "production":
    warn("Internet-facing production asset: elevating scan depth to comprehensive")

# Scope validation
required_skills = map_scope_to_skills(assessment_scope)
if len(required_skills) > 5 and depth_level == "comprehensive":
    estimate_duration = len(required_skills) * 15  # minutes per skill at T2
    warn(f"Comprehensive scan will invoke {len(required_skills)} skills, ~{estimate_duration} minutes")
```

**Authority checks:**

- Read access to target environments (no write/deploy permissions required)
- API/CLI credentials for cloud providers (AWS, Azure, GCP) if cloud scope
- Source code repository access if application scope
- Network scan permissions if infrastructure scope

**Source citations (accessed 2025-10-26T16:45:00-04:00):**

- NIST CSF 2.0 (CSWP 29): https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
- CVSS v4.0 Specification: https://www.first.org/cvss/v4.0/specification-document
- NIST CSF Assessment Guide: https://securecontrolsframework.com/blog/nist-csf-20-assessment-guide/
- IBM Security X-Force Threat Intelligence Index 2025: Organizations using unified security reduce MTTD by 62%, MTTR by 74%

## Procedure

### Tier 1 (≤2k tokens): Quick Security Scan

**Goal:** Identify critical security risks across all domains in <15 minutes.

**Steps:**

1. **Map scope to skills** (determine which security-* skills to invoke)
   - `application` → security-appsec-validator
   - `infrastructure` → security-network-validator, security-os-validator
   - `cloud` → security-cloud-analyzer, security-iam-reviewer
   - `full-stack` → all 10 security-* skills

2. **Invoke skills in parallel** (T1 tier for each)
   - Set `check_level: critical-only` for all delegated skills
   - Collect findings with CVSS ≥7.0 (High/Critical severity only)
   - Timeout: 90 seconds per skill invocation

3. **Aggregate critical findings**
   - Deduplicate cross-skill findings (e.g., same IAM issue found by cloud + zerotrust skills)
   - Sort by CVSS score descending
   - Group by NIST CSF function (Identify, Protect, Detect, Respond, Recover, Govern)

4. **Quick risk scoring**
   - Calculate **Critical Risk Index (CRI)**: `(count_critical × 10) + (count_high × 5)`
   - If CRI >50 → **immediate action required**
   - If CRI 20-50 → **standard remediation timeline (30 days)**
   - If CRI <20 → **low priority (90 days)**

5. **Output quick wins** (top 3 highest-impact remediations)
   - Example: "Public S3 bucket with PII exposed (CVSS 9.8) → add bucket policy denying public access"
   - Example: "Overpermissive IAM role with admin access (CVSS 8.1) → apply principle of least privilege"
   - Example: "Unpatched OS vulnerability (CVE-2024-1234, CVSS 7.5) → apply security patch"

**Token budget checkpoint:** ~1.8k tokens for skill orchestration, aggregation, risk scoring, output formatting.

### Tier 2 (≤6k tokens): Comprehensive Security Assessment

**Goal:** Generate detailed security posture report with NIST CSF 2.0 alignment and prioritized remediation roadmap.

**Extends T1 with:**

6. **Invoke all in-scope skills at T2 depth**
   - Set `check_level: standard` for delegated skills
   - Collect all findings (CVSS ≥4.0, Medium/High/Critical)
   - Enable compliance checks where applicable (CIS Benchmarks, OWASP Top 10, etc.)

   **Skill invocation matrix:**

   | Domain | Skill | NIST CSF Functions | Compliance |
   |--------|-------|-------------------|------------|
   | Application | security-appsec-validator | Protect (PR.AC, PR.DS) | OWASP Top 10, API Top 10 |
   | Cloud | security-cloud-analyzer | Identify (ID.AM), Protect (PR.AC) | CIS Benchmarks, Well-Architected |
   | Container | security-container-validator | Protect (PR.IP) | CIS Docker/K8s |
   | Cryptography | security-crypto-validator | Protect (PR.DS) | FIPS 140-2 |
   | IAM | security-iam-reviewer | Protect (PR.AC) | CIS IAM |
   | Network | security-network-validator | Protect (PR.PT), Detect (DE.CM) | CIS Network |
   | OS | security-os-validator | Protect (PR.IP) | CIS OS Benchmarks |
   | Supply Chain | security-supplychain-validator | Identify (ID.SC), Govern (GV.SC) | NIST SSDF, SLSA |
   | Zero Trust | security-zerotrust-architect | Govern (GV.PO), Protect (PR.AC) | NIST SP 800-207 |
   | Zero Trust Assess | security-zerotrust-assessor | Identify (ID.RA) | CISA ZT Maturity |

7. **Cross-domain finding correlation**
   - Identify **attack paths**: chain findings across domains
     - Example: "Overpermissive IAM role (security-iam-reviewer) + public S3 bucket (security-cloud-analyzer) + weak encryption (security-crypto-validator) = complete data breach path"
   - Calculate **attack path exploitability**: multiply individual CVSS scores by 0.8 (cumulative risk)
   - Flag correlated findings with `attack_path_id` for tracking

8. **NIST CSF 2.0 coverage analysis**
   - Map findings to CSF Categories and Subcategories
   - Calculate **function coverage** (% of subcategories assessed vs total)
   - Generate coverage report:
     ```
     Govern (GV): 85% coverage (17/20 subcategories)
     Identify (ID): 90% coverage (27/30 subcategories)
     Protect (PR): 78% coverage (39/50 subcategories)
     Detect (DE): 65% coverage (26/40 subcategories)
     Respond (RS): 45% coverage (18/40 subcategories) ← low coverage, gap
     Recover (RC): 30% coverage (9/30 subcategories) ← low coverage, gap
     ```

9. **Security maturity assessment**
   - Evaluate maturity per NIST CSF function using SCF scoring (Conforms, Significant Deficiency, Material Weakness)
   - Assign maturity level (0-10 scale):
     - **Crawl (0-3)**: Ad-hoc, reactive, significant gaps
     - **Walk (4-6)**: Defined processes, some automation, moderate gaps
     - **Run (7-10)**: Optimized, automated, continuous improvement, minimal gaps
   - Calculate **overall security maturity score**: weighted average across 6 functions
     - Govern: 20% weight (highest priority in CSF 2.0)
     - Identify: 15%
     - Protect: 25% (largest function)
     - Detect: 15%
     - Respond: 15%
     - Recover: 10%

10. **Contextual risk scoring** (CVSS 4.0 + business factors)
    - Base CVSS score from vulnerability databases
    - **Business criticality multiplier** (1.0-2.0):
      - Mission-critical production asset: 2.0x
      - Production asset: 1.5x
      - Non-production: 1.0x
    - **Exploit intelligence modifier** (+0.5 to +2.0):
      - Active exploits in the wild: +2.0
      - PoC exploit available: +1.0
      - Theoretical exploit: +0.5
    - **Data sensitivity modifier** (+0.5 to +1.5):
      - PII/PHI/financial data: +1.5
      - Confidential business data: +1.0
      - Public data: +0.5
    - **Internet exposure modifier** (+1.0 if internet-facing)

    **Final risk score formula:**
    ```
    Risk Score = (CVSS × Business Multiplier) + Exploit Modifier + Data Modifier + Exposure Modifier
    ```

11. **Prioritized remediation roadmap**
    - Rank findings by **ROI** (risk reduction / effort):
      - Effort scale: Low (1 hour), Medium (1 day), High (1 week), Very High (1 month+)
      - ROI = `Final Risk Score / Effort Hours`
    - Group remediation into phases:
      - **Phase 1 (0-30 days)**: Critical (CVSS ≥9.0) + High-ROI (ROI >5)
      - **Phase 2 (31-90 days)**: High (CVSS 7.0-8.9) + Medium-ROI (ROI 2-5)
      - **Phase 3 (91-180 days)**: Medium (CVSS 4.0-6.9) + Low-ROI (ROI <2)
      - **Accepted Risk**: Low (CVSS <4.0) or business justification for deferral
    - Assign ownership (AppSec, CloudOps, NetOps, DevOps, Platform) per finding domain

12. **Generate comprehensive report**
    - **Executive summary**: Overall maturity score, CRI, top 5 risks, estimated remediation timeline
    - **Detailed findings**: Per-domain breakdown with CVSS scores, attack paths, remediation steps
    - **NIST CSF compliance**: Function coverage, maturity scores, gap analysis
    - **Remediation roadmap**: Phased timeline, ownership assignments, effort estimates

**Authority sources (accessed 2025-10-26T16:45:00-04:00):**

- NIST CSF 2.0 Functions and Categories: https://www.nist.gov/cyberframework/framework
- CVSS v4.0 Base Metrics: https://www.first.org/cvss/v4.0/specification-document
- Secure Controls Framework (SCF) Maturity Model: https://securecontrolsframework.com/
- IBM X-Force 2025: 280,000+ CVEs in NVD, 32% YoY increase in vulnerability submissions

**Output:** JSON report with sections: executive_summary, findings_by_domain, nist_csf_coverage, security_maturity_assessment, attack_paths, prioritized_roadmap.

**Token budget checkpoint:** ~5.5k tokens (includes T1 + comprehensive skill orchestration + detailed analysis).

### T3: Enterprise Security Governance (≤12k tokens)

**Goal:** Deep governance alignment, continuous monitoring strategy, and board-level security metrics for organizations with >$100M revenue or regulatory requirements.

**Extends T2 with:**

13. **Continuous monitoring strategy**
    - Map findings to automated detection rules (SIEM, CSPM, CNAPP)
    - Recommend security tool stack (SAST, DAST, SCA, CSPM, CNAPP, EDR, SIEM)
    - Define SLA targets per severity: Critical (4h), High (24h), Medium (7d), Low (30d)

14. **Regulatory compliance mapping**
    - Cross-reference findings with specific compliance controls:
      - SOC 2 Trust Service Criteria (CC, A, PI, C, P)
      - ISO 27001:2022 Annex A controls
      - FedRAMP High baseline (NIST SP 800-53 Rev 5)
      - PCI-DSS 4.0 requirements
    - Generate compliance gap report with remediation-to-compliance mapping

15. **Board-level security metrics**
    - **Cyber Risk Quantification (CRQ):** Dollar value of risk exposure (ALE = ARO × SLE)
    - **Security ROI:** Cost of remediation vs cost of breach (based on industry breach costs)
    - **Trend analysis:** Compare current vs previous assessment (quarterly tracking)
    - **Benchmark comparison:** Compare maturity vs industry peers (anonymized data)

16. **Third-party risk assessment**
    - Extend assessment to supply chain dependencies (npm, PyPI, Maven, container images)
    - Evaluate vendor security questionnaires against NIST CSF alignment
    - Recommend vendor security SLA requirements

17. **Incident response readiness**
    - Evaluate Respond (RS) and Recover (RC) function maturity
    - Validate incident response plan (IRP) against NIST CSF subcategories
    - Recommend tabletop exercise scenarios based on identified attack paths

**Authority sources (accessed 2025-10-26T16:45:00-04:00):**

- NIST SP 800-61 Rev 3 (Incident Response): https://csrc.nist.gov/pubs/sp/800/61/r3/final
- Cyber Risk Quantification (Factor Analysis): https://www.fairinstitute.org/
- IBM Cost of a Data Breach 2025: Average breach cost $4.88M (+10% from 2024)

**Output:** Full enterprise security governance package including CRQ analysis, compliance mapping, board metrics, continuous monitoring blueprint, and incident response readiness assessment.

**Token budget checkpoint:** ~11k tokens (includes T1 + T2 + enterprise-grade governance analysis).

## Decision Rules

**When to abort:**

- No access to target environment → insufficient permissions; emit access requirement checklist
- <3 security skills applicable to scope → use specific security-* skill directly, not orchestrator
- Contradictory compliance requirements (e.g., "FedRAMP High + no budget for controls") → document conflicts, request prioritization

**Ambiguity thresholds:**

- **Maturity scoring:** If <50% CSF subcategory coverage → report "Insufficient Coverage" instead of maturity score
- **Attack path correlation:** Only correlate findings if exploitability chain probability >30% (avoid false positives)
- **Risk prioritization:** If business context missing → use CVSS base score only (no multipliers) and flag as "incomplete risk assessment"

**Prioritization logic:**

1. **Severity-first:** Critical (CVSS ≥9.0) always ranked highest, regardless of ROI
2. **ROI-based:** Within same severity tier, rank by ROI (risk reduction / effort)
3. **Compliance-driven:** If compliance requirement specified, elevate findings mapped to that framework
4. **Internet-facing:** Public-facing production assets get +2 priority boost

**NIST CSF principle application (accessed 2025-10-26T16:45:00-04:00):**

Per NIST CSF 2.0 (https://www.nist.gov/cyberframework):

- **"Govern first":** Prioritize Govern (GV) function findings, as they cascade to all other functions
- **"Continuous improvement":** Track maturity scores over time (quarterly assessments recommended)
- **"Risk-informed":** All recommendations incorporate risk tolerance and business impact

## Output Contract

**Schema (JSON):**

```json
{
  "assessment_metadata": {
    "timestamp": "2025-10-26T16:45:00-04:00",
    "scope": "full-stack",
    "environment": "production",
    "depth": "comprehensive",
    "skills_invoked": 10
  },
  "executive_summary": {
    "overall_maturity_score": 6.2,
    "critical_risk_index": 47,
    "total_findings": 142,
    "breakdown": {
      "critical": 3,
      "high": 18,
      "medium": 67,
      "low": 54
    },
    "top_5_risks": [
      {
        "finding_id": "IAM-001",
        "title": "Overpermissive admin role attached to 50+ users",
        "cvss": 8.8,
        "risk_score": 15.8,
        "domain": "iam"
      }
    ],
    "estimated_remediation_timeline": "90 days for all Critical+High findings"
  },
  "findings_by_domain": [
    {
      "domain": "application",
      "skill": "security-appsec-validator",
      "findings_count": 28,
      "findings": [
        {
          "id": "APP-001",
          "title": "SQL injection vulnerability in /api/users endpoint",
          "severity": "critical",
          "cvss": 9.8,
          "risk_score": 19.3,
          "owasp_category": "A03:2021 - Injection",
          "remediation": "Use parameterized queries, ORM with escaping",
          "effort": "medium",
          "owner": "appsec-team"
        }
      ]
    }
  ],
  "nist_csf_coverage": {
    "govern": {"coverage_pct": 85, "maturity_score": 7.2},
    "identify": {"coverage_pct": 90, "maturity_score": 6.8},
    "protect": {"coverage_pct": 78, "maturity_score": 6.1},
    "detect": {"coverage_pct": 65, "maturity_score": 5.5},
    "respond": {"coverage_pct": 45, "maturity_score": 4.2},
    "recover": {"coverage_pct": 30, "maturity_score": 3.8}
  },
  "attack_paths": [
    {
      "path_id": "AP-001",
      "description": "Public S3 bucket → overpermissive IAM → PII data exfiltration",
      "exploitability": "high",
      "combined_risk_score": 17.6,
      "findings": ["CLOUD-012", "IAM-001", "CRYPTO-005"]
    }
  ],
  "prioritized_roadmap": [
    {
      "phase": "Phase 1 (0-30 days)",
      "findings_count": 21,
      "estimated_effort": "120 hours",
      "risk_reduction": 68.5,
      "items": [
        {
          "finding_id": "APP-001",
          "priority": 1,
          "action": "Remediate SQL injection vulnerabilities",
          "owner": "appsec-team",
          "effort": "medium",
          "roi": 12.3
        }
      ]
    }
  ]
}
```

**Required fields:** assessment_metadata, executive_summary (with maturity_score, CRI, total_findings), nist_csf_coverage, prioritized_roadmap.

**Optional fields:** attack_paths (only if correlations found), findings_by_domain (can be filtered by severity).

## Examples

```yaml
# Example: Full-stack security assessment for production SaaS application
input:
  assessment_scope: full-stack
  target_environment: production
  compliance_requirements: nist-csf
  business_context:
    asset_criticality: mission-critical
    data_sensitivity: pii-phi
    internet_facing: true
  depth_level: comprehensive

output:
  overall_maturity: 6.2 (Walk tier)
  critical_risk_index: 47 (immediate action)
  findings: 142 total (3 critical, 18 high, 67 medium, 54 low)
  top_risks:
    1. SQL injection (CVSS 9.8, risk_score 19.3)
    2. Overpermissive IAM (CVSS 8.8, risk_score 15.8)
    3. Public S3 bucket with PII (CVSS 8.6, risk_score 15.2)
  attack_paths:
    - Public S3 → IAM escalation → PII exfiltration (risk 17.6)
  roadmap:
    Phase 1 (0-30d): 21 items, 120h effort, 68.5 risk reduction
    Phase 2 (31-90d): 45 items, 280h effort, 24.3 risk reduction
    Phase 3 (91-180d): 76 items, 450h effort, 7.2 risk reduction
```

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - quick security scan with critical findings only (CVSS ≥7.0)
- **T2**: ≤6,000 tokens - comprehensive assessment with NIST CSF alignment, maturity scoring, attack path analysis, and prioritized roadmap
- **T3**: ≤12,000 tokens - enterprise governance with CRQ, compliance mapping, board metrics, continuous monitoring, and incident response readiness

**Accuracy requirements:**

- CVSS scores must match official NVD/vendor advisories (no estimation)
- Maturity scores validated against NIST CSF 2.0 subcategory criteria
- Attack path correlations verified for logical exploitability chain

**Safety constraints:**

- **Read-only assessment:** No modification of production systems, configurations, or data
- **Secure finding storage:** Encrypt findings at rest, restrict access to security team + executives
- **Audit trail:** Log all skill invocations with timestamps, scopes, and results

**Auditability:**

- Cite specific NIST CSF subcategories for each finding
- Document maturity scoring methodology (SCF criteria used)
- Include timestamps and data sources for all CVSS scores

**Determinism:**

- Same inputs + same environment state → same findings and scores
- Configurable thresholds (CRI limits, maturity boundaries, ROI minimums)

## Resources

**Official NIST CSF 2.0 documentation:**

- NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
- CSWP 29 (CSF 2.0 Specification): https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
- CSF 2.0 Assessment Resources: https://www.nist.gov/cyberframework/assessment-auditing-resources

**Risk scoring and vulnerability management:**

- CVSS v4.0 Specification: https://www.first.org/cvss/v4.0/specification-document
- CVSS v4.0 Calculator: https://www.first.org/cvss/calculator/4.0
- NVD (National Vulnerability Database): https://nvd.nist.gov/

**Security frameworks and standards:**

- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- OWASP Top 10 2021: https://owasp.org/www-project-top-ten/
- OWASP API Security Top 10: https://owasp.org/API-Security/
- NIST SP 800-207 (Zero Trust Architecture): https://csrc.nist.gov/pubs/sp/800/207/final

**Compliance and governance:**

- Secure Controls Framework (SCF): https://securecontrolsframework.com/
- FedRAMP Baselines: https://www.fedramp.gov/baselines/
- SOC 2 Trust Service Criteria: https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2

**Industry research:**

- IBM Cost of a Data Breach Report 2025: https://www.ibm.com/security/data-breach
- Verizon Data Breach Investigations Report 2025: https://www.verizon.com/business/resources/reports/dbir/

**Related skills:**

This meta-skill orchestrates the following specialist skills:

- `security-appsec-validator`: Application security (OWASP Top 10)
- `security-cloud-analyzer`: Cloud security posture (AWS, Azure, GCP)
- `security-container-validator`: Container and Kubernetes security
- `security-crypto-validator`: Cryptography and encryption validation
- `security-iam-reviewer`: Identity and access management review
- `security-network-validator`: Network security and segmentation
- `security-os-validator`: Operating system hardening
- `security-supplychain-validator`: Software supply chain security
- `security-zerotrust-architect`: Zero trust architecture design
- `security-zerotrust-assessor`: Zero trust maturity assessment

**Complementary skills:**

- `compliance-oscal-validator`: OSCAL-formatted compliance validation
- `compliance-fedramp-validator`: FedRAMP-specific compliance
- `compliance-automation-engine`: Automated compliance monitoring
