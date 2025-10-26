# Changelog

All notable changes to the Container Image Optimizer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of container-image-optimizer skill
- T1 tier: Basic multi-stage Dockerfile generation with .dockerignore
- T2 tier: Production optimization with security scanning, hardening, and size reduction
- T3 tier: Multi-architecture builds, SBOM generation, image signing, CI/CD integration
- Support for Node.js, Python, Go, Java, and Rust applications
- Base image selection (distroless, alpine, scratch, ubuntu)
- Vulnerability scanning integration (Trivy, Grype)
- Layer caching optimization strategies
- Non-root user configuration and security best practices

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- Docker BuildKit and multi-stage build best practices
- Follows CLAUDE.md §3 structure and token budgets
