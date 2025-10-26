# Changelog - Infrastructure Drift Detection and Remediation

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of infrastructure-drift-detector skill
- T1 fast path: Single-stack drift detection with basic remediation guidance (≤2k tokens)
- T2 extended path: Multi-stack analysis, impact assessment, automated remediation (≤6k tokens)
- Support for Terraform, CloudFormation, Pulumi, and driftctl
- Drift severity classification (high/medium/low)
- Remediation plan generation with approval workflows
- Compliance impact analysis with control mapping
- Drift trend analysis and reporting
- Notification integration (Slack, email, webhook)
- Automated remediation execution with rollback support
- Comprehensive examples and resource templates
- 5 evaluation scenarios covering common use cases

### Documentation
- Complete SKILL.md with authoritative sources (accessed 2025-10-25T21:30:36-04:00)
- Drift detection configuration examples
- Remediation workflow templates
- Compliance mapping reference

### Sources
- HashiCorp Terraform Cloud drift detection tutorial
- Pulumi drift detection and remediation docs
- AWS CloudFormation drift detection user guide
- Snyk driftctl GitHub repository
- Spacelift drift management best practices

### Dependencies
- Requires: devops-pipeline-architect (for IaC context and CI/CD integration)

### Security
- No credentials stored in skill outputs
- State files accessed read-only unless remediation authorized
- Audit log of all remediation actions
- Principle of least privilege for cloud provider access
