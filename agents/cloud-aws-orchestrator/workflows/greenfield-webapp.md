# Workflow: Greenfield Serverless Web Application

**Scenario:** Launch new SaaS MVP with minimal operational overhead and cost.

**Typical inputs:**
- Business objective: Launch beta product
- Workload: Web application (API + frontend)
- Constraints: Budget <$1000/month, 6-8 week timeline, no compliance
- Complexity: **simple**
- Scope: **full**

---

## Phase 1: Discovery

**Questions to validate:**
1. Expected user base: <1000 (simple) | 1000-10,000 (moderate) | >10,000 (complex)
2. Data sensitivity: Public | Internal | Regulated
3. Availability requirement: Best-effort | 99.9% | 99.99%
4. Integration needs: None | 3rd-party APIs | Legacy systems

**Output:** Validated requirements document

---

## Phase 2: Design

**Skill invocation:**
```
aws-multi-service-architect (T1 - quick recommendations)
  Inputs:
    - requirements: {performance: <500ms API latency, cost: $1000/month max}
    - workload_type: web-app
    - deployment_tier: T1
    - regions: [us-east-1]

  Expected output:
    - Serverless architecture: API Gateway + Lambda + DynamoDB + S3 + CloudFront
    - Estimated cost: $200-400/month (1000 users, 100K requests/month)
```

**ADR (if needed):**
- Decision: Serverless (Lambda) vs Containers (ECS Fargate)
- Rationale: Cost optimization for variable load, auto-scaling to zero
- Trade-offs: 15-minute Lambda timeout accepted (no long-running tasks)

**Output:** Architecture design with 5-6 AWS services, 1 ADR, cost estimate

---

## Phase 3: Validation

**Simplified validation (simple tier):**
- Cost check: Estimate within budget? ✓
- Security baseline: Encryption at-rest, HTTPS, IAM roles? ✓
- Deployment: Single-phase launch (no migration complexity)

**Skill invocation:** SKIP cost-optimization-analyzer (built-in estimates sufficient)

**Output:** Validated architecture, single-phase deployment plan

---

## Phase 4: Delivery

**Handoff package:**
```
/handoff-package/
  README.md - Quick-start guide
  /architecture/
    serverless-webapp-overview.md - Architecture description
    adr-001-compute-serverless.md - Lambda vs ECS decision
  /iac/
    cloudformation/
      serverless-stack.yaml - Single CloudFormation template (~150 lines)
  /deployment/
    deployment-guide.md - 4-step deployment (deploy stack, upload frontend to S3, configure DNS, validate)
  /operations/
    cost-estimate.md - $200-400/month breakdown
    monitoring-config.yaml - CloudWatch alarms for Lambda errors, API latency
```

**Quality checklist:**
- [x] CloudFormation template validates successfully
- [x] IAM policies follow least-privilege (Lambda execution role)
- [x] S3 bucket has encryption enabled, no public access
- [x] API Gateway uses HTTPS with custom domain
- [x] Cost estimate within budget ($400 vs $1000)
- [x] Deployment guide tested (4 steps, <30 minutes)

---

## Timeline

- **Week 1-2:** Discovery + Design (requirements → architecture)
- **Week 3-4:** Implementation (CloudFormation development, frontend build)
- **Week 5-6:** Testing + Deployment (integration tests, beta launch)

**Total token usage:** ~6k tokens (discovery 2k + design 2k + validation 1k + delivery 1k)

---

## Success Criteria

- Architecture deployed successfully in AWS
- Application accessible via HTTPS custom domain
- Cost tracking enabled (AWS Budgets alert at $500/month)
- Monitoring dashboards live (CloudWatch Lambda metrics, API Gateway latency)
- Handoff package delivered to development team
