---
name: "Zero Trust Architecture Designer"
slug: "zero-trust-architecture-designer"
description: "Design zero-trust architectures with identity-centric security, micro-segmentation, continuous verification, and CISA ZTMM maturity assessment."
capabilities:
  - Zero-trust architecture design following NIST SP 800-207
  - CISA Zero Trust Maturity Model (ZTMM) assessment across 5 pillars
  - Identity-centric security and access control design
  - Network micro-segmentation architecture
  - Continuous verification and dynamic policy enforcement
  - Zero-trust deployment model selection (EIG, Microsegmentation, SDP)
  - Never Trust, Always Verify principle implementation
  - Least privilege access control design
  - Zero-trust roadmap and migration planning
  - BeyondCorp-style implementation guidance
inputs:
  - target_environment: "environment identifier (on-prem, cloud, hybrid) (string)"
  - current_architecture: "existing architecture description or diagram reference (string)"
  - assessment_tier: "T1 (maturity check) | T2 (architecture design) | T3 (comprehensive roadmap) (string, default: T1)"
  - ztmm_pillars: "array of pillars to assess [identity, devices, networks, applications, data] (array, default: all)"
  - compliance_requirements: "regulatory/compliance drivers (array, optional)"
  - business_objectives: "business goals driving zero-trust adoption (string, optional)"
outputs:
  - maturity_assessment: "CISA ZTMM maturity across pillars (Traditional|Initial|Advanced|Optimal)"
  - architecture_design: "Zero-trust architecture diagram and component specifications"
  - deployment_model: "Recommended deployment approach (EIG|Microsegmentation|SDP|Hybrid)"
  - implementation_roadmap: "Phased migration plan with priorities and timelines"
  - policy_recommendations: "Dynamic access policies and continuous verification rules"
  - gap_analysis: "Current vs. target state with remediation priorities"
keywords:
  - zero-trust
  - zero-trust-architecture
  - zta
  - ztmm
  - cisa-maturity-model
  - nist-800-207
  - beyondcorp
  - never-trust-always-verify
  - identity-centric-security
  - micro-segmentation
  - continuous-verification
  - least-privilege
  - policy-engine
  - policy-decision-point
  - policy-enforcement-point
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://csrc.nist.gov/publications/detail/sp/800-207/final
  - https://www.cisa.gov/zero-trust-maturity-model
  - https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf
  - https://cloud.google.com/beyondcorp
  - https://csrc.nist.gov/pubs/sp/800/207/a/final
  - https://www.microsoft.com/en-us/security/business/zero-trust
  - https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf
---

## Purpose & When-To-Use

**Trigger conditions:**
- Zero-trust adoption roadmap needed for enterprise security transformation
- NIST SP 800-207 implementation required for federal/defense systems
- CISA Zero Trust Maturity Model assessment mandated by OMB M-22-09
- Perimeter security to zero-trust migration project
- Continuous verification design for identity-centric access control
- Remote workforce security requiring location-agnostic controls
- Cloud migration requiring zero-trust networking
- Breach containment strategy requiring micro-segmentation
- Compliance with EO 14028 (federal cybersecurity modernization)

**Not for:**
- Traditional perimeter security design (antithetical to zero-trust)
- Quick security fixes (zero-trust requires architectural transformation)
- Tactical firewall rules (use network security tools instead)
- Identity provider selection only (broader architectural scope)
- Real-time threat detection (use SIEM/XDR tools instead)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `target_environment` must be: on-prem, cloud, hybrid, or multi-cloud
- `current_architecture` must reference existing architecture documentation or provide description
- `assessment_tier` must be: T1, T2, or T3
- `ztmm_pillars` must be subset of: [identity, devices, networks, applications, data]
- `compliance_requirements` must be valid framework identifiers (if provided)
- `business_objectives` should articulate clear drivers (if provided)

**Source freshness:**
- NIST SP 800-207 (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/publications/detail/sp/800-207/final - August 2020 final version
- CISA ZTMM v2.0 (accessed 2025-10-25T21:30:36-04:00): https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf - April 2023
- NIST SP 800-207A Cloud-Native ZTA (accessed 2025-10-25T21:30:36-04:00): https://csrc.nist.gov/pubs/sp/800/207/a/final - June 2023
- Google BeyondCorp (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/beyondcorp - current version
- OMB M-22-09 (accessed 2025-10-25T21:30:36-04:00): https://www.whitehouse.gov/wp-content/uploads/2022/01/M-22-09.pdf - January 2022

**Dependency check:**
- `security-assessment-framework` skill available (required for T2+)
- `cloud-native-deployment-orchestrator` skill available (required for cloud environments)
- Architecture documentation accessible or current state can be assessed

---

## Procedure

### T1: Zero-Trust Maturity Quick Check (≤2k tokens)

**Fast path for initial maturity assessment (80% use case):**

1. **Apply CISA ZTMM Five Pillars Assessment:**
   - **Identity**: Evaluate identity governance, MFA adoption, centralized identity management
     - Traditional: Username/password, static credentials
     - Initial: MFA deployed, centralized IdP
     - Advanced: Phishing-resistant MFA, FIDO2/WebAuthn, risk-based authentication
     - Optimal: Continuous authentication, passwordless, biometrics integrated

   - **Devices**: Assess device inventory, compliance, EDR/MDM coverage
     - Traditional: No device inventory or compliance checks
     - Initial: Basic device inventory, antivirus deployed
     - Advanced: EDR/XDR deployed, automated compliance enforcement
     - Optimal: Real-time device posture assessment, automated remediation

   - **Networks**: Evaluate network segmentation, encryption, micro-segmentation
     - Traditional: Flat network, perimeter firewall only
     - Initial: VLANs, basic segmentation
     - Advanced: Micro-segmentation, encrypted traffic (mTLS)
     - Optimal: Software-defined perimeter (SDP), application-layer segmentation

   - **Applications**: Review app authentication, API security, workload isolation
     - Traditional: Shared credentials, no app-level authN/authZ
     - Initial: App-level authentication, basic API keys
     - Advanced: OAuth2/OIDC, service mesh with mTLS
     - Optimal: Dynamic policy enforcement, runtime app security (RASP)

   - **Data**: Check data classification, encryption, DLP, access controls
     - Traditional: No data classification or encryption at rest
     - Initial: Data classification scheme, encryption at rest
     - Advanced: Encryption in transit and at rest, field-level encryption, DLP
     - Optimal: Continuous data monitoring, dynamic data protection, encrypted compute

2. **Score Maturity Level per Pillar:**
   - Output: JSON structure with pillar → maturity mapping
   - Identify gaps between current (Traditional/Initial) and target (Advanced/Optimal)

3. **Quick Recommendations:**
   - Prioritize pillars at "Traditional" level (highest risk)
   - Suggest 3-5 immediate actions per pillar
   - Estimate effort: Low (< 3 months) | Medium (3-6 months) | High (6-12 months)

**Output (T1):**
```json
{
  "maturity_assessment": {
    "identity": "Initial",
    "devices": "Traditional",
    "networks": "Initial",
    "applications": "Traditional",
    "data": "Traditional"
  },
  "overall_maturity": "Traditional",
  "critical_gaps": ["devices", "applications", "data"],
  "quick_wins": [
    "Deploy MFA across all users (identity)",
    "Implement device inventory and EDR (devices)",
    "Enable mTLS for service-to-service communication (networks)"
  ]
}
```

**Token budget check:** T1 ≤ 2k tokens

---

### T2: Zero-Trust Architecture Design (≤6k tokens)

**Extended design with deployment model selection:**

**Prerequisites:** T1 maturity assessment completed OR existing architecture documented.

1. **Apply NIST SP 800-207 Core Principles:**
   - **Never Trust, Always Verify:** No implicit trust based on network location
   - **Least Privilege Access:** Grant minimum necessary permissions per session
   - **Assume Breach:** Design controls assuming attackers are already inside
   - **Verify Explicitly:** Authenticate and authorize every access request
   - **Inspect and Log:** Comprehensive logging and traffic inspection

2. **Select Deployment Model (NIST SP 800-207 Reference Architectures):**

   **A) Enhanced Identity Governance (EIG):**
   - **Use when:** Strong IdP exists, cloud-first architecture, web-based apps
   - **Components:**
     - Policy Engine (PE): Evaluates access requests against policies
     - Policy Administrator (PA): Establishes/closes sessions based on PE decisions
     - Policy Enforcement Point (PEP): Sits in front of resources, enforces PA decisions
     - Identity Provider (IdP): SSO, MFA, SAML/OIDC integration
   - **Pros:** Leverages existing IdP, agentless for apps, fast deployment
   - **Cons:** Requires modern apps with OIDC/SAML, less effective for legacy systems

   **B) Micro-Segmentation Architecture:**
   - **Use when:** East-west traffic control critical, datacenter-heavy, container/K8s environments
   - **Components:**
     - Network segmentation (VLANs, VPCs, subnets)
     - Host-based agents or SDN for granular zone isolation
     - Next-gen firewalls with identity-aware rules
     - Service mesh (Istio, Linkerd) for container workloads
   - **Pros:** Strong network isolation, works with legacy apps, defense-in-depth
   - **Cons:** Complex to manage, requires agents or SDN, potential performance overhead

   **C) Software-Defined Perimeter (SDP):**
   - **Use when:** Remote workforce, BYOD, zero standing access required
   - **Components:**
     - SDP controller: Authenticates users/devices, provisions access
     - SDP gateways: Overlay network hiding resources until authenticated
     - Client software: Agent on user devices
   - **Pros:** Resources invisible until authenticated, strong remote access control
   - **Cons:** Requires client software, overlay network complexity, vendor lock-in risk

   **D) Hybrid Model (Recommended for most enterprises):**
   - Combine EIG for cloud apps, Micro-segmentation for datacenter, SDP for remote access
   - Example: Use Okta/Azure AD (EIG) + Istio service mesh (Micro-seg) + Zscaler Private Access (SDP)

3. **Design Policy Engine and Policy Decision Point (PDP):**
   - **Policy Engine Inputs:**
     - Subject identity (user, service account, device)
     - Resource attributes (sensitivity, location, data classification)
     - Contextual signals (time, location, device posture, risk score)
     - Threat intelligence (recent breaches, anomalous behavior)

   - **Policy Decision Logic:**
     - Evaluate against attribute-based access control (ABAC) policies
     - Calculate risk score: (identity_trust + device_trust + context_trust) / 3
     - Apply continuous verification: Re-evaluate every session, not just at login
     - Enforce least privilege: Grant narrowest scope for shortest duration

   - **Example Policy (pseudo-code):**
     ```
     IF user.mfa_verified AND device.compliant AND risk_score < 30 AND data.classification != "top-secret"
       THEN GRANT access WITH session_timeout=4h AND log_level=INFO
     ELSE IF risk_score >= 30 AND risk_score < 70
       THEN REQUIRE step_up_auth AND GRANT access WITH session_timeout=1h
     ELSE
       DENY access AND ALERT soc@company.com
     ```

4. **Design Continuous Verification Mechanisms:**
   - **Session-based re-authentication:** Re-verify every N minutes (e.g., 15min for high-value resources)
   - **Behavioral analytics:** Detect anomalies (impossible travel, unusual data access)
   - **Device posture monitoring:** Continuously check OS patches, EDR status, disk encryption
   - **Step-up authentication:** Require additional MFA for sensitive actions (e.g., delete database)

5. **Invoke Dependency Skills (if available):**
   - Call `security-assessment-framework` with `security_domains=["iam", "networksec", "zerotrust"]` for baseline security posture
   - Call `cloud-native-deployment-orchestrator` for K8s/service mesh architecture (if cloud target)

**Output (T2):**
```json
{
  "deployment_model": "Hybrid",
  "components": {
    "policy_engine": "Azure AD Conditional Access + custom ABAC engine",
    "policy_enforcement_points": ["API Gateway (Kong)", "Istio Envoy Proxy", "Zscaler ZPA"],
    "identity_provider": "Azure AD with FIDO2 MFA",
    "micro_segmentation": "Istio service mesh (K8s) + AWS Security Groups (cloud)",
    "sdp": "Zscaler Private Access (remote workforce)"
  },
  "architecture_diagram_ref": "resources/zero-trust-hybrid-architecture.png",
  "policy_examples": "resources/abac-policy-examples.json"
}
```

**Token budget check:** T2 ≤ 6k tokens

---

### T3: Comprehensive Zero-Trust Roadmap (≤12k tokens)

**Deep-dive with phased migration plan, policy library, and compliance mapping:**

**Prerequisites:** T2 architecture design completed OR detailed current-state documentation.

1. **Perform Detailed Gap Analysis (Current → Target State):**
   - **Identity Pillar:**
     - Current: List existing IdPs, MFA coverage %, authentication protocols
     - Gaps: Missing phishing-resistant MFA, no centralized IdP, no risk-based authN
     - Target: Centralized IdP (Azure AD/Okta), FIDO2 MFA 100% coverage, continuous authN

   - **Devices Pillar:**
     - Current: Device inventory coverage %, EDR deployment %, compliance enforcement
     - Gaps: No automated device posture checks, missing EDR on 40% endpoints
     - Target: 100% device inventory, EDR/XDR on all endpoints, real-time posture API

   - **Networks Pillar:**
     - Current: Network architecture (flat/segmented), encryption coverage, firewall rules
     - Gaps: Flat network, no micro-segmentation, 60% unencrypted internal traffic
     - Target: Micro-segmentation via service mesh, mTLS 100%, application-layer segmentation

   - **Applications Pillar:**
     - Current: App authentication methods, API security, workload isolation
     - Gaps: 50% apps use shared credentials, no OAuth2, no service mesh
     - Target: 100% apps with OIDC/OAuth2, service mesh with mTLS, runtime security

   - **Data Pillar:**
     - Current: Data classification scheme, encryption coverage, DLP deployment
     - Gaps: No data classification, 30% data unencrypted at rest, no DLP
     - Target: Comprehensive classification, encryption at rest/transit/use, DLP with ML

2. **Design Phased Migration Roadmap:**

   **Phase 1: Foundation (Months 1-6) - Move to "Initial" Maturity:**
   - **Identity:** Deploy centralized IdP (Azure AD), enforce MFA 100%, migrate from passwords to passwordless
   - **Devices:** Implement device inventory (MDM), deploy EDR on critical endpoints (70% coverage)
   - **Networks:** Implement basic segmentation (VLANs/VPCs), enable encryption in transit (TLS 1.3)
   - **Applications:** Migrate 20% high-value apps to OIDC/OAuth2, implement API gateway
   - **Data:** Establish data classification scheme, encrypt data at rest (databases, file shares)
   - **Metrics:** Identity=Initial, Devices=Initial, Networks=Initial, Apps=Traditional, Data=Initial
   - **Investment:** $500k-$1M (IdP licenses, EDR, consulting)

   **Phase 2: Acceleration (Months 7-12) - Move to "Advanced" Maturity:**
   - **Identity:** Deploy FIDO2/WebAuthn, implement risk-based authentication, integrate UBA
   - **Devices:** Achieve 100% EDR coverage, automate compliance enforcement, integrate device posture API
   - **Networks:** Deploy micro-segmentation (Istio service mesh for K8s, AWS Security Groups)
   - **Applications:** Migrate 80% apps to OIDC, deploy service mesh with mTLS, implement RASP
   - **Data:** Deploy DLP with ML, implement field-level encryption, enable encrypted search
   - **Metrics:** Identity=Advanced, Devices=Advanced, Networks=Advanced, Apps=Advanced, Data=Advanced
   - **Investment:** $1M-$2M (service mesh, DLP, RASP, advanced MFA)

   **Phase 3: Optimization (Months 13-24) - Move to "Optimal" Maturity:**
   - **Identity:** Continuous authentication, biometric integration, passwordless 100%
   - **Devices:** Real-time device posture, automated remediation, zero-trust device enrollment
   - **Networks:** Software-defined perimeter (SDP), application-layer segmentation, AI-driven anomaly detection
   - **Applications:** 100% apps with dynamic policy enforcement, runtime protection, automated threat response
   - **Data:** Continuous data monitoring, confidential computing (encrypted in use), homomorphic encryption (where feasible)
   - **Metrics:** Identity=Optimal, Devices=Optimal, Networks=Optimal, Apps=Optimal, Data=Optimal
   - **Investment:** $2M-$4M (SDP, confidential compute, advanced AI/ML security)

3. **Generate Policy Library and Decision Rules:**

   **Policy Template Structure (ABAC):**
   ```json
   {
     "policy_id": "zt-policy-001",
     "name": "Financial Data Access - High Risk User",
     "description": "Dynamic policy for accessing financial data based on user risk score",
     "subject": {
       "user.role": ["finance", "audit"],
       "user.clearance": ["confidential", "secret"]
     },
     "resource": {
       "data.classification": "financial",
       "data.location": ["us-east-1", "us-west-2"]
     },
     "context": {
       "time.business_hours": true,
       "location.approved_country": true,
       "device.compliant": true,
       "user.risk_score": "<= 30"
     },
     "action": "GRANT",
     "obligations": {
       "session_timeout_minutes": 60,
       "re_auth_interval_minutes": 15,
       "log_level": "VERBOSE",
       "watermark_documents": true,
       "disable_download": true
     }
   }
   ```

   **Generate Policy Library (10-15 policies covering):**
   - Low-risk user accessing public resources
   - High-risk user accessing sensitive data
   - Service-to-service communication (APIs)
   - Admin access to production systems
   - Remote workforce access (BYOD)
   - Third-party contractor access (limited scope)
   - Break-glass emergency access
   - Data exfiltration prevention (DLP integration)

   **Store policies in:** `resources/policy-library/`

4. **Map to Compliance Frameworks:**
   - **NIST SP 800-53 Rev 5:** AC-3 (Access Enforcement), AC-4 (Information Flow), AC-6 (Least Privilege), IA-2 (Identification and Authentication), SC-7 (Boundary Protection)
   - **NIST SP 800-171:** 3.1.1 (Limit system access), 3.1.3 (Control connection of mobile devices), 3.5.3 (Multifactor authentication)
   - **FedRAMP:** Continuous monitoring, least privilege, encryption in transit/rest, audit logging
   - **CMMC 2.0:** Level 3 requires zero-trust principles for DIB contractors
   - **PCI-DSS 4.0:** Requirement 8 (Identify users and authenticate access), Requirement 11 (Test security)
   - **Output:** Compliance mapping matrix in `resources/compliance-mapping.csv`

5. **Design Metrics and Success Criteria:**
   - **Maturity Metrics:** Track CISA ZTMM pillar maturity quarterly
   - **Technical Metrics:**
     - MFA adoption rate (target: 100%)
     - Device compliance rate (target: 95%+)
     - Encrypted traffic percentage (target: 100% internal)
     - Policy deny rate (should decrease as policies tune)
     - Mean time to authenticate (MTTA) (target: <2 seconds)
   - **Business Metrics:**
     - Reduction in security incidents (target: 50% reduction year-over-year)
     - Reduction in breach containment time (target: <15 minutes with micro-segmentation)
     - User productivity impact (target: <5% increase in auth time)
   - **Compliance Metrics:**
     - Number of controls satisfied by ZTA
     - Audit findings reduction (target: 70% reduction in access control findings)

6. **Generate Architecture Diagrams and Documentation:**
   - **High-level architecture:** Policy Engine, PEP, PA, IdP, trust zones
   - **Data flow diagrams:** User → PEP → PE → PA → Resource (with decision points)
   - **Deployment diagrams:** Cloud (AWS/Azure/GCP), on-prem, hybrid
   - **Sequence diagrams:** Authentication flow, authorization flow, continuous verification
   - **Store diagrams in:** `resources/architecture-diagrams/`

7. **Risk Assessment and Mitigation:**
   - **Risk:** User productivity impact from frequent re-authentication
     - **Mitigation:** Implement adaptive authentication (low-risk users = less friction)
   - **Risk:** Operational complexity of managing micro-segmentation policies
     - **Mitigation:** Start with coarse-grained policies, automate policy generation from traffic baselines
   - **Risk:** Vendor lock-in with proprietary SDP solutions
     - **Mitigation:** Use open standards (OIDC, SAML, mTLS), design modular architecture
   - **Risk:** Legacy applications incompatible with modern auth (no OIDC/SAML)
     - **Mitigation:** Use PEP proxies for legacy apps, plan app modernization roadmap

**Output (T3):**
```json
{
  "gap_analysis": {
    "identity": {"current": "Initial", "target": "Optimal", "priority": "High"},
    "devices": {"current": "Traditional", "target": "Advanced", "priority": "Critical"},
    "networks": {"current": "Initial", "target": "Advanced", "priority": "High"},
    "applications": {"current": "Traditional", "target": "Advanced", "priority": "Critical"},
    "data": {"current": "Traditional", "target": "Optimal", "priority": "Critical"}
  },
  "roadmap": {
    "phase_1": {
      "duration_months": 6,
      "target_maturity": "Initial",
      "investment_usd": "500k-1M",
      "key_deliverables": ["Centralized IdP", "MFA 100%", "Basic segmentation", "Data classification"]
    },
    "phase_2": {
      "duration_months": 6,
      "target_maturity": "Advanced",
      "investment_usd": "1M-2M",
      "key_deliverables": ["FIDO2 MFA", "Micro-segmentation", "Service mesh", "DLP deployment"]
    },
    "phase_3": {
      "duration_months": 12,
      "target_maturity": "Optimal",
      "investment_usd": "2M-4M",
      "key_deliverables": ["Continuous authN", "SDP", "Confidential compute", "AI-driven security"]
    }
  },
  "policy_library_ref": "resources/policy-library/",
  "architecture_diagrams_ref": "resources/architecture-diagrams/",
  "compliance_mapping_ref": "resources/compliance-mapping.csv",
  "metrics_dashboard_spec": "resources/metrics-dashboard.json"
}
```

**Token budget check:** T3 ≤ 12k tokens

---

## Decision Rules

**Tier selection:**
- Use **T1** when: Quick maturity check needed, no detailed architecture design required, initial ZTA awareness
- Use **T2** when: Architecture design needed, deployment model selection required, technical implementation planning
- Use **T3** when: Comprehensive roadmap required, compliance mapping needed, phased migration plan with budgets, executive presentation

**Abort conditions:**
- If `current_architecture` unavailable and cannot be assessed → Request architecture documentation, output TODO
- If `target_environment` is incompatible with zero-trust (e.g., air-gapped system with no identity source) → Flag incompatibility, suggest alternatives
- If token budget exceeded at any tier → Truncate output, provide summary + link to full analysis in resources/

**Deployment model selection logic:**
- **Choose EIG** if: Cloud-first (80%+ cloud apps), modern apps with OIDC/SAML, strong IdP exists
- **Choose Micro-segmentation** if: Datacenter-heavy, containers/K8s, east-west traffic security critical, legacy apps prevalent
- **Choose SDP** if: Remote workforce (>50% remote), BYOD policy, zero standing access required, resources must be hidden
- **Choose Hybrid (most common)** if: Mixed environment (cloud + datacenter), diverse app portfolio, phased migration

**Escalation triggers:**
- If CISA ZTMM maturity = "Traditional" across all pillars → Flag as critical risk, recommend executive briefing
- If compliance requirement (e.g., OMB M-22-09, CMMC Level 3) mandates specific maturity → Highlight in roadmap priorities
- If budget constraints conflict with compliance timeline → Surface trade-offs, propose risk acceptance vs. timeline extension

---

## Output Contract

**Required fields (all tiers):**
```typescript
{
  maturity_assessment: {
    identity: "Traditional" | "Initial" | "Advanced" | "Optimal",
    devices: "Traditional" | "Initial" | "Advanced" | "Optimal",
    networks: "Traditional" | "Initial" | "Advanced" | "Optimal",
    applications: "Traditional" | "Initial" | "Advanced" | "Optimal",
    data: "Traditional" | "Initial" | "Advanced" | "Optimal"
  },
  overall_maturity: "Traditional" | "Initial" | "Advanced" | "Optimal",
  critical_gaps: string[],  // Pillars at "Traditional" or significantly behind target
  quick_wins: string[]      // 3-5 immediate actions
}
```

**Additional fields (T2+):**
```typescript
{
  deployment_model: "EIG" | "Microsegmentation" | "SDP" | "Hybrid",
  components: {
    policy_engine: string,
    policy_enforcement_points: string[],
    identity_provider: string,
    micro_segmentation?: string,  // If applicable
    sdp?: string                   // If applicable
  },
  architecture_diagram_ref: string,  // Path to resources/
  policy_examples: string            // Path to resources/
}
```

**Additional fields (T3 only):**
```typescript
{
  gap_analysis: {
    [pillar: string]: {
      current: string,
      target: string,
      priority: "Low" | "Medium" | "High" | "Critical"
    }
  },
  roadmap: {
    [phase: string]: {
      duration_months: number,
      target_maturity: string,
      investment_usd: string,
      key_deliverables: string[]
    }
  },
  policy_library_ref: string,
  architecture_diagrams_ref: string,
  compliance_mapping_ref: string,
  metrics_dashboard_spec: string
}
```

**All outputs must:**
- Use JSON format for structured data
- Include references to resources/ for diagrams, policies, templates (not inline)
- Cite NIST SP 800-207, CISA ZTMM v2.0, and other sources with access date = `NOW_ET`
- Provide actionable recommendations (not abstract concepts)
- Align with business objectives and compliance requirements (if provided)

---

## Examples

**Example: T1 Maturity Assessment**

```
Input:
{
  "target_environment": "hybrid",
  "assessment_tier": "T1",
  "ztmm_pillars": ["identity", "devices", "networks", "applications", "data"]
}

Output:
{
  "maturity_assessment": {
    "identity": "Initial",      // MFA deployed, centralized Azure AD
    "devices": "Traditional",   // No device inventory or compliance checks
    "networks": "Initial",      // VLANs exist, no micro-segmentation
    "applications": "Traditional", // Shared credentials, no OAuth2
    "data": "Traditional"       // No classification or DLP
  },
  "overall_maturity": "Traditional",
  "critical_gaps": ["devices", "applications", "data"],
  "quick_wins": [
    "Deploy Intune/Jamf for device inventory and compliance (devices)",
    "Migrate top 5 apps to Azure AD OAuth2 (applications)",
    "Establish 3-tier data classification scheme (data)"
  ]
}
```

---

## Quality Gates

**Token budgets (enforced):**
- T1: ≤ 2,000 tokens (quick maturity assessment only)
- T2: ≤ 6,000 tokens (architecture design + deployment model)
- T3: ≤ 12,000 tokens (comprehensive roadmap + policy library + compliance mapping)

**Safety and privacy:**
- No secrets, API keys, or PII in outputs
- Architecture diagrams must not expose internal IP addresses or security-sensitive topology
- Policy examples must use placeholder values (e.g., `user.email = "*@company.com"`, not real emails)

**Auditability:**
- All claims about NIST SP 800-207 or CISA ZTMM must cite specific section/page with access date
- Maturity level assignments must reference CISA ZTMM v2.0 pillar definitions
- Compliance mappings must reference specific controls (e.g., NIST 800-53 AC-3, not just "access control")

**Determinism:**
- Same inputs → same maturity assessment (deterministic scoring)
- Deployment model selection uses decision rules (not random)
- Roadmap phases follow consistent structure (Foundation → Acceleration → Optimization)

**Actionability:**
- Every gap must have 1+ remediation actions
- Every roadmap phase must have deliverables + investment estimate
- Every policy must have concrete implementation guidance (not abstract principles)

**Composability:**
- Outputs compatible with `security-assessment-framework` findings format
- Architecture diagrams reference `cloud-native-deployment-orchestrator` patterns (if applicable)
- Compliance mappings align with `compliance-automation-engine` control library

---

## Resources

**NIST Publications:**
- NIST SP 800-207 Zero Trust Architecture (August 2020): https://csrc.nist.gov/publications/detail/sp/800-207/final
- NIST SP 800-207A Cloud-Native ZTA (June 2023): https://csrc.nist.gov/pubs/sp/800/207/a/final
- NIST SP 800-53 Rev 5 Security Controls (September 2020): https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- NIST SP 800-63B Digital Identity Guidelines (June 2017, updated 2020): https://csrc.nist.gov/publications/detail/sp/800-63b/final

**CISA Resources:**
- CISA Zero Trust Maturity Model v2.0 (April 2023): https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf
- CISA Zero Trust Maturity Model Overview: https://www.cisa.gov/zero-trust-maturity-model
- OMB M-22-09 Federal Zero Trust Strategy (January 2022): https://www.whitehouse.gov/wp-content/uploads/2022/01/M-22-09.pdf

**Industry Implementations:**
- Google BeyondCorp Zero Trust: https://cloud.google.com/beyondcorp
- Microsoft Zero Trust Architecture: https://www.microsoft.com/en-us/security/business/zero-trust
- AWS Zero Trust Architecture: https://aws.amazon.com/blogs/publicsector/how-to-approach-zero-trust-security-aws/

**Tools and Frameworks:**
- CNCF Service Mesh Landscape: https://landscape.cncf.io/guide#runtime--cloud-native-network--service-mesh
- OpenID Connect (OIDC) Spec: https://openid.net/connect/
- FIDO Alliance (FIDO2/WebAuthn): https://fidoalliance.org/fido2/

**Local Resources (generated by this skill):**
- `resources/policy-library/` - ABAC policy templates (JSON)
- `resources/architecture-diagrams/` - ZTA reference architectures (PNG/SVG)
- `resources/compliance-mapping.csv` - Control mappings (NIST 800-53, CMMC, PCI-DSS)
- `resources/ztmm-assessment-template.xlsx` - CISA ZTMM pillar assessment worksheet
- `resources/metrics-dashboard.json` - Grafana/Datadog dashboard spec for ZTA metrics
