# Changelog - Security Assessment Framework

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of security-assessment-framework skill
- T1 (≤2k tokens): Quick security scan across 8 domains (AppSec, CloudSec, ContainerSec, CryptoSec, IAM, NetworkSec, OSSec, ZeroTrust)
- T2 (≤6k tokens): Domain-specific deep dive with OWASP, NIST, CIS, CISA standards
- T3 (≤12k tokens): Comprehensive threat modeling with STRIDE/DREAD analysis
- Complete OWASP Top 10 2021 coverage
- OWASP API Security Top 10 integration
- NIST SP 800-53 Rev 5 control mapping
- CIS Benchmarks integration (Linux, Windows, Docker, Kubernetes)
- CISA Zero Trust Maturity Model assessment
- Cloud security assessment (AWS, Azure, GCP)
- Compliance framework mapping (NIST, FedRAMP, PCI-DSS, HIPAA)
- CVSS v3.1 scoring for all findings
- Resource templates: AppSec checklist, CloudSec checklist, ZeroTrust maturity
- Example T1 assessment output
- Comprehensive documentation with 8 authoritative sources

### Security
- All sources cited with access dates (NOW_ET: 2025-10-25T21:30:36-04:00)
- No credential exposure in examples
- No exploitation code provided
- No PII in outputs

### Documentation
- Complete SKILL.md with all required sections per CLAUDE.md §3
- Front-matter with all required keys
- Progressive disclosure (T1 → T2 → T3)
- Token budgets enforced and documented
- Decision rules and abort conditions specified
- Output contract with JSON schemas
