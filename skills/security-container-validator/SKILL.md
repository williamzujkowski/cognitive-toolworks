---
name: "Container Security Checker"
slug: "security-container-validator"
description: "Validate container and Kubernetes security using CIS benchmarks with pod security standards, RBAC review, and image vulnerability checks."
capabilities:
  - CIS Docker and Kubernetes benchmark validation
  - Pod Security Standards enforcement (Baseline, Restricted)
  - Kubernetes RBAC configuration review
  - Container image security verification (trusted registries, non-root users)
  - Network policies and admission controller checks
inputs:
  - platform: "docker | kubernetes | both (string, required)"
  - cluster_identifier: "Kubernetes cluster name (string, optional for docker-only)"
  - check_scope: "images | runtime | rbac | network | all (string, default: all)"
outputs:
  - findings: "JSON array of container security findings with CIS control references"
  - cis_compliance: "CIS Benchmark compliance status"
  - remediation_manifests: "Kubernetes YAML or Dockerfile snippets for fixes"
keywords:
  - container-security
  - kubernetes-security
  - docker-security
  - cis-benchmark
  - pod-security
  - rbac
  - network-policies
  - admission-controller
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://www.cisecurity.org/benchmark/docker
  - https://www.cisecurity.org/benchmark/kubernetes
  - https://kubernetes.io/docs/concepts/security/pod-security-standards/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Container security audit before production deployment
- Kubernetes cluster security review
- CIS Benchmark compliance requirement
- Post-incident container security assessment
- Third-party container security questionnaire

**Not for:**
- Image vulnerability scanning (use dedicated SBOM/CVE scanning tools)
- Runtime threat detection (use container runtime security tools)
- Application security (use security-appsec-validator)
- Cloud infrastructure security (use security-cloud-analyzer)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `platform` must be one of: [docker, kubernetes, both]
- `check_scope` must be one of: [images, runtime, rbac, network, all]
- If `platform` includes kubernetes, `cluster_identifier` should be provided

**Source freshness:**
- CIS Docker Benchmark (accessed 2025-10-26T01:33:55-04:00): https://www.cisecurity.org/benchmark/docker
- CIS Kubernetes Benchmark v1.8+ (accessed 2025-10-26T01:33:55-04:00): https://www.cisecurity.org/benchmark/kubernetes
- Pod Security Standards (accessed 2025-10-26T01:33:55-04:00): https://kubernetes.io/docs/concepts/security/pod-security-standards/

---

## Procedure

### Step 1: Critical Container Security Controls

**Docker/Container Images:**
1. Container images from trusted registries (verified signatures)
2. Non-root user execution (USER directive in Dockerfile)
3. No secrets in environment variables or image layers
4. Resource limits defined (memory, CPU)

**Kubernetes Pod Security:**
1. Pod Security Standards enforcement (Baseline or Restricted level)
2. Non-privileged containers (securityContext.privileged: false)
3. Read-only root filesystem where possible
4. No host namespace sharing (hostNetwork, hostPID, hostIPC: false)

**Kubernetes RBAC:**
1. Role bindings follow least privilege principle
2. No wildcard permissions in Roles/ClusterRoles
3. Service accounts scoped to namespaces
4. Minimal ClusterRole bindings

**Kubernetes Network Security:**
1. Network policies defined for namespace isolation
2. Ingress and egress rules explicit (no default allow-all)
3. Service mesh security (if applicable)

### Step 2: Generate CIS-Aligned Remediation

For each finding, provide:
- CIS Benchmark control reference
- Kubernetes YAML manifest fixes or Dockerfile changes
- Platform-specific commands (kubectl, docker)

**Token budgets:**
- **T1:** ≤2k tokens (critical findings)
- **T2:** ≤6k tokens (full CIS coverage)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If cluster access unavailable → request kubeconfig or architecture docs
- If Dockerfile unavailable → assess runtime configuration only

**Abort conditions:**
- No platform specified → cannot proceed
- Kubernetes platform selected but no cluster access → limited to manifest review

**Severity classification:**
- Critical: Privileged containers, host namespace sharing (CVSS 9.0-10.0)
- High: Weak RBAC, missing network policies (CVSS 7.0-8.9)
- Medium: Resource limits missing, root user (CVSS 4.0-6.9)
- Low: Best practice deviations (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "platform": "docker|kubernetes|both",
  "cluster_identifier": "string or null",
  "check_scope": "images|runtime|rbac|network|all",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "check_type": "image|pod|rbac|network",
      "resource_type": "pod|deployment|role|networkpolicy|...",
      "resource_name": "resource identifier",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "cis_control": "CIS Docker 4.1 or CIS Kubernetes 5.2.3",
      "remediation": "specific fix steps",
      "remediation_manifest": "YAML or Dockerfile snippet"
    }
  ],
  "cis_compliance": {
    "benchmark": "CIS Docker v1.6.0 or CIS Kubernetes v1.8.0",
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

**Example: Kubernetes Pod Security Check**

```yaml
# Input
platform: "kubernetes"
cluster_identifier: "prod-cluster-us-east"
check_scope: "runtime"

# Output (abbreviated)
{
  "platform": "kubernetes",
  "findings": [
    {
      "id": "CONTAINER-001",
      "check_type": "pod",
      "resource_name": "web-app-deployment",
      "severity": "high",
      "cvss_score": 7.5,
      "title": "Privileged container detected",
      "cis_control": "CIS Kubernetes 5.2.1",
      "remediation_manifest": "securityContext:\\n  privileged: false"
    }
  ],
  "summary": {"high_count": 1, "overall_risk": "high"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical findings only)
- T2 ≤6k tokens (full CIS Benchmark coverage)

**Safety:**
- No secrets in remediation manifests
- No actual cluster credentials

**Auditability:**
- Findings cite CIS Benchmark controls
- CVSS scores follow CVSSv3.1 methodology

**Determinism:**
- Same cluster state + inputs = consistent findings

---

## Resources

**CIS Benchmarks:**
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker (accessed 2025-10-26T01:33:55-04:00)
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes (accessed 2025-10-26T01:33:55-04:00)

**Kubernetes Security:**
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/ (accessed 2025-10-26T01:33:55-04:00)
- Kubernetes Security Best Practices: https://kubernetes.io/docs/concepts/security/ (accessed 2025-10-26T01:33:55-04:00)
- RBAC Documentation: https://kubernetes.io/docs/reference/access-authn-authz/rbac/ (accessed 2025-10-26T01:33:55-04:00)

**Container Security:**
- Docker Security Best Practices: https://docs.docker.com/engine/security/ (accessed 2025-10-26T01:33:55-04:00)
- Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/ (accessed 2025-10-26T01:33:55-04:00)
