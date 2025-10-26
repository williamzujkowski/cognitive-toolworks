# Changelog

All notable changes to the Helm Chart Builder skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of helm-chart-builder skill
- T1 tier: Basic Helm chart structure with Chart.yaml, values.yaml, and parameterized templates
- T2 tier: Multi-environment values files, chart dependencies, hooks, advanced templating, values schema
- T3 tier: Chart testing, comprehensive documentation, packaging and signing
- Support for Deployment, Service, StatefulSet, Ingress, ConfigMap, Secret templates
- Chart dependency management with Chart.lock
- Helm hooks for pre-install, post-install, pre-upgrade lifecycle events
- Named templates in _helpers.tpl for reusable template snippets
- Multi-environment configuration (dev, staging, prod)
- Helm lint and template validation

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- Helm 3.x best practices and template guide
- Follows CLAUDE.md §3 structure and token budgets
