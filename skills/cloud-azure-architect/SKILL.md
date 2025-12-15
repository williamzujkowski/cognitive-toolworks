---
name: "Azure Multi-Service Architect"
slug: "cloud-azure-architect"
description: "Design Azure solutions across compute, storage, networking, and serverless with cost optimization, security hardening, and Framework alignment."
capabilities:
  - Azure compute service selection (VMs, App Service, Container Apps, Functions, AKS)
  - Storage architecture design (Blob Storage, Managed Disks, Azure Files)
  - Network topology design (Virtual Network, Load Balancer, Application Gateway, Front Door)
  - Serverless architecture patterns (Functions, Logic Apps, Event Grid, Service Bus)
  - Bicep and Terraform infrastructure-as-code generation
  - Cost optimization with Reserved Instances and Spot VM recommendations
  - Well-Architected Framework assessment (reliability, security, cost, operational excellence, performance)
  - Multi-region and disaster recovery architecture
  - RBAC policy design with managed identities and least-privilege principles
  - Service integration and data flow design
inputs:
  - requirements: "functional and non-functional requirements (object with performance, security, cost, compliance)"
  - workload_type: "web-app, data-processing, real-time, batch, machine-learning, hybrid (string)"
  - current_architecture: "description of existing infrastructure if migration (string, optional)"
  - deployment_tier: "T1 (quick recommendation) | T2 (detailed design with IaC) (string, default: T1)"
  - regions: "primary and DR regions (array, default: single region)"
  - budget_constraints: "monthly budget or cost sensitivity (string, optional)"
outputs:
  - architecture_design: "Azure service selection with rationale and data flow diagram description"
  - iac_templates: "Bicep or Terraform code for infrastructure deployment (T2)"
  - cost_estimate: "TCO analysis with monthly/annual projections and optimization recommendations"
  - security_configuration: "RBAC policies, NSG rules, encryption settings, and compliance mappings"
  - well_architected_assessment: "alignment with Azure Well-Architected Framework pillars and recommendations"
  - migration_strategy: "phased migration plan if current_architecture provided (T2)"
keywords:
  - azure
  - cloud-architecture
  - virtual-machines
  - app-service
  - container-apps
  - functions
  - aks
  - blob-storage
  - bicep
  - terraform
  - well-architected
  - serverless
  - cost-optimization
  - multi-region
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://learn.microsoft.com/en-us/azure/well-architected/
  - https://learn.microsoft.com/en-us/azure/
  - https://azure.microsoft.com/en-us/pricing/calculator/
  - https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
  - https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview
  - https://learn.microsoft.com/en-us/azure/developer/terraform/overview
---

## Purpose & When-To-Use

**Trigger conditions:**
- Azure solution design spanning multiple services (compute + storage + networking)
- Well-Architected Framework assessment or optimization
- Cost optimization review for existing Azure infrastructure
- Multi-region or disaster recovery architecture planning
- Migration from on-premises or other clouds to Azure
- Serverless vs container vs VM architecture decision
- Azure service selection for new workload requirements
- Bicep or Terraform template generation for infrastructure
- Compliance-driven architecture (HIPAA, PCI-DSS, ISO 27001 on Azure)

**Not for:**
- Single Azure service deep-dive (use service-specific documentation)
- Application code development (focuses on infrastructure)
- Non-Azure multi-cloud strategy (use cloud-multicloud-advisor skill)
- Kubernetes-specific deployment patterns without Azure context
- Detailed cost analysis without architecture context (use finops-cost-analyzer)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T14:45:00-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `requirements` must include at least one of: performance, security, cost, compliance
- `workload_type` must be one of: web-app, data-processing, real-time, batch, machine-learning, hybrid
- `deployment_tier` must be: T1 or T2
- `regions` if specified must be valid Azure region codes (e.g., eastus, westeurope, southeastasia)
- `budget_constraints` if provided must specify monthly or annual budget

**Source freshness:**
- Azure Well-Architected Framework (accessed 2025-10-26T14:45:00-04:00): https://learn.microsoft.com/en-us/azure/well-architected/ - verify 2024+ versions
- Azure Compute Services (accessed 2025-10-26T14:45:00-04:00): https://azure.microsoft.com/en-us/products - VMs, App Service, Container Apps, Functions, AKS feature matrix
- Azure Storage Services (accessed 2025-10-26T14:45:00-04:00): https://azure.microsoft.com/en-us/products - Blob Storage, Managed Disks, Files durability and performance SLAs
- Azure Networking (accessed 2025-10-26T14:45:00-04:00): https://learn.microsoft.com/en-us/azure/virtual-network/ - VNet design patterns and limits
- Azure RBAC Best Practices (accessed 2025-10-26T14:45:00-04:00): https://learn.microsoft.com/en-us/azure/role-based-access-control/overview - least-privilege policies
- Azure Pricing (accessed 2025-10-26T14:45:00-04:00): https://azure.microsoft.com/en-us/pricing/reserved-vm-instances/ - Reserved Instances and Spot VMs

**Decision thresholds:**
- Functions recommended if: stateless, event-driven, <10min execution (durable functions for longer), minimal config
- App Service recommended if: web/API apps, PaaS preferred, built-in scaling, deployment slots
- Container Apps recommended if: microservices, containerized, serverless containers, event-driven scaling
- AKS recommended if: Kubernetes-native, complex orchestration, multi-cloud portability
- VMs recommended if: full OS control, specialized VM sizes, legacy dependencies, lift-and-shift
- Blob Storage recommended for: object storage, static assets, data lakes, archival (multiple redundancy options)
- Managed Disks recommended for: VM block storage, database volumes, high performance
- Azure Files recommended for: SMB/NFS file shares, lift-and-shift file workloads

---

## Procedure

### T1: Quick Architecture Recommendation (≤2k tokens)

**Fast path for 80% of Azure architecture decisions:**

1. **Workload classification:**
   - **Web application**: App Service + Azure SQL OR Front Door + Container Apps + Cosmos DB
   - **Data processing**: Functions + Blob Storage + Synapse Analytics OR Databricks
   - **Real-time**: Event Hubs + Functions + Cosmos DB OR AKS with Kafka
   - **Batch**: Batch + Blob Storage OR Functions with Queue Storage triggers
   - **Machine learning**: Machine Learning + Blob Storage + Container Instances for inference

2. **Core service selection:**
   - **Compute**: Choose based on decision thresholds (see Pre-Checks)
   - **Storage**: Blob Storage for objects, Azure SQL/Cosmos DB for databases, Managed Disks for block
   - **Networking**: Virtual Network with subnets, Application Gateway, Front Door
   - **Integration**: Event Grid for events, Service Bus for messaging, Logic Apps for workflows

3. **Quick cost estimate:**
   - Compute: VM hours x hourly rate OR App Service tier cost OR Function executions x GB-seconds
   - Storage: GB stored x storage tier rate + transaction costs + data transfer
   - Networking: data egress + load balancer costs
   - Database: DTU/vCore hours + storage (Azure SQL) OR RU/s provisioned (Cosmos DB)

4. **Security baseline:**
   - Virtual Network with network security groups (NSGs) for subnet-level security
   - Private endpoints for PaaS services to avoid public internet exposure
   - Managed identities for Azure resources (no credentials in code)
   - Azure Key Vault for secrets, keys, and certificates
   - Encryption at rest (Storage Service Encryption, disk encryption, Transparent Data Encryption)
   - Encryption in transit (TLS/HTTPS required)

5. **Output (T1):**
   - Azure service architecture diagram (textual description with service names)
   - Core services with justification (compute, storage, database, networking)
   - Rough monthly cost estimate (±30% accuracy)
   - Well-Architected Framework pillar alignment summary
   - Recommended next steps for T2 detailed design

**Abort conditions:**
- Workload requirements unclear or conflicting
- Compliance requirements needing legal review (note for T2)
- Budget constraints conflict with availability requirements

---

### T2: Detailed Architecture Design with IaC (≤6k tokens)

**For production-ready Azure architectures with infrastructure-as-code:**

1. **All T1 steps** plus:

2. **Comprehensive service integration:**

   **Compute tier:**
   - Virtual Machines: VM series selection (B-series burstable, D-series general, E-series memory, F-series compute)
   - Virtual Machine Scale Sets with autoscaling rules (CPU, memory, custom metrics)
   - Availability Sets or Availability Zones for high availability
   - Spot VMs for fault-tolerant workloads (variable pricing, significant discounts)
   - App Service: tier selection (Free, Shared, Basic, Standard, Premium, Isolated), deployment slots
   - Container Apps: scale rules (HTTP, CPU, memory, custom), Dapr integration
   - Functions: hosting plans (Consumption, Premium, Dedicated), Durable Functions for stateful workflows
   - AKS: cluster autoscaler, virtual nodes, Azure CNI networking, workload identity

   **Storage tier:**
   - Blob Storage: access tiers (Hot, Cool, Archive), lifecycle management policies
   - Redundancy options: LRS, ZRS (zone-redundant), GRS (geo-redundant), GZRS
   - Blob versioning and soft delete for data protection
   - Managed Disks: disk types (Standard HDD, Standard SSD, Premium SSD, Ultra Disk)
   - Azure Files: Standard or Premium tiers, SMB or NFS protocols
   - Azure NetApp Files for enterprise NAS workloads

   **Networking tier:**
   - Virtual Network design: address space planning, subnet segmentation, multi-region peering
   - Network Security Groups (NSGs) with application security groups (ASGs)
   - Private endpoints for Azure PaaS services (Storage, SQL, Cosmos DB)
   - Azure Firewall for centralized network security
   - Application Gateway with Web Application Firewall (WAF) for HTTP/HTTPS traffic
   - Azure Front Door for global HTTP load balancing and CDN
   - Traffic Manager for DNS-based global load balancing
   - Azure Bastion for secure RDP/SSH without public IPs

   **Serverless integration:**
   - Azure Functions with triggers (HTTP, Timer, Queue, Blob, Event Grid, Service Bus)
   - Event Grid for event-driven architectures with custom topics
   - Service Bus for enterprise messaging (queues, topics, sessions)
   - Logic Apps for visual workflow automation
   - API Management for API gateway with policies, rate limiting, caching

   **Database selection:**
   - Azure SQL Database: DTU or vCore model, Business Critical or General Purpose tier
   - SQL Managed Instance for full SQL Server compatibility
   - Cosmos DB: API selection (SQL, MongoDB, Cassandra, Gremlin, Table), consistency levels
   - PostgreSQL/MySQL flexible servers with zone-redundant HA
   - Azure Synapse Analytics for data warehousing
   - Azure Cache for Redis for caching and session state

3. **Well-Architected Framework deep-dive:**

   **Reliability:**
   - Availability Zones for zone redundancy (minimum 2 zones, 3 for critical workloads)
   - Multi-region deployments for disaster recovery (active-passive or active-active)
   - Azure Site Recovery for VM replication and failover
   - Azure Backup for automated backup and restore
   - Application Gateway or Front Door health probes with automatic failover
   - Geo-redundant storage (GRS/GZRS) for critical data

   **Security:**
   - Managed identities for Azure resources (system-assigned or user-assigned)
   - Azure RBAC with built-in roles (Owner, Contributor, Reader, service-specific roles)
   - Azure Policy for governance and compliance enforcement
   - Microsoft Defender for Cloud for security posture management
   - Azure Key Vault with soft delete and purge protection
   - Private Link for private connectivity to PaaS services
   - Network Security Groups with minimal required rules
   - Azure DDoS Protection Standard for critical workloads
   - Encryption at rest with customer-managed keys (CMK) in Key Vault

   **Cost Optimization:**
   - Reserved Instances for VMs and SQL Database (up to 72% discount for 1-3 year terms)
   - Azure Hybrid Benefit for Windows Server and SQL Server (up to 80% combined savings)
   - Spot VMs for batch and fault-tolerant workloads (variable pricing)
   - Autoscaling to match capacity with demand
   - Blob Storage lifecycle policies (Hot → Cool → Archive)
   - Right-sizing recommendations from Azure Advisor
   - Resource tags for cost allocation and chargeback
   - Azure Cost Management + Billing with budgets and alerts

   **Operational Excellence:**
   - Bicep or Terraform for infrastructure-as-code
   - Azure Monitor with Log Analytics for centralized logging
   - Application Insights for application performance monitoring (APM)
   - Azure Alerts with action groups (email, SMS, webhook, runbook)
   - Azure Automation for runbook-based remediation
   - Azure DevOps or GitHub Actions for CI/CD pipelines

   **Performance Efficiency:**
   - Azure Front Door or CDN for content delivery
   - Azure Cache for Redis for application caching
   - SQL Database read replicas or Cosmos DB multi-region writes
   - Premium SSD or Ultra Disk for high IOPS workloads
   - Accelerated Networking for VMs (SR-IOV)
   - Proximity placement groups for low-latency workloads

4. **Infrastructure-as-Code generation:**

   **Bicep approach:**
   - Modular files with parameters for environment-specific values
   - Resource symbolic names for clean references
   - Outputs for cross-module dependencies
   - Built-in functions for dynamic resource naming
   - Native Azure integration with immediate API support

   **Terraform approach:**
   - Modular configuration (network.tf, compute.tf, database.tf, storage.tf)
   - Variables and locals for reusable values
   - Remote state in Azure Storage with state locking
   - AzureRM provider with explicit versions
   - Use of data sources for existing resources

5. **Security hardening:**
   - Just-in-Time (JIT) VM access via Defender for Cloud
   - Azure Bastion for secure RDP/SSH without public IPs
   - Managed identities for all Azure resource authentication
   - Key Vault access policies or RBAC for secrets management
   - Storage Account firewall rules with virtual network service endpoints
   - SQL Database firewall rules and Microsoft Entra authentication
   - Encryption at rest enabled for all storage services
   - TLS 1.2+ enforced for all HTTPS endpoints
   - Azure Policy for regulatory compliance (PCI-DSS, HIPAA, ISO 27001)

6. **Cost estimation (detailed):**
   - Compute: VM series, hours/month, Reserved Instance discount
   - Storage: Blob tiers, capacity, transactions, replication type
   - Database: DTU/vCore/RU capacity, storage, backup costs
   - Networking: egress charges (inter-region, internet), gateway costs
   - Total Cost of Ownership (TCO): 1-year and 3-year projections
   - Cost optimization opportunities: reservations, hybrid benefit, rightsizing, autoscaling

7. **Migration strategy (if current_architecture provided):**
   - **Discovery phase**: Azure Migrate assessment, dependency mapping
   - **Planning**: Azure TCO Calculator, service mapping
   - **Migration waves**:
     - Wave 1: Stateless web tier (Azure App Service migration assistant or lift-and-shift to VMs)
     - Wave 2: Database tier (Database Migration Service for minimal downtime)
     - Wave 3: Integration points (Service Bus, Event Grid, Blob Storage)
   - **Cutover strategy**: DNS-based with Traffic Manager weighted routing (10% → 50% → 100%)
   - **Validation**: smoke tests, performance benchmarks, rollback procedures

8. **Output (T2):**
   - Complete architecture diagram with all Azure services and data flows
   - Bicep modules OR Terraform configuration (modular, production-ready)
   - Detailed cost estimate with 1-year/3-year TCO and optimization recommendations
   - RBAC role assignments and NSG rules (least-privilege)
   - Well-Architected Framework assessment with pillar scores and recommendations
   - Deployment guide with prerequisites and step-by-step instructions
   - Migration plan with timeline, risks, and rollback procedures (if applicable)
   - Monitoring and alerting configuration (Azure Monitor dashboards, alert rules)

**Abort conditions:**
- Specialized GPU/FPGA requirements needing detailed VM series expertise
- Highly regulated workloads (FedRAMP High, IL5) requiring compliance specialist review
- Complex hybrid connectivity (ExpressRoute, multiple VPN gateways) needing network architect
- Custom VM image creation or hardening outside of Azure managed services

---

### T3: Not Implemented

**Note:** This skill implements T1 (quick recommendations) and T2 (detailed design with IaC) tiers only. T2 provides production-ready Azure architectures with comprehensive Well-Architected Framework assessment, security hardening, cost optimization, and migration planning. For specialized scenarios requiring deeper analysis (custom compliance frameworks, complex hybrid architectures, or enterprise-wide Azure Landing Zone design), consult Microsoft Customer Success Account Managers or Microsoft Consulting Services.

**Future T3 considerations:**
- Enterprise-wide Azure Landing Zone design with management groups
- Multi-subscription strategy with Azure Policy and Blueprints
- Complex hybrid architectures with ExpressRoute and Azure Virtual WAN
- Custom compliance frameworks beyond built-in Azure Policy definitions
- Azure Arc and hybrid/multi-cloud management
- Large-scale migration program management with Azure Migrate at scale

---

## Decision Rules

**Compute service selection:**
- **Functions** if all of:
  - Stateless or state in Cosmos DB/Blob Storage
  - <10min execution time (or Durable Functions for longer workflows)
  - Event-driven (HTTP, Timer, Queue, Blob, Event Grid, Service Bus)
  - Variable/unpredictable load (auto-scales to zero)
  - Minimal configuration preferred

- **App Service** if:
  - Web or API application
  - PaaS preferred over IaaS
  - Deployment slots needed (staging, canary)
  - Built-in autoscaling and load balancing
  - .NET, Java, Node.js, Python, PHP support

- **Container Apps** if:
  - Microservices architecture
  - Containerized workloads
  - Serverless containers (scale-to-zero)
  - Event-driven autoscaling (Keda)
  - Dapr integration for distributed app patterns

- **AKS** if:
  - Kubernetes-native (existing K8s apps or team expertise)
  - Complex orchestration (>20 microservices)
  - Multi-cloud portability required
  - Advanced networking (Istio, service mesh)

- **VMs** if:
  - Full OS control (custom software, drivers)
  - Specialized VM sizes (GPU, high memory, constrained vCPU)
  - Legacy applications not containerizable
  - Bring Your Own License (BYOL) with Azure Hybrid Benefit

**Storage service selection:**
- **Blob Storage** for: object storage, static assets, data lakes, backups, archival
- **Managed Disks** for: VM block storage, databases (SQL Server, PostgreSQL), high IOPS
- **Azure Files** for: SMB/NFS file shares across VMs/AKS, lift-and-shift file workloads
- **Azure NetApp Files** for: enterprise NAS, high-performance file workloads

**Database service selection:**
- **Azure SQL Database** if: relational database, SQL Server compatibility, PaaS preferred
- **SQL Managed Instance** if: near 100% SQL Server compatibility, lift-and-shift
- **Cosmos DB** if: globally distributed NoSQL, multi-model (document, graph, key-value), <10ms latency
- **PostgreSQL/MySQL** if: open-source relational database, flexible server with zone redundancy
- **Synapse Analytics** if: data warehouse, OLAP analytics, petabyte-scale
- **Azure Cache for Redis** if: in-memory caching, session store, pub/sub messaging

**Networking design:**
- **Single VNet** if: small footprint (<100 resources), single application
- **Hub-spoke VNet** if: multiple applications need connectivity, centralized network services (firewall, VPN)
- **VNet peering** if: VNets in same or different regions need connectivity
- **Private endpoints** vs **Service endpoints**: prefer private endpoints for dedicated private IP access

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
        "service_name": "Azure service name (e.g., App Service, Blob Storage, Functions)",
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
  "well_architected_alignment": {
    "reliability": "high | medium | low with justification",
    "security": "high | medium | low with justification",
    "cost_optimization": "high | medium | low with justification",
    "operational_excellence": "high | medium | low with justification",
    "performance_efficiency": "high | medium | low with justification"
  },
  "next_steps": ["array of actionable recommendations"]
}
```

**Additional T2 fields:**
```json
{
  "iac_code": {
    "type": "bicep | terraform",
    "files": [
      {
        "filename": "string (e.g., main.bicep, variables.tf)",
        "content": "string (Bicep or Terraform HCL code)",
        "description": "purpose of this configuration file"
      }
    ]
  },
  "security_configuration": {
    "rbac_assignments": [
      {
        "principal": "string (managed identity or service principal)",
        "role": "built-in or custom role name",
        "scope": "subscription | resource group | resource"
      }
    ],
    "nsg_rules": [
      {
        "name": "string",
        "direction": "Inbound | Outbound",
        "access": "Allow | Deny",
        "protocol": "TCP | UDP | *",
        "source": "CIDR or service tag",
        "destination": "CIDR or service tag",
        "port": "port range"
      }
    ],
    "encryption": {
      "at_rest": "services and encryption methods (Microsoft-managed or customer-managed)",
      "in_transit": "TLS configuration and certificate management"
    }
  },
  "monitoring": {
    "dashboards": "description of key metrics to monitor",
    "alert_rules": [
      {
        "metric": "string (e.g., CPU percentage, HTTP 5xx errors)",
        "threshold": "number",
        "action": "action group (email, SMS, webhook, runbook)"
      }
    ],
    "logs": "centralized logging strategy (Log Analytics workspace)"
  },
  "migration_plan": {
    "phases": [
      {
        "phase_number": "integer",
        "description": "string",
        "services_migrated": ["array of Azure services deployed"],
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
# App Service + Azure SQL + Blob Storage + Front Door

Services:
  Compute: App Service (Standard S1, autoscale 1-5 instances, .NET 8)
  Database: Azure SQL Database (General Purpose, 2 vCores, 32GB storage)
  Storage: Blob Storage (Hot tier, LRS, static assets + user uploads)
  CDN: Azure Front Door (global distribution, WAF enabled)
  Cache: Azure Cache for Redis (Basic C0, 250MB)
  Auth: Microsoft Entra ID (B2C for customer authentication)

Estimated Monthly Cost (10K users, 1M requests):
  App Service: $73 (Standard S1)
  Azure SQL: $115 (2 vCore General Purpose)
  Blob Storage: $5 (10GB Hot, 100K transactions)
  Front Door: $40 (1M requests, 100GB egress)
  Redis Cache: $17 (Basic C0)
  Total: ~$250/month

Cost Optimizations:
  - Use Reserved Instance for SQL Database (save 33-72%)
  - Move old blobs to Cool/Archive tiers
  - Consider App Service reserved capacity (save 20-40%)
```

(Full T2 Bicep example: `/resources/bicep-serverless-webapp/`)
(Full T2 Terraform example: `/resources/terraform-serverless-webapp/`)

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - service selection + cost estimate + Well-Architected summary
- **T2**: ≤6,000 tokens - detailed design + IaC templates + security + migration plan

**Safety checks:**
- No credentials or connection strings in IaC (use Key Vault references)
- RBAC assignments use built-in roles where possible (avoid overly permissive custom roles)
- NSG rules have no 0.0.0.0/0 ingress for RDP/SSH (use Azure Bastion)
- Storage Accounts have firewall rules or private endpoints configured
- Encryption enabled for all data stores (Blob Storage, Managed Disks, SQL Database)

**Auditability:**
- All Azure service recommendations cite official documentation with access date (NOW_ET)
- Cost estimates include calculation methodology (hours, DTUs, RU/s, GB-months)
- Well-Architected Framework pillars mapped to specific Azure services and configurations
- Compliance controls (if applicable) mapped to Azure Policy definitions

**Determinism:**
- Given same inputs, produce identical service selection recommendations
- Cost estimates use consistent Azure pricing (with discounts noted)
- Bicep/Terraform configurations follow Azure best practices

**Validation requirements:**
- T2 Bicep files must pass `az bicep build`
- T2 Terraform configurations must pass `terraform validate`
- RBAC assignments must use valid built-in or custom role names
- NSG rules must have valid CIDR blocks and port ranges

---

## Resources

**Official Azure Documentation (accessed 2025-10-26T14:45:00-04:00):**
- Azure Well-Architected Framework: https://learn.microsoft.com/en-us/azure/well-architected/
- Azure Architecture Center: https://learn.microsoft.com/en-us/azure/architecture/
- Azure Compute Services: https://azure.microsoft.com/en-us/products/category/compute/
- Azure Storage Services: https://azure.microsoft.com/en-us/products/category/storage/
- Azure Networking: https://learn.microsoft.com/en-us/azure/networking/
- Azure Compute Decision Tree: https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree

**Azure Service Documentation:**
- Virtual Machines: https://learn.microsoft.com/en-us/azure/virtual-machines/
- App Service: https://learn.microsoft.com/en-us/azure/app-service/
- Container Apps: https://learn.microsoft.com/en-us/azure/container-apps/
- Azure Functions: https://learn.microsoft.com/en-us/azure/azure-functions/
- Azure Kubernetes Service: https://learn.microsoft.com/en-us/azure/aks/
- Blob Storage: https://learn.microsoft.com/en-us/azure/storage/blobs/
- Azure SQL Database: https://learn.microsoft.com/en-us/azure/azure-sql/
- Cosmos DB: https://learn.microsoft.com/en-us/azure/cosmos-db/

**Infrastructure-as-Code:**
- Azure Bicep: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview
- Terraform on Azure: https://learn.microsoft.com/en-us/azure/developer/terraform/overview
- Terraform AzureRM Provider: https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs
- ARM Templates: https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/

**Cost Optimization:**
- Azure Pricing Calculator: https://azure.microsoft.com/en-us/pricing/calculator/
- Reserved VM Instances: https://azure.microsoft.com/en-us/pricing/reserved-vm-instances/
- Spot VMs: https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms
- Azure Hybrid Benefit: https://azure.microsoft.com/en-us/pricing/hybrid-benefit/
- Azure Cost Management: https://learn.microsoft.com/en-us/azure/cost-management-billing/

**Security Best Practices:**
- Azure RBAC: https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
- Managed Identities: https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/
- Azure Key Vault: https://learn.microsoft.com/en-us/azure/key-vault/
- Microsoft Defender for Cloud: https://learn.microsoft.com/en-us/azure/defender-for-cloud/
- Azure Policy: https://learn.microsoft.com/en-us/azure/governance/policy/

**Example Templates:**
- `/resources/bicep-serverless-webapp/` - Complete serverless web app with App Service, SQL Database, Blob Storage
- `/resources/terraform-aks-cluster/` - AKS cluster with autoscaling, workload identity, Azure CNI
- `/resources/rbac-assignments-examples.json` - Example RBAC role assignments with built-in roles
- `/resources/vnet-hub-spoke.bicep` - Hub-spoke VNet topology with Azure Firewall

**Migration Resources:**
- Azure Migrate: https://learn.microsoft.com/en-us/azure/migrate/
- Database Migration Service: https://learn.microsoft.com/en-us/azure/dms/
- App Service Migration Assistant: https://azure.microsoft.com/en-us/services/app-service/migration-assistant/
- Azure TCO Calculator: https://azure.microsoft.com/en-us/pricing/tco/calculator/
