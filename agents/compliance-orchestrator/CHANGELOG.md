# Changelog — Compliance Orchestrator

All notable changes to the Compliance Orchestrator agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial agent specification following CLAUDE.md standards
- 4-step workflow: Discovery → Assessment → Synthesis → Validation
- Multi-framework support: FedRAMP (Low/Moderate/High), NIST 800-53 Rev 5, FISMA, HIPAA, GDPR
- OSCAL artifact generation: SSP, SAP, SAR, POA&M (tier-dependent)
- System prompt with orchestration logic (1,347 tokens, within 1,500 limit)
- Tool usage guidelines for Read, Write, Bash, Grep, Glob, Task
- Skills integration patterns (oscal-ssp-validate, security-assessment-framework)
- FedRAMP ATO preparation example (≤30 lines)
- Quality gates for coverage thresholds, evidence age, critical gaps
- Resource citations with NOW_ET timestamps (accessed 2025-10-26T01:33:55-04:00)

### Framework Capabilities
- **FedRAMP**: Low (125 controls), Moderate (325 controls), High (421 controls)
- **NIST 800-53 Rev 5**: 20 control families with parameter customization
- **FISMA**: FIPS 199 categorization, RMF integration
- **HIPAA**: Security Rule (45 CFR 164.308-316), PHI protection
- **GDPR**: Articles 5, 25, 32 (data protection, security)
- **Cross-framework mapping**: NIST CSF as pivot for control alignment

### Orchestration Features
- Progressive disclosure: T1 (quick check) → T2 (OSCAL SSP) → T3 (full suite)
- Evidence validation: freshness checks, coverage metrics, gap analysis
- Control inheritance analysis: AWS GovCloud, Azure Government
- Risk-based prioritization: NIST RMF risk scoring framework
- Continuous monitoring design: dashboard schemas, alerting thresholds
- Audit trail: NOW_ET timestamps, justifications, responsible parties

### Design Decisions
- Model set to "inherit" for flexibility across Sonnet/Opus/Haiku
- Toolset: Read, Write, Bash, Grep, Glob, Task (delegation-capable)
- System prompt extraction: Detailed procedures in workflows/ directory
- Agent vs Skill decision rule: ≥4 steps = agent, ≤2 steps = skill
- OSCAL schema version: 1.1.2+ (latest stable)

### Quality Metrics
- System prompt: 1,347 tokens (within 1,500 limit)
- Description: 135 characters (within 160 limit)
- Example: 30 lines (FedRAMP ATO preparation workflow)
- Sources cited: 15+ with access dates
- Tool restrictions: All MCP-approved

### Quality Thresholds
- Coverage warning: <80% (improvement recommended)
- Coverage error: <70% (defer assessment)
- Evidence age warning: >90 days (refresh recommended)
- Evidence age error: >365 days (refresh required)
- Critical gaps: AC-1, AC-2, IA-2, IA-5, SC-7, SC-8 = ATO blockers

### Output Contract
- compliance_report (JSON): metadata, summary, gaps, metrics
- oscal_artifacts (JSON/XML): SSP, SAP, SAR, POA&M
- remediation_plan (markdown): prioritized gaps, effort estimates
- dashboard_data (JSON): time-series metrics for visualization

### References
- Migrated from /skills/compliance-automation-engine/SKILL.md (deprecated)
- Follows CLAUDE.md v1.0.0 agent specification format
- Based on NIST SP 800-37 Rev 2 Risk Management Framework (accessed 2025-10-26T01:33:55-04:00)
- Based on FedRAMP authorization requirements (accessed 2025-10-26T01:33:55-04:00)
- Based on OSCAL 1.1.2 specification (accessed 2025-10-26T01:33:55-04:00)
