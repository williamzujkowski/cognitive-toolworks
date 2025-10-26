# Agent Design Checklist

Use this checklist when designing new Claude Code agents to ensure CLAUDE.md compliance and production readiness.

## Phase 1: Requirements Gathering

- [ ] **Topic validation**: Does this require ≥3 steps? (If <3, recommend skill instead)
- [ ] **Capabilities defined**: List 3-7 core capabilities
- [ ] **Tool requirements**: Identify which MCP tools are needed (default: Read, Write, Bash, Grep, Glob)
- [ ] **Constraints captured**: Token budgets, response times, external dependencies
- [ ] **Slug uniqueness**: Check `/index/agents-index.json` for duplicates
- [ ] **NOW_ET computed**: `env TZ=America/New_York date +"%Y-%m-%dT%H:%M:%S%z"`

## Phase 2: System Prompt Design

- [ ] **Persona defined**: Clear role/expertise statement (1-2 sentences)
- [ ] **Objectives listed**: 3-5 core responsibilities
- [ ] **Decision rules**: When to use each tool, workflow branching logic
- [ ] **Quality gates**: Success criteria, validation checkpoints
- [ ] **Token budget**: Measure draft prompt (must be ≤1500 tokens)
  - **Estimation**: ~4 chars per token → 6000 chars max
  - **Actual count**: Use `wc -c` or token counter
- [ ] **Skills referenced**: By slug only, never full content
- [ ] **CLAUDE.md reminders**: Enforcement notes for compliance

**Token reduction strategies** (if >1500):
- Extract verbose workflows to `/agents/<slug>/workflows/*.md`
- Move detailed examples to `/agents/<slug>/examples/`
- Replace long lists with references to Resources section
- Consolidate decision rules into bullet points

## Phase 3: Specification Generation

### Frontmatter
- [ ] `name`: Human-readable title
- [ ] `slug`: Unique kebab-case identifier
- [ ] `description`: ≤160 characters, clear value proposition
- [ ] `model`: "inherit" (or specify: sonnet/opus/haiku)
- [ ] `tools`: Array of MCP-approved tools
- [ ] `persona`: One-line role statement
- [ ] `version`: "1.0.0" (semantic versioning)
- [ ] `owner`: "cognitive-toolworks"
- [ ] `license`: "Apache-2.0"
- [ ] `keywords`: 4-8 relevant terms
- [ ] `security`: pii=none, secrets=never, audit=sources+NOW_ET
- [ ] `links.docs`: 2-4 authoritative URLs

### Required Sections (in order)
1. [ ] **Purpose & When-To-Use**: Trigger patterns, agent vs skill decision
2. [ ] **System Prompt**: Persona + objectives + decision rules (≤1500 tokens)
3. [ ] **Tool Usage Guidelines**: Which tools, when, why, decision rules
4. [ ] **Workflow Patterns**: Multi-step procedures with branching logic
5. [ ] **Skills Integration**: Referenced by slug, invocation patterns
6. [ ] **Examples**: 1-2 interaction scenarios (≤30 lines each)
7. [ ] **Quality Gates**: Pre/post checks, success metrics
8. [ ] **Resources**: Links only (no long pastes), with access dates

### Supporting Files
- [ ] `/agents/<slug>/examples/<slug>-example.txt`: ≤30 lines
- [ ] `/agents/<slug>/CHANGELOG.md`: v1.0.0 with design decisions
- [ ] `/agents/<slug>/workflows/*.md`: Optional detailed procedures
- [ ] `.gitkeep` in empty directories

## Phase 4: Validation & Indexing

### Pre-flight Checks
- [ ] **Frontmatter valid**: All required keys present
- [ ] **Description length**: ≤160 characters
- [ ] **System prompt tokens**: ≤1500 (hard limit)
- [ ] **Section order**: All 8 sections in correct sequence
- [ ] **Examples length**: ≤30 lines each
- [ ] **Tools valid**: All in MCP approved list
- [ ] **No secrets**: Scan for API keys, tokens, credentials
- [ ] **Citations (T2+)**: 2-4 sources with titles + URLs + NOW_ET
- [ ] **Slug unique**: No duplicates in agents-index.json

### Index Entry
```json
{
  "slug": "<slug>",
  "name": "<name>",
  "description": "<description ≤160 chars>",
  "keywords": ["kw1", "kw2", ...],
  "model": "inherit",
  "tools": ["Read", "Write", ...],
  "version": "1.0.0",
  "owner": "cognitive-toolworks",
  "entry": "agents/<slug>/AGENT.md"
}
```
- [ ] Entry added to `/index/agents-index.json`
- [ ] JSON valid (no trailing commas, proper escaping)
- [ ] Deterministic ordering (sort by slug)

### Test Scenarios (T3)
- [ ] **Happy path**: Multi-step success scenario
- [ ] **Missing input**: Graceful degradation with TODO list
- [ ] **Tool failure**: Error handling and recovery
- [ ] **Edge case**: Boundary conditions (max tokens, unavailable tools)
- [ ] **Skills integration**: Verify skill invocations work
- [ ] Saved to `/tests/evals_agent_<slug>.yaml`

### Documentation
- [ ] **Migration guide**: How to invoke agent (vs old skill if applicable)
- [ ] **Invocation syntax**: `orchestrator use <slug> [args]`
- [ ] **Example commands**: 2-3 common use cases

## Phase 5: Post-Creation

- [ ] **Validation script**: Run `tooling/validate_agent.py` (if exists)
- [ ] **Lint check**: Verify links resolve, no dead URLs
- [ ] **Token audit**: Re-measure system prompt with official counter
- [ ] **Deprecation**: If migrating from skill, add deprecation notice to old SKILL.md
- [ ] **CI pipeline**: Ensure agents-ci.yaml runs successfully
- [ ] **Manual test**: Invoke agent with sample request, verify outputs

## Common Pitfalls to Avoid

- **Token bloat**: System prompts >1500 tokens (extract to workflows/)
- **Tool sprawl**: Requesting too many tools (default to minimal set)
- **Pasting skills**: Including full SKILL.md content (reference by slug only)
- **Vague persona**: Generic "helpful assistant" (be specific: "Senior DevOps engineer...")
- **Missing decision rules**: Ambiguous tool selection (when/why each tool)
- **No error handling**: Workflows without abort conditions
- **Fabricated specs**: Guessing at API signatures (mark [TODO] instead)
- **Long examples**: >30 lines (move to examples/ directory)
- **Uncited claims**: Version numbers without sources (link to docs)
- **Duplicate slugs**: Collisions with existing agents (check index first)

## Agent vs Skill Decision Matrix

| Criterion | Agent | Skill |
|-----------|-------|-------|
| Steps | ≥3 | 1-2 |
| Context | Separate window | Shared with main |
| Invocation | User explicit | Model implicit |
| State | Stateful workflows | Stateless transforms |
| Orchestration | Yes (multi-skill) | No (single capability) |
| Examples | Security auditor, Cost analyzer | Time normalization, JSON validation |

## Token Estimation Quick Reference

- **1 token ≈ 4 characters** (rough estimate for English text)
- **1500 tokens ≈ 6000 characters**
- **Line count**: Typical line ≈ 60-80 chars → ~75 lines max for system prompt
- **Tool**: Use `wc -c` for character count, divide by 4 for token estimate
- **Accuracy**: Final validation should use tiktoken cl100k_base encoder

---

**Last Updated**: 2025-10-26T01:19:05-04:00
**Audit Cadence**: Review checklist every 90 days or after 5 agent creations
