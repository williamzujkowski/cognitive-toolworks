# Changelog - Zero Trust Architecture Designer

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of zero-trust-architecture-designer skill
- CISA Zero Trust Maturity Model (ZTMM) v2.0 assessment across 5 pillars (Identity, Devices, Networks, Applications, Data)
- NIST SP 800-207 deployment model selection (EIG, Micro-segmentation, SDP, Hybrid)
- T1 tier: Quick maturity assessment (≤2k tokens)
- T2 tier: Architecture design with deployment model selection (≤6k tokens)
- T3 tier: Comprehensive roadmap with phased migration plan, policy library, compliance mapping (≤12k tokens)
- ABAC policy template library with 10-15 example policies
- Compliance mapping to NIST SP 800-53, NIST SP 800-171, FedRAMP, CMMC 2.0, PCI-DSS 4.0
- Architecture diagrams and data flow diagrams for ZTA components
- Integration with security-assessment-framework and cloud-native-deployment-orchestrator skills
- Resource templates: policy-library/, architecture-diagrams/, compliance-mapping.csv, ztmm-assessment-template.xlsx

### Referenced Sources (accessed 2025-10-25T21:30:36-04:00)
- NIST SP 800-207 Zero Trust Architecture (August 2020)
- CISA Zero Trust Maturity Model v2.0 (April 2023)
- NIST SP 800-207A Cloud-Native ZTA (June 2023)
- OMB M-22-09 Federal Zero Trust Strategy (January 2022)
- Google BeyondCorp Zero Trust
- Microsoft Zero Trust Architecture
- FIDO Alliance FIDO2/WebAuthn specifications
- OpenID Connect (OIDC) specifications

### Quality Gates
- Token budgets enforced: T1 ≤2k, T2 ≤6k, T3 ≤12k
- All claims cited with access dates
- No secrets or PII in outputs
- Deterministic maturity scoring
- Actionable recommendations with investment estimates
