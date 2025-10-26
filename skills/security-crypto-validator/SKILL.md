---
name: "Cryptographic Security Validator"
slug: "security-crypto-validator"
description: "Validate cryptographic implementations using NIST standards with TLS configuration, cipher suite analysis, and certificate lifecycle checks."
capabilities:
  - TLS 1.2+ enforcement validation
  - Cipher suite strength analysis (no weak ciphers)
  - Certificate validity and lifecycle management
  - Key rotation mechanism verification
  - FIPS 140-2/3 compliance checking
inputs:
  - target_system: "System or application identifier (string, required)"
  - crypto_scope: "tls | certificates | key-management | all (string, default: all)"
  - compliance_standard: "nist | fips | pci-dss | none (string, default: nist)"
outputs:
  - findings: "JSON array of cryptographic security findings with NIST references"
  - compliance_status: "NIST/FIPS/PCI-DSS compliance status (if requested)"
  - remediation_config: "TLS/cipher configuration snippets"
keywords:
  - cryptography
  - tls
  - ssl
  - certificates
  - encryption
  - key-management
  - cipher-suites
  - nist
  - fips
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final
  - https://csrc.nist.gov/publications/detail/sp/800-175b/final
  - https://csrc.nist.gov/projects/cryptographic-module-validation-program
---

## Purpose & When-To-Use

**Trigger conditions:**
- Cryptographic implementation review before production deployment
- TLS/SSL configuration audit
- Certificate lifecycle management validation
- FIPS 140-2/3 compliance requirement
- Post-incident cryptographic security assessment

**Not for:**
- Cryptographic algorithm design (use research/academic resources)
- Quantum-resistant cryptography evaluation (requires specialized analysis)
- Application-level encryption implementation (use security-appsec-validator)
- Physical HSM security assessment (requires on-site evaluation)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `target_system` must be non-empty string
- `crypto_scope` must be one of: [tls, certificates, key-management, all]
- `compliance_standard` must be one of: [nist, fips, pci-dss, none]

**Source freshness:**
- NIST SP 800-52 Rev 2 - TLS Guidelines (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final
- NIST SP 800-175B - Key Management (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-175b/final
- FIPS 140-2/3 Standards (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/projects/cryptographic-module-validation-program

---

## Procedure

### Step 1: Critical Cryptographic Controls Check

**TLS Configuration:**
1. TLS 1.2 or higher enforced (TLS 1.0/1.1 disabled)
2. Strong cipher suites only (per NIST SP 800-52 Rev 2, accessed 2025-10-26T01:33:55-04:00)
   - Prohibited: RC4, DES, 3DES, MD5, SHA-1 for signatures
   - Required: AES-GCM, ChaCha20-Poly1305, ECDHE/DHE key exchange
3. Perfect Forward Secrecy (PFS) enabled
4. Secure renegotiation configured

**Certificate Management:**
1. Certificate validity (not expired, not self-signed for production)
2. Certificate chain completeness
3. Certificate revocation checking (OCSP or CRL)
4. Key strength (RSA ≥2048-bit, ECC ≥256-bit)
5. Certificate rotation process exists

**Key Management:**
1. Key rotation mechanism present (90-day max for high-security)
2. Keys stored in HSM or secure key management service
3. No hardcoded keys in code or configuration
4. Separate keys for encryption vs signing

### Step 2: Generate NIST-Aligned Remediation

For each finding, provide:
- NIST SP 800-52/175B control reference
- TLS/cipher configuration snippets (Apache, Nginx, IIS, etc.)
- Certificate management procedures

**Token budgets:**
- **T1:** ≤2k tokens (critical TLS/certificate findings)
- **T2:** ≤6k tokens (full cryptographic audit with NIST compliance)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If TLS configuration unavailable → request server config files or scan results
- If certificate details missing → request certificate chain PEM files

**Abort conditions:**
- No target system specified → cannot proceed
- No TLS endpoints or certificates found → verify system has encrypted communications

**Severity classification:**
- Critical: Weak ciphers (RC4, DES), expired certificates (CVSS 9.0-10.0)
- High: TLS 1.0/1.1 enabled, missing PFS (CVSS 7.0-8.9)
- Medium: Certificate rotation gaps, weak key sizes (CVSS 4.0-6.9)
- Low: OCSP stapling missing, cipher ordering (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "target_system": "string",
  "crypto_scope": "tls|certificates|key-management|all",
  "compliance_standard": "nist|fips|pci-dss|none",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "category": "tls|certificate|key-management",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "nist_reference": "SP 800-52 Rev 2 section X.Y",
      "affected_endpoints": ["URLs or service names"],
      "remediation": "specific fix steps",
      "remediation_config": "configuration snippet"
    }
  ],
  "compliance_status": {
    "standard": "nist|fips|pci-dss",
    "controls_assessed": ["list"],
    "controls_passed": ["list"],
    "controls_failed": ["list"]
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

**Example: TLS Configuration Check**

```yaml
# Input
target_system: "api.example.com"
crypto_scope: "tls"
compliance_standard: "nist"

# Output (abbreviated)
{
  "target_system": "api.example.com",
  "findings": [
    {
      "id": "CRYPTO-001",
      "category": "tls",
      "severity": "high",
      "cvss_score": 7.4,
      "title": "TLS 1.1 enabled (deprecated protocol)",
      "nist_reference": "SP 800-52 Rev 2 Section 3.1",
      "remediation_config": "SSLProtocol -all +TLSv1.2 +TLSv1.3"
    }
  ],
  "summary": {"high_count": 1, "overall_risk": "high"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical TLS/certificate findings)
- T2 ≤6k tokens (full cryptographic audit with NIST compliance)

**Safety:**
- No private keys in examples or remediation
- No actual certificate details

**Auditability:**
- Findings cite NIST SP 800-52/175B references
- Cipher recommendations align with current NIST guidance

**Determinism:**
- Same TLS/certificate state + inputs = consistent findings

---

## Resources

**NIST Standards:**
- NIST SP 800-52 Rev 2 (TLS Guidelines): https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final (accessed 2025-10-26T01:33:55-04:00)
- NIST SP 800-175B (Key Management): https://csrc.nist.gov/publications/detail/sp/800-175b/final (accessed 2025-10-26T01:33:55-04:00)
- FIPS 140-2/3 Standards: https://csrc.nist.gov/projects/cryptographic-module-validation-program (accessed 2025-10-26T01:33:55-04:00)

**TLS Configuration Guides:**
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/ (accessed 2025-10-26T01:33:55-04:00)
- OWASP TLS Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html (accessed 2025-10-26T01:33:55-04:00)

**Certificate Management:**
- CA/Browser Forum Baseline Requirements: https://cabforum.org/baseline-requirements-documents/ (accessed 2025-10-26T01:33:55-04:00)
