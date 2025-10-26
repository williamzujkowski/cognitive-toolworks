# Changelog

All notable changes to the API Design Validator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of API Design Validator skill
- T1: Schema validation for REST (OpenAPI 3.x) and GraphQL APIs
- T2: OWASP API Security Top 10 2023 compliance checking
- REST design patterns: pagination, filtering, sorting, versioning, error handling
- GraphQL design patterns: Relay connections, DataLoader, depth limiting
- OpenAPI 3.1.0 specification compliance validation
- GraphQL SDL syntax validation
- Security recommendations with OWASP mappings
- Integration with security-assessment-framework for advanced IAM scenarios

### Security
- All validation rules based on OWASP API Security Top 10 2023
- No execution of untrusted API specifications
- No credential or secret exposure in examples or validation output

### Documentation
- Complete SKILL.md with T1/T2 tier procedures
- Example validation scenarios (REST and GraphQL)
- Resource templates and schemas in `/resources/`
- Evaluation scenarios in `/tests/evals_api-design-validator.yaml`

### References
- OpenAPI 3.1.0 Specification (accessed 2025-10-25T21:30:36-04:00)
- GraphQL Specification October 2021 (accessed 2025-10-25T21:30:36-04:00)
- OWASP API Security Top 10 2023 (accessed 2025-10-25T21:30:36-04:00)
- HTTP Semantics RFC 9110 (accessed 2025-10-25T21:30:36-04:00)
- RFC 9457 Problem Details for HTTP APIs (accessed 2025-10-25T21:30:36-04:00)
- Relay GraphQL Cursor Connections Specification (accessed 2025-10-25T21:30:36-04:00)
