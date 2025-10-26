---
name: "Software Supply Chain Security Validator"
slug: "security-supplychain-validator"
description: "Validate software supply chain security with SBOM generation, dependency scanning, provenance verification, and SLSA attestation."
capabilities:
  - Generate SPDX and CycloneDX SBOMs
  - Scan dependencies for known vulnerabilities
  - Verify SLSA provenance and build attestations
  - Validate Sigstore signatures and transparency logs
  - Assess supply chain security posture
  - Generate compliance evidence for EO 14028
inputs:
  - artifact_type: "source code | container image | binary | package (string)"
  - artifact_location: "path, URL, or registry reference (string)"
  - sbom_format: "spdx | cyclonedx | both (string, default: spdx)"
  - slsa_level: "target SLSA level 1-4 (number, optional)"
  - vulnerability_threshold: "low | medium | high | critical (string, default: medium)"
  - verification_tier: "T1 (basic) | T2 (full validation) (string, default: T1)"
outputs:
  - sbom: "generated SBOM in requested format(s)"
  - vulnerabilities: "array of CVEs with severity, CVSS scores, remediation"
  - provenance: "SLSA provenance attestation (if available)"
  - signature_verification: "Sigstore/Cosign verification results"
  - compliance_report: "EO 14028 compliance status"
  - risk_score: "numerical supply chain risk assessment (0-100)"
keywords:
  - supply-chain-security
  - sbom
  - spdx
  - cyclonedx
  - slsa
  - provenance
  - sigstore
  - cosign
  - vulnerability-scanning
  - dependency-analysis
  - eo-14028
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://slsa.dev/spec/v1.0/
  - https://spdx.dev/use/specifications/
  - https://cyclonedx.org/specification/overview/
  - https://www.nist.gov/itl/executive-order-improving-nations-cybersecurity
  - https://docs.sigstore.dev/
  - https://www.cisa.gov/sbom
---

## Purpose & When-To-Use

**Trigger conditions:**
- SBOM generation required for compliance (EO 14028, NTIA minimum elements)
- Pre-deployment dependency vulnerability assessment
- SLSA provenance verification for critical artifacts
- Supply chain risk evaluation for third-party components
- Container image security validation before deployment
- Software procurement requiring supply chain attestation
- Zero-trust deployment requiring artifact provenance

**Not for:**
- Source code static analysis (use SAST tools)
- Runtime vulnerability detection (use runtime security agents)
- License compliance analysis (use dedicated license scanners)
- Malware detection (use AV/EDR solutions)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T22:34:11-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `artifact_type` must be one of: source, container, binary, package
- `artifact_location` must be accessible path/URL or valid registry reference
- `sbom_format` must be: spdx, cyclonedx, or both
- `slsa_level` if specified must be integer 1-4
- `vulnerability_threshold` must be: low, medium, high, or critical
- `verification_tier` must be: T1 or T2

**Source freshness:**
- SLSA v1.0 specification (accessed 2025-10-25T22:34:11-04:00): https://slsa.dev/spec/v1.0/
- SPDX 2.3 specification (accessed 2025-10-25T22:34:11-04:00): https://spdx.github.io/spdx-spec/v2.3/
- CycloneDX 1.5 specification (accessed 2025-10-25T22:34:11-04:00): https://cyclonedx.org/docs/1.5/
- NIST EO 14028 guidance (accessed 2025-10-25T22:34:11-04:00): https://www.nist.gov/itl/executive-order-improving-nations-cybersecurity/software-security-supply-chains
- Sigstore documentation (accessed 2025-10-25T22:34:11-04:00): https://docs.sigstore.dev/
- CISA SBOM guidance (accessed 2025-10-25T22:34:11-04:00): https://www.cisa.gov/sbom

---

## Procedure

### T1: Basic SBOM Generation and Vulnerability Scan (≤2k tokens)

**Fast path for 80% of supply chain validation:**

1. **Artifact identification:**
   - Detect artifact type from extension, manifest, or registry metadata
   - Extract package manager files (package.json, go.mod, requirements.txt, pom.xml, etc.)
   - Identify base images for containers

2. **SBOM generation:**
   - Use format-appropriate tooling:
     - SPDX: syft, spdx-sbom-generator, or tern
     - CycloneDX: cyclonedx-cli, cdxgen, or syft
   - Include NTIA minimum elements:
     - Supplier name, component name, version, unique identifier
     - Dependency relationships, author, timestamp
   - Output to file: `<artifact>-sbom.<format>`

3. **Vulnerability scanning:**
   - Scan SBOM against NVD, OSV, GitHub Advisory Database
   - Tools: grype, trivy, osv-scanner
   - Filter by `vulnerability_threshold`
   - Report: CVE ID, severity, CVSS score, affected component, fix version

4. **Basic compliance check:**
   - Verify SBOM contains NTIA minimum elements
   - Flag components with critical/high vulnerabilities
   - Output: pass/fail with findings count

**Decision point:** If `slsa_level` specified or `verification_tier=T2` → proceed to T2

**T1 output schema:**
```json
{
  "sbom_location": "path/to/sbom.spdx.json",
  "format": "spdx",
  "component_count": 247,
  "vulnerabilities": [
    {
      "cve_id": "CVE-2024-1234",
      "severity": "HIGH",
      "cvss_score": 8.2,
      "component": "lodash@4.17.20",
      "fixed_version": "4.17.21",
      "description": "Prototype pollution vulnerability"
    }
  ],
  "critical_count": 2,
  "high_count": 5,
  "compliance": "PASS_WITH_WARNINGS"
}
```

### T2: Full Provenance Verification and SLSA Attestation (≤6k tokens)

**Extended validation with provenance and attestation:**

1. **SLSA provenance retrieval:**
   - Check for in-toto attestation bundles
   - Query Sigstore Rekor transparency log for provenance
   - Verify provenance schema matches SLSA level requirements
   - Extract build metadata: source repo, commit SHA, build timestamp, builder identity

2. **SLSA level assessment:**
   - L1: Build process documented, provenance available
   - L2: Version control, hosted build service, provenance generated by build service
   - L3: Hardened builds, non-falsifiable provenance
   - L4: Two-party review, hermetic builds
   - Compare actual vs. target `slsa_level`

3. **Signature verification:**
   - Verify Sigstore/Cosign signatures using Rekor transparency log
   - Check certificate validity and issuer (GitHub, GitLab, etc.)
   - Validate signature chain of trust
   - Tools: cosign verify, sigstore-python
   - Output: verified/failed with certificate details

4. **Dependency provenance:**
   - For each dependency in SBOM, attempt provenance retrieval
   - Calculate provenance coverage percentage
   - Flag unpinned dependencies (floating versions)
   - Identify dependencies without SLSA attestation

5. **Supply chain risk scoring:**
   - Base score: 100
   - Deduct for: missing SLSA attestation (-20), critical CVEs (-10 each), unpinned deps (-5), no signature (-15)
   - Deduct for: typosquatting risk (-10), unmaintained packages (-5), deprecated deps (-5)
   - Output: 0-100 risk score (lower is riskier)

6. **EO 14028 compliance report:**
   - SBOM present and complete (NTIA elements): yes/no
   - SBOM machine-readable format: yes/no
   - Cryptographic signing present: yes/no
   - Provenance attestation available: yes/no
   - Overall compliance: COMPLIANT | PARTIAL | NON_COMPLIANT

**T2 output schema:**
```json
{
  "sbom": { /* T1 output */ },
  "provenance": {
    "available": true,
    "slsa_level": "SLSA_BUILD_LEVEL_3",
    "builder": "https://github.com/slsa-framework/slsa-github-generator/.github/workflows/builder.yml@v1.2.0",
    "source_repo": "https://github.com/org/repo",
    "commit_sha": "abc123def456",
    "build_timestamp": "2025-10-24T14:32:00Z"
  },
  "signature_verification": {
    "verified": true,
    "signer": "sigstore.dev",
    "certificate_identity": "https://github.com/org/repo/.github/workflows/release.yml@refs/heads/main",
    "transparency_log_entry": "https://rekor.sigstore.dev/api/v1/log/entries/24296fb24b8ad77a..."
  },
  "dependency_provenance_coverage": "67%",
  "risk_score": 75,
  "eo_14028_compliance": {
    "sbom_present": true,
    "sbom_machine_readable": true,
    "cryptographic_signing": true,
    "provenance_attestation": true,
    "overall": "COMPLIANT"
  }
}
```

---

## Decision Rules

**SBOM format selection:**
- Default to SPDX for broad compatibility and NTIA alignment
- Use CycloneDX for security-focused use cases (includes VEX)
- Generate both formats if `sbom_format=both` and artifact is production-critical

**Vulnerability threshold enforcement:**
- `critical`: Block deployment if any CRITICAL severity CVEs found
- `high`: Block if CRITICAL or HIGH severity CVEs found
- `medium`: Block if CRITICAL, HIGH, or MEDIUM severity CVEs found
- `low`: Report all vulnerabilities but allow deployment

**SLSA level requirements:**
- L1-L2: Basic provenance sufficient for most internal tools
- L3: Recommended for production services handling sensitive data
- L4: Required for critical infrastructure, supply chain integrity paramount

**Abort conditions:**
- Artifact not found or inaccessible → ABORT with error
- SBOM generation fails (missing package manager files) → ABORT with suggestions
- Signature verification fails and artifact is production-bound → ABORT with security warning
- Vulnerability count exceeds threshold → ABORT with remediation guidance

---

## Output Contract

**Required fields (all tiers):**
- `sbom_location` (string): path to generated SBOM file
- `format` (string): spdx | cyclonedx
- `component_count` (number): total dependencies found
- `vulnerabilities` (array): CVE objects with id, severity, cvss_score, component, fixed_version, description
- `critical_count` (number): count of CRITICAL severity vulnerabilities
- `high_count` (number): count of HIGH severity vulnerabilities
- `compliance` (string): PASS | PASS_WITH_WARNINGS | FAIL

**Additional fields (T2 only):**
- `provenance` (object): SLSA provenance details
- `signature_verification` (object): cryptographic verification results
- `dependency_provenance_coverage` (string): percentage of dependencies with provenance
- `risk_score` (number): 0-100 supply chain risk score
- `eo_14028_compliance` (object): Executive Order compliance details

**Output formats:**
- JSON (default): machine-readable for CI/CD integration
- Markdown report: human-readable summary for documentation
- SARIF: for integration with code scanning platforms

---

## Examples

**Example: Container image SBOM generation and vulnerability scan**

```bash
# Input: artifact_type=container, location=ghcr.io/org/app:v1.2.3, tier=T1

# Generate SBOM and scan
syft ghcr.io/org/app:v1.2.3 -o spdx-json > app-sbom.spdx.json
grype sbom:app-sbom.spdx.json --fail-on high

# Output
{
  "sbom_location": "app-sbom.spdx.json",
  "component_count": 312,
  "vulnerabilities": [{
    "cve_id": "CVE-2024-5678",
    "severity": "CRITICAL",
    "cvss_score": 9.8,
    "component": "openssl@1.1.1k",
    "fixed_version": "1.1.1w"
  }],
  "critical_count": 1,
  "high_count": 3,
  "compliance": "FAIL"
}
# See examples/sbom-example.txt for full example
```

---

## Quality Gates

**Token budgets (mandatory enforcement):**
- T1: ≤2k tokens - SBOM generation + basic vulnerability scan
- T2: ≤6k tokens - + provenance verification + SLSA attestation + risk scoring
- T3: N/A - skill does not implement T3 tier

**Safety checks:**
- Never expose secrets, API keys, or credentials in SBOM output
- Redact internal paths that reveal infrastructure details
- Sanitize build metadata to remove sensitive information

**Auditability:**
- All SBOM generation commands logged with timestamps
- Vulnerability database versions recorded (NVD snapshot date)
- Provenance verification results cryptographically signed
- Full audit trail for EO 14028 compliance

**Determinism:**
- Same artifact + same tool versions → identical SBOM (excluding timestamps)
- Vulnerability scan results deterministic for same database version
- SLSA level assessment follows specification strictly

**Performance targets:**
- T1: <60 seconds for typical application (100-500 dependencies)
- T2: <180 seconds including provenance retrieval and signature verification
- Timeout after 300 seconds with partial results

---

## Resources

**SLSA Framework:**
- SLSA v1.0 Specification: https://slsa.dev/spec/v1.0/
- SLSA Tooling: https://github.com/slsa-framework
- SLSA GitHub Generator: https://github.com/slsa-framework/slsa-github-generator

**SBOM Standards:**
- SPDX 2.3 Specification: https://spdx.github.io/spdx-spec/v2.3/
- CycloneDX 1.5 Specification: https://cyclonedx.org/docs/1.5/
- NTIA Minimum Elements: https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf

**Tools:**
- Syft (SBOM generation): https://github.com/anchore/syft
- Grype (vulnerability scanning): https://github.com/anchore/grype
- Trivy (multi-scanner): https://github.com/aquasecurity/trivy
- Sigstore/Cosign (signing): https://github.com/sigstore/cosign
- OSV-Scanner: https://github.com/google/osv-scanner

**Compliance:**
- NIST EO 14028 Guidance: https://www.nist.gov/itl/executive-order-improving-nations-cybersecurity
- CISA SBOM Resources: https://www.cisa.gov/sbom
- OpenSSF Best Practices: https://bestpractices.coreinfrastructure.org/

**Vulnerability Databases:**
- National Vulnerability Database: https://nvd.nist.gov/
- OSV (Open Source Vulnerabilities): https://osv.dev/
- GitHub Advisory Database: https://github.com/advisories
