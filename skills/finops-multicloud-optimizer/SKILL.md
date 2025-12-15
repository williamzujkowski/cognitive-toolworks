---
name: Multi-Cloud Cost Optimizer
slug: finops-multicloud-optimizer
description: Optimize costs across AWS, GCP, Azure with cross-cloud waste detection, workload placement, commitment balancing, and unified FinOps.
capabilities:
  - Cross-cloud cost normalization and comparison (AWS + GCP + Azure)
  - Multi-cloud waste detection (duplicate resources, unused cross-cloud connectivity)
  - Workload placement optimization based on cost differentials
  - Commitment optimization across providers (RIs, SPs, CUDs balance)
  - Cross-cloud tagging compliance and unified cost allocation
  - Egress cost optimization (identify expensive inter-cloud data transfer)
  - Multi-cloud FinOps maturity assessment
inputs:
  - Cloud accounts array (provider, account_id, billing API access) for AWS, GCP, Azure
  - Optimization scope (all, compute, storage, network, data-transfer)
  - Business constraints (critical workloads, compliance, migration flexibility)
  - Time range (30d, 90d, 180d)
  - Cost allocation model (showback, chargeback, unified)
outputs:
  - Unified cost report with spend by provider and savings potential
  - Workload placement recommendations with migration ROI
  - Commitment balance plan across all cloud providers
  - Cross-cloud waste inventory with remediation actions
  - Prioritized action plan with effort and impact estimates
keywords:
  - multi-cloud cost optimization
  - cross-cloud finops
  - workload placement
  - commitment optimization
  - cloud cost arbitrage
  - multi-cloud waste detection
  - unified cost allocation
  - egress cost optimization
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  - Read-only access to billing APIs across all cloud providers
  - Secure aggregation of cost data (contains sensitive business intelligence)
  - No automated resource migration without approval
  - Audit logging of all cross-cloud recommendations
links:
  - https://www.finops.org/framework/
  - https://www.cloudzero.com/blog/finops-best-practices/
  - https://www.prosperops.com/blog/multi-cloud-cost-management-guide/
  - https://holori.com/20-best-finops-and-cloud-cost-management-tools-in-2025/
---

## Purpose & When-To-Use

**Primary trigger conditions:**

- Operating workloads across 2+ cloud providers (AWS, GCP, Azure) with monthly spend >$50k
- Seeking cost arbitrage opportunities by placing workloads on most cost-effective cloud
- Need unified view of waste and optimization opportunities across all clouds
- Balancing commitment purchases (RIs, Savings Plans, CUDs) across multiple providers
- High egress costs (>15% of total spend) from cross-cloud data transfer
- Executive request for multi-cloud cost consolidation and reduction
- FinOps team managing multiple cloud providers seeking unified optimization

**When NOT to use this skill:**

- Single cloud deployment → use finops-cost-analyzer instead
- Multi-cloud strategic planning phase → use cloud-multicloud-advisor first
- Real-time cost tracking → use native cloud dashboards
- Workloads cannot be migrated due to compliance/latency constraints

**Value proposition:** Identifies 20-35% additional savings beyond single-cloud optimization by leveraging cross-cloud price competition, workload placement optimization, and eliminating multi-cloud waste patterns. Organizations using multi-cloud cost optimization tools achieve 35-68% total cost reductions (CloudZero, accessed 2025-10-26T14:30:00-04:00).

## Pre-Checks

**Required inputs validation:**

```python
NOW_ET = "2025-10-26T14:30:00-04:00"

assert len(cloud_accounts) >= 2, "Multi-cloud optimization requires ≥2 cloud providers"
assert all(acc["billing_api_access"] for acc in cloud_accounts), "Billing API access required for all accounts"
assert time_range in ["30d", "90d", "180d"], "Valid time ranges: 30d, 90d, 180d"
assert optimization_scope in ["all", "compute", "storage", "network", "data-transfer"]

# Data freshness check
for account in cloud_accounts:
    if account["last_billing_sync"] > 48h:
        warn(f"{account['provider']} billing data stale; recommendations may be outdated")

# Minimum spend threshold check
total_monthly_spend = sum_monthly_spend(cloud_accounts)
if total_monthly_spend < 50000:
    suggest("Multi-cloud optimization most valuable for monthly spend >$50k")
```

**Authority checks:**

- **AWS:** Cost Explorer API enabled, `ce:GetCostAndUsage`, `organizations:ListAccounts` if using AWS Organizations
- **GCP:** Cloud Billing API enabled, `billing.accounts.get`, `billing.resourceCosts.list` permissions
- **Azure:** Cost Management API access, Reader role on subscriptions, `Microsoft.CostManagement/query/action` permission

**Source citations (accessed 2025-10-26T14:30:00-04:00):**

- FinOps Best Practices 2025: https://www.cloudzero.com/blog/finops-best-practices/
- Multi-Cloud Cost Management Guide: https://www.prosperops.com/blog/multi-cloud-cost-management-guide/
- Top 50 FinOps Tools 2025: https://holori.com/20-best-finops-and-cloud-cost-management-tools-in-2025/
- FinOps Framework (Multi-Cloud): https://www.finops.org/framework/

## Procedure

### Tier 1 (≤2k tokens): Quick Multi-Cloud Cost Health Check

**Goal:** Identify top 3 cross-cloud optimization opportunities in <5 minutes.

**Steps:**

1. **Fetch unified cost summary** for time_range across all providers
   - Normalize currency and time periods (AWS monthly, GCP daily, Azure daily → unified monthly)
   - Calculate total spend by provider and trend (% change from previous period)
   - Identify largest cost contributors by service category (compute, storage, network)

2. **Quick cross-cloud waste scan**
   - **Duplicate resources:** Same workload/data running on multiple clouds (accidental redundancy)
   - **Unused cross-cloud connectivity:** VPN tunnels, Direct Connect/ExpressRoute/Interconnect with zero traffic (last 30 days)
   - **Orphaned cross-cloud resources:** Load balancers, NAT gateways pointing to deleted resources
   - **Commitment under-utilization:** RIs/SPs/CUDs with <70% utilization across all clouds

3. **Cross-cloud price comparison** (same workload on different clouds)
   - Identify 5 largest compute workloads
   - Calculate equivalent cost on each cloud (normalize instance types: AWS m5.xlarge ≈ GCP n2-standard-4 ≈ Azure D4s v3)
   - Flag workloads with >20% cost differential for placement optimization

4. **Output quick wins** (3 highest impact items)
   - Example: "Migrate analytics workload from AWS Redshift to GCP BigQuery → save $3,200/month (55% reduction)"
   - Example: "Delete 6 unused AWS Direct Connect + Azure ExpressRoute connections → save $1,800/month"
   - Example: "Rebalance commitments: reduce AWS RI, increase GCP CUD → save $2,400/month"

**Token budget checkpoint:** ~1.8k tokens for API calls, normalization, analysis, output formatting.

### Tier 2 (≤6k tokens): Comprehensive Multi-Cloud Cost Optimization

**Goal:** Generate detailed cross-cloud optimization plan with quantified savings and migration recommendations.

**Extends T1 with:**

5. **Cross-cloud workload placement analysis**
   - Fetch detailed resource inventory (compute, database, storage) from all clouds
   - Calculate **unit economics** per cloud (cost per vCPU-hour, cost per GB storage, cost per 1M requests)
   - Identify **migration candidates** (workloads without hard dependencies on current cloud):
     - No compliance restrictions (data residency, FedRAMP, etc.)
     - No vendor-specific services (avoid migrating from Aurora/BigQuery/Cosmos DB)
     - Latency tolerance >50ms (can tolerate cross-region placement)
   - Calculate **migration cost vs savings ROI:**
     - Migration cost: data transfer (egress) + downtime + testing
     - Annual savings: (current_cloud_cost - target_cloud_cost) × 12
     - ROI = annual_savings / migration_cost (recommend if ROI >3x)

   **Example calculation (accessed 2025-10-26T14:30:00-04:00):**
   ```
   Workload: 500TB PostgreSQL database + 50 vCPU app tier
   Current: AWS RDS Aurora PostgreSQL $12,000/month, EC2 m5.4xlarge reserved $1,500/month
   Target: GCP Cloud SQL PostgreSQL $7,200/month, n2-standard-16 CUD $900/month
   Monthly savings: $5,400/month
   Migration cost: 500TB egress ($45,000) + 2 weeks downtime ($10,000) = $55,000
   Annual savings: $64,800
   ROI: $64,800 / $55,000 = 1.18x → recommend if strategic, defer if purely financial
   ```

6. **Commitment optimization across clouds**
   - Analyze commitment coverage across all providers:
     - AWS: Reserved Instances + Compute/EC2 Savings Plans coverage
     - GCP: Committed Use Discounts (resource-based and spend-based)
     - Azure: Reserved VM Instances + Azure Hybrid Benefit
   - Calculate **blended commitment rate** (weighted average discount across clouds)
   - Identify **under-committed clouds** (on-demand spend >50%) and **over-committed clouds** (RI/CUD utilization <80%)
   - Recommend **commitment rebalancing**:
     - Reduce commitments on expensive/declining clouds
     - Increase commitments on cost-effective/growing clouds
     - Target: 70-85% commitment coverage across all clouds (sweet spot)

   **Sources (accessed 2025-10-26T14:30:00-04:00):**
   - AWS Savings Plans: https://aws.amazon.com/savingsplans/ (up to 72% savings)
   - GCP Committed Use Discounts: https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview (up to 70% savings)
   - Azure Reserved Instances: https://learn.microsoft.com/azure/cost-management-billing/reservations/ (up to 72% savings)

7. **Egress and data transfer cost optimization**
   - Map cross-cloud data flows (AWS → GCP, Azure → AWS, etc.)
   - Calculate egress costs by route:
     - Same-region cross-cloud: typically highest ($0.08-0.12/GB)
     - Cross-region same-cloud: medium ($0.01-0.02/GB)
     - Cloud → internet → cloud (via CDN): varies
   - Recommend egress reduction strategies:
     - **Colocation:** Place communicating services in same cloud
     - **Caching:** Use CloudFront/Cloud CDN/Azure CDN to reduce origin fetches
     - **Compression:** Enable gzip/brotli for API responses
     - **Direct peering:** Use AWS Direct Connect + GCP Interconnect partner connections (not public internet)

   **Egress cost examples (accessed 2025-10-26T14:30:00-04:00):**
   - AWS to internet: $0.09/GB first 10TB, $0.085/GB next 40TB
   - GCP to internet: $0.12/GB first 1TB, $0.11/GB next 9TB
   - Azure to internet: $0.087/GB first 5GB

8. **Cross-cloud tagging compliance and cost allocation**
   - Audit tagging across all clouds using unified tag schema (environment, team, cost-center, project)
   - Calculate **tag compliance rate** per cloud (% resources with required tags)
   - Identify **untagged cost allocation gaps** (spend that cannot be attributed to teams/projects)
   - Recommend standardized tagging policy across AWS/GCP/Azure (harmonize tag keys)

9. **Multi-cloud FinOps maturity assessment**
   - Evaluate FinOps maturity across dimensions:
     - **Visibility:** Single dashboard for all clouds vs siloed per-cloud tools
     - **Optimization:** Automated vs manual optimization across clouds
     - **Governance:** Unified policies vs per-cloud inconsistency
     - **Culture:** Cross-functional FinOps team vs isolated cloud admins
   - Assign maturity score: Crawl (0-3), Walk (4-6), Run (7-10)
   - Recommend next steps to improve maturity (e.g., "Implement unified tagging → +2 maturity points")

10. **Generate comprehensive report**
    - **Executive summary:** Total multi-cloud spend, waste identified, savings potential
    - **Cost breakdown by cloud:** AWS $X, GCP $Y, Azure $Z with trends
    - **Cross-cloud opportunities:** Workload placement (top 10), commitment rebalancing, egress optimization
    - **Action plan:** Prioritized by ROI (savings/effort) with owner assignments

**Authority sources (accessed 2025-10-26T14:30:00-04:00):**

- Multi-Cloud FinOps Best Practices: https://www.prosperops.com/blog/multi-cloud-cost-management-guide/
- FinOps Framework Principles: https://www.finops.org/framework/principles/
- Cloud Cost Optimization Statistics: Organizations waste 32% of cloud spend; multi-cloud tools achieve 35-68% cost reductions (CloudZero 2025)

**Output:** JSON report with sections: unified_cost_summary, cross_cloud_waste (T1), workload_placement_recommendations, commitment_balance_plan, egress_optimization, tagging_compliance, finops_maturity_score, prioritized_action_plan.

**Token budget checkpoint:** ~5.5k tokens (includes T1 + extended multi-cloud analysis + detailed outputs).

### T3: Enterprise Multi-Cloud Optimization (≤12k tokens)

**Goal:** Deep financial modeling, predictive forecasting, and custom multi-cloud optimization strategies for >$1M annual spend.

**Extends T2 with:**

11. **Predictive cost forecasting**
    - Machine learning models trained on historical spend patterns (6+ months data)
    - Forecast next 12 months spend by cloud, service, and team
    - Identify seasonal patterns (e.g., Q4 spike, weekend drop-off)
    - Alert on forecast anomalies (>15% deviation from expected)

12. **Custom commitment optimization algorithms**
    - Optimize commitment portfolio across clouds using linear programming
    - Constraints: budget limits, risk tolerance, workload volatility
    - Objective function: maximize total discount percentage across all clouds
    - Account for commitment term trade-offs (1-year flexibility vs 3-year deeper discounts)

13. **Multi-cloud vendor negotiation intelligence**
    - Aggregate total spend across clouds to strengthen negotiation position
    - Benchmark against similar-sized organizations (anonymized peer data)
    - Identify Private Pricing Agreement (PPA) opportunities with AWS/GCP/Azure
    - Calculate Enterprise Discount Program (EDP) eligibility and potential savings

14. **Sustainability and carbon cost optimization**
    - Map cloud regions to carbon intensity (gCO2/kWh)
    - Calculate carbon footprint by cloud and workload
    - Recommend low-carbon region placement (GCP Iowa vs AWS Virginia)
    - Integrate carbon costs into TCO (emerging regulatory requirement)

15. **Multi-account/multi-org consolidation**
    - AWS: Consolidate billing across AWS Organizations (50+ accounts)
    - GCP: Aggregate billing across multiple billing accounts
    - Azure: Unified cost view across subscriptions and management groups
    - Enable volume discounts and cross-account commitment sharing

**Authority sources (accessed 2025-10-26T14:30:00-04:00):**

- FinOps Market Growth: $5.5B in 2025, 34.8% CAGR (Holori 2025)
- Cloud Computing Market: $723.4B in 2025, 21.5% YoY growth
- AWS Enterprise Discount Programs: https://aws.amazon.com/pricing/
- GCP Committed Use Discount strategies: https://cloud.google.com/docs/cuds-recommendations

**Output:** Full enterprise-grade multi-cloud financial optimization plan including forecasts, custom commitment strategies, vendor negotiation playbook, sustainability metrics, and multi-account consolidation roadmap.

**Token budget checkpoint:** ~11k tokens (includes T1 + T2 + enterprise-grade analysis).

## Decision Rules

**When to abort:**

- Billing API access fails for any cloud → insufficient permissions; emit setup instructions per cloud
- Cost data <30 days → insufficient for trend analysis; wait for more data
- Migration restrictions block all workload placement → report "no cross-cloud opportunities"

**Ambiguity thresholds:**

- **Workload placement confidence:** Only recommend migration if:
  - Cost differential >20% AND annual savings >$10k (avoid noise)
  - No hard compliance/latency constraints
  - ROI >2x (conservative threshold; adjust to 3x for risk-averse orgs)
- **Commitment rebalancing:** Recommend only if:
  - Current utilization <80% (under-utilized) OR coverage <60% (under-committed)
  - Rebalance would improve blended discount rate by ≥5 percentage points
- **Egress optimization:** Flag only if egress costs >10% of total spend OR >$5k/month absolute

**Prioritization logic:**

1. **ROI-based ranking:** `(annual_savings / implementation_effort_cost)` descending
   - Effort scale: Low (delete unused) < Medium (commitment rebalance) < High (workload migration)
2. **Quick wins first:** Zero-downtime, zero-risk changes (delete unused cross-cloud connections) rank highest
3. **Strategic alignment:** If business strategy favors specific cloud (e.g., AWS for ML), deprioritize migration away from it

**FinOps principle application (accessed 2025-10-26T14:30:00-04:00):**

Per FinOps Foundation principles (https://www.finops.org/framework/principles/):

- **"Teams collaborate":** Multi-cloud optimization requires cross-team coordination (cloud admins, finance, engineering)
- **"Decisions are data-driven":** All recommendations backed by normalized cost data across clouds
- **"Take advantage of variable cost model":** Leverage spot instances, preemptible VMs, and commitment flexibility across clouds

## Output Contract

**Schema (JSON):**

```json
{
  "unified_cost_report": {
    "period": "2025-09-26 to 2025-10-26",
    "total_spend": 245000.00,
    "breakdown_by_cloud": {
      "aws": {"spend": 125000.00, "percentage": 51.0, "trend": "+5%"},
      "gcp": {"spend": 80000.00, "percentage": 32.7, "trend": "-2%"},
      "azure": {"spend": 40000.00, "percentage": 16.3, "trend": "+8%"}
    },
    "waste_identified": 68000.00,
    "savings_potential": {
      "monthly": 52000.00,
      "annual": 624000.00,
      "percentage": 21.2
    }
  },
  "workload_placement_recommendations": [
    {
      "workload_id": "analytics-cluster-01",
      "current_cloud": "aws",
      "current_cost_monthly": 12000.00,
      "recommended_cloud": "gcp",
      "recommended_cost_monthly": 6800.00,
      "monthly_savings": 5200.00,
      "annual_savings": 62400.00,
      "migration_cost": 55000.00,
      "roi": 1.13,
      "rationale": "BigQuery vs Redshift cost advantage for analytics workload"
    }
  ],
  "commitment_balance_plan": {
    "current_coverage_rate": 58.0,
    "target_coverage_rate": 75.0,
    "current_blended_discount": 28.0,
    "target_blended_discount": 42.0,
    "recommendations": [
      {
        "cloud": "aws",
        "action": "reduce",
        "current_commitment_monthly": 60000.00,
        "recommended_commitment_monthly": 48000.00,
        "rationale": "RI utilization at 68%, under-utilized"
      },
      {
        "cloud": "gcp",
        "action": "increase",
        "current_commitment_monthly": 15000.00,
        "recommended_commitment_monthly": 32000.00,
        "rationale": "On-demand spend at 72%, opportunity for 70% CUD savings"
      }
    ]
  },
  "cross_cloud_waste_inventory": [
    {
      "waste_type": "unused_cross_cloud_vpn",
      "resources": [
        {"provider": "aws", "resource_id": "vpn-0a1b2c3d", "idle_days": 60},
        {"provider": "azure", "resource_id": "vpn-xyz789", "idle_days": 60}
      ],
      "monthly_cost": 1800.00
    },
    {
      "waste_type": "duplicate_backup_storage",
      "resources": [
        {"provider": "aws", "resource_id": "s3://backups-prod", "size_tb": 50},
        {"provider": "gcp", "resource_id": "gs://backups-prod", "size_tb": 50}
      ],
      "monthly_cost": 2300.00
    }
  ],
  "action_plan": [
    {
      "priority": 1,
      "action": "Delete unused cross-cloud VPN connections",
      "impact": "medium",
      "effort": "low",
      "monthly_savings": 1800.00,
      "owner": "cloud-networking-team"
    },
    {
      "priority": 2,
      "action": "Rebalance commitments (reduce AWS RI, increase GCP CUD)",
      "impact": "high",
      "effort": "medium",
      "monthly_savings": 8400.00,
      "owner": "finops-team"
    }
  ]
}
```

**Required fields:** unified_cost_report (with breakdown_by_cloud, savings_potential), action_plan (prioritized).

**Optional fields:** workload_placement_recommendations, commitment_balance_plan (only if applicable based on business_constraints).

## Examples

```yaml
# Multi-cloud: AWS $125k/mo, GCP $80k/mo, Azure $40k/mo
input: {scope: all, time_range: 90d, model: chargeback}

output:
  total_spend: $245k, waste: $68k (28%), savings: $52k/mo
  workload_placement:
    - analytics: AWS Redshift $12k → GCP BigQuery $6.8k (save $5.2k/mo)
  cross_cloud_waste:
    - unused VPN (AWS+Azure): $1.8k/mo
    - duplicate backups (AWS+GCP): $2.3k/mo
  commitment_rebalance:
    AWS RI: $60k → $48k/mo (reduce)
    GCP CUD: $15k → $32k/mo (increase)
  action_plan:
    1. Delete unused VPN (LOW effort) → $1.8k/mo
    2. Consolidate backups (LOW effort) → $2.3k/mo
    3. Rebalance commitments (MED effort) → $8.4k/mo
    4. Migrate analytics (HIGH effort, ROI 1.13x) → $5.2k/mo
```

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - quick multi-cloud health check with top 3 cross-cloud opportunities
- **T2**: ≤6,000 tokens - comprehensive multi-cloud optimization with workload placement, commitment rebalancing, egress optimization, and unified FinOps analytics
- **T3**: ≤12,000 tokens - enterprise-grade optimization with ML forecasting, custom commitment algorithms, vendor negotiation intelligence, sustainability metrics

**Accuracy requirements:**

- Cost normalization must account for currency (USD/EUR/GBP) and time period differences
- Cross-cloud price comparisons validated against official pricing APIs (accessed on NOW_ET)
- Workload placement ROI calculations include migration costs (egress, downtime, testing)

**Safety constraints:**

- **No automatic workload migration:** All cross-cloud moves require manual approval and testing
- **Compliance checks:** Flag workloads with data residency/sovereignty requirements before recommending migration
- **Commitment purchase limits:** Never recommend commitments exceeding 85% coverage (maintain flexibility)

**Auditability:**

- Cite pricing source for all cost calculations (AWS Pricing API, GCP Cloud Billing, Azure Rate Card)
- Document assumptions in workload placement (instance type equivalence, network latency tolerance)
- Record baseline metrics for each cloud at analysis time

**Determinism:**

- Same inputs + same cost data → same recommendations
- Configurable thresholds (ROI minimum, egress cost %, commitment coverage targets)

## Resources

**Official cloud provider documentation:**

- AWS Cost Management: https://aws.amazon.com/aws-cost-management/
- AWS Savings Plans: https://aws.amazon.com/savingsplans/
- GCP Cloud Billing: https://cloud.google.com/billing/docs
- GCP Committed Use Discounts: https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview
- Azure Cost Management: https://learn.microsoft.com/azure/cost-management-billing/
- Azure Reserved Instances: https://learn.microsoft.com/azure/cost-management-billing/reservations/

**FinOps Foundation resources:**

- FinOps Framework: https://www.finops.org/framework/
- FinOps Principles: https://www.finops.org/framework/principles/
- Multi-Cloud FinOps Guidance: https://www.finops.org/framework/capabilities/

**Multi-cloud cost optimization guides:**

- Multi-Cloud Cost Management Best Practices 2025: https://www.prosperops.com/blog/multi-cloud-cost-management-guide/ (accessed 2025-10-26T14:30:00-04:00)
- FinOps Best Practices 2025: https://www.cloudzero.com/blog/finops-best-practices/ (accessed 2025-10-26T14:30:00-04:00)
- Top 50 FinOps Tools 2025: https://holori.com/20-best-finops-and-cloud-cost-management-tools-in-2025/ (accessed 2025-10-26T14:30:00-04:00)
- Cloud Pricing Comparison 2025: https://cast.ai/blog/cloud-pricing-comparison/ (accessed 2025-10-26T14:30:00-04:00)

**Related skills:**

- `finops-cost-analyzer`: For single-cloud cost optimization (invoke before multi-cloud aggregation)
- `cloud-multicloud-advisor`: For strategic multi-cloud architecture design (invoke before deployment)
- `cloud-provider-advisor`: For initial cloud provider selection (invoke during planning phase)
