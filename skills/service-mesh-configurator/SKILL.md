---
name: "Service Mesh Configurator"
slug: "service-mesh-configurator"
description: "Configure service mesh (Istio, Linkerd, Consul) with traffic routing, mTLS, observability, and advanced traffic management for microservices."
capabilities:
  - Istio, Linkerd, Consul Connect service mesh configuration
  - VirtualService and DestinationRule traffic routing
  - Mutual TLS (mTLS) encryption for service-to-service communication
  - Circuit breaking and retry policies
  - Traffic splitting for canary deployments
  - Service mesh observability (metrics, tracing, logging)
  - Authorization policies and service-to-service authentication
inputs:
  - mesh_type: "istio, linkerd, consul (string)"
  - services: "array of service names requiring mesh configuration (array)"
  - traffic_management: "canary, blue-green, mirroring, fault-injection (string, optional)"
  - mtls_mode: "strict, permissive, disabled (string, default: strict)"
  - observability_enabled: "enable distributed tracing and metrics (boolean, default: true)"
  - authorization_required: "enable service-to-service authz (boolean, default: false)"
outputs:
  - mesh_config: "service mesh installation and configuration"
  - traffic_rules: "VirtualService, DestinationRule, or equivalent configs"
  - security_config: "mTLS, AuthorizationPolicy, and certificate configs"
  - observability_config: "distributed tracing and metrics collection setup"
keywords:
  - service-mesh
  - istio
  - linkerd
  - consul
  - mtls
  - traffic-management
  - canary-deployment
  - circuit-breaker
  - distributed-tracing
  - microservices
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://istio.io/latest/docs/
  - https://linkerd.io/2/reference/
  - https://www.consul.io/docs/connect
  - https://istio.io/latest/docs/concepts/traffic-management/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Microservices architecture requiring service-to-service communication security
- Need for advanced traffic management (canary, blue/green, A/B testing)
- Distributed tracing and observability across multiple services
- Circuit breaking and fault tolerance for resilient microservices
- Zero-trust networking with mTLS encryption
- Traffic mirroring for testing in production

**Not for:**
- Simple Kubernetes deployments with <5 services (use kubernetes-manifest-generator)
- Serverless architectures (use serverless-deployment-designer)
- Complete cloud-native orchestration (use cloud-native-orchestrator agent)
- Service mesh installation on clusters (focuses on configuration, not installation)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `mesh_type` must be: istio, linkerd, or consul
- `services` array must contain at least 2 services
- `mtls_mode` must be: strict, permissive, or disabled
- `traffic_management` if specified must be: canary, blue-green, mirroring, or fault-injection

**Source freshness:**
- Istio Traffic Management (accessed 2025-10-26T01:33:54-04:00): https://istio.io/latest/docs/concepts/traffic-management/
- Istio Security (accessed 2025-10-26T01:33:54-04:00): https://istio.io/latest/docs/concepts/security/
- Linkerd Documentation (accessed 2025-10-26T01:33:54-04:00): https://linkerd.io/2/reference/
- Consul Connect (accessed 2025-10-26T01:33:54-04:00): https://www.consul.io/docs/connect

**Decision thresholds:**
- T1 for basic mesh sidecar injection and mTLS configuration
- T2 for advanced traffic management, circuit breaking, and observability

---

## Procedure

### T1: Basic Mesh Configuration (≤2k tokens)

**Step 1: Enable service mesh sidecar injection**
- Configure namespace label for automatic sidecar injection
- Generate sidecar proxy annotations for services
- Set mTLS mode (strict or permissive)

**Step 2: Create basic traffic routing**
- Generate VirtualService for HTTP routing (Istio) or ServiceProfile (Linkerd)
- Configure DestinationRule for load balancing
- Enable mTLS peer authentication

**Output:**
- Namespace configuration with sidecar injection
- Basic VirtualService and DestinationRule configs
- mTLS PeerAuthentication policy

**Abort conditions:**
- Service mesh not installed on cluster (pre-requisite check)
- Services missing required labels or ports

---

### T2: Advanced Traffic Management (≤6k tokens)

**All T1 steps plus:**

**Step 1: Traffic splitting and canary deployment**
- Configure weighted traffic routing (90% stable, 10% canary)
- Add traffic mirroring for shadow testing
- Implement header-based routing for A/B testing

**Step 2: Resilience patterns**
- Configure circuit breaker with outlier detection
- Add retry policies with exponential backoff
- Set timeout policies for requests
- Configure fault injection for chaos testing

**Step 3: Authorization and security**
- Create AuthorizationPolicy for service-to-service access control
- Define RequestAuthentication for JWT validation
- Configure namespace-level security policies

**Step 4: Observability integration**
- Enable distributed tracing (Jaeger, Tempo)
- Configure Prometheus metrics scraping
- Add Grafana dashboards for service mesh metrics
- Define telemetry filters and sampling rates

**Output:**
- Complete traffic management configurations
- Circuit breaker and retry policies
- Authorization and authentication policies
- Observability stack integration configs

**Abort conditions:**
- Conflicting traffic rules (multiple VirtualServices for same host)
- mTLS configuration incompatible with legacy services
- Authorization policies block critical service communication

---

### T3: Production-Grade Mesh (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Multi-cluster mesh**
- Configure service mesh federation across clusters
- Set up cross-cluster service discovery
- Implement multi-cluster mTLS trust domain

**Step 2: Advanced security**
- Configure certificate rotation policies
- Implement egress gateway for external traffic control
- Add WASM filters for custom security policies

**Step 3: Performance optimization**
- Tune sidecar resource limits
- Configure request batching and connection pooling
- Optimize telemetry sampling for high-throughput services

**Output:**
- Multi-cluster mesh configuration
- Advanced security policies with egress control
- Performance-tuned mesh settings
- Complete observability and SLO monitoring

---

## Decision Rules

**Mesh type selection:**
- **Istio**: Feature-rich, complex traffic management, large microservice environments (>10 services)
- **Linkerd**: Lightweight, simple, lower resource overhead, moderate microservice count (5-20 services)
- **Consul Connect**: HashiCorp ecosystem integration, multi-datacenter, hybrid cloud

**mTLS mode:**
- **Strict**: Production environments, zero-trust requirement, all services mesh-enabled
- **Permissive**: Migration phase, mixed mesh and non-mesh workloads
- **Disabled**: Development/testing only, not recommended for production

**Traffic management strategy:**
- **Canary**: Progressive rollout with metrics-based promotion (5% → 25% → 50% → 100%)
- **Blue/Green**: Instant traffic switch between versions, easy rollback
- **Mirroring**: Test new version with production traffic without affecting users
- **Fault Injection**: Chaos engineering, test resilience with deliberate failures

**Circuit breaker thresholds:**
- **Consecutive errors**: 5 errors trigger open circuit
- **Base ejection time**: 30 seconds minimum before retry
- **Max ejection percentage**: 50% of instances to maintain availability

**Ambiguity handling:**
- If mesh_type not specified → recommend Linkerd for simplicity, Istio for advanced features
- If traffic_management unclear → request deployment strategy and rollback requirements
- If services list incomplete → scan cluster for services with mesh-compatible labels

---

## Output Contract

**Required fields (all tiers):**
```yaml
mesh_config:
  namespace_labels:
    istio-injection: enabled  # or linkerd.io/inject: enabled
  mtls_mode: "strict | permissive | disabled"

traffic_rules:
  virtual_service: "VirtualService YAML (Istio) or ServiceProfile (Linkerd)"
  destination_rule: "DestinationRule YAML with load balancing"

security_config:
  peer_authentication: "PeerAuthentication YAML for mTLS"
  certificates: "certificate management configuration"
```

**Additional T2 fields:**
```yaml
advanced_traffic:
  canary_config:
    stable_weight: integer
    canary_weight: integer
  circuit_breaker:
    consecutive_errors: integer
    interval: "duration"
    base_ejection_time: "duration"
  retry_policy:
    attempts: integer
    per_try_timeout: "duration"
    retry_on: "5xx,gateway-error,reset,connect-failure"

authorization:
  authorization_policy: "AuthorizationPolicy YAML"
  request_authentication: "RequestAuthentication YAML for JWT"

observability:
  distributed_tracing:
    enabled: boolean
    sampling_rate: float
    backend: "jaeger | tempo | zipkin"
  metrics:
    prometheus_scrape: boolean
    custom_metrics: ["array of metric names"]
  dashboards:
    grafana_dashboards: ["array of dashboard URLs"]
```

**Additional T3 fields:**
```yaml
multi_cluster:
  trust_domain: "cluster.local"
  cluster_federation: "multi-cluster mesh configuration"

egress_control:
  egress_gateway: "Gateway YAML for external traffic"
  service_entry: "ServiceEntry for external services"

performance_tuning:
  sidecar_resources:
    cpu_request: "100m"
    memory_request: "128Mi"
  telemetry_optimization:
    sampling_rate: 0.01
    batch_size: integer
```

---

## Examples

```yaml
# T1 Example: Istio VirtualService and DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 100
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
  subsets:
  - name: v1
    labels:
      version: v1
```

```yaml
# T2 Example: Circuit Breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-circuit-breaker
spec:
  host: api-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic mesh injection, mTLS, simple routing
- **T2**: ≤6,000 tokens - advanced traffic management, circuit breaking, authz, observability
- **T3**: ≤12,000 tokens - multi-cluster, egress control, performance tuning

**Safety checks:**
- mTLS enabled for production workloads (strict mode)
- Authorization policies prevent unauthorized service access
- Circuit breakers prevent cascading failures
- Retry policies include timeout limits to prevent retry storms

**Auditability:**
- All mesh configs specify API versions (networking.istio.io/v1beta1)
- Traffic rules cite official service mesh documentation
- mTLS mode selection includes security justification
- Circuit breaker thresholds based on documented best practices

**Determinism:**
- Same inputs produce identical mesh configurations
- Traffic weights are deterministic (no randomization without explicit config)
- Load balancing algorithms are explicitly specified

**Validation requirements:**
- All Istio configs pass `istioctl analyze` validation
- Linkerd configs validate with `linkerd check`
- T2+ configs include observability integration validation

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- Istio Concepts: https://istio.io/latest/docs/concepts/
- Istio Traffic Management: https://istio.io/latest/docs/concepts/traffic-management/
- Istio Security: https://istio.io/latest/docs/concepts/security/
- Istio Observability: https://istio.io/latest/docs/concepts/observability/
- Linkerd Architecture: https://linkerd.io/2/reference/architecture/
- Linkerd Traffic Splitting: https://linkerd.io/2/features/traffic-split/
- Consul Connect: https://www.consul.io/docs/connect

**Best Practices:**
- Istio Best Practices: https://istio.io/latest/docs/ops/best-practices/
- Linkerd Best Practices: https://linkerd.io/2/tasks/books/
- Service Mesh Comparison: https://servicemesh.es/

**Observability Integration:**
- Istio with Jaeger: https://istio.io/latest/docs/tasks/observability/distributed-tracing/jaeger/
- Istio with Prometheus: https://istio.io/latest/docs/ops/integrations/prometheus/
- Linkerd with Grafana: https://linkerd.io/2/tasks/grafana/

**Advanced Patterns:**
- Canary Deployments with Flagger: https://docs.flagger.app/
- Multi-cluster Istio: https://istio.io/latest/docs/setup/install/multicluster/
