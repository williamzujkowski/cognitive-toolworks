# Migration Guide: devops-pipeline-architect → devops-pipeline-orchestrator

## Overview

The monolithic `devops-pipeline-architect` skill has been refactored into:

- **4 focused skills** (≤2 steps each)
- **1 orchestrator agent** (coordinates the 4 skills)

This migration guide helps users transition from the deprecated skill to the new architecture.

---

## Why the Change?

**Problems with monolithic skill:**

- Violated ≤2 step principle (had 5+ major capabilities)
- Token budget inefficient (loaded everything even for simple use cases)
- Difficult to maintain and test
- Couldn't be composed with other skills easily

**Benefits of new architecture:**

- Each skill focused and reusable independently
- Progressive disclosure: use only what you need
- Better token efficiency
- Easier testing and validation
- Composable with other workflows

---

## Mapping: Old Skill → New Skills

| Old Capability | New Skill | Slug |
|----------------|-----------|------|
| `design_cicd_pipelines` | CI/CD Pipeline Generator | `cicd-pipeline-generator` |
| `generate_platform_configs` | CI/CD Pipeline Generator | `cicd-pipeline-generator` |
| `create_iac_templates` | IaC Template Generator | `iac-template-generator` |
| `configure_observability_stack` | Observability Stack Configurator | `observability-stack-configurator` |
| `implement_deployment_strategies` | Deployment Strategy Designer | `deployment-strategy-designer` |

---

## When to Use What

### Use Individual Skills When:

- **Need only one component**: e.g., just CI/CD pipeline, not full stack
- **Integrating into existing workflow**: e.g., already have IaC, need observability
- **Quick iteration**: testing or prototyping single component

**Examples:**

```
# Just need CI/CD pipeline
Use: skills/cicd-pipeline-generator

# Just need Terraform templates
Use: skills/iac-template-generator

# Just need monitoring setup
Use: skills/observability-stack-configurator

# Just need deployment strategy
Use: skills/deployment-strategy-designer
```

### Use Orchestrator Agent When:

- **End-to-end pipeline needed**: CI/CD + IaC + observability + deployment
- **Greenfield project**: starting from scratch
- **Comprehensive modernization**: upgrading all DevOps components
- **Ensuring integration**: need components to work together seamlessly

**Example:**

```
# Complete DevOps pipeline for new microservice
Use: agents/devops-pipeline-orchestrator
```

---

## Migration Examples

### Example 1: Simple CI/CD Pipeline

**Old approach (devops-pipeline-architect):**
```
Invoke skill with:
- platform: github-actions
- tech_stack: [nodejs]
- requirements: {testing: unit, deploy: single-env}

Result: Full skill loaded (2k-6k tokens) even though only need CI/CD
```

**New approach:**
```
Invoke cicd-pipeline-generator skill with:
- platform: github-actions
- tech_stack: [nodejs]
- stages: {build, test, deploy}

Result: Focused skill (≤2k tokens T1), only what's needed
```

### Example 2: Infrastructure Only

**Old approach:**
```
Invoke devops-pipeline-architect, set requirements to skip CI/CD
- Wasteful: loaded CI/CD logic anyway
- Confusing: had to specify "no CI/CD" requirements
```

**New approach:**
```
Invoke iac-template-generator skill directly with:
- iac_tool: terraform
- cloud_provider: aws
- resources: [vpc, compute, database]

Result: Direct, focused, efficient
```

### Example 3: Complete Pipeline

**Old approach:**
```
Invoke devops-pipeline-architect with complete requirements
- Single monolithic invocation
- T2 tier: ≤6k tokens
- All or nothing approach
```

**New approach (orchestrator):**
```
Invoke devops-pipeline-orchestrator agent with:
- platform: github-actions
- tech_stack: [nodejs, docker, kubernetes]
- cloud_provider: aws
- requirements: {full observability, canary deployment}

Result:
- Orchestrator coordinates 4 skill invocations
- Each skill T1 or T2 as needed
- Total ≤10k tokens with better organization
- Integration guide included
```

---

## Input Schema Changes

### Old Schema (devops-pipeline-architect)

```yaml
inputs:
  platform: string (github-actions, gitlab-ci, jenkins, azure-devops, multi)
  tech_stack: array
  requirements:
    testing: object
    security_gates: array
    deployment_strategy: string
    observability_requirements: object
  infrastructure:
    cloud_provider: string
    iac_tool: string
    environments: array
```

### New Schemas (Individual Skills)

**cicd-pipeline-generator:**
```yaml
inputs:
  platform: string (github-actions, gitlab-ci, jenkins, azure-devops)
  tech_stack: array
  stages: object (build, test, security, deploy)
```

**iac-template-generator:**
```yaml
inputs:
  iac_tool: string (terraform, cloudformation, pulumi, cdk)
  cloud_provider: string (aws, azure, gcp, multi-cloud)
  resources: array
  environments: array (optional)
```

**observability-stack-configurator:**
```yaml
inputs:
  platform: string (kubernetes, aws, azure, gcp, on-premise)
  tech_stack: array
  requirements:
    slis: array
    alerting_rules: object
    retention_policies: object
```

**deployment-strategy-designer:**
```yaml
inputs:
  deployment_target: string (kubernetes, ecs, lambda, vm)
  application_type: string (stateless, stateful, serverless, batch)
  requirements:
    downtime_tolerance: string
    risk_tolerance: string
    rollback_time: string
```

### New Schema (Orchestrator Agent)

```yaml
inputs:
  platform: string (CI/CD platform)
  tech_stack: array
  cloud_provider: string
  requirements:
    environments: array
    security_gates: array
    observability: object
    deployment_strategy: string
    downtime_tolerance: string
```

---

## Breaking Changes

1. **Skill slug**: `devops-pipeline-architect` is deprecated
   - Use individual skills or orchestrator agent

2. **Output structure**: Old skill returned flat structure
   - New orchestrator returns organized by skill domain

3. **Token budgets**: Old T1≤2k, T2≤6k
   - New skills: each has T1≤2k, T2≤6k, T3≤12k
   - Orchestrator: total ≤10k across all skills

4. **Invocation pattern**: Old was single invocation
   - New orchestrator invokes 4 skills sequentially

---

## Deprecation Timeline

- **2025-10-26**: New skills and orchestrator released
- **2025-10-26**: Old skill marked as deprecated (frontmatter update)
- **2026-01-26**: Old skill removed from index (3 months deprecation period)
- **2026-01-26**: Old skill file archived to `/deprecated/`

---

## Support

For questions or issues with migration:

1. Review skill documentation in `/skills/<slug>/SKILL.md`
2. Review agent documentation in `/agents/devops-pipeline-orchestrator/AGENT.md`
3. Check examples in `/skills/<slug>/examples/`
4. Open issue in repository with `migration` label

---

## Quick Reference

| Task | Old Invocation | New Invocation |
|------|----------------|----------------|
| CI/CD only | devops-pipeline-architect (wasteful) | cicd-pipeline-generator |
| IaC only | devops-pipeline-architect (wasteful) | iac-template-generator |
| Observability only | devops-pipeline-architect (wasteful) | observability-stack-configurator |
| Deployment only | devops-pipeline-architect (wasteful) | deployment-strategy-designer |
| Full pipeline | devops-pipeline-architect | devops-pipeline-orchestrator |
