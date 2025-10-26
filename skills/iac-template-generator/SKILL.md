---
name: "Infrastructure as Code Template Generator"
slug: iac-template-generator
description: "Generate IaC templates for Terraform, CloudFormation, and Pulumi with modules for compute, storage, networking, and multi-environment support."
capabilities:
  - generate_iac_templates
  - multi_environment_config
inputs:
  iac_tool:
    type: string
    description: "IaC tool: terraform, cloudformation, pulumi, cdk"
    required: true
  cloud_provider:
    type: string
    description: "Cloud provider: aws, azure, gcp, multi-cloud"
    required: true
  resources:
    type: array
    description: "Resources to provision: vpc, compute, storage, database, etc."
    required: true
  environments:
    type: array
    description: "Target environments: dev, staging, production"
    required: false
outputs:
  iac_templates:
    type: object
    description: "IaC modules with variables and documentation"
  state_config:
    type: code
    description: "Remote state backend configuration"
keywords:
  - infrastructure-as-code
  - terraform
  - cloudformation
  - pulumi
  - cdk
  - aws
  - azure
  - gcp
  - iac
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: required
links:
  - https://developer.hashicorp.com/terraform/docs
  - https://docs.aws.amazon.com/cloudformation/
  - https://www.pulumi.com/docs/
  - https://docs.aws.amazon.com/cdk/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Infrastructure provisioning needed for new project
- Existing infrastructure requires IaC conversion (eliminate drift)
- Multi-environment deployment needs consistent infrastructure
- Cloud migration requires infrastructure templates
- Infrastructure security hardening requires declarative config

**Use this skill when** you need production-ready Infrastructure as Code templates with modules, variables, and remote state management.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T01:33:56-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `iac_tool` is one of: `terraform`, `cloudformation`, `pulumi`, `cdk`
   - `cloud_provider` is one of: `aws`, `azure`, `gcp`, `multi-cloud`
   - `resources` contains valid resource types
   - `environments` list is non-empty if multi-environment support needed
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Tool compatibility**: Verify IaC tool supports target cloud provider

**Abort conditions:**

- IaC tool doesn't support target cloud provider (e.g., CloudFormation for Azure)
- Resource types incompatible with cloud provider
- Circular dependencies in resource graph

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Generate basic IaC templates for common resources in single environment.

**Steps:**

1. **Analyze inputs and select modules** (400 tokens):
   - Determine IaC tool syntax and structure
   - Map resources to cloud provider services
   - Identify resource dependencies and ordering
   - Select appropriate module structure

2. **Generate IaC templates** (1600 tokens):
   - Create main configuration file
   - Generate resource modules (VPC, compute, storage)
   - Define input variables with types and defaults
   - Configure output values for cross-module references
   - Add remote state backend configuration (S3+DynamoDB for Terraform, etc.)
   - Include inline documentation and comments
   - Generate README with usage instructions

**Decision point**: If requirements include multiple environments, custom networking, or advanced security → escalate to T2.

---

### Tier 2 (Extended Analysis, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Multi-environment IaC with workspaces, advanced networking, security hardening, and compliance.

**Steps:**

1. **Design multi-environment architecture** (2000 tokens):
   - **Terraform** (accessed 2025-10-26T01:33:56-04:00):
     - Configure workspaces for environment isolation
     - Remote state with S3 backend and DynamoDB locking
     - Workspace-specific variable files (terraform.tfvars.dev, terraform.tfvars.prod)
     - Module versioning and source references
   - **CloudFormation** (accessed 2025-10-26T01:33:56-04:00):
     - Stack sets for multi-account deployment
     - Cross-stack references for shared resources
     - Parameters and mappings for environment-specific values
   - **Pulumi** (accessed 2025-10-26T01:33:56-04:00):
     - Stack configuration files per environment
     - Programmatic resource creation with language features
     - State backend configuration (Pulumi Cloud or self-hosted)
   - **CDK** (accessed 2025-10-26T01:33:56-04:00):
     - Environment-specific context values
     - Synthesized CloudFormation templates
     - Asset management and bundling

2. **Generate comprehensive templates** (4000 tokens):
   - **Networking**:
     - VPC with public/private subnets across multiple AZs
     - NAT gateways, internet gateways, route tables
     - Network ACLs and security groups
     - VPC peering and transit gateway (if multi-VPC)
   - **Compute**:
     - EC2 instances with auto-scaling groups
     - Launch templates with user data scripts
     - Load balancers (ALB/NLB)
     - ECS/EKS clusters for containerized workloads
     - Lambda functions for serverless
   - **Storage**:
     - S3 buckets with versioning, encryption, lifecycle policies
     - EBS volumes with encryption
     - EFS for shared file systems
   - **Database**:
     - RDS instances with multi-AZ, backups, encryption
     - DynamoDB tables with autoscaling
     - ElastiCache clusters
   - **Security**:
     - IAM roles and policies with least privilege
     - KMS keys for encryption at rest
     - Secrets Manager for credential storage
     - Security group rules with minimal exposure
     - VPC flow logs and CloudTrail
   - **Monitoring**:
     - CloudWatch alarms and dashboards
     - SNS topics for alerts
     - Log groups with retention policies

**Sources cited** (accessed 2025-10-26T01:33:56-04:00):

- **Terraform Best Practices**: https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices
- **AWS CloudFormation**: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/
- **Pulumi Architecture**: https://www.pulumi.com/docs/concepts/
- **AWS CDK Best Practices**: https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html

---

### Tier 3 (Deep Dive, ≤12k tokens)

**Token budget**: ≤12k tokens

**Scope**: Enterprise IaC with policy-as-code, compliance automation, and multi-cloud orchestration.

**Steps:**

1. **Policy-as-code integration** (4000 tokens):
   - **Terraform**: Sentinel or OPA policy enforcement
   - **CloudFormation**: Guard rules for compliance validation
   - **Pulumi**: Policy packs for resource validation
   - Generate policies for:
     - Resource tagging requirements
     - Security best practices (encryption, public access)
     - Cost controls (instance types, storage classes)
     - Compliance requirements (HIPAA, PCI-DSS, FedRAMP)

2. **Advanced orchestration** (4000 tokens):
   - Multi-cloud resource provisioning with cloud-agnostic abstractions
   - Cross-region disaster recovery configurations
   - Blue-green infrastructure for zero-downtime migrations
   - Infrastructure testing with Terratest, Kitchen-Terraform, or CDK assertions
   - Drift detection and automated remediation
   - Cost estimation and budget alerts

3. **Enterprise features** (4000 tokens):
   - Service catalog integration for self-service provisioning
   - GitOps workflows with automated plan/apply on PR merge
   - Secrets injection from external vaults (HashiCorp Vault, AWS Secrets Manager)
   - Compliance artifact generation (resource inventories, security configs)
   - Module registry and version management
   - Documentation generation from IaC source

**Additional sources** (accessed 2025-10-26T01:33:56-04:00):

- **Terraform Sentinel**: https://developer.hashicorp.com/sentinel
- **AWS CloudFormation Guard**: https://docs.aws.amazon.com/cfn-guard/latest/ug/
- **Pulumi CrossGuard**: https://www.pulumi.com/docs/using-pulumi/crossguard/

---

## Decision Rules

**IaC tool selection:**

- **Terraform**: Multi-cloud, large community, declarative HCL syntax
- **CloudFormation**: AWS-native, tight integration, no external state
- **Pulumi**: Familiar languages (Python, TypeScript), programmatic flexibility
- **CDK**: AWS-native with programming languages, synthesizes to CloudFormation

**Resource organization:**

- Group related resources into logical modules (networking, compute, data)
- Use separate state files for independent infrastructure components
- Version modules for stability and testing

**Environment strategy:**

- **Workspaces**: Good for small differences between environments
- **Separate state files**: Better for production isolation
- **Account separation**: Best for regulatory compliance (dev/prod in different AWS accounts)

**Escalation conditions:**

- Multi-cloud orchestration with complex dependencies
- Custom compliance requirements requiring policy development
- Requirements exceed T3 scope (novel cloud services, experimental features)

**Abort conditions:**

- Resource dependencies create circular references
- Cloud provider quotas prevent required resource provisioning
- Conflicting security requirements (e.g., "publicly accessible" with "private only")

---

## Output Contract

**Required outputs:**

```json
{
  "iac_templates": {
    "type": "object",
    "properties": {
      "tool": "string (terraform|cloudformation|pulumi|cdk)",
      "modules": [
        {
          "name": "string (networking, compute, storage, etc.)",
          "file_path": "string (relative path to module)",
          "content": "string (IaC code)",
          "variables": ["array of input variable definitions"],
          "outputs": ["array of output value definitions"]
        }
      ]
    }
  },
  "state_config": {
    "type": "object",
    "properties": {
      "backend": "string (s3, azurerm, gcs, pulumi-cloud)",
      "config": "object (backend-specific configuration)",
      "content": "string (backend configuration code)"
    }
  }
}
```

**Quality guarantees:**

- IaC templates pass validation (terraform validate, cfn-lint, pulumi preview)
- All variables have types and descriptions
- Remote state backend configured for collaboration
- Security best practices applied (encryption, least privilege)
- Resource dependencies correctly defined

---

## Examples

**Example: Terraform AWS VPC module**

```hcl
# modules/networking/main.tf
variable "environment" {
  type = string
  description = "Environment name (dev, staging, prod)"
}

variable "vpc_cidr" {
  type = string
  description = "CIDR block for VPC"
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "${var.environment}-vpc"
    Environment = var.environment
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

---

## Quality Gates

**Token budgets:**

- **T1**: ≤2k tokens (basic single-environment IaC)
- **T2**: ≤6k tokens (multi-environment with security hardening)
- **T3**: ≤12k tokens (enterprise policy-as-code and orchestration)

**Safety checks:**

- No hardcoded secrets or credentials in templates
- All resources encrypted at rest (where applicable)
- IAM policies follow least privilege principle
- Public access explicitly controlled and justified

**Auditability:**

- All resource changes tracked in version control
- State file changes logged and backed up
- Resource tagging for cost allocation and ownership

**Determinism:**

- Same inputs produce identical IaC templates
- Module versions pinned for stability
- Provider versions locked in configuration

---

## Resources

**Official Documentation** (accessed 2025-10-26T01:33:56-04:00):

- Terraform: https://developer.hashicorp.com/terraform/docs
- CloudFormation: https://docs.aws.amazon.com/cloudformation/
- Pulumi: https://www.pulumi.com/docs/
- AWS CDK: https://docs.aws.amazon.com/cdk/

**Best Practices** (accessed 2025-10-26T01:33:56-04:00):

- Terraform Registry: https://registry.terraform.io/
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- Google Cloud Architecture Framework: https://cloud.google.com/architecture/framework

**Templates** (in repository `/resources/`):

- Terraform modules for AWS, Azure, GCP
- CloudFormation templates for common architectures
- Pulumi examples in Python and TypeScript
