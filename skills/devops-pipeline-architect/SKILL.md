---
name: "DevOps Pipeline Architect"
slug: devops-pipeline-architect
description: "Design CI/CD pipelines, IaC templates, and observability stacks with platform-specific integrations and best practices."
capabilities:
  - design_cicd_pipelines
  - generate_platform_configs
  - create_iac_templates
  - configure_observability_stack
  - implement_deployment_strategies
inputs:
  platform:
    type: string
    description: "Target platform: github-actions, gitlab-ci, jenkins, azure-devops, or multi"
    required: true
  tech_stack:
    type: array
    description: "Languages, frameworks, and deployment targets (k8s, lambda, ecs, etc.)"
    required: true
  requirements:
    type: object
    description: "Testing needs, security gates, deployment strategy, observability requirements"
    required: true
  infrastructure:
    type: object
    description: "Cloud provider, IaC tool preference (terraform/cloudformation/pulumi), environments"
    required: false
outputs:
  pipeline_config:
    type: code
    description: "Platform-specific CI/CD configuration file(s)"
  iac_templates:
    type: code
    description: "Infrastructure as Code modules for deployment targets"
  observability_config:
    type: code
    description: "Monitoring, logging, and tracing configurations"
  deployment_strategy:
    type: markdown
    description: "Detailed deployment approach with rollback procedures"
keywords:
  - cicd
  - github-actions
  - gitlab-ci
  - jenkins
  - infrastructure-as-code
  - terraform
  - observability
  - monitoring
  - deployment
  - devops
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: required
links:
  - https://docs.github.com/en/actions
  - https://docs.gitlab.com/ee/ci/
  - https://www.jenkins.io/doc/book/pipeline/
  - https://developer.hashicorp.com/terraform/docs
  - https://opentelemetry.io/docs/
---

## Purpose & When-To-Use

**Trigger conditions:**

- New project needs CI/CD pipeline setup from scratch
- Existing pipeline requires modernization or platform migration
- Infrastructure drift detected; need IaC implementation
- Production incidents reveal observability gaps
- Multi-environment deployment strategy needed (dev/staging/prod)
- Deployment automation missing or manual
- Compliance requirements demand auditable deployment processes

**Use this skill when** you need end-to-end DevOps pipeline design that integrates build, test, deploy, and monitor phases with platform-specific optimizations and industry best practices.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-25T21:30:36-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `platform` is one of: `github-actions`, `gitlab-ci`, `jenkins`, `azure-devops`, `circleci`, `multi`
   - `tech_stack` contains valid identifiers (e.g., `python`, `nodejs`, `docker`, `kubernetes`)
   - `requirements.testing` specifies test types and coverage targets
   - `requirements.security_gates` lists required checks (SAST, SCA, secret scanning, etc.)
   - `requirements.deployment_strategy` indicates approach: `rolling`, `blue-green`, `canary`, or `recreate`
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Platform access**: Confirm target platform and IaC tools are accessible/licensed

**Abort conditions:**

- Platform is proprietary/undocumented with no public API
- Tech stack contains conflicting deployment targets (e.g., serverless + stateful containers without clear separation)
- Requirements demand sub-second deployment latency (unrealistic for most CD systems)
- No test strategy defined and security gates require test coverage metrics

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Generate basic CI/CD pipeline for common tech stacks (Node.js, Python, Java, Go) with standard testing and deployment to single environment.

**Steps:**

1. **Analyze inputs** (50 tokens):
   - Determine platform and language
   - Identify deployment target (VM, container, serverless)

2. **Select pipeline template** (100 tokens):
   - GitHub Actions: `.github/workflows/ci-cd.yml`
   - GitLab CI: `.gitlab-ci.yml`
   - Jenkins: `Jenkinsfile`

3. **Generate base pipeline** (800 tokens):
   - **Build stage**: Install dependencies, compile/build
   - **Test stage**: Run unit and integration tests
   - **Security stage**: SAST scan, dependency check
   - **Deploy stage**: Push to container registry or deploy to target
   - Include caching for dependencies
   - Use matrix builds for multi-version testing if applicable

4. **Add basic observability** (300 tokens):
   - Pipeline execution metrics (build time, failure rate)
   - Simple health check endpoint monitoring
   - Log aggregation configuration

5. **Output artifacts** (750 tokens):
   - Primary pipeline configuration file
   - README with setup instructions
   - Environment variable checklist

**Decision point**: If requirements include multiple environments, IaC, advanced deployment strategies, or custom observability → escalate to T2.

---

### Tier 2 (Extended Analysis, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Multi-environment pipelines with IaC integration, advanced deployment strategies, comprehensive observability, and security hardening.

**Steps:**

1. **Environment strategy design** (400 tokens):
   - Define environment progression: dev → staging → prod
   - Configure environment-specific variables and secrets management
   - Implement promotion gates (manual approval, automated checks)

2. **Infrastructure as Code integration** (1200 tokens):
   - **Terraform** (accessed 2025-10-25T21:30:36-04:00): Generate modules for VPC, compute, storage, networking
     - Use remote state (S3 + DynamoDB or Terraform Cloud)
     - Implement workspaces for environment isolation
     - Include `terraform plan` in pipeline with approval gate
   - **CloudFormation/CDK**: Generate stacks with cross-stack references
   - **Pulumi**: Generate programs in language matching tech_stack
   - Version and store IaC templates in repository
   - Apply IaC changes via pipeline automation

3. **Advanced deployment strategies** (800 tokens):
   - **Blue-Green** (accessed 2025-10-25T21:30:36-04:00):
     - Provision parallel environments
     - Traffic switching via load balancer or DNS
     - Automated rollback on health check failure
   - **Canary** (accessed 2025-10-25T21:30:36-04:00):
     - Progressive traffic shifting (5% → 25% → 50% → 100%)
     - Metric-based promotion criteria
     - Automatic rollback on error rate threshold
   - **Rolling**: Zero-downtime updates with health checks
   - Generate platform-specific implementation (K8s, ECS, serverless)

4. **Comprehensive observability stack** (1000 tokens):
   - **Metrics** (Prometheus, CloudWatch, Datadog):
     - Application metrics: request rate, error rate, latency (RED method)
     - Infrastructure metrics: CPU, memory, disk, network
     - Business metrics: throughput, conversion, SLIs
   - **Logging** (ELK, Loki, CloudWatch Logs):
     - Structured logging configuration
     - Log correlation with trace IDs
     - Retention policies and cost optimization
   - **Tracing** (OpenTelemetry, Jaeger, X-Ray):
     - Distributed tracing instrumentation
     - Service dependency mapping
     - Performance bottleneck identification
   - **Alerting**:
     - Threshold-based and anomaly detection
     - Alert routing and escalation policies
     - Runbook links in alert descriptions

5. **Security hardening** (700 tokens):
   - **SAST** (SonarQube, Semgrep): Static code analysis for vulnerabilities
   - **SCA** (Snyk, Dependabot): Dependency vulnerability scanning with auto-remediation
   - **Secret scanning**: Pre-commit hooks and pipeline checks (git-secrets, truffleHog)
   - **Container scanning** (Trivy, Clair): Image vulnerability analysis
   - **DAST** (optional): Dynamic testing against staging environment
   - **Compliance gates**: Policy-as-code (OPA, Sentinel) for infrastructure validation
   - Sign artifacts with Cosign/Sigstore for supply chain security

6. **Testing integration** (500 tokens):
   - Invoke `testing-strategy-composer` skill (dependency) for test scaffolding
   - Integrate unit, integration, e2e, and performance tests into pipeline
   - Parallel test execution for speed
   - Code coverage reporting with quality gates (e.g., minimum 80%)
   - Performance benchmarking with baseline comparison

7. **Documentation and outputs** (400 tokens):
   - Architecture diagrams (deployment flow, infrastructure)
   - Runbooks for common operations (rollback, scale-up, incident response)
   - Pipeline configuration with inline comments
   - IaC templates with variable documentation
   - Observability dashboard templates

**Sources cited** (accessed 2025-10-25T21:30:36-04:00):

- **GitHub Actions**: https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider
- **GitLab CI/CD**: https://docs.gitlab.com/ee/ci/yaml/
- **Jenkins Pipeline**: https://www.jenkins.io/doc/book/pipeline/syntax/
- **Terraform Best Practices**: https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices
- **OpenTelemetry**: https://opentelemetry.io/docs/concepts/
- **DORA Metrics**: https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance

---

### Tier 3 (Deep Dive, not implemented)

**Token budget**: T3 not implemented for this skill

**Rationale**: T2 tier provides comprehensive coverage for DevOps pipeline design. T3 would potentially cover highly specialized scenarios (multi-region active-active, custom compliance automation, novel deployment patterns) that are better handled through expert consultation or custom skill development.

---

## Decision Rules

**Platform selection criteria:**

- **GitHub Actions**: Best for GitHub-hosted projects, generous free tier, extensive marketplace
- **GitLab CI**: Best for GitLab projects, integrated security scanning, robust Kubernetes integration
- **Jenkins**: Best for on-premise requirements, maximum flexibility, steep learning curve
- **Azure DevOps**: Best for Microsoft stack integration, enterprise compliance features
- **Multi-platform**: Generate portable configurations (e.g., Docker-based workflows)

**Deployment strategy selection:**

- **Rolling**: Default for stateless applications, simple and reliable
- **Blue-Green**: High-confidence releases, critical services, allows instant rollback
- **Canary**: Risk mitigation for user-facing changes, requires robust monitoring
- **Recreate**: Acceptable downtime, cost-sensitive deployments

**IaC tool selection:**

- **Terraform**: Multi-cloud, large community, HCL declarative syntax
- **CloudFormation/CDK**: AWS-native, tight integration, no state management overhead
- **Pulumi**: Prefer familiar languages (Python, TypeScript), programmatic flexibility

**Escalation conditions:**

- Requirements exceed T2 scope (multi-region active-active, complex compliance automation)
- Novel technology stack without established pipeline patterns
- Custom tooling integration requiring development work

**Abort conditions:**

- Conflicting requirements (e.g., "instant rollback" with "recreate strategy")
- Missing critical information and stakeholder unavailable for clarification
- Platform limitations prevent security requirements (e.g., air-gapped Jenkins without approved SAST tool)

---

## Output Contract

**Required outputs:**

```json
{
  "pipeline_config": {
    "type": "object",
    "properties": {
      "platform": "string (github-actions|gitlab-ci|jenkins|azure-devops)",
      "files": [
        {
          "path": "string (.github/workflows/ci-cd.yml, .gitlab-ci.yml, Jenkinsfile)",
          "content": "string (complete configuration)",
          "language": "string (yaml|groovy)"
        }
      ],
      "secrets_required": ["array of secret names"],
      "estimated_runtime": "string (e.g., '5-8 minutes')"
    }
  },
  "iac_templates": {
    "type": "object",
    "properties": {
      "tool": "string (terraform|cloudformation|pulumi)",
      "modules": [
        {
          "name": "string (vpc, compute, storage, etc.)",
          "path": "string (relative path)",
          "content": "string (IaC code)",
          "variables": ["array of variable definitions"]
        }
      ]
    }
  },
  "observability_config": {
    "type": "object",
    "properties": {
      "metrics": "string (Prometheus config, CloudWatch alarms, etc.)",
      "logging": "string (logging configuration)",
      "tracing": "string (OpenTelemetry config)",
      "dashboards": ["array of dashboard JSON/YAML"]
    }
  },
  "deployment_strategy": {
    "type": "markdown",
    "description": "Detailed strategy document with rollback procedures"
  },
  "documentation": {
    "type": "object",
    "properties": {
      "setup_guide": "markdown",
      "architecture_diagram": "mermaid or link",
      "runbooks": ["array of operational runbooks"]
    }
  }
}
```

**Quality guarantees:**

- Pipeline configurations are syntactically valid for target platform
- IaC templates pass validation (`terraform validate`, `cfn-lint`)
- All secrets referenced but never hardcoded
- Observability configurations include at minimum: error rate, latency, throughput metrics
- Deployment strategy includes explicit rollback procedure

---

## Examples

**Example 1: GitHub Actions pipeline for Node.js app deployed to AWS ECS**

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci && npm run lint
      - run: npm test -- --coverage
      - run: npm run build

  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
      - run: aws ecs update-service --cluster staging --service api --force-new-deployment
```

*Full example in `/resources/github-actions-nodejs-template.yml`*

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens (basic single-environment pipeline)
- **T2**: ≤6k tokens (multi-environment with IaC and observability)

**Safety checks:**

- No hardcoded secrets in generated configurations
- All external dependencies pinned to specific versions (prevent supply chain attacks)
- Security scanning stages are blocking (fail pipeline on critical vulnerabilities)
- IaC state stored in secure, versioned backend (never local)

**Auditability:**

- All pipeline runs logged with timestamps and actor
- IaC changes tracked in git with plan output in PR comments
- Deployment approvals recorded with approver identity
- Observability data retained per compliance requirements (typically 30-90 days)

**Determinism:**

- Same inputs produce same pipeline configuration
- Dependency versions locked (package.lock, Gemfile.lock, go.sum)
- Build environments reproducible (containerized or versioned base images)

---

## Resources

**Official Documentation** (accessed 2025-10-25T21:30:36-04:00):

- GitHub Actions: https://docs.github.com/en/actions
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- Jenkins Documentation: https://www.jenkins.io/doc/
- Terraform Registry: https://registry.terraform.io/
- OpenTelemetry: https://opentelemetry.io/docs/
- Prometheus: https://prometheus.io/docs/introduction/overview/

**Best Practices** (accessed 2025-10-25T21:30:36-04:00):

- Google SRE Books: https://sre.google/books/
- DORA State of DevOps: https://dora.dev/research/
- CNCF Cloud Native Glossary: https://glossary.cncf.io/

**Templates** (in `/resources/`):

- `github-actions-templates/`: Node.js, Python, Go, Java workflows
- `gitlab-ci-templates/`: Multi-stage pipelines with security scanning
- `jenkins-templates/`: Declarative and scripted pipelines
- `terraform-modules/`: AWS, Azure, GCP infrastructure patterns
- `observability-configs/`: Prometheus, Grafana, OpenTelemetry setups
