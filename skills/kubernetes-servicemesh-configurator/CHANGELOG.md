# Changelog

All notable changes to the Service Mesh Configurator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of service-mesh-configurator skill
- T1 tier: Basic sidecar injection, mTLS, and simple traffic routing
- T2 tier: Advanced traffic management with canary, circuit breaking, retry policies, authorization, observability
- T3 tier: Multi-cluster mesh federation, egress control, performance tuning
- Support for Istio, Linkerd, and Consul Connect service meshes
- VirtualService and DestinationRule configuration for traffic routing
- Mutual TLS (mTLS) configuration with strict, permissive, and disabled modes
- Circuit breaker and retry policy configuration for resilience
- Authorization and authentication policies for zero-trust security
- Distributed tracing and metrics integration (Jaeger, Prometheus, Grafana)

### References
- Extracted from cloud-native-deployment-orchestrator v1.0.0
- Istio, Linkerd, and Consul Connect best practices
- Follows CLAUDE.md §3 structure and token budgets
