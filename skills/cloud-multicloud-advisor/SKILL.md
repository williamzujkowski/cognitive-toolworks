---
name: Multi-Cloud Strategy Advisor
slug: cloud-multicloud-advisor
description: Design multi-cloud and hybrid cloud strategies with vendor selection, integration patterns, TCO analysis, and lock-in mitigation.
capabilities:
  - Compare cloud vendor capabilities across AWS, Azure, GCP
  - Design cloud-agnostic architectures and integration patterns
  - Calculate and optimize Total Cost of Ownership (TCO) across clouds
  - Recommend vendor lock-in mitigation strategies
  - Generate multi-cloud deployment roadmaps
inputs:
  - Business requirements (latency, compliance, budget constraints)
  - Current infrastructure inventory (on-prem, cloud, hybrid)
  - Workload characteristics (compute, storage, network demands)
  - Risk tolerance and exit strategy requirements
outputs:
  - Vendor comparison matrix with scoring
  - Multi-cloud architecture diagram
  - TCO analysis with 3/5/7 year projections
  - Integration pattern recommendations
  - Phased migration roadmap
keywords:
  - multi-cloud
  - hybrid-cloud
  - vendor-selection
  - cloud-strategy
  - TCO
  - vendor-lock-in
  - AWS
  - Azure
  - GCP
  - cloud-agnostic
version: 1.0.0
owner: cognitive-toolworks
license: Apache-2.0
security: Public skill - no PII/secrets; uses public cloud vendor documentation
links:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-education-hybrid-multicloud/introduction.html
  - https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/hybrid/enterprise-scale-landing-zone
  - https://cloud.google.com/anthos
  - https://www.cncf.io/
  - https://library.educause.edu/resources/2015/4/tco-for-cloud-services-a-framework
  - https://buzzclan.com/cloud/vendor-lock-in/
---

## Purpose & When-To-Use

Invoke this skill when:

* Designing a **multi-cloud strategy** that spans AWS, Azure, GCP, or other providers
* Evaluating **vendor lock-in risks** and need mitigation strategies
* Performing **vendor selection** with objective capability comparison
* Calculating **Total Cost of Ownership (TCO)** across multiple cloud platforms
* Planning **hybrid cloud** architectures that integrate on-premises with multiple clouds
* Designing **cloud-agnostic** abstractions and integration patterns
* Conducting **cloud cost arbitrage** analysis for workload placement

**Do NOT use** for single-cloud optimization (use cloud-aws-architect instead) or Kubernetes-only deployments (use cloud-native-deployment-orchestrator).

## Pre-Checks

1. **Time normalization**: `NOW_ET = 2025-10-25T21:30:36-04:00` (NIST/time.gov semantics)
2. **Input validation**:
   * Business requirements specify at least one: latency targets, compliance needs, or budget constraints
   * Workload characteristics include compute/storage/network demands or current infrastructure inventory
   * Risk tolerance defined: low (accept lock-in), medium (prefer portability), high (require multi-cloud)
3. **Source freshness**: All vendor documentation links accessed on `NOW_ET`; verify pricing/features current within 90 days
4. **Abort conditions**:
   * If requirements clearly fit single cloud provider → route to cloud-aws-architect
   * If purely Kubernetes deployment → route to cloud-native-deployment-orchestrator
   * If missing all business requirements → request clarification

## Procedure

### T1: Quick Multi-Cloud Assessment (≤2k tokens)

**Trigger**: Initial vendor selection or high-level strategy question

**Steps**:
1. **Parse requirements** to extract:
   * Compliance mandates (FedRAMP, GDPR, HIPAA) → filter vendors by region/certification
   * Latency requirements (<100ms) → identify required regions/edge locations
   * Budget constraints → tier vendors by cost profile
2. **Apply decision matrix** (accessed 2025-10-25T21:30:36-04:00):
   * **AWS**: Broadest service catalog (200+ services), strongest enterprise adoption, best for hybrid via AWS Outposts (https://aws.amazon.com/hybrid/)
   * **Azure**: Best Microsoft integration (AD, Office 365), strong hybrid via Azure Arc (https://learn.microsoft.com/en-us/azure/azure-arc/overview accessed 2025-10-25T21:30:36-04:00), 60+ compliance certifications
   * **GCP**: Best for data analytics (BigQuery), Kubernetes-native via Anthos (https://cloud.google.com/anthos accessed 2025-10-25T21:30:36-04:00), competitive ML platform (Vertex AI)
3. **Generate recommendation**:
   * If 1 vendor meets >90% requirements → **single-cloud** (cite rationale)
   * If 2-3 vendors needed → **multi-cloud** (proceed to T2)
   * If on-prem integration required → **hybrid cloud** (proceed to T2)

**Output**: Vendor shortlist (1-3 providers) with one-sentence justification each

### T2: Multi-Cloud Strategy Design (≤6k tokens)

**Trigger**: Multi-cloud or hybrid architecture needed; TCO analysis required

**Steps**:
1. **Vendor capability comparison** (sources accessed 2025-10-25T21:30:36-04:00):
   * **Compute**: EC2 (AWS) vs Azure VMs vs Compute Engine (GCP) → scoring: flexibility, pricing, reserved instance discounts
   * **Storage**: S3 vs Blob Storage vs Cloud Storage → scoring: durability (11 9's), egress costs, lifecycle policies
   * **Networking**: VPC vs VNet vs VPC → scoring: peering options, bandwidth costs, global backbone quality
   * **Serverless**: Lambda vs Functions vs Cloud Functions → scoring: cold start times, concurrency limits, pricing model
   * **Kubernetes**: EKS vs AKS vs GKE → scoring: control plane cost ($0.10/hr AWS vs free Azure/GCP), auto-scaling, version lag
   * **Hybrid**: Outposts vs Arc vs Anthos → scoring: hardware ownership, management overhead, multi-cloud support

2. **TCO calculation framework** (https://library.educause.edu/resources/2015/4/tco-for-cloud-services-a-framework accessed 2025-10-25T21:30:36-04:00):
   * **Compute costs**: Instance hours × (on-demand rate OR reserved instance rate with 30-70% discount)
   * **Storage costs**: GB-months × storage tier rate + request costs + egress costs (major cost driver)
   * **Network costs**: Intra-region (free), inter-region ($0.01-0.02/GB), internet egress ($0.08-0.12/GB first 10TB)
   * **Managed services**: RDS/SQL Database/Cloud SQL → add 30-50% premium over self-managed
   * **Hidden costs**: Support (3-10% of monthly spend), training, certification, multi-cloud tooling
   * **Time horizons**: 3-year (standard), 5-year (enterprise), 7-year (government)
   * **TCO formula**: `TCO = (Compute + Storage + Network + Services + Support + Training + Tooling) × Time Horizon`

3. **Integration pattern selection** (CNCF cloud-native patterns https://www.cncf.io/ accessed 2025-10-25T21:30:36-04:00):
   * **Cloud-agnostic abstraction layer**:
     - **Infrastructure as Code**: Terraform/Pulumi for multi-cloud provisioning (not CloudFormation/ARM/Deployment Manager)
     - **Orchestration**: Kubernetes (EKS/AKS/GKE) for workload portability
     - **Service mesh**: Istio/Linkerd for cross-cloud service discovery and mTLS
   * **Data integration**:
     - **Replication**: Bidirectional (active-active) vs unidirectional (DR)
     - **Event streaming**: Kafka (self-managed) or Confluent Cloud (multi-cloud SaaS)
     - **ETL/ELT**: Airbyte, Fivetran for cross-cloud data pipelines
   * **Identity federation**:
     - **SAML/OIDC**: Single sign-on across AWS (IAM Identity Center), Azure (Entra ID), GCP (Cloud Identity)
     - **Workload identity**: SPIFFE/SPIRE for zero-trust service authentication
   * **Network connectivity**:
     - **VPN**: Site-to-site IPSec for low-bandwidth (<1Gbps)
     - **Direct connect**: AWS Direct Connect, Azure ExpressRoute, GCP Interconnect for high-bandwidth (1-100Gbps)
     - **SD-WAN**: Multi-cloud overlay network (Cisco Viptela, VMware VeloCloud)

4. **Vendor lock-in mitigation** (https://buzzclan.com/cloud/vendor-lock-in/ accessed 2025-10-25T21:30:36-04:00):
   * **Data portability**: Use open formats (Parquet, Avro, ORC) not proprietary (DynamoDB format, Cosmos DB)
   * **API abstraction**: Abstract vendor-specific APIs (S3 SDK → MinIO-compatible API)
   * **Containerization**: Package workloads in OCI containers (not Lambda/Functions/Cloud Functions)
   * **Schema portability**: Use PostgreSQL/MySQL (available on all clouds) not Aurora/CosmosDB/Spanner
   * **Exit strategy**: Test restore/migration quarterly; maintain cross-cloud DR every 6 months
   * **Top mitigation strategies** (accessed 2025-10-25T21:30:36-04:00):
     - Make informed decisions before vendor selection (66.4% organizations)
     - Maintain open environment for continuous competition (52.3%)
     - Use standard software components with proven interfaces (39.3%)

5. **Generate deliverables**:
   * **Vendor comparison matrix**: JSON with vendor, service, score (0-10), justification
   * **TCO spreadsheet schema**: Columns: vendor, category, unit_cost, quantity, subtotal, 3yr/5yr/7yr totals
   * **Architecture diagram**: Text-based (PlantUML/Mermaid) showing cloud boundaries, integration points, data flows
   * **Migration roadmap**: Phases (assess → pilot → migrate → optimize), duration, dependencies, rollback plan

**Output**: Complete multi-cloud strategy package (vendor matrix, TCO analysis, architecture, roadmap)

### T3: Deep Analysis (Out of Scope for T2)

T3 tier not implemented. For deep dives:
* **Cost optimization** → invoke finops-cost-analyzer
* **Security hardening** → invoke security-assessment-framework with security-zerotrust-architect
* **Kubernetes federation** → invoke cloud-native-deployment-orchestrator

## Decision Rules

1. **Vendor selection threshold**:
   * Score delta <10% → **tie** → select by strategic fit (existing skills, partnerships)
   * Score delta 10-30% → **slight preference** → validate with pilot
   * Score delta >30% → **clear winner** → proceed with confidence

2. **Multi-cloud vs hybrid**:
   * If compliance requires data residency → **hybrid** (on-prem + cloud)
   * If workload portability >70% → **multi-cloud** (2+ public clouds)
   * If vendor diversification risk mitigation → **multi-cloud**
   * Else → **single-cloud** (simplicity wins)

3. **TCO ambiguity handling**:
   * If egress costs >30% of total → flag for optimization (CDN, regional caching)
   * If reserved instance savings >40% → mandate 1-year commitments
   * If support costs >10% → review tier (business vs enterprise)

4. **Abort conditions**:
   * If user requests implementation details → stop; emit architecture and route to cloud-native-deployment-orchestrator
   * If data sovereignty conflicts with vendor regions → stop; document blockers

## Output Contract

**JSON Schema**:

```json
{
  "strategy_type": "multi-cloud | hybrid-cloud | single-cloud",
  "vendors": [
    {
      "name": "AWS | Azure | GCP | Other",
      "role": "primary | secondary | DR",
      "services": ["compute", "storage", "network", "managed-services"],
      "score": 0-10,
      "justification": "string (≤160 chars)"
    }
  ],
  "tco_analysis": {
    "time_horizon_years": 3 | 5 | 7,
    "total_tco_usd": "number",
    "breakdown": {
      "compute": "number",
      "storage": "number",
      "network": "number",
      "managed_services": "number",
      "support": "number",
      "training_tooling": "number"
    },
    "comparison": "string (vendor A $X vs vendor B $Y over N years)"
  },
  "integration_patterns": [
    {
      "pattern": "IaC | Kubernetes | Service Mesh | Event Streaming | Identity Federation",
      "tool": "string (Terraform, Istio, Kafka, etc.)",
      "rationale": "string (≤100 chars)"
    }
  ],
  "lock_in_mitigation": [
    {
      "risk": "data | API | schema | network",
      "mitigation": "string",
      "priority": "high | medium | low"
    }
  ],
  "roadmap": [
    {
      "phase": "assess | pilot | migrate | optimize",
      "duration_weeks": "number",
      "deliverables": ["string"],
      "dependencies": ["string"]
    }
  ],
  "sources": [
    {
      "title": "string",
      "url": "string",
      "access_date": "2025-10-25T21:30:36-04:00"
    }
  ]
}
```

**Required fields**: `strategy_type`, `vendors` (≥1), `tco_analysis`, `integration_patterns`, `roadmap`

## Examples

```yaml
# Input: Global SaaS, <50ms latency, GDPR/HIPAA, $500k/yr
requirements: {latency: <50ms, compliance: [GDPR, HIPAA],
  workloads: {vms: 100, db: 50TB, ml: GPU}, risk: medium}

# Output (T2): Multi-cloud AWS+GCP
strategy_type: multi-cloud
vendors:
  - {name: AWS, role: primary, score: 8.5,
     justification: 30 regions global}
  - {name: GCP, role: ML/analytics, score: 9.0,
     justification: Vertex AI best}
tco_5yr: $2.1M {compute: $1.2M, storage: $300k,
  network: $400k, services: $100k, support: $80k}
integration_patterns:
  - {pattern: IaC, tool: Terraform}
  - {pattern: K8s, tool: EKS+GKE}
lock_in_mitigation:
  - {risk: data, mitigation: Parquet, priority: high}
  - {risk: API, mitigation: Abstract SDKs, priority: high}
roadmap:
  - {phase: pilot, weeks: 8, deliverables: [POC AWS+GCP]}
  - {phase: migrate, weeks: 16, deliverables: [blue/green]}
sources: [aws.amazon.com/hybrid, cloud.google.com/anthos,
  cncf.io] (accessed 2025-10-25T21:30:36-04:00)
```

## Quality Gates

1. **Token budgets**:
   * T1 ≤ 2k tokens (vendor shortlist only)
   * T2 ≤ 6k tokens (full strategy with TCO, architecture, roadmap)
   * T3 not implemented (route to specialized skills)

2. **Safety**:
   * No secrets or credentials in outputs
   * Pricing data cited with access dates (must be <90 days old)
   * Compliance claims verified against official vendor docs

3. **Auditability**:
   * Every TCO assumption documented (instance types, storage tiers, network estimates)
   * Every vendor score justified with comparison criteria
   * Sources include title, URL, and `NOW_ET` access date

4. **Determinism**:
   * Same inputs → same vendor scores (no randomness)
   * TCO calculations reproducible (explicit formulas)
   * Decision rules transparent and consistent

5. **Abort on uncertainty**:
   * If pricing data >90 days old → request manual verification
   * If workload characteristics ambiguous → request clarification
   * If compliance conflicts detected → stop and document

## Resources

### Official Vendor Documentation
* **AWS Hybrid/Multi-Cloud**: https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-education-hybrid-multicloud/introduction.html (accessed 2025-10-25T21:30:36-04:00)
* **AWS Hybrid Best Practices**: https://docs.aws.amazon.com/prescriptive-guidance/latest/hybrid-cloud-best-practices/introduction.html (accessed 2025-10-25T21:30:36-04:00)
* **Azure Arc Overview**: https://learn.microsoft.com/en-us/azure/azure-arc/overview (accessed 2025-10-25T21:30:36-04:00)
* **Azure Hybrid Landing Zones**: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/hybrid/enterprise-scale-landing-zone (accessed 2025-10-25T21:30:36-04:00)
* **Google Anthos**: https://cloud.google.com/anthos (accessed 2025-10-25T21:30:36-04:00)

### Standards & Frameworks
* **CNCF Cloud Native Projects**: https://www.cncf.io/ (accessed 2025-10-25T21:30:36-04:00)
* **CNCF Cloud Native Maturity Model 4.0**: https://www.cncf.io/blog/2025/10/22/cloud-native-maturity-model-4-0-beta-reflecting-whats-next-for-cloud-native-and-we-want-your-input/ (accessed 2025-10-25T21:30:36-04:00)
* **TCO Framework (EDUCAUSE)**: https://library.educause.edu/resources/2015/4/tco-for-cloud-services-a-framework (accessed 2025-10-25T21:30:36-04:00)

### Vendor Lock-In Mitigation
* **Vendor Lock-In Prevention Guide 2025**: https://buzzclan.com/cloud/vendor-lock-in/ (accessed 2025-10-25T21:30:36-04:00)
* **Managing Technical Lock-In (UK Gov)**: https://www.gov.uk/guidance/managing-technical-lock-in-in-the-cloud (accessed 2025-10-25T21:30:36-04:00)

### Multi-Cloud Patterns
* **Multi-Cloud Architecture 2025**: https://futransolutions.com/blog/multi-cloud-architecture-2025-the-blueprint-for-future-ready-enterprises/ (accessed 2025-10-25T21:30:36-04:00)

### Resource Files (in resources/)
* `vendor-comparison-matrix.json` - Template for scoring AWS/Azure/GCP across service categories
* `tco-calculator-template.csv` - Spreadsheet template with formulas for 3/5/7 year projections
* `integration-patterns.md` - Common multi-cloud integration patterns with Terraform/Kubernetes examples
