---
name: "Kubernetes Manifest Generator"
slug: "kubernetes-manifest-generator"
description: "Generate and validate Kubernetes YAML manifests with best practices for Deployments, Services, ConfigMaps, and security policies."
capabilities:
  - Kubernetes Deployment and Service manifest generation
  - ConfigMap and Secret manifest creation
  - NetworkPolicy and RBAC configuration
  - Resource requests and limits optimization
  - Health check (liveness/readiness) configuration
  - Pod Security Standards enforcement
inputs:
  - workload_name: "name of the workload (string)"
  - workload_type: "deployment, statefulset, daemonset, job, cronjob (string)"
  - container_image: "container image with tag (string)"
  - port: "exposed container port (integer, optional)"
  - replicas: "number of replicas (integer, default: 3)"
  - resources: "CPU/memory requests and limits (object, optional)"
  - health_checks: "liveness and readiness probe config (object, optional)"
  - security_context: "pod and container security settings (object, optional)"
outputs:
  - kubernetes_manifests: "validated K8s YAML for Deployment and Service"
  - validation_results: "kubectl dry-run validation output"
  - best_practices_report: "compliance with K8s best practices"
keywords:
  - kubernetes
  - yaml
  - deployment
  - service
  - configmap
  - networkpolicy
  - rbac
  - pod-security
  - manifest-generation
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
  - https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
  - https://kubernetes.io/docs/concepts/configuration/overview/
  - https://kubernetes.io/docs/concepts/security/pod-security-standards/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Need to generate Kubernetes Deployment and Service manifests
- Converting application specifications to K8s YAML
- Applying K8s best practices to existing manifests
- Validating manifest syntax and resource configurations
- Creating base manifests for Helm charts or Kustomize overlays

**Not for:**
- Complete production orchestration (use cloud-native-orchestrator agent)
- Helm chart templating with complex logic (use kubernetes-helm-builder skill)
- Service mesh configuration (use kubernetes-servicemesh-configurator skill)
- Multi-cloud deployment strategies (use cloud-native-orchestrator agent)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `workload_name` must be DNS-1123 compliant (lowercase, alphanumeric, hyphens)
- `workload_type` must be one of: deployment, statefulset, daemonset, job, cronjob
- `container_image` must include tag (not :latest for production)
- `replicas` must be ≥1 (≥3 recommended for production)
- `resources.requests` must be ≤ `resources.limits` if both specified

**Source freshness:**
- Kubernetes API Reference (accessed 2025-10-26T01:33:54-04:00): https://kubernetes.io/docs/reference/kubernetes-api/ - verify v1.28+ APIs
- Kubernetes Best Practices (accessed 2025-10-26T01:33:54-04:00): https://kubernetes.io/docs/concepts/configuration/overview/
- Pod Security Standards (accessed 2025-10-26T01:33:54-04:00): https://kubernetes.io/docs/concepts/security/pod-security-standards/

**Decision thresholds:**
- T1 for basic manifests (Deployment + Service only)
- T2 for production configs (add security, network policies, resource optimization)

---

## Procedure

### T1: Basic Manifest Generation (≤2k tokens)

**Step 1: Generate core Kubernetes manifests**
- Create Deployment manifest with specified workload type, image, and replicas
- Add Service manifest if port is specified (ClusterIP by default)
- Include basic resource requests (cpu: 100m, memory: 128Mi) if not specified
- Add standard labels (app, version, component)

**Step 2: Validate and output**
- Return YAML manifests
- Provide kubectl dry-run validation command
- List next steps for T2 hardening

**Abort conditions:**
- Invalid workload_name (contains uppercase or special characters)
- Missing required inputs (workload_type, container_image)

---

### T2: Production-Grade Manifests (≤6k tokens)

**All T1 steps plus:**

**Step 1: Add health checks**
- Configure liveness probe (httpGet, tcpSocket, or exec)
- Configure readiness probe with appropriate initial delays
- Set reasonable timeout and failure thresholds

**Step 2: Apply security hardening**
- Set securityContext: runAsNonRoot, readOnlyRootFilesystem
- Drop unnecessary capabilities (ALL by default, add only required)
- Apply Pod Security Standard: restricted profile
- Create ServiceAccount with least-privilege RBAC

**Step 3: Add resource management**
- Define CPU and memory requests based on workload type
- Set limits (typically 2x requests for burstable QoS)
- Add HorizontalPodAutoscaler for scalable workloads

**Step 4: Network security**
- Generate NetworkPolicy for pod-to-pod communication
- Implement default-deny with explicit allowlist rules

**Step 5: Validate and report**
- Run kubectl dry-run validation
- Check against kube-score or Polaris best practices
- Return compliance report with security posture

**Abort conditions:**
- Conflicting security requirements (e.g., privileged + restricted PSS)
- Missing health check endpoints for critical services

---

### T3: Extended Configuration (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Advanced workload features**
- Add PersistentVolumeClaims for StatefulSets
- Configure affinity rules (podAntiAffinity for HA)
- Set topology spread constraints for multi-AZ
- Define PodDisruptionBudget

**Step 2: Complete GitOps structure**
- Organize manifests for Kustomize base/overlays
- Add namespace and resource quota definitions
- Include monitoring ServiceMonitor CRDs

**Output:**
- Complete manifest directory structure
- Validation results and best practices compliance
- Kustomization.yaml for GitOps workflows

---

## Decision Rules

**Workload type selection:**
- **Deployment**: Stateless applications, horizontal scaling
- **StatefulSet**: Stateful apps needing stable network identity, ordered deployment
- **DaemonSet**: Node-level services (logging, monitoring agents)
- **Job**: One-time batch processing
- **CronJob**: Scheduled batch tasks

**Resource sizing defaults:**
- **Small workload** (APIs, web servers): cpu: 100m-250m, memory: 128Mi-512Mi
- **Medium workload** (data processing): cpu: 500m-1000m, memory: 512Mi-2Gi
- **Large workload** (ML, analytics): cpu: 2000m+, memory: 4Gi+

**Health check defaults:**
- **HTTP services**: httpGet probe on /health or /ready endpoints
- **TCP services**: tcpSocket probe on service port
- **Batch jobs**: No liveness probe, use restartPolicy: OnFailure

**Ambiguity handling:**
- If resource requirements unknown → use small defaults + recommend load testing
- If health check endpoint unknown → request application health endpoint details
- If security context conflicts → apply most restrictive settings and warn

---

## Output Contract

**Required fields (all tiers):**
```yaml
kubernetes_manifests:
  deployment: "Deployment YAML with metadata, spec, containers"
  service: "Service YAML (if port specified)"

validation_results:
  syntax_valid: boolean
  kubectl_dry_run: "command output or error"

best_practices_report:
  checks_passed: integer
  checks_failed: integer
  recommendations: ["array of improvement suggestions"]
```

**Additional T2 fields:**
```yaml
security_config:
  service_account: "ServiceAccount YAML"
  rbac_role: "Role or ClusterRole YAML"
  rbac_binding: "RoleBinding YAML"
  network_policy: "NetworkPolicy YAML"
  pod_security_standard: "restricted | baseline | privileged"

autoscaling:
  hpa: "HorizontalPodAutoscaler YAML (if applicable)"
  metrics: ["cpu", "memory", "custom"]
```

**Additional T3 fields:**
```yaml
advanced_features:
  pvc: "PersistentVolumeClaim YAML (if StatefulSet)"
  pdb: "PodDisruptionBudget YAML"
  affinity_rules: "Pod affinity configuration"

gitops_structure:
  kustomization: "Kustomization.yaml for base"
  namespace: "Namespace YAML with ResourceQuota"
  service_monitor: "Prometheus ServiceMonitor CRD (if applicable)"
```

---

## Examples

```yaml
# T1 Example: Basic Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
  labels:
    app: web-api
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-api
  template:
    metadata:
      labels:
        app: web-api
    spec:
      containers:
      - name: api
        image: myregistry/web-api:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests: {cpu: 100m, memory: 128Mi}
          limits: {cpu: 200m, memory: 256Mi}
```

(Service manifest generated alongside Deployment)

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic Deployment + Service generation
- **T2**: ≤6,000 tokens - production hardening with security and health checks
- **T3**: ≤12,000 tokens - advanced features and GitOps structure

**Safety checks:**
- No privileged containers unless explicitly required
- Resource limits defined for all containers
- SecurityContext enforces non-root user (T2+)
- NetworkPolicies restrict traffic to necessary paths (T2+)

**Auditability:**
- All manifests use explicit API versions (apps/v1, v1, networking.k8s.io/v1)
- Security controls cite Pod Security Standards
- Resource sizing includes rationale

**Determinism:**
- Same inputs produce identical YAML output
- Label conventions follow Kubernetes recommended labels
- Manifest structure follows community best practices

**Validation requirements:**
- All manifests must pass `kubectl apply --dry-run=client -f -`
- T2+ manifests must pass kube-score with score ≥7/10

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- Kubernetes Workload Resources: https://kubernetes.io/docs/concepts/workloads/
- Kubernetes Services: https://kubernetes.io/docs/concepts/services-networking/service/
- Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Health Checks: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
- Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/

**Validation Tools:**
- kube-score: https://github.com/zegl/kube-score
- Polaris: https://github.com/FairwindsOps/polaris
- kubectl dry-run: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-apply-em-

**Best Practices:**
- Configuration Best Practices: https://kubernetes.io/docs/concepts/configuration/overview/
- Recommended Labels: https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/
