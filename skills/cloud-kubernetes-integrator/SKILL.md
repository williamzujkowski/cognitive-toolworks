---
name: "Cloud Platform Integrator"
slug: "cloud-kubernetes-integrator"
description: "Integrate Kubernetes workloads with AWS EKS, Azure AKS, and GCP GKE including IAM, ingress controllers, storage classes, and platform-specific features."
capabilities:
  - EKS, AKS, GKE cluster integration configuration
  - Cloud-native ingress controller setup (ALB, App Gateway, Cloud Load Balancing)
  - IAM roles for service accounts (IRSA, Workload Identity, AAD Pod Identity)
  - Cloud storage class integration (EBS, Azure Disk, Persistent Disk)
  - Autoscaling configuration (Cluster Autoscaler, Karpenter)
  - Cloud-specific monitoring and logging integration
inputs:
  - cloud_provider: "aws, azure, gcp (string)"
  - cluster_name: "Kubernetes cluster name (string)"
  - region: "cloud region (string)"
  - ingress_type: "alb, nginx, traefik, app-gateway, cloud-load-balancer (string, optional)"
  - storage_required: "requires persistent storage (boolean, default: false)"
  - autoscaling_enabled: "enable cluster autoscaling (boolean, default: false)"
outputs:
  - platform_config: "cloud-specific Kubernetes configuration"
  - iam_config: "service account to IAM role bindings"
  - ingress_controller: "ingress controller setup and configuration"
  - storage_classes: "cloud-native storage class definitions"
  - monitoring_integration: "CloudWatch/Azure Monitor/Cloud Logging setup"
keywords:
  - eks
  - aks
  - gke
  - cloud-kubernetes
  - irsa
  - workload-identity
  - alb-controller
  - cluster-autoscaler
  - karpenter
  - cloud-native
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://aws.github.io/aws-eks-best-practices/
  - https://learn.microsoft.com/en-us/azure/aks/best-practices
  - https://cloud.google.com/kubernetes-engine/docs/best-practices
  - https://docs.aws.amazon.com/eks/latest/userguide/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Deploying Kubernetes workloads to managed cloud clusters (EKS, AKS, GKE)
- Integrating cloud IAM with Kubernetes service accounts
- Setting up cloud-native ingress controllers
- Configuring persistent storage with cloud block storage
- Enabling cluster autoscaling for dynamic workloads
- Integrating cloud monitoring and logging services

**Not for:**
- Generic Kubernetes manifest generation (use kubernetes-manifest-generator)
- Helm chart creation (use kubernetes-helm-builder)
- Service mesh configuration (use kubernetes-servicemesh-configurator)
- Serverless deployments (use cloud-serverless-designer)
- Complete orchestration (use cloud-native-orchestrator agent)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `cloud_provider` must be: aws, azure, or gcp
- `cluster_name` must be valid for cloud provider naming rules
- `region` must be valid region for selected cloud provider
- `ingress_type` if specified must match cloud provider capabilities

**Source freshness:**
- AWS EKS Best Practices (accessed 2025-10-26T01:33:54-04:00): https://aws.github.io/aws-eks-best-practices/
- Azure AKS Best Practices (accessed 2025-10-26T01:33:54-04:00): https://learn.microsoft.com/en-us/azure/aks/best-practices
- GCP GKE Best Practices (accessed 2025-10-26T01:33:54-04:00): https://cloud.google.com/kubernetes-engine/docs/best-practices

**Decision thresholds:**
- T1 for basic cloud integration (IAM, storage classes)
- T2 for production integration (ingress, autoscaling, monitoring)

---

## Procedure

### T1: Basic Cloud Integration (≤2k tokens)

**Step 1: Configure IAM for Kubernetes**
- **AWS**: Create IRSA (IAM Roles for Service Accounts) configuration
- **Azure**: Configure AAD Pod Identity or Workload Identity
- **GCP**: Set up Workload Identity binding
- Generate ServiceAccount with cloud IAM annotation

**Step 2: Define storage classes**
- **AWS**: Create StorageClass for gp3 EBS volumes with encryption
- **Azure**: Create StorageClass for Azure Disk (Premium_LRS)
- **GCP**: Create StorageClass for Persistent Disk (pd-ssd)
- Add reclaim policy and volume expansion settings

**Output:**
- Cloud IAM to Kubernetes ServiceAccount binding config
- StorageClass definitions for persistent storage
- Basic integration validation steps

**Abort conditions:**
- Cloud region not supported by cluster
- IAM permissions insufficient for IRSA/Workload Identity setup

---

### T2: Production Cloud Integration (≤6k tokens)

**All T1 steps plus:**

**Step 1: Deploy cloud-native ingress controller**
- **AWS**: Install AWS Load Balancer Controller for ALB/NLB ingress
- **Azure**: Configure Application Gateway Ingress Controller (AGIC)
- **GCP**: Set up GKE Ingress for Cloud Load Balancing
- Configure ingress annotations for SSL, health checks, routing

**Step 2: Enable cluster autoscaling**
- **AWS**: Deploy Cluster Autoscaler or Karpenter for node provisioning
- **Azure**: Configure AKS cluster autoscaler with node pools
- **GCP**: Enable GKE cluster autoscaler with min/max node counts
- Set autoscaling policies based on CPU/memory utilization

**Step 3: Integrate cloud monitoring**
- **AWS**: Configure Container Insights with CloudWatch
- **Azure**: Enable Azure Monitor for containers
- **GCP**: Set up Cloud Logging and Cloud Monitoring
- Add log aggregation and metrics collection configs

**Step 4: Configure container registry integration**
- **AWS**: Set up ECR pull secrets or IRSA for ECR
- **Azure**: Configure ACR integration with AKS
- **GCP**: Enable Artifact Registry with Workload Identity
- Add imagePullSecrets to ServiceAccount

**Step 5: Network policy and security**
- Configure cloud-specific network policies
- Set up VPC/VNet integration for private clusters
- Add security group rules for ingress/egress
- Enable pod security policies (PSPs) or Pod Security Standards

**Output:**
- Complete cloud-native ingress setup
- Cluster autoscaling configuration
- Monitoring and logging integration
- Container registry authentication
- Network and security configurations

**Abort conditions:**
- Ingress controller conflicts with existing setup
- Insufficient cloud quotas for autoscaling
- Network policy conflicts with cloud VPC rules

---

### T3: Advanced Cloud Platform Features (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Multi-AZ and high availability**
- Configure node pools across availability zones
- Set topology spread constraints for pod distribution
- Add pod disruption budgets for maintenance

**Step 2: Advanced autoscaling**
- Configure custom metrics autoscaling (KEDA)
- Set up predictive autoscaling based on schedules
- Add spot/preemptible instance integration

**Step 3: Disaster recovery and backup**
- Configure Velero with cloud storage backend
- Set up cross-region cluster federation
- Add automated backup schedules

**Output:**
- Multi-AZ HA configuration
- Advanced autoscaling with custom metrics
- Disaster recovery and backup setup

---

## Decision Rules

**Cloud provider-specific features:**
- **AWS EKS**: IRSA for IAM, ALB Controller, Karpenter for autoscaling, EBS CSI driver
- **Azure AKS**: Workload Identity, AGIC, Virtual nodes, Azure Monitor
- **GCP GKE**: Workload Identity, GKE Ingress, Autopilot mode, Cloud Logging native

**Ingress controller selection:**
- **AWS ALB**: Native AWS integration, Layer 7 load balancing, WAF integration
- **Azure App Gateway**: Azure-native, WAF, SSL offload
- **GCP GKE Ingress**: Cloud Load Balancing, global load balancing, CDN integration
- **NGINX/Traefik**: Cloud-agnostic, advanced routing, middleware support

**Storage class types:**
- **AWS**: gp3 (general purpose SSD), io2 (high IOPS), efs (shared filesystem)
- **Azure**: Premium_LRS (SSD), Standard_LRS (HDD), Azure Files (shared)
- **GCP**: pd-ssd (SSD), pd-standard (HDD), Filestore (shared NFS)

**Autoscaling strategy:**
- **Cluster Autoscaler**: Standard, multi-cloud compatible
- **Karpenter (AWS)**: Fast, bin-packing optimization, spot instances
- **GKE Autopilot**: Fully managed, pay-per-pod
- **AKS Virtual Nodes**: Serverless node pool with ACI

**Ambiguity handling:**
- If ingress_type not specified → use cloud-native option (ALB, AGIC, GKE Ingress)
- If storage_required unclear → ask about stateful application needs
- If autoscaling_enabled unclear → recommend based on workload variability

---

## Output Contract

**Required fields (all tiers):**
```yaml
iam_config:
  platform: "aws-irsa | azure-workload-identity | gcp-workload-identity"
  service_account:
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: "app-sa"
      annotations:
        cloud_annotation: "arn:aws:iam::xxx | azure_client_id | gcp_sa_email"
  iam_policy: "cloud IAM policy or role definition"

storage_classes:
  - name: "cloud-storage"
    provisioner: "cloud-specific CSI driver"
    parameters:
      type: "gp3 | Premium_LRS | pd-ssd"
      encrypted: "true"
    reclaimPolicy: "Retain | Delete"
    allowVolumeExpansion: true
```

**Additional T2 fields:**
```yaml
ingress_controller:
  type: "alb | app-gateway | gke-ingress | nginx"
  installation: "Helm chart or manifest YAML"
  configuration: "controller-specific settings"
  ingress_class: "IngressClass resource YAML"

autoscaling:
  type: "cluster-autoscaler | karpenter | aks-autoscaler | gke-autoscaler"
  configuration: "autoscaler deployment or managed config"
  scaling_policies:
    min_nodes: integer
    max_nodes: integer
    target_cpu_utilization: integer

monitoring:
  platform: "cloudwatch | azure-monitor | cloud-logging"
  configuration: "monitoring agent DaemonSet or managed config"
  log_aggregation: "FluentBit/Fluentd configuration"
  metrics_collection: "Prometheus scraping or cloud metrics"

registry_auth:
  method: "irsa | workload-identity | image-pull-secret"
  configuration: "registry authentication setup"
```

**Additional T3 fields:**
```yaml
high_availability:
  multi_az: boolean
  topology_spread_constraints: "pod topology config"
  pod_disruption_budgets: "PDB YAML"

advanced_autoscaling:
  keda_scalers: ["custom metric scalers"]
  predictive_scaling: "schedule-based scaling rules"
  spot_instances:
    enabled: boolean
    fallback_to_on_demand: boolean

disaster_recovery:
  velero_config: "Velero installation with cloud storage"
  backup_schedule: "cron schedule for backups"
  cross_region_replication: boolean
```

---

## Examples

```yaml
# T1 Example: AWS IRSA ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/app-role
```

```yaml
# T1 Example: AWS EBS StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
  iops: "3000"
  throughput: "125"
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

```yaml
# T2 Example: AWS ALB Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:...
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic IAM and storage integration
- **T2**: ≤6,000 tokens - ingress, autoscaling, monitoring, registry auth
- **T3**: ≤12,000 tokens - HA, advanced autoscaling, disaster recovery

**Safety checks:**
- IAM policies follow least-privilege principle
- Storage encryption enabled by default
- Ingress configured with HTTPS/TLS (production)
- Network policies restrict unnecessary traffic

**Auditability:**
- All cloud resources cite official cloud provider documentation
- IAM role ARNs/IDs explicitly specified
- Storage classes specify encryption and reclaim policies
- Autoscaling policies include min/max node constraints

**Determinism:**
- Same inputs produce identical cloud integration configs
- Storage class parameters are explicit (not cloud defaults)
- IAM annotations use consistent format

**Validation requirements:**
- Cloud IAM configs validate against cloud provider schemas
- StorageClass manifests validate with kubectl
- Ingress resources validate against Kubernetes API
- T2+ configs include cost estimate for cloud resources

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- AWS EKS User Guide: https://docs.aws.amazon.com/eks/latest/userguide/
- AWS EKS Best Practices: https://aws.github.io/aws-eks-best-practices/
- AWS Load Balancer Controller: https://kubernetes-sigs.github.io/aws-load-balancer-controller/
- Azure AKS Documentation: https://learn.microsoft.com/en-us/azure/aks/
- Azure AKS Best Practices: https://learn.microsoft.com/en-us/azure/aks/best-practices
- GCP GKE Documentation: https://cloud.google.com/kubernetes-engine/docs
- GCP GKE Best Practices: https://cloud.google.com/kubernetes-engine/docs/best-practices

**IAM and Identity:**
- AWS IRSA: https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
- Azure Workload Identity: https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview
- GCP Workload Identity: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity

**Storage and Networking:**
- AWS EBS CSI Driver: https://github.com/kubernetes-sigs/aws-ebs-csi-driver
- Azure Disk CSI Driver: https://github.com/kubernetes-sigs/azuredisk-csi-driver
- GCP Persistent Disk CSI Driver: https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver

**Autoscaling:**
- Cluster Autoscaler: https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler
- Karpenter: https://karpenter.sh/
- AKS Cluster Autoscaler: https://learn.microsoft.com/en-us/azure/aks/cluster-autoscaler
- GKE Cluster Autoscaler: https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler
