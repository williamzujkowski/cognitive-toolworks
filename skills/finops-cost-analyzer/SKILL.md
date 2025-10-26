---
name: Cloud Cost Optimization Analyzer
slug: finops-cost-analyzer
description: Analyze and optimize cloud costs across AWS, Azure, GCP with rightsizing, reserved instances, waste detection, and FinOps best practices.
capabilities:
  - Multi-cloud cost analysis (AWS, Azure, GCP)
  - Resource rightsizing recommendations
  - Reserved instance and savings plan optimization
  - Waste and idle resource detection
  - FinOps framework implementation
  - Cost anomaly detection and alerting
inputs:
  - cloud_provider: string (aws|azure|gcp|multi)
  - cost_data_source: string (billing API, cost explorer, CSV export)
  - optimization_targets: array (compute|storage|network|database)
  - budget_constraints: object {monthly_budget, alert_threshold}
  - time_range: string (7d|30d|90d|custom)
outputs:
  - cost_analysis_report: object {current_spend, waste_identified, savings_potential}
  - rightsizing_recommendations: array of {resource_id, current_size, recommended_size, savings}
  - commitment_recommendations: array of {service, plan_type, term, savings}
  - waste_inventory: array of {resource_id, type, idle_days, monthly_cost}
  - action_plan: prioritized list of optimization actions
keywords:
  - cloud cost optimization
  - finops
  - rightsizing
  - reserved instances
  - savings plans
  - cost anomaly detection
  - waste detection
  - TCO optimization
  - budget management
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  - Read-only access to billing APIs
  - No modification of live resources without approval
  - Secure handling of cost data (may contain sensitive business info)
  - Audit logging of all recommendations
links:
  - https://aws.amazon.com/aws-cost-management/
  - https://azure.microsoft.com/solutions/cost-optimization/
  - https://cloud.google.com/cost-management
  - https://www.finops.org/framework/
---

## Purpose & When-To-Use

**Primary trigger conditions:**

- Monthly cloud bill shows unexpected increase (>10% variance)
- Budget alert fired indicating overspend
- Regular cost optimization review cycle (quarterly FinOps practice)
- Pre-budget planning phase requires accurate TCO estimates
- Executive request for cloud cost reduction initiatives
- Migration to cloud requires cost modeling
- Reserved instance or savings plan renewal decision needed

**When NOT to use this skill:**

- Real-time cost tracking (use native dashboards instead)
- One-time spot instance pricing lookup (use pricing calculators)
- Architecture design phase (use cloud-aws-architect first)

**Value proposition:** Identifies 30-40% of typical cloud waste through systematic analysis of rightsizing, commitment discounts, and idle resources using FinOps principles.

## Pre-Checks

**Required inputs validation:**

```python
NOW_ET = "2025-10-25T22:42:30-04:00"

assert cloud_provider in ["aws", "azure", "gcp", "multi"], "Invalid cloud provider"
assert cost_data_source is not None, "Cost data source required"
assert time_range in ["7d", "30d", "90d"] or matches_custom_format(time_range)
assert len(optimization_targets) > 0, "At least one optimization target required"

# Data freshness check
if cost_data_age > 24h:
    warn("Cost data is stale; recommendations may be outdated")

# Minimum data volume check
if time_range == "7d" and total_resources < 10:
    suggest("Use 30d+ range for better trend analysis")
```

**Authority checks:**

- AWS: Cost Explorer API enabled, `ce:GetCostAndUsage` permission
- Azure: Cost Management API access, Reader role on subscriptions
- GCP: Cloud Billing API enabled, `billing.accounts.getSpendingInformation` permission

**Source citations (accessed 2025-10-25T22:42:30-04:00):**

- AWS Cost Management: https://aws.amazon.com/aws-cost-management/
- Azure Cost Optimization: https://azure.microsoft.com/solutions/cost-optimization/
- GCP Cost Management: https://cloud.google.com/cost-management
- FinOps Framework: https://www.finops.org/framework/
- FinOps Principles: https://www.finops.org/framework/principles/

## Procedure

### Tier 1 (≤2k tokens): Quick Cost Health Check

**Goal:** Identify top 3 cost optimization opportunities in <5 minutes.

**Steps:**

1. **Fetch cost summary** for specified time_range
   - Group by service/resource type
   - Calculate total spend and trend (% change from previous period)

2. **Quick waste scan** (top offenders only)
   - Stopped instances still attached to storage
   - Unattached EBS volumes / Azure managed disks / GCP persistent disks
   - Unused Elastic IPs / Public IPs / Static external IPs
   - Load balancers with zero traffic (last 7 days)

3. **Commitment coverage check**
   - Calculate % of compute spend covered by reserved instances / savings plans / committed use discounts
   - If <60% coverage → flag as optimization opportunity

4. **Output quick wins** (3 highest impact items)
   - Example: "Delete 15 unattached EBS volumes → save $450/month"
   - Example: "Purchase EC2 Savings Plan (3-year) → save $2,400/month"
   - Example: "Rightsize 8 over-provisioned RDS instances → save $1,200/month"

**Token budget checkpoint:** ~1.5k tokens for API calls, analysis, and output formatting.

### Tier 2 (≤6k tokens): Comprehensive Cost Analysis

**Goal:** Generate detailed, actionable cost optimization plan with quantified savings.

**Extends T1 with:**

5. **Rightsizing analysis**
   - Fetch CloudWatch / Azure Monitor / GCP Monitoring metrics (CPU, memory, network utilization)
   - Identify resources with <20% utilization over 90th percentile
   - Recommend downsizing (example: m5.2xlarge → m5.xlarge saves $150/month)
   - Calculate savings per resource: `(current_price - recommended_price) * hours_per_month`

6. **Reserved instance / Savings plan optimization**
   - Analyze historical usage patterns (30d minimum, 90d preferred)
   - Identify stable workloads eligible for commitments
   - Calculate break-even point: `upfront_cost / monthly_savings`
   - Recommend commitment term (1-year vs 3-year) based on usage stability
   - **AWS:** Compare Compute Savings Plans vs EC2 RIs vs convertible RIs
   - **Azure:** Compare Reserved VM Instances vs Azure Hybrid Benefit
   - **GCP:** Compare Committed Use Discounts (CUD) vs Sustained Use Discounts (SUD)

7. **Storage optimization**
   - Identify candidates for lifecycle policies (hot → cool → archive)
   - **AWS S3:** Recommend Intelligent-Tiering or S3 Glacier transitions
   - **Azure Blob:** Recommend tiering to Cool or Archive
   - **GCP Cloud Storage:** Recommend Nearline or Coldline classes
   - Calculate savings: `(current_storage_cost - optimized_cost) * TB_stored`

8. **Network cost optimization**
   - Identify cross-region / cross-AZ traffic (expensive)
   - Recommend VPC endpoints / Private Link to avoid NAT gateway costs
   - Flag public internet egress (most expensive path)

9. **Cost anomaly detection**
   - Calculate baseline spend (average + 2 std deviations)
   - Flag spikes >20% above baseline
   - Attribute anomaly to specific service/resource

10. **FinOps maturity assessment** (basic)
    - Tag compliance: % resources with required cost allocation tags
    - Budget variance: actual vs budgeted spend
    - Commitment utilization: % of purchased RI/SP actually used
    - Waste ratio: idle_cost / total_cost

**Authority sources (accessed 2025-10-25T22:42:30-04:00):**

- AWS Reserved Instances: https://aws.amazon.com/ec2/pricing/reserved-instances/
- AWS Savings Plans: https://aws.amazon.com/savingsplans/ (up to 72% savings)
- Azure Reserved Instances: https://learn.microsoft.com/azure/cost-management-billing/reservations/
- Azure Hybrid Benefit: https://azure.microsoft.com/pricing/hybrid-benefit/ (up to 36% for Windows Server)
- GCP Committed Use Discounts: https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview
- FinOps "Crawl, Walk, Run" maturity: https://www.finops.org/framework/

**Output:** JSON report with sections: cost_summary, quick_wins (T1), rightsizing_recommendations, commitment_recommendations, storage_optimization, network_optimization, anomalies, finops_maturity_score.

**Token budget checkpoint:** ~5k tokens (includes T1 + extended analysis + detailed output).

### Tier 3 (not implemented for T2 skill)

Reserved for future enhancements: predictive cost forecasting, ML-based anomaly detection, multi-account/org-wide consolidation, custom FinOps policies.

## Decision Rules

**When to abort:**

- Cost data source returns 403/401 → insufficient permissions; emit setup instructions
- Cost data empty or <7 days → insufficient data for analysis
- All optimization targets already at maximum efficiency (rare) → report "no action needed"

**Ambiguity thresholds:**

- **Rightsizing confidence:** Only recommend if utilization <20% for 90% of time period (avoids false positives from bursty workloads)
- **Commitment recommendations:** Require 90d minimum history AND <10% variance in daily usage to recommend 3-year term
- **Anomaly detection:** Only flag if >20% deviation AND >$100 absolute difference (avoid noise)

**Prioritization logic:**

1. **Highest ROI first:** `savings_per_month / implementation_effort`
   - Effort scale: Low (delete unused) < Medium (rightsize) < High (migrate architecture)
2. **Quick wins:** Zero-downtime changes (stop unused, delete orphaned) rank highest
3. **Risk-adjusted:** Downsizing production workloads requires manual approval; rank lower

**FinOps principle application (accessed 2025-10-25T22:42:30-04:00):**

Per FinOps Foundation principles (https://www.finops.org/framework/principles/):

- **"Everyone takes ownership":** Tag all recommendations with owning team/project via cost allocation tags
- **"Centralized optimization":** Reserved instance / savings plan purchases centralized; this skill generates recommendations for central FinOps team
- **"Variable cost model as opportunity":** Emphasize autoscaling and spot instances as cost-saving strategies

## Output Contract

**Schema (JSON):**

```json
{
  "cost_analysis_report": {
    "period": "2025-09-25 to 2025-10-25",
    "cloud_provider": "aws",
    "total_spend": 47500.32,
    "waste_identified": 14250.10,
    "savings_potential": {
      "monthly": 12800.00,
      "annual": 153600.00,
      "percentage": 26.9
    }
  },
  "quick_wins": [
    {
      "category": "unused_resources",
      "description": "Delete 12 unattached EBS volumes",
      "monthly_savings": 360.00,
      "implementation_effort": "low",
      "risk_level": "none"
    }
  ],
  "rightsizing_recommendations": [
    {
      "resource_id": "i-0a1b2c3d4e5f6g7h8",
      "resource_type": "ec2_instance",
      "current_type": "m5.2xlarge",
      "recommended_type": "m5.xlarge",
      "utilization_avg": 18.5,
      "monthly_savings": 150.00,
      "confidence": "high"
    }
  ],
  "commitment_recommendations": [
    {
      "service": "ec2_compute",
      "plan_type": "compute_savings_plan",
      "term": "3_year",
      "upfront": "partial",
      "monthly_commitment": 5000.00,
      "monthly_savings": 1200.00,
      "break_even_months": 4.2
    }
  ],
  "waste_inventory": [
    {
      "resource_id": "vol-0123456789abcdef",
      "type": "ebs_volume_unattached",
      "idle_days": 45,
      "monthly_cost": 30.00
    }
  ],
  "action_plan": [
    {
      "priority": 1,
      "action": "Delete unused resources",
      "impact": "high",
      "effort": "low",
      "items_count": 27,
      "monthly_savings": 810.00
    }
  ]
}
```

**Required fields:** cost_analysis_report (with total_spend, savings_potential), action_plan (prioritized).

**Optional fields:** rightsizing_recommendations, commitment_recommendations (only if applicable).

## Examples

```yaml
# Example: AWS cost optimization for over-provisioned workload
input:
  cloud_provider: aws
  cost_data_source: cost_explorer_api
  optimization_targets: [compute, storage, network]
  budget_constraints:
    monthly_budget: 50000
    alert_threshold: 0.90
  time_range: 90d

output:
  cost_analysis_report:
    total_spend: 47500.32
    waste_identified: 14250.10
    savings_potential:
      monthly: 12800
      annual: 153600
      percentage: 26.9
  quick_wins:
    - category: unused_resources
      description: Delete 12 unattached EBS volumes
      monthly_savings: 360
  rightsizing_recommendations:
    - resource_id: i-0a1b2c3d4e5f
      current_type: m5.2xlarge
      recommended_type: m5.xlarge
      utilization_avg: 18.5
      monthly_savings: 150
```

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - quick health check with top 3 cost optimization opportunities
- **T2**: ≤6,000 tokens - comprehensive analysis with rightsizing, commitments, storage optimization, anomalies, and FinOps maturity
- **T3**: (not implemented) - reserved for predictive cost forecasting, ML-based anomaly detection, multi-account consolidation

**Accuracy requirements:**

- Cost calculations must match cloud provider billing (±2% tolerance)
- Rightsizing recommendations validated against 90th percentile utilization metrics
- Commitment savings verified against current pricing (as of NOW_ET)

**Safety constraints:**

- **No automatic resource deletion:** All recommendations require human approval
- **Production safeguards:** Flag production resources; require elevated approval for changes
- **Audit trail:** Log all API calls and recommendations with timestamps

**Auditability:**

- Cite source for all pricing data (AWS Pricing API, Azure Rate Card, GCP Pricing Calculator)
- Include confidence scores for probabilistic recommendations (rightsizing, anomalies)
- Record baseline metrics used for comparisons

**Determinism:**

- Same inputs + same cost data → same recommendations
- Cost anomaly thresholds configurable (default: 20% deviation, $100 minimum)

## Resources

**Official cloud provider documentation:**

- AWS Cost Optimization Hub: https://docs.aws.amazon.com/cost-optimization-hub/
- AWS Trusted Advisor: https://aws.amazon.com/premiumsupport/technology/trusted-advisor/
- AWS Cost Explorer: https://aws.amazon.com/aws-cost-management/aws-cost-explorer/
- Azure Cost Management: https://learn.microsoft.com/azure/cost-management-billing/
- Azure Advisor: https://learn.microsoft.com/azure/advisor/advisor-cost-recommendations
- GCP Recommender: https://cloud.google.com/recommender/docs
- GCP Cloud Billing: https://cloud.google.com/billing/docs

**FinOps Foundation resources:**

- FinOps Framework: https://www.finops.org/framework/
- FinOps Principles (6 core tenets): https://www.finops.org/framework/principles/
- FinOps Maturity Model: https://www.finops.org/framework/maturity-model/
- FinOps Personas: https://www.finops.org/framework/personas/

**Third-party cost optimization guides:**

- Cloud cost optimization best practices 2025: https://www.cloudzero.com/blog/aws-cost-management-best-practices/ (accessed 2025-10-25T22:42:30-04:00)
- Azure cost optimization tactics: https://cast.ai/blog/azure-cost-optimization/ (accessed 2025-10-25T22:42:30-04:00)
- GCP cost optimization tools: https://www.cloudzero.com/blog/gcp-cost-optimization-tools/ (accessed 2025-10-25T22:42:30-04:00)

**Related skills:**

- `cloud-aws-architect`: For architecture-level cost optimization during design phase
- `devops-pipeline-architect`: For CI/CD cost optimization (ephemeral environments)
- `cloud-native-deployment-orchestrator`: For Kubernetes cost optimization (cluster rightsizing)
