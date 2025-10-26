# Changelog - Incident Response Orchestrator

All notable changes to the Incident Response Orchestrator agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-26

### Added
- Initial release of Incident Response Orchestrator agent
- 4-step orchestration workflow: Detection → Triage → Response → Post-Mortem
- NIST SP 800-61 Rev 2 lifecycle enforcement across all incident types
- Multi-skill coordination:
  - incident-response-playbook-generator (primary playbook generation)
  - security-assessment-framework (security incident threat modeling)
  - observability-stack-generator (infrastructure incident debugging)
  - compliance-orchestrator (HIPAA, PCI-DSS, SOC2, FedRAMP reporting)
- Auto-escalation based on severity (P0/P1/P2/P3) and duration thresholds
- Compliance-driven workflows for HIPAA, PCI-DSS, SOC2, FedRAMP
- Incident timeline tracking with ISO-8601 timestamps
- Post-mortem generation with 5 Whys root cause analysis
- MTTD/MTTR metrics computation
- System prompt ≤1500 token budget (actual: ~480 tokens)
- Total workflow token budget: ≤6.5k tokens (T1/T2 tier support)

### Decision Rules
- P0/P1 security incidents → Always invoke security-assessment-framework
- Data breach incidents → Auto-invoke HIPAA/PCI-DSS compliance reporting
- Infrastructure incidents → Coordinate with observability skills
- Auto-escalation: P0=30min, P1=2hr, P2=8hr duration thresholds

### Documentation
- Complete AGENT.md with 8 required sections per CLAUDE.md
- Example workflow for data breach (P0) with HIPAA compliance
- Token budget tracking and validation
- NIST SP 800-61 and PagerDuty best practices citations (accessed 2025-10-26T01:56:01-04:00)

### Quality Gates
- System prompt: 480 tokens (within 1500 budget)
- No secrets or PII handling (references only)
- All timestamps in ISO-8601 America/New_York format
- Deterministic skill routing based on incident classification

---

## Template for Future Releases

### [Unreleased]

#### Added
- New features and capabilities

#### Changed
- Updates to existing functionality

#### Deprecated
- Features marked for removal

#### Removed
- Deleted features

#### Fixed
- Bug fixes

#### Security
- Security improvements or patches

---

**Maintenance Notes:**
- Update `LAST_AUDIT` during validation runs
- Review NIST SP 800-61 and PagerDuty documentation quarterly for updates
- Validate skill coordination contracts when coordinated skills are updated
- Keep system prompt under 1500 token budget for all changes
