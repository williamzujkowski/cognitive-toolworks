---
name: "Cloud Security Posture Analyzer"
slug: "cloudsec-posture-analyzer"
description: "Evaluate cloud security posture across AWS, Azure, and GCP with storage exposure checks, IAM policy review, and encryption validation."
capabilities:
  - Public storage bucket detection (S3, Azure Storage, GCS)
  - IAM overpermissive policy identification
  - Encryption at rest and in transit validation
  - VPC/network segmentation verification
  - Cloud platform security best practices alignment
inputs:
  - cloud_platform: "aws | azure | gcp (string, required)"
  - resource_scope: "storage | iam | network | compute | all (string, default: all)"
  - compliance_check: "cis | well-architected | both | none (string, default: none)"
outputs:
  - findings: "JSON array of cloud security findings with platform-specific details"
  - compliance_status: "CIS Benchmark or Well-Architected alignment (if requested)"
  - remediation_commands: "Platform-specific CLI commands for fixes"
keywords:
  - cloud-security
  - aws-security
  - azure-security
  - gcp-security
  - iam
  - storage-security
  - encryption
  - network-security
  - cis-benchmark
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://aws.amazon.com/architecture/security-identity-compliance/
  - https://cloud.google.com/architecture/framework/security
  - https://learn.microsoft.com/azure/security/
  - https://www.cisecurity.org/cis-benchmarks
---

## Purpose & When-To-Use

**Trigger conditions:**
- Cloud security audit before production deployment
- Compliance requirement (CIS Benchmarks, Well-Architected Framework)
- Post-incident cloud configuration review
- Cloud migration security validation
- Third-party cloud security questionnaire response

**Not for:**
- Application-level security (use appsec-validator)
- Container security (use container-security-checker)
- Real-time cloud security monitoring (use CSPM tools)
- Cost optimization (use cost-optimization-analyzer skill)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `cloud_platform` must be one of: [aws, azure, gcp]
- `resource_scope` must be one of: [storage, iam, network, compute, all]
- `compliance_check` must be one of: [cis, well-architected, both, none]

**Source freshness:**
- AWS Well-Architected Security Pillar (accessed 2025-10-26T01:33:55-04:00): https://aws.amazon.com/architecture/well-architected/
- Google Cloud Security Framework (accessed 2025-10-26T01:33:55-04:00): https://cloud.google.com/architecture/framework/security
- Azure Security Baseline (accessed 2025-10-26T01:33:55-04:00): https://learn.microsoft.com/azure/security/
- CIS Benchmarks (accessed 2025-10-26T01:33:55-04:00): https://www.cisecurity.org/cis-benchmarks

---

## Procedure

### Step 1: Critical Cloud Security Controls Check

**Storage Security (AWS S3, Azure Storage, GCS):**
1. Public bucket/container exposure check (immediate critical finding if public)
2. Encryption at rest validation (AES-256, customer-managed keys preferred)
3. Versioning enabled for critical buckets
4. Access logging enabled

**IAM Security:**
1. Overpermissive policies (wildcard `*` resource or action)
2. Root account usage (AWS) or high-privilege account activity
3. MFA enforcement on privileged accounts
4. Service account key rotation (90-day max age)

**Network Security:**
1. VPC/VNet segmentation (public vs private subnets)
2. Security group/NSG rules (default deny, minimal ingress)
3. Network flow logging enabled
4. Public IP exposure on sensitive resources

**Compute Security (if scope includes compute):**
1. Unencrypted volumes/disks
2. Overly permissive instance metadata access
3. Missing security patches
4. Publicly accessible management ports (SSH, RDP)

### Step 2: Generate Platform-Specific Remediation

For each finding, provide CLI commands or IaC snippets:
- **AWS:** AWS CLI, CloudFormation, or Terraform
- **Azure:** Azure CLI or ARM templates
- **GCP:** gcloud commands or Terraform

**Token budgets:**
- **T1:** ≤2k tokens (critical findings only)
- **T2:** ≤6k tokens (full scope with remediation)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If cloud account access is unavailable → request read-only credentials or architecture docs
- If resource tagging is incomplete → assess based on resource names/patterns

**Abort conditions:**
- No cloud platform specified → cannot proceed
- Zero resources found in scope → verify account access

**Severity classification:**
- Critical: Public data exposure, overpermissive root access (CVSS 9.0-10.0)
- High: Encryption missing, weak IAM policies (CVSS 7.0-8.9)
- Medium: Logging gaps, network misconfiguration (CVSS 4.0-6.9)
- Low: Best practice deviations (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "cloud_platform": "aws|azure|gcp",
  "resource_scope": "storage|iam|network|compute|all",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "resource_type": "s3-bucket|iam-role|security-group|...",
      "resource_id": "ARN or resource identifier",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "platform_control": "CIS control ID or Well-Architected pillar",
      "remediation": "specific fix steps",
      "remediation_command": "CLI command or IaC snippet"
    }
  ],
  "compliance_status": {
    "framework": "cis|well-architected",
    "controls_assessed": ["list"],
    "controls_passed": ["list"],
    "controls_failed": ["list"]
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

---

## Examples

**Example: AWS S3 Security Check**

```yaml
# Input
cloud_platform: "aws"
resource_scope: "storage"
compliance_check: "cis"

# Output (abbreviated)
{
  "cloud_platform": "aws",
  "findings": [
    {
      "id": "CLOUD-001",
      "resource_type": "s3-bucket",
      "resource_id": "arn:aws:s3:::public-data-bucket",
      "severity": "critical",
      "cvss_score": 9.1,
      "title": "S3 bucket publicly accessible",
      "remediation_command": "aws s3api put-public-access-block --bucket public-data-bucket --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    }
  ],
  "summary": {"critical_count": 1, "overall_risk": "critical"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical findings only)
- T2 ≤6k tokens (full scope with remediation commands)

**Safety:**
- No credentials in remediation commands
- No actual resource identifiers in examples

**Auditability:**
- Findings cite CIS Benchmark or Well-Architected controls
- CVSS scores follow CVSSv3.1 methodology

**Determinism:**
- Same cloud state + inputs = consistent findings

---

## Resources

**AWS Security:**
- AWS Well-Architected Security Pillar: https://aws.amazon.com/architecture/well-architected/ (accessed 2025-10-26T01:33:55-04:00)
- AWS Security Best Practices: https://aws.amazon.com/architecture/security-identity-compliance/ (accessed 2025-10-26T01:33:55-04:00)

**Azure Security:**
- Azure Security Baseline: https://learn.microsoft.com/azure/security/ (accessed 2025-10-26T01:33:55-04:00)
- Azure Security Best Practices: https://learn.microsoft.com/azure/security/fundamentals/best-practices-and-patterns (accessed 2025-10-26T01:33:55-04:00)

**GCP Security:**
- Google Cloud Security Framework: https://cloud.google.com/architecture/framework/security (accessed 2025-10-26T01:33:55-04:00)
- GCP Security Best Practices: https://cloud.google.com/security/best-practices (accessed 2025-10-26T01:33:55-04:00)

**Multi-Cloud:**
- CIS Benchmarks (AWS, Azure, GCP): https://www.cisecurity.org/cis-benchmarks (accessed 2025-10-26T01:33:55-04:00)
- Cloud Security Alliance (CSA) Cloud Controls Matrix: https://cloudsecurityalliance.org/research/cloud-controls-matrix (accessed 2025-10-26T01:33:55-04:00)
