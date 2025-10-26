---
name: "Comprehensive Security Assessment Framework"
slug: "security-assessment-framework"
description: "Multi-tier security analysis covering AppSec, CloudSec, ContainerSec, CryptoSec, IAM, NetworkSec, OSSec, and ZeroTrust with threat modeling."
capabilities:
  - Application security assessment (OWASP Top 10, API security)
  - Cloud security posture evaluation (AWS, Azure, GCP)
  - Container and Kubernetes security validation
  - Cryptographic implementation analysis
  - Identity and access management review
  - Network security architecture assessment
  - Operating system hardening verification
  - Zero-trust architecture evaluation
  - STRIDE/DREAD threat modeling
  - Security control gap analysis
inputs:
  - target_system: "system/application identifier (string)"
  - security_domains: "array of domains to assess (array, default: all)"
  - assessment_tier: "T1 (quick) | T2 (domain-specific) | T3 (comprehensive) (string, default: T1)"
  - compliance_frameworks: "NIST, FedRAMP, OWASP, CIS (array, optional)"
  - threat_model_required: "boolean (default: false for T1/T2, true for T3)"
outputs:
  - findings: "JSON array of security findings with severity/CVSS scores"
  - threat_model: "STRIDE/DREAD analysis (if requested)"
  - remediation_plan: "Prioritized action items with references"
  - compliance_mapping: "Controls mapped to frameworks (if specified)"
keywords:
  - security-assessment
  - appsec
  - cloudsec
  - container-security
  - cryptography
  - iam
  - network-security
  - ossec
  - zero-trust
  - threat-modeling
  - owasp
  - nist
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
deprecated: true
deprecated_date: "2025-10-26"
deprecation_reason: "Split into 8 focused skills + 1 orchestrator agent for better modularity"
replacement_agent: "security-auditor"
replacement_skills:
  - "security-appsec-validator"
  - "security-cloud-analyzer"
  - "security-container-validator"
  - "security-crypto-validator"
  - "security-iam-reviewer"
  - "security-network-validator"
  - "security-os-validator"
  - "security-zerotrust-assessor"
migration_guide: "/agents/security-auditor/MIGRATION.md"
links:
  - https://owasp.org/www-project-top-ten/
  - https://owasp.org/API-Security/
  - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
  - https://www.cisecurity.org/cis-benchmarks
  - https://www.cisa.gov/zero-trust-maturity-model
  - https://csrc.nist.gov/publications/detail/sp/800-63b/final
  - https://cloud.google.com/architecture/framework/security
  - https://aws.amazon.com/architecture/security-identity-compliance/
---

> **⚠️ DEPRECATED as of 2025-10-26**
>
> This monolithic skill has been split into 8 focused skills + 1 orchestrator agent for better modularity and adherence to CLAUDE.md ≤2 step principle.
>
> **For multi-domain assessments, use:** `/agents/security-auditor/AGENT.md`
>
> **For single-domain assessments, use individual skills:**
> - `/skills/security-security-appsec-validator/SKILL.md`
> - `/skills/security-cloud-analyzer/SKILL.md`
> - `/skills/security-container-validator/SKILL.md`
> - `/skills/security-crypto-validator/SKILL.md`
> - `/skills/security-iam-reviewer/SKILL.md`
> - `/skills/security-network-validator/SKILL.md`
> - `/skills/security-os-validator/SKILL.md`
> - `/skills/security-zerotrust-assessor/SKILL.md`
>
> **Migration guide:** `/agents/security-auditor/MIGRATION.md`
>
> **Archive date:** 2026-01-26 (90-day deprecation period)

## Purpose & When-To-Use

**Trigger conditions:**
- Security audit or assessment required before production deployment
- Compliance requirement (FedRAMP, SOC2, PCI-DSS, HIPAA)
- Incident response or post-breach security review
- Architecture review requiring threat modeling
- Periodic security posture evaluation
- Third-party security questionnaire response
- Zero-trust architecture maturity assessment

**Not for:**
- Real-time intrusion detection (use SIEM/IDS tools)
- Source code vulnerability scanning (use SAST/DAST tools)
- Penetration testing execution (provides methodology only)
- Legal/regulatory compliance interpretation (provides technical controls only)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `target_system` must be a valid identifier with architecture documentation available
- `security_domains` must be subset of: [appsec, cloudsec, containersec, cryptosec, iam, networksec, ossec, zerotrust]
- `assessment_tier` must be: T1, T2, or T3
- `compliance_frameworks` must be valid framework identifiers (if provided)
- `threat_model_required` must be boolean

**Source freshness:**
- OWASP Top 10 (accessed 2025-10-25T21:30:36-04:00): https://owasp.org/www-project-top-ten/ - verify using 2021+ version
- NIST SP 800-53 Rev 5 (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- CIS Benchmarks (accessed 2025-10-25T21:30:36-04:00): https://www.cisecurity.org/cis-benchmarks - verify latest platform versions
- CISA Zero Trust Maturity Model (accessed 2025-10-25T21:30:36-04:00): https://www.cisa.gov/zero-trust-maturity-model

---

## Procedure

### T1: Quick Security Scan (≤2k tokens)

**Fast path for 80% of quick assessments:**

1. **Domain Selection**
   - If `security_domains` is empty → assess all 8 domains at surface level
   - If specified → focus only on requested domains

2. **Critical Controls Check** (per domain)

   **AppSec:**
   - Authentication mechanisms present (OWASP A07:2021 - Identification and Authentication Failures, accessed 2025-10-25T21:30:36-04:00)
   - Input validation on user-facing endpoints
   - SQL injection prevention (parameterized queries)
   - XSS protection (output encoding)

   **CloudSec:**
   - Public S3 buckets or storage (immediate critical finding)
   - IAM overpermissive roles (wildcard policies)
   - Encryption at rest enabled
   - VPC/network segmentation present

   **ContainerSec:**
   - Container images from trusted registries
   - Non-root user execution
   - Resource limits defined
   - Secrets not in environment variables

   **CryptoSec:**
   - TLS 1.2+ enforced
   - Strong cipher suites (no RC4, DES, MD5)
   - Certificate validity
   - Key rotation mechanism exists

   **IAM:**
   - Multi-factor authentication enabled
   - Least privilege principle applied
   - Password policy compliance (NIST SP 800-63B, accessed 2025-10-25T21:30:36-04:00)
   - Service account key rotation

   **NetworkSec:**
   - Firewall rules documented
   - Default deny stance
   - Network segmentation (DMZ, internal zones)
   - VPN/encrypted transit for sensitive data

   **OSSec:**
   - OS patches current (within 30 days)
   - CIS Benchmark compliance (accessed 2025-10-25T21:30:36-04:00)
   - Unnecessary services disabled
   - Host-based firewall active

   **ZeroTrust:**
   - Identity verification on all requests
   - Device trust assessment
   - Micro-segmentation present
   - Continuous monitoring enabled

3. **Severity Scoring**
   - Critical: Immediate exploitation risk (CVSS 9.0-10.0)
   - High: Likely exploitation path (CVSS 7.0-8.9)
   - Medium: Potential vulnerability (CVSS 4.0-6.9)
   - Low: Best practice deviation (CVSS 0.1-3.9)

4. **Quick Findings Output**
   ```json
   {
     "assessment_tier": "T1",
     "timestamp": "NOW_ET",
     "domains_assessed": ["list"],
     "findings": [
       {
         "domain": "appsec|cloudsec|...",
         "severity": "critical|high|medium|low",
         "cvss_score": 0.0,
         "title": "Brief description",
         "control_reference": "OWASP A01|NIST SC-7|CIS 1.2.3"
       }
     ],
     "summary": {
       "critical_count": 0,
       "high_count": 0,
       "medium_count": 0,
       "low_count": 0,
       "overall_risk": "critical|high|medium|low"
     }
   }
   ```

**Decision:** If no critical/high findings OR `assessment_tier == "T1"` → STOP; otherwise proceed to T2.

---

### T2: Domain-Specific Deep Dive (≤6k tokens)

**Extended validation for specific security domains:**

1. **Domain-Specific Frameworks**

   **AppSec - OWASP Top 10 2021 Deep Dive:**
   - A01:2021 - Broken Access Control (accessed 2025-10-25T21:30:36-04:00): https://owasp.org/Top10/A01_2021-Broken_Access_Control/
   - A02:2021 - Cryptographic Failures
   - A03:2021 - Injection (SQL, NoSQL, LDAP, OS command)
   - A04:2021 - Insecure Design (threat modeling required)
   - A05:2021 - Security Misconfiguration
   - A06:2021 - Vulnerable and Outdated Components
   - A07:2021 - Identification and Authentication Failures
   - A08:2021 - Software and Data Integrity Failures
   - A09:2021 - Security Logging and Monitoring Failures
   - A10:2021 - Server-Side Request Forgery (SSRF)

   **API Security:**
   - OWASP API Security Top 10 (accessed 2025-10-25T21:30:36-04:00): https://owasp.org/API-Security/
   - API1:2023 - Broken Object Level Authorization (BOLA)
   - API2:2023 - Broken Authentication
   - API3:2023 - Broken Object Property Level Authorization
   - API4:2023 - Unrestricted Resource Consumption
   - Rate limiting and throttling
   - API key rotation and management

   **CloudSec - Platform-Specific:**
   - AWS Well-Architected Security Pillar (accessed 2025-10-25T21:30:36-04:00): https://aws.amazon.com/architecture/well-architected/
   - Google Cloud Security Framework (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/architecture/framework/security
   - Azure Security Baseline
   - Cloud Security Alliance (CSA) Cloud Controls Matrix
   - Shared responsibility model adherence

   **ContainerSec - CIS Kubernetes Benchmark:**
   - CIS Kubernetes Benchmark v1.8+ (accessed 2025-10-25T21:30:36-04:00): https://www.cisecurity.org/benchmark/kubernetes
   - Pod Security Standards (Baseline, Restricted)
   - Network policies enforcement
   - RBAC configuration review
   - Admission controller policies
   - Image vulnerability scanning integration

   **CryptoSec - NIST Standards:**
   - NIST SP 800-52 Rev 2 - TLS Guidelines (accessed 2025-10-25T21:30:36-04:00)
   - NIST SP 800-175B - Key Management
   - Cryptographic algorithm selection (FIPS 140-2/3 compliance)
   - Certificate lifecycle management
   - Hardware Security Module (HSM) usage

   **IAM - NIST SP 800-63:**
   - NIST SP 800-63B - Digital Identity Guidelines (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-63b/final
   - Authenticator Assurance Levels (AAL1, AAL2, AAL3)
   - Federation and SSO security
   - Privileged Access Management (PAM)
   - Just-in-time (JIT) access provisioning

   **NetworkSec - Defense in Depth:**
   - Network segmentation strategy
   - Micro-segmentation for east-west traffic
   - DMZ architecture validation
   - VPN and remote access security
   - DDoS protection mechanisms
   - Intrusion Prevention System (IPS) coverage

   **OSSec - CIS Benchmarks by OS:**
   - CIS Linux Benchmark (accessed 2025-10-25T21:30:36-04:00)
   - CIS Windows Server Benchmark
   - Kernel hardening (SELinux/AppArmor)
   - File integrity monitoring
   - Patch management process
   - Baseline configuration drift detection

   **ZeroTrust - CISA Maturity Model:**
   - CISA Zero Trust Maturity Model (accessed 2025-10-25T21:30:36-04:00): https://www.cisa.gov/zero-trust-maturity-model
   - Identity pillar: centralized identity management, MFA everywhere
   - Device pillar: device inventory, compliance checking
   - Network pillar: micro-segmentation, encrypted traffic
   - Application pillar: authorization at application layer
   - Data pillar: data categorization, encryption, DLP
   - Maturity level assessment: Traditional → Initial → Advanced → Optimal

2. **Compliance Mapping** (if `compliance_frameworks` provided)
   - Map findings to NIST SP 800-53 controls
   - Map to CIS Controls v8
   - Generate compliance gap report
   - Prioritize remediations by compliance impact

3. **Detailed Remediation Plan**
   - For each finding: provide specific fix steps
   - Include code examples (where applicable)
   - Reference authoritative sources
   - Estimate remediation effort (hours/days)
   - Assign priority based on risk + compliance

**Decision:** If `threat_model_required == true` OR `assessment_tier == "T3"` → proceed to T3; otherwise STOP.

---

### T3: Comprehensive Threat Model & Research (≤12k tokens)

**Deep dive with threat modeling and architectural analysis:**

1. **STRIDE Threat Modeling**
   - **S**poofing: Identity verification weaknesses
   - **T**ampering: Data integrity vulnerabilities
   - **R**epudiation: Logging and audit gaps
   - **I**nformation Disclosure: Data leakage paths
   - **D**enial of Service: Availability attack vectors
   - **E**levation of Privilege: Authorization bypass opportunities

2. **DREAD Risk Rating** (per threat)
   - **D**amage Potential: 1-10 scale
   - **R**eproducibility: How easy to replicate
   - **E**xploitability: Skill level required
   - **A**ffected Users: Scope of impact
   - **D**iscoverability: How easy to find
   - Calculate DREAD Score: (D+R+E+A+D)/5

3. **Attack Tree Construction**
   - Identify attacker goals
   - Map attack paths to goals
   - Calculate path probabilities
   - Identify critical chokepoints
   - Recommend defensive controls per path

4. **Data Flow Diagram (DFD) Security Analysis**
   - Map trust boundaries
   - Identify data flows crossing boundaries
   - Validate authentication/authorization at boundaries
   - Verify encryption in transit
   - Check data validation at entry points

5. **Security Control Framework Mapping**
   - NIST Cybersecurity Framework: Identify, Protect, Detect, Respond, Recover
   - Map existing controls to CSF functions
   - Identify control gaps
   - Recommend compensating controls

6. **Architecture Security Patterns**
   - Evaluate defense-in-depth layers
   - Check fail-secure vs fail-open mechanisms
   - Validate security by design principles
   - Assess security pattern anti-patterns (security through obscurity, etc.)

7. **Comprehensive Report Generation**
   - Executive summary (1 page, non-technical)
   - Threat model diagrams (STRIDE, attack trees)
   - Detailed findings by domain
   - Remediation roadmap with phases
   - Compliance attestation (if applicable)
   - Risk register with residual risk calculations

**Output:** Complete security assessment package ready for stakeholder review.

---

## Decision Rules

**Ambiguity thresholds:**
- If architecture documentation is incomplete → request clarification; DO NOT assume
- If security domain is unclear → assess as AppSec (most common)
- If compliance framework version is ambiguous → use latest published version

**Abort conditions:**
- No architecture documentation available → cannot perform T2/T3
- Target system identifier does not resolve → cannot proceed
- All security domains return "not applicable" → verify target_system is correct

**Escalation triggers:**
- Critical findings (CVSS ≥9.0) → immediately flag for security team
- Active exploitation evidence → escalate to incident response
- Compliance violation with ATO impact → escalate to compliance team

**Tier progression logic:**
- T1 → T2: If high/critical findings OR user explicitly requests T2
- T2 → T3: If threat_model_required OR user explicitly requests T3
- Force stop at T1: If `assessment_tier == "T1"` regardless of findings

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "assessment_tier": "T1|T2|T3",
  "timestamp": "ISO-8601 with timezone",
  "target_system": "string",
  "domains_assessed": ["array of domains"],
  "findings": [
    {
      "id": "unique identifier",
      "domain": "security domain",
      "severity": "critical|high|medium|low",
      "cvss_score": "float 0.0-10.0",
      "title": "brief description",
      "description": "detailed finding",
      "affected_components": ["list"],
      "cwe_id": "CWE-XXX (if applicable)",
      "owasp_category": "A0X:2021 (if applicable)",
      "control_reference": "NIST/CIS/etc control ID",
      "remediation": "specific fix steps",
      "effort_estimate": "hours or days",
      "priority": "1-5 (1=highest)"
    }
  ],
  "summary": {
    "total_findings": "integer",
    "critical_count": "integer",
    "high_count": "integer",
    "medium_count": "integer",
    "low_count": "integer",
    "overall_risk": "critical|high|medium|low"
  }
}
```

**Additional fields for T2:**
- `compliance_mapping`: Object mapping findings to framework controls
- `remediation_plan`: Phased remediation roadmap with timelines

**Additional fields for T3:**
- `threat_model`: STRIDE analysis with attack trees
- `dread_scores`: Risk ratings per threat
- `data_flow_analysis`: DFD with trust boundaries
- `executive_summary`: Non-technical summary for leadership
- `risk_register`: Residual risk calculations

**Type constraints:**
- All timestamps: ISO-8601 format with timezone
- CVSS scores: Float between 0.0 and 10.0 (CVSSv3.1 scoring)
- Severity: Must be one of [critical, high, medium, low]
- Priority: Integer 1-5 (1 is highest priority)

---

## Examples

**Example: T1 Quick Assessment**

```yaml
# Input: T1 Quick Assessment
target_system: "web-application-prod"
security_domains: ["appsec", "cloudsec"]
assessment_tier: "T1"

# Output (abbreviated JSON)
{
  "assessment_tier": "T1",
  "timestamp": "2025-10-25T21:30:36-04:00",
  "domains_assessed": ["appsec", "cloudsec"],
  "findings": [
    {
      "id": "F001",
      "domain": "appsec",
      "severity": "high",
      "cvss_score": 8.1,
      "title": "SQL Injection in /api/users",
      "owasp_category": "A03:2021-Injection"
    }
  ],
  "summary": {
    "critical_count": 0,
    "high_count": 1,
    "overall_risk": "high"
  }
}
```

---

## Quality Gates

**Token budgets (mandatory enforcement):**
- T1: ≤2k tokens - Quick scan only, no deep research
- T2: ≤6k tokens - Domain-specific analysis with 2-4 authoritative sources
- T3: ≤12k tokens - Full threat model with 6-8 authoritative sources and research

**Safety checks:**
- No credential exposure in findings or remediation steps
- No exploitation code provided (methodology only)
- No PII in example outputs

**Auditability:**
- All claims cite OWASP, NIST, CIS, or CISA sources with access dates
- CVSS scores calculated using CVSSv3.1 methodology
- Severity ratings justified by risk impact

**Determinism:**
- Same inputs + same system state = same findings
- Timestamp varies but findings remain consistent
- Control references are stable (e.g., NIST SP 800-53 Rev 5 AC-2)

**Source citation requirements:**
- Tier 1: Minimum 2 sources (OWASP + 1 other)
- Tier 2: Minimum 4 sources (domain-specific standards)
- Tier 3: Minimum 6-8 sources (comprehensive coverage)
- All sources include access date = NOW_ET

---

## Resources

**OWASP Resources:**
- OWASP Top 10 2021: https://owasp.org/www-project-top-ten/ (accessed 2025-10-25T21:30:36-04:00)
- OWASP API Security Top 10: https://owasp.org/API-Security/ (accessed 2025-10-25T21:30:36-04:00)
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/ (accessed 2025-10-25T21:30:36-04:00)

**NIST Publications:**
- NIST SP 800-53 Rev 5 (Security Controls): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (accessed 2025-10-25T21:30:36-04:00)
- NIST SP 800-63B (Digital Identity): https://csrc.nist.gov/publications/detail/sp/800-63b/final (accessed 2025-10-25T21:30:36-04:00)
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework (accessed 2025-10-25T21:30:36-04:00)

**CIS Resources:**
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks (accessed 2025-10-25T21:30:36-04:00)
- CIS Controls v8: https://www.cisecurity.org/controls (accessed 2025-10-25T21:30:36-04:00)

**Cloud Security:**
- AWS Security Best Practices: https://aws.amazon.com/architecture/security-identity-compliance/ (accessed 2025-10-25T21:30:36-04:00)
- Google Cloud Security: https://cloud.google.com/architecture/framework/security (accessed 2025-10-25T21:30:36-04:00)
- Azure Security: https://learn.microsoft.com/azure/security/ (accessed 2025-10-25T21:30:36-04:00)

**Zero Trust:**
- CISA Zero Trust Maturity Model: https://www.cisa.gov/zero-trust-maturity-model (accessed 2025-10-25T21:30:36-04:00)
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/publications/detail/sp/800-207/final (accessed 2025-10-25T21:30:36-04:00)

**Threat Modeling:**
- Microsoft STRIDE: https://learn.microsoft.com/security/engineering/threat-modeling (accessed 2025-10-25T21:30:36-04:00)
- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling (accessed 2025-10-25T21:30:36-04:00)

**Container Security:**
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker (accessed 2025-10-25T21:30:36-04:00)
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes (accessed 2025-10-25T21:30:36-04:00)
