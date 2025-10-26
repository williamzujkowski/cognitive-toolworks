---
name: "Application Security Validator"
slug: "security-appsec-validator"
description: "Validate application security using OWASP Top 10 2021 and API Security Top 10 guidelines with injection prevention and access control checks."
capabilities:
  - OWASP Top 10 2021 compliance checking
  - API security validation (OWASP API Security Top 10)
  - SQL injection and XSS prevention verification
  - Authentication and authorization review
  - Security misconfiguration detection
inputs:
  - application_identifier: "Application or API identifier (string, required)"
  - assessment_scope: "web-app | api | mobile-backend (string, default: web-app)"
  - check_level: "critical-only | standard | comprehensive (string, default: standard)"
outputs:
  - findings: "JSON array of AppSec findings with OWASP category and CVSS scores"
  - owasp_coverage: "Coverage map of OWASP Top 10 categories assessed"
  - remediation_steps: "Specific fix guidance with code examples"
keywords:
  - appsec
  - owasp
  - web-security
  - api-security
  - injection
  - xss
  - authentication
  - authorization
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://owasp.org/www-project-top-ten/
  - https://owasp.org/API-Security/
  - https://cheatsheetseries.owasp.org/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Application security review before production deployment
- API security validation required
- Post-incident application security assessment
- Compliance requirement for web application security (OWASP alignment)
- Third-party application security questionnaire response

**Not for:**
- Automated SAST/DAST tool execution (provides methodology only)
- Penetration testing (provides control verification only)
- Infrastructure or cloud security (use security-cloud-analyzer)
- Network security assessment (use security-network-validator)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `application_identifier` must be non-empty string
- `assessment_scope` must be one of: [web-app, api, mobile-backend]
- `check_level` must be one of: [critical-only, standard, comprehensive]

**Source freshness:**
- OWASP Top 10 2021 (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/www-project-top-ten/
- OWASP API Security Top 10 2023 (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/API-Security/
- OWASP Cheat Sheet Series (accessed 2025-10-26T01:33:55-04:00): https://cheatsheetseries.owasp.org/

---

## Procedure

### Step 1: Critical Controls Check

**For web-app and mobile-backend:**
1. **A01:2021 - Broken Access Control** (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/Top10/A01_2021-Broken_Access_Control/
   - Verify authorization checks on protected resources
   - Check for insecure direct object references (IDOR)
   - Validate access control enforcement at API/backend layer

2. **A03:2021 - Injection** (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/Top10/A03_2021-Injection/
   - SQL injection prevention: parameterized queries or ORM usage
   - XSS protection: output encoding and Content Security Policy
   - Command injection: input validation and safe API usage

3. **A07:2021 - Identification and Authentication Failures** (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
   - Multi-factor authentication available for sensitive operations
   - Password policy compliance
   - Session management security (secure cookies, timeout)

**For api scope:**
1. **API1:2023 - Broken Object Level Authorization (BOLA)** (accessed 2025-10-26T01:33:55-04:00): https://owasp.org/API-Security/
   - Object-level authorization on every API endpoint
   - User context validation for resource access

2. **API2:2023 - Broken Authentication**
   - API key/token management and rotation
   - Authentication mechanism strength

3. **API4:2023 - Unrestricted Resource Consumption**
   - Rate limiting implementation
   - Request throttling and quotas

### Step 2: Generate Findings with Severity Scoring

For each failed check:
- Assign CVSS v3.1 score based on exploitability and impact
- Map to OWASP category (A01-A10 or API1-API10)
- Provide specific remediation steps with code examples where applicable

**Token budget:** T1 ≤2k tokens (critical-only), T2 ≤6k tokens (standard), T3 ≤12k tokens (comprehensive)

---

## Decision Rules

**Ambiguity thresholds:**
- If application architecture is unclear → request application documentation
- If authentication mechanism is not documented → flag as unknown risk

**Abort conditions:**
- No application identifier provided → cannot proceed
- Application architecture documentation unavailable → limited to surface-level checks only

**Severity classification:**
- Critical: Immediate exploitation risk (CVSS 9.0-10.0)
- High: Likely exploitation path (CVSS 7.0-8.9)
- Medium: Potential vulnerability (CVSS 4.0-6.9)
- Low: Best practice deviation (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "application_identifier": "string",
  "assessment_scope": "web-app|api|mobile-backend",
  "check_level": "critical-only|standard|comprehensive",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "owasp_category": "A01:2021|A02:2021|...|API1:2023|API2:2023|...",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "affected_endpoints": ["list of URLs or API paths"],
      "cwe_id": "CWE-XXX",
      "remediation": "specific fix steps with code examples",
      "references": ["URLs to OWASP guidance"]
    }
  ],
  "owasp_coverage": {
    "categories_assessed": ["A01:2021", "A02:2021", "..."],
    "categories_passed": ["list"],
    "categories_failed": ["list"]
  },
  "summary": {
    "total_findings": 0,
    "critical_count": 0,
    "high_count": 0,
    "medium_count": 0,
    "low_count": 0,
    "overall_risk": "critical|high|medium|low"
  }
}
```

**Type constraints:**
- CVSS scores: Float 0.0-10.0 (CVSSv3.1)
- Severity: Must be one of [critical, high, medium, low]
- Timestamps: ISO-8601 with timezone

---

## Examples

**Example: API Security Check**

```yaml
# Input
application_identifier: "payment-api-v2"
assessment_scope: "api"
check_level: "standard"

# Output (abbreviated)
{
  "application_identifier": "payment-api-v2",
  "assessment_scope": "api",
  "findings": [
    {
      "id": "APPSEC-001",
      "owasp_category": "API1:2023-BOLA",
      "severity": "high",
      "cvss_score": 8.1,
      "title": "Missing object-level authorization on /api/transactions/{id}",
      "remediation": "Add user ownership check before returning transaction data"
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

**Token budgets:**
- Critical-only: ≤2k tokens (top 3 OWASP categories only)
- Standard: ≤6k tokens (all critical + high severity checks)
- Comprehensive: ≤12k tokens (full OWASP Top 10 coverage with examples)

**Safety:**
- No credential exposure in findings
- No exploitation code provided

**Auditability:**
- All findings cite OWASP categories with access dates
- CVSS scores follow CVSSv3.1 methodology

**Determinism:**
- Same application state + inputs = consistent findings
- OWASP category mappings are stable

---

## Resources

**OWASP Top 10 2021:**
- A01:2021 - Broken Access Control: https://owasp.org/Top10/A01_2021-Broken_Access_Control/ (accessed 2025-10-26T01:33:55-04:00)
- A02:2021 - Cryptographic Failures: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/ (accessed 2025-10-26T01:33:55-04:00)
- A03:2021 - Injection: https://owasp.org/Top10/A03_2021-Injection/ (accessed 2025-10-26T01:33:55-04:00)
- Full Top 10: https://owasp.org/www-project-top-ten/ (accessed 2025-10-26T01:33:55-04:00)

**OWASP API Security:**
- API Security Top 10 2023: https://owasp.org/API-Security/ (accessed 2025-10-26T01:33:55-04:00)
- API Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html (accessed 2025-10-26T01:33:55-04:00)

**Additional Resources:**
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/ (accessed 2025-10-26T01:33:55-04:00)
- CWE Top 25: https://cwe.mitre.org/top25/ (accessed 2025-10-26T01:33:55-04:00)
