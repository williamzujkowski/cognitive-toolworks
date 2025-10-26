# Changelog - DevOps Pipeline Architect

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of DevOps Pipeline Architect skill
- T1 tier: Basic CI/CD pipeline generation for common tech stacks
- T2 tier: Multi-environment pipelines with IaC, deployment strategies, and observability
- Support for GitHub Actions, GitLab CI, Jenkins, Azure DevOps platforms
- Infrastructure as Code templates for Terraform, CloudFormation, Pulumi
- Observability stack configuration (Prometheus, OpenTelemetry, logging)
- Deployment strategies: rolling, blue-green, canary, recreate
- Security hardening: SAST, SCA, secret scanning, container scanning
- Integration with testing-strategy-composer skill (dependency)
- Comprehensive decision rules for platform, deployment strategy, and IaC tool selection
- Example configurations and resource templates
- NIST time normalization (NOW_ET) in Pre-Checks
- Token budgets: T1 ≤2k, T2 ≤6k
- 6 authoritative sources cited with access dates (2025-10-25T21:30:36-04:00)

### Documentation
- Architecture diagrams for deployment flows
- Runbooks for common operations
- Setup guides and environment variable checklists
- Quality gates and safety checks documented

### Security
- No PII or secrets in outputs
- Sandbox execution required
- Supply chain security with artifact signing (Cosign/Sigstore)
- Compliance gates with policy-as-code (OPA, Sentinel)
