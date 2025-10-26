# Changelog - cryptosec-validator

All notable changes to this skill will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release extracted from security-assessment-framework skill
- TLS 1.2+ enforcement validation
- Cipher suite strength analysis (NIST SP 800-52 Rev 2 compliance)
- Certificate validity and lifecycle management checks
- Key rotation mechanism verification
- FIPS 140-2/3 compliance checking
- Support for NIST, FIPS, and PCI-DSS compliance standards
- Token budget enforcement: T1 ≤2k, T2 ≤6k
- TLS/cipher configuration snippets for remediation

### Notes
- Focused single-domain skill following CLAUDE.md ≤2 step principle
- All NIST cryptographic standards updated with 2025-10-26 access dates
