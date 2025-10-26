---
name: "Network Security Architecture Validator"
slug: "networksec-architecture-validator"
description: "Validate network security architecture with firewall rule analysis, segmentation verification, and defense-in-depth assessment."
capabilities:
  - Firewall rule documentation and default-deny validation
  - Network segmentation review (DMZ, internal zones)
  - VPN and encrypted transit verification
  - Intrusion Prevention System (IPS) coverage
  - Micro-segmentation for east-west traffic
inputs:
  - network_identifier: "Network or environment identifier (string, required)"
  - architecture_scope: "perimeter | internal | vpn | all (string, default: all)"
  - segmentation_model: "dmz | zero-trust | hybrid (string, optional)"
outputs:
  - findings: "JSON array of network security findings with control references"
  - segmentation_analysis: "Network zone isolation assessment"
  - remediation_rules: "Firewall rule or network policy configurations"
keywords:
  - network-security
  - firewall
  - segmentation
  - dmz
  - vpn
  - ips
  - micro-segmentation
  - defense-in-depth
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
  - https://www.cisecurity.org/controls
---

## Purpose & When-To-Use

**Trigger conditions:**
- Network security architecture review before production deployment
- Network segmentation validation
- Firewall rule audit
- VPN security assessment
- Post-incident network security review

**Not for:**
- Real-time intrusion detection (use IDS/IPS tools)
- Network performance optimization (use network monitoring tools)
- Cloud network security (use cloudsec-posture-analyzer)
- Application-level security (use appsec-validator)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `network_identifier` must be non-empty string
- `architecture_scope` must be one of: [perimeter, internal, vpn, all]
- `segmentation_model` must be one of: [dmz, zero-trust, hybrid] or omitted

**Source freshness:**
- NIST SP 800-53 Rev 5 (SC family - System and Communications Protection) (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- CIS Controls v8 (Network Security) (accessed 2025-10-26T01:33:55-04:00): https://www.cisecurity.org/controls

---

## Procedure

### Step 1: Critical Network Security Controls Check

**Perimeter Security:**
1. Firewall rules documented and reviewed (NIST SP 800-53 SC-7, accessed 2025-10-26T01:33:55-04:00)
2. Default-deny firewall stance (explicit allow-list only)
3. No overly permissive rules (0.0.0.0/0 ingress on sensitive ports)
4. DMZ zone for internet-facing services

**Internal Segmentation:**
1. Network zones defined (production, staging, management, user)
2. Inter-zone traffic restrictions (east-west segmentation)
3. Micro-segmentation for critical assets
4. Broadcast domain isolation

**Encrypted Transit:**
1. VPN for remote access (IPsec or WireGuard)
2. TLS/SSL for sensitive data in transit
3. No cleartext protocols on sensitive networks (FTP, Telnet, HTTP)

**Monitoring and Detection:**
1. Network flow logging enabled
2. Intrusion Prevention System (IPS) deployed
3. DDoS protection mechanisms

### Step 2: Generate Remediation Rules

For each finding, provide:
- NIST SP 800-53 control reference (SC family)
- Firewall rule syntax (iptables, pf, cloud security groups)
- Network policy configuration (Kubernetes NetworkPolicy, Cisco ACL)

**Token budgets:**
- **T1:** ≤2k tokens (critical network security findings)
- **T2:** ≤6k tokens (full network architecture audit)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If network diagram unavailable → request architecture documentation
- If firewall rules inaccessible → assess based on observed traffic patterns

**Abort conditions:**
- No network identifier specified → cannot proceed
- No firewall rules or network policies accessible → limited to high-level assessment

**Severity classification:**
- Critical: Default-allow firewall, no segmentation (CVSS 9.0-10.0)
- High: Overpermissive rules, missing VPN encryption (CVSS 7.0-8.9)
- Medium: Logging gaps, weak segmentation (CVSS 4.0-6.9)
- Low: Documentation gaps, rule optimization (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "network_identifier": "string",
  "architecture_scope": "perimeter|internal|vpn|all",
  "segmentation_model": "dmz|zero-trust|hybrid or null",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "category": "firewall|segmentation|vpn|monitoring",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "nist_control": "SC-7 or similar",
      "affected_zones": ["network zones or segments"],
      "remediation": "specific fix steps",
      "remediation_rule": "firewall rule or policy config"
    }
  ],
  "segmentation_analysis": {
    "zones_defined": ["list of network zones"],
    "isolation_score": "0-100 (100=perfect isolation)",
    "gaps": ["list of segmentation gaps"]
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

**Example: Firewall Rule Audit**

```yaml
# Input
network_identifier: "production-network"
architecture_scope: "perimeter"
segmentation_model: "dmz"

# Output (abbreviated)
{
  "network_identifier": "production-network",
  "findings": [
    {
      "id": "NET-001",
      "category": "firewall",
      "severity": "high",
      "cvss_score": 7.5,
      "title": "Overly permissive SSH ingress rule",
      "nist_control": "SC-7(5)",
      "remediation_rule": "iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT"
    }
  ],
  "summary": {"high_count": 1, "overall_risk": "high"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical network security findings)
- T2 ≤6k tokens (full network architecture audit)

**Safety:**
- No actual IP addresses in public examples
- No sensitive network topology details

**Auditability:**
- Findings cite NIST SP 800-53 SC controls
- Firewall rules follow security best practices

**Determinism:**
- Same network state + inputs = consistent findings

---

## Resources

**NIST Standards:**
- NIST SP 800-53 Rev 5 (SC family): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (accessed 2025-10-26T01:33:55-04:00)

**CIS Controls:**
- CIS Controls v8 (Network Security): https://www.cisecurity.org/controls (accessed 2025-10-26T01:33:55-04:00)

**Network Security Best Practices:**
- NIST SP 800-41 Rev 1 (Firewall and Network Security): https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final (accessed 2025-10-26T01:33:55-04:00)
- NIST SP 800-77 (VPN Security): https://csrc.nist.gov/publications/detail/sp/800-77/final (accessed 2025-10-26T01:33:55-04:00)
