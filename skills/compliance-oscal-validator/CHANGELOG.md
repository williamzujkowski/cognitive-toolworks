# Changelog - oscal-ssp-validate

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of OSCAL SSP validation skill
- Three-tier validation approach (T1: schema, T2: profile, T3: cross-ref)
- Support for JSON, XML, and YAML SSP formats
- Profile alignment checking against OSCAL profiles
- Cross-reference integrity validation for components and UUIDs
- Structured JSON output with markdown summary
- Citation discipline with 4 authoritative NIST sources
- Token budgets: T1 ≤2k, T2 ≤6k, T3 ≤12k tokens
- Example validation scenario (≤30 lines)
- Quality gates for safety, auditability, and determinism

### References
- NIST OSCAL SSP Model v1.1.2 (accessed 2025-10-25T21:04:34-04:00)
- OSCAL validation concepts and FedRAMP layers documentation
- OSCAL GitHub repository schemas and tools
