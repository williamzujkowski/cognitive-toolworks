# Changelog

All notable changes to the Cloud Cost Optimization Analyzer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of Cloud Cost Optimization Analyzer skill
- Multi-cloud support for AWS, Azure, and GCP cost analysis
- T1 tier: Quick cost health check (≤2k tokens)
- T2 tier: Comprehensive cost analysis with rightsizing, commitment optimization, and storage tiering (≤6k tokens)
- Waste detection for idle and unused resources
- Reserved instance and savings plan recommendations
- Storage lifecycle and tiering optimization
- Network cost optimization analysis
- Cost anomaly detection with configurable thresholds
- Basic FinOps maturity assessment
- Prioritized action plan with ROI calculations
- JSON output schema with required and optional fields
- Integration with aws-multi-service-architect skill
- Comprehensive resource links to AWS, Azure, GCP, and FinOps Foundation
- Example input/output scenarios
- Quality gates for token budgets, accuracy, and auditability

### Security
- Read-only access to billing APIs enforced
- No automatic resource modification without approval
- Secure handling of sensitive cost data
- Audit logging of all recommendations

### Sources
- AWS Cost Management documentation (accessed 2025-10-25T22:42:30-04:00)
- Azure Cost Optimization documentation (accessed 2025-10-25T22:42:30-04:00)
- GCP Cost Management documentation (accessed 2025-10-25T22:42:30-04:00)
- FinOps Foundation framework and principles (accessed 2025-10-25T22:42:30-04:00)

## [Unreleased]

### Planned for future versions
- T3 tier: Predictive cost forecasting using ML
- Multi-account and organization-wide cost consolidation
- Custom FinOps policy enforcement
- Real-time cost anomaly alerting integration
- Kubernetes cost optimization (namespace-level)
- Spot instance and preemptible VM recommendations
- Cross-cloud cost comparison and arbitrage analysis
