# Changelog - security-auditor

All notable changes to this agent will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release as orchestrator agent for comprehensive security assessments
- Multi-domain security orchestration across 8 specialized skills:
  - appsec-validator (Application Security)
  - cloudsec-posture-analyzer (Cloud Security)
  - container-security-checker (Container/Kubernetes Security)
  - cryptosec-validator (Cryptographic Security)
  - iam-security-reviewer (Identity and Access Management)
  - networksec-architecture-validator (Network Security)
  - ossec-hardening-checker (Operating System Hardening)
  - zerotrust-maturity-assessor (Zero Trust Maturity)
- Three-tier assessment workflow: T1 (Quick), T2 (Standard), T3 (Comprehensive)
- STRIDE/DREAD threat modeling coordination (T3)
- Compliance framework mapping (NIST, FedRAMP, OWASP, CIS)
- Automatic domain detection based on target system type
- Parallel skill execution for efficiency
- Finding aggregation and cross-domain risk scoring
- Unified remediation roadmap generation
- Executive summary generation (T3 only)

### Notes
- Replaces monolithic security-assessment-framework skill
- Follows CLAUDE.md agent orchestration patterns
- System prompt optimized to ≤1500 tokens
- Total token budgets: T1 ≤8k, T2 ≤30k, T3 ≤100k
