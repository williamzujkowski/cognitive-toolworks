---
name: "Zero Trust Maturity Assessor"
slug: "zerotrust-maturity-assessor"
description: "Evaluate zero-trust architecture maturity using CISA ZTMM with identity verification, device trust, micro-segmentation, and continuous monitoring."
capabilities:
  - CISA Zero Trust Maturity Model (ZTMM) assessment
  - Identity pillar evaluation (centralized identity, MFA)
  - Device pillar assessment (device inventory, compliance checking)
  - Network pillar review (micro-segmentation, encrypted traffic)
  - Maturity level determination (Traditional, Initial, Advanced, Optimal)
inputs:
  - organization_identifier: "Organization or environment identifier (string, required)"
  - ztmm_pillars: "identity | device | network | application | data | all (array, default: all)"
  - target_maturity: "initial | advanced | optimal (string, optional)"
outputs:
  - maturity_assessment: "Per-pillar maturity level and gap analysis"
  - roadmap: "Maturity progression roadmap with prioritized initiatives"
  - cisa_ztmm_alignment: "CISA ZTMM pillar compliance status"
keywords:
  - zero-trust
  - zero-trust-architecture
  - zta
  - ztmm
  - cisa
  - never-trust-always-verify
  - micro-segmentation
  - continuous-verification
  - identity-centric
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://www.cisa.gov/zero-trust-maturity-model
  - https://csrc.nist.gov/publications/detail/sp/800-207/final
---

## Purpose & When-To-Use

**Trigger conditions:**
- Zero-trust architecture maturity assessment
- CISA ZTMM compliance requirement
- Zero-trust migration planning
- Security architecture modernization initiative
- Third-party zero-trust readiness questionnaire

**Not for:**
- Zero-trust implementation (provides assessment only)
- Real-time access policy enforcement (use zero-trust products)
- Traditional perimeter security assessment (use networksec-architecture-validator)
- Application security (use appsec-validator)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:55-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `organization_identifier` must be non-empty string
- `ztmm_pillars` must be subset of: [identity, device, network, application, data]
- `target_maturity` must be one of: [initial, advanced, optimal] or omitted

**Source freshness:**
- CISA Zero Trust Maturity Model (accessed 2025-10-26T01:33:55-04:00): https://www.cisa.gov/zero-trust-maturity-model
- NIST SP 800-207 Zero Trust Architecture (accessed 2025-10-26T01:33:55-04:00): https://csrc.nist.gov/publications/detail/sp/800-207/final

---

## Procedure

### Step 1: CISA ZTMM Pillar Assessment

**Identity Pillar (CISA ZTMM 2.0, accessed 2025-10-26T01:33:55-04:00):**
- **Traditional:** Basic directory service, passwords
- **Initial:** Centralized identity management, some MFA
- **Advanced:** Enterprise-wide SSO, MFA everywhere, risk-based auth
- **Optimal:** Continuous authentication, behavior analytics, FIDO2

**Device Pillar:**
- **Traditional:** Manual device tracking
- **Initial:** Device inventory exists, basic compliance
- **Advanced:** Automated compliance checking, device health attestation
- **Optimal:** Real-time device risk scoring, zero-touch provisioning

**Network Pillar:**
- **Traditional:** Perimeter-based security, VLANs
- **Initial:** Some micro-segmentation, encrypted traffic
- **Advanced:** Comprehensive micro-segmentation, application-layer routing
- **Optimal:** Dynamic micro-perimeters, software-defined perimeter (SDP)

**Application Pillar:**
- **Traditional:** Network-based access control
- **Initial:** Application-aware proxies, some authorization
- **Advanced:** Fine-grained authorization, API gateways
- **Optimal:** Continuous authorization, context-aware access

**Data Pillar:**
- **Traditional:** File-system permissions
- **Initial:** Data classification, basic encryption
- **Advanced:** Data-centric security, DLP, rights management
- **Optimal:** Data-level access control, automated data tagging

### Step 2: Maturity Gaps and Roadmap

For each pillar:
1. Identify current maturity level
2. Calculate gap to target maturity (if specified)
3. Prioritize initiatives by impact and effort
4. Generate phased roadmap (90-day, 180-day, 1-year milestones)

**Token budgets:**
- **T1:** ≤2k tokens (current maturity assessment only)
- **T2:** ≤6k tokens (full maturity assessment with roadmap and initiatives)
- **T3:** Not applicable for this skill (use security-auditor agent for comprehensive assessments)

---

## Decision Rules

**Ambiguity thresholds:**
- If pillar data incomplete → assess based on available information and flag gaps
- If technology stack unclear → request architecture documentation

**Abort conditions:**
- No organization identifier → cannot proceed
- Zero pillars selected → default to all 5 pillars

**Maturity scoring:**
- Assign lowest maturity level if any critical gap exists
- Partial compliance = lower maturity level (no partial credit)

---

## Output Contract

**Required fields:**
```json
{
  "organization_identifier": "string",
  "ztmm_pillars": ["identity", "device", "network", "application", "data"],
  "target_maturity": "initial|advanced|optimal or null",
  "timestamp": "ISO-8601 with timezone",
  "maturity_assessment": {
    "identity": {
      "current_level": "traditional|initial|advanced|optimal",
      "target_level": "initial|advanced|optimal or null",
      "gaps": ["list of capability gaps"],
      "initiatives": ["prioritized initiatives to progress"]
    },
    "device": { "..." },
    "network": { "..." },
    "application": { "..." },
    "data": { "..." }
  },
  "overall_maturity": "traditional|initial|advanced|optimal",
  "roadmap": {
    "90_day_milestones": ["list of quick wins"],
    "180_day_milestones": ["list of medium-term initiatives"],
    "1_year_milestones": ["list of strategic initiatives"]
  },
  "cisa_ztmm_alignment": {
    "version": "CISA ZTMM 2.0",
    "compliant_pillars": ["list"],
    "non_compliant_pillars": ["list"]
  }
}
```

---

## Examples

**Example: Identity Pillar Assessment**

```yaml
# Input
organization_identifier: "enterprise-corp"
ztmm_pillars: ["identity"]
target_maturity: "advanced"

# Output (abbreviated)
{
  "organization_identifier": "enterprise-corp",
  "maturity_assessment": {
    "identity": {
      "current_level": "initial",
      "target_level": "advanced",
      "gaps": [
        "MFA not enforced organization-wide",
        "No risk-based authentication"
      ],
      "initiatives": [
        "Deploy enterprise-wide SSO",
        "Enable MFA on all accounts",
        "Implement risk-based authentication"
      ]
    }
  },
  "overall_maturity": "initial",
  "roadmap": {
    "90_day_milestones": ["Enable MFA for privileged accounts"],
    "180_day_milestones": ["Deploy SSO across applications"]
  }
}
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (current maturity assessment only)
- T2 ≤6k tokens (full maturity assessment with roadmap)

**Safety:**
- No organizational details in public examples
- No technology vendor lock-in in recommendations

**Auditability:**
- Assessments cite CISA ZTMM and NIST SP 800-207
- Maturity levels align with CISA definitions

**Determinism:**
- Same capabilities + inputs = consistent maturity level

---

## Resources

**Zero Trust Standards:**
- CISA Zero Trust Maturity Model v2.0: https://www.cisa.gov/zero-trust-maturity-model (accessed 2025-10-26T01:33:55-04:00)
- NIST SP 800-207 (Zero Trust Architecture): https://csrc.nist.gov/publications/detail/sp/800-207/final (accessed 2025-10-26T01:33:55-04:00)

**Zero Trust Implementation:**
- Google BeyondCorp: https://cloud.google.com/beyondcorp (accessed 2025-10-26T01:33:55-04:00)
- Microsoft Zero Trust: https://www.microsoft.com/en-us/security/business/zero-trust (accessed 2025-10-26T01:33:55-04:00)

**Policy and Guidance:**
- OMB M-22-09 (Federal Zero Trust Strategy): https://www.whitehouse.gov/omb/briefing-room/2022/01/26/m-22-09-federal-zero-trust-strategy/ (accessed 2025-10-26T01:33:55-04:00)
