# Changelog - cloudsec-posture-analyzer

All notable changes to this skill will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release extracted from security-assessment-framework skill
- Multi-cloud support: AWS, Azure, GCP
- Public storage bucket detection (S3, Azure Storage, GCS)
- IAM overpermissive policy identification
- Encryption at rest and in transit validation
- VPC/network segmentation verification
- CIS Benchmark and Well-Architected Framework compliance checking
- Platform-specific remediation commands (AWS CLI, Azure CLI, gcloud)
- Token budget enforcement: T1 ≤2k, T2 ≤6k

### Notes
- Focused single-domain skill following CLAUDE.md ≤2 step principle
- All cloud platform references updated with 2025-10-26 access dates
