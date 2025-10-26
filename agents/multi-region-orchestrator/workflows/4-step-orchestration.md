# Multi-Region Deployment Orchestration Workflow

This document describes the 4-step orchestration workflow executed by the Multi-Region Deployment Orchestrator agent.

## Overview

**Total Token Budget**: ≤12,000 tokens across all steps
**Execution Model**: Sequential (each step depends on previous step outputs)
**Failure Handling**: Fail fast - abort on any step failure, surface errors clearly

## Workflow Steps

### Step 1: Topology Design (≤2k tokens)

**Inputs:**
- Target regions (user preference or compliance requirements)
- Latency SLA (e.g., <100ms for 95% of global users)
- Compliance requirements (GDPR, data residency)
- Budget constraints

**Process:**
1. Analyze user population density and map to cloud provider regions
2. Filter regions by compliance requirements (e.g., EU-only for GDPR)
3. Validate service availability in selected regions
4. Design traffic routing strategy (latency-based, failover, weighted)
5. Create network topology (VPC peering, transit gateway, global LB)

**Skill Delegation:**
- `multicloud-strategy-advisor` - if multi-cloud vendor comparison needed

**Outputs:**
- Regional topology diagram (PlantUML/Mermaid)
- Region list with justification
- Traffic routing configuration
- Network architecture design

**Decision Points:**
- Latency SLA <50ms globally → require 5+ regions across continents
- Compliance requires EU data residency → mandate EU regions for EU users
- Budget <2x single-region → recommend active-passive over active-active

---

### Step 2: Regional Deployment (≤4k tokens)

**Inputs:**
- Topology design from Step 1
- Application architecture (containers, VMs, serverless, databases)
- Regional customization requirements

**Process:**
1. Generate IaC templates for each region (Terraform, CloudFormation, ARM)
2. Parameterize region-specific variables (AZs, CIDR blocks, instance types)
3. Deploy compute resources (EC2/VMs, EKS/AKS/GKE clusters)
4. Configure regional networking (VPC/VNet, security groups, peering)
5. Implement progressive rollout (canary region first)

**Skill Delegation:**
- `iac-template-generator` - generate IaC for each region
- `cloud-platform-integrator` - configure Kubernetes clusters per region
- `networksec-architecture-validator` - validate security posture
- `deployment-strategy-designer` - design regional rollout plan

**Outputs:**
- IaC templates for all regions
- Deployment scripts with regional sequencing
- Network topology with cross-region connectivity
- Security configurations validated per region

**Decision Points:**
- Stateless application → deploy all regions in parallel after canary
- Stateful application → sequential deployment with data migration coordination
- Critical production → require manual approval between regions

---

### Step 3: Data Replication (≤3k tokens)

**Inputs:**
- Data strategy (active-active, active-passive, read-replicas, sharded)
- Database type (relational, NoSQL, caching, object storage)
- Consistency requirements (strong, eventual, causal)
- RPO and RTO requirements

**Process:**
1. Select replication strategy based on consistency requirements
2. Configure database replication (DynamoDB Global Tables, RDS cross-region, etc.)
3. Implement conflict resolution (LWW, CRDTs, application-level merge)
4. Set up monitoring for replication lag and conflicts
5. Validate data consistency across regions

**Skill Delegation:**
- `database-optimization-analyzer` - optimize replication performance

**Outputs:**
- Replication configuration for each data store
- Conflict resolution strategy documentation
- Replication lag monitoring setup
- Data consistency validation scripts

**Decision Points:**
- RPO <5 minutes → require synchronous replication (performance impact)
- Application handles conflicts → use eventual consistency with LWW
- No conflict resolution strategy → mandate active-passive or sharded

---

### Step 4: Validation (≤1.5k tokens)

**Inputs:**
- Deployed regional infrastructure from Step 2
- Replication configuration from Step 3
- Latency SLA and failover requirements from Step 1

**Process:**
1. Execute regional health checks (verify each region serves traffic)
2. Test failover scenarios (simulate primary region failure)
3. Measure end-to-end latency from global test locations
4. Validate data replication (write to primary, read from secondary)
5. Perform load testing across regions

**Outputs:**
- Validation test results (pass/fail per region)
- Latency measurements by region
- Failover test report (RTO/RPO measurements)
- Data consistency validation results

**Decision Points:**
- Any region fails health checks → block production promotion
- Latency SLA not met → revisit region selection or add edge locations
- RTO exceeds requirements → automate failover or add regions

---

## Integration Between Steps

```
Step 1 (Topology Design)
  ↓
  Outputs: region list, network topology, traffic routing
  ↓
Step 2 (Regional Deployment)
  ↓
  Outputs: IaC templates, deployed infrastructure, regional endpoints
  ↓
Step 3 (Data Replication)
  ↓
  Outputs: replication config, consistency model, conflict resolution
  ↓
Step 4 (Validation)
  ↓
  Outputs: test results, latency measurements, failover validation
```

## Error Handling

**Step Failures:**
- **Step 1 fails**: Abort - cannot proceed without topology design
- **Step 2 fails**: Abort - partial deployment unsafe; rollback deployed regions
- **Step 3 fails**: Abort - cannot serve traffic without data replication
- **Step 4 fails**: Block production promotion - fix issues before traffic routing

**Rollback Procedures:**
- Regional rollback: destroy IaC resources in failed region only
- Preserve successful regions for debugging
- Document failure reason and resolution steps

## Example Execution Timeline

For a 3-region AWS deployment (us-east-1, eu-west-1, ap-southeast-1):

```
T+0:00   Step 1: Topology Design starts
T+0:02   Step 1: Complete (2k tokens)
T+0:02   Step 2: Regional Deployment starts
         - Deploy canary region (ap-southeast-1)
T+0:15   - Validate canary health
         - Deploy remaining regions (us-east-1, eu-west-1)
T+0:30   Step 2: Complete (4k tokens)
T+0:30   Step 3: Data Replication starts
         - Configure RDS cross-region read replicas
         - Set up S3 CRR
         - Enable replication lag monitoring
T+0:45   Step 3: Complete (3k tokens)
T+0:45   Step 4: Validation starts
         - Regional health checks
         - Failover test (simulate us-east-1 failure)
         - Latency validation from 10 global locations
         - Data consistency validation
T+1:00   Step 4: Complete (1.5k tokens)
T+1:00   Orchestration complete - ready for production traffic
```

**Total Tokens**: 10.5k (within ≤12k budget)
**Total Time**: ~60 minutes (deployment time varies by infrastructure size)

## Validation Checklist

- [ ] All regions pass independent health checks
- [ ] Failover test successful (RTO < requirements)
- [ ] Latency SLA met from all test locations
- [ ] Data replication working (write to primary, read from secondary)
- [ ] Replication lag within acceptable thresholds
- [ ] Monitoring dashboards operational in all regions
- [ ] Alerting configured for regional failures
- [ ] Runbook documented for manual failover procedures
- [ ] Cost estimation validated against budget constraints
- [ ] Security validated (encryption in transit and at rest)
