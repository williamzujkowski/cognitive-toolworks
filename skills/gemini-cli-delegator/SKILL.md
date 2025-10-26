---
name: "Gemini CLI Delegation & Large Context Routing"
slug: gemini-cli-delegator
description: "Intelligently delegate large-context tasks to Gemini CLI via MCP integration for document analysis, codebase review, and multi-file processing."
capabilities:
  - Large file and codebase analysis delegation
  - Context window optimization (Claude ≤200k vs Gemini ≤1M tokens)
  - Multi-file dependency tracking via Gemini
  - Sandbox code testing through Gemini MCP
  - Strategic task routing between Claude and Gemini
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
version: 1.0.0
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

Use this skill when facing tasks that exceed Claude's optimal context window or require capabilities better suited to Gemini's architecture:

- **Large document analysis**: Single files >100KB or PDFs with dense content
- **Full codebase review**: Projects with >20 files requiring holistic understanding
- **Multi-file dependency analysis**: Tracking imports, function calls, or data flow across numerous files
- **Extended context reasoning**: Tasks requiring >200k tokens of context
- **Sandbox code testing**: Safe execution of unfamiliar or potentially risky code

**Do NOT use when:**

- Task requires interactive editing or precise code modifications (Claude excels here)
- Single small file (<50KB) with focused query
- Real-time debugging or iterative refinement
- Tasks requiring tool use or API integrations unavailable to Gemini

---

## Pre-Checks

**Timestamp & Environment**

```
NOW_ET = 2025-10-25T23:14:09-04:00 (America/New_York, ISO-8601)
```

**Required validations before delegation:**

1. **Gemini MCP availability**: Verify `gemini-mcp-tool` is configured in Claude Desktop MCP settings
2. **Input schema validation**:
   - `task_description` is non-empty string
   - `file_paths` (if provided) resolve to accessible files/directories
   - `context_size_estimate` is positive integer or "unknown"
3. **Security pre-flight**:
   - Scan file paths for patterns like `.env`, `credentials.json`, `*.key`, `*.pem`
   - Check task_description for API keys (regex: `[A-Za-z0-9_-]{20,}`)
   - Abort if secrets detected; prompt user to sanitize
4. **Source freshness**: Confirm gemini-mcp-tool version ≥1.0.0 (breaking changes possible)

---

## Procedure

**Token Budget Tiers:**

- **T1 (≤2k tokens)**: Single-file delegation decision (fast path)
- **T2 (≤6k tokens)**: Multi-file codebase analysis with source validation

### T1: Fast Path (Single File Delegation)

**Context:** User provides one file path or small set of files (<5).

1. **Size check**: `stat -f%z <file>` (macOS) or `stat -c%s <file>` (Linux)
   - If size >100KB → **delegate to Gemini**
   - If size <50KB → **keep in Claude**
   - If 50KB–100KB → proceed to step 2
2. **Task type analysis**:
   - `analysis|review|summarize` → **delegate to Gemini** (strength: comprehension)
   - `edit|refactor|debug` → **keep in Claude** (strength: precision)
3. **Emit decision** and skip T2

### T2: Extended Analysis (Multi-File & Codebase)

**Context:** User requests codebase-wide analysis or multi-file task.

1. **Count files**: `find <directory> -type f | wc -l`
   - If >20 files → **strong delegation signal**
   - If >50 files → **always delegate to Gemini**
2. **Estimate total context**:
   - Sum file sizes: `find <directory> -type f -exec stat -c%s {} + | awk '{s+=$1} END {print s}'`
   - Rough token estimate: `total_bytes / 4` (approximation)
   - If >150k tokens → **delegate to Gemini** (Claude context strain)
3. **Consult decision matrix** (see `resources/delegation-decision-matrix.md`):
   - Cross-reference task type and file count
   - Apply delegation threshold rules
4. **Format MCP command** if delegating:
   ```
   ask-gemini: "analyze @<directory> and provide <specific analysis>"
   ```
5. **Return delegation package**: decision, command, rationale

### T3: Deep Dive (Not Implemented)

Reserved for future meta-analysis of delegation patterns and performance tuning. T2 is sufficient for current scope.

---

## Decision Rules

**Primary Routing Logic:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Single file size | >100KB | Delegate to Gemini |
| File count | >20 files | Consider Gemini; >50 → always delegate |
| Estimated tokens | >150k | Delegate to Gemini |
| Task type | `analysis`, `review`, `summarize` | Prefer Gemini for large contexts |
| Task type | `edit`, `refactor`, `debug` | Prefer Claude for precision |
| Sandbox execution | Any code testing | Always use Gemini sandbox |

**Ambiguity Handling:**

- If context size is "unknown" and file count <10: default to **Claude**
- If task type is ambiguous (e.g., "understand and fix"): split into delegation (understand → Gemini) + execution (fix → Claude)
- If MCP unavailable: abort delegation; return error with setup instructions

**Abort Conditions:**

- Secrets detected in file paths or task description
- Gemini MCP not configured (check fails)
- File paths resolve to >500 files (risk of timeout; prompt user to narrow scope)

---

## Output Contract

**Schema (TypeScript-style):**

```typescript
interface DelegationResult {
  delegation_decision: boolean;           // true = delegate to Gemini
  recommended_tool: "claude" | "gemini-mcp";
  delegation_command?: string;            // only if delegation_decision = true
  rationale: string;                      // max 160 chars
  context_estimate: {
    file_count: number;
    total_size_kb: number;
    estimated_tokens: number;
  };
  security_flags: string[];               // empty if clean; else warnings
}
```

**Required fields:**

- `delegation_decision`, `recommended_tool`, `rationale` (always)
- `delegation_command` (only if `delegation_decision = true`)
- `context_estimate` (best-effort; may contain `null` for unknown values)
- `security_flags` (always; empty array if no issues)

---

## Examples

**Example 1: Large PDF Analysis (Delegate)**

```yaml
# Input
task_description: "Summarize key findings from research paper"
file_paths: ["./research/neural-networks-2024.pdf"]
context_size_estimate: 3500  # KB

# Output
{
  "delegation_decision": true,
  "recommended_tool": "gemini-mcp",
  "delegation_command": "ask gemini to analyze @./research/neural-networks-2024.pdf and summarize key findings, methodology, and conclusions",
  "rationale": "File size 3.5MB exceeds 100KB threshold; analysis task suits Gemini's long context",
  "context_estimate": {"file_count": 1, "total_size_kb": 3500, "estimated_tokens": 875000},
  "security_flags": []
}
```

---

## Quality Gates

**Token Budget Enforcement:**

- T1 implementation must complete in ≤2k tokens (size check + fast decision)
- T2 implementation must complete in ≤6k tokens (file enumeration + matrix lookup + command formatting)
- Example must be ≤30 lines (including fences)

**Safety Checks:**

- [ ] No API keys or secrets in delegation_command
- [ ] PII screening if task involves user data (warn user; require confirmation)
- [ ] Sandbox isolation for any code execution (enforce `sandbox-test` tool)

**Auditability:**

- [ ] Log all delegation decisions with timestamp, rationale, and file paths (optional feature for tooling)
- [ ] Rationale must cite specific threshold (e.g., "file count 45 > 20 threshold")

**Determinism:**

- Same inputs (file paths, sizes, task type) must produce same delegation decision
- Decision matrix must be version-controlled and referenced by hash/version

---

## Resources

**Primary Sources:**

- [Gemini MCP Tool Repository](https://github.com/jamubc/gemini-mcp-tool) — MCP server implementation, CLI integration (accessed 2025-10-25T23:14:09-04:00)
- [Gemini API Long Context Documentation](https://ai.google.dev/gemini-api/docs/long-context) — 1M token context window, caching strategies (accessed 2025-10-25T23:14:09-04:00)
- [Model Context Protocol - Claude Docs](https://docs.claude.com/en/docs/mcp) — MCP specification, client/server architecture (accessed 2025-10-25T23:14:09-04:00)
- [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) — MCP origins, primitives, adoption (accessed 2025-10-25T23:14:09-04:00)

**Configuration Templates:**

- `resources/mcp-config-template.json` — Claude Desktop MCP setup for gemini-mcp-tool
- `resources/delegation-decision-matrix.md` — Task routing lookup table

**Related Skills:**

- `codebase-analyzer` (if exists) — may use this skill internally for routing decisions
- `security-scanner` (if exists) — for pre-delegation secret detection
