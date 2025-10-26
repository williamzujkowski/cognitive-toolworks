---
name: "CI/CD Pipeline Generator"
slug: cicd-pipeline-generator
description: "Generate platform-specific CI/CD pipeline configurations for GitHub Actions, GitLab CI, Jenkins, and Azure DevOps with build, test, and deploy stages."
capabilities:
  - generate_pipeline_config
  - platform_specific_optimization
inputs:
  platform:
    type: string
    description: "Target platform: github-actions, gitlab-ci, jenkins, azure-devops"
    required: true
  tech_stack:
    type: array
    description: "Languages and frameworks (python, nodejs, java, go, docker)"
    required: true
  stages:
    type: object
    description: "Pipeline stages: build, test, security, deploy configurations"
    required: true
outputs:
  pipeline_config:
    type: code
    description: "Platform-specific CI/CD configuration file"
  setup_guide:
    type: markdown
    description: "Setup instructions and required secrets"
keywords:
  - cicd
  - github-actions
  - gitlab-ci
  - jenkins
  - azure-devops
  - pipeline
  - automation
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
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/
---

## Purpose & When-To-Use

**Trigger conditions:**

- New project needs CI/CD pipeline from scratch
- Migrating between CI/CD platforms
- Standardizing pipeline configurations across projects
- Adding missing stages (security, testing) to existing pipeline
- Tech stack change requires pipeline updates

**Use this skill when** you need a complete, platform-optimized CI/CD pipeline configuration file with build, test, security, and deploy stages.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T01:33:56-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `platform` is one of: `github-actions`, `gitlab-ci`, `jenkins`, `azure-devops`
   - `tech_stack` contains valid language identifiers
   - `stages` object specifies at minimum: build and test configurations
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Platform access**: Confirm target platform is available and licensed

**Abort conditions:**

- Platform is proprietary/undocumented with no public API reference
- Tech stack language not supported by target platform
- Conflicting stage requirements (e.g., parallel and sequential for same stage)

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Generate basic CI/CD pipeline for common tech stacks with standard build, test, and deploy stages.

**Steps:**

1. **Analyze inputs and select template** (300 tokens):
   - Determine platform format (YAML for GitHub Actions/GitLab, Groovy for Jenkins, YAML for Azure DevOps)
   - Identify language-specific runners and dependencies
   - Map stages to platform constructs (jobs, stages, steps)

2. **Generate pipeline configuration** (1700 tokens):
   - **Build stage**: Install dependencies, compile/build artifacts
   - **Test stage**: Run unit and integration tests with coverage
   - **Security stage**: SAST scan, dependency vulnerability check
   - **Deploy stage**: Push to registry or deploy to target environment
   - Include dependency caching for performance
   - Add matrix builds for multi-version testing if applicable
   - Output pipeline file with inline comments
   - Generate setup guide with required secrets and variables

**Decision point**: If requirements include multi-environment deployments, advanced security gates, or custom integrations → escalate to T2.

---

### Tier 2 (Extended Analysis, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Multi-environment pipelines with advanced security, approval gates, and performance optimization.

**Steps:**

1. **Design multi-environment pipeline** (2000 tokens):
   - Configure environment-specific stages (dev, staging, production)
   - Implement promotion gates with manual approvals
   - Add environment-specific variables and secret management
   - Configure conditional execution based on branch patterns
   - **GitHub Actions** (accessed 2025-10-26T01:33:56-04:00): Use environments with protection rules
   - **GitLab CI** (accessed 2025-10-26T01:33:56-04:00): Implement environment-specific jobs with deployment strategies
   - **Jenkins** (accessed 2025-10-26T01:33:56-04:00): Use input steps for approvals and parameters for environments
   - **Azure DevOps** (accessed 2025-10-26T01:33:56-04:00): Configure deployment stages with approval gates

2. **Generate optimized configuration** (4000 tokens):
   - Advanced caching strategies (layer caching, dependency caching, build caching)
   - Parallel job execution for independent stages
   - Security hardening:
     - SAST with SonarQube or Semgrep
     - SCA with Snyk or Dependabot integration
     - Secret scanning with git-secrets or TruffleHog
     - Container image scanning with Trivy
   - Testing integration:
     - Unit, integration, and e2e test suites
     - Code coverage reporting with quality gates (minimum 80%)
     - Performance benchmarking
   - Artifact management:
     - Build artifact storage and versioning
     - Container image tagging strategies
     - Retention policies
   - Notifications and reporting:
     - Slack/Teams notifications for failures
     - Status badges and dashboards
     - Metrics collection (build time, success rate)

**Sources cited** (accessed 2025-10-26T01:33:56-04:00):

- **GitHub Actions**: https://docs.github.com/en/actions/deployment/targeting-different-environments
- **GitLab CI/CD**: https://docs.gitlab.com/ee/ci/yaml/
- **Jenkins Pipeline**: https://www.jenkins.io/doc/book/pipeline/syntax/
- **Azure DevOps Pipelines**: https://learn.microsoft.com/en-us/azure/devops/pipelines/

---

### Tier 3 (Deep Dive, ≤12k tokens)

**Token budget**: ≤12k tokens

**Scope**: Enterprise-grade pipelines with compliance automation, custom plugins, and advanced orchestration.

**Steps:**

1. **Enterprise compliance integration** (4000 tokens):
   - Policy-as-code validation (OPA, Sentinel) in pipeline
   - Compliance artifact generation (SBOM, attestations, audit logs)
   - Regulatory gate enforcement (SOC2, HIPAA, FedRAMP requirements)
   - Signed commits and artifact signing with Cosign/Sigstore

2. **Advanced orchestration** (4000 tokens):
   - Cross-pipeline dependencies and triggers
   - Dynamic pipeline generation based on repository changes
   - Custom plugin/action development for specialized tasks
   - Pipeline-as-code templating and reusability patterns
   - Multi-repository coordination (monorepo strategies)

3. **Performance and reliability optimization** (4000 tokens):
   - Pipeline performance profiling and bottleneck analysis
   - Retry logic and failure recovery strategies
   - Resource optimization (runner sizing, autoscaling)
   - Pipeline observability (metrics, logs, traces)
   - Chaos engineering for pipeline resilience testing

**Additional sources** (accessed 2025-10-26T01:33:56-04:00):

- **SLSA Framework**: https://slsa.dev/spec/v1.0/
- **Sigstore**: https://www.sigstore.dev/
- **OWASP CI/CD Security**: https://owasp.org/www-project-top-10-ci-cd-security-risks/

---

## Decision Rules

**Platform selection guidance:**

- **GitHub Actions**: GitHub-hosted projects, generous free tier, extensive marketplace
- **GitLab CI**: GitLab projects, integrated security scanning, robust Kubernetes support
- **Jenkins**: On-premise requirements, maximum flexibility, legacy system integration
- **Azure DevOps**: Microsoft ecosystem, enterprise compliance features

**Stage configuration:**

- **Build**: Always include dependency locking and caching
- **Test**: Fail fast on test failures; generate coverage reports
- **Security**: Block on critical vulnerabilities; allow warnings
- **Deploy**: Require manual approval for production

**Escalation conditions:**

- Custom compliance requirements not covered by standard tools
- Novel platform or unsupported tech stack combination
- Requirements exceed T3 scope (multi-cloud orchestration, custom tooling development)

**Abort conditions:**

- Platform limitations prevent required security controls
- Missing critical information and stakeholder unavailable
- Conflicting requirements (e.g., "zero approval gates" with "manual production approval")

---

## Output Contract

**Required outputs:**

```json
{
  "pipeline_config": {
    "type": "object",
    "properties": {
      "platform": "string (github-actions|gitlab-ci|jenkins|azure-devops)",
      "file_path": "string (.github/workflows/ci.yml, .gitlab-ci.yml, Jenkinsfile)",
      "content": "string (complete pipeline configuration)",
      "language": "string (yaml|groovy)"
    }
  },
  "setup_guide": {
    "type": "markdown",
    "properties": {
      "secrets_required": ["array of secret names and descriptions"],
      "variables_required": ["array of variable names and defaults"],
      "setup_steps": "string (step-by-step setup instructions)"
    }
  }
}
```

**Quality guarantees:**

- Pipeline configuration is syntactically valid for target platform
- All secrets referenced but never hardcoded
- Required stages (build, test) are present and properly configured
- Caching is enabled for dependencies to improve performance
- Error handling and failure notifications configured

---

## Examples

**Example: GitHub Actions pipeline for Node.js application**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
```

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens (basic single-environment pipeline)
- **T2**: ≤6k tokens (multi-environment with advanced security)
- **T3**: ≤12k tokens (enterprise compliance and orchestration)

**Safety checks:**

- No hardcoded secrets in generated configurations
- All external actions/dependencies pinned to specific versions
- Security scanning stages fail on critical vulnerabilities
- Minimum test coverage threshold enforced

**Auditability:**

- All pipeline runs logged with timestamps and triggering actor
- Approval gates record approver identity
- Generated configurations include inline documentation

**Determinism:**

- Same inputs produce identical pipeline configuration
- Dependency versions locked (package-lock.json, requirements.txt)
- Build environments use versioned base images

---

## Resources

**Official Documentation** (accessed 2025-10-26T01:33:56-04:00):

- GitHub Actions: https://docs.github.com/en/actions
- GitLab CI/CD: https://docs.gitlab.com/ee/ci/
- Jenkins Documentation: https://www.jenkins.io/doc/
- Azure DevOps Pipelines: https://learn.microsoft.com/en-us/azure/devops/pipelines/

**Best Practices** (accessed 2025-10-26T01:33:56-04:00):

- DORA Metrics: https://dora.dev/research/
- CI/CD Security: https://owasp.org/www-project-top-10-ci-cd-security-risks/
- Software Supply Chain: https://slsa.dev/

**Templates** (in repository `/resources/`):

- GitHub Actions templates for Python, Node.js, Go, Java
- GitLab CI templates with security scanning
- Jenkins declarative pipeline examples
