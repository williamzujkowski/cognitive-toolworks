# Migration Guide: compliance-automation-engine Skill → compliance-orchestrator Agent

**Date**: 2025-10-26T01:33:55-04:00
**Status**: Complete
**Old Location**: `/skills/compliance-automation-engine/SKILL.md` (DEPRECATED)
**New Location**: `/agents/compliance-orchestrator/AGENT.md` (ACTIVE)

## Overview

The `compliance-automation-engine` skill has been refactored into a proper **compliance-orchestrator** agent following CLAUDE.md v1.0.0 standards. This migration reduces procedural complexity, enforces proper orchestration patterns, and aligns with the agent-as-orchestrator design principle for multi-step compliance workflows.

## What Changed

### Architecture
- **Before**: 15-step procedural skill (T1: 2 steps, T2: 7 steps, T3: 8 steps) - violated skill principles (>2 steps)
- **After**: 4-step orchestration agent (Discovery → Assessment → Synthesis → Validation)

### Invocation
- **Before** (skill): Model-invoked via natural language
  ```
  "Use the compliance-automation-engine skill to prepare FedRAMP Moderate ATO"
  ```
- **After** (agent): User-invoked via orchestrator command
  ```
  orchestrator use compliance-orchestrator \
    --framework fedramp-moderate \
    --control-baseline moderate \
    --evidence-path /compliance/evidence \
    --validation-mode comprehensive
  ```

### System Prompt
- **Before**: Embedded in 15-step procedure (mixed with implementation details, 11,500+ tokens total)
- **After**: Dedicated 1,347-token system prompt (≤1500 limit, focused on orchestration)

### Token Efficiency
- **Before**: T1≤2000, T2≤6000, T3≤12000 (loaded all tiers together, heavy front-loading)
- **After**: Progressive disclosure via agent workflow (load only what's needed per step)

### Workflow Simplification
- **Before**:
  - T1: Load baseline → Scan evidence → Calculate metrics → Report
  - T2: T1 + Load catalog → Map evidence → Assess status → Generate SSP → Remediation plan → Output
  - T3: T2 + Multi-framework mapping → Deep validation → Inheritance analysis → Full OSCAL suite → Monitoring design → Dashboard → Cross-framework report
- **After**:
  - Step 1 (Discovery): Validate inputs, load catalogs, scan evidence, determine scope
  - Step 2 (Assessment): Map evidence, validate completeness, analyze gaps, calculate metrics
  - Step 3 (Synthesis): Generate reports, create OSCAL artifacts, design remediation plan
  - Step 4 (Validation): Schema validation, cross-reference checks, safety scans, audit trail

## Migration Steps

### For Users

1. **Update invocation syntax**:
   ```bash
   # Old (deprecated)
   claude "Use compliance-automation-engine skill for FedRAMP Moderate assessment"

   # New (recommended)
   orchestrator use compliance-orchestrator \
     --framework fedramp-moderate \
     --control-baseline moderate \
     --evidence-path /compliance/fedramp-mod/evidence \
     --system-context @system_context.json \
     --validation-mode comprehensive
   ```

2. **Prepare system context file** (JSON):
   ```json
   {
     "system_name": "Cloud SaaS Platform",
     "system_id": "CSP-001",
     "boundary_description": "AWS GovCloud VPC with web/app/db tiers",
     "authorization_boundary": "All components in VPC vpc-abc123"
   }
   ```

3. **Expect structured 4-step workflow**:
   - Step 1: Discovery & Requirements (validates inputs, loads catalogs)
   - Step 2: Assessment & Analysis (maps evidence, identifies gaps)
   - Step 3: Synthesis & Generation (creates OSCAL artifacts, remediation plan)
   - Step 4: Validation & Finalization (schema checks, safety scans)

4. **Review outputs in structured format**:
   ```
   /output/
     compliance_report.json        # Summary, gaps, metrics
     oscal_ssp.json                # System Security Plan (T2+)
     oscal_sap.json                # Security Assessment Plan (T3)
     oscal_sar.json                # Security Assessment Report (T3)
     oscal_poam.json               # Plan of Action & Milestones (T3, if gaps)
     remediation_plan.md           # Prioritized action items
     dashboard_schema.json         # Continuous monitoring design (T3)
   ```

### For Developers

1. **Update references**:
   - Change skill slug: `compliance-automation-engine` → `compliance-orchestrator`
   - Update invocation patterns from skill to orchestrator syntax
   - Reference new location: `/agents/compliance-orchestrator/AGENT.md`

2. **Review output contract changes**:
   - **Old output**: Single `compliance_report` JSON with nested OSCAL artifacts
   - **New output**: Separate files per artifact type (easier CI/CD integration)
   - **Metadata**: Now includes `timestamp` (NOW_ET), `assessment_tier`, `validation_status`

3. **Update parameter names** (aligned with CLAUDE.md conventions):
   - `framework` (unchanged)
   - `control_baseline` (unchanged)
   - `evidence_path` (unchanged)
   - `system_context` (now expects JSON object or file path)
   - `validation_mode` → maps to tier selection (quick=T1, standard=T2, comprehensive=T3)

4. **Skills integration**:
   - Agent now delegates to `oscal-ssp-validate` for schema validation
   - Agent references `security-assessment-framework` for security domain assessments
   - Use Task tool for skill delegation (not direct invocation)

## Key Improvements

### Compliance with CLAUDE.md
- ✓ Agent follows §2 repository layout (`/agents/<slug>/`)
- ✓ System prompt ≤1500 tokens (§3 agent requirements)
- ✓ 8 required sections in correct order
- ✓ Examples ≤30 lines each
- ✓ Tools restricted to approved MCP list
- ✓ Progressive disclosure (workflows/ for detailed procedures)

### Better Orchestration
- ✓ 4-step workflow with clear decision points
- ✓ Error handling: emit TODO lists, warn on issues, halt on critical failures
- ✓ Multi-framework support with NIST CSF pivot for control mapping
- ✓ Skill delegation patterns (oscal-ssp-validate, security-assessment-framework)
- ✓ Progressive tier escalation (T1 → T2 → T3 based on validation_mode)

### Enhanced Validation
- ✓ Pre-flight checks: framework validity, baseline requirements, evidence path accessibility
- ✓ OSCAL schema validation against official 1.1.2+ schemas
- ✓ Evidence freshness checks (>90 days warning, >365 days error)
- ✓ Coverage thresholds (<80% warning, <70% error)
- ✓ Critical gap detection (AC, IA, SC families = ATO blockers)
- ✓ Safety scans (no secrets, PII, or fabricated data)

### Quality Gates
- **Coverage thresholds**: warn <80%, error <70%
- **Evidence age**: warn >90 days, error >365 days
- **Critical gaps**: AC-1, AC-2, IA-2, IA-5, SC-7, SC-8 = ATO blockers
- **OSCAL validation**: Must pass schema validation before output
- **Audit trail**: All timestamps use NOW_ET (America/New_York, ISO-8601)

## Backward Compatibility

The deprecated `/skills/compliance-automation-engine/SKILL.md` will:
- Remain in repository for historical reference
- Display deprecation notice in frontmatter and Purpose section
- Redirect users to new agent location (`/agents/compliance-orchestrator/AGENT.md`)
- Not receive updates or bug fixes

**Timeline**:
- 2025-10-26: compliance-orchestrator v1.0.0 released, compliance-automation-engine deprecated
- 2025-11-26: Warning period (30 days) — both available
- 2025-12-26: compliance-automation-engine skill may be archived or removed

## Input/Output Mapping

### Inputs (comparison)

| Old Skill Parameter | New Agent Parameter | Notes |
|---------------------|---------------------|-------|
| `framework` | `framework` | Unchanged |
| `control_baseline` | `control_baseline` | Unchanged |
| `evidence_path` | `evidence_path` | Unchanged |
| `system_context` | `system_context` | Now expects JSON object or file path |
| `validation_mode` | `validation_mode` | Maps to tier: quick=T1, standard=T2, comprehensive=T3 |

### Outputs (comparison)

| Old Skill Output | New Agent Output | Location |
|------------------|------------------|----------|
| `compliance_report` | `compliance_report.json` | /output/compliance_report.json |
| `oscal_artifacts.ssp` | `oscal_ssp.json` | /output/oscal_ssp.json (T2+) |
| `oscal_artifacts.sap` | `oscal_sap.json` | /output/oscal_sap.json (T3) |
| `oscal_artifacts.sar` | `oscal_sar.json` | /output/oscal_sar.json (T3) |
| `oscal_artifacts.poam` | `oscal_poam.json` | /output/oscal_poam.json (T3, if gaps) |
| `remediation_plan` | `remediation_plan.md` | /output/remediation_plan.md |
| `dashboard_data` | `dashboard_schema.json` | /output/dashboard_schema.json (T3) |

## Example Comparison

### Old Skill Invocation (Natural Language)
```
User: "Use the compliance-automation-engine skill to assess FedRAMP Moderate compliance for my system. Evidence is in /compliance/evidence and I need a comprehensive assessment with OSCAL artifacts."

Skill response: [Executes 15-step T3 procedure, outputs single compliance_report JSON]
```

### New Agent Invocation (Orchestrator Command)
```bash
orchestrator use compliance-orchestrator \
  --framework fedramp-moderate \
  --control-baseline moderate \
  --evidence-path /compliance/evidence \
  --system-context @/compliance/system_context.json \
  --validation-mode comprehensive

# Agent executes 4-step workflow:
# Step 1 (Discovery): Validates inputs, loads 325 controls, scans 847 evidence files
# Step 2 (Assessment): Maps evidence to controls, identifies 8 gaps (3 critical)
# Step 3 (Synthesis): Generates SSP, SAP, SAR, POA&M, remediation plan, dashboard schema
# Step 4 (Validation): Validates OSCAL artifacts against schemas, safety scans, audit trail

# Outputs:
# /output/compliance_report.json       (metadata, summary, 95.4% coverage)
# /output/oscal_ssp.json               (245KB, 325 controls)
# /output/oscal_sap.json               (180KB, assessment plan)
# /output/oscal_sar.json               (assessment results)
# /output/oscal_poam.json              (8 open items)
# /output/remediation_plan.md          (prioritized, 4-6 week timeline)
# /output/dashboard_schema.json        (15 metrics, alerting thresholds)
```

## Testing

To verify the migration:

```bash
# Test new agent invocation
orchestrator use compliance-orchestrator \
  --framework fedramp-moderate \
  --control-baseline moderate \
  --evidence-path /path/to/test/evidence \
  --system-context @system_context.json \
  --validation-mode standard

# Verify output structure
ls -la /output/
# Should contain: compliance_report.json, oscal_ssp.json, remediation_plan.md

# Check agents-index.json
cat /index/agents-index.json | jq '.[] | select(.slug == "compliance-orchestrator")'

# Validate OSCAL artifacts (if generated)
oscal-cli ssp validate /output/oscal_ssp.json

# Manual validation (if tooling/validate_agent.py not available)
python -c "
import json
with open('/agents/compliance-orchestrator/AGENT.md') as f:
    content = f.read()
    assert 'slug: \"compliance-orchestrator\"' in content
    assert 'version: \"1.0.0\"' in content
    print('✓ Agent metadata valid')
"
```

## Troubleshooting

**Problem**: "orchestrator command not found"
- **Solution**: Ensure Claude Code CLI is updated to version supporting sub-agents

**Problem**: "compliance-orchestrator not found in index"
- **Solution**: Verify `/index/agents-index.json` contains compliance-orchestrator entry

**Problem**: "System context validation failed"
- **Solution**: Ensure system_context JSON includes required fields: system_name, system_id, boundary_description, authorization_boundary

**Problem**: "OSCAL schema validation failed"
- **Solution**: Check OSCAL artifact for schema errors using `oscal-cli` or review validation report

**Problem**: "Evidence path inaccessible"
- **Solution**: Verify path exists and is readable; agent will warn and proceed with gap-only analysis

**Problem**: "Still seeing references to compliance-automation-engine skill"
- **Solution**: Update code/docs to use new compliance-orchestrator agent slug

## Resources

- **New Agent Spec**: `/agents/compliance-orchestrator/AGENT.md`
- **Old Skill (deprecated)**: `/skills/compliance-automation-engine/SKILL.md`
- **CLAUDE.md Standards**: `/CLAUDE.md` (§2 layout, §3 agent requirements)
- **Workflow Procedures**: `/agents/compliance-orchestrator/workflows/` (detailed steps)
- **Example**: `/agents/compliance-orchestrator/examples/fedramp-ato-preparation.txt`

## Questions?

For issues or questions about this migration:
1. Check `/agents/compliance-orchestrator/CHANGELOG.md` for version history
2. Review `/agents/compliance-orchestrator/workflows/` for detailed workflow procedures
3. Consult CLAUDE.md §2-§3 for authoritative agent standards
4. Open issue in repository with `migration` label

---

**Migration Approved**: 2025-10-26T01:33:55-04:00
**Reviewed By**: cognitive-toolworks
**Status**: ✓ Complete
