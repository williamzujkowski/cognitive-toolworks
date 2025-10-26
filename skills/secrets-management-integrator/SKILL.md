---
name: "Secrets Management Integrator"
slug: "secrets-management-integrator"
description: "Integrate secrets management (Vault, AWS, Azure, GCP) with rotation policies, access controls, and Kubernetes/CI/CD application integration."
capabilities:
  - HashiCorp Vault integration (static and dynamic secrets)
  - AWS Secrets Manager configuration with automatic rotation
  - Azure Key Vault integration with managed identities
  - GCP Secret Manager setup with workload identity
  - Kubernetes external-secrets operator configuration
  - CI/CD pipeline secrets integration
  - Dynamic database credentials and certificate management
  - Access policy and RBAC configuration
inputs:
  - secrets_backend: "vault | aws-secrets | azure-keyvault | gcp-secretmanager (string, required)"
  - integration_target: "kubernetes | cicd | application (string, required)"
  - rotation_policy: "manual | automatic | dynamic (string, required)"
  - credential_type: "database | api-key | certificate | generic (string, optional)"
outputs:
  - secrets_config: "Backend-specific configuration (HCL, JSON, or YAML)"
  - access_policies: "Role and policy definitions for least-privilege access"
  - integration_code: "Application SDK usage examples with language-specific clients"
  - rotation_scripts: "Automated rotation workflows (Lambda, Cloud Functions, or CronJobs)"
keywords:
  - secrets-management
  - vault
  - aws-secrets-manager
  - azure-key-vault
  - gcp-secret-manager
  - kubernetes-secrets
  - external-secrets
  - dynamic-credentials
  - secret-rotation
  - zero-trust
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no actual secrets or credentials; safe for open repositories"
links:
  - https://developer.hashicorp.com/vault/docs
  - https://docs.aws.amazon.com/secretsmanager/
  - https://learn.microsoft.com/en-us/azure/key-vault/
  - https://cloud.google.com/secret-manager/docs
  - https://external-secrets.io/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Application requires centralized secrets management
- Database credentials need automatic rotation
- Kubernetes workloads need secure secret injection
- CI/CD pipelines require secrets from external vault
- Dynamic credentials needed for cloud resources (AWS IAM, GCP service accounts)
- Certificate lifecycle management (TLS, mutual TLS)
- Migration from environment variables or config files to secrets manager

**Not for:**
- Password managers for end-users (use 1Password, Bitwarden, etc.)
- Configuration management without sensitive data (use ConfigMaps, parameter stores)
- Public API keys or non-sensitive tokens
- Single-tenant applications without security requirements

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T02:31:21-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `secrets_backend` must be one of: [vault, aws-secrets, azure-keyvault, gcp-secretmanager]
- `integration_target` must be one of: [kubernetes, cicd, application]
- `rotation_policy` must be one of: [manual, automatic, dynamic]
- If `credential_type` provided, must be one of: [database, api-key, certificate, generic]

**Source freshness:**
- HashiCorp Vault v1.15+ documentation (accessed 2025-10-26T02:31:21-04:00): https://developer.hashicorp.com/vault/docs
- AWS Secrets Manager Best Practices (accessed 2025-10-26T02:31:21-04:00): https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html
- External Secrets Operator v0.9+ (accessed 2025-10-26T02:31:21-04:00): https://external-secrets.io/latest/
- OWASP Secrets Management Cheat Sheet (accessed 2025-10-26T02:31:21-04:00): https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

---

## Procedure

### T1: Basic Secrets Storage and Retrieval (≤2k tokens)

**HashiCorp Vault:**
1. Enable KV secrets engine (v2 for versioning)
2. Create secret at logical path
3. Configure application authentication (AppRole, Kubernetes auth)
4. Retrieve secret via Vault API or SDK

**AWS Secrets Manager:**
1. Create secret via AWS CLI or SDK
2. Configure IAM policy for least-privilege access
3. Enable encryption with AWS KMS
4. Retrieve secret in application code (AWS SDK)

**Azure Key Vault:**
1. Create Key Vault resource
2. Store secret via Azure CLI or SDK
3. Assign managed identity to application
4. Access secret using Azure Identity SDK

**GCP Secret Manager:**
1. Create secret in GCP project
2. Configure IAM permissions (Secret Manager Secret Accessor role)
3. Enable workload identity for GKE pods
4. Retrieve secret using GCP client library

### T2: Rotation Policies and Access Controls (≤6k tokens)

**Automatic Rotation (AWS Secrets Manager):**
1. Define rotation Lambda function with database credentials logic
2. Configure rotation schedule (30, 60, 90 days)
3. Use AWS managed rotation for RDS, Redshift, DocumentDB
4. Monitor rotation via CloudWatch events

**Dynamic Credentials (Vault Database Engine):**
1. Enable database secrets engine
2. Configure database connection (PostgreSQL, MySQL, MongoDB)
3. Define role with SQL statements for credential creation
4. Generate short-lived credentials on demand (default TTL 1 hour)

**Access Policies:**
- Vault: HCL policy files with path-based permissions (read, create, update, delete)
- AWS: IAM policies with resource ARNs and condition keys (aws:SecureTransport, aws:SourceVpc)
- Azure: RBAC assignments scoped to Key Vault (Key Vault Secrets User, Key Vault Secrets Officer)
- GCP: IAM bindings with least-privilege roles (roles/secretmanager.secretAccessor)

**Audit Logging:**
- Vault: Enable audit device (file, syslog, socket)
- AWS: CloudTrail integration for Secrets Manager API calls
- Azure: Monitor diagnostic settings for Key Vault access
- GCP: Cloud Audit Logs for Secret Manager operations

### T3: Application Integration Patterns (≤12k tokens)

**Kubernetes Integration (External Secrets Operator):**
1. Install external-secrets operator via Helm chart
2. Configure SecretStore CRD for backend (Vault, AWS, Azure, GCP)
3. Create ExternalSecret CRD referencing secret path
4. Operator syncs secrets to Kubernetes Secret objects
5. Mount secrets as environment variables or files in pods

**CI/CD Integration:**
- GitHub Actions: Use AWS OIDC provider or Vault JWT auth with GitHub token
- GitLab CI: Vault integration via JWT authentication with CI_JOB_JWT
- Jenkins: Vault plugin with AppRole authentication
- Azure DevOps: Azure Key Vault task with service connection

**Application SDK Usage:**
- Python: `hvac` (Vault), `boto3` (AWS), `azure-keyvault-secrets`, `google-cloud-secret-manager`
- Go: Vault API client, AWS SDK v2, Azure SDK, GCP client libraries
- Node.js: `node-vault`, AWS SDK v3, `@azure/keyvault-secrets`, `@google-cloud/secret-manager`
- Java: Spring Cloud Vault, AWS SDK v2, Azure Key Vault SDK, GCP Secret Manager client

**Certificate Management:**
- Vault PKI engine for internal CA and certificate issuance
- cert-manager integration with Vault, AWS ACM, or Let's Encrypt
- Automatic certificate renewal with 30-day window before expiration

**Token budgets:**
- **T1:** ≤2k tokens (single backend, basic storage/retrieval)
- **T2:** ≤6k tokens (rotation, access policies, audit logging)
- **T3:** ≤12k tokens (Kubernetes, CI/CD, multi-language SDKs, certificate management)

---

## Decision Rules

**Backend Selection:**
- Use **Vault** for: multi-cloud, dynamic credentials, PKI, advanced policy engine
- Use **AWS Secrets Manager** for: AWS-native applications, managed RDS rotation
- Use **Azure Key Vault** for: Azure-native applications, HSM-backed keys, managed identities
- Use **GCP Secret Manager** for: GCP-native applications, workload identity, simple key-value storage

**Rotation Policy:**
- **Manual:** Low-risk secrets, infrequent access, legacy systems
- **Automatic:** Database passwords, API keys with fixed rotation schedule
- **Dynamic:** High-security environments, short-lived credentials (≤24 hours), zero standing privileges

**Abort Conditions:**
- No backend specified → cannot proceed
- Kubernetes integration requested but no cluster access → provide manifest templates only
- Dynamic credentials requested for unsupported database → fallback to automatic rotation

**Ambiguity Thresholds:**
- If application language unspecified → provide examples for Python, Go, Node.js
- If rotation schedule unspecified → default to 90 days for automatic, 1 hour for dynamic
- If access policy unspecified → generate least-privilege policy based on integration target

---

## Output Contract

**Required fields:**
```json
{
  "secrets_backend": "vault|aws-secrets|azure-keyvault|gcp-secretmanager",
  "integration_target": "kubernetes|cicd|application",
  "rotation_policy": "manual|automatic|dynamic",
  "credential_type": "database|api-key|certificate|generic",
  "timestamp": "ISO-8601 with timezone",
  "secrets_config": {
    "backend_endpoint": "https://vault.example.com:8200 or AWS region",
    "authentication_method": "kubernetes|approle|iam|managed-identity|workload-identity",
    "secret_path": "logical path or ARN",
    "config_file": "HCL, JSON, or YAML configuration"
  },
  "access_policies": {
    "policy_name": "application-secrets-reader",
    "policy_type": "vault-policy|iam-policy|rbac-assignment|iam-binding",
    "policy_document": "HCL, JSON, or YAML policy definition",
    "scope": "path or resource ARN"
  },
  "integration_code": {
    "language": "python|go|nodejs|java",
    "sdk_version": "library version (e.g., hvac==2.1.0)",
    "authentication_snippet": "code for backend authentication",
    "secret_retrieval_snippet": "code for fetching secret",
    "error_handling": "retry logic and fallback strategy"
  },
  "rotation_scripts": {
    "rotation_type": "lambda|cloud-function|cronjob|vault-engine",
    "schedule": "cron expression or TTL",
    "rotation_logic": "code or configuration for rotation",
    "notification": "SNS, Pub/Sub, or webhook for rotation events"
  },
  "deployment_manifests": [
    {
      "type": "kubernetes|terraform|cloudformation",
      "filename": "external-secret.yaml or main.tf",
      "content": "manifest or IaC code"
    }
  ]
}
```

---

## Examples

**Example: Vault + Kubernetes External Secrets**

```yaml
# Input: vault backend, kubernetes target, dynamic rotation
# Output: ExternalSecret for PostgreSQL dynamic credentials
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      auth:
        kubernetes:
          role: "production-app"
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: postgres-creds
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
  data:
    - secretKey: username
      remoteRef:
        key: database/creds/postgres-prod
    - secretKey: password
      remoteRef:
        key: database/creds/postgres-prod
```

---

## Quality Gates

**Token budgets:**
- T1 ≤2k tokens (basic setup and retrieval)
- T2 ≤6k tokens (rotation and access policies)
- T3 ≤12k tokens (full integration with Kubernetes/CI/CD)

**Safety:**
- No actual secrets or credentials in output
- All examples use placeholders (example.com, REDACTED, etc.)
- No production endpoint URLs or account IDs

**Auditability:**
- All configurations cite official documentation
- Access policies follow least-privilege principle
- Audit logging enabled for all backends

**Determinism:**
- Same inputs + backend = consistent configuration
- SDK versions pinned in integration code
- Rotation schedules explicit (no vague "periodic" rotation)

---

## Resources

**HashiCorp Vault:**
- Vault Documentation: https://developer.hashicorp.com/vault/docs (accessed 2025-10-26T02:31:21-04:00)
- Vault Kubernetes Auth: https://developer.hashicorp.com/vault/docs/auth/kubernetes (accessed 2025-10-26T02:31:21-04:00)
- Vault Database Secrets Engine: https://developer.hashicorp.com/vault/docs/secrets/databases (accessed 2025-10-26T02:31:21-04:00)
- Vault PKI Secrets Engine: https://developer.hashicorp.com/vault/docs/secrets/pki (accessed 2025-10-26T02:31:21-04:00)

**AWS Secrets Manager:**
- AWS Secrets Manager Best Practices: https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html (accessed 2025-10-26T02:31:21-04:00)
- Secrets Manager Rotation: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html (accessed 2025-10-26T02:31:21-04:00)

**Azure Key Vault:**
- Azure Key Vault Overview: https://learn.microsoft.com/en-us/azure/key-vault/general/overview (accessed 2025-10-26T02:31:21-04:00)
- Managed Identities: https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview (accessed 2025-10-26T02:31:21-04:00)

**GCP Secret Manager:**
- Secret Manager Documentation: https://cloud.google.com/secret-manager/docs (accessed 2025-10-26T02:31:21-04:00)
- Workload Identity: https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity (accessed 2025-10-26T02:31:21-04:00)

**Kubernetes Integration:**
- External Secrets Operator: https://external-secrets.io/latest/ (accessed 2025-10-26T02:31:21-04:00)
- Kubernetes Secrets: https://kubernetes.io/docs/concepts/configuration/secret/ (accessed 2025-10-26T02:31:21-04:00)

**Security Best Practices:**
- OWASP Secrets Management: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html (accessed 2025-10-26T02:31:21-04:00)
- NIST SP 800-57 Key Management: https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final (accessed 2025-10-26T02:31:21-04:00)
