---
name: "Helm Chart Builder"
slug: "kubernetes-helm-builder"
description: "Build production-grade Helm charts with templating, values.yaml parameterization, dependencies, and hooks for multi-environment Kubernetes deployments."
capabilities:
  - Helm chart structure generation with Chart.yaml
  - Template parameterization with values.yaml
  - Chart dependencies management
  - Pre-install, post-install, and upgrade hooks
  - Multi-environment values overlays (dev, staging, prod)
  - Helm chart validation and linting
inputs:
  - chart_name: "name of the Helm chart (string)"
  - app_version: "application version (string)"
  - chart_version: "chart version (string, default: 0.1.0)"
  - resources: "array of Kubernetes resource types to include (array)"
  - environments: "array of target environments (array, optional)"
  - dependencies: "array of chart dependencies (array, optional)"
outputs:
  - chart_structure: "complete Helm chart directory structure"
  - templates: "parameterized Kubernetes manifest templates"
  - values_files: "values.yaml and environment-specific overrides"
  - validation_results: "helm lint and template validation output"
keywords:
  - helm
  - helm-chart
  - kubernetes
  - templating
  - values-yaml
  - chart-dependencies
  - helm-hooks
  - multi-environment
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://helm.sh/docs/
  - https://helm.sh/docs/chart_best_practices/
  - https://helm.sh/docs/topics/charts/
  - https://helm.sh/docs/chart_template_guide/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Deploying applications to multiple Kubernetes environments (dev, staging, prod)
- Packaging Kubernetes manifests for reusability and distribution
- Managing complex applications with dependencies (databases, message queues)
- Implementing GitOps workflows with parameterized deployments
- Version-controlling Kubernetes configurations with semantic versioning

**Not for:**
- Simple single-environment deployments (use kubernetes-manifest-generator)
- Serverless deployments (use cloud-serverless-designer)
- Service mesh configuration (use kubernetes-servicemesh-configurator)
- Complete orchestration across deployment types (use cloud-native-orchestrator agent)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `chart_name` must be DNS-1123 compliant (lowercase, alphanumeric, hyphens)
- `app_version` must follow semantic versioning (e.g., 1.0.0)
- `chart_version` must follow semantic versioning
- `resources` array must contain valid K8s resource types (Deployment, Service, etc.)

**Source freshness:**
- Helm Documentation (accessed 2025-10-26T01:33:54-04:00): https://helm.sh/docs/
- Helm Best Practices (accessed 2025-10-26T01:33:54-04:00): https://helm.sh/docs/chart_best_practices/
- Helm Chart Template Guide (accessed 2025-10-26T01:33:54-04:00): https://helm.sh/docs/chart_template_guide/

**Decision thresholds:**
- T1 for basic chart structure with single environment
- T2 for multi-environment charts with dependencies and hooks

---

## Procedure

### T1: Basic Helm Chart Structure (≤2k tokens)

**Step 1: Create chart directory structure**
- Generate Chart.yaml with metadata (name, version, appVersion, description)
- Create values.yaml with default configuration parameters
- Build templates/ directory with basic resource templates
- Add NOTES.txt for post-install instructions

**Step 2: Parameterize templates**
- Convert static manifests to Helm templates with {{ .Values.* }}
- Add image repository, tag, and pull policy parameters
- Parameterize replica count, resource limits, service ports
- Include conditional blocks for optional resources

**Output:**
- Basic Helm chart structure
- Parameterized templates for core resources
- values.yaml with sensible defaults
- helm install command

**Abort conditions:**
- chart_name conflicts with existing chart
- Invalid Kubernetes resource types in resources array

---

### T2: Production-Grade Helm Chart (≤6k tokens)

**All T1 steps plus:**

**Step 1: Multi-environment configuration**
- Create values-dev.yaml, values-staging.yaml, values-prod.yaml
- Environment-specific overrides (replicas, resources, ingress)
- Secret management strategy (external-secrets, sealed-secrets)
- ConfigMap templating for environment config

**Step 2: Chart dependencies**
- Define dependencies in Chart.yaml (PostgreSQL, Redis, etc.)
- Configure dependency conditions (enable/disable based on values)
- Add subchart value overrides
- Generate Chart.lock with dependency versions

**Step 3: Helm hooks**
- Pre-install hook for database migration jobs
- Post-install hook for validation or smoke tests
- Pre-upgrade hook for backup or compatibility checks
- Add hook deletion policies (before-hook-creation, hook-succeeded)

**Step 4: Advanced templating**
- Named templates (_helpers.tpl) for reusable snippets
- Range loops for multiple similar resources
- Conditional resource creation with {{ if .Values.enabled }}
- Template functions (quote, toYaml, include, etc.)

**Step 5: Validation and linting**
- Run helm lint to check chart structure and templates
- Validate with helm template --debug
- Test installation in dry-run mode
- Generate schema for values.yaml validation

**Output:**
- Complete multi-environment Helm chart
- Chart dependencies with Chart.lock
- Helm hooks for lifecycle management
- Validation and installation instructions
- values.schema.json for values validation

**Abort conditions:**
- Dependency versions incompatible or unavailable
- Template syntax errors in complex conditionals
- Hook jobs fail validation

---

### T3: Enterprise Helm Chart (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Chart testing**
- Create tests/ directory with connection tests
- Add helm test YAML for post-deployment validation
- Include integration test scripts

**Step 2: Documentation**
- Generate comprehensive README.md with parameter tables
- Document all values.yaml parameters with descriptions
- Add upgrade guides and migration notes
- Include troubleshooting section

**Step 3: Chart repository packaging**
- Package chart with helm package
- Generate index.yaml for chart repository
- Sign chart with GPG for provenance

**Output:**
- Enterprise-ready Helm chart with tests
- Complete documentation
- Packaged and signed chart ready for distribution
- Chart repository index

---

## Decision Rules

**Chart structure patterns:**
- **Simple app**: Deployment, Service, ConfigMap, Secret templates only
- **Stateful app**: Add StatefulSet, PersistentVolumeClaim, headless Service
- **Ingress required**: Include Ingress template with TLS configuration
- **Jobs/CronJobs**: Add job templates with completion tracking

**Dependency management:**
- **Include subchart**: Common dependencies (PostgreSQL, Redis) as subcharts
- **External dependency**: Reference external charts in Chart.yaml dependencies
- **Conditional dependency**: Use `condition` or `tags` for optional dependencies

**Hook usage:**
- **Pre-install**: Database schema initialization, secret generation
- **Post-install**: Smoke tests, notification webhooks
- **Pre-upgrade**: Backup jobs, compatibility validation
- **Post-upgrade**: Migration cleanup, cache invalidation

**Values organization:**
- **Global values**: Shared across all environments (image repository, labels)
- **Environment values**: Replicas, resources, domains (in values-{env}.yaml)
- **Secret values**: Not in values files, use external-secrets or Vault

**Ambiguity handling:**
- If environments not specified → create values.yaml only (single environment)
- If dependencies unclear → request application architecture diagram
- If resource types unknown → infer from application type (web app → Deployment + Service)

---

## Output Contract

**Required fields (all tiers):**
```yaml
chart_structure:
  Chart.yaml: "chart metadata"
  values.yaml: "default configuration values"
  templates/:
    - deployment.yaml
    - service.yaml
    - _helpers.tpl
  NOTES.txt: "post-install instructions"

validation_results:
  helm_lint: "output of helm lint"
  template_render: "output of helm template"
  errors: ["array of validation errors if any"]
```

**Additional T2 fields:**
```yaml
multi_environment:
  values_dev.yaml: "development overrides"
  values_staging.yaml: "staging overrides"
  values_prod.yaml: "production overrides"

dependencies:
  Chart.yaml_dependencies: ["array of chart dependencies"]
  Chart.lock: "locked dependency versions"

hooks:
  pre_install: ["array of pre-install hook jobs"]
  post_install: ["array of post-install hook jobs"]
  pre_upgrade: ["array of pre-upgrade hook jobs"]

helpers:
  _helpers.tpl: "named template definitions"

values_schema:
  values.schema.json: "JSON schema for values validation"
```

**Additional T3 fields:**
```yaml
testing:
  tests/: ["array of test YAML files"]
  test_commands: ["helm test chart-name"]

documentation:
  README.md: "comprehensive chart documentation"
  UPGRADING.md: "upgrade and migration guide"

packaging:
  chart_package: "chart-name-version.tgz"
  chart_signature: "chart-name-version.tgz.prov"
  index.yaml: "chart repository index"
```

---

## Examples

```yaml
# T1 Example: Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
maintainers:
- name: Developer
  email: dev@example.com
```

```yaml
# T1 Example: values.yaml
replicaCount: 3

image:
  repository: myregistry/myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
```

```yaml
# T1 Example: templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 8080
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic chart structure with parameterization
- **T2**: ≤6,000 tokens - multi-environment, dependencies, hooks, validation
- **T3**: ≤12,000 tokens - testing, documentation, packaging, signing

**Safety checks:**
- No hardcoded secrets in values.yaml or templates
- Image tags are parameterized (not hardcoded :latest)
- Resource limits defined in values.yaml
- NOTES.txt provides clear installation instructions

**Auditability:**
- Chart.yaml includes maintainer information
- Semantic versioning for chart and app versions
- All template functions cite Helm documentation
- Dependency versions locked in Chart.lock

**Determinism:**
- helm template renders identical output for same values
- Chart dependencies are version-locked
- Named templates produce consistent output

**Validation requirements:**
- Chart must pass `helm lint` without errors
- Templates must render without errors using `helm template`
- T2+ charts must include values.schema.json validation
- T3 charts must pass `helm test` successfully

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- Helm Documentation: https://helm.sh/docs/
- Helm Chart Best Practices: https://helm.sh/docs/chart_best_practices/
- Chart Template Guide: https://helm.sh/docs/chart_template_guide/
- Helm Hooks: https://helm.sh/docs/topics/charts_hooks/
- Chart Dependencies: https://helm.sh/docs/helm/helm_dependency/
- Values Files: https://helm.sh/docs/chart_template_guide/values_files/

**Template Functions:**
- Sprig Functions: http://masterminds.github.io/sprig/
- Template Function List: https://helm.sh/docs/chart_template_guide/function_list/

**Validation and Testing:**
- Helm Lint: https://helm.sh/docs/helm/helm_lint/
- Helm Test: https://helm.sh/docs/helm/helm_test/
- Chart Testing (ct): https://github.com/helm/chart-testing

**Chart Repositories:**
- Artifact Hub: https://artifacthub.io/
- Helm Chart Repository Guide: https://helm.sh/docs/topics/chart_repository/
