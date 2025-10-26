# Changelog

All notable changes to the Deployment Strategy Designer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of Deployment Strategy Designer skill
- Support for rolling, blue-green, canary, and recreate deployment strategies
- T1 tier: Basic strategy selection and documentation
- T2 tier: Advanced strategies with progressive rollout and automated rollback
- T3 tier: Multi-region deployment and database migration strategies
- Platform-specific implementations (Kubernetes, ECS, Lambda)
- Automated rollback procedures with monitoring integration
- Health check and validation configurations

### Notes
- Extracted from devops-pipeline-architect skill as focused capability
- Follows CLAUDE.md standards with ≤2 step procedure
- Token budgets: T1≤2k, T2≤6k, T3≤12k
