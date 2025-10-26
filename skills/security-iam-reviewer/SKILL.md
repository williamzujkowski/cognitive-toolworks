---
name: "IAM Security Reviewer"
slug: "security-iam-reviewer"
description: "Review identity and access management using NIST SP 800-63B guidelines with MFA enforcement, password policy, and least privilege validation."
capabilities:
  - Multi-factor authentication (MFA) enforcement review
  - Password policy compliance (NIST SP 800-63B)
  - Least privilege principle verification
  - Service account key rotation validation
  - Privileged Access Management (PAM) assessment
inputs:
  - identity_provider: "System or IAM service identifier (string, required)"
  - iam_scope: "authentication | authorization | accounts | all (string, default: all)"
  - authenticator_level: "AAL1 | AAL2 | AAL3 (string, optional for NIST compliance)"
outputs:
  - findings: "JSON array of IAM security findings with NIST 800-63B references"
  - nist_aal_compliance: "Authenticator Assurance Level compliance (if requested)"
  - remediation_policies: "IAM policy JSON or configuration snippets"
keywords:
  - iam
  - identity
  - authentication
  - authorization
  - mfa
  - password-policy
  - least-privilege
  - pam
  - nist-800-63b
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://csrc.nist.gov/publications/detail/sp/800-63b/final
  - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
---

## Purpose & When-To-Use

**Trigger conditions:**
- IAM security audit before production deployment
- NIST SP 800-63B compliance requirement
- Post-incident identity and access review
- Privileged access management (PAM) assessment
- Third-party IAM security questionnaire

**Not for:**
- IAM system implementation (provides assessment only)
- Real-time access monitoring (use SIEM/access analytics tools)
- Cloud-specific IAM (use security-cloud-analyzer for AWS/Azure/GCP IAM)
- Application-level authentication (use security-appsec-validator)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `identity_provider` must be non-empty string
- `iam_scope` must be one of: [authentication, authorization, accounts, all]
- `authenticator_level` must be one of: [AAL1, AAL2, AAL3] or omitted

**Source freshness:**
- NIST SP 800-63B Digital Identity Guidelines (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-63b/final
- NIST SP 800-53 Rev 5 IAM Controls (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

---

## Procedure

### Step 1: Critical IAM Controls Check

**Authentication:**
1. Multi-factor authentication (MFA) enabled for privileged accounts
2. Password policy compliance per NIST SP 800-63B (accessed 2025-10-26T01:33:55-04:00):
   - Minimum 8 characters (12+ for privileged accounts)
   - No complexity requirements (NIST deprecates forced character mixing)
   - Password breach database checking
   - No periodic password rotation (only change on compromise)
3. Session timeout configured (15-30 minutes for privileged access)
4. Secure session cookies (HttpOnly, Secure, SameSite)

**Authorization:**
1. Least privilege principle applied (no overpermissive roles)
2. Role-based access control (RBAC) or attribute-based access control (ABAC)
3. Separation of duties for critical operations
4. Just-in-time (JIT) access provisioning for privileged operations

**Account Management:**
1. Service account key rotation (90-day max age)
2. Inactive account deactivation (30-60 days of inactivity)
3. Privileged account monitoring and logging
4. No shared accounts for individual users

### Step 2: NIST Authenticator Assurance Level (AAL) Compliance

If `authenticator_level` specified, validate:
- **AAL1:** Single-factor authentication acceptable
- **AAL2:** MFA required (something you know + something you have)
- **AAL3:** Hardware-based authenticator required (FIDO2, smart card)

**Token budgets:**
- **T1:** ≤2k tokens (critical IAM controls)
- **T2:** ≤6k tokens (full IAM audit with NIST AAL compliance)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If IAM configuration unavailable → request policy documents or admin access
- If password policy unclear → request authentication system documentation

**Abort conditions:**
- No identity provider specified → cannot proceed
- No IAM policies or user data accessible → limited to documentation review

**Severity classification:**
- Critical: No MFA on admin accounts, shared credentials (CVSS 9.0-10.0)
- High: Overpermissive policies, no key rotation (CVSS 7.0-8.9)
- Medium: Password policy gaps, missing session timeout (CVSS 4.0-6.9)
- Low: Best practice deviations (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "identity_provider": "string",
  "iam_scope": "authentication|authorization|accounts|all",
  "authenticator_level": "AAL1|AAL2|AAL3 or null",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "category": "authentication|authorization|account-management",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "nist_reference": "SP 800-63B section X.Y or SP 800-53 AC-2",
      "affected_accounts": ["account names or roles"],
      "remediation": "specific fix steps",
      "remediation_policy": "IAM policy JSON or config snippet"
    }
  ],
  "nist_aal_compliance": {
    "target_level": "AAL1|AAL2|AAL3",
    "current_level": "AAL1|AAL2|AAL3",
    "compliant": true,
    "gaps": ["list of gaps if not compliant"]
  },
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "overall_risk": "critical|high|medium|low"
  }
}
```

---

## Examples

**Example: MFA Enforcement Check**

```yaml
# Input
identity_provider: "corporate-idp"
iam_scope: "authentication"
authenticator_level: "AAL2"

# Output (abbreviated)
{
  "identity_provider": "corporate-idp",
  "findings": [
    {
      "id": "IAM-001",
      "category": "authentication",
      "severity": "critical",
      "cvss_score": 9.1,
      "title": "MFA not enforced for admin role",
      "nist_reference": "SP 800-63B Section 4.2 (AAL2)",
      "remediation": "Enable MFA requirement for all admin accounts"
    }
  ],
  "nist_aal_compliance": {
    "target_level": "AAL2",
    "current_level": "AAL1",
    "compliant": false,
    "gaps": ["MFA not enforced"]
  },
  "summary": {"critical_count": 1, "overall_risk": "critical"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical IAM controls)
- T2 ≤6k tokens (full IAM audit with NIST AAL compliance)

**Safety:**
- No credentials or tokens in examples
- No actual account names in public findings

**Auditability:**
- Findings cite NIST SP 800-63B or SP 800-53 controls
- Password policy recommendations align with current NIST guidance

**Determinism:**
- Same IAM state + inputs = consistent findings

---

## Resources

**NIST Standards:**
- NIST SP 800-63B (Digital Identity Guidelines): https://csrc.nist.gov/publications/detail/sp/800-63b/final (accessed 2025-10-26T01:33:55-04:00)
- NIST SP 800-53 Rev 5 (IAM Controls AC family): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (accessed 2025-10-26T01:33:55-04:00)

**IAM Best Practices:**
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html (accessed 2025-10-26T01:33:55-04:00)
- CIS Controls v8 (Access Control): https://www.cisecurity.org/controls (accessed 2025-10-26T01:33:55-04:00)

**Privileged Access:**
- NIST Privileged Account Management: https://csrc.nist.gov/glossary/term/privileged_account (accessed 2025-10-26T01:33:55-04:00)
