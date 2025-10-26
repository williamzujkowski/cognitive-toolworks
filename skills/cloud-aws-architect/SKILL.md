---
name: "AWS Multi-Service Architect"
slug: "cloud-aws-architect"
description: "Design AWS solutions across compute, storage, networking, and serverless with cost optimization, security hardening, and Well-Architected Framework alignment."
capabilities:
  - AWS compute service selection (EC2, ECS, EKS, Lambda, Fargate, Batch)
  - Storage architecture design (S3, EBS, EFS, FSx, Glacier, Storage Gateway)
  - Network topology design (VPC, subnets, routing, NAT, VPN, Direct Connect, Transit Gateway)
  - Serverless architecture patterns (Lambda, API Gateway, EventBridge, Step Functions, SQS/SNS)
  - CloudFormation and CDK infrastructure-as-code generation
  - Cost optimization with TCO analysis and reserved capacity recommendations
  - Well-Architected Framework assessment (operational excellence, security, reliability, performance, cost)
  - Multi-region and disaster recovery architecture
  - IAM policy design with least-privilege principles
  - Service integration and data flow design
inputs:
  - requirements: "functional and non-functional requirements (object with performance, security, cost, compliance)"
  - workload_type: "web-app, data-processing, real-time, batch, machine-learning, hybrid (string)"
  - current_architecture: "description of existing AWS infrastructure if migration (string, optional)"
  - deployment_tier: "T1 (quick recommendation) | T2 (detailed design with IaC) (string, default: T1)"
  - regions: "primary and DR regions (array, default: single region)"
  - budget_constraints: "monthly budget or cost sensitivity (string, optional)"
outputs:
  - architecture_design: "AWS service selection with rationale and data flow diagram description"
  - iac_templates: "CloudFormation or CDK code for infrastructure deployment (T2)"
  - cost_estimate: "TCO analysis with monthly/annual projections and optimization recommendations"
  - security_configuration: "IAM policies, security groups, encryption settings, and compliance mappings"
  - well_architected_assessment: "alignment with AWS Well-Architected pillars and recommendations"
  - migration_strategy: "phased migration plan if current_architecture provided (T2)"
keywords:
  - aws
  - cloud-architecture
  - ec2
  - s3
  - lambda
  - vpc
  - cloudformation
  - cdk
  - well-architected
  - serverless
  - compute
  - storage
  - networking
  - cost-optimization
  - multi-region
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://aws.amazon.com/architecture/well-architected/
  - https://docs.aws.amazon.com/
  - https://aws.amazon.com/pricing/
  - https://calculator.aws/
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
  - https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
---

## Purpose & When-To-Use

**Trigger conditions:**
- AWS solution design spanning multiple services (compute + storage + networking)
- Well-Architected Framework assessment or optimization
- Cost optimization review for existing AWS infrastructure
- Multi-region or disaster recovery architecture planning
- Migration from on-premises or other clouds to AWS
- Serverless vs container vs EC2 architecture decision
- AWS service selection for new workload requirements
- CloudFormation or CDK template generation for infrastructure
- Compliance-driven architecture (HIPAA, PCI-DSS, FedRAMP on AWS)

**Not for:**
- Single AWS service deep-dive (use service-specific documentation)
- Application code development (focuses on infrastructure)
- Non-AWS multi-cloud strategy (use cloud-multicloud-advisor skill)
- Kubernetes-specific deployment patterns (use cloud-native-deployment-orchestrator)
- Detailed cost analysis without architecture context (use finops-cost-analyzer)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `requirements` must include at least one of: performance, security, cost, compliance
- `workload_type` must be one of: web-app, data-processing, real-time, batch, machine-learning, hybrid
- `deployment_tier` must be: T1 or T2
- `regions` if specified must be valid AWS region codes (e.g., us-east-1, eu-west-1)
- `budget_constraints` if provided must specify monthly or annual budget

**Source freshness:**
- AWS Well-Architected Framework (accessed 2025-10-25T21:30:36-04:00): https://aws.amazon.com/architecture/well-architected/ - verify 2024+ whitepaper versions
- AWS Compute Services (accessed 2025-10-25T21:30:36-04:00): https://aws.amazon.com/products/compute/ - EC2, Lambda, ECS, EKS, Fargate feature matrix
- AWS Storage Services (accessed 2025-10-25T21:30:36-04:00): https://aws.amazon.com/products/storage/ - S3, EBS, EFS durability and performance SLAs
- AWS Networking (accessed 2025-10-25T21:30:36-04:00): https://docs.aws.amazon.com/vpc/latest/userguide/ - VPC design patterns and limits
- AWS Pricing Calculator (accessed 2025-10-25T21:30:36-04:00): https://calculator.aws/ - cost estimation methodology
- AWS IAM Best Practices (accessed 2025-10-25T21:30:36-04:00): https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html - least-privilege policies

**Decision thresholds:**
- Lambda recommended if: stateless, event-driven, <15min execution, variable load
- ECS/Fargate recommended if: containerized, moderate complexity, managed orchestration preferred
- EKS recommended if: Kubernetes-native, complex orchestration, multi-cloud portability
- EC2 recommended if: specialized instance types, full OS control, legacy dependencies
- S3 recommended for: object storage, static assets, data lakes, archival (11 9s durability)
- EBS recommended for: block storage, database volumes, low-latency (<1ms)
- EFS recommended for: shared file systems, NFS compatibility, auto-scaling storage

---

## Procedure

### T1: Quick Architecture Recommendation (≤2k tokens)

**Fast path for 80% of AWS architecture decisions:**

1. **Workload classification:**
   - **Web application**: API Gateway + Lambda OR ALB + ECS Fargate
   - **Data processing**: Lambda + S3 + Glue OR EMR for big data
   - **Real-time**: Kinesis + Lambda + DynamoDB OR ECS with streaming
   - **Batch**: Batch + S3 OR Step Functions + Lambda
   - **Machine learning**: SageMaker + S3 + Lambda for inference

2. **Core service selection:**
   - **Compute**: Choose based on decision thresholds (see Pre-Checks)
   - **Storage**: S3 for objects, RDS/DynamoDB for databases, EBS for block
   - **Networking**: VPC with public/private subnets, NAT Gateway, Internet Gateway
   - **Integration**: API Gateway for APIs, EventBridge for events, SQS/SNS for messaging

3. **Quick cost estimate:**
   - Compute: instance hours x hourly rate OR Lambda invocations x GB-seconds
   - Storage: GB stored x storage rate + data transfer costs
   - Networking: data transfer out + NAT Gateway hours
   - Database: instance hours + I/O + storage (RDS) OR read/write units (DynamoDB)

4. **Security baseline:**
   - VPC with private subnets for compute, public subnets for load balancers
   - Security groups with least-privilege ingress rules
   - IAM roles with managed policies (AmazonS3ReadOnlyAccess, etc.)
   - Encryption at rest (S3 default encryption, EBS encryption, RDS encryption)
   - Encryption in transit (TLS/HTTPS required)

5. **Output (T1):**
   - AWS service architecture diagram (textual description with service names)
   - Core services with justification (compute, storage, database, networking)
   - Rough monthly cost estimate (±30% accuracy)
   - Well-Architected pillar alignment summary
   - Recommended next steps for T2 detailed design

**Abort conditions:**
- Workload requirements unclear or conflicting (e.g., "real-time + batch")
- Compliance requirements (HIPAA, PCI-DSS) needing legal review (note for T2)
- Budget constraints conflict with availability requirements

---

### T2: Detailed Architecture Design with IaC (≤6k tokens)

**For production-ready AWS architectures with infrastructure-as-code:**

1. **All T1 steps** plus:

2. **Comprehensive service integration:**

   **Compute tier:**
   - EC2: instance family selection (compute-optimized c6i, memory-optimized r6i, general t3/t4g)
   - Auto Scaling Groups with target tracking policies (CPU, ALB requests, custom metrics)
   - Launch Templates with user data for bootstrapping
   - Spot instances for fault-tolerant workloads (up to 90% cost savings)
   - Lambda: runtime selection (Python 3.12, Node.js 20), memory optimization, reserved concurrency
   - ECS Fargate: task definitions with resource limits, task placement strategies
   - EKS: managed node groups with mixed instance types, cluster autoscaler

   **Storage tier:**
   - S3: bucket policies with encryption (SSE-S3, SSE-KMS), versioning, lifecycle policies
   - S3 Intelligent-Tiering for automatic cost optimization
   - S3 Transfer Acceleration for global uploads
   - S3 Glacier for archival (Deep Archive for long-term retention)
   - EBS: volume types (gp3 for general, io2 Block Express for high IOPS, st1 for throughput)
   - EFS: performance modes (General Purpose, Max I/O), throughput modes (Elastic, Provisioned)
   - FSx: file system choice (Lustre for HPC, Windows File Server, NetApp ONTAP)

   **Networking tier:**
   - VPC design: CIDR planning (/16 VPC, /24 subnets), multi-AZ for high availability
   - Public subnets (0.0.0.0/0 route to IGW) for ALB, NAT Gateway
   - Private subnets for compute with route to NAT Gateway OR VPC Endpoints
   - VPC Endpoints (Gateway for S3/DynamoDB, Interface for other services) to reduce NAT costs
   - Network ACLs for subnet-level security (stateless), Security Groups for instance-level (stateful)
   - Transit Gateway for multi-VPC or hybrid connectivity
   - Route 53 for DNS with health checks and routing policies (weighted, latency, geolocation)

   **Serverless integration:**
   - API Gateway REST/HTTP APIs with custom domains, usage plans, API keys
   - Lambda integration with EventBridge rules, S3 events, DynamoDB Streams
   - Step Functions state machines for orchestration with error handling and retries
   - SQS for decoupling (standard for throughput, FIFO for ordering), dead-letter queues
   - SNS for fan-out messaging patterns, email/SMS notifications

   **Database selection:**
   - RDS: engine choice (PostgreSQL, MySQL, Aurora for performance), Multi-AZ for HA
   - Aurora Serverless v2 for variable workloads with auto-scaling
   - DynamoDB: on-demand vs provisioned capacity, global tables for multi-region
   - ElastiCache: Redis for caching with cluster mode, Memcached for simple caching
   - Redshift for data warehousing with Spectrum for S3 queries

3. **Well-Architected Framework deep-dive:**

   **Operational Excellence:**
   - CloudFormation/CDK for IaC with stack drift detection
   - CloudWatch Logs centralization, Log Insights queries
   - CloudWatch Alarms with SNS notifications
   - Systems Manager for parameter store, patch management, session manager
   - AWS Config for compliance monitoring and resource inventory

   **Security:**
   - IAM roles for EC2/Lambda (no access keys), cross-account roles with external ID
   - IAM policies with least privilege, service control policies (SCPs) for organization
   - Secrets Manager for database credentials with automatic rotation
   - GuardDuty for threat detection, Security Hub for compliance dashboards
   - AWS WAF for application firewall (API Gateway, ALB), Shield Standard/Advanced for DDoS
   - VPC Flow Logs for network traffic analysis
   - KMS customer-managed keys for encryption with key rotation

   **Reliability:**
   - Multi-AZ deployments (at least 2 AZs, 3 for critical workloads)
   - Multi-region for disaster recovery (pilot light, warm standby, or active-active)
   - Route 53 health checks with failover routing
   - RDS automated backups (point-in-time recovery), cross-region snapshots
   - S3 Cross-Region Replication (CRR) for critical data
   - CloudFormation StackSets for multi-region deployment

   **Performance Efficiency:**
   - CloudFront CDN for static content and API caching
   - ElastiCache for database query caching
   - RDS Read Replicas for read-heavy workloads
   - DynamoDB DAX for microsecond latency
   - Lambda Provisioned Concurrency to eliminate cold starts
   - EBS provisioned IOPS (io2) for latency-sensitive databases

   **Cost Optimization:**
   - Savings Plans (Compute Savings Plans for EC2/Fargate/Lambda flexibility)
   - Reserved Instances for predictable workloads (1-year or 3-year commitment)
   - S3 Intelligent-Tiering and lifecycle policies (Standard → IA → Glacier)
   - Spot Instances for fault-tolerant batch/analytics (Spot Fleet with price limits)
   - Auto Scaling to match capacity with demand
   - Cost Allocation Tags for cost attribution by team/project
   - AWS Cost Explorer and Budgets with alerts

4. **Infrastructure-as-Code generation:**

   **CloudFormation approach:**
   - Modular templates with nested stacks (network, compute, database, storage)
   - Parameters for environment-specific values (CIDR ranges, instance types)
   - Mappings for region-specific AMIs and availability zones
   - Outputs for cross-stack references (VPC ID, subnet IDs, security group IDs)
   - Stack policies to prevent accidental deletion of critical resources

   **CDK approach:**
   - Construct reuse with higher-level abstractions
   - Type safety and IDE autocomplete (TypeScript/Python)
   - Built-in best practices (default encryption, least-privilege IAM)
   - Aspects for cross-cutting concerns (tagging, logging)
   - CDK Pipelines for CI/CD deployment

5. **Security hardening:**
   - IMDSv2 enforcement for EC2 instance metadata
   - S3 Block Public Access at account level
   - EBS default encryption enabled
   - RDS/Aurora encryption at rest with KMS
   - Certificate Manager for TLS certificates with auto-renewal
   - Macie for S3 sensitive data discovery
   - Inspector for EC2 vulnerability scanning
   - CloudTrail for API audit logging with log file validation

6. **Cost estimation (detailed):**
   - Compute: instance family, hours/month, Savings Plan discount
   - Storage: S3 storage classes (Standard, IA, Glacier), requests, data transfer
   - Database: RDS instance hours, I/O operations, backup storage
   - Networking: data transfer out (inter-region, internet), NAT Gateway hours
   - Total Cost of Ownership (TCO): 1-year and 3-year projections
   - Cost optimization opportunities: reserved capacity, rightsizing, lifecycle policies

7. **Migration strategy (if current_architecture provided):**
   - **Discovery phase**: Application Discovery Service, Migration Hub
   - **Planning**: AWS Migration Evaluator for TCO, Database Migration Service (DMS) for schema conversion
   - **Migration waves**:
     - Wave 1: Stateless web tier (rehost with EC2 or refactor to containers/Lambda)
     - Wave 2: Database tier (DMS with minimal downtime, or snapshot restore)
     - Wave 3: Integration points (message queues, caching, file storage)
   - **Cutover strategy**: DNS-based with Route 53 weighted routing (10% → 50% → 100%)
   - **Validation**: smoke tests, performance benchmarks, rollback procedures

8. **Output (T2):**
   - Complete architecture diagram with all AWS services and data flows
   - CloudFormation templates OR CDK code (modular, production-ready)
   - Detailed cost estimate with 1-year/3-year TCO and optimization recommendations
   - IAM policies and security group rules (least-privilege)
   - Well-Architected Framework assessment with pillar scores and recommendations
   - Deployment guide with prerequisites and step-by-step instructions
   - Migration plan with timeline, risks, and rollback procedures (if applicable)
   - Monitoring and alerting configuration (CloudWatch dashboards, alarms)

**Abort conditions:**
- Specialized GPU/FPGA requirements needing EC2 instance family expertise
- Highly regulated workloads (FedRAMP High, IL5) requiring compliance specialist review
- Complex hybrid connectivity (multiple Direct Connect, VPN mesh) needing network architect
- Custom AMI creation or OS hardening outside of AWS managed services

---

### T3: Not Implemented

**Note:** This skill implements T1 (quick recommendations) and T2 (detailed design with IaC) tiers only. T2 provides production-ready AWS architectures with comprehensive Well-Architected Framework assessment, security hardening, cost optimization, and migration planning. For specialized scenarios requiring deeper analysis (custom compliance frameworks, complex hybrid architectures, or organization-wide AWS Landing Zone design), consult AWS Solutions Architects or AWS Professional Services.

**Future T3 considerations:**
- Organization-wide AWS Landing Zone design with AWS Control Tower
- Multi-account strategy with AWS Organizations and consolidated billing
- Complex hybrid architectures with Direct Connect, Transit Gateway mesh, and SD-WAN
- Custom compliance frameworks beyond standard AWS Config rules
- AWS Outposts and hybrid edge deployment patterns
- Large-scale migration program management (Application Portfolio Assessment)

---

## Decision Rules

**Compute service selection:**
- **Lambda** if all of:
  - Stateless or state in DynamoDB/S3
  - <15min execution time (<900 seconds)
  - Event-driven (API Gateway, S3, EventBridge, SQS)
  - Variable/unpredictable load (auto-scales to zero)
  - Cost-sensitive for low/moderate traffic

- **ECS Fargate** if:
  - Containerized application
  - Don't want to manage EC2 instances
  - Moderate complexity (1-20 containers)
  - Predictable resource requirements

- **EKS** if:
  - Kubernetes-native (existing K8s apps or team expertise)
  - Complex orchestration (>20 microservices)
  - Multi-cloud portability required
  - Advanced networking (Istio, service mesh)

- **EC2** if:
  - Specialized instance types (GPU, high memory, burstable credits)
  - Full OS control (custom kernel, drivers)
  - Legacy applications not containerizable
  - Bring Your Own License (BYOL)

**Storage service selection:**
- **S3** for: object storage, static assets (images, videos), data lakes, backups, archival
- **EBS** for: EC2 block storage, databases (PostgreSQL, MySQL), low-latency (<1ms)
- **EFS** for: shared file storage across multiple EC2/ECS, NFS workloads, auto-scaling
- **FSx** for: Windows file server (SMB), Lustre (HPC), NetApp ONTAP (enterprise NAS)

**Database service selection:**
- **RDS Aurora** if: relational database, high performance (5x MySQL, 3x PostgreSQL), Multi-AZ HA
- **RDS (PostgreSQL/MySQL)** if: managed relational database, compatibility with open-source engines
- **DynamoDB** if: NoSQL key-value or document store, single-digit millisecond latency, global tables
- **ElastiCache Redis** if: in-memory caching, session store, pub/sub messaging
- **Redshift** if: data warehouse, OLAP analytics, petabyte-scale

**Networking design:**
- **Single VPC** if: small footprint (<100 resources), single application
- **Multi-VPC** if: isolation required (dev/staging/prod), different teams/applications
- **Transit Gateway** if: >3 VPCs or hybrid connectivity (on-premises)
- **VPC Peering** if: 2-3 VPCs within same region needing connectivity
- **NAT Gateway** vs **VPC Endpoints**: use VPC Endpoints for S3/DynamoDB to save NAT costs

**Multi-region strategy:**
- **Single region** if: latency requirements met, no DR requirements, cost-sensitive
- **Multi-region active-passive** if: disaster recovery (RTO <1 hour, RPO <1 hour)
- **Multi-region active-active** if: global user base, <100ms latency requirement, highest availability

**Ambiguity handling:**
- If workload type unclear → request architecture diagram or user journey map
- If performance requirements unknown → recommend T1 baseline with monitoring, iterate
- If budget constraints conflict with availability → present trade-off matrix with RTO/RPO vs cost

**Stop conditions:**
- Conflicting requirements (e.g., "lowest cost + highest availability + multi-region")
- Regulatory requirements without defined compliance framework
- No clear application architecture or data flow documentation (T2 requires this)

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "architecture": {
    "workload_type": "web-app | data-processing | real-time | batch | ml | hybrid",
    "services": [
      {
        "category": "compute | storage | database | networking | integration | security",
        "service_name": "AWS service name (e.g., EC2, S3, Lambda)",
        "rationale": "why this service was selected",
        "configuration_summary": "key configuration details"
      }
    ],
    "data_flow": "textual description of data flow between services"
  },
  "cost_estimate": {
    "monthly_usd": "number (approximate for T1, detailed for T2)",
    "breakdown": {
      "compute": "number",
      "storage": "number",
      "database": "number",
      "networking": "number",
      "other": "number"
    },
    "optimization_opportunities": ["array of cost reduction recommendations"]
  },
  "well_architected_alignment": {
    "operational_excellence": "high | medium | low with justification",
    "security": "high | medium | low with justification",
    "reliability": "high | medium | low with justification",
    "performance_efficiency": "high | medium | low with justification",
    "cost_optimization": "high | medium | low with justification"
  },
  "next_steps": ["array of actionable recommendations"]
}
```

**Additional T2 fields:**
```json
{
  "iac_code": {
    "type": "cloudformation | cdk",
    "language": "yaml | typescript | python (for CDK)",
    "files": [
      {
        "filename": "string",
        "content": "string (CloudFormation YAML or CDK code)",
        "description": "purpose of this template/stack"
      }
    ]
  },
  "security_configuration": {
    "iam_policies": [
      {
        "role_name": "string",
        "policy_document": "JSON IAM policy with least privilege"
      }
    ],
    "security_groups": [
      {
        "name": "string",
        "ingress_rules": ["array of allowed inbound traffic"],
        "egress_rules": ["array of allowed outbound traffic"]
      }
    ],
    "encryption": {
      "at_rest": "services and encryption methods (KMS keys)",
      "in_transit": "TLS configuration and certificate management"
    }
  },
  "monitoring": {
    "cloudwatch_dashboards": "description of key metrics to monitor",
    "alarms": [
      {
        "metric": "string (e.g., CPUUtilization, 5XXError)",
        "threshold": "number",
        "action": "SNS notification or Auto Scaling action"
      }
    ],
    "logs": "centralized logging strategy (CloudWatch Logs, Log Groups)"
  },
  "migration_plan": {
    "phases": [
      {
        "phase_number": "integer",
        "description": "string",
        "services_migrated": ["array of AWS services deployed"],
        "duration": "string (e.g., 2 weeks)",
        "success_criteria": ["array of validation steps"],
        "rollback_procedure": "string"
      }
    ]
  }
}
```

---

## Examples

```yaml
# T1 Example: Serverless Web Application Architecture
# API Gateway + Lambda + DynamoDB + S3 + CloudFront

Services:
  Compute: Lambda (Python 3.12, 512MB memory, on-demand)
  Database: DynamoDB (on-demand capacity, single table design)
  Storage: S3 (Standard, static assets + user uploads)
  CDN: CloudFront (distribution for S3 + API Gateway)
  API: API Gateway (HTTP API, JWT authorizer)
  Auth: Cognito User Pools (user management)

Estimated Monthly Cost (10K users, 1M requests):
  Lambda: $20 (1M invocations, 512MB, 200ms avg)
  DynamoDB: $10 (1GB storage, 1M read/write units)
  S3: $5 (10GB storage, 100K requests)
  CloudFront: $15 (100GB transfer)
  API Gateway: $10 (1M requests)
  Total: ~$60/month
```

(Full T2 CloudFormation example: `/resources/cloudformation-serverless-webapp.yaml`)
(Full T2 CDK example: `/resources/cdk-webapp-stack.ts`)

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - service selection + cost estimate + Well-Architected summary
- **T2**: ≤6,000 tokens - detailed design + IaC templates + security + migration plan

**Safety checks:**
- No hardcoded credentials in IaC templates (use Secrets Manager references)
- IAM policies use least-privilege principles (deny by default, explicit allows)
- Security groups have no 0.0.0.0/0 SSH access (use Systems Manager Session Manager)
- S3 buckets have Block Public Access enabled unless explicitly public
- Encryption enabled for all data stores (S3, EBS, RDS, DynamoDB)

**Auditability:**
- All AWS service recommendations cite official documentation with access date (NOW_ET)
- Cost estimates include calculation methodology (instance hours, GB-months, requests)
- Well-Architected pillars mapped to specific AWS services and configurations
- Compliance controls (if applicable) mapped to AWS Config rules or Security Hub standards

**Determinism:**
- Given same inputs, produce identical service selection recommendations
- Cost estimates use AWS Pricing Calculator methodology (consistent rates)
- IaC templates follow AWS CloudFormation best practices or CDK constructs

**Validation requirements:**
- T2 CloudFormation templates must pass `aws cloudformation validate-template`
- T2 CDK code must pass `cdk synth` without errors
- IAM policies must be valid JSON and comply with IAM policy grammar
- Security group rules must have valid CIDR blocks and port ranges

---

## Resources

**Official AWS Documentation (accessed 2025-10-25T21:30:36-04:00):**
- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- AWS Well-Architected Tool: https://aws.amazon.com/well-architected-tool/
- AWS Architecture Center: https://aws.amazon.com/architecture/
- AWS Compute Services: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html
- AWS Storage Services: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html
- AWS Networking: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/networking-services.html

**AWS Service Documentation:**
- Amazon EC2: https://docs.aws.amazon.com/ec2/
- AWS Lambda: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
- Amazon S3: https://docs.aws.amazon.com/s3/
- Amazon VPC: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- Amazon RDS: https://docs.aws.amazon.com/rds/
- Amazon DynamoDB: https://docs.aws.amazon.com/dynamodb/

**Infrastructure-as-Code:**
- AWS CloudFormation: https://docs.aws.amazon.com/cloudformation/
- AWS CDK: https://docs.aws.amazon.com/cdk/v2/guide/home.html
- CDK Patterns: https://cdkpatterns.com/
- CloudFormation Best Practices: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html

**Cost Optimization:**
- AWS Pricing Calculator: https://calculator.aws/
- AWS Cost Management: https://aws.amazon.com/aws-cost-management/
- AWS Cost Optimization Pillar: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
- Savings Plans: https://aws.amazon.com/savingsplans/
- Reserved Instances: https://aws.amazon.com/ec2/pricing/reserved-instances/

**Security Best Practices:**
- IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Security Pillar: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html
- AWS Security Hub: https://docs.aws.amazon.com/securityhub/
- AWS Secrets Manager: https://docs.aws.amazon.com/secretsmanager/

**Example Templates:**
- `/resources/cloudformation-serverless-webapp.yaml` - Complete serverless web app stack
- `/resources/cloudformation-ecs-fargate.yaml` - ECS Fargate with ALB and RDS
- `/resources/cdk-webapp-stack.ts` - CDK TypeScript example for web application
- `/resources/iam-least-privilege-policies.json` - Example least-privilege IAM policies
- `/resources/vpc-reference-architecture.yaml` - Multi-AZ VPC with public/private subnets

**Migration Resources:**
- AWS Migration Hub: https://aws.amazon.com/migration-hub/
- AWS Database Migration Service: https://aws.amazon.com/dms/
- AWS Application Discovery Service: https://aws.amazon.com/application-discovery/
- 6 R's Migration Strategies: https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-strategies/welcome.html
