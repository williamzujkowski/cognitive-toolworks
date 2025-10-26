# Migration Guide: agent-creation Skill → agent-creator Agent

**Date**: 2025-10-26T01:19:05-04:00
**Status**: Complete
**Old Location**: `/skills/agent-creation/SKILL.md` (DEPRECATED)
**New Location**: `/agents/agent-creator/AGENT.md` (ACTIVE)

## Overview

The `agent-creation` skill has been refactored into a proper **agent-creator** agent following CLAUDE.md v1.1.0 standards. This migration reduces system prompt bloat, enforces proper orchestration patterns, and aligns with the agent-as-orchestrator design principle.

## What Changed

### Architecture
- **Before**: 15-step procedural skill (violated skill principles: too complex, >3 steps)
- **After**: 4-step orchestration agent (Research → Design → Generate → Validate)

### Invocation
- **Before** (skill): Model-invoked via natural language
  ```
  "Use the agent-creation skill to build a security auditor"
  ```
- **After** (agent): User-invoked via orchestrator command
  ```
  orchestrator use agent-creator --topic "security auditor for multi-tier apps"
  ```

### System Prompt
- **Before**: Embedded in 15-step procedure (mixed with implementation details)
- **After**: Dedicated 518-token system prompt (≤1500 limit, focused on orchestration)

### Token Efficiency
- **Before**: T1≤2000, T2≤6000, T3≤12000 (loaded all tiers together)
- **After**: Progressive disclosure via agent workflow (load only what's needed per step)

## Migration Steps

### For Users

1. **Update invocation syntax**:
   ```bash
   # Old (deprecated)
   claude "Use the agent-creation skill to create an agent for [topic]"

   # New (recommended)
   orchestrator use agent-creator --topic "[topic]" --capabilities "[cap1, cap2]"
   ```

2. **Use explicit parameters** (optional but recommended):
   ```bash
   orchestrator use agent-creator \
     --topic "Security audit orchestrator" \
     --capabilities "vulnerability scanning, compliance checking, report generation" \
     --tools "Read, Bash, Grep, Task"
   ```

3. **Expect structured workflow**:
   - Step 1: Research & Requirements (validates agent vs skill decision)
   - Step 2: Design System Prompt (token budget enforcement)
   - Step 3: Generate Specification (AGENT.md + examples + CHANGELOG)
   - Step 4: Validate & Index (quality gates + agents-index.json update)

### For Developers

1. **Update references**:
   - Change skill slug references from `agent-creation` → `agent-creator`
   - Update invocation patterns from skill to orchestrator syntax
   - Reference new location: `/agents/agent-creator/AGENT.md`

2. **Review output contract**:
   - Old: Returned `agent_folder` + `index_entry` + `validation_results`
   - New: Same structure, but with stricter validation gates

3. **Check token budgets**:
   - System prompts now strictly ≤1500 tokens (measured, not estimated)
   - Examples strictly ≤30 lines (enforced)
   - Description strictly ≤160 chars (enforced)

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
- ✓ Error handling for missing inputs (TODO lists + stop)
- ✓ Token overflow handling (extract to workflows/)
- ✓ Skill integration patterns (reference by slug only)

### Enhanced Validation
- ✓ Pre-flight checks (agent vs skill decision, tool availability)
- ✓ Token counting (character count → token estimate)
- ✓ Citation verification (NOW_ET timestamps required)
- ✓ Index entry validation (no duplicate slugs)

## Backward Compatibility

The deprecated `/skills/agent-creation/SKILL.md` will:
- Remain in repository for historical reference
- Display deprecation notice in frontmatter and Purpose section
- Redirect users to new agent location
- Not receive updates or bug fixes

**Timeline**:
- 2025-10-26: agent-creator v1.0.0 released, agent-creation deprecated
- 2025-11-26: Warning period (30 days) — both available
- 2025-12-26: agent-creation skill may be archived or removed

## Testing

To verify the migration:

```bash
# Test new agent invocation
orchestrator use agent-creator --topic "Test agent for demo purposes"

# Verify output structure
ls -la /agents/test-agent/
# Should contain: AGENT.md, examples/, workflows/, CHANGELOG.md

# Check agents-index.json
cat /index/agents-index.json | jq '.[] | select(.slug == "test-agent")'

# Validate against CLAUDE.md standards
python tooling/validate_agent.py /agents/test-agent/AGENT.md
```

## Troubleshooting

**Problem**: "orchestrator command not found"
- **Solution**: Ensure Claude Code CLI is updated to version supporting sub-agents

**Problem**: "agent-creator not found in index"
- **Solution**: Verify `/index/agents-index.json` contains agent-creator entry

**Problem**: "System prompt exceeds 1500 tokens"
- **Solution**: Agent will auto-extract verbose details to workflows/; check output

**Problem**: "Still seeing references to agent-creation skill"
- **Solution**: Update code/docs to use new agent-creator slug

## Resources

- **New Agent Spec**: `/agents/agent-creator/AGENT.md`
- **Old Skill (deprecated)**: `/skills/agent-creation/SKILL.md`
- **CLAUDE.md Standards**: `/CLAUDE.md` (§2 layout, §3 agent requirements)
- **Agent Design Checklist**: `/agents/agent-creator/workflows/agent-design-checklist.md`
- **Example**: `/agents/agent-creator/examples/security-auditor-creation.txt`

## Questions?

For issues or questions about this migration:
1. Check `/agents/agent-creator/CHANGELOG.md` for version history
2. Review `/agents/agent-creator/workflows/agent-design-checklist.md` for design patterns
3. Consult CLAUDE.md §2-§3 for authoritative agent standards
4. Open issue in repository with `migration` label

---

**Migration Approved**: 2025-10-26T01:19:05-04:00
**Reviewed By**: cognitive-toolworks
**Status**: ✓ Complete
