---
name: "Operating System Security Hardening Checker"
slug: "ossec-hardening-checker"
description: "Verify operating system hardening using CIS benchmarks with patch management, kernel hardening, and host-based firewall validation."
capabilities:
  - CIS benchmark compliance (Linux, Windows Server)
  - OS patch currency validation (within 30-day threshold)
  - Kernel hardening verification (SELinux, AppArmor)
  - Host-based firewall configuration review
  - File integrity monitoring assessment
inputs:
  - os_platform: "linux | windows | both (string, required)"
  - os_distribution: "ubuntu | rhel | centos | debian | windows-server (string, optional)"
  - cis_level: "1 | 2 (string, default: 1)"
outputs:
  - findings: "JSON array of OS hardening findings with CIS benchmark references"
  - cis_compliance_score: "CIS benchmark compliance percentage"
  - remediation_commands: "OS-specific shell commands for hardening"
keywords:
  - os-security
  - cis-benchmark
  - hardening
  - patching
  - selinux
  - apparmor
  - host-firewall
  - file-integrity
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://www.cisecurity.org/cis-benchmarks
  - https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
---

## Purpose & When-To-Use

**Trigger conditions:**
- Operating system hardening validation before production deployment
- CIS benchmark compliance requirement
- OS patch management audit
- Post-incident OS security review
- Host security configuration assessment

**Not for:**
- Real-time OS threat detection (use EDR/host IDS tools)
- OS performance optimization (use performance monitoring tools)
- Cloud infrastructure security (use cloudsec-posture-analyzer)
- Container security (use container-security-checker)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `os_platform` must be one of: [linux, windows, both]
- `os_distribution` must be one of: [ubuntu, rhel, centos, debian, windows-server] or omitted
- `cis_level` must be one of: [1, 2] (Level 1=basic, Level 2=comprehensive)

**Source freshness:**
- CIS Benchmarks (Linux, Windows) (accessed 2025-10-26T01:33:55-04:00): https://www.cisecurity.org/cis-benchmarks
- NIST SP 800-53 Rev 5 (CM, SI families) (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

---

## Procedure

### Step 1: Critical OS Hardening Controls Check

**Patch Management:**
1. OS patches current (within 30 days of release)
2. Security patches prioritized over feature updates
3. Patch management process documented
4. Critical vulnerabilities patched within 7 days

**Kernel Hardening (Linux):**
1. SELinux or AppArmor enabled and enforcing
2. Kernel modules restricted (no unnecessary modules loaded)
3. Core dumps disabled for security
4. Address Space Layout Randomization (ASLR) enabled

**Host-Based Firewall:**
1. Firewall active (iptables, nftables, Windows Firewall)
2. Default-deny policy
3. Only necessary ports open
4. Firewall rules documented

**Services and Processes:**
1. Unnecessary services disabled (per CIS Benchmark, accessed 2025-10-26T01:33:55-04:00)
2. No legacy protocols enabled (Telnet, FTP, rsh)
3. Secure SSH configuration (no root login, key-based auth)

**File Integrity Monitoring:**
1. File integrity monitoring tool installed (AIDE, Tripwire, Samhain)
2. Critical system files monitored
3. Regular integrity checks scheduled

### Step 2: CIS Benchmark Compliance Scoring

For each CIS control assessed:
- Calculate compliance score: (passed controls / total controls) * 100
- Prioritize Level 1 controls (basic hardening)
- Include Level 2 controls if `cis_level=2` (defense-in-depth)

**Token budgets:**
- **T1:** ≤2k tokens (critical OS hardening controls)
- **T2:** ≤6k tokens (full CIS benchmark audit)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If OS distribution unknown → use generic Linux or Windows CIS baseline
- If patch date unavailable → flag as unknown risk

**Abort conditions:**
- No OS platform specified → cannot proceed
- No OS access or configuration files → limited to documentation review

**Severity classification:**
- Critical: Unpatched critical CVEs, SELinux/AppArmor disabled (CVSS 9.0-10.0)
- High: Patches >30 days old, firewall disabled (CVSS 7.0-8.9)
- Medium: Unnecessary services, weak SSH config (CVSS 4.0-6.9)
- Low: Documentation gaps, CIS Level 2 deviations (CVSS 0.1-3.9)

---

## Output Contract

**Required fields:**
```json
{
  "os_platform": "linux|windows|both",
  "os_distribution": "ubuntu|rhel|centos|debian|windows-server or null",
  "cis_level": "1|2",
  "timestamp": "ISO-8601 with timezone",
  "findings": [
    {
      "id": "unique identifier",
      "category": "patching|kernel|firewall|services|fim",
      "severity": "critical|high|medium|low",
      "cvss_score": 0.0,
      "title": "brief description",
      "description": "detailed finding",
      "cis_control": "CIS Benchmark control ID",
      "nist_control": "SP 800-53 control (e.g., CM-7, SI-2)",
      "remediation": "specific fix steps",
      "remediation_command": "shell command or script"
    }
  ],
  "cis_compliance_score": 0.0,
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

**Example: Linux Hardening Check**

```yaml
# Input
os_platform: "linux"
os_distribution: "ubuntu"
cis_level: "1"

# Output (abbreviated)
{
  "os_platform": "linux",
  "os_distribution": "ubuntu",
  "findings": [
    {
      "id": "OS-001",
      "category": "kernel",
      "severity": "high",
      "cvss_score": 7.8,
      "title": "AppArmor not enabled",
      "cis_control": "CIS Ubuntu 1.6.1",
      "remediation_command": "systemctl enable apparmor && systemctl start apparmor"
    }
  ],
  "cis_compliance_score": 72.5,
  "summary": {"high_count": 1, "overall_risk": "high"}
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (critical OS hardening controls)
- T2 ≤6k tokens (full CIS benchmark audit)

**Safety:**
- No system credentials in remediation commands
- No actual hostnames in examples

**Auditability:**
- Findings cite CIS Benchmark and NIST SP 800-53 controls
- Patch recommendations align with vendor advisories

**Determinism:**
- Same OS state + inputs = consistent findings

---

## Resources

**CIS Benchmarks:**
- CIS Benchmarks (all OS): https://www.cisecurity.org/cis-benchmarks (accessed 2025-10-26T01:33:55-04:00)
- CIS Ubuntu Benchmark: https://www.cisecurity.org/benchmark/ubuntu_linux (accessed 2025-10-26T01:33:55-04:00)
- CIS RHEL Benchmark: https://www.cisecurity.org/benchmark/red_hat_linux (accessed 2025-10-26T01:33:55-04:00)
- CIS Windows Server Benchmark: https://www.cisecurity.org/benchmark/microsoft_windows_server (accessed 2025-10-26T01:33:55-04:00)

**NIST Standards:**
- NIST SP 800-53 Rev 5 (CM, SI families): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final (accessed 2025-10-26T01:33:55-04:00)

**Hardening Guides:**
- SELinux Documentation: https://www.redhat.com/en/topics/linux/what-is-selinux (accessed 2025-10-26T01:33:55-04:00)
- AppArmor Documentation: https://ubuntu.com/server/docs/security-apparmor (accessed 2025-10-26T01:33:55-04:00)
