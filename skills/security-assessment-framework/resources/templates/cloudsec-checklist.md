# Cloud Security Assessment Checklist

## AWS Security Checklist

### Identity & Access Management (IAM)
- [ ] Root account MFA enabled
- [ ] IAM users have individual accounts (no shared)
- [ ] Least privilege principle applied
- [ ] IAM password policy enforced
- [ ] Access keys rotated regularly
- [ ] IAM roles used instead of access keys where possible

### Storage Security
- [ ] S3 buckets not publicly accessible (unless explicitly required)
- [ ] S3 bucket encryption enabled
- [ ] S3 versioning enabled for critical data
- [ ] EBS volumes encrypted
- [ ] RDS encryption at rest enabled

### Network Security
- [ ] Security groups follow least privilege
- [ ] Default VPC not used for production
- [ ] Network ACLs configured
- [ ] VPC Flow Logs enabled
- [ ] CloudTrail logging enabled

### Compute Security
- [ ] EC2 instances not publicly accessible (unless required)
- [ ] Instance metadata service v2 (IMDSv2) enforced
- [ ] Systems Manager for patch management
- [ ] Security groups restrict SSH/RDP access

## Azure Security Checklist

### Identity
- [ ] Azure AD MFA enforced
- [ ] Conditional Access policies configured
- [ ] Privileged Identity Management (PIM) enabled
- [ ] RBAC least privilege applied

### Storage & Data
- [ ] Storage account encryption enabled
- [ ] Blob storage not publicly accessible
- [ ] Azure Key Vault for secrets management
- [ ] SQL TDE (Transparent Data Encryption) enabled

### Network
- [ ] Network Security Groups (NSGs) configured
- [ ] Azure Firewall or NVA deployed
- [ ] DDoS Protection Standard enabled
- [ ] VNet service endpoints used

## GCP Security Checklist

### IAM & Access
- [ ] Organization policies enforced
- [ ] Service accounts use minimal permissions
- [ ] Cloud IAM conditions used
- [ ] VPC Service Controls implemented

### Data Protection
- [ ] Cloud KMS for encryption
- [ ] Cloud Storage bucket permissions reviewed
- [ ] BigQuery dataset access controls
- [ ] Cloud SQL encryption enabled

### Network Security
- [ ] VPC firewall rules follow least privilege
- [ ] Cloud Armor (WAF) configured
- [ ] Private Google Access enabled
- [ ] VPC Flow Logs enabled

## Cloud Security Alliance (CSA) Domains
- [ ] Governance & Risk Management
- [ ] Legal & Compliance
- [ ] Information Governance
- [ ] Audit Assurance & Compliance
