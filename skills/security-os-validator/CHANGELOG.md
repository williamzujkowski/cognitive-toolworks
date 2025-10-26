# Changelog - ossec-hardening-checker

All notable changes to this skill will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release extracted from security-assessment-framework skill
- CIS benchmark compliance validation (Linux, Windows Server)
- OS patch currency validation (30-day threshold)
- Kernel hardening verification (SELinux, AppArmor)
- Host-based firewall configuration review
- File integrity monitoring assessment
- Support for ubuntu, rhel, centos, debian, windows-server distributions
- CIS Level 1 (basic) and Level 2 (comprehensive) compliance
- Token budget enforcement: T1 ≤2k, T2 ≤6k
- OS-specific remediation commands

### Notes
- Focused single-domain skill following CLAUDE.md ≤2 step principle
- All CIS Benchmark references updated with 2025-10-26 access dates
