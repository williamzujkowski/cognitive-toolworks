# DevOps Pipeline Orchestration Workflow

## Overview

This workflow defines the 4-step orchestration pattern for coordinating specialized DevOps skills.

---

## Workflow Steps

### Step 1: CI/CD Pipeline Generation

**Skill**: `cicd-pipeline-generator`

**Inputs**:
- `platform`: CI/CD platform (from orchestrator input)
- `tech_stack`: Application technologies (from orchestrator input)
- `stages`: Derived from requirements (build, test, security, deploy)

**Tier selection**:
- **T1**: Single environment, basic stages
- **T2**: Multi-environment, advanced security gates, approval workflows
- **T3**: Enterprise compliance, custom integrations

**Outputs captured**:
- `pipeline_config`: CI/CD configuration file(s)
- `setup_guide`: Secrets and variables documentation

**Integration needs**:
- Pipeline must reference IaC deployment commands
- Pipeline must reference deployment strategy execution

---

### Step 2: Infrastructure as Code Generation

**Skill**: `iac-template-generator`

**Inputs**:
- `iac_tool`: Derived from cloud_provider (terraform for multi-cloud, cloudformation for AWS-only)
- `cloud_provider`: From orchestrator input
- `resources`: Derived from tech_stack (e.g., kubernetes → EKS, docker → ECS)
- `environments`: From requirements

**Tier selection**:
- **T1**: Single environment, basic resources
- **T2**: Multi-environment with security hardening
- **T3**: Policy-as-code, multi-cloud orchestration

**Outputs captured**:
- `iac_templates`: Infrastructure modules
- `state_config`: Remote state backend configuration

**Integration needs**:
- CI/CD pipeline includes IaC apply stages
- Deployment strategy references provisioned infrastructure

---

### Step 3: Observability Stack Configuration

**Skill**: `observability-stack-configurator`

**Inputs**:
- `platform`: Derived from deployment target (kubernetes, aws, etc.)
- `tech_stack`: From orchestrator input
- `requirements`: From orchestrator requirements.observability

**Tier selection**:
- **T1**: Basic metrics and logs
- **T2**: Distributed tracing, SLO tracking, advanced alerting
- **T3**: AI/ML insights, security monitoring

**Outputs captured**:
- `metrics_config`: Prometheus/CloudWatch configuration
- `logging_config`: Log aggregation configuration
- `tracing_config`: OpenTelemetry instrumentation
- `dashboards`: Grafana/CloudWatch dashboards
- `alerting_rules`: Alert configurations

**Integration needs**:
- Deployment strategy references health check endpoints
- CI/CD pipeline includes observability deployment
- IaC provisions observability infrastructure

---

### Step 4: Deployment Strategy Design

**Skill**: `deployment-strategy-designer`

**Inputs**:
- `deployment_target`: Derived from tech_stack (kubernetes, ecs, lambda)
- `application_type`: Inferred from tech_stack (stateless vs stateful)
- `requirements`: From orchestrator requirements (downtime_tolerance, rollback_time)

**Tier selection**:
- **T1**: Basic strategy (rolling, recreate)
- **T2**: Advanced strategies (canary, blue-green) with automation
- **T3**: Multi-region, database migrations

**Outputs captured**:
- `strategy_document`: Deployment strategy with rationale
- `implementation_config`: Platform-specific deployment configuration
- `rollback_procedure`: Rollback steps and automation

**Integration needs**:
- CI/CD pipeline executes deployment strategy
- Deployment references observability metrics for health checks
- Strategy assumes IaC-provisioned infrastructure

---

## Integration Phase

After all 4 skills complete, orchestrator performs integration:

1. **Validate consistency**:
   - CI/CD platform matches deployment target capabilities
   - IaC cloud provider matches deployment platform
   - Observability platform compatible with deployment target

2. **Generate integration guide**:
   - How CI/CD invokes IaC (terraform apply, cloudformation deploy)
   - How CI/CD executes deployment (kubectl apply, ecs update-service)
   - How deployment references observability (health checks, metrics)
   - Shared environment variables and secrets

3. **Generate setup guide**:
   - Prerequisites (accounts, tools, permissions)
   - Execution sequence:
     1. Provision infrastructure via IaC
     2. Deploy observability stack
     3. Configure CI/CD pipeline
     4. Execute first deployment using strategy
   - Validation steps at each stage

4. **Generate validation checklist**:
   - [ ] IaC state backend configured and accessible
   - [ ] CI/CD platform authorized and secrets configured
   - [ ] Observability stack deployed and collecting metrics
   - [ ] Deployment strategy tested with rollback verification
   - [ ] Integration points functional (CI/CD → IaC → Deploy → Monitor)

---

## Error Handling

**Skill failure**:
- Log which skill failed and why
- Surface error to user with context
- Abort orchestration (do not proceed to dependent steps)
- Provide remediation guidance if available

**Integration failure**:
- Identify incompatible outputs
- Suggest configuration changes
- Offer alternative approaches
- Do not proceed to deployment

**Token budget exceeded**:
- Identify which skill exceeded budget
- Suggest tier downgrade or requirement simplification
- Abort orchestration if total budget >10k tokens

---

## Success Criteria

Orchestration succeeds when:

1. All 4 skills complete successfully
2. All outputs validated and consistent
3. Integration points clearly documented
4. Setup guide comprehensive and sequenced
5. Validation checklist complete
6. Total token budget ≤10k tokens
