---
name: "Serverless Deployment Designer"
slug: "serverless-deployment-designer"
description: "Design serverless function deployments for AWS Lambda, Azure Functions, and Google Cloud Functions with event sources, IAM, and cold start optimization."
capabilities:
  - AWS Lambda, Azure Functions, Google Cloud Functions configuration
  - Event source mapping (API Gateway, S3, EventBridge, Queue triggers)
  - IAM role and permission configuration with least privilege
  - Cold start optimization strategies
  - Serverless framework and SAM template generation
  - VPC integration for private resource access
  - Concurrency and throttling configuration
inputs:
  - cloud_provider: "aws, azure, gcp (string)"
  - runtime: "nodejs, python, go, java, dotnet (string)"
  - trigger_type: "http, s3, queue, schedule, stream (string)"
  - memory_mb: "allocated memory in MB (integer, default: 512)"
  - timeout_seconds: "function timeout (integer, default: 30)"
  - vpc_required: "requires VPC access (boolean, default: false)"
  - reserved_concurrency: "concurrent executions limit (integer, optional)"
outputs:
  - function_config: "platform-specific function configuration"
  - iam_policy: "least-privilege IAM policy or managed identity"
  - event_source_config: "trigger and event source configuration"
  - deployment_template: "SAM, Serverless Framework, or Terraform config"
  - optimization_recommendations: "cold start and cost optimization tips"
keywords:
  - serverless
  - lambda
  - azure-functions
  - cloud-functions
  - event-driven
  - iam
  - sam
  - serverless-framework
  - cold-start-optimization
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
  - https://learn.microsoft.com/en-us/azure/azure-functions/
  - https://cloud.google.com/functions/docs
  - https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
---

## Purpose & When-To-Use

**Trigger conditions:**
- Designing event-driven serverless architecture
- Converting application logic to serverless functions
- Configuring event sources and triggers for functions
- Implementing least-privilege IAM for serverless workloads
- Optimizing serverless cold start performance
- Deploying HTTP APIs with API Gateway + Lambda

**Not for:**
- Long-running processes >15 minutes (use containers instead)
- Stateful applications requiring persistent connections
- Complete orchestration across multiple deployment types (use cloud-native-orchestrator agent)
- Container-based serverless (Fargate, Cloud Run) - use kubernetes-manifest-generator

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `cloud_provider` must be: aws, azure, or gcp
- `runtime` must be supported by cloud provider (check version compatibility)
- `trigger_type` must be: http, s3, queue, schedule, stream, or custom
- `memory_mb` must be within provider limits (AWS: 128-10240, Azure: 128-4096)
- `timeout_seconds` must be ≤900 (15 minutes max across all providers)

**Source freshness:**
- AWS Lambda Best Practices (accessed 2025-10-26T01:33:54-04:00): https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
- Azure Functions Best Practices (accessed 2025-10-26T01:33:54-04:00): https://learn.microsoft.com/en-us/azure/azure-functions/functions-best-practices
- Google Cloud Functions Best Practices (accessed 2025-10-26T01:33:54-04:00): https://cloud.google.com/functions/docs/bestpractices

**Decision thresholds:**
- T1 for basic function configuration with single event source
- T2 for production deployment with IAM, VPC, and optimization

---

## Procedure

### T1: Basic Function Configuration (≤2k tokens)

**Step 1: Generate function configuration**
- Create platform-specific function definition (AWS Lambda config, Azure function.json)
- Configure runtime, memory, and timeout
- Add basic environment variables placeholder
- Define handler entry point

**Step 2: Configure event source**
- Map trigger type to platform-specific event source
- HTTP → API Gateway (AWS), HTTP Trigger (Azure), HTTP Functions (GCP)
- Queue → SQS/SNS (AWS), Queue Trigger (Azure), Pub/Sub (GCP)
- Schedule → EventBridge (AWS), Timer Trigger (Azure), Cloud Scheduler (GCP)

**Output:**
- Basic function configuration
- Event source mapping
- Deployment command

**Abort conditions:**
- Runtime not supported by selected cloud provider
- Trigger type incompatible with cloud provider

---

### T2: Production-Ready Deployment (≤6k tokens)

**All T1 steps plus:**

**Step 1: IAM and security configuration**
- Generate least-privilege IAM policy/managed identity
- Add permissions for event sources (S3 read, SQS poll, etc.)
- Configure VPC access if required (security groups, subnets)
- Add encryption for environment variables
- Enable dead letter queue for failure handling

**Step 2: Cold start optimization**
- Minimize package size (exclude dev dependencies)
- Configure provisioned concurrency if needed
- Use appropriate runtime version (latest ARM64 for AWS)
- Implement connection pooling for database clients
- Add lambda layers for shared dependencies (AWS)

**Step 3: Deployment template generation**
- Create SAM template (AWS) or Serverless Framework config
- Add API Gateway resource with throttling and caching
- Configure CORS and authorization
- Add CloudWatch Logs retention policy
- Include X-Ray tracing configuration

**Step 4: Cost and performance optimization**
- Calculate cost estimate based on invocations and memory
- Recommend memory sizing based on workload type
- Configure concurrency limits to prevent runaway costs
- Add CloudWatch alarms for error rate and throttling

**Output:**
- Complete SAM/Serverless Framework template
- IAM policy with least-privilege permissions
- VPC configuration (if applicable)
- Cost estimate with optimization recommendations
- Deployment and testing commands

**Abort conditions:**
- VPC requirements conflict with cold start performance needs
- Timeout requirements exceed platform limits
- Concurrency requirements exceed account limits

---

### T3: Advanced Serverless Architecture (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Multi-function orchestration**
- Design Step Functions (AWS) or Durable Functions (Azure) workflow
- Add retry policies and error handling
- Configure function chaining and parallel execution

**Step 2: Advanced monitoring**
- Structured logging with correlation IDs
- Custom CloudWatch metrics
- Distributed tracing with X-Ray/Application Insights
- Cost anomaly detection alerts

**Step 3: CI/CD integration**
- GitHub Actions or GitLab CI pipeline for deployment
- Blue/green deployment strategy
- Automated integration tests
- Canary deployment with traffic shifting

**Output:**
- Multi-function orchestration workflow
- Complete CI/CD pipeline
- Observability stack configuration
- Disaster recovery and rollback procedures

---

## Decision Rules

**Cloud provider-specific features:**
- **AWS Lambda**: Best ARM64 support, extensive event sources, Step Functions orchestration
- **Azure Functions**: .NET integration, Durable Functions for stateful workflows, Premium plan for VNet
- **Google Cloud Functions**: Integrated with Pub/Sub, Cloud Run for containerized, Eventarc for event routing

**Memory sizing:**
- **Small functions** (simple transforms): 128-512 MB
- **Medium functions** (API handlers): 512-1024 MB
- **Large functions** (data processing): 1024-3008 MB
- **Memory-intensive** (ML inference): 3008-10240 MB

**Runtime selection:**
- **Node.js**: Fast cold starts, good for I/O-bound tasks
- **Python**: ML/data processing libraries, moderate cold starts
- **Go**: Fastest cold starts, compiled binary, low memory footprint
- **Java**: Enterprise libraries, slower cold starts (use SnapStart on AWS)
- **.NET**: C# integration, moderate cold starts, Azure-optimized

**Concurrency strategy:**
- **On-demand**: Variable traffic, cost-sensitive
- **Provisioned**: Latency-sensitive, predictable traffic, cold start elimination
- **Reserved**: High throughput, cost predictable, guaranteed capacity

**Ambiguity handling:**
- If trigger_type unclear → request application event flow diagram
- If memory_mb not specified → start with 512 MB and recommend load testing
- If vpc_required unclear → ask about private resource dependencies

---

## Output Contract

**Required fields (all tiers):**
```yaml
function_config:
  name: "function-name"
  runtime: "nodejs18.x | python3.11 | go1.x | etc"
  handler: "index.handler"
  memory_mb: integer
  timeout_seconds: integer
  environment_variables:
    - key: value (placeholders)

event_source:
  type: "http | s3 | queue | schedule"
  configuration: "platform-specific event source config"

deployment_command: "aws deploy | func deploy | gcloud deploy"
```

**Additional T2 fields:**
```yaml
iam_policy:
  platform: "aws-iam | azure-managed-identity | gcp-service-account"
  permissions: ["array of least-privilege permissions"]
  policy_document: "JSON or YAML policy"

vpc_config:
  enabled: boolean
  security_group_ids: ["sg-xxx"]
  subnet_ids: ["subnet-xxx"]

cold_start_optimization:
  package_size_mb: float
  provisioned_concurrency: integer
  optimization_techniques: ["array of applied optimizations"]

cost_estimate:
  monthly_invocations: integer
  estimated_cost_usd: float
  cost_per_million_requests: float
```

**Additional T3 fields:**
```yaml
orchestration:
  workflow_type: "step-functions | durable-functions | workflows"
  workflow_definition: "ASL or workflow config"

ci_cd_pipeline:
  platform: "github-actions | gitlab-ci"
  pipeline_config: "YAML workflow definition"
  deployment_strategy: "blue-green | canary | rolling"

observability:
  logging: "structured logging configuration"
  metrics: "custom metrics definitions"
  tracing: "x-ray | application-insights config"
  alerts: ["array of CloudWatch/Azure Monitor alerts"]
```

---

## Examples

```yaml
# T1 Example: AWS Lambda with API Gateway (SAM)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs18.x
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          NODE_ENV: production
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /api
            Method: GET
```

```python
# T2 Example: IAM Policy (AWS Lambda)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic function and event source configuration
- **T2**: ≤6,000 tokens - production IAM, VPC, optimization, deployment template
- **T3**: ≤12,000 tokens - orchestration, CI/CD, advanced observability

**Safety checks:**
- No hardcoded secrets in function code or environment variables
- IAM policies follow least-privilege principle
- Dead letter queues configured for async invocations (T2+)
- Timeout set appropriately to prevent runaway executions
- Concurrency limits prevent cost overruns

**Auditability:**
- Runtime versions explicitly specified (not :latest)
- IAM permissions documented with justification
- Event source configurations cite official documentation
- Cost estimates include methodology and assumptions

**Determinism:**
- Same inputs produce identical configuration
- Memory and timeout settings based on documented guidelines
- IAM policies generated from standard templates

**Validation requirements:**
- Function config validates against platform schema (SAM validate, etc.)
- IAM policies pass IAM policy validator
- T2+ configs include cost estimate with breakdown

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- AWS Lambda Developer Guide: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
- AWS Lambda Best Practices: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
- AWS SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/
- Azure Functions Documentation: https://learn.microsoft.com/en-us/azure/azure-functions/
- Google Cloud Functions Documentation: https://cloud.google.com/functions/docs
- Serverless Framework: https://www.serverless.com/framework/docs

**Cold Start Optimization:**
- AWS Lambda Cold Starts: https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/
- Azure Functions Performance: https://learn.microsoft.com/en-us/azure/azure-functions/performance-reliability
- Lambda SnapStart: https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html

**IAM and Security:**
- AWS Lambda Security Best Practices: https://docs.aws.amazon.com/lambda/latest/dg/lambda-security.html
- Azure Functions Security: https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts
- Least Privilege IAM: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

**Cost Optimization:**
- AWS Lambda Pricing: https://aws.amazon.com/lambda/pricing/
- AWS Lambda Power Tuning: https://github.com/alexcasalboni/aws-lambda-power-tuning
