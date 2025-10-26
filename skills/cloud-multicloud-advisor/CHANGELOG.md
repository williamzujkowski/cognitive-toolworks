# Changelog - multicloud-strategy-advisor

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of Multi-Cloud Strategy Advisor skill
- T1 tier: Quick multi-cloud assessment with vendor shortlist (≤2k tokens)
- T2 tier: Complete strategy with vendor comparison, TCO analysis, integration patterns, lock-in mitigation (≤6k tokens)
- Vendor comparison framework across AWS, Azure, GCP for compute, storage, networking, serverless, Kubernetes, hybrid
- TCO calculation framework with 3/5/7 year projections including compute, storage, network, managed services, support, training
- Integration pattern recommendations: IaC (Terraform/Pulumi), Kubernetes, service mesh, event streaming, identity federation, network connectivity
- Vendor lock-in mitigation strategies: data portability, API abstraction, containerization, schema portability, exit strategy planning
- Decision rules for vendor selection thresholds, multi-cloud vs hybrid determination, TCO optimization
- JSON output contract with vendors, TCO analysis, integration patterns, lock-in mitigation, roadmap
- Quality gates for token budgets, safety, auditability, determinism
- 10 authoritative sources with access dates (AWS, Azure, GCP, CNCF, EDUCAUSE, vendor lock-in guides)
- Example showing global, compliant workload split between AWS (primary) and GCP (ML/analytics)
- Resource files: vendor comparison matrix, TCO calculator template, integration patterns guide

### Dependencies
- aws-multi-service-architect (leverages)
- cloud-native-deployment-orchestrator (leverages)

### Notes
- Consolidates "cloud-multicloud-strategy" from original 272-directory analysis
- Priority P3, Phase 3, T2 budget per analyst-implementation-plan.json
- All sources accessed 2025-10-25T21:30:36-04:00 per CLAUDE.md requirements
