---
name: "GCP Multi-Service Architect"
slug: "cloud-gcp-architect"
description: "Design GCP solutions across compute, storage, networking, and serverless with cost optimization, security hardening, and Framework alignment."
capabilities:
  - GCP compute service selection (Compute Engine, Cloud Run, Cloud Functions, GKE)
  - Storage architecture design (Cloud Storage, Persistent Disk, Filestore)
  - Network topology design (VPC, Cloud Load Balancing, Cloud CDN, Cloud Armor)
  - Serverless architecture patterns (Cloud Run, Cloud Functions, Eventarc, Pub/Sub, Workflows)
  - Terraform infrastructure-as-code generation
  - Cost optimization with committed use discounts and Spot VM recommendations
  - Architecture Framework assessment (operational excellence, security, reliability, performance, cost)
  - Multi-region and disaster recovery architecture
  - IAM policy design with least-privilege principles
  - Service integration and data flow design
inputs:
  - requirements: "functional and non-functional requirements (object with performance, security, cost, compliance)"
  - workload_type: "web-app, data-processing, real-time, batch, machine-learning, hybrid (string)"
  - current_architecture: "description of existing infrastructure if migration (string, optional)"
  - deployment_tier: "T1 (quick recommendation) | T2 (detailed design with IaC) (string, default: T1)"
  - regions: "primary and DR regions (array, default: single region)"
  - budget_constraints: "monthly budget or cost sensitivity (string, optional)"
outputs:
  - architecture_design: "GCP service selection with rationale and data flow diagram description"
  - iac_templates: "Terraform code for infrastructure deployment (T2)"
  - cost_estimate: "TCO analysis with monthly/annual projections and optimization recommendations"
  - security_configuration: "IAM policies, firewall rules, encryption settings, and compliance mappings"
  - architecture_framework_assessment: "alignment with GCP Architecture Framework pillars and recommendations"
  - migration_strategy: "phased migration plan if current_architecture provided (T2)"
keywords:
  - gcp
  - google-cloud
  - cloud-architecture
  - compute-engine
  - cloud-run
  - cloud-functions
  - gke
  - cloud-storage
  - terraform
  - architecture-framework
  - serverless
  - cost-optimization
  - multi-region
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://cloud.google.com/architecture/framework
  - https://cloud.google.com/docs
  - https://cloud.google.com/products/calculator
  - https://cloud.google.com/iam/docs/overview
  - https://cloud.google.com/docs/terraform
---

## Purpose & When-To-Use

**Trigger conditions:**
- GCP solution design spanning multiple services (compute + storage + networking)
- Architecture Framework assessment or optimization
- Cost optimization review for existing GCP infrastructure
- Multi-region or disaster recovery architecture planning
- Migration from on-premises or other clouds to GCP
- Serverless vs container vs VM architecture decision
- GCP service selection for new workload requirements
- Terraform template generation for infrastructure
- Compliance-driven architecture (HIPAA, PCI-DSS, ISO 27001 on GCP)

**Not for:**
- Single GCP service deep-dive (use service-specific documentation)
- Application code development (focuses on infrastructure)
- Non-GCP multi-cloud strategy (use cloud-multicloud-advisor skill)
- Kubernetes-specific deployment patterns without GCP context
- Detailed cost analysis without architecture context (use finops-cost-analyzer)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T14:30:00-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `requirements` must include at least one of: performance, security, cost, compliance
- `workload_type` must be one of: web-app, data-processing, real-time, batch, machine-learning, hybrid
- `deployment_tier` must be: T1 or T2
- `regions` if specified must be valid GCP region codes (e.g., us-central1, europe-west1)
- `budget_constraints` if provided must specify monthly or annual budget

**Source freshness:**
- GCP Architecture Framework (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/architecture/framework - verify 2024+ versions
- GCP Compute Services (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/products - Compute Engine, Cloud Run, Cloud Functions, GKE feature matrix
- GCP Storage Services (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/products - Cloud Storage, Persistent Disk, Filestore durability and performance SLAs
- GCP Networking (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/vpc - VPC design patterns and limits
- GCP IAM Best Practices (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/iam/docs/overview - least-privilege policies
- GCP Pricing (accessed 2025-10-26T14:30:00-04:00): https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts - committed use discounts and Spot VMs

**Decision thresholds:**
- Cloud Functions recommended if: stateless, event-driven, <9min execution (540s timeout), minimal config
- Cloud Run recommended if: containerized, HTTP-based, automatic scaling, pay-per-use
- GKE recommended if: Kubernetes-native, complex orchestration, multi-cloud portability
- Compute Engine recommended if: full OS control, specialized machine types, legacy dependencies
- Cloud Storage recommended for: object storage, static assets, data lakes, archival (11 9s durability)
- Persistent Disk recommended for: VM block storage, database volumes, low-latency
- Filestore recommended for: shared NFS file systems, lift-and-shift workloads

---

## Procedure

### T1: Quick Architecture Recommendation (≤2k tokens)

**Fast path for 80% of GCP architecture decisions:**

1. **Workload classification:**
   - **Web application**: Cloud Run + Cloud SQL OR Cloud Load Balancing + GKE
   - **Data processing**: Cloud Functions + Cloud Storage + Dataflow OR Dataproc for big data
   - **Real-time**: Pub/Sub + Cloud Run + Firestore OR GKE with streaming
   - **Batch**: Cloud Tasks + Cloud Functions OR Batch for large-scale processing
   - **Machine learning**: Vertex AI + Cloud Storage + Cloud Run for inference

2. **Core service selection:**
   - **Compute**: Choose based on decision thresholds (see Pre-Checks)
   - **Storage**: Cloud Storage for objects, Cloud SQL/Firestore for databases, Persistent Disk for block
   - **Networking**: VPC with subnets, Cloud NAT, Cloud Load Balancing
   - **Integration**: Eventarc for events, Pub/Sub for messaging, Workflows for orchestration

3. **Quick cost estimate:**
   - Compute: VM hours x hourly rate OR Cloud Run requests x execution time
   - Storage: GB stored x storage class rate + data transfer costs
   - Networking: egress charges + load balancer costs
   - Database: instance hours + storage + I/O (Cloud SQL) OR read/write operations (Firestore)

4. **Security baseline:**
   - VPC with private subnets for compute, public subnets for load balancers
   - Firewall rules with least-privilege ingress/egress
   - Service accounts with predefined IAM roles (no basic roles)
   - Encryption at rest (Cloud Storage default encryption, disk encryption, Cloud SQL encryption)
   - Encryption in transit (TLS/HTTPS required)

5. **Output (T1):**
   - GCP service architecture diagram (textual description with service names)
   - Core services with justification (compute, storage, database, networking)
   - Rough monthly cost estimate (±30% accuracy)
   - Architecture Framework pillar alignment summary
   - Recommended next steps for T2 detailed design

**Abort conditions:**
- Workload requirements unclear or conflicting
- Compliance requirements needing legal review (note for T2)
- Budget constraints conflict with availability requirements

---

### T2: Detailed Architecture Design with IaC (≤6k tokens)

**For production-ready GCP architectures with infrastructure-as-code:**

1. **All T1 steps** plus:

2. **Comprehensive service integration:**

   **Compute tier:**
   - Compute Engine: machine family selection (general-purpose n2, compute-optimized c2, memory-optimized m2)
   - Managed Instance Groups with autoscaling policies (CPU, load balancer utilization, custom metrics)
   - Instance templates with startup scripts
   - Spot VMs for fault-tolerant workloads (60-91% cost savings)
   - Cloud Run: automatic scaling with concurrency limits, minimum instances, CPU allocation
   - Cloud Functions: runtime selection (Python 3.12, Node.js 20), memory optimization, max instances
   - GKE: Autopilot for fully managed OR Standard with node pools, cluster autoscaler, workload identity

   **Storage tier:**
   - Cloud Storage: bucket policies with encryption (Google-managed or customer-managed), versioning, lifecycle policies
   - Storage classes: Standard, Nearline (30-day minimum), Coldline (90-day), Archive (365-day)
   - Object lifecycle management for automatic cost optimization
   - Transfer Service for large-scale data migration
   - Persistent Disk: disk types (balanced pd-balanced, SSD pd-ssd, standard pd-standard, extreme pd-extreme)
   - Filestore: service tiers (Basic HDD/SSD, Enterprise for high availability)

   **Networking tier:**
   - VPC design: subnet creation with custom IP ranges, multi-region for HA
   - Public subnets for load balancers and bastion hosts
   - Private subnets for compute with Cloud NAT for outbound internet access
   - Private Service Connect for private access to Google APIs
   - Firewall rules with tags and service accounts for dynamic security
   - Cloud Load Balancing: Global HTTP(S), Regional Network, Internal TCP/UDP
   - Cloud CDN for content delivery with cache modes
   - Cloud Armor for WAF and DDoS protection

   **Serverless integration:**
   - Cloud Run for containerized HTTP services with custom domains, authentication
   - Cloud Functions with Eventarc triggers (Pub/Sub, Cloud Storage, direct events)
   - Workflows for state machine orchestration with retries and error handling
   - Pub/Sub for async messaging (exactly-once delivery, dead-letter topics)
   - Cloud Tasks for task queue management with rate limiting

   **Database selection:**
   - Cloud SQL: engine choice (PostgreSQL, MySQL), high availability with automatic failover
   - AlloyDB for PostgreSQL-compatible high-performance workloads
   - Cloud Spanner: globally distributed relational with strong consistency
   - Firestore: serverless NoSQL document database with real-time sync
   - Bigtable: wide-column NoSQL for high-throughput analytics
   - BigQuery: serverless data warehouse with petabyte-scale analytics

3. **Architecture Framework deep-dive:**

   **Operational Excellence:**
   - Terraform for IaC with remote state in Cloud Storage
   - Cloud Logging centralization with log sinks and exports
   - Cloud Monitoring dashboards, alerts, and uptime checks
   - Cloud Trace for distributed tracing
   - Config Connector for Kubernetes-based infrastructure management

   **Security:**
   - Service accounts for workload identity (no service account keys for VMs)
   - IAM policies with least privilege, organization policies for constraints
   - Secret Manager for sensitive data with automatic rotation
   - Security Command Center for threat detection and compliance monitoring
   - VPC Service Controls for data exfiltration prevention
   - Cloud Armor for application layer security
   - Binary Authorization for container image signing and deployment policies
   - Cloud KMS customer-managed encryption keys (CMEK) with key rotation

   **Reliability:**
   - Multi-zone deployments (at least 2 zones, 3 for critical workloads)
   - Multi-region for disaster recovery (warm standby or active-active)
   - Cloud Load Balancing health checks with automatic failover
   - Cloud SQL automated backups with point-in-time recovery, cross-region replicas
   - Cloud Storage multi-region or dual-region for critical data
   - Deployment Manager or Terraform for consistent multi-region deployment

   **Performance Efficiency:**
   - Cloud CDN for static content caching
   - Memorystore (Redis/Memcached) for application caching
   - Cloud SQL read replicas for read-heavy workloads
   - Firestore with proper indexing and query optimization
   - Cloud Run minimum instances to reduce cold start latency
   - Persistent Disk provisioned IOPS for database performance

   **Cost Optimization:**
   - Committed Use Discounts (up to 55%, up to 70% for memory-optimized) for 1-year or 3-year commitments
   - Spot VMs for batch and fault-tolerant workloads (60-91% discount)
   - Cloud Storage lifecycle policies (Standard → Nearline → Coldline → Archive)
   - Right-sizing recommendations from Active Assist
   - Autoscaling to match capacity with demand
   - Labels and network tags for cost attribution
   - Cloud Billing budgets and alerts

4. **Infrastructure-as-Code generation:**

   **Terraform approach:**
   - Modular configuration with separate files (network.tf, compute.tf, database.tf, storage.tf)
   - Variables for environment-specific values (project ID, region, machine types)
   - Outputs for cross-module references (VPC ID, subnet IDs)
   - Remote state in Cloud Storage with state locking
   - Google provider configuration with explicit versions

5. **Security hardening:**
   - OS Login for SSH key management via IAM
   - Private Google Access for VM access to Google APIs without external IPs
   - Cloud SQL with private IP and Cloud SQL Auth Proxy
   - VPC Service Controls perimeter for data protection
   - Organization policies to enforce security constraints
   - Security Health Analytics for vulnerability scanning
   - Cloud Asset Inventory for resource discovery and compliance
   - Cloud Audit Logs for API activity monitoring

6. **Cost estimation (detailed):**
   - Compute: machine family, hours/month, committed use discount
   - Storage: Cloud Storage classes, operations, data transfer
   - Database: Cloud SQL instance hours, storage, backups
   - Networking: egress charges (inter-region, internet), load balancer hours
   - Total Cost of Ownership (TCO): 1-year and 3-year projections
   - Cost optimization opportunities: committed use, Spot VMs, rightsizing, lifecycle policies

7. **Migration strategy (if current_architecture provided):**
   - **Discovery phase**: Migrate to Virtual Machines assessment, Database Migration Service compatibility checks
   - **Planning**: TCO estimation, service mapping
   - **Migration waves**:
     - Wave 1: Stateless web tier (lift-and-shift to Compute Engine or containerize for Cloud Run/GKE)
     - Wave 2: Database tier (Database Migration Service for minimal downtime, or snapshot restore)
     - Wave 3: Integration points (Pub/Sub, Memorystore, Cloud Storage)
   - **Cutover strategy**: DNS-based with Cloud Load Balancing traffic splitting (10% → 50% → 100%)
   - **Validation**: smoke tests, performance benchmarks, rollback procedures

8. **Output (T2):**
   - Complete architecture diagram with all GCP services and data flows
   - Terraform configuration (modular, production-ready)
   - Detailed cost estimate with 1-year/3-year TCO and optimization recommendations
   - IAM policies and firewall rules (least-privilege)
   - Architecture Framework assessment with pillar scores and recommendations
   - Deployment guide with prerequisites and step-by-step instructions
   - Migration plan with timeline, risks, and rollback procedures (if applicable)
   - Monitoring and alerting configuration (Cloud Monitoring dashboards, alert policies)

**Abort conditions:**
- Specialized GPU/TPU requirements needing detailed machine family expertise
- Highly regulated workloads (FedRAMP, IL5) requiring compliance specialist review
- Complex hybrid connectivity (Dedicated Interconnect, Partner Interconnect mesh) needing network architect
- Custom OS image creation or hardening outside of GCP managed services

---

### T3: Not Implemented

**Note:** This skill implements T1 (quick recommendations) and T2 (detailed design with IaC) tiers only. T2 provides production-ready GCP architectures with comprehensive Architecture Framework assessment, security hardening, cost optimization, and migration planning. For specialized scenarios requiring deeper analysis (custom compliance frameworks, complex hybrid architectures, or organization-wide GCP setup), consult Google Cloud Customer Engineers or Google Cloud Professional Services.

**Future T3 considerations:**
- Organization-wide GCP setup with Cloud Identity and resource hierarchy design
- Multi-project strategy with shared VPC and centralized billing
- Complex hybrid architectures with Dedicated Interconnect and Cloud VPN mesh
- Custom compliance frameworks beyond standard Security Command Center detectors
- Anthos and hybrid/multi-cloud deployment patterns
- Large-scale migration program management with portfolio assessment

---

## Decision Rules

**Compute service selection:**
- **Cloud Functions** if all of:
  - Stateless or state in Firestore/Cloud Storage
  - <9min execution time (<540 seconds)
  - Event-driven (Pub/Sub, Cloud Storage, Eventarc)
  - Variable/unpredictable load (auto-scales to zero)
  - Minimal configuration preferred

- **Cloud Run** if:
  - Containerized application
  - HTTP/gRPC endpoints
  - Automatic scaling desired (including scale-to-zero)
  - Pay-per-use pricing preferred
  - No Kubernetes complexity needed

- **GKE** if:
  - Kubernetes-native (existing K8s apps or team expertise)
  - Complex orchestration (>20 microservices)
  - Multi-cloud portability required
  - Advanced networking (Istio, Anthos Service Mesh)

- **Compute Engine** if:
  - Full OS control (custom kernel, drivers)
  - Specialized machine types (GPU, high memory, sole-tenant)
  - Legacy applications not containerizable
  - Bring Your Own License (BYOL)

**Storage service selection:**
- **Cloud Storage** for: object storage, static assets, data lakes, backups, archival
- **Persistent Disk** for: VM block storage, databases (PostgreSQL, MySQL), low-latency
- **Filestore** for: NFS file shares across VMs/GKE, lift-and-shift file workloads
- **Cloud Storage for Firebase** for: mobile/web app file storage with client SDKs

**Database service selection:**
- **Cloud Spanner** if: globally distributed relational, strong consistency, horizontal scaling
- **Cloud SQL** if: managed relational database, regional deployment, PostgreSQL/MySQL compatibility
- **AlloyDB** if: high-performance PostgreSQL, 4x faster than standard PostgreSQL
- **Firestore** if: serverless NoSQL document store, real-time synchronization, mobile/web apps
- **Bigtable** if: wide-column NoSQL, high-throughput (>1M ops/sec), analytics workloads
- **BigQuery** if: data warehouse, OLAP analytics, petabyte-scale, SQL interface

**Networking design:**
- **Single VPC** if: small footprint (<100 resources), single application
- **Shared VPC** if: multiple projects need network connectivity, centralized network administration
- **VPC Peering** if: VPCs in different organizations need connectivity
- **Cloud NAT** vs **Private Google Access**: use Private Google Access for Google APIs access without external IPs

**Multi-region strategy:**
- **Single region** if: latency requirements met, no DR requirements, cost-sensitive
- **Multi-region active-passive** if: disaster recovery (RTO <1 hour, RPO <1 hour)
- **Multi-region active-active** if: global user base, <100ms latency requirement, highest availability

**Ambiguity handling:**
- If workload type unclear → request architecture diagram or user journey map
- If performance requirements unknown → recommend T1 baseline with monitoring, iterate
- If budget constraints conflict with availability → present trade-off matrix with RTO/RPO vs cost

**Stop conditions:**
- Conflicting requirements (e.g., "lowest cost + highest availability + multi-region")
- Regulatory requirements without defined compliance framework
- No clear application architecture or data flow documentation (T2 requires this)

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "architecture": {
    "workload_type": "web-app | data-processing | real-time | batch | ml | hybrid",
    "services": [
      {
        "category": "compute | storage | database | networking | integration | security",
        "service_name": "GCP service name (e.g., Compute Engine, Cloud Run, Cloud Functions)",
        "rationale": "why this service was selected",
        "configuration_summary": "key configuration details"
      }
    ],
    "data_flow": "textual description of data flow between services"
  },
  "cost_estimate": {
    "monthly_usd": "number (approximate for T1, detailed for T2)",
    "breakdown": {
      "compute": "number",
      "storage": "number",
      "database": "number",
      "networking": "number",
      "other": "number"
    },
    "optimization_opportunities": ["array of cost reduction recommendations"]
  },
  "architecture_framework_alignment": {
    "operational_excellence": "high | medium | low with justification",
    "security": "high | medium | low with justification",
    "reliability": "high | medium | low with justification",
    "performance_efficiency": "high | medium | low with justification",
    "cost_optimization": "high | medium | low with justification"
  },
  "next_steps": ["array of actionable recommendations"]
}
```

**Additional T2 fields:**
```json
{
  "iac_code": {
    "type": "terraform",
    "files": [
      {
        "filename": "string (e.g., main.tf, variables.tf)",
        "content": "string (Terraform HCL code)",
        "description": "purpose of this configuration file"
      }
    ]
  },
  "security_configuration": {
    "iam_policies": [
      {
        "service_account": "string",
        "roles": ["array of predefined IAM roles with least privilege"]
      }
    ],
    "firewall_rules": [
      {
        "name": "string",
        "direction": "INGRESS | EGRESS",
        "allowed": ["array of allowed protocols and ports"],
        "source_ranges": ["array of source CIDR blocks or tags"]
      }
    ],
    "encryption": {
      "at_rest": "services and encryption methods (Google-managed or CMEK)",
      "in_transit": "TLS configuration and certificate management"
    }
  },
  "monitoring": {
    "dashboards": "description of key metrics to monitor",
    "alert_policies": [
      {
        "metric": "string (e.g., compute.googleapis.com/instance/cpu/utilization)",
        "threshold": "number",
        "action": "notification channel or action"
      }
    ],
    "logs": "centralized logging strategy (Cloud Logging, log sinks)"
  },
  "migration_plan": {
    "phases": [
      {
        "phase_number": "integer",
        "description": "string",
        "services_migrated": ["array of GCP services deployed"],
        "duration": "string (e.g., 2 weeks)",
        "success_criteria": ["array of validation steps"],
        "rollback_procedure": "string"
      }
    ]
  }
}
```

---

## Examples

```yaml
# T1 Example: Serverless Web Application Architecture
# Cloud Run + Cloud SQL + Cloud Storage + Cloud CDN

Services:
  Compute: Cloud Run (Python 3.12, 1 vCPU, 512Mi memory, auto-scale 0-100)
  Database: Cloud SQL PostgreSQL (db-f1-micro, 10GB storage, automated backups)
  Storage: Cloud Storage (Standard class, static assets + user uploads)
  CDN: Cloud CDN (distribution for Cloud Storage + Cloud Run)
  Load Balancer: Global HTTP(S) Load Balancer (with SSL certificate)
  Auth: Identity Platform (user management, social auth providers)

Estimated Monthly Cost (10K users, 1M requests):
  Cloud Run: $15 (1M requests, 512Mi, 200ms avg execution)
  Cloud SQL: $25 (db-f1-micro, 10GB storage, 100 connection hours)
  Cloud Storage: $3 (10GB Standard storage, 100K requests)
  Cloud CDN: $12 (100GB cache egress)
  Load Balancer: $8 (forwarding rules + bandwidth)
  Total: ~$63/month
```

(Full T2 Terraform example: `/resources/terraform-serverless-webapp/`)

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - service selection + cost estimate + Architecture Framework summary
- **T2**: ≤6,000 tokens - detailed design + Terraform templates + security + migration plan

**Safety checks:**
- No service account keys in Terraform (use workload identity or default service accounts)
- IAM policies use predefined roles where possible (avoid overly permissive custom roles)
- Firewall rules have no 0.0.0.0/0 ingress for SSH (use Identity-Aware Proxy)
- Cloud Storage buckets have appropriate access controls (no public access unless required)
- Encryption enabled for all data stores (Cloud Storage, Persistent Disk, Cloud SQL)

**Auditability:**
- All GCP service recommendations cite official documentation with access date (NOW_ET)
- Cost estimates include calculation methodology (instance hours, GB-months, requests)
- Architecture Framework pillars mapped to specific GCP services and configurations
- Compliance controls (if applicable) mapped to Security Command Center standards

**Determinism:**
- Given same inputs, produce identical service selection recommendations
- Cost estimates use consistent GCP pricing (with committed use/Spot VM discounts noted)
- Terraform configurations follow Google Cloud best practices

**Validation requirements:**
- T2 Terraform configurations must pass `terraform validate`
- IAM policies must use valid predefined or custom role names
- Firewall rules must have valid CIDR blocks and protocol/port combinations

---

## Resources

**Official GCP Documentation (accessed 2025-10-26T14:30:00-04:00):**
- GCP Architecture Framework: https://cloud.google.com/architecture/framework
- GCP Architecture Center: https://cloud.google.com/architecture
- GCP Compute Services: https://cloud.google.com/products/compute
- GCP Storage Services: https://cloud.google.com/products/storage
- GCP Networking: https://cloud.google.com/vpc/docs
- GCP Hosting Options: https://cloud.google.com/hosting-options

**GCP Service Documentation:**
- Compute Engine: https://cloud.google.com/compute/docs
- Cloud Run: https://cloud.google.com/run/docs
- Cloud Functions: https://cloud.google.com/functions/docs
- Google Kubernetes Engine: https://cloud.google.com/kubernetes-engine/docs
- Cloud Storage: https://cloud.google.com/storage/docs
- Cloud SQL: https://cloud.google.com/sql/docs
- Cloud Spanner: https://cloud.google.com/spanner/docs
- Firestore: https://cloud.google.com/firestore/docs
- BigQuery: https://cloud.google.com/bigquery/docs

**Infrastructure-as-Code:**
- Terraform on GCP: https://cloud.google.com/docs/terraform
- Terraform Google Provider: https://registry.terraform.io/providers/hashicorp/google/latest/docs
- Terraform Modules for GCP: https://github.com/terraform-google-modules
- Config Connector: https://cloud.google.com/config-connector/docs

**Cost Optimization:**
- GCP Pricing Calculator: https://cloud.google.com/products/calculator
- Committed Use Discounts: https://cloud.google.com/compute/docs/instances/signing-up-committed-use-discounts
- Spot VMs: https://cloud.google.com/compute/docs/instances/spot
- Cloud Billing: https://cloud.google.com/billing/docs
- Active Assist Recommendations: https://cloud.google.com/recommender/docs

**Security Best Practices:**
- IAM Overview: https://cloud.google.com/iam/docs/overview
- IAM Best Practices: https://cloud.google.com/iam/docs/best-practices
- Security Command Center: https://cloud.google.com/security-command-center/docs
- Secret Manager: https://cloud.google.com/secret-manager/docs
- VPC Service Controls: https://cloud.google.com/vpc-service-controls/docs
- Binary Authorization: https://cloud.google.com/binary-authorization/docs

**Example Templates:**
- `/resources/terraform-serverless-webapp/` - Complete serverless web app with Cloud Run, Cloud SQL, Cloud Storage
- `/resources/terraform-gke-cluster/` - GKE Standard cluster with node pools, autoscaling, workload identity
- `/resources/iam-least-privilege-examples.json` - Example IAM bindings with predefined roles
- `/resources/vpc-reference-architecture.tf` - Multi-zone VPC with public/private subnets

**Migration Resources:**
- Migrate to Virtual Machines: https://cloud.google.com/migrate/virtual-machines/docs
- Database Migration Service: https://cloud.google.com/database-migration/docs
- Transfer Service: https://cloud.google.com/storage-transfer/docs
- Migration Guides: https://cloud.google.com/architecture/migration-to-gcp-getting-started
