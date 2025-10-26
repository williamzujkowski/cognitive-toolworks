# Changelog

All notable changes to the Cloud-Native Deployment Orchestrator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of cloud-native deployment orchestrator skill
- T1 tier: Quick deployment pattern recommendations (≤2k tokens)
- T2 tier: Extended deployment design with platform-specific optimization (≤6k tokens)
- T3 tier: Production-ready deployment with comprehensive security and observability (≤12k tokens)
- Support for Kubernetes, serverless, and hybrid deployment patterns
- Multi-cloud support (AWS EKS, Azure AKS, GCP GKE)
- Service mesh configuration guidance (Istio, Linkerd)
- Helm chart generation and templating
- Docker containerization best practices with multi-stage builds
- Security hardening: NetworkPolicy, RBAC, Pod Security Standards
- Autoscaling configuration: HPA, VPA, cluster autoscaling
- Observability integration: Prometheus, Grafana, OpenTelemetry
- GitOps workflow integration (ArgoCD, Flux)
- Cost optimization recommendations
- Disaster recovery and backup strategies
- Migration planning for legacy to cloud-native

### Documentation
- Complete SKILL.md with 8 authoritative sources (accessed 2025-10-25T21:30:36-04:00)
- Example deployment manifest (≤30 lines)
- Resource templates: Dockerfile, K8s manifests, Helm charts
- Decision rules for platform selection
- Output contract with JSON schema
- Quality gates and validation requirements

### Sources
- Kubernetes official documentation (v1.28+)
- Docker best practices guide
- CNCF landscape and project maturity
- Helm 3.x best practices
- Istio service mesh documentation
- AWS EKS best practices guide
- Azure AKS best practices
- GCP GKE best practices

## [Unreleased]

### Planned
- Knative serverless on Kubernetes integration
- eBPF-based observability patterns
- WebAssembly (Wasm) workload support
- GitOps progressive delivery patterns (Argo Rollouts advanced strategies)
- Multi-cluster federation guidance
- Service mesh comparison matrix (Istio vs Linkerd vs Consul)
