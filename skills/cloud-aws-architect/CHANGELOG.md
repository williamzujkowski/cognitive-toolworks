# Changelog - AWS Multi-Service Architect

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of AWS Multi-Service Architect skill
- T1 tier: Quick architecture recommendations for common workload types
- T2 tier: Detailed architecture design with CloudFormation/CDK templates
- Comprehensive AWS service coverage: compute (EC2, Lambda, ECS, EKS), storage (S3, EBS, EFS), networking (VPC), serverless
- Well-Architected Framework assessment across all five pillars
- Cost estimation with TCO analysis and optimization recommendations
- IAM policy generation with least-privilege principles
- Migration strategy planning for existing infrastructure
- CloudFormation and CDK infrastructure-as-code template generation
- Security hardening recommendations (encryption, IAM, security groups, VPC design)
- Multi-region and disaster recovery architecture patterns
- Example templates in resources/ directory

### Documentation
- Complete SKILL.md following CLAUDE.md §3 format
- Token budgets enforced: T1 ≤2k, T2 ≤6k
- Source citations with access dates (2025-10-25T21:30:36-04:00)
- Decision rules for service selection and architecture patterns
- Output contracts with JSON schemas for programmatic consumption

### Resources
- CloudFormation example for serverless web application
- CloudFormation example for ECS Fargate with ALB
- CDK TypeScript example for web application stack
- IAM least-privilege policy examples
- VPC reference architecture template

### Dependencies
- Leverages: cloud-native-deployment-orchestrator (for Kubernetes/ECS patterns)
- Leverages: security-assessment-framework (for security hardening)

### Compliance
- Aligned with AWS Well-Architected Framework (2024 version)
- No secrets or PII in templates
- All examples use placeholder values
