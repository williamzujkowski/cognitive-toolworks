# Changelog

All notable changes to the Incident Response Playbook Generator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of incident-response-playbook-generator skill
- NIST SP 800-61 Rev 2 compliant playbook generation
- Support for security incidents, outages, and disaster recovery scenarios
- Escalation matrix templates with severity-based thresholds
- Post-mortem templates with 5 Whys root cause analysis
- Compliance integration for HIPAA, SOC2, PCI-DSS, FedRAMP
- Service-specific runbook generation (T2 tier)
- Communication plan templates for internal and external stakeholders
- Two-tier implementation: T1 (template, ≤2k tokens) and T2 (detailed, ≤6k tokens)
- Integration with security-assessment-framework for security incidents
- Examples for data breach, outage, and disaster recovery scenarios
- Resource templates: playbook, escalation matrix, post-mortem, runbook

### Sources
- NIST SP 800-61 Rev 2 (accessed 2025-10-25T21:30:36-04:00)
- Atlassian Incident Management (accessed 2025-10-25T21:30:36-04:00)
- PagerDuty Incident Response (accessed 2025-10-25T21:30:36-04:00)
- SANS Incident Handler's Handbook (accessed 2025-10-25T21:30:36-04:00)
- Google SRE Book (accessed 2025-10-25T21:30:36-04:00)

### Compliance
- HIPAA Breach Notification (60-day requirement)
- PCI DSS v4.0 Requirement 12.10 (incident response)
- SOC2 CC7.3 (incident communications)
- FedRAMP IR-4 and IR-6 controls (NIST SP 800-53 Rev 5)
