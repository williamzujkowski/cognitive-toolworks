# Changelog

All notable changes to the supply-chain-security-validator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of Software Supply Chain Security Validator skill
- T1 tier: Basic SBOM generation (SPDX/CycloneDX) and vulnerability scanning
- T2 tier: Full SLSA provenance verification and Sigstore attestation
- Support for multiple artifact types: source, container, binary, package
- Vulnerability scanning with configurable thresholds (low/medium/high/critical)
- SLSA level assessment (L1-L4) with build provenance validation
- Signature verification via Sigstore/Cosign with Rekor transparency log
- Supply chain risk scoring (0-100 scale)
- EO 14028 compliance reporting
- Integration guidance for syft, grype, trivy, cosign, osv-scanner
- Comprehensive examples for container images and source code
- NTIA minimum elements validation
- Machine-readable JSON output and human-readable Markdown reports
