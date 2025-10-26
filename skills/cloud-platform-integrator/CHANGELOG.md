# Changelog

All notable changes to the Cloud Platform Integrator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of cloud-platform-integrator skill
- T1 tier: Basic cloud IAM integration (IRSA, Workload Identity) and storage classes
- T2 tier: Cloud-native ingress controllers, cluster autoscaling, monitoring integration, registry authentication
- T3 tier: Multi-AZ HA configuration, advanced autoscaling with custom metrics, disaster recovery with Velero
- Support for AWS EKS, Azure AKS, and Google Cloud GKE
- IAM roles for service accounts (IRSA for AWS, Workload Identity for Azure/GCP)
- Cloud-native ingress controllers (ALB Controller, AGIC, GKE Ingress)
- Storage class definitions for EBS, Azure Disk, and Persistent Disk
- Cluster autoscaling with Cluster Autoscaler, Karpenter (AWS), and managed autoscalers
- Cloud monitoring integration (CloudWatch Container Insights, Azure Monitor, Cloud Logging)

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- AWS EKS, Azure AKS, Google Cloud GKE best practices
- Follows CLAUDE.md §3 structure and token budgets
