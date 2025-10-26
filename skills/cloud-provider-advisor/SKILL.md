---
name: "Cloud Provider Selection Advisor"
slug: "cloud-provider-advisor"
description: "Compare AWS, GCP, and Azure to select the best cloud provider based on workload requirements, cost, compliance, and migration complexity."
capabilities:
  - Service comparison matrix (compute, storage, database, networking)
  - Cost model analysis (pricing, discounts, commitments across providers)
  - Regional coverage and compliance assessment (FedRAMP, HIPAA, ISO 27001)
  - Migration complexity evaluation (current state → target cloud)
  - Multi-cloud and hybrid strategy recommendations
  - Vendor lock-in risk assessment
  - Ecosystem maturity comparison (tooling, SDKs, community)
inputs:
  - requirements: "functional and non-functional requirements (object with performance, security, cost, compliance)"
  - workload_type: "web-app, data-processing, real-time, batch, machine-learning, hybrid (string)"
  - current_state: "existing infrastructure (on-premises, AWS, GCP, Azure, multi-cloud) (string, optional)"
  - priorities: "ranked list of decision factors (cost, performance, compliance, ecosystem, migration-ease) (array)"
  - constraints: "hard requirements (region, compliance, vendor preferences) (object, optional)"
outputs:
  - recommendation: "primary cloud provider with detailed rationale"
  - service_mapping: "equivalent services across AWS/GCP/Azure for workload"
  - cost_comparison: "estimated costs across providers with discount strategies"
  - migration_assessment: "migration complexity and timeline if applicable"
  - multi_cloud_strategy: "when and how to use multiple providers (if applicable)"
keywords:
  - cloud-comparison
  - aws
  - gcp
  - azure
  - cloud-selection
  - multi-cloud
  - vendor-comparison
  - cost-comparison
  - migration-planning
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://aws.amazon.com/
  - https://cloud.google.com/
  - https://azure.microsoft.com/
  - https://www.gartner.com/en/documents/cloud-infrastructure-services
---

## Purpose & When-To-Use

**Trigger conditions:**
- Choosing cloud provider for new project or workload
- Evaluating migration from on-premises to cloud
- Switching cloud providers for cost or feature reasons
- Designing multi-cloud or hybrid cloud strategy
- Comparing specific services across AWS, GCP, Azure
- Assessing vendor lock-in risk and mitigation strategies
- Compliance-driven cloud selection (FedRAMP, HIPAA, ISO 27001)

**Not for:**
- Deep architecture design within a single cloud (use cloud-aws-architect, cloud-gcp-architect, cloud-azure-architect)
- Detailed cost optimization within one provider (use finops-cost-analyzer)
- Kubernetes-only deployment (cloud-agnostic, use cloud-kubernetes-integrator)
- Edge computing or CDN-specific decisions (use cloud-edge-architect)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T18:00:00-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `requirements` must include at least one priority: cost, performance, security, compliance
- `workload_type` must be one of: web-app, data-processing, real-time, batch, machine-learning, hybrid
- `priorities` must be ranked list (highest priority first)
- `constraints` if provided must specify hard requirements (e.g., "must support eu-west-1", "must have FedRAMP High")

**Source freshness:**
- AWS Well-Architected Framework (accessed 2025-10-26T18:00:00-04:00): https://aws.amazon.com/architecture/well-architected/
- GCP Architecture Framework (accessed 2025-10-26T18:00:00-04:00): https://cloud.google.com/architecture/framework
- Azure Well-Architected Framework (accessed 2025-10-26T18:00:00-04:00): https://learn.microsoft.com/en-us/azure/well-architected/
- Gartner Magic Quadrant for Cloud Infrastructure (accessed 2025-10-26T18:00:00-04:00): https://www.gartner.com/en/documents/cloud-infrastructure-services

---

## Procedure

### T1: Quick Provider Recommendation (≤2k tokens)

**Fast path for 80% of cloud selection decisions:**

1. **Service equivalence mapping:**

   | Category | AWS | GCP | Azure |
   |----------|-----|-----|-------|
   | **Compute (VMs)** | EC2 | Compute Engine | Virtual Machines |
   | **Compute (Serverless)** | Lambda | Cloud Functions | Functions |
   | **Compute (Containers)** | ECS/Fargate | Cloud Run | Container Apps |
   | **Compute (K8s)** | EKS | GKE | AKS |
   | **Object Storage** | S3 | Cloud Storage | Blob Storage |
   | **Block Storage** | EBS | Persistent Disk | Managed Disks |
   | **Relational DB** | RDS/Aurora | Cloud SQL | SQL Database |
   | **NoSQL** | DynamoDB | Firestore/Bigtable | Cosmos DB |
   | **Data Warehouse** | Redshift | BigQuery | Synapse Analytics |
   | **Networking** | VPC | VPC | Virtual Network |
   | **Load Balancer** | ALB/NLB | Cloud Load Balancing | Load Balancer/App Gateway |
   | **CDN** | CloudFront | Cloud CDN | Front Door |

2. **Cost model comparison:**

   **AWS:**
   - Pricing: On-demand, Savings Plans (1-3 year), Spot (up to 90% discount)
   - Free tier: 12 months (EC2 t2.micro 750hrs, S3 5GB, RDS 750hrs)
   - Billing: Per-second (EC2/Fargate), per-request (Lambda), per-GB-month (S3)

   **GCP:**
   - Pricing: On-demand, Committed Use Discounts (1-3 year, up to 70%), Spot VMs (60-91% discount)
   - Free tier: Always free (Cloud Run 2M requests, Cloud Functions 2M invocations, Compute Engine e2-micro)
   - Billing: Per-second (all compute), sustained use discounts (automatic 20-30% for consistent usage)

   **Azure:**
   - Pricing: On-demand, Reserved Instances (1-3 year, up to 72%), Spot VMs (variable)
   - Free tier: 12 months (VMs B1S 750hrs, Blob Storage 5GB, SQL Database 250GB)
   - Billing: Per-second (VMs), per-execution (Functions), per-DTU/vCore (SQL Database)
   - Azure Hybrid Benefit: Up to 80% savings with Windows Server/SQL Server licenses

3. **Quick decision criteria:**

   **Choose AWS if:**
   - Broadest service catalog (200+ services)
   - Largest global footprint (33 regions, 105 availability zones)
   - Mature ecosystem and largest market share (32% global market)
   - Enterprise-grade compliance (FedRAMP High, DoD IL5, HIPAA)
   - Strong serverless capabilities (Lambda, Step Functions, EventBridge)

   **Choose GCP if:**
   - Data analytics and machine learning focus (BigQuery, Vertex AI, TensorFlow)
   - Kubernetes-native workloads (GKE is most mature managed K8s)
   - Automatic cost optimization (sustained use discounts without commitment)
   - Developer-friendly APIs and tooling (gcloud CLI, Cloud Shell)
   - Open-source and multi-cloud compatibility (Anthos, Terraform)

   **Choose Azure if:**
   - Microsoft ecosystem integration (Active Directory, Office 365, Dynamics 365)
   - Hybrid cloud requirements (Azure Arc, Azure Stack)
   - Windows Server and SQL Server workloads (Azure Hybrid Benefit)
   - Enterprise agreements and licensing flexibility
   - Strong regional presence in Europe and government clouds

4. **Migration complexity assessment:**

   **From on-premises:**
   - AWS: AWS Migration Hub, Database Migration Service (DMS), Server Migration Service
   - GCP: Migrate to Virtual Machines, Database Migration Service, Transfer Service
   - Azure: Azure Migrate, Database Migration Service, Azure Site Recovery

   **From AWS to GCP/Azure:**
   - Complexity: Medium to High (service mapping, IAM translation, networking redesign)
   - Timeline: 3-6 months for small apps, 12-24 months for large enterprises
   - Tools: CloudEndure, Velostrata, third-party migration platforms

   **From GCP to AWS/Azure:**
   - Complexity: Medium (fewer proprietary services, Kubernetes portability)
   - Timeline: 3-6 months for containerized apps, 6-12 months for GCP-native services
   - Tools: Terraform for IaC translation, Kubernetes manifest migration

5. **Output (T1):**
   - Primary cloud provider recommendation with 3-5 bullet justification
   - Service mapping table for workload
   - Rough monthly cost estimate across providers (±30% accuracy)
   - Migration complexity rating (Low/Medium/High) if applicable
   - Vendor lock-in assessment and mitigation strategies

**Abort conditions:**
- Requirements conflict (e.g., "cheapest possible + must use AWS")
- Insufficient workload details to map services
- Specialized requirements needing vendor consultation (e.g., quantum computing, specialized hardware)

---

### T2: Detailed Multi-Cloud Strategy (≤6k tokens)

**For complex cloud selection with detailed comparison:**

1. **All T1 steps** plus:

2. **Comprehensive service comparison:**

   **Compute tier:**
   - **Serverless**: AWS Lambda (15min timeout) vs GCP Cloud Functions (9min) vs Azure Functions (10min)
   - **Containers**: AWS ECS/Fargate (AWS-specific) vs GCP Cloud Run (serverless, Knative) vs Azure Container Apps (Dapr integration)
   - **Kubernetes**: AWS EKS vs GCP GKE (most mature, Autopilot mode) vs Azure AKS (Azure AD integration)
   - **VMs**: AWS EC2 (broadest instance types) vs GCP Compute Engine (custom machine types) vs Azure VMs (Azure Hybrid Benefit)

   **Storage tier:**
   - **Object Storage**: AWS S3 (industry standard, 11 9s durability) vs GCP Cloud Storage (uniform API, multi-region) vs Azure Blob Storage (Hot/Cool/Archive tiers)
   - **Block Storage**: AWS EBS (io2 Block Express 256K IOPS) vs GCP Persistent Disk (flexible sizing) vs Azure Managed Disks (Ultra Disk 160K IOPS)
   - **File Storage**: AWS EFS (NFS) vs GCP Filestore (NFS/SMB) vs Azure Files (SMB, AD integration)

   **Database tier:**
   - **Relational**: AWS Aurora (MySQL/PostgreSQL compatible, 5x perf) vs GCP Cloud SQL (managed PostgreSQL/MySQL) vs Azure SQL Database (SQL Server compatibility)
   - **NoSQL**: AWS DynamoDB (key-value, single-digit ms) vs GCP Firestore (document, real-time) vs Azure Cosmos DB (multi-model, 5 consistency levels)
   - **Global**: AWS DynamoDB Global Tables vs GCP Cloud Spanner (strong consistency) vs Azure Cosmos DB (turnkey global distribution)
   - **Analytics**: AWS Redshift (columnar, Spectrum) vs GCP BigQuery (serverless, petabyte-scale) vs Azure Synapse Analytics (unified analytics)

3. **Cost comparison deep-dive:**

   **Compute cost example (4 vCPU, 16GB RAM, 730 hrs/month):**
   - AWS: EC2 m5.xlarge on-demand $140/mo, 1-yr Savings Plan $91/mo (35% savings), Spot $28/mo (80% savings)
   - GCP: n2-standard-4 on-demand $122/mo, 1-yr CUD $73/mo (40% savings), Spot VMs $24-$49/mo (60-80% savings)
   - Azure: Standard D4s v3 on-demand $140/mo, 1-yr Reserved $91/mo (35% savings), Spot $28-$70/mo (variable)

   **Storage cost example (1TB object storage, 100K requests/month):**
   - AWS: S3 Standard $23/mo + requests $0.40 = $23.40/mo, Glacier $4/mo (archival)
   - GCP: Cloud Storage Standard $20/mo + requests $0.40 = $20.40/mo, Archive $1.20/mo
   - Azure: Blob Hot $18/mo + requests $0.44 = $18.44/mo, Archive $1/mo

   **Data transfer costs (100GB outbound/month):**
   - AWS: $9/100GB (first 10TB)
   - GCP: $12/100GB (first 1TB)
   - Azure: $8.70/100GB (first 10TB)

4. **Compliance and regional coverage:**

   **FedRAMP:**
   - AWS: FedRAMP High (us-gov-east-1, us-gov-west-1)
   - GCP: FedRAMP High (us-east4, us-west2)
   - Azure: FedRAMP High (Government regions: usgovvirginia, usgovtexas)

   **HIPAA:**
   - AWS: Business Associate Agreement (BAA) available for most services
   - GCP: HIPAA-compliant with BAA, best for healthcare analytics (BigQuery)
   - Azure: HIPAA/HITECH compliant, strong healthcare integration (HL7 FHIR)

   **Data residency:**
   - AWS: 33 regions globally, most granular region control
   - GCP: 40 regions, strong presence in Asia-Pacific
   - Azure: 60+ regions, strongest European presence (GDPR compliance)

5. **Ecosystem and tooling:**

   **Developer experience:**
   - AWS: aws-cli (comprehensive), CloudFormation (YAML/JSON), CDK (TypeScript/Python)
   - GCP: gcloud CLI (intuitive), Terraform (GCP preference), Deployment Manager
   - Azure: az CLI, ARM templates (JSON), Bicep (DSL), Azure PowerShell

   **CI/CD integration:**
   - AWS: CodePipeline, CodeBuild, CodeDeploy (AWS-specific)
   - GCP: Cloud Build, Cloud Deploy (GKE-native)
   - Azure: Azure DevOps (strongest integration with GitHub, Microsoft stack)

   **Monitoring and observability:**
   - AWS: CloudWatch (comprehensive), X-Ray (tracing), Cost Explorer
   - GCP: Cloud Monitoring (Stackdriver), Cloud Trace, Cloud Profiler
   - Azure: Azure Monitor, Application Insights (best APM), Log Analytics

6. **Multi-cloud strategy recommendations:**

   **When to use multi-cloud:**
   - Avoid vendor lock-in (distribute workloads across AWS, GCP, Azure)
   - Leverage best-of-breed services (BigQuery on GCP, Lambda on AWS, Azure AD on Azure)
   - Compliance requirements (data residency in multiple jurisdictions)
   - Disaster recovery and business continuity (cross-cloud failover)
   - Mergers and acquisitions (consolidate different cloud footprints)

   **Multi-cloud patterns:**
   - **Best-of-breed**: Use AWS Lambda, GCP BigQuery, Azure AD (manage via Terraform, Pulumi)
   - **Primary + DR**: AWS primary, Azure secondary (cross-cloud replication, Route 53/Traffic Manager failover)
   - **Data distribution**: Data processing in GCP (BigQuery), application in AWS (ECS), identity in Azure (AD)
   - **Geographic**: AWS in US, GCP in APAC, Azure in Europe (latency optimization)

   **Multi-cloud challenges:**
   - **Complexity**: Multiple IaC tools, separate monitoring, cross-cloud networking
   - **Cost**: Egress charges (AWS→GCP: $0.02-0.09/GB, AWS→Azure: similar)
   - **Skillset**: Team needs expertise in multiple clouds
   - **Support**: Separate support contracts, fragmented troubleshooting

7. **Vendor lock-in mitigation:**

   **High lock-in risk:**
   - AWS: DynamoDB (proprietary NoSQL), Step Functions (workflow orchestration), SageMaker (ML platform)
   - GCP: BigQuery (analytics), Firestore (NoSQL), Vertex AI (ML platform)
   - Azure: Cosmos DB (multi-model NoSQL), Azure AD (identity), Synapse Analytics

   **Low lock-in risk:**
   - Kubernetes (portable across EKS, GKE, AKS)
   - PostgreSQL/MySQL (RDS, Cloud SQL, Azure Database)
   - Object storage (S3 API compatible with Cloud Storage, Blob Storage)
   - Terraform/Pulumi for IaC (cloud-agnostic)

   **Mitigation strategies:**
   - Use open-source databases (PostgreSQL, MySQL, MongoDB, Cassandra)
   - Containerize applications (Docker, Kubernetes)
   - Avoid proprietary services (DynamoDB → PostgreSQL, BigQuery → ClickHouse)
   - Abstract cloud services with APIs (use CDN abstraction layer instead of CloudFront/Cloud CDN/Front Door directly)

8. **Output (T2):**
   - Detailed cloud provider recommendation with comprehensive justification
   - Service-by-service comparison table with pros/cons
   - Accurate monthly cost estimate (±10% accuracy) across providers
   - Migration plan with timeline, phases, and tools (if applicable)
   - Multi-cloud strategy with specific architecture patterns (if applicable)
   - Vendor lock-in risk matrix with mitigation tactics
   - Next steps: contact sales, set up pilot, begin migration planning

**Abort conditions:**
- Proprietary hardware or software requirements (e.g., mainframe, specialized GPU)
- Geopolitical constraints (e.g., data sovereignty laws prohibiting certain clouds)
- Extreme scale requirements needing vendor-specific optimization (>1PB data, >100K req/sec)

---

### T3: Not Implemented

**Note:** This skill implements T1 (quick recommendations) and T2 (detailed comparison with multi-cloud strategy) tiers only. T2 provides comprehensive cloud provider comparison with service-by-service analysis, cost breakdowns, migration planning, and multi-cloud architecture patterns. For highly specialized scenarios requiring deeper vendor consultation (custom pricing negotiations, enterprise agreements, dedicated support contracts), engage directly with AWS, GCP, or Azure sales teams.

**Future T3 considerations:**
- Enterprise agreement negotiation strategies across providers
- Custom pricing analysis for >$1M/year cloud spend
- Dedicated support contract comparison (AWS Enterprise Support, GCP Premium Support, Azure Premier Support)
- Private cloud integration (AWS Outposts, Google Distributed Cloud, Azure Stack)
- Specialized compliance frameworks (ITAR, CUI, classified workloads)
- Quantum computing and emerging technology roadmaps

---

## Decision Rules

**Primary cloud selection:**

**AWS if:**
- Broadest service catalog needed (AI/ML, IoT, blockchain, quantum)
- Largest ecosystem and community support
- Enterprise compliance (FedRAMP High, DoD IL5)
- Existing AWS expertise or investment
- Serverless-first architecture

**GCP if:**
- Data analytics and BigQuery use case (petabyte-scale analytics)
- Kubernetes-native workloads (GKE Autopilot)
- Machine learning with TensorFlow/Vertex AI
- Open-source preference (Knative, Istio, Anthos)
- Automatic cost optimization (sustained use discounts)

**Azure if:**
- Microsoft ecosystem (Windows Server, SQL Server, Active Directory, Office 365)
- Hybrid cloud requirements (Azure Arc, Azure Stack)
- Enterprise agreement and licensing flexibility
- Strongest regional presence in Europe
- .NET or Microsoft-stack development

**Multi-cloud if:**
- Avoid vendor lock-in (distribute risk across providers)
- Best-of-breed services (BigQuery + Lambda + Azure AD)
- Compliance requires multiple providers (data residency)
- Mergers and acquisitions (legacy multi-cloud)

**Cost priority:**
1. GCP (sustained use discounts automatic, competitive pricing)
2. Azure (Reserved Instances + Hybrid Benefit can be cheapest for Windows/SQL)
3. AWS (Savings Plans flexible, but requires commitment planning)

**Performance priority:**
1. AWS (lowest latency globally, most regions)
2. GCP (fastest networking, best for data analytics)
3. Azure (strong in Europe and government clouds)

**Ease of migration:**
1. Azure (from on-premises Windows/SQL, Azure Migrate)
2. AWS (mature migration tools, largest partner ecosystem)
3. GCP (Kubernetes-native apps easiest, others more complex)

**Ambiguity handling:**
- If workload unclear → request architecture diagram, data flow
- If cost priority conflicts with compliance → present trade-off matrix
- If multi-cloud requested without justification → challenge with single-cloud simplicity benefits

**Stop conditions:**
- Requirements are contradictory (e.g., "must use AWS and GCP exclusively")
- Workload details insufficient to map services
- Specialized hardware/software needs (quantum, mainframe, proprietary)

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "recommendation": {
    "primary_provider": "aws | gcp | azure | multi-cloud",
    "rationale": ["array of 3-5 reasons for recommendation"],
    "confidence": "high | medium | low"
  },
  "service_mapping": {
    "compute": {
      "aws": "service name",
      "gcp": "service name",
      "azure": "service name",
      "recommended": "provider::service with justification"
    },
    "storage": "...",
    "database": "...",
    "networking": "..."
  },
  "cost_comparison": {
    "aws_monthly_usd": "number",
    "gcp_monthly_usd": "number",
    "azure_monthly_usd": "number",
    "cheapest": "provider",
    "optimization_strategies": ["array of discount/commitment options"]
  },
  "considerations": {
    "vendor_lock_in": "low | medium | high with services at risk",
    "migration_complexity": "low | medium | high (if applicable)",
    "compliance": ["array of compliance frameworks met"],
    "regional_coverage": "assessment of region availability"
  }
}
```

**Additional T2 fields:**
```json
{
  "detailed_service_comparison": [
    {
      "category": "compute | storage | database | networking",
      "aws": {"service": "name", "pros": [], "cons": []},
      "gcp": {"service": "name", "pros": [], "cons": []},
      "azure": {"service": "name", "pros": [], "cons": []}
    }
  ],
  "cost_breakdown": {
    "compute": {"aws": "number", "gcp": "number", "azure": "number"},
    "storage": {"aws": "number", "gcp": "number", "azure": "number"},
    "database": {"aws": "number", "gcp": "number", "azure": "number"},
    "networking": {"aws": "number", "gcp": "number", "azure": "number"}
  },
  "migration_plan": {
    "source": "current infrastructure",
    "target": "recommended provider",
    "complexity": "low | medium | high",
    "timeline": "string (e.g., 3-6 months)",
    "phases": ["array of migration phases"],
    "tools": ["array of migration tools"]
  },
  "multi_cloud_architecture": {
    "pattern": "best-of-breed | primary-dr | data-distribution | geographic",
    "providers": ["array of providers used"],
    "service_distribution": {"provider": ["array of services"]}
  }
}
```

---

## Examples

```yaml
# T1 Example: Startup Web Application

Requirements:
  workload_type: web-app
  priorities: [cost, developer-experience, scalability]
  constraints: {region: us-east, compliance: none}

Recommendation: GCP
Rationale:
  - Lowest cost with sustained use discounts (automatic 20-30% savings)
  - Developer-friendly gcloud CLI and Cloud Shell
  - Cloud Run for serverless containers (better than Lambda for web apps)
  - Free tier generous (Cloud Run 2M requests/month)

Service Mapping:
  Compute: Cloud Run (serverless containers, auto-scale 0-1000)
  Database: Cloud SQL PostgreSQL (managed, automated backups)
  Storage: Cloud Storage (static assets, 11 9s durability)
  CDN: Cloud CDN (integrated with Cloud Run)

Cost Estimate:
  GCP: $45/month (Cloud Run $15, Cloud SQL $25, Storage $5)
  AWS: $63/month (Lambda $20, RDS $35, S3 $8)
  Azure: $73/month (Functions $18, SQL Database $45, Blob $10)

Migration: N/A (greenfield project)
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - service mapping + cost comparison + recommendation
- **T2**: ≤6,000 tokens - detailed comparison + multi-cloud strategy + migration plan

**Accuracy requirements:**
- Service equivalents must be functionally equivalent (not just similar names)
- Cost estimates based on current pricing (as of NOW_ET)
- Regional coverage and compliance data verified (cite source with access date)

**Determinism:**
- Given same inputs and priorities, recommend same provider
- Cost calculations use consistent methodology across providers

---

## Resources

**Official Cloud Documentation (accessed 2025-10-26T18:00:00-04:00):**
- AWS: https://aws.amazon.com/
- GCP: https://cloud.google.com/
- Azure: https://azure.microsoft.com/

**Pricing Calculators:**
- AWS Pricing Calculator: https://calculator.aws/
- GCP Pricing Calculator: https://cloud.google.com/products/calculator
- Azure Pricing Calculator: https://azure.microsoft.com/en-us/pricing/calculator/

**Well-Architected Frameworks:**
- AWS: https://aws.amazon.com/architecture/well-architected/
- GCP: https://cloud.google.com/architecture/framework
- Azure: https://learn.microsoft.com/en-us/azure/well-architected/

**Migration Tools:**
- AWS Migration Hub: https://aws.amazon.com/migration-hub/
- GCP Migrate to Virtual Machines: https://cloud.google.com/migrate/virtual-machines
- Azure Migrate: https://azure.microsoft.com/en-us/products/azure-migrate/

**Third-Party Comparisons:**
- Gartner Magic Quadrant: https://www.gartner.com/en/documents/cloud-infrastructure-services
- Forrester Wave: https://www.forrester.com/report/the-forrester-wave-public-cloud-infrastructure-platforms/

**Related Skills:**
- Detailed architecture: `cloud-aws-architect`, `cloud-gcp-architect`, `cloud-azure-architect`
- Cost analysis: `finops-cost-analyzer`
- Multi-cloud: `cloud-multicloud-advisor`
- Kubernetes: `cloud-kubernetes-integrator`
