# Agent→Skill Dependency Graph

## Summary Statistics

- **Total Agents**: 18
- **Unique Skills Referenced**: 30
- **Total Skill References**: 40
- **Avg Skills per Agent**: 2.2

## Agent Dependencies

| Agent | Skills Referenced | Count |
|-------|-------------------|-------|
| agent-creator |  | 0 |
| architecture-decision-orchestrator |  | 0 |
| cloud-aws-orchestrator |  | 0 |
| cloud-azure-orchestrator |  | 0 |
| cloud-gcp-orchestrator |  | 0 |
| cloud-native-orchestrator |  | 0 |
| compliance-orchestrator | compliance-oscal-validator | 1 |
| cost-optimization-orchestrator | finops-cost-analyzer | 1 |
| database-migration-orchestrator | data-pipeline-designer, database-optimization-analyzer, testing-strategy-composer | 3 |
| design-system-builder | documentation-content-generator, frontend-designsystem-validator, frontend-framework-advisor, ... (+1 more) | 4 |
| devops-pipeline-orchestrator | devops-cicd-generator, devops-deployment-designer, devops-iac-generator, ... (+1 more) | 4 |
| disaster-recovery-orchestrator |  | 0 |
| incident-response-orchestrator |  | 0 |
| multi-region-orchestrator | cloud-kubernetes-integrator, cloud-multicloud-advisor, database-optimization-analyzer, ... (+3 more) | 6 |
| observability-orchestrator | observability-stack-configurator | 1 |
| performance-orchestrator | cloud-edge-architect, container-image-optimizer, database-optimization-analyzer, ... (+2 more) | 5 |
| security-auditor | security-cloud-analyzer, security-container-validator, security-crypto-validator, ... (+4 more) | 7 |
| testing-orchestrator | api-contract-testing, devops-cicd-generator, e2e-testing-generator, ... (+5 more) | 8 |

## Skill Usage by Agents

| Skill | Used By Agents | Count |
|-------|----------------|-------|
| database-optimization-analyzer | database-migration-orchestrator, multi-region-orchestrator, ... (+1 more) | 3 |
| observability-stack-configurator | devops-pipeline-orchestrator, observability-orchestrator, ... (+1 more) | 3 |
| finops-cost-analyzer | cost-optimization-orchestrator, performance-orchestrator | 2 |
| testing-strategy-composer | database-migration-orchestrator, testing-orchestrator | 2 |
| devops-cicd-generator | devops-pipeline-orchestrator, testing-orchestrator | 2 |
| devops-deployment-designer | devops-pipeline-orchestrator, multi-region-orchestrator | 2 |
| devops-iac-generator | devops-pipeline-orchestrator, multi-region-orchestrator | 2 |
| security-network-validator | multi-region-orchestrator, security-auditor | 2 |
| compliance-oscal-validator | compliance-orchestrator | 1 |
| data-pipeline-designer | database-migration-orchestrator | 1 |
| documentation-content-generator | design-system-builder | 1 |
| frontend-designsystem-validator | design-system-builder | 1 |
| frontend-framework-advisor | design-system-builder | 1 |
| ux-wireframe-designer | design-system-builder | 1 |
| cloud-kubernetes-integrator | multi-region-orchestrator | 1 |
| cloud-multicloud-advisor | multi-region-orchestrator | 1 |
| cloud-edge-architect | performance-orchestrator | 1 |
| container-image-optimizer | performance-orchestrator | 1 |
| security-cloud-analyzer | security-auditor | 1 |
| security-container-validator | security-auditor | 1 |
| security-crypto-validator | security-auditor | 1 |
| security-iam-reviewer | security-auditor | 1 |
| security-os-validator | security-auditor | 1 |
| security-zerotrust-assessor | security-auditor | 1 |
| api-contract-testing | testing-orchestrator | 1 |
| e2e-testing-generator | testing-orchestrator | 1 |
| testing-chaos-designer | testing-orchestrator | 1 |
| testing-integration-designer | testing-orchestrator | 1 |
| testing-load-designer | testing-orchestrator | 1 |
| testing-unit-generator | testing-orchestrator | 1 |

## Insights

### Orphaned Skills (35)

Skills not referenced by any agent (directly user-invoked or routing-based):

- `api-design-validator`
- `api-graphql-designer`
- `architecture-decision-framework`
- `cloud-aws-architect`
- `cloud-serverless-designer`
- `compliance-automation-engine`
- `compliance-fedramp-validator`
- `core-agent-authoring`
- `core-codex-delegator`
- `core-gemini-delegator`
- `core-skill-authoring`
- `database-migration-generator`
- `database-schema-designer`
- `devops-drift-detector`
- `integration-messagequeue-designer`
- `kubernetes-helm-builder`
- `kubernetes-manifest-generator`
- `kubernetes-servicemesh-configurator`
- `microservices-pattern-architect`
- `mlops-lifecycle-manager`
- ... and 15 more

### Heavily Referenced Skills (8)

Skills used by multiple agents:

- **database-optimization-analyzer** (3 agents): database-migration-orchestrator, multi-region-orchestrator, performance-orchestrator
- **observability-stack-configurator** (3 agents): devops-pipeline-orchestrator, observability-orchestrator, performance-orchestrator
- **finops-cost-analyzer** (2 agents): cost-optimization-orchestrator, performance-orchestrator
- **testing-strategy-composer** (2 agents): database-migration-orchestrator, testing-orchestrator
- **devops-cicd-generator** (2 agents): devops-pipeline-orchestrator, testing-orchestrator
- **devops-deployment-designer** (2 agents): devops-pipeline-orchestrator, multi-region-orchestrator
- **devops-iac-generator** (2 agents): devops-pipeline-orchestrator, multi-region-orchestrator
- **security-network-validator** (2 agents): multi-region-orchestrator, security-auditor

### Agents with No Skill Dependencies (8)

- `agent-creator`
- `architecture-decision-orchestrator`
- `cloud-aws-orchestrator`
- `cloud-azure-orchestrator`
- `cloud-gcp-orchestrator`
- `cloud-native-orchestrator`
- `disaster-recovery-orchestrator`
- `incident-response-orchestrator`

## Dependency Graph Visualization

```mermaid
graph LR
  classDef agent fill:#e1f5ff,stroke:#01579b,stroke-width:2px
  classDef skill fill:#fff3e0,stroke:#e65100,stroke-width:1px

  agent_creator[Agent Creator]:::agent
  architecture_decision_orchestrator[Architecture Decision Orchestrator]:::agent
  cloud_aws_orchestrator[AWS Cloud Architect]:::agent
  cloud_azure_orchestrator[Azure Cloud Architect]:::agent
  cloud_gcp_orchestrator[GCP Cloud Architect]:::agent
  cloud_native_orchestrator[Cloud-Native Deployment Orchestrator]:::agent
  compliance_orchestrator[Compliance Orchestrator]:::agent
  cost_optimization_orchestrator[Cost Optimization Orchestrator]:::agent
  database_migration_orchestrator[Database Migration Orchestrator]:::agent
  design_system_builder[Design System Builder]:::agent
  devops_pipeline_orchestrator[DevOps Pipeline Orchestrator]:::agent
  disaster_recovery_orchestrator[Disaster Recovery Orchestrator]:::agent
  incident_response_orchestrator[Incident Response Orchestrator]:::agent
  multi_region_orchestrator[Multi-Region Deployment Orchestrator]:::agent
  observability_orchestrator[Observability Orchestrator]:::agent
  performance_orchestrator[Performance Orchestrator]:::agent
  security_auditor[Security Auditor]:::agent
  testing_orchestrator[Testing Strategy Orchestrator]:::agent

  api_contract_testing[api-contract-testing]:::skill
  cloud_edge_architect[cloud-edge-architect]:::skill
  cloud_kubernetes_integrator[cloud-kubernetes-integrator]:::skill
  cloud_multicloud_advisor[cloud-multicloud-advisor]:::skill
  compliance_oscal_validator[compliance-oscal-validator]:::skill
  container_image_optimizer[container-image-optimizer]:::skill
  data_pipeline_designer[data-pipeline-designer]:::skill
  database_optimization_analyzer[database-optimization-analyzer]:::skill
  devops_cicd_generator[devops-cicd-generator]:::skill
  devops_deployment_designer[devops-deployment-designer]:::skill
  devops_iac_generator[devops-iac-generator]:::skill
  documentation_content_generator[documentation-content-generator]:::skill
  e2e_testing_generator[e2e-testing-generator]:::skill
  finops_cost_analyzer[finops-cost-analyzer]:::skill
  frontend_designsystem_validator[frontend-designsystem-validator]:::skill
  frontend_framework_advisor[frontend-framework-advisor]:::skill
  observability_stack_configurator[observability-stack-configurator]:::skill
  security_cloud_analyzer[security-cloud-analyzer]:::skill
  security_container_validator[security-container-validator]:::skill
  security_crypto_validator[security-crypto-validator]:::skill
  security_iam_reviewer[security-iam-reviewer]:::skill
  security_network_validator[security-network-validator]:::skill
  security_os_validator[security-os-validator]:::skill
  security_zerotrust_assessor[security-zerotrust-assessor]:::skill
  testing_chaos_designer[testing-chaos-designer]:::skill
  testing_integration_designer[testing-integration-designer]:::skill
  testing_load_designer[testing-load-designer]:::skill
  testing_strategy_composer[testing-strategy-composer]:::skill
  testing_unit_generator[testing-unit-generator]:::skill
  ux_wireframe_designer[ux-wireframe-designer]:::skill

  compliance_orchestrator --> compliance_oscal_validator
  cost_optimization_orchestrator --> finops_cost_analyzer
  database_migration_orchestrator --> data_pipeline_designer
  database_migration_orchestrator --> database_optimization_analyzer
  database_migration_orchestrator --> testing_strategy_composer
  design_system_builder --> documentation_content_generator
  design_system_builder --> frontend_designsystem_validator
  design_system_builder --> frontend_framework_advisor
  design_system_builder --> ux_wireframe_designer
  devops_pipeline_orchestrator --> devops_cicd_generator
  devops_pipeline_orchestrator --> devops_deployment_designer
  devops_pipeline_orchestrator --> devops_iac_generator
  devops_pipeline_orchestrator --> observability_stack_configurator
  multi_region_orchestrator --> cloud_kubernetes_integrator
  multi_region_orchestrator --> cloud_multicloud_advisor
  multi_region_orchestrator --> database_optimization_analyzer
  multi_region_orchestrator --> devops_deployment_designer
  multi_region_orchestrator --> devops_iac_generator
  multi_region_orchestrator --> security_network_validator
  observability_orchestrator --> observability_stack_configurator
  performance_orchestrator --> cloud_edge_architect
  performance_orchestrator --> container_image_optimizer
  performance_orchestrator --> database_optimization_analyzer
  performance_orchestrator --> finops_cost_analyzer
  performance_orchestrator --> observability_stack_configurator
  security_auditor --> security_cloud_analyzer
  security_auditor --> security_container_validator
  security_auditor --> security_crypto_validator
  security_auditor --> security_iam_reviewer
  security_auditor --> security_network_validator
  security_auditor --> security_os_validator
  security_auditor --> security_zerotrust_assessor
  testing_orchestrator --> api_contract_testing
  testing_orchestrator --> devops_cicd_generator
  testing_orchestrator --> e2e_testing_generator
  testing_orchestrator --> testing_chaos_designer
  testing_orchestrator --> testing_integration_designer
  testing_orchestrator --> testing_load_designer
  testing_orchestrator --> testing_strategy_composer
  testing_orchestrator --> testing_unit_generator
```
