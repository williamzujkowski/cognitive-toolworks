---
name: "Cloud-Native Deployment Orchestrator"
slug: "cloud-native-deployment-orchestrator"
description: "Design and validate Kubernetes, container, serverless, and service mesh deployments with platform-specific optimizations for AWS, Azure, and GCP."
capabilities:
  - Kubernetes manifest generation and validation with best practices
  - Docker containerization strategy and multi-stage build optimization
  - Serverless deployment patterns (AWS Lambda, Azure Functions, Cloud Functions)
  - Service mesh configuration (Istio, Linkerd, Consul)
  - Helm chart creation and templating
  - Cloud platform integration (EKS, AKS, GKE)
  - Container security scanning and hardening
  - Deployment strategy design (blue/green, canary, rolling)
  - Resource optimization and autoscaling configuration
  - Multi-cloud deployment orchestration
inputs:
  - application_type: "monolith, microservices, batch, event-driven (string)"
  - target_platform: "kubernetes, serverless, hybrid (string)"
  - cloud_provider: "aws, azure, gcp, multi-cloud (string, optional)"
  - deployment_tier: "T1 (quick) | T2 (extended) | T3 (production-ready) (string, default: T1)"
  - requirements: "performance, security, cost constraints (object)"
  - existing_infrastructure: "description of current state (string, optional)"
outputs:
  - deployment_manifests: "K8s YAML, Dockerfiles, Helm charts, or serverless configs"
  - architecture_diagram: "Deployment architecture description with components"
  - security_config: "Network policies, RBAC, secrets management configuration"
  - ci_cd_integration: "Pipeline configuration snippets"
  - cost_estimate: "Resource sizing and estimated monthly costs"
  - migration_plan: "Step-by-step deployment/migration guide (T3 only)"
keywords:
  - kubernetes
  - docker
  - containers
  - serverless
  - service-mesh
  - helm
  - cloud-native
  - eks
  - aks
  - gke
  - istio
  - deployment
  - orchestration
  - cncf
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://kubernetes.io/docs/home/
  - https://docs.docker.com/develop/dev-best-practices/
  - https://helm.sh/docs/
  - https://istio.io/latest/docs/
  - https://www.cncf.io/projects/
  - https://aws.amazon.com/eks/
  - https://azure.microsoft.com/en-us/products/kubernetes-service
  - https://cloud.google.com/kubernetes-engine
---

## Purpose & When-To-Use

**Trigger conditions:**
- Microservice application requires cloud-native deployment strategy
- Containerization of legacy application for cloud migration
- Kubernetes adoption decision and implementation planning
- Multi-cloud or hybrid cloud deployment requirements
- Service mesh evaluation and implementation for microservices
- Serverless vs container orchestration architecture decision
- Production-grade deployment with security, scalability, and observability
- CI/CD pipeline integration for cloud-native applications
- Cost optimization of cloud-native infrastructure

**Not for:**
- Simple static website hosting (use CDN/object storage)
- Single VM deployment (use traditional IaaS)
- Legacy application without containerization readiness assessment
- Bare-metal Kubernetes cluster installation (focuses on managed services)
- Application code development (focuses on deployment infrastructure)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `application_type` must be one of: monolith, microservices, batch, event-driven
- `target_platform` must be: kubernetes, serverless, or hybrid
- `cloud_provider` if specified must be: aws, azure, gcp, or multi-cloud
- `deployment_tier` must be: T1, T2, or T3
- `requirements` must include at least one of: performance, security, cost
- `existing_infrastructure` if provided must describe current deployment state

**Source freshness:**
- Kubernetes Documentation (accessed 2025-10-25T21:30:36-04:00): https://kubernetes.io/docs/home/ - verify v1.28+ content
- Docker Best Practices (accessed 2025-10-25T21:30:36-04:00): https://docs.docker.com/develop/dev-best-practices/
- CNCF Landscape (accessed 2025-10-25T21:30:36-04:00): https://www.cncf.io/projects/ - verify project maturity levels
- Helm Documentation (accessed 2025-10-25T21:30:36-04:00): https://helm.sh/docs/ - verify Helm 3.x best practices
- Istio Service Mesh (accessed 2025-10-25T21:30:36-04:00): https://istio.io/latest/docs/ - verify ambient mesh features
- AWS EKS Best Practices (accessed 2025-10-25T21:30:36-04:00): https://aws.github.io/aws-eks-best-practices/
- Azure AKS Best Practices (accessed 2025-10-25T21:30:36-04:00): https://learn.microsoft.com/en-us/azure/aks/best-practices
- GCP GKE Best Practices (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/kubernetes-engine/docs/best-practices

**Decision thresholds:**
- Serverless recommended if: stateless, event-driven, variable load, execution time <15min
- Kubernetes recommended if: stateful, persistent connections, complex orchestration, multi-service
- Service mesh recommended if: >5 microservices, complex routing, distributed tracing required

---

## Procedure

### T1: Quick Deployment Pattern (≤2k tokens)

**Fast path for 80% of deployment recommendations:**

1. **Application analysis:**
   - Classify workload type: stateless/stateful, synchronous/asynchronous
   - Identify scaling requirements: fixed, predictable, variable, burst
   - Determine state management needs: ephemeral, persistent, distributed

2. **Platform recommendation:**
   - **Serverless** if: event-driven, stateless, <15min execution, cost-sensitive
   - **Kubernetes** if: stateful, long-running, complex dependencies, multi-service
   - **Hybrid** if: mixed workload types (use K8s for core, serverless for workers)

3. **Quick start configuration:**
   - Generate minimal viable Dockerfile with multi-stage build
   - Provide basic K8s Deployment + Service YAML or serverless function config
   - Include resource requests/limits based on application type
   - Add health check endpoints (liveness/readiness for K8s)

4. **Output (T1):**
   - Recommended platform with justification
   - Basic deployment manifest (≤30 lines)
   - Resource sizing estimate (CPU/memory)
   - Next steps for T2/T3 hardening

**Abort conditions:**
- Application type is unclear or requires profiling
- Conflicting requirements (e.g., "serverless + stateful database")
- Cloud provider not specified but required for cost estimation

---

### T2: Extended Deployment Design (≤6k tokens)

**For deployments requiring platform-specific optimization:**

1. **All T1 steps** plus:

2. **Platform-specific deep dive:**

   **If Kubernetes:**
   - Generate complete manifests: Deployment, Service, ConfigMap, Secret
   - Add NetworkPolicy for pod-to-pod security
   - Configure HorizontalPodAutoscaler (HPA) with target metrics
   - Include Ingress resource with TLS termination
   - Add PersistentVolumeClaim for stateful workloads
   - Apply pod security standards (restricted profile)

   **If Serverless:**
   - Design event sources and triggers
   - Configure IAM roles with least privilege (AWS) or managed identities (Azure)
   - Set concurrency limits and reserved capacity
   - Add dead-letter queues for failure handling
   - Configure VPC integration for private resources
   - Optimize cold start (language runtime, package size)

   **If Service Mesh (Istio/Linkerd):**
   - Configure VirtualService for traffic routing
   - Add DestinationRule for load balancing and circuit breaking
   - Define AuthorizationPolicy for service-to-service auth
   - Configure mTLS for encrypted service communication
   - Add observability: distributed tracing, metrics collection

3. **Cloud provider integration:**
   - **AWS**: EKS with managed node groups, ALB Ingress Controller, ECR for images
   - **Azure**: AKS with Azure CNI, Application Gateway Ingress, ACR for images
   - **GCP**: GKE Autopilot/Standard, Cloud Load Balancing, Artifact Registry

4. **Helm chart generation (if Kubernetes):**
   - Create Chart.yaml with dependencies
   - Parameterize values.yaml for environment-specific overrides
   - Template manifests with conditional logic
   - Include hooks for pre/post-deployment tasks

5. **Security hardening:**
   - Non-root user in Dockerfile
   - Read-only root filesystem where applicable
   - Drop unnecessary Linux capabilities
   - Scan images for vulnerabilities (reference tools: Trivy, Grype)
   - Secrets management via cloud provider secret stores

6. **Output (T2):**
   - Complete deployment manifests or Helm chart
   - Security configuration (RBAC, NetworkPolicy, IAM)
   - Autoscaling configuration with thresholds
   - Monitoring integration (Prometheus metrics, CloudWatch)
   - Platform-specific cost estimate with instance types

**Abort conditions:**
- Requires custom Kubernetes operators or CRDs (recommend specialist)
- Compliance requirements (HIPAA, PCI-DSS) needing audit trail (escalate to T3)
- Complex stateful migration requiring data replication strategy

---

### T3: Production-Ready Deployment (≤12k tokens)

**For production deployments requiring comprehensive security, observability, and resilience:**

1. **All T1 + T2 steps** plus:

2. **Advanced deployment strategies:**
   - **Blue/Green**: Dual environment setup with traffic switch mechanism
   - **Canary**: Progressive rollout with metrics-based promotion (Flagger, Argo Rollouts)
   - **Rolling Update**: Configure maxSurge/maxUnavailable for zero-downtime
   - **Shadow Traffic**: Mirror production traffic to new version for validation

3. **Comprehensive security:**
   - **Network security**: Implement network policies with default-deny + allowlist
   - **Pod security**: Enforce Pod Security Standards (PSS) at namespace level
   - **Image security**: Sign images with Sigstore/Cosign, verify signatures at admission
   - **Runtime security**: Integrate Falco or similar for runtime threat detection
   - **Secret management**: Use External Secrets Operator with cloud provider vaults
   - **RBAC**: Least-privilege service accounts with namespace isolation
   - **Admission control**: Implement OPA Gatekeeper policies or Kyverno

4. **Observability stack:**
   - **Metrics**: Prometheus scraping, ServiceMonitor CRDs, custom metrics for HPA
   - **Logging**: Structured logging with log aggregation (EFK/Loki)
   - **Tracing**: OpenTelemetry instrumentation with Jaeger/Tempo backend
   - **Dashboards**: Grafana dashboards for RED metrics (Rate, Errors, Duration)
   - **Alerting**: PrometheusRules for SLO-based alerts

5. **Resilience patterns:**
   - **Circuit breaker**: Service mesh or application-level (Envoy, Resilience4j)
   - **Retry logic**: Exponential backoff with jitter
   - **Timeout policies**: Request timeouts at ingress and service mesh
   - **Rate limiting**: API gateway or service mesh rate limiting
   - **Pod disruption budgets**: Ensure minimum available replicas during maintenance
   - **Multi-AZ/multi-region**: Topology spread constraints for high availability

6. **GitOps integration:**
   - Structure manifests for ArgoCD/Flux deployment
   - Implement Kustomize overlays for dev/staging/prod
   - Define promotion workflow between environments
   - Add health checks and sync policies

7. **Cost optimization:**
   - **Right-sizing**: Analyze resource usage, recommend VPA (Vertical Pod Autoscaler)
   - **Spot instances**: Configure node affinity for fault-tolerant workloads
   - **Cluster autoscaling**: Configure cluster-autoscaler or Karpenter (AWS)
   - **Resource quotas**: Namespace-level limits to prevent over-provisioning
   - **Reserved capacity**: Analyze steady-state usage for committed use discounts

8. **Migration strategy (if existing infrastructure):**
   - **Phase 1**: Containerize application, validate locally
   - **Phase 2**: Deploy to dev/staging cluster, integration testing
   - **Phase 3**: Canary production traffic (5% → 25% → 50% → 100%)
   - **Phase 4**: Monitor SLOs, rollback procedure if degradation
   - **Phase 5**: Decommission legacy infrastructure

9. **Disaster recovery:**
   - **Backup strategy**: Velero for cluster state and persistent volumes
   - **RTO/RPO targets**: Define and validate recovery time/point objectives
   - **Failover testing**: Chaos engineering experiments (Pod failure, AZ failure)
   - **Documentation**: Runbooks for common failure scenarios

10. **Compliance and governance:**
    - **Audit logging**: Enable API server audit logs, CloudTrail/Activity Log
    - **Policy enforcement**: Network policies, admission policies, image policies
    - **Compliance mapping**: Map controls to CIS Kubernetes Benchmark
    - **SBOM generation**: Generate Software Bill of Materials for supply chain security

11. **Output (T3):**
    - Complete production-ready manifest repository structure
    - Multi-environment Helm charts or Kustomize overlays
    - GitOps workflow configuration (ArgoCD/Flux)
    - Security hardening checklist with validation steps
    - Observability stack integration (dashboards, alerts, SLOs)
    - Deployment strategy with rollback procedures
    - Cost analysis with optimization recommendations
    - Migration plan with timeline and risk mitigation
    - Disaster recovery runbook
    - Compliance documentation mapping

**Abort conditions:**
- Requires regulatory approval (legal/compliance team review)
- Custom hardware acceleration (GPU, FPGA) needing specialized node pools
- Highly regulated data residency requirements needing legal review

---

## Decision Rules

**Platform selection:**
- **Serverless** if all of:
  - Stateless or state externalized (DynamoDB, S3, etc.)
  - Execution time <15 minutes
  - Event-driven or HTTP triggered
  - Variable/unpredictable load patterns
  - Cost-sensitivity prioritized over cold start latency

- **Kubernetes** if any of:
  - Stateful applications (databases, message queues)
  - Long-running processes or persistent connections
  - Complex multi-service orchestration
  - Requires advanced networking (service mesh)
  - Need for fine-grained resource control

- **Hybrid** if:
  - Core services require state/persistence (K8s)
  - Worker processes are event-driven (serverless)
  - Cost optimization via workload placement

**Service mesh adoption:**
- **Required** if:
  - >10 microservices with complex routing needs
  - mTLS encryption mandatory for compliance
  - Advanced traffic management (A/B testing, canary)
  - Distributed tracing required across services

- **Optional** if:
  - <10 microservices with simple routing
  - Can achieve requirements with Ingress + NetworkPolicy
  - Team lacks service mesh operational expertise

**Cloud provider selection:**
- **AWS** if: existing AWS footprint, Lambda ecosystem integration, EKS maturity
- **Azure** if: existing Azure/Microsoft ecosystem, enterprise agreements, AKS features
- **GCP** if: GKE Autopilot simplicity, BigQuery/ML integration, Google Cloud native
- **Multi-cloud** if: vendor lock-in avoidance, disaster recovery across clouds, data residency

**Ambiguity handling:**
- If application type unclear → request architecture diagram or component inventory
- If scaling requirements unknown → recommend T1 baseline, plan for T2 iteration
- If budget constraints conflict with requirements → present trade-off matrix with options

**Stop conditions:**
- Lack of application architecture documentation (T2+ requires this)
- Conflicting non-functional requirements (e.g., "lowest cost + highest availability")
- Regulatory compliance requirements without defined controls

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "deployment_recommendation": {
    "platform": "kubernetes | serverless | hybrid",
    "cloud_provider": "aws | azure | gcp | multi-cloud",
    "rationale": "explanation of platform choice"
  },
  "manifests": {
    "type": "dockerfile | kubernetes | helm | serverless",
    "files": [
      {
        "filename": "string",
        "content": "string (YAML or Dockerfile)",
        "description": "purpose of this file"
      }
    ]
  },
  "resource_sizing": {
    "cpu": "string (e.g., 500m, 2 vCPU)",
    "memory": "string (e.g., 512Mi, 2Gi)",
    "storage": "string (e.g., 10Gi, S3 bucket)",
    "estimated_monthly_cost_usd": "number (approximate)"
  },
  "next_steps": ["array of actionable recommendations"]
}
```

**Additional T2 fields:**
```json
{
  "security_config": {
    "rbac": "Kubernetes RBAC manifests or IAM policies",
    "network_policies": "NetworkPolicy YAML or security groups",
    "secrets_management": "approach and tool recommendation"
  },
  "autoscaling": {
    "type": "HPA | VPA | cluster-autoscaler | Lambda concurrency",
    "metrics": "CPU, memory, custom metrics",
    "thresholds": "scale up/down triggers"
  },
  "monitoring": {
    "metrics_endpoint": "Prometheus /metrics or CloudWatch namespace",
    "recommended_alerts": ["array of SLO-based alerts"]
  }
}
```

**Additional T3 fields:**
```json
{
  "deployment_strategy": {
    "type": "blue-green | canary | rolling",
    "configuration": "detailed rollout configuration",
    "rollback_procedure": "step-by-step rollback instructions"
  },
  "observability": {
    "metrics": "Prometheus configuration",
    "logging": "log aggregation setup",
    "tracing": "OpenTelemetry configuration",
    "dashboards": "Grafana dashboard JSON or links"
  },
  "disaster_recovery": {
    "backup_strategy": "Velero configuration or snapshot policies",
    "rto_rpo": "Recovery time/point objectives",
    "failover_procedure": "detailed failover runbook"
  },
  "migration_plan": {
    "phases": [
      {
        "phase_number": "integer",
        "description": "string",
        "duration": "string",
        "success_criteria": ["array of validation steps"]
      }
    ]
  },
  "compliance": {
    "frameworks": ["CIS Kubernetes Benchmark", "etc."],
    "controls_implemented": ["array of security controls"],
    "audit_logs": "configuration for audit logging"
  }
}
```

---

## Examples

```yaml
# T1 Example: Basic Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: myregistry/api:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests: {cpu: 250m, memory: 512Mi}
          limits: {cpu: 500m, memory: 1Gi}
        livenessProbe:
          httpGet: {path: /health, port: 8080}
          initialDelaySeconds: 30
        readinessProbe:
          httpGet: {path: /ready, port: 8080}
```

(Full T2/T3 examples: `/resources/k8s-complete-example.yaml`, `/resources/helm-chart-template/`)

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - platform recommendation + basic manifest
- **T2**: ≤6,000 tokens - platform-specific optimization + security + Helm
- **T3**: ≤12,000 tokens - production-ready with observability + DR + migration

**Safety checks:**
- No hardcoded secrets in manifests (use placeholders or references)
- No privileged containers unless explicitly justified
- Resource limits defined for all containers
- Health checks defined for production deployments (T2+)
- Network policies enforce least-privilege communication (T2+)

**Auditability:**
- All cloud provider recommendations cite official documentation with access date
- Kubernetes API versions specified (apps/v1, networking.k8s.io/v1, etc.)
- Security controls mapped to CIS Kubernetes Benchmark sections (T3)
- Cost estimates include methodology (instance type, hours/month, etc.)

**Determinism:**
- Given same inputs, produce identical platform recommendation
- Manifest structure follows community conventions (Helm chart structure, K8s best practices)
- Security configurations based on documented standards, not heuristics

**Validation requirements:**
- T2+ manifests must pass `kubectl apply --dry-run=client` validation
- Helm charts must pass `helm lint` without errors
- Serverless configs must validate against cloud provider schema (SAM, Terraform)

---

## Resources

**Official Documentation (accessed 2025-10-25T21:30:36-04:00):**
- Kubernetes Concepts: https://kubernetes.io/docs/concepts/
- Kubernetes Best Practices: https://kubernetes.io/docs/concepts/configuration/overview/
- Docker Multi-Stage Builds: https://docs.docker.com/build/building/multi-stage/
- Helm Chart Best Practices: https://helm.sh/docs/chart_best_practices/
- Istio Traffic Management: https://istio.io/latest/docs/concepts/traffic-management/
- Linkerd Architecture: https://linkerd.io/2/reference/architecture/

**Cloud Provider Resources:**
- AWS EKS Best Practices Guide: https://aws.github.io/aws-eks-best-practices/
- Azure AKS Baseline Architecture: https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks
- GCP GKE Security Hardening Guide: https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster
- AWS Lambda Best Practices: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html

**CNCF Ecosystem:**
- CNCF Cloud Native Trail Map: https://github.com/cncf/trailmap
- CNCF Landscape: https://landscape.cncf.io/
- Prometheus Operator: https://prometheus-operator.dev/
- Argo CD Documentation: https://argo-cd.readthedocs.io/

**Security Standards:**
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes
- NSA Kubernetes Hardening Guide: https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF
- OWASP Kubernetes Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html

**Example Manifest Libraries:**
- `/resources/dockerfile-multi-stage.example` - Optimized multi-stage Dockerfile
- `/resources/k8s-complete-example.yaml` - Full K8s stack with security
- `/resources/helm-chart-template/` - Production Helm chart structure
- `/resources/istio-traffic-management.yaml` - Service mesh configuration
- `/resources/argocd-application.yaml` - GitOps deployment manifest

**Tools and Validators:**
- Kube-score (manifest validation): https://github.com/zegl/kube-score
- Polaris (best practices audit): https://github.com/FairwindsOps/polaris
- Trivy (image scanning): https://github.com/aquasecurity/trivy
- Checkov (IaC security): https://github.com/bridgecrewio/checkov
