# Multi-Cloud Integration Patterns

**Version**: 1.0.0
**Access Date**: 2025-10-25T21:30:36-04:00
**Sources**: CNCF, AWS, Azure, GCP official documentation

## 1. Cloud-Agnostic Infrastructure as Code (IaC)

### Pattern: Use Terraform/Pulumi for Multi-Cloud Provisioning

**Problem**: CloudFormation (AWS), ARM/Bicep (Azure), Deployment Manager (GCP) create vendor lock-in.

**Solution**: Use cloud-agnostic IaC tools that support all providers.

**Terraform Example**:
```hcl
# provider.tf - Multi-cloud provider configuration
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

# modules/compute/main.tf - Abstract compute module
variable "cloud_provider" {
  type = string
  validation {
    condition = contains(["aws", "azure", "gcp"], var.cloud_provider)
  }
}

resource "aws_instance" "vm" {
  count = var.cloud_provider == "aws" ? 1 : 0
  ami           = var.aws_ami
  instance_type = "t3.xlarge"
}

resource "azurerm_linux_virtual_machine" "vm" {
  count = var.cloud_provider == "azure" ? 1 : 0
  size  = "Standard_D4s_v3"
  # ... Azure-specific config
}

resource "google_compute_instance" "vm" {
  count = var.cloud_provider == "gcp" ? 1 : 0
  machine_type = "n2-standard-4"
  # ... GCP-specific config
}
```

**Benefits**: Single codebase, consistent workflow, easier migration between clouds.

**Limitations**: Abstractions can hide cloud-specific optimizations; state management complexity.

---

## 2. Kubernetes for Workload Portability

### Pattern: Deploy workloads to EKS, AKS, GKE using identical manifests

**Problem**: Vendor-specific compute services (EC2, Azure VMs, Compute Engine) lack portability.

**Solution**: Containerize applications and deploy to managed Kubernetes (EKS/AKS/GKE).

**Kubernetes Manifest (Cloud-Agnostic)**:
```yaml
# deployment.yaml - Runs identically on EKS, AKS, GKE
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: app
        image: myregistry/web-app:v1.2.3
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
---
# service.yaml - LoadBalancer type supported by all clouds
apiVersion: v1
kind: Service
metadata:
  name: web-app-svc
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
```

**Cloud-Specific Annotations (when needed)**:
```yaml
# AWS EKS: Use NLB
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"

# Azure AKS: Use internal LB
metadata:
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"

# GCP GKE: Use regional LB
metadata:
  annotations:
    cloud.google.com/load-balancer-type: "External"
```

**Benefits**: Write-once-run-anywhere for containerized workloads; avoid VM-level lock-in.

**Limitations**: Storage (EBS vs Azure Disk vs Persistent Disk) requires cloud-specific StorageClasses.

---

## 3. Service Mesh for Cross-Cloud Service Discovery

### Pattern: Istio/Linkerd for mTLS and traffic management

**Problem**: Service-to-service communication across clouds requires manual certificate management and routing.

**Solution**: Deploy service mesh (Istio/Linkerd) with federated control plane.

**Istio Multi-Cluster Setup**:
```yaml
# istio-multicluster.yaml - Federation across EKS (AWS) and GKE (GCP)
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-multicluster
spec:
  values:
    global:
      meshID: prod-mesh
      multiCluster:
        clusterName: eks-us-east-1  # or gke-us-central1
      network: aws-network  # or gcp-network
  components:
    ingressGateways:
    - name: istio-eastwestgateway
      enabled: true
      label:
        istio: eastwestgateway
      k8s:
        service:
          type: LoadBalancer
          ports:
          - port: 15443  # mTLS cross-cluster traffic
```

**Benefits**: Automatic mTLS, traffic shifting (canary/blue-green), distributed tracing across clouds.

**Limitations**: Latency overhead (5-10ms per hop); requires Kubernetes on all clouds.

---

## 4. Event Streaming for Async Integration

### Pattern: Kafka/Confluent Cloud for cross-cloud event-driven architecture

**Problem**: Tightly coupled synchronous APIs create cascading failures across clouds.

**Solution**: Use managed Kafka (Confluent Cloud, AWS MSK, Azure Event Hubs Kafka) for async messaging.

**Confluent Cloud (Multi-Cloud SaaS)**:
```yaml
# Terraform: Deploy Kafka cluster in AWS + consumers in Azure/GCP
resource "confluent_kafka_cluster" "main" {
  cloud        = "AWS"
  region       = "us-east-1"
  availability = "MULTI_ZONE"
}

resource "confluent_kafka_topic" "orders" {
  kafka_cluster_id = confluent_kafka_cluster.main.id
  topic_name       = "orders"
  partitions_count = 6
  config = {
    "retention.ms" = "86400000"  # 1 day
  }
}

# Producer in AWS EKS
# Consumer in Azure AKS or GCP GKE
# Both connect via Confluent Cloud endpoint (cross-cloud)
```

**Benefits**: Decouples clouds; supports async, event-driven patterns; exactly-once semantics.

**Limitations**: Egress costs for cross-cloud data transfer; SaaS vendor dependency.

---

## 5. Identity Federation with OIDC/SAML

### Pattern: Single sign-on across AWS IAM Identity Center, Azure Entra ID, GCP Cloud Identity

**Problem**: Managing separate identities per cloud increases attack surface and friction.

**Solution**: Federate identities using OIDC or SAML with central IdP (Okta, Auth0, or Azure AD).

**Architecture**:
```
[Azure Entra ID as Central IdP]
         |
         |--> AWS IAM Identity Center (SAML trust)
         |--> Azure subscriptions (native)
         |--> GCP Cloud Identity (SAML trust)
```

**AWS IAM Identity Center SAML Config**:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::123456789012:saml-provider/AzureAD"
    },
    "Action": "sts:AssumeRoleWithSAML",
    "Condition": {
      "StringEquals": {
        "SAML:aud": "https://signin.aws.amazon.com/saml"
      }
    }
  }]
}
```

**Benefits**: Single credential store; centralized MFA; consistent RBAC policies.

**Limitations**: IdP becomes single point of failure; SAML complexity.

---

## 6. Network Connectivity: VPN vs Direct Connect

### Pattern: Site-to-site VPN for low-bandwidth; Direct Connect/ExpressRoute/Interconnect for high-bandwidth

**Scenario 1: VPN for <1Gbps**
```
[On-Prem DC] <--IPSec VPN--> [AWS VPN Gateway]
[On-Prem DC] <--IPSec VPN--> [Azure VPN Gateway]
[On-Prem DC] <--IPSec VPN--> [GCP Cloud VPN]
```
**Cost**: ~$0.05/hr per VPN connection + egress ($0.09/GB)

**Scenario 2: Direct Connect for ≥1Gbps**
```
[On-Prem DC] <--Fiber--> [Equinix Colocation]
                           |--> AWS Direct Connect (1Gbps: $0.30/hr)
                           |--> Azure ExpressRoute (1Gbps: $0.18/hr)
                           |--> GCP Interconnect (1Gbps: $0.18/hr)
```
**Cost**: Port hour fees + egress (reduced rates: $0.02-0.05/GB vs $0.09/GB internet)

**Benefits**: VPN = easy setup, low cost. Direct = low latency (<10ms), predictable bandwidth.

**Limitations**: Direct requires physical fiber installation (weeks-months lead time).

---

## 7. Data Portability: Open Formats

### Pattern: Use Parquet, Avro, ORC instead of vendor-specific formats

**Anti-Pattern** (Locked-In):
```python
# AWS DynamoDB native format
dynamodb.put_item(TableName='users', Item={'id': {'S': '123'}, 'name': {'S': 'Alice'}})

# Azure Cosmos DB native format
cosmos_db.create_item(body={'id': '123', 'name': 'Alice', '_ts': 1730000000})
```

**Best Practice** (Portable):
```python
# Export to Parquet (columnar, compressed, cloud-agnostic)
import pandas as pd
df = pd.DataFrame({'id': [123], 'name': ['Alice']})
df.to_parquet('s3://bucket/users/2025-10-25.parquet')  # AWS S3
df.to_parquet('az://container/users/2025-10-25.parquet')  # Azure Blob
df.to_parquet('gs://bucket/users/2025-10-25.parquet')  # GCP Cloud Storage

# Read from any cloud
df = pd.read_parquet('s3://bucket/users/2025-10-25.parquet')
```

**Benefits**: Zero-effort migration; works with Spark, Presto, BigQuery; 10x compression.

**Limitations**: Query performance lower than native NoSQL (DynamoDB, Cosmos DB, Firestore).

---

## 8. API Abstraction Layer

### Pattern: Abstract vendor-specific SDKs behind common interface

**Example: Object Storage Abstraction**
```python
# storage_adapter.py - Cloud-agnostic storage interface
from abc import ABC, abstractmethod

class StorageAdapter(ABC):
    @abstractmethod
    def upload(self, bucket: str, key: str, data: bytes) -> None:
        pass

    @abstractmethod
    def download(self, bucket: str, key: str) -> bytes:
        pass

class S3Adapter(StorageAdapter):
    def __init__(self):
        import boto3
        self.s3 = boto3.client('s3')

    def upload(self, bucket: str, key: str, data: bytes) -> None:
        self.s3.put_object(Bucket=bucket, Key=key, Body=data)

    def download(self, bucket: str, key: str) -> bytes:
        return self.s3.get_object(Bucket=bucket, Key=key)['Body'].read()

class AzureBlobAdapter(StorageAdapter):
    def __init__(self):
        from azure.storage.blob import BlobServiceClient
        self.client = BlobServiceClient(account_url="https://...")

    def upload(self, bucket: str, key: str, data: bytes) -> None:
        container = self.client.get_container_client(bucket)
        container.upload_blob(name=key, data=data)

    def download(self, bucket: str, key: str) -> bytes:
        container = self.client.get_container_client(bucket)
        return container.download_blob(key).readall()

# app.py - Use abstraction
storage = S3Adapter() if os.getenv('CLOUD') == 'aws' else AzureBlobAdapter()
storage.upload('my-bucket', 'file.txt', b'Hello')
```

**Benefits**: Swap clouds by changing env var; testable with mock adapter.

**Limitations**: Abstraction hides cloud-specific optimizations (S3 multipart upload, Azure CDN).

---

## Summary Matrix

| Pattern | Lock-In Mitigation | Complexity | Cost Impact |
|---------|-------------------|------------|-------------|
| Terraform/Pulumi IaC | High | Medium | Low |
| Kubernetes (EKS/AKS/GKE) | High | High | Medium (control plane fees) |
| Service Mesh (Istio) | Medium | High | Low (latency overhead) |
| Kafka/Event Streaming | Medium | Medium | High (egress costs) |
| Identity Federation (OIDC) | High | Medium | Low |
| Direct Connect/VPN | Low (physical) | High (Direct) | High (port fees) |
| Open Data Formats (Parquet) | High | Low | Low |
| API Abstraction Layer | High | Medium | Low (dev effort) |

---

## Exit Strategy Best Practices

1. **Quarterly DR Drill**: Restore production workload to secondary cloud every 90 days
2. **Test Migration**: Validate Terraform/Kubernetes manifests work on new cloud
3. **Data Replication**: Maintain real-time or near-real-time copy in alternative cloud
4. **Documentation**: Keep runbook for "migrate from AWS to Azure in 7 days" scenario
5. **Contract Review**: Avoid multi-year commit discounts >50%; maintain flexibility

**Sources**:
- CNCF Cloud Native Computing Foundation: https://www.cncf.io/ (accessed 2025-10-25T21:30:36-04:00)
- Vendor Lock-In Prevention Guide: https://buzzclan.com/cloud/vendor-lock-in/ (accessed 2025-10-25T21:30:36-04:00)
- AWS Hybrid Best Practices: https://docs.aws.amazon.com/prescriptive-guidance/latest/hybrid-cloud-best-practices/ (accessed 2025-10-25T21:30:36-04:00)
