# Changelog

All notable changes to the Kubernetes Manifest Generator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of kubernetes-manifest-generator skill
- T1 tier: Basic Deployment and Service manifest generation
- T2 tier: Production hardening with security contexts, health checks, RBAC, NetworkPolicies
- T3 tier: Advanced features including PVCs, PDBs, affinity rules, GitOps structure
- Support for Deployment, StatefulSet, DaemonSet, Job, and CronJob workload types
- Validation using kubectl dry-run
- Best practices compliance reporting
- Pod Security Standards enforcement (restricted profile)
- Resource sizing recommendations based on workload type

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- Kubernetes API v1.28+ compatibility
- Follows CLAUDE.md §3 structure and token budgets
