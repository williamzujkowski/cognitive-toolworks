# cognitive-toolworks

31 production-ready Skills and agent-creation infrastructure for Claude CLI. No fluff.

## What This Is

A library of small, composable **Skills** and **Agent** specifications using Anthropic's SKILL.md format. Each component is:
- **Focused**: Does one thing, does it right
- **Tiered**: T1 (≤2k tokens) → T2 (≤6k) → T3 (≤12k) for progressive disclosure
- **Cited**: Every claim has a source with access date. Zero tolerance for hallucinations.
- **Validated**: CI enforces format, checks secrets, verifies links

**Skills** are single-purpose capabilities invoked by Claude during conversations. **Agents** are multi-step orchestrators you invoke explicitly for complex workflows requiring ≥3 steps and separate context windows.

## Usage with Claude CLI

### 1. Clone and Point Claude at It

```bash
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
```

Tell Claude CLI about this repo by referencing `CLAUDE.md` in your conversations. Claude will load only what it needs.

### 2. Use a Skill

Ask Claude to use a skill by name:

```
Use the microservices-pattern-architect skill to recommend patterns for my e-commerce checkout flow.
```

Claude loads progressively: T1 for simple cases, T2/T3 when you need depth. You don't specify tiers—Claude decides based on complexity.

### 3. Creating Skills

Use the `skill-creation` meta-skill to generate production-ready skills automatically:

```
Use the skill-creation skill to build a new skill for Kubernetes deployment validation.
```

**What you get:**
- `skills/<slug>/SKILL.md` (complete, validated structure)
- `skills/<slug>/examples/<slug>-example.txt` (≤30 lines)
- `tests/evals_<slug>.yaml` (3–5 test scenarios)
- Index entry in `index/skills-index.json`

**Enforces automatically:**
- CLAUDE.md §3 format (required sections, token budgets)
- Source citations with access dates
- No secrets or PII
- Examples ≤30 lines
- T1/T2/T3 token budgets

**Requirements:**
- Provide topic/domain clearly
- Specify inputs/outputs if known (skill will ask if unclear)
- Review generated skill and run `python3 tooling/validate_skill.py` before committing

### 4. Creating Agents

Use the `agent-creation` meta-skill for multi-step orchestration workflows:

```
Use the agent-creation skill to build a security audit orchestrator for multi-tier applications.
```

**What you get:**
- `agents/<slug>/AGENT.md` (system prompt, tool restrictions, workflows)
- `agents/<slug>/examples/` (1–2 interaction examples ≤30 lines each)
- `agents/<slug>/workflows/` (optional multi-step procedures)
- `tests/evals_agent_<slug>.yaml` (3–5 test scenarios)
- Index entry in `index/agents-index.json`

**Enforces automatically:**
- System prompt ≤1500 tokens
- Tool restrictions to approved MCP list
- Required sections (Purpose, System Prompt, Tool Usage, Workflow Patterns, Skills Integration, Examples, Quality Gates, Resources)
- No embedding of full skills (reference by slug only)

**When to use Agent vs Skill:**
- **Agent**: ≥3 steps, requires orchestration, stateful workflows, user-invoked (e.g., `orchestrator audit security...`)
- **Skill**: Single capability, model-invoked, shares main context

## What's Inside

**31 skills across 5 categories:**

- **Architecture** (8): Decision frameworks, microservices patterns, data pipelines, frontend frameworks, IaC, containers, databases, APIs
- **Operations** (8): Security assessment, compliance, code review, performance, testing, deployment, monitoring, cloud migration
- **Specialized** (12): MLOps, zero-trust, incident response, supply chain security, docs, cost optimization, SRE SLO, drift detection, UX design systems, chaos engineering, multi-cloud, edge computing
- **Meta-Skills** (2): skill-creation, agent-creation
- **AI Delegation** (2): Gemini CLI (large context), Codex CLI (code generation)

**Agents infrastructure:**
- `agent-creation` skill for generating new agents
- `/agents/` directory structure (ready for your custom orchestrators)
- Separate validation pipeline (`validate_agent.py`, `build_agent_index.py`)

Full skill list: `ls skills/` or check `index/skills-index.json`.

## Rules (Read CLAUDE.md)

CLAUDE.md is the authoritative rulebook. Key points:

- **Accuracy**: Zero tolerance for fabrication. Every claim needs a source with access date.
- **Token budgets**: T1/T2/T3 are hard limits, not suggestions. Validated by CI.
- **Examples**: ≤30 lines. No exceptions. Longer samples go in `resources/`.
- **No secrets**: Commit an API key and CI fails immediately.
- **Git workflow**: Feature branches only. Squash-merge to main. See CLAUDE.md §13.
- **Agent system prompts**: ≤1500 tokens. Reference skills by slug, never paste full skill content.

## Contributing

### Creating a New Skill

1. **Use the meta-skill** (recommended):
   ```
   Use the skill-creation skill to build a new skill for <your-topic>.
   ```
   Review output, validate, commit.

2. **Manual creation** (if you must):
   - Read CLAUDE.md §3 format requirements
   - Branch: `git checkout -b feature/your-skill`
   - Build skill following exact section order
   - Run validator: `python3 tooling/validate_skill.py`
   - Build index: `python3 tooling/build_index.py`
   - PR with `gh pr create` (see CLAUDE.md §13 for template)

### Creating a New Agent

1. **Use the meta-skill**:
   ```
   Use the agent-creation skill to build a new agent for <your-orchestration-workflow>.
   ```
   Specify topic, capabilities, and tool requirements.

2. **Manual creation**:
   - Read CLAUDE.md §2 for AGENT.md structure
   - Follow same git workflow as skills
   - Validate with `python3 tooling/validate_agent.py`

### Quality Gates (CI enforced)

Every PR must pass:
1. **Validation** (format, token budgets, secrets check, link verification)
2. **Linting** (section order, headings, citation format)
3. **Index build** (deterministic, no duplicate slugs)
4. **Evals** (test scenarios must be valid YAML and pass basic sanity)

If CI fails, fix it. No hand-waving. See CLAUDE.md §8 for specifics.

## Structure

```
agents/<slug>/
  AGENT.md                    # Agent specification (frontmatter + 8 sections)
  examples/                   # Interaction examples (≤30 lines each)
  workflows/                  # Multi-step procedures (optional)
  CHANGELOG.md

skills/<slug>/
  SKILL.md                    # The skill (required sections, cited sources)
  examples/                   # Small examples (≤30 lines each)
  resources/                  # Templates, schemas, configs
  CHANGELOG.md

tests/
  evals_<slug>.yaml           # 3–5 test scenarios per skill
  evals_agent_<slug>.yaml     # 3–5 scenarios per agent

index/
  skills-index.json           # Discovery manifest (generated)
  agents-index.json           # Agent discovery manifest (generated)
  embeddings/                 # Optional ANN vectors (tiny)
```

## Examples

### Creating a Custom Skill

**Task**: Build a skill for validating Terraform configurations against AWS Well-Architected Framework.

**Command**:
```
Use the skill-creation skill with topic "Terraform AWS Well-Architected validation" and tier T2. Include compliance checks for security pillar.
```

**Result**:
- `skills/terraform-aws-waf-validate/SKILL.md` with T1/T2 procedures
- Example showing input (Terraform files) → output (compliance report)
- Tests with happy path + missing required tags + cross-region violation scenarios
- Index entry with keywords `["terraform", "aws", "well-architected", "compliance"]`

### Creating a Custom Agent

**Task**: Build an agent that orchestrates incident response for security events.

**Command**:
```
Use the agent-creation skill for topic "Incident response orchestrator for security events" with tools Read, Bash, Grep, and Task. Include workflow for severity classification, evidence collection, and stakeholder notification.
```

**Result**:
- `agents/incident-responder/AGENT.md` with system prompt (≤1500 tokens)
- Tool usage: Read logs → Grep patterns → Bash (run forensics) → Task (delegate deep analysis)
- Workflow: 1) Classify severity → 2) Collect evidence → 3) Invoke security-assessment-framework skill → 4) Generate report
- Skills integration: References `security-assessment-framework` and `compliance-automation-engine` by slug
- 3 example scenarios: critical breach, false positive, partial data

## License

Apache-2.0

## Maintainer

Personal project - cognitive-toolworks

---

**Last Updated**: 2025-10-26T00:23:51-04:00
**CLAUDE.md Version**: 1.1.0
**Skills**: 31
**Agents**: Infrastructure ready (use agent-creation skill to build)
**Status**: Production
