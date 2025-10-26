# CISA Zero Trust Maturity Model Assessment Guide

## Overview
This guide provides practical assessment criteria for evaluating zero-trust maturity across the five CISA ZTMM pillars.

Reference: CISA Zero Trust Maturity Model v2.0 (April 2023)
URL: https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf

## Five Pillars and Maturity Levels

### 1. Identity
- **Traditional**: Username/password authentication, no MFA, local accounts
- **Initial**: MFA deployed (SMS/TOTP), centralized IdP (Azure AD/Okta), SSO
- **Advanced**: Phishing-resistant MFA (FIDO2/WebAuthn), risk-based authentication, UBA
- **Optimal**: Continuous authentication, passwordless, biometric integration

### 2. Devices
- **Traditional**: No device inventory, no compliance checks, manual patching
- **Initial**: Device inventory (MDM), antivirus deployed, patch management
- **Advanced**: EDR/XDR deployed, automated compliance enforcement, device posture API
- **Optimal**: Real-time device posture assessment, automated remediation, zero-trust enrollment

### 3. Networks
- **Traditional**: Flat network, perimeter firewall only, unencrypted internal traffic
- **Initial**: VLANs/VPCs, basic segmentation, TLS for external traffic
- **Advanced**: Micro-segmentation, mTLS for service-to-service, encrypted DNS
- **Optimal**: SDP, application-layer segmentation, AI-driven traffic analysis

### 4. Applications and Workloads
- **Traditional**: Shared credentials, no app-level authN/authZ, static permissions
- **Initial**: App-level authentication, API keys, basic RBAC
- **Advanced**: OAuth2/OIDC, service mesh with mTLS, dynamic RBAC
- **Optimal**: Dynamic policy enforcement, RASP, runtime threat detection

### 5. Data
- **Traditional**: No data classification, unencrypted data at rest, no DLP
- **Initial**: Data classification scheme, encryption at rest, basic access logs
- **Advanced**: Encryption in transit and at rest, field-level encryption, DLP deployed
- **Optimal**: Continuous data monitoring, encrypted compute (confidential computing), homomorphic encryption

## Assessment Methodology

1. Review current capabilities for each pillar
2. Score against maturity definitions (Traditional → Optimal)
3. Identify gaps between current and target maturity
4. Prioritize remediations (focus on "Traditional" pillars first)
5. Develop phased roadmap aligned with business objectives

## Cross-Cutting Capabilities (per CISA ZTMM v2.0)

1. **Visibility and Analytics**: Comprehensive logging, SIEM integration, UBA
2. **Automation and Orchestration**: Automated policy enforcement, SOAR integration
3. **Governance**: Policy management, compliance reporting, risk management
