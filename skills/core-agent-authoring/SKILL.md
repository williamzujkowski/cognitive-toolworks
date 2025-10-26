---
name: "Create Specialized Agent for Claude Code CLI"
slug: "core-agent-authoring"
description: "Generate comprehensive AGENT.md specs with system prompts, workflows, and tool restrictions following Claude Code CLI standards."
deprecated: true
deprecation_notice: "This skill has been refactored into a proper agent. Use `/agents/agent-creator/AGENT.md` instead. Migration: Invoke via 'orchestrator use agent-creator ...' rather than skill invocation."
deprecated_date: "2025-10-26"
replacement: "agents/agent-creator"
capabilities:
  - "research Claude Code agent specifications"
  - "generate AGENT.md with YAML frontmatter"
  - "design agent system prompts (≤1500 tokens)"
  - "define tool restrictions and workflow patterns"
  - "emit agent index entries and validation configs"
inputs:
  - name: "topic"
    type: "string"
    required: true
  - name: "agent_type"
    type: "string"
    required: false
  - name: "capabilities"
    type: "array[string]"
    required: false
  - name: "tier"
    type: "string"
    required: false
  - name: "tools"
    type: "array[string]"
    required: false
  - name: "constraints"
    type: "json"
    required: false
outputs:
  - name: "agent_folder"
    type: "directory"
  - name: "index_entry"
    type: "json"
  - name: "validation_results"
    type: "json"
keywords: ["agent-authoring", "claude-code", "system-prompt", "workflow", "orchestration", "mcp"]
version: "1.0.0"
owner: "cognitive-toolworks"
license: "Apache-2.0"
security:
  pii: "none"
  secrets: "never embed; use env/cred mgr"
  audit: "include sources with titles/URLs; normalize NIST time"
links:
  docs:
    - "https://docs.claude.com/en/docs/claude-code/sub-agents"
    - "https://modelcontextprotocol.io/introduction"
    - "https://platform.openai.com/docs/guides/agent-design"
---

## Purpose & When-To-Use

> **DEPRECATED as of 2025-10-26**: This skill has been refactored into a proper agent at `/agents/agent-creator/AGENT.md`. Please use `orchestrator use agent-creator ...` instead of skill invocation. This file is retained for historical reference only.

Use when a developer needs a **specialized Claude Code agent** for multi-step workflows (e.g., security audits, cost analysis, incident response) that orchestrates skills and operates in a separate context window. Agents are **user-invoked** (not model-invoked like skills) and suited for complex, stateful tasks requiring ≥3 steps.

**Decision: Agent vs Skill**
- **Agent**: Multi-step workflows, separate context, orchestration, user-invoked (e.g., "orchestrator use swarm...")
- **Skill**: Single focused capability, shares main context, model-invoked (e.g., "Use the core-skill-authoring skill...")

## Pre-Checks

- **Authoritative time**: Set `NOW_ET` to ISO 8601 in `America/New_York` using NIST/time.gov semantics. Include `NOW_ET` in citations' access dates.
- **Scope validation**: Confirm topic requires multi-step orchestration (if ≤2 steps, recommend a skill instead).
- **Tool availability**: Verify requested tools exist in MCP/Claude Code toolset.
- **Sources**: Identify authoritative docs for agent patterns, system prompts, and MCP specs.
- **Placement**: Default to `/agents/<slug>/` unless user specifies alternate path.

## Procedure

### Tier 1 — Generate Minimal Agent Spec (T1≤2000 tokens)

1. **Create AGENT.md scaffold** with YAML frontmatter:
   - Required fields: `name`, `description` (≤160 chars), `model` (sonnet/opus/haiku/inherit), `tools`, `persona`, `version`, `owner`, `keywords`
   - Set `model: inherit` unless user specifies; restrict `tools` to approved MCP list
2. **Draft 8 required sections**:
   - `## Purpose & When-To-Use` — trigger conditions (user-invoked workflows)
   - `## System Prompt` — concise persona + objectives (≤1500 tokens; *never* include full skill text)
   - `## Tool Usage Guidelines` — which tools, when, and why
   - `## Workflow Patterns` — multi-step procedures (e.g., 1. Research → 2. Analyze → 3. Report)
   - `## Skills Integration` — which skills to invoke at each step (reference by slug)
   - `## Examples` — 1–2 interaction examples (≤30 lines each)
   - `## Quality Gates` — validation criteria, success metrics
   - `## Resources` — links to relevant docs/templates
3. **System Prompt Guidelines**:
   - Keep ≤1500 tokens
   - Focus on role/persona + high-level goals
   - Reference skills by slug (don't paste skill content)
   - Include CLAUDE.md enforcement reminder
4. **Output minimal index entry**: `slug`, `name`, `description`, `keywords`, `version`, `entry`

### Tier 2 — Source-Backed Validation (T2≤6000 tokens)

1. **Add 2–4 primary sources** with titles, URLs, and `NOW_ET` access dates:
   - Claude Code sub-agents documentation
   - Model Context Protocol specs
   - Relevant agent design patterns
2. **Refine Tool Usage**:
   - Specify tool restrictions (e.g., `tools: ["Read", "Bash", "Grep"]`)
   - Add decision rules for when to use each tool
   - Document tool dependencies (e.g., "Use Grep before Read for large codebases")
3. **Expand Workflow Patterns**:
   - Add branching logic (if/else conditions)
   - Include error handling procedures
   - Define abort conditions
4. **Create example interaction**: Show realistic user request → agent workflow → expected outputs

### Tier 3 — Deep Orchestration & Validation (T3≤12000 tokens)

1. **Generate `/agents/<slug>/workflows/` procedures**:
   - Multi-step markdown guides for complex flows
   - Include skill invocation syntax
   - Add validation checkpoints
2. **Create `tests/evals_agent_<slug>.yaml`** with 3–5 scenarios:
   - Happy path (multi-step success)
   - Missing input (graceful degradation)
   - Tool failure (error handling)
   - Edge case (boundary conditions)
   - Skill integration (verify skill invocations work)
3. **Emit CHANGELOG.md** starting at `v1.0.0`
4. **Finalize index entry** with all metadata
5. **Validation script stub**: Create placeholder for `tooling/validate_agent.py` if not present

## Decision Rules

- **Agent vs Skill**: If task requires ≤2 steps or no state → recommend skill; if ≥3 steps or orchestration → agent
- **Tool restrictions**: If user doesn't specify tools → default to `["Read", "Write", "Bash", "Grep", "Glob"]`
- **Model selection**: Default to `inherit` (uses user's selected model); only specify if agent needs specific capability (e.g., `opus` for complex reasoning)
- **System prompt length**: If draft exceeds 1500 tokens → extract details to workflows/ or resources/
- **Missing schemas**: If agent requires external API/service specs → emit `[TODO: verify schema for X]` and stop at T2

## Output Contract

```typescript
interface AgentOutput {
  agent_folder: {
    path: string;              // "/agents/<slug>/"
    files: {
      AGENT_md: string;        // Full AGENT.md content
      examples: string[];      // ≤30 lines each
      workflows?: string[];    // Optional multi-step procedures
      CHANGELOG_md: string;    // Version history
    };
  };
  index_entry: {
    slug: string;
    name: string;
    description: string;       // ≤160 chars
    keywords: string[];
    model: string;             // "sonnet" | "opus" | "haiku" | "inherit"
    tools: string[];
    version: string;
    owner: string;
    entry: string;             // "agents/<slug>/AGENT.md"
  };
  validation_results: {
    frontmatter_valid: boolean;
    system_prompt_length: number;    // Must be ≤1500 tokens
    required_sections_present: boolean;
    examples_valid: boolean;          // ≤30 lines each
    tools_valid: boolean;             // All tools in approved MCP list
  };
}
```

**Required Fields**:
- `agent_folder.path`: Must follow `/agents/<slug>/` pattern
- `agent_folder.files.AGENT_md`: Complete AGENT.md with frontmatter + 8 sections
- `index_entry.slug`: Unique identifier (kebab-case)
- `index_entry.description`: ≤160 characters
- `validation_results.*`: All boolean checks must be true

## Examples

**Input**:
```text
topic: "Security audit orchestrator for multi-tier applications"
agent_type: "orchestrator"
capabilities: ["vulnerability scanning", "compliance checking", "report generation"]
tier: "T2"
tools: ["Read", "Bash", "Grep", "Task"]
```

**Output (simplified)**:
```text
agents/security-auditor/AGENT.md created with:

Frontmatter:
  name: security-auditor
  description: Orchestrates comprehensive security audits across multi-tier applications
  model: inherit
  tools: [Read, Bash, Grep, Task]
  persona: Senior security engineer conducting systematic audits

Sections:
  - Purpose & When-To-Use: Trigger = "orchestrator audit security..."
  - System Prompt: ≤1500 tokens, references security-assessment-framework skill
  - Tool Usage: Read configs, Bash scanners, Grep patterns, Task delegation
  - Workflow: Discovery → Analysis → Compliance → Report
  - Skills Integration: security-assessment-framework, compliance-automation-engine
  - Examples: 3 interaction scenarios (breach, false positive, partial data)
  - Quality Gates: Severity categorization, control mapping, remediation guidance
  - Resources: OWASP Top 10, NIST SP 800-53
```

## Quality Gates

- **Frontmatter validation**: All required YAML keys present; description ≤160 chars
- **System prompt**: ≤1500 tokens (measure via `tiktoken cl100k_base`)
- **Required sections**: All 8 sections present in correct order
- **Examples**: ≤30 lines each; show realistic interaction
- **Tool restrictions**: All tools exist in approved MCP list
- **Index entry**: Valid JSON; no duplicate slugs
- **Citations**: T2+ includes 2–4 sources with titles, URLs, and `NOW_ET` access dates
- **No secrets**: Validator scans for API keys, tokens, credentials
- **Evals**: T3 includes 3–5 test scenarios in `tests/evals_agent_<slug>.yaml`

## Resources

- **Claude Code Sub-Agents Documentation** (accessed 2025-10-26T00:23:51-04:00): https://docs.claude.com/en/docs/claude-code/sub-agents
- **Model Context Protocol Introduction** (accessed 2025-10-26T00:23:51-04:00): https://modelcontextprotocol.io/introduction
- **Agent Design Patterns (OpenAI)** (accessed 2025-10-26T00:23:51-04:00): https://platform.openai.com/docs/guides/agent-design
- **Anthropic Skills Overview** (accessed 2025-10-26T00:23:51-04:00): https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **NIST Time Services** (accessed 2025-10-26T00:23:51-04:00): https://www.nist.gov/pml/time-and-frequency-division/time-services
