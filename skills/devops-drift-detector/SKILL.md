---
name: Infrastructure Drift Detection and Remediation
slug: devops-drift-detector
description: Detect and remediate infrastructure drift between IaC definitions and live state with continuous monitoring and automated remediation.
capabilities:
  - Detect drift across Terraform/CloudFormation/Pulumi
  - Generate remediation plans with impact analysis
  - Auto-remediate approved drifts with rollback support
  - Report drift trends and compliance violations
inputs:
  - IaC tool type (Terraform, CloudFormation, Pulumi, driftctl)
  - State file location or cloud provider credentials
  - Drift detection schedule or on-demand trigger
  - Remediation policy (manual, semi-automated, fully-automated)
  - Notification channels (Slack, email, webhook)
outputs:
  - Drift detection report with changed resources and attributes
  - Remediation plan with prioritized actions
  - Compliance status and trend analysis
  - Automated remediation logs and rollback instructions
keywords:
  - infrastructure drift
  - terraform drift
  - cloudformation drift
  - pulumi drift
  - drift detection
  - drift remediation
  - IaC reconciliation
  - state management
  - compliance monitoring
  - policy-as-code
version: 1.0.0
owner: william@cognitive-toolworks
license: Apache-2.0
security:
  - No credentials stored in skill outputs
  - State files accessed read-only unless remediation authorized
  - Audit log of all remediation actions
  - Principle of least privilege for cloud provider access
links:
  - https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy
  - https://www.pulumi.com/docs/pulumi-cloud/deployments/drift/
  - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html
  - https://github.com/snyk/driftctl
---

## Purpose & When-To-Use

**Trigger this skill when:**

* Manual infrastructure changes detected outside IaC workflow
* Compliance violation suspected from untracked modifications
* Scheduled drift scan required (daily, weekly, pre-deployment)
* IaC state reconciliation needed after provider API changes
* Post-incident analysis to identify unauthorized changes
* Continuous compliance monitoring for regulated environments

**Outputs:** Drift detection report with changed resources, remediation plan with impact analysis, compliance status, optional auto-remediation execution with audit trail.

## Pre-Checks

**Time normalization:**
* Compute `NOW_ET` = 2025-10-25T21:30:36-04:00 (NIST/time.gov semantics, America/New_York, ISO-8601)

**Input validation:**
* [ ] IaC tool type specified and supported (Terraform, CloudFormation, Pulumi, driftctl)
* [ ] State file location accessible or cloud credentials valid
* [ ] Drift detection scope defined (full stack, specific resources, tag-based)
* [ ] Remediation policy clear (manual-only, semi-auto, full-auto)
* [ ] Notification channels configured if automated alerts required

**Source freshness:**
* [ ] IaC tool documentation current (accessed NOW_ET)
* [ ] Cloud provider drift detection APIs available
* [ ] State file not corrupted and version compatible

**Abort conditions:**
* Missing cloud credentials for state comparison
* IaC tool version incompatibility
* State file locked by active operation

## Procedure

### T1: Fast Path (≤2k tokens) - Quick Drift Scan

**Scope:** Single stack/workspace, on-demand drift check, common 80% case

1. **Identify IaC tool and load state:**
   * Terraform: `terraform plan -refresh-only -detailed-exitcode` to preview state refresh
   * CloudFormation: `aws cloudformation detect-stack-drift --stack-name <name>` then poll `DescribeStackDriftDetectionStatus`
   * Pulumi: `pulumi refresh --preview-only` to compare desired vs actual
   * driftctl: `driftctl scan --from tfstate://<path> --to <provider>` for multi-resource scan

2. **Parse drift detection results:**
   * Extract changed resources (added, modified, deleted, drifted)
   * Identify changed attributes and values (before → after)
   * Calculate drift severity: high (security/network), medium (config), low (tags/metadata)

3. **Generate quick remediation guidance:**
   * **Accept drift:** Update IaC to match live state if change is intentional
   * **Revert drift:** Apply IaC to overwrite live state if change is unauthorized
   * **Ignore drift:** Tag resource as exception if drift is acceptable

4. **Output drift summary:**
   ```json
   {
     "drift_detected": true,
     "tool": "terraform",
     "timestamp": "NOW_ET",
     "drifted_resources": 3,
     "severity": "high",
     "resources": [
       {"id": "aws_security_group.web", "change": "ingress_rules_modified", "severity": "high"}
     ],
     "recommended_action": "revert"
   }
   ```

**Token budget: ≤2k** (state comparison, basic drift report)

### T2: Extended Path (≤6k tokens) - Comprehensive Drift Analysis + Remediation

**Scope:** Multiple stacks, scheduled detection, compliance reporting, semi-automated remediation

1. **T1 fast path** (all steps above)

2. **Multi-stack drift detection:**
   * Terraform Cloud: Enable continuous drift detection via workspace settings; configure schedule (daily/weekly)
     * Source: [Terraform Cloud Drift Detection](https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy) (accessed 2025-10-25T21:30:36-04:00)
   * Pulumi Cloud: Setup Deployments with drift schedules; configure auto-remediation policy
     * Source: [Pulumi Drift Detection](https://www.pulumi.com/docs/pulumi-cloud/deployments/drift/) (accessed 2025-10-25T21:30:36-04:00)
   * CloudFormation: Use AWS Config rule `cloudformation-stack-drift-detection-check` for automated compliance
     * Source: [AWS CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) (accessed 2025-10-25T21:30:36-04:00)
   * driftctl: Run `driftctl scan --filter "Type=='aws_s3_bucket'"` for resource-type scoping
     * Source: [driftctl GitHub](https://github.com/snyk/driftctl) (accessed 2025-10-25T21:30:36-04:00)

3. **Drift impact analysis:**
   * **Security impact:** Check if drift affects IAM, security groups, encryption, network ACLs
   * **Compliance impact:** Map drifted resources to compliance controls (NIST, FedRAMP, PCI-DSS)
   * **Dependency impact:** Identify downstream resources affected by drift
   * **Cost impact:** Calculate cost delta from drift (instance type changes, storage modifications)

4. **Generate remediation plan:**
   ```yaml
   remediation_plan:
     strategy: semi-automated
     steps:
       - action: revert
         resource: aws_security_group.web
         reason: Unauthorized ingress rule added (port 22 from 0.0.0.0/0)
         severity: high
         method: terraform apply
         approval: required
       - action: accept
         resource: aws_instance.app
         reason: Instance type upgraded via console (approved change ticket CHG-123)
         severity: low
         method: terraform import + update code
         approval: auto
       - action: ignore
         resource: aws_s3_bucket.logs
         reason: Tags modified by automation (exemption EXEMPT-456)
         severity: low
         method: add lifecycle ignore_changes
         approval: auto
     estimated_duration: 15min
     rollback_plan: "terraform state backup + manual revert if apply fails"
   ```

5. **Automated remediation execution (if policy allows):**
   * **Pre-flight checks:** Verify no active operations, backup state file
   * **Execute remediation:** Apply IaC changes with `--auto-approve` (if fully-automated) or prompt for approval
   * **Validation:** Run post-remediation drift scan to confirm drift resolved
   * **Logging:** Record remediation action, operator, timestamp, result in audit log

6. **Drift trend analysis:**
   * Track drift frequency over time (daily, weekly, monthly)
   * Identify drift-prone resources or teams
   * Correlate drift with incidents or change tickets
   * Generate compliance dashboard showing drift % by severity

7. **Notification delivery:**
   * Slack: Post drift summary to #infrastructure-alerts with severity emoji
   * Email: Send detailed drift report to platform team with remediation plan
   * Webhook: POST drift JSON to SIEM or compliance platform

**Token budget: ≤6k** (multi-stack scan, impact analysis, remediation plan, notifications)

**Authoritative sources used:**
* [Terraform Cloud Drift Detection Tutorial](https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy) - HashiCorp official docs (accessed 2025-10-25T21:30:36-04:00)
* [Pulumi Drift Detection Docs](https://www.pulumi.com/docs/pulumi-cloud/deployments/drift/) - Pulumi official docs (accessed 2025-10-25T21:30:36-04:00)
* [AWS CloudFormation Drift Detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html) - AWS official docs (accessed 2025-10-25T21:30:36-04:00)
* [driftctl GitHub Repository](https://github.com/snyk/driftctl) - Snyk/driftctl open source tool (accessed 2025-10-25T21:30:36-04:00)
* [Spacelift Drift Detection Guide](https://spacelift.io/blog/drift-detection) - Infrastructure drift best practices (accessed 2025-10-25T21:30:36-04:00)

## Decision Rules

**When to revert drift vs accept drift:**
* **Revert** if: Security resource modified, no change ticket, compliance violation, unauthorized operator
* **Accept** if: Change ticket approved, manual fix during incident, IaC code out of date
* **Ignore** if: Exemption granted, resource lifecycle managed externally, tags/metadata only

**Remediation approval thresholds:**
* **Auto-remediate:** Low severity, pre-approved resource types, non-production environments
* **Require approval:** High/medium severity, production resources, security/network changes
* **Manual only:** Critical infrastructure, multi-region resources, shared services

**Escalation triggers:**
* Drift affects >10 resources: Escalate to platform lead
* Drift unresolved >24h: Create incident ticket
* Repeated drift on same resource >3x: Investigate root cause

**Abort conditions:**
* State file corrupted during remediation: Halt, restore backup, alert on-call
* Cloud provider API errors during apply: Retry with exponential backoff, max 3 attempts
* Dependency conflict detected: Pause remediation, request manual review

## Output Contract

**Required fields:**

```typescript
interface DriftDetectionOutput {
  timestamp: string;              // ISO-8601, NOW_ET
  tool: "terraform" | "cloudformation" | "pulumi" | "driftctl";
  scope: string;                  // stack/workspace name or "all"
  drift_detected: boolean;
  drifted_resources: number;
  resources: DriftedResource[];
  severity_summary: {
    high: number;
    medium: number;
    low: number;
  };
  remediation_plan?: RemediationPlan;
  compliance_impact?: string[];   // Array of violated controls
  trend?: {
    drift_frequency: string;      // "increasing" | "stable" | "decreasing"
    most_drifted_resources: string[];
  };
  audit_log_id?: string;          // Reference to remediation execution log
}

interface DriftedResource {
  id: string;                     // Resource identifier
  type: string;                   // Resource type (aws_security_group, etc.)
  change_type: "added" | "modified" | "deleted";
  severity: "high" | "medium" | "low";
  changed_attributes: {
    attribute: string;
    before: any;
    after: any;
  }[];
  recommended_action: "revert" | "accept" | "ignore";
}

interface RemediationPlan {
  strategy: "manual" | "semi-automated" | "fully-automated";
  steps: RemediationStep[];
  estimated_duration: string;
  rollback_plan: string;
}

interface RemediationStep {
  action: "revert" | "accept" | "ignore";
  resource: string;
  reason: string;
  severity: "high" | "medium" | "low";
  method: string;                 // terraform apply, import, etc.
  approval: "required" | "auto";
}
```

**Example output:** See `/skills/devops-drift-detector/examples/drift-detection-example.txt`

## Examples

```yaml
# Terraform drift detection with semi-automated remediation
input:
  tool: terraform
  workspace: prod-webapp
  remediation_policy: semi-automated

output:
  timestamp: "2025-10-25T21:30:36-04:00"
  tool: terraform
  scope: prod-webapp
  drift_detected: true
  drifted_resources: 2
  resources:
    - id: aws_security_group.web
      type: aws_security_group
      change_type: modified
      severity: high
      changed_attributes:
        - attribute: ingress
          before: [{cidr: "10.0.0.0/8", port: 443}]
          after: [{cidr: "0.0.0.0/0", port: 22}]
      recommended_action: revert
  severity_summary: {high: 1, medium: 0, low: 1}
  remediation_plan:
    strategy: semi-automated
    steps:
      - action: revert
        resource: aws_security_group.web
        approval: required
```

## Quality Gates

**Token budgets enforced:**
* T1 ≤ 2k tokens: Single-stack drift scan with basic remediation guidance
* T2 ≤ 6k tokens: Multi-stack analysis, impact assessment, remediation execution, trend reporting
* T3 not implemented (skill targets T2 complexity)

**Safety checks:**
* [ ] State file backups created before remediation
* [ ] Approval required for high-severity changes
* [ ] Rollback plan documented and validated
* [ ] Audit log captured with operator, timestamp, action

**Auditability:**
* All drift detections logged with timestamp, operator, scope
* Remediation actions recorded with before/after state snapshots
* Compliance violations mapped to controls with evidence trail

**Determinism:**
* Same state file + same cloud state = same drift report
* Drift severity calculated consistently using predefined rules
* Remediation plan generation follows policy-as-code rules

## Resources

**Terraform Drift Detection:**
* [Terraform Cloud Drift Detection Tutorial](https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy)
* [Spacelift Terraform Drift Guide](https://spacelift.io/blog/terraform-drift-detection)

**Pulumi Drift Detection:**
* [Pulumi Drift Detection Docs](https://www.pulumi.com/docs/pulumi-cloud/deployments/drift/)
* [Pulumi Drift Announcement Blog](https://www.pulumi.com/blog/drift-detection/)

**AWS CloudFormation Drift:**
* [CloudFormation Drift Detection User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
* [Automated CloudFormation Drift Remediation](https://aws.amazon.com/blogs/mt/implement-automatic-drift-remediation-for-aws-cloudformation-using-amazon-cloudwatch-and-aws-lambda/)

**driftctl:**
* [driftctl GitHub Repository](https://github.com/snyk/driftctl)
* [Snyk Infrastructure Drift Blog](https://snyk.io/blog/infrastructure-drift-detection-mitigation/)

**Drift Management Best Practices:**
* [Spacelift Drift Management Guide](https://spacelift.io/blog/drift-management)
* [Policy-as-Code for Drift Detection](https://devops.com/cloud-drift-detection-with-policy-as-code/)

**Resource files:**
* `/skills/devops-drift-detector/resources/drift-detection-config.yaml` - Sample drift detection configuration
* `/skills/devops-drift-detector/resources/remediation-workflow.yaml` - Remediation workflow template
* `/skills/devops-drift-detector/resources/compliance-mapping.json` - Drift to compliance control mapping
