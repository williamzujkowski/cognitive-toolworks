# Changelog

All notable changes to the DevOps Pipeline Orchestrator agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of DevOps Pipeline Orchestrator agent
- 4-step workflow orchestrating specialized skills:
  1. CI/CD pipeline generation
  2. Infrastructure as Code template generation
  3. Observability stack configuration
  4. Deployment strategy design
- System prompt ≤1500 tokens for efficient orchestration
- Integration guide generation for component coordination
- Comprehensive setup guide with dependency sequencing
- Validation checklist for deployment readiness
- Token budget management across skill invocations

### Notes
- Replaces monolithic devops-pipeline-architect skill with focused orchestration
- Delegates to 4 specialized skills instead of reimplementing capabilities
- Follows CLAUDE.md agent standards with 8 required sections
- Total token budget: ≤10k tokens across all skill invocations
