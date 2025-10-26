# Changelog

All notable changes to the Serverless Deployment Designer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of serverless-deployment-designer skill
- T1 tier: Basic function configuration with single event source
- T2 tier: Production IAM policies, VPC integration, cold start optimization, SAM/Serverless Framework templates
- T3 tier: Multi-function orchestration with Step Functions, CI/CD pipelines, advanced observability
- Support for AWS Lambda, Azure Functions, Google Cloud Functions
- Event source mapping for HTTP, S3, Queue, Schedule, and Stream triggers
- Least-privilege IAM policy generation
- Cold start optimization strategies (provisioned concurrency, package size reduction)
- Cost estimation and optimization recommendations

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- AWS Lambda, Azure Functions, Google Cloud Functions best practices
- Follows CLAUDE.md §3 structure and token budgets
