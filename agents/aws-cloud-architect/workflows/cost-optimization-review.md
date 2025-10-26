# Workflow: Quarterly Cost Optimization Review

**Scenario:** Existing AWS infrastructure needs cost reduction without impacting availability.

**Typical inputs:**
- Business objective: Reduce cloud spend by 20-30%
- Workload: Existing production architecture (web-app, data-processing, etc.)
- Constraints: No downtime, maintain 99.9% SLA
- Complexity: **moderate**
- Scope: **optimize** (Phases 1-3 only)
- existing_state: Current AWS cost data + resource inventory

---

## Phase 1: Discovery

**Questions to validate:**
1. Current monthly spend: Baseline and trend (increasing/stable/decreasing)
2. Cost breakdown: Compute, storage, database, networking percentages
3. Business constraints: Can we change instance types? Reserved commitments OK?
4. Timeline: When do optimization changes need to complete?

**Required data:**
- AWS Cost Explorer export (90 days minimum)
- Resource inventory (EC2, RDS, S3, etc.)
- Availability requirements per service

**Output:** Cost baseline, optimization targets identified

---

## Phase 2: Design

**Skill invocation:**
```
aws-multi-service-architect (T2 - review existing architecture)
  Inputs:
    - current_architecture: "3-tier web app: 8x t3.large EC2, 2x RDS Multi-AZ, 5TB S3, ALB"
    - requirements: {cost: reduce 25%, availability: maintain 99.9%}
    - deployment_tier: T2

  Expected output:
    - Rightsizing recommendations: t3.large → t3.medium (over-provisioned CPU)
    - Reserved Instance opportunities: 2x RDS instances (1-year RI)
    - S3 lifecycle policies: Move 3TB to Glacier Deep Archive (accessed <1/year)
```

**ADR (if needed):**
- Decision: Immediate optimization vs phased approach
- Rationale: Phased allows A/B testing and risk mitigation
- Phases: 1) S3 lifecycle (low risk), 2) EC2 rightsizing (test in dev first), 3) RDS RI commitment

**Output:** Optimized architecture design, implementation phases

---

## Phase 3: Validation

**Skill invocation:**
```
cost-optimization-analyzer
  Inputs:
    - cloud_provider: aws
    - cost_data_source: Cost Explorer API (90-day data)
    - optimization_targets: [compute, storage, database]
    - time_range: 90d

  Expected output:
    - Waste inventory: 2x EC2 stopped instances ($120/month), 500GB unused EBS volumes ($50/month)
    - Rightsizing: 8x t3.large → 8x t3.medium (CPU <30%, saves $300/month)
    - Commitment recommendations: RDS 1-year RI (saves $400/month), EC2 Savings Plan (saves $250/month)
    - Total savings potential: $1120/month (28% reduction from $4000 baseline)
```

**deployment-strategy-designer:**
```
  Inputs:
    - deployment_type: optimization (no migration)
    - architecture: current + optimized from Phase 2
    - risk_tolerance: medium (phased rollout)

  Expected output:
    - Phase 1 (Week 1): Delete stopped EC2, apply S3 lifecycle policies (saves $170/month, zero risk)
    - Phase 2 (Week 2-3): Test t3.medium in dev, rolling EC2 resize (saves $300/month, low risk)
    - Phase 3 (Week 4): Purchase RDS RI + EC2 Savings Plan (saves $650/month, commitment required)
    - Rollback: Keep original instance snapshots, cancel RI if performance degrades (60-day window)
```

**Output:** Validated cost optimization plan with savings projections and risk mitigation

---

## Phase 4: Delivery (SKIPPED for optimize scope)

**Note:** Scope=optimize stops at Phase 3. Implementation team receives:
- Cost optimization report (current vs optimized architecture)
- Phased implementation plan (3 waves with rollback procedures)
- Updated IaC templates (CloudFormation/CDK with rightsized instances)

---

## Timeline

- **Week 1:** Discovery + Validation (cost analysis)
- **Week 2-3:** Design + Optimization planning
- **Week 4-6:** Phased implementation (per deployment-strategy-designer output)

**Total token usage:** ~11k tokens (discovery 3k + design 4k + validation 4k)

---

## Success Criteria

- Cost savings: ≥20% reduction achieved ($800/month on $4000 baseline)
- Availability: 99.9% SLA maintained (no degradation)
- Monitoring: Cost anomaly alerts configured (AWS Budgets)
- Documentation: Optimization decisions recorded in ADRs
- Next review: Scheduled in 90 days (continuous FinOps practice)

---

## Common Optimization Patterns

**Compute:**
- Rightsizing: CPU <40% for 2+ weeks → downsize
- Reserved Instances: Predictable workloads, 1-year commitment
- Spot Instances: Batch/fault-tolerant workloads, 70-90% savings

**Storage:**
- S3 Intelligent-Tiering: Automatic cost optimization
- Lifecycle policies: Standard → IA (30d) → Glacier (90d) → Deep Archive (365d)
- EBS snapshots: Delete old snapshots, use DLM policies

**Database:**
- RDS Reserved Instances: 30-60% savings for production databases
- Aurora Serverless v2: Auto-scaling for variable workloads
- Read Replicas: Cache frequently-read data (vs vertical scaling)

**Networking:**
- VPC Endpoints: S3/DynamoDB Gateway Endpoints (eliminate NAT Gateway costs)
- CloudFront: Cache API responses (reduce origin traffic)
- Data Transfer: Keep inter-service traffic in same region/AZ
