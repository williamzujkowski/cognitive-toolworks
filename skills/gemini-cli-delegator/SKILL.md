---
name: "Gemini CLI Delegation & Large Context Routing"
slug: gemini-cli-delegator
description: "Fast delegation of large-context tasks to Gemini CLI via MCP when file size exceeds 100KB or task requires analysis/review."
capabilities:
  - Large file analysis delegation (>100KB)
  - Simple task routing between Claude and Gemini
  - Sandbox code testing through Gemini MCP
inputs:
  - task_description: "Natural language description of the analysis or processing task"
  - file_paths: "List of file paths or directory patterns (optional)"
  - context_size_estimate: "Estimated token count or file size in KB"
  - task_type: "One of: analysis, review, edit, debug, test"
outputs:
  - delegation_decision: "Boolean indicating whether to delegate to Gemini"
  - recommended_tool: "claude|gemini-mcp"
  - delegation_command: "Formatted MCP command if delegating to Gemini"
  - rationale: "Brief justification for routing decision"
keywords:
  - delegation
  - gemini
  - mcp
  - large-context
  - task-routing
  - codebase-analysis
version: 2.0.0
owner: cognitive-toolworks
license: MIT
security:
  - no_secrets_in_delegation: "Validate no API keys or credentials in delegated content"
  - pii_check: "Screen for personal identifiable information before delegation"
  - sandbox_isolation: "Use Gemini sandbox for code execution tasks"
links:
  - url: "https://github.com/jamubc/gemini-mcp-tool"
    title: "Gemini MCP Tool Repository"
    accessed: "2025-10-25T23:14:09-04:00"
  - url: "https://ai.google.dev/gemini-api/docs/long-context"
    title: "Gemini API Long Context Documentation"
    accessed: "2025-10-25T23:14:09-04:00"
  - url: "https://docs.claude.com/en/docs/mcp"
    title: "Model Context Protocol - Claude Docs"
    accessed: "2025-10-25T23:14:09-04:00"
  - url: "https://www.anthropic.com/news/model-context-protocol"
    title: "Introducing the Model Context Protocol"
    accessed: "2025-10-25T23:14:09-04:00"
---

## Purpose & When-To-Use

**Trigger Conditions:**

Use this skill for fast delegation decisions when:

- **Large file analysis**: Single file >100KB
- **Analysis/review tasks**: Summarization, comprehension, codebase review
- **Sandbox code testing**: Safe execution of unfamiliar code

**Do NOT use when:**

- File <100KB and task is edit/refactor/debug (Claude excels here)
- Multi-file orchestration needed (use separate orchestration agent)
- Real-time debugging or iterative refinement

---

## Pre-Checks

**Timestamp & Environment**

```
NOW_ET = 2025-10-26T01:18:53-04:00 (America/New_York, ISO-8601)
```

**Required validations before delegation:**

1. **Input schema validation**:
   - `task_description` is non-empty string
   - `file_paths` (if provided) resolve to accessible files
2. **Security pre-flight**:
   - Scan file paths for patterns like `.env`, `credentials.json`, `*.key`, `*.pem`
   - Abort if secrets detected; prompt user to sanitize

---

## Procedure

**Token Budget: T1≤2000 tokens**

### Tier 1 — Fast Delegation Decision (T1≤2000 tokens)

**Two-step process:**

1. **Delegation gate** (primary decision):
   - If file size >100KB → **delegate to Gemini**
   - If task type = `analysis|review|summarize|codebase-review` → **delegate to Gemini**
   - Else → **keep in Claude**

2. **Format output**:
   - If delegating: emit `delegation_command` for Gemini MCP
   - Else: emit `recommended_tool: "claude"`
   - Include brief rationale citing threshold

---

## Decision Rules

**Primary Routing Logic:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| File size | >100KB | Delegate to Gemini |
| Task type | `analysis`, `review`, `summarize`, `codebase-review` | Delegate to Gemini |
| Sandbox execution | Any code testing | Delegate to Gemini |
| Otherwise | Default | Keep in Claude |

**Note:** Complex multi-file orchestration belongs in a separate orchestration agent, not this skill.

**Abort Conditions:**

- Secrets detected in file paths or task description

---

## Output Contract

**Schema (TypeScript-style):**

```typescript
interface DelegationResult {
  delegation_decision: boolean;           // true = delegate to Gemini
  recommended_tool: "claude" | "gemini-mcp";
  delegation_command?: string;            // only if delegation_decision = true
  rationale: string;                      // max 160 chars, cites threshold
  security_flags: string[];               // empty if clean; else warnings
}
```

**Required fields:**

- `delegation_decision`, `recommended_tool`, `rationale`, `security_flags` (always)
- `delegation_command` (only if `delegation_decision = true`)

---

## Examples

**Example 1: Large File Analysis (Delegate)**

```yaml
# Input
task_description: "Summarize research paper"
file_paths: ["./paper.pdf"]
context_size_estimate: 3500  # KB

# Output
{
  "delegation_decision": true,
  "recommended_tool": "gemini-mcp",
  "delegation_command": "ask gemini to analyze @./paper.pdf and summarize key findings",
  "rationale": "File size 3.5MB > 100KB threshold",
  "security_flags": []
}
```

**Example 2: Small File Edit (Keep in Claude)**

```yaml
# Input
task_description: "Refactor authentication function"
file_paths: ["./auth.py"]
context_size_estimate: 45  # KB

# Output
{
  "delegation_decision": false,
  "recommended_tool": "claude",
  "rationale": "File <100KB and task type 'refactor' suits Claude precision",
  "security_flags": []
}
```

---

## Quality Gates

**Token Budget Enforcement:**

- **Token budget**: T1≤2k tokens for fast delegation decision (T2/T3 not applicable - skill simplified to T1 only)
- Examples must be ≤30 lines each (including fences)

**Safety Checks:**

- [ ] No API keys or secrets in delegation_command
- [ ] PII screening if task involves user data
- [ ] Sandbox isolation for code execution tasks

**Determinism:**

- Same inputs (file size, task type) must produce same delegation decision
- Rationale must cite specific threshold (e.g., "File size >100KB")

---

## Resources

**Primary Sources:**

- [Gemini MCP Tool Repository](https://github.com/jamubc/gemini-mcp-tool) — MCP server implementation, CLI integration (accessed 2025-10-26T01:18:53-04:00)
- [Gemini API Long Context Documentation](https://ai.google.dev/gemini-api/docs/long-context) — 1M token context window (accessed 2025-10-26T01:18:53-04:00)
- [Model Context Protocol - Claude Docs](https://docs.claude.com/en/docs/mcp) — MCP specification (accessed 2025-10-26T01:18:53-04:00)

**Configuration Templates:**

- `resources/mcp-config-template.json` — Claude Desktop MCP setup for gemini-mcp-tool
- `resources/delegation-decision-matrix.md` — Static reference table (not computed during skill execution)
