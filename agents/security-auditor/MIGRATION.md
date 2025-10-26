# Migration Guide: security-assessment-framework → security-auditor

## Overview

The `security-assessment-framework` skill has been decomposed into:
- **8 focused skills** (one per security domain)
- **1 orchestrator agent** (`security-auditor`) that coordinates the skills

This migration guide helps users transition from the monolithic skill to the new modular architecture.

---

## What Changed

### Before (Monolithic Skill)
```yaml
# Single skill invocation
skill: security-assessment-framework
inputs:
  target_system: "my-app"
  security_domains: ["appsec", "cloudsec", "iam"]
  assessment_tier: "T2"
```

### After (Agent + Skills)

**Option 1: Use orchestrator agent for multi-domain assessments**
```yaml
# Agent invocation (recommended for 2+ domains)
agent: security-auditor
inputs:
  target_system: "my-app"
  security_domains: ["appsec", "cloudsec", "iam"]
  assessment_tier: "T2"
```

**Option 2: Use individual skills for single-domain assessments**
```yaml
# Direct skill invocation (for single domain)
skill: appsec-validator
inputs:
  application_identifier: "my-app"
  assessment_scope: "web-app"
  check_level: "standard"
```

---

## Mapping: Old Domains → New Skills

| Old Domain | New Skill Slug | Use When |
|------------|----------------|----------|
| appsec | appsec-validator | Assessing web apps, APIs, mobile backends |
| cloudsec | cloudsec-posture-analyzer | Assessing AWS, Azure, GCP infrastructure |
| containersec | container-security-checker | Assessing Docker, Kubernetes, containers |
| cryptosec | cryptosec-validator | Assessing TLS, certificates, encryption |
| iam | iam-security-reviewer | Assessing identity, authentication, authorization |
| networksec | networksec-architecture-validator | Assessing firewalls, segmentation, VPNs |
| ossec | ossec-hardening-checker | Assessing OS hardening, patching |
| zerotrust | zerotrust-maturity-assessor | Assessing zero-trust maturity |

---

## Input Mapping

### Old Skill Inputs
```yaml
target_system: "string"
security_domains: ["array"]
assessment_tier: "T1|T2|T3"
compliance_frameworks: ["array"]
threat_model_required: true/false
```

### New Agent Inputs (Same Interface!)
```yaml
target_system: "string"
security_domains: ["array"] # optional, auto-detect if empty
assessment_tier: "T1|T2|T3"
compliance_frameworks: ["array"] # optional
threat_model_required: true/false # optional
```

**No changes required for agent usage!** The interface is backward-compatible.

### New Individual Skill Inputs

Each skill has domain-specific inputs. Examples:

**appsec-validator:**
```yaml
application_identifier: "my-app"
assessment_scope: "web-app|api|mobile-backend"
check_level: "critical-only|standard|comprehensive"
```

**cloudsec-posture-analyzer:**
```yaml
cloud_platform: "aws|azure|gcp"
resource_scope: "storage|iam|network|compute|all"
compliance_check: "cis|well-architected|both|none"
```

**iam-security-reviewer:**
```yaml
identity_provider: "corporate-idp"
iam_scope: "authentication|authorization|accounts|all"
authenticator_level: "AAL1|AAL2|AAL3" # optional
```

See individual skill SKILL.md files for complete input specifications.

---

## Output Format Changes

### Agent Output (Multi-Domain)
The agent aggregates findings from multiple skills:

```json
{
  "assessment_metadata": {
    "target_system": "string",
    "assessment_tier": "T1|T2|T3",
    "domains_assessed": ["list"]
  },
  "overall_risk": "critical|high|medium|low",
  "domain_findings": {
    "appsec": { "findings": [], "risk": "..." },
    "cloudsec": { "..." }
  },
  "aggregated_findings": [
    {
      "id": "unified-finding-id",
      "domains": ["appsec", "iam"],
      "severity": "high",
      "cvss_score": 8.1,
      "remediation": "..."
    }
  ],
  "remediation_roadmap": {
    "quick_wins": ["0-30 days"],
    "short_term": ["30-90 days"],
    "long_term": ["90+ days"]
  }
}
```

### Individual Skill Output
Each skill returns domain-specific findings:

```json
{
  "application_identifier": "my-app",
  "findings": [
    {
      "id": "APPSEC-001",
      "owasp_category": "A01:2021",
      "severity": "high",
      "cvss_score": 8.1,
      "remediation": "..."
    }
  ],
  "summary": {
    "critical_count": 0,
    "high_count": 1
  }
}
```

---

## When to Use What

### Use security-auditor agent when:
- Assessing 2+ security domains
- Need cross-domain risk aggregation
- Need unified remediation roadmap
- Compliance mapping across multiple domains
- Threat modeling required (T3)

### Use individual skills when:
- Assessing single security domain
- Need domain-specific deep dive
- Integrating into automated pipelines (one domain at a time)
- Token budget constraints (skills use fewer tokens)

---

## Breaking Changes

### 1. Removed Features
- Monolithic skill no longer accepts single-domain assessments efficiently
- Old skill deprecated (use agent or individual skills)

### 2. New Features (Enhancements)
- Parallel skill execution for faster multi-domain assessments
- More granular control over individual domain assessments
- Improved token efficiency (invoke only needed skills)
- Better modularity and testability

---

## Migration Checklist

- [ ] Review your current usage of `security-assessment-framework`
- [ ] Identify if you need multi-domain (agent) or single-domain (skill) assessments
- [ ] Update invocation to use `security-auditor` agent OR specific skill
- [ ] Verify input mappings (agent inputs are backward-compatible)
- [ ] Update output parsing if using programmatic access
- [ ] Test assessment workflows in non-production environment
- [ ] Update documentation and runbooks

---

## Rollback Plan

If you encounter issues with the new architecture:

1. The old `security-assessment-framework` skill is deprecated but still available (read-only)
2. File an issue describing the problem
3. Temporarily revert to old skill if critical path
4. We will assist with migration debugging

---

## Support

For migration questions or issues:
- Check individual skill documentation: `/skills/<skill-slug>/SKILL.md`
- Check agent documentation: `/agents/security-auditor/AGENT.md`
- Review examples in `/agents/security-auditor/examples/`

---

## Timeline

- **2025-10-26:** New skills and agent released (v1.0.0)
- **2025-10-26:** Old skill deprecated with migration notice
- **2026-01-26:** Old skill archived (90-day deprecation period)
