---
name: "Deployment Strategy Designer"
slug: deployment-strategy-designer
description: "Design deployment strategies (rolling, blue-green, canary) with platform-specific implementations and automated rollback procedures."
capabilities:
  - design_deployment_strategy
  - generate_rollback_procedures
inputs:
  deployment_target:
    type: string
    description: "Target platform: kubernetes, ecs, lambda, vm, on-premise"
    required: true
  application_type:
    type: string
    description: "Application type: stateless, stateful, serverless, batch"
    required: true
  requirements:
    type: object
    description: "Downtime tolerance, risk tolerance, rollback time, traffic control"
    required: true
outputs:
  strategy_document:
    type: markdown
    description: "Detailed deployment strategy with decision rationale"
  implementation_config:
    type: code
    description: "Platform-specific deployment configuration"
  rollback_procedure:
    type: markdown
    description: "Step-by-step rollback instructions with automation scripts"
keywords:
  - deployment-strategy
  - rolling-deployment
  - blue-green
  - canary
  - rollback
  - kubernetes
  - ecs
  - zero-downtime
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: required
links:
  - https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
  - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html
  - https://martinfowler.com/bliki/BlueGreenDeployment.html
  - https://martinfowler.com/bliki/CanaryRelease.html
---

## Purpose & When-To-Use

**Trigger conditions:**

- New application deployment requires strategy definition
- Existing deployment causes unacceptable downtime or risk
- Migration to new deployment platform (VM → container → serverless)
- Compliance requires zero-downtime deployments
- Production incidents reveal inadequate rollback capabilities
- High-risk releases need gradual rollout

**Use this skill when** you need a well-defined deployment strategy with platform-specific implementation and tested rollback procedures.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T01:33:56-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `deployment_target` is one of: `kubernetes`, `ecs`, `lambda`, `vm`, `on-premise`
   - `application_type` is one of: `stateless`, `stateful`, `serverless`, `batch`
   - `requirements.downtime_tolerance` specifies acceptable downtime (e.g., "zero", "< 5 minutes")
   - `requirements.risk_tolerance` indicates risk appetite (low, medium, high)
   - `requirements.rollback_time` specifies maximum rollback duration
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Platform capabilities**: Confirm deployment target supports selected strategy

**Abort conditions:**

- Platform doesn't support zero-downtime deployment when required
- Stateful application requires zero downtime without platform support for live migration
- Conflicting requirements (e.g., "instant rollback" with "stateful database migration")
- Resource constraints prevent parallel environment provisioning (blue-green)

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Select and document deployment strategy for common scenarios with basic implementation.

**Steps:**

1. **Analyze requirements and select strategy** (600 tokens):
   - **Input analysis**:
     - Downtime tolerance → zero = blue-green or rolling; acceptable = recreate
     - Risk tolerance → low = canary; medium = rolling; high = big-bang
     - Application type → stateless = flexible; stateful = rolling with care
   - **Strategy selection**:
     - **Rolling**: Default for stateless applications, gradual replacement
     - **Blue-Green**: Zero downtime, instant rollback, requires 2x resources
     - **Canary**: Risk mitigation, gradual traffic shift, requires monitoring
     - **Recreate**: Simple, acceptable downtime, resource-efficient

2. **Generate strategy document and implementation** (1400 tokens):
   - **Strategy document**:
     - Selected strategy with decision rationale
     - Deployment phases (pre-deployment, deployment, post-deployment, validation)
     - Success criteria and health checks
     - Rollback triggers (error rate threshold, manual intervention)
   - **Platform-specific implementation**:
     - **Kubernetes**: Deployment manifest with strategy configuration
     - **ECS**: Service update configuration with deployment parameters
     - **Lambda**: Alias and version-based traffic shifting
   - **Rollback procedure**:
     - Detection: monitoring alerts, health check failures
     - Decision: automated vs. manual rollback trigger
     - Execution: platform-specific rollback commands
     - Verification: health checks and smoke tests post-rollback

**Decision point**: If requirements include progressive traffic shifting, automated rollback, or multi-region → escalate to T2.

---

### Tier 2 (Extended Analysis, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Advanced deployment strategies with automated progressive rollout and intelligent rollback.

**Steps:**

1. **Design advanced deployment strategy** (2500 tokens):
   - **Canary deployment** (accessed 2025-10-26T01:33:56-04:00):
     - Progressive traffic shifting: 5% → 25% → 50% → 100%
     - Stage duration based on confidence interval (15-60 minutes per stage)
     - Automated promotion criteria:
       - Error rate < 1% compared to baseline
       - Latency p99 < baseline + 10%
       - No critical alerts triggered
     - Automated rollback triggers:
       - Error rate > 5%
       - Latency degradation > 50%
       - Health check failures > 10%
   - **Blue-Green deployment** (accessed 2025-10-26T01:33:56-04:00):
     - Parallel environment provisioning (blue = current, green = new)
     - Traffic switching mechanisms:
       - **Load balancer**: Target group swap (ELB, ALB)
       - **DNS**: Route53 weighted routing
       - **Service mesh**: Istio/Linkerd traffic split
     - Warm-up period for green environment (pre-flight checks, cache warming)
     - Instant rollback via traffic switch (< 30 seconds)
   - **Rolling deployment optimization**:
     - Surge and unavailability parameters (maxSurge: 25%, maxUnavailable: 0)
     - Pod disruption budgets for Kubernetes
     - Health checks and readiness probes
     - Progressive rollout with pause for validation

2. **Generate comprehensive implementation** (3500 tokens):
   - **Kubernetes advanced**:
     - Deployment with progressive rollout strategy
     - HorizontalPodAutoscaler for capacity management
     - Service mesh integration (Istio VirtualService for traffic splitting)
     - Automated rollback with kubectl rollout undo
   - **ECS advanced**:
     - Service with deployment circuit breaker
     - ALB target groups for blue-green
     - CloudWatch alarms for automated rollback
     - CodeDeploy integration for progressive rollout
   - **Lambda advanced**:
     - Alias-based traffic shifting with versions
     - CloudWatch alarms monitoring invocation errors
     - Automated rollback via SAM or CDK
     - Gradual deployment with 10-minute increments
   - **Monitoring and validation**:
     - Real-time metrics dashboard for deployment progress
     - Automated health checks at each stage
     - SLO compliance monitoring during deployment
     - Alert configuration for deployment failures
   - **Rollback automation**:
     - Automated rollback scripts triggered by metrics
     - Database migration rollback procedures (if applicable)
     - State reconciliation after rollback
     - Post-rollback verification tests

**Sources cited** (accessed 2025-10-26T01:33:56-04:00):

- **Kubernetes Deployments**: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- **AWS ECS Deployment**: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html
- **Martin Fowler - Blue-Green**: https://martinfowler.com/bliki/BlueGreenDeployment.html
- **Google SRE - Canarying**: https://sre.google/workbook/canarying-releases/

---

### Tier 3 (Deep Dive, ≤12k tokens)

**Token budget**: ≤12k tokens

**Scope**: Enterprise deployment with multi-region coordination, database migrations, and compliance.

**Steps:**

1. **Multi-region deployment orchestration** (4000 tokens):
   - Regional rollout sequencing (canary region → low-traffic regions → high-traffic regions)
   - Traffic management across regions with global load balancing
   - Data consistency during multi-region deployment
   - Partial rollback (rollback specific regions while maintaining others)
   - Disaster recovery integration

2. **Database and stateful service migrations** (4000 tokens):
   - Schema migration strategies (expand-contract pattern)
   - Zero-downtime database migrations:
     - Read replica promotion
     - Dual-write pattern with eventual consistency
     - Online schema change tools (gh-ost, pt-online-schema-change)
   - Stateful application versioning (version compatibility matrix)
   - Data migration validation and reconciliation
   - Rollback procedures for database changes

3. **Compliance and governance** (4000 tokens):
   - Change approval workflows (ITIL, CAB processes)
   - Deployment windows and blackout periods
   - Audit trail and evidence collection
   - Compliance gates (security scan, policy validation)
   - Deployment notifications and stakeholder communication
   - Post-deployment review and retrospective automation

**Additional sources** (accessed 2025-10-26T01:33:56-04:00):

- **GitHub gh-ost**: https://github.com/github/gh-ost
- **AWS Multi-Region Deployment**: https://aws.amazon.com/solutions/implementations/multi-region-application-architecture/
- **Database Reliability Engineering**: https://www.oreilly.com/library/view/database-reliability-engineering/9781491925935/

---

## Decision Rules

**Strategy selection matrix:**

| Requirement | Rolling | Blue-Green | Canary | Recreate |
|-------------|---------|------------|--------|----------|
| Zero downtime | ✓ | ✓ | ✓ | ✗ |
| Instant rollback | ✗ | ✓ | ✗ | ✗ |
| Risk mitigation | ✓ | ✓✓ | ✓✓✓ | ✗ |
| Resource efficient | ✓ | ✗ (2x) | ✓ | ✓✓ |
| Stateful apps | ✓ (care) | ✗ | ✗ | ✓ |
| Complexity | Low | Medium | High | Low |

**Health check configuration:**

- Readiness probe: Application ready to serve traffic
- Liveness probe: Application is healthy and should not be restarted
- Startup probe: Application has completed initialization
- Health check intervals: 10-30 seconds during deployment

**Rollback decision criteria:**

- **Automated rollback**: Error rate > 5%, critical alerts, health check failures
- **Manual rollback**: Performance degradation, business metrics impact, stakeholder decision
- **No rollback**: Minor warnings, acceptable performance degradation within SLO

**Escalation conditions:**

- Novel deployment pattern not covered by standard strategies
- Requirements exceed T3 scope (multi-cloud coordination, regulatory constraints)
- Custom orchestration tooling development required

**Abort conditions:**

- Platform limitations prevent required strategy
- Conflicting requirements (e.g., "zero downtime" with "database schema breaking change")
- Resource constraints incompatible with strategy (blue-green needs 2x capacity)

---

## Output Contract

**Required outputs:**

```json
{
  "strategy_document": {
    "type": "markdown",
    "properties": {
      "selected_strategy": "string (rolling|blue-green|canary|recreate)",
      "decision_rationale": "string",
      "deployment_phases": "array of phase descriptions",
      "success_criteria": "array of validation checks",
      "rollback_triggers": "array of conditions"
    }
  },
  "implementation_config": {
    "type": "object",
    "properties": {
      "platform": "string (kubernetes|ecs|lambda)",
      "config_files": [
        {
          "file_path": "string",
          "content": "string (YAML, JSON, or HCL)",
          "description": "string"
        }
      ]
    }
  },
  "rollback_procedure": {
    "type": "markdown",
    "properties": {
      "detection_methods": "string",
      "rollback_steps": "array of steps",
      "automation_scripts": "optional code snippets",
      "verification_steps": "array of post-rollback checks"
    }
  }
}
```

**Quality guarantees:**

- Deployment strategy matches requirements and constraints
- Implementation configuration is valid for target platform
- Rollback procedure is tested and executable
- Health checks configured to detect failures early
- Success criteria are measurable and objective

---

## Examples

**Example: Kubernetes rolling deployment with automated rollback**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: api
        image: api:v2.0.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
```

**Rollback command**: `kubectl rollout undo deployment/api-service`

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens (basic strategy selection and documentation)
- **T2**: ≤6k tokens (advanced strategies with automation)
- **T3**: ≤12k tokens (multi-region, stateful, compliance)

**Safety checks:**

- Health checks configured to prevent unhealthy deployments
- Rollback procedures tested and validated
- Monitoring and alerting in place before deployment
- Deployment windows respect business constraints

**Auditability:**

- All deployments logged with version, timestamp, and actor
- Approval records maintained for production deployments
- Rollback events documented with reason and outcome

**Determinism:**

- Same inputs produce identical deployment strategy
- Health check thresholds based on data-driven baselines
- Automated decisions reproducible and explainable

---

## Resources

**Official Documentation** (accessed 2025-10-26T01:33:56-04:00):

- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- AWS ECS Deployment: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html
- AWS Lambda Deployment: https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html
- Istio Traffic Management: https://istio.io/latest/docs/concepts/traffic-management/

**Best Practices** (accessed 2025-10-26T01:33:56-04:00):

- Martin Fowler - Blue-Green Deployment: https://martinfowler.com/bliki/BlueGreenDeployment.html
- Martin Fowler - Canary Release: https://martinfowler.com/bliki/CanaryRelease.html
- Google SRE - Canarying Releases: https://sre.google/workbook/canarying-releases/
- DORA Deployment Frequency: https://dora.dev/

**Templates** (in repository `/resources/`):

- Kubernetes rolling deployment manifests
- ECS blue-green deployment with CodeDeploy
- Lambda canary deployment with SAM
- Rollback automation scripts
