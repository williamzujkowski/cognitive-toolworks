# Changelog

All notable changes to the Compliance Automation Engine skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of Compliance Automation Engine skill
- Multi-framework support: NIST CSF, NIST 800-53, FedRAMP, FISMA, GDPR, HIPAA, PCI-DSS
- Three-tier validation modes (T1: quick check ≤2k tokens, T2: standard ≤6k tokens, T3: comprehensive ≤12k tokens)
- OSCAL artifact generation (SSP, SAP, SAR, POA&M) compliant with OSCAL 1.1.2
- Automated evidence collection and validation
- Gap analysis with risk-based prioritization
- Control inheritance analysis for cloud providers (AWS, Azure)
- Cross-framework control mapping using NIST CSF as pivot
- Continuous compliance monitoring design
- Remediation planning with effort estimation
- Compliance dashboard metrics generation
- 8 authoritative source citations with access dates (NIST, FedRAMP, GDPR, HIPAA)
- Comprehensive examples and evaluation scenarios
- Integration with existing oscal-ssp-validate and fedramp-poam-qc skills

### Quality Gates
- Token budgets enforced: T1 ≤2k, T2 ≤6k, T3 ≤12k
- OSCAL schema validation against official NIST schemas
- No secrets or PII in generated artifacts
- Deterministic output for identical inputs
- All sources cited with NOW_ET access dates

### Documentation
- Complete SKILL.md following CLAUDE.md §3 requirements
- Example ≤30 lines (27 lines actual)
- 5 evaluation scenarios in evals YAML
- Resource templates and schemas provided
