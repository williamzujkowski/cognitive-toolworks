# cognitive-toolworks

61 production-ready Skills and 14 orchestrator Agents for Claude CLI. No fluff.

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

Use the `core-skill-authoring` meta-skill to generate production-ready skills automatically:

```
Use the core-skill-authoring skill to build a new skill for Kubernetes deployment validation.
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

Use the `core-agent-authoring` meta-skill for multi-step orchestration workflows:

```
Use the core-agent-authoring skill to build a security audit orchestrator for multi-tier applications.
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

**61 skills across 3-tier taxonomy (see CLAUDE.md §2A):**

- **Tier 1 - Core/Foundation** (4): `core-skill-authoring`, `core-agent-authoring`, `core-codex-delegator`, `core-gemini-delegator`
- **Tier 2 - Domain Skills** (39): Security (8), Testing (5), Cloud (5), DevOps (5), Compliance (2), Frontend (2), Data (1), Observability (2), FinOps (1), Resilience (1), Documentation (1), Quality (1), Integration (1), Tooling (1), plus Architecture, API, Container, Database, MLOps, Microservices, Mobile, Secrets
- **Tier 3 - Specialized** (18): Kubernetes (3), API (3), Database (2), Compliance (2), Mobile (1), Rust (1), Go (1), Python (1), Terraform (1), SLO (1), E2E Testing (1), Secrets (1)

**Naming convention (domain-first):**
- Security: `security-appsec-validator`, `security-cloud-analyzer`, `security-iam-reviewer`
- Testing: `testing-unit-generator`, `testing-integration-designer`, `testing-load-designer`
- Cloud: `cloud-aws-architect`, `cloud-multicloud-advisor`, `cloud-edge-architect`
- DevOps: `devops-cicd-generator`, `devops-iac-generator`, `devops-drift-detector`

**14 orchestrator agents:**
- **Meta**: `agent-creator` — generates new agents
- **Architecture**: `architecture-decision-orchestrator` — ADR generation
- **Cloud**: `cloud-native-orchestrator`, `cloud-aws-orchestrator`, `multi-region-orchestrator`
- **Compliance**: `compliance-orchestrator`
- **Cost**: `cost-optimization-orchestrator`
- **Database**: `database-migration-orchestrator`
- **DevOps**: `devops-pipeline-orchestrator`
- **Observability**: `observability-orchestrator`
- **Performance**: `performance-orchestrator`
- **Resilience**: `disaster-recovery-orchestrator`, `incident-response-orchestrator`
- **Security**: `security-auditor`

Full skill list: `ls skills/` or check `index/skills-index.json`. Full agent list: `ls agents/` or check `index/agents-index.json`.

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
   Use the core-skill-authoring skill to build a new skill for <your-topic>.
   ```
   Review output, validate, commit. Follow naming convention from CLAUDE.md §2A.

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
   Use the core-agent-authoring skill to build a new agent for <your-orchestration-workflow>.
   ```
   Specify topic, capabilities, and tool requirements. Agent names end in `-orchestrator`.

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
Use the core-skill-authoring skill with topic "Terraform AWS Well-Architected validation" and tier T2. Include compliance checks for security pillar.
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
Use the core-agent-authoring skill for topic "Incident response orchestrator for security events" with tools Read, Bash, Grep, and Task. Include workflow for severity classification, evidence collection, and stakeholder notification.
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

**Last Updated**: 2025-10-26T16:00:00-04:00
**CLAUDE.md Version**: 1.4.0 (added §2A naming convention taxonomy)
**Skills**: 61 (3-tier taxonomy: core → domain → specialized)
**Agents**: 14 orchestrators
**Status**: Production (cleaned, no deprecated skills)
