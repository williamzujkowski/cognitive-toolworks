---
name: MLOps Lifecycle Manager
slug: mlops-lifecycle-manager
description: Manage ML model lifecycle from development to deployment with experiment tracking, versioning, monitoring, and automated retraining workflows.
capabilities:
  - Experiment tracking setup and configuration
  - Model versioning and registry management
  - Deployment pipeline design (batch/online/edge)
  - Model monitoring and drift detection
  - Automated retraining triggers and workflows
  - Model governance and lineage tracking
  - Feature store integration
  - A/B testing and canary deployments
inputs:
  - model_type: classification, regression, clustering, generative, etc.
  - deployment_target: batch, online, edge, embedded
  - scale_requirements: requests_per_second, latency_sla, data_volume
  - governance_level: experimental, staging, production
  - existing_stack: mlflow, kubeflow, vertex_ai, sagemaker, etc.
outputs:
  - experiment_config: MLflow/W&B tracking configuration
  - model_registry_schema: versioning and metadata structure
  - deployment_manifest: K8s/cloud-specific deployment config
  - monitoring_dashboard: metrics, alerts, drift detection queries
  - retraining_pipeline: automated workflow definition
keywords:
  - mlops
  - machine-learning
  - model-deployment
  - experiment-tracking
  - model-monitoring
  - feature-engineering
  - model-versioning
  - ml-pipeline
version: 1.0.0
owner: cognitive-toolworks
license: CC0-1.0
security: public; no secrets or PII
links:
  - https://mlflow.org/docs/latest/
  - https://www.kubeflow.org/docs/
  - https://ml-ops.org/
  - https://cloud.google.com/vertex-ai/docs
  - https://neptune.ai/blog/mlops
  - https://docs.seldon.io/
---

## Purpose & When-To-Use

**Trigger conditions:**

* Transitioning ML model from notebook/experiment to production deployment
* Model performance degradation detected in production
* Need to establish experiment tracking for ML team collaboration
* Designing automated ML pipeline from training to deployment
* Implementing model governance and compliance requirements
* Setting up model monitoring and observability
* Managing multiple model versions across environments

**Use this skill when:**

* Building end-to-end MLOps infrastructure from scratch
* Migrating ad-hoc ML workflows to production-grade systems
* Implementing MLOps best practices (accessed 2025-10-25T21:30:36-04:00): https://ml-ops.org/content/three-levels-of-ml-software
* Establishing model lifecycle governance for regulated industries
* Optimizing model deployment patterns for scale and latency
* Integrating ML workflows with existing DevOps pipelines

## Pre-Checks

**Time normalization:**
```
NOW_ET = 2025-10-25T21:30:36-04:00
```

**Input validation:**

* `model_type` must match supported categories: classification, regression, clustering, ranking, generative, time-series, recommendation, computer-vision, nlp
* `deployment_target` must be: batch, online, edge, embedded, or hybrid
* `scale_requirements` must include at least one of: rps (requests per second), latency_ms, data_volume_gb, concurrent_users
* `governance_level` must be: experimental, staging, production (determines compliance/audit requirements)
* `existing_stack` is optional; if provided, must be recognized platform: mlflow, kubeflow, vertex_ai, sagemaker, azure_ml, databricks, neptune, wandb, custom

**MLOps maturity check:**

* Level 0: Manual process (no automation) - recommend full T3 implementation
* Level 1: ML pipeline automation - focus on monitoring and governance (T2)
* Level 2: CI/CD for ML pipelines - focus on advanced patterns (T2-T3)
* Reference: Google MLOps Maturity Model (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

**Framework/platform compatibility:**

* Kubernetes available: enables Kubeflow, Seldon, KServe deployments
* Cloud-managed: Vertex AI (GCP), SageMaker (AWS), Azure ML (Azure)
* Hybrid/on-prem: MLflow + model servers (TorchServe, TensorFlow Serving, Triton)

## Procedure

### Tier 1: Quick MLOps Assessment and Recommendations (≤2k tokens)

**Goal:** Provide fast MLOps setup recommendations based on model type and deployment target

**Steps:**

1. **Analyze requirements**
   * Identify primary model type and deployment pattern
   * Assess scale requirements (batch vs. online, latency constraints)
   * Determine existing infrastructure capabilities

2. **Recommend core stack**
   * **Experiment tracking:** MLflow (open-source, cloud-agnostic) or platform-native (Vertex AI Experiments, SageMaker Experiments)
   * **Model registry:** MLflow Model Registry or cloud-managed registry
   * **Deployment:**
     - Batch: Kubernetes CronJobs, Airflow/Prefect orchestration
     - Online: KServe/Seldon (K8s) or cloud endpoints (Vertex AI Prediction, SageMaker Inference)
     - Edge: TensorFlow Lite, ONNX Runtime, TorchScript
   * **Monitoring:** Prometheus + Grafana for metrics, Evidently AI or Alibi Detect for drift

3. **Generate quick-start checklist**
   * Install experiment tracker
   * Configure model registry with versioning schema
   * Setup basic deployment pipeline
   * Enable core metrics collection (latency, throughput, error rate)

4. **Output minimal configuration**
   * MLflow tracking URI and artifact store location
   * Model registry schema (model name, version, stage: staging/production)
   * Deployment command template
   * Basic monitoring dashboard query examples

**Abort conditions:**
* Incompatible infrastructure (e.g., edge deployment requested but no ONNX/TFLite tooling)
* Conflicting requirements (e.g., <50ms latency with large ensemble model on CPU)

### Tier 2: Production MLOps Pipeline Design (≤6k tokens)

**Goal:** Design production-ready MLOps pipeline with monitoring and governance

**Steps:**

1. **Experiment tracking setup**
   * **MLflow configuration** (accessed 2025-10-25T21:30:36-04:00): https://mlflow.org/docs/latest/tracking.html
     - Backend store: PostgreSQL/MySQL for metadata
     - Artifact store: S3/GCS/Azure Blob for models/artifacts
     - Authentication: integrate with LDAP/OAuth
   * **Logging best practices:**
     - Parameters: hyperparameters, data versioning, feature engineering config
     - Metrics: training/validation loss, accuracy, precision, recall, F1, AUC
     - Artifacts: model binaries, confusion matrices, feature importance plots
     - Tags: team, project, experiment_type for filtering

2. **Model versioning and registry**
   * **Versioning schema:**
     - Semantic versioning: major.minor.patch
     - Git commit SHA for code reproducibility
     - Data version hash for training data lineage
   * **Model stages:** None → Staging → Production → Archived
   * **Metadata requirements:**
     - Model type, framework (scikit-learn, TensorFlow, PyTorch, XGBoost)
     - Performance metrics on validation/test sets
     - Hardware requirements (CPU/GPU, memory)
     - Inference latency benchmarks
     - Training data statistics and schema

3. **Deployment pipeline design**
   * **Online serving** (accessed 2025-10-25T21:30:36-04:00): https://www.kubeflow.org/docs/components/kserve/
     - KServe InferenceService for autoscaling and canary deployments
     - Model server selection: TorchServe (PyTorch), TensorFlow Serving, Triton (multi-framework)
     - API design: REST or gRPC with request/response schemas
     - Traffic splitting: 90/10 for canary, 50/50 for A/B testing
   * **Batch inference:**
     - Kubernetes Jobs or cloud batch services
     - Input data partitioning for parallelism
     - Output schema validation and storage
   * **Feature store integration:**
     - Feast (open-source) or cloud-native (Vertex AI Feature Store, SageMaker Feature Store)
     - Online features: low-latency key-value store (Redis, DynamoDB)
     - Offline features: data warehouse (BigQuery, Snowflake) for training

4. **Model monitoring configuration**
   * **Performance monitoring:**
     - Latency: p50, p95, p99 percentiles
     - Throughput: requests per second
     - Error rates: 4xx, 5xx responses, prediction failures
   * **Data drift detection** (accessed 2025-10-25T21:30:36-04:00): https://docs.evidentlyai.com/
     - Statistical tests: Kolmogorov-Smirnov, Population Stability Index (PSI)
     - Feature distribution monitoring
     - Alert thresholds: PSI > 0.2 triggers investigation
   * **Model drift (concept drift):**
     - Prediction distribution shifts
     - Accuracy degradation on labeled subset
     - Business metric impact (conversion rate, revenue)

5. **Generate production artifacts**
   * MLflow project configuration (MLproject file)
   * Kubernetes deployment manifests (Deployment, Service, HPA)
   * Monitoring dashboard (Grafana JSON)
   * CI/CD pipeline config (GitHub Actions, GitLab CI, Jenkins)

**Decision rules:**
* If latency SLA < 100ms → use model compression (quantization, pruning) or edge deployment
* If scale > 1000 rps → enable autoscaling (HPA) with GPU node pools
* If governance_level = production → require model approval workflow and audit logging

### Tier 3: Comprehensive MLOps Lifecycle with Governance (≤12k tokens)

**Goal:** Full MLOps implementation with automated retraining, governance, and advanced patterns

**Steps:**

1. **Advanced experiment tracking**
   * **Hyperparameter optimization integration:**
     - Optuna, Ray Tune, Katib (Kubeflow) integration
     - Parallel trial execution and early stopping
     - Best model auto-promotion to registry
   * **Distributed training:**
     - Horovod, PyTorch DDP, TensorFlow MultiWorkerMirroredStrategy
     - Training cluster setup (K8s with GPU node pools)
     - Checkpoint management and fault tolerance

2. **Model governance and lineage**
   * **Model cards** (accessed 2025-10-25T21:30:36-04:00): https://modelcards.withgoogle.com/about
     - Model details: architecture, training data, intended use
     - Performance metrics: accuracy by demographic subgroup
     - Ethical considerations: fairness, bias mitigation
     - Limitations and recommendations
   * **Data lineage tracking:**
     - DAG visualization: raw data → features → model
     - Versioned datasets with checksums
     - Feature engineering pipeline capture
   * **Compliance and audit:**
     - Model approval workflows (JIRA, ServiceNow integration)
     - Access control: RBAC for model deployment
     - Audit logs: who deployed which model when

3. **Automated retraining pipelines**
   * **Trigger conditions:**
     - Scheduled: weekly, monthly based on data volume
     - Performance-based: accuracy drops below threshold
     - Data drift: PSI > 0.25 or KS test p-value < 0.05
     - Business rules: quarterly regulatory updates
   * **Retraining workflow** (accessed 2025-10-25T21:30:36-04:00): https://www.kubeflow.org/docs/components/pipelines/
     - Data validation: schema checks, outlier detection (TensorFlow Data Validation)
     - Feature engineering: reproducible transformations
     - Training: distributed with experiment tracking
     - Evaluation: challenger vs. champion comparison
     - Conditional deployment: only if challenger outperforms by X%
   * **Kubeflow Pipelines or Vertex AI Pipelines:**
     - DAG definition with components (data prep, train, eval, deploy)
     - Pipeline versioning and parameterization
     - Artifact caching for efficiency

4. **Advanced deployment patterns**
   * **Multi-model serving:**
     - Model ensemble aggregation (voting, stacking)
     - Conditional routing: use simple model for 80% cases, complex for 20%
     - Resource optimization: shared GPU for multiple models
   * **Shadow deployment:**
     - Route traffic to both old and new models
     - Compare predictions without affecting users
     - Gather real-world performance data before cutover
   * **Progressive rollout:**
     - Canary: 5% → 25% → 50% → 100%
     - Automated rollback on SLO violation
     - Feature flags for A/B testing (LaunchDarkly, Unleash)

5. **Observability and incident response**
   * **Distributed tracing:**
     - OpenTelemetry integration for request tracing
     - Trace prediction path: API → feature fetch → inference → response
     - Latency breakdown by component
   * **Alerting strategy:**
     - P0: Model serving down (Opsgenie/PagerDuty)
     - P1: SLO violation (latency, error rate)
     - P2: Data drift detected (Slack notification)
     - P3: Retraining pipeline failure
   * **Incident runbooks:**
     - Model rollback procedure
     - Cache warming after deployment
     - Debugging prediction anomalies

6. **Cost optimization**
   * **Compute optimization:**
     - Autoscaling based on traffic patterns
     - Spot/preemptible instances for training
     - CPU vs. GPU cost-benefit analysis
   * **Model optimization:**
     - Quantization: FP32 → FP16 or INT8 (TensorRT, ONNX Runtime)
     - Pruning: remove low-importance weights
     - Knowledge distillation: train smaller student model
   * **Storage optimization:**
     - Artifact lifecycle policies: archive old model versions
     - Compression for model binaries

7. **Generate comprehensive deliverables**
   * Complete MLflow project with reproducible runs
   * Kubeflow Pipeline YAML or Python DSL
   * Model monitoring dashboard (Grafana + custom panels)
   * Retraining automation scripts
   * Model governance documentation (model cards, lineage diagrams)
   * Runbooks for common incidents
   * Cost analysis and optimization report

**Research sources for T3:**
* MLOps principles (accessed 2025-10-25T21:30:36-04:00): https://ml-ops.org/content/mlops-principles
* Model monitoring patterns (accessed 2025-10-25T21:30:36-04:00): https://christophergs.com/machine%20learning/2020/03/14/how-to-monitor-machine-learning-models/
* Feature stores (accessed 2025-10-25T21:30:36-04:00): https://www.featurestore.org/
* Model deployment strategies (accessed 2025-10-25T21:30:36-04:00): https://docs.seldon.io/projects/seldon-core/en/latest/analytics/routers.html

## Decision Rules

**Stack selection:**
* If existing_stack specified → integrate with existing tools rather than replace
* If cloud-native → prefer managed services (Vertex AI, SageMaker) for faster setup
* If on-prem/hybrid → prefer open-source (MLflow, Kubeflow) for portability
* If team < 5 → start with MLflow + simple deployment (T1-T2); avoid Kubeflow complexity
* If regulated industry → enforce model governance and audit logging (T3)

**Deployment pattern selection:**
* If latency_sla < 50ms → edge deployment or model optimization required
* If 50ms ≤ latency_sla < 500ms → online serving with optimized model servers
* If latency_sla ≥ 500ms OR batch → batch inference acceptable
* If rps > 1000 → enable autoscaling and consider model caching
* If model_size > 1GB → use model compression or multi-stage loading

**Monitoring thresholds:**
* Data drift (PSI): 0.1-0.2 = monitor, >0.2 = investigate, >0.25 = trigger retraining
* Model accuracy degradation: >5% drop = investigate, >10% = immediate retraining
* Latency SLO: p95 < target_latency; alert if p95 > 1.5x target for 10+ minutes
* Error rate: >1% = alert, >5% = page on-call engineer

**Abort conditions:**
* Incompatible model format for target deployment (e.g., Keras model to TorchServe)
* Insufficient infrastructure for scale requirements
* Conflicting governance requirements (e.g., model explainability mandate without supported framework)

## Output Contract

**Experiment tracking configuration:**
```json
{
  "tracking_uri": "http://mlflow-server:5000",
  "artifact_location": "s3://mlops-artifacts/experiments",
  "backend_store": "postgresql://mlflow:***@db:5432/mlflow",
  "default_artifact_root": "s3://mlops-artifacts",
  "auth_enabled": true
}
```

**Model registry schema:**
```json
{
  "model_name": "fraud-detection-v2",
  "version": "2.1.0",
  "stage": "Production",
  "framework": "XGBoost 1.7.0",
  "metrics": {
    "auc": 0.943,
    "precision": 0.89,
    "recall": 0.87,
    "f1": 0.88
  },
  "metadata": {
    "training_data_version": "2024-10-01",
    "git_commit": "a3f4d9e",
    "trained_at": "2025-10-20T14:32:18Z",
    "trained_by": "data-scientist@example.com"
  },
  "requirements": {
    "cpu_cores": 2,
    "memory_gb": 4,
    "gpu_required": false
  },
  "signature": {
    "inputs": "[{\"name\": \"transaction_amount\", \"type\": \"double\"}, ...]",
    "outputs": "[{\"name\": \"fraud_probability\", \"type\": \"double\"}]"
  }
}
```

**Deployment manifest (KServe example):**
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: fraud-detection
spec:
  predictor:
    model:
      modelFormat:
        name: xgboost
      storageUri: s3://mlops-models/fraud-detection/v2.1.0
      resources:
        limits:
          cpu: "2"
          memory: 4Gi
        requests:
          cpu: "1"
          memory: 2Gi
    minReplicas: 2
    maxReplicas: 10
    scaleTarget: 80
    scaleMetric: concurrency
  canaryTrafficPercent: 10
```

**Monitoring dashboard config:**
```json
{
  "metrics": [
    {
      "name": "prediction_latency_ms",
      "type": "histogram",
      "aggregations": ["p50", "p95", "p99"],
      "alert_threshold": {"p95": 200}
    },
    {
      "name": "predictions_per_second",
      "type": "counter",
      "aggregations": ["rate"]
    },
    {
      "name": "prediction_error_rate",
      "type": "counter",
      "alert_threshold": {"rate": 0.01}
    },
    {
      "name": "feature_drift_psi",
      "type": "gauge",
      "alert_threshold": {"value": 0.2}
    }
  ],
  "dashboards": [
    "grafana_dashboard_url"
  ]
}
```

**Retraining pipeline definition:**
```yaml
pipeline_name: fraud-detection-retraining
schedule: "0 2 * * 0"  # Weekly on Sunday 2 AM
triggers:
  - type: performance
    metric: f1_score
    threshold: 0.85
    operator: less_than
  - type: drift
    metric: psi
    threshold: 0.25
    operator: greater_than
steps:
  - name: data-validation
    component: tfx.DataValidator
    config:
      schema_path: s3://schemas/fraud-detection.json
  - name: feature-engineering
    component: custom.FeatureTransformer
    dependencies: [data-validation]
  - name: model-training
    component: xgboost.Trainer
    dependencies: [feature-engineering]
    hyperparameters:
      max_depth: 6
      learning_rate: 0.1
      n_estimators: 100
  - name: model-evaluation
    component: custom.Evaluator
    dependencies: [model-training]
    approval_required: true
  - name: model-deployment
    component: kserve.Deployer
    dependencies: [model-evaluation]
    conditional: "evaluation.f1_score > 0.88"
```

## Examples

```python
# Example: Setup MLOps pipeline for fraud detection model
from mlops_lifecycle_manager import MLOpsManager

mgr = MLOpsManager(
    model_type="classification", deployment_target="online",
    scale_requirements={"rps": 500, "latency_ms": 150},
    governance_level="production"
)

# T1: Quick setup - basic stack recommendations
config = mgr.quick_setup(tracking="mlflow", deployment="kserve")
print(config.get_start_commands())

# T2: Production pipeline with monitoring
pipeline = mgr.design_pipeline(
    experiment_tracking=True, model_monitoring=True,
    drift_detection="evidently"
)
pipeline.generate_manifests(output_dir="./mlops-config")

# T3: Full lifecycle with automated retraining
lifecycle = mgr.full_lifecycle(
    retraining_triggers=["drift", "performance"],
    governance={"model_cards": True, "audit_logs": True}
)
lifecycle.deploy(dry_run=False)
```

## Quality Gates

**Token budgets:**
* T1 (quick assessment): ≤2000 tokens - basic stack recommendations only
* T2 (production pipeline): ≤6000 tokens - monitoring and deployment included
* T3 (full lifecycle): ≤12000 tokens - governance, retraining, advanced patterns

**Validation checks:**
* All recommendations must cite authoritative sources with access dates
* Generated configs must be valid YAML/JSON (validate before output)
* Monitoring thresholds must be specific and actionable
* No hardcoded credentials or secrets in any outputs
* Model registry schema must include versioning and metadata

**Safety requirements:**
* Never recommend storing secrets in code or configs (use secret managers)
* Always include rollback procedures in deployment plans
* Require approval workflows for production deployments
* Implement gradual rollouts (canary/blue-green) for production models
* Include data privacy checks for regulated industries (GDPR, HIPAA)

**Auditability:**
* All model deployments must be traceable to training runs
* Model cards required for production governance_level
* Change logs for model versions
* Access control and RBAC for model registry

**Determinism:**
* Reproducible training: fix random seeds, log dependency versions
* Model signatures must define input/output schemas
* Feature engineering must be versioned and reversible

## Resources

**MLOps frameworks and platforms:**
* MLflow documentation (accessed 2025-10-25T21:30:36-04:00): https://mlflow.org/docs/latest/
* Kubeflow documentation (accessed 2025-10-25T21:30:36-04:00): https://www.kubeflow.org/docs/
* ML-Ops.org principles (accessed 2025-10-25T21:30:36-04:00): https://ml-ops.org/
* Google Cloud Vertex AI (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/vertex-ai/docs
* AWS SageMaker MLOps (accessed 2025-10-25T21:30:36-04:00): https://docs.aws.amazon.com/sagemaker/latest/dg/mlops.html
* Neptune.ai MLOps guide (accessed 2025-10-25T21:30:36-04:00): https://neptune.ai/blog/mlops

**Model serving and deployment:**
* KServe documentation (accessed 2025-10-25T21:30:36-04:00): https://kserve.github.io/website/
* Seldon Core patterns (accessed 2025-10-25T21:30:36-04:00): https://docs.seldon.io/
* TorchServe (accessed 2025-10-25T21:30:36-04:00): https://pytorch.org/serve/
* TensorFlow Serving (accessed 2025-10-25T21:30:36-04:00): https://www.tensorflow.org/tfx/guide/serving

**Monitoring and observability:**
* Evidently AI drift detection (accessed 2025-10-25T21:30:36-04:00): https://docs.evidentlyai.com/
* Model monitoring guide (accessed 2025-10-25T21:30:36-04:00): https://christophergs.com/machine%20learning/2020/03/14/how-to-monitor-machine-learning-models/
* Prometheus for ML metrics (accessed 2025-10-25T21:30:36-04:00): https://prometheus.io/docs/introduction/overview/

**Governance and best practices:**
* Model cards (accessed 2025-10-25T21:30:36-04:00): https://modelcards.withgoogle.com/about
* Google MLOps maturity model (accessed 2025-10-25T21:30:36-04:00): https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
* Feature store concepts (accessed 2025-10-25T21:30:36-04:00): https://www.featurestore.org/

**Additional resources in /skills/mlops-lifecycle-manager/resources/:**
* mlflow-tracking-config.yaml - Complete MLflow server configuration
* kserve-inference-service.yaml - Production-ready KServe manifest template
* model-card-template.md - Standardized model documentation template
* monitoring-dashboard.json - Grafana dashboard for ML models
* retraining-pipeline.py - Kubeflow Pipeline example with automated triggers
