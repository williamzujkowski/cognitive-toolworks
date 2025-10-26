---
name: "Codex CLI Delegation & Code Generation Routing"
slug: core-codex-delegator
description: "Intelligently delegate code generation, boilerplate creation, and automation tasks to OpenAI Codex CLI for rapid prototyping and development."
capabilities:
  - Code generation task routing between Claude and Codex
  - Boilerplate and scaffold generation delegation
  - Test suite generation routing
  - Multi-file project creation delegation
  - Interactive vs non-interactive mode selection
inputs:
  - task_description: string
  - task_type: enum[generation, modification, analysis, testing]
  - existing_files: list[filepath]
  - context_required: boolean
  - complexity: enum[simple, moderate, complex]
outputs:
  - delegation_decision: enum[codex, claude, hybrid]
  - codex_command: string (if delegated)
  - rationale: string
  - execution_mode: enum[interactive, non-interactive]
  - quality_checks: list[string]
keywords:
  - code-generation
  - delegation
  - codex
  - automation
  - scaffolding
  - boilerplate
  - routing
  - ai-agents
version: 1.1.0
owner: personal
license: Apache-2.0
security:
  - no-secrets-in-prompts
  - validate-generated-code
  - review-before-execution
links:
  - https://github.com/openai/codex
  - https://developers.openai.com/codex/cli/
  - https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started
---

## Purpose & When-To-Use

**Trigger this skill when:**

* User requests generation of new code from scratch (boilerplate, scaffolds, templates)
* Task involves creating test suites from existing code
* Rapid prototyping with natural language specifications is needed
* Large-scale repetitive code patterns must be generated
* Multi-file project initialization is required
* Converting pseudocode or diagrams to implementation

**Do NOT trigger when:**

* Debugging existing code with business context
* Refactoring code requiring architectural understanding
* Performing code review or security analysis
* Modifying existing code with complex dependencies
* Interactive problem-solving requiring domain expertise

## Pre-Checks

**Time normalization:**
```
NOW_ET = 2025-10-26T01:18:52-04:00
```

**Input validation:**

1. Verify `task_description` is non-empty and specific
2. Confirm `task_type` is one of: generation, modification, analysis, testing
3. Check `existing_files` list for valid paths if task_type = modification
4. Validate Codex CLI availability: `which codex` returns valid path
5. Confirm Codex authentication: check `~/.codex/config.toml` exists or user is authenticated

**Source freshness:**

* Codex CLI repo (https://github.com/openai/codex, accessed 2025-10-26T01:18:52-04:00)
* Codex documentation (https://developers.openai.com/codex/cli/, accessed 2025-10-26T01:18:52-04:00)
* Codex getting started guide (https://help.openai.com/en/articles/11096431, accessed 2025-10-26T01:18:52-04:00)
* AI code generation best practices (https://getdx.com/blog/ai-code-enterprise-adoption/, accessed 2025-10-26T01:18:52-04:00)

## Procedure

### T1: Simple Delegation Decision (≤2k tokens)

**Steps:**

1. **Check task type** against delegation matrix (see `resources/delegation-decision-matrix.md`):
   * Boilerplate/scaffold/code-generation from scratch? → Delegate to Codex
   * Modification/debugging/refactoring existing code? → Keep in Claude
   * Security-sensitive or requires business context? → Keep in Claude

2. **Return decision** with rationale and command (if delegating):
   * If delegating → provide `codex exec --prompt "<task_description>"` command
   * If keeping → explain why Claude is better suited
   * Set `review_required = true` for all Codex delegations

**Token budget: ≤2k**

**Note:** For complex validation workflows with scoring matrices, use a separate validation agent. This skill focuses on fast, simple routing decisions.

## Decision Rules

### Delegate to Codex (simple criteria)

* New boilerplate generation from scratch
* Project scaffolding (REST APIs, CLIs, web apps)
* Test suite generation from specifications
* Repetitive code patterns (CRUD, data models)
* Zero or minimal existing files
* Clear natural language specifications

### Keep in Claude (simple criteria)

* Modifying existing code
* Debugging or refactoring
* Security-sensitive operations (auth, encryption, data)
* Code requiring business context or domain knowledge
* Architecture analysis or code review
* Interactive problem-solving

### Abort and escalate if:

* Task type is ambiguous or unclear
* Security implications are uncertain
* Codex CLI is not installed or authenticated
* User input validation fails

## Output Contract

**Required fields:**
```typescript
interface DelegationResult {
  delegation_decision: "codex" | "claude";
  rationale: string; // ≤160 chars
  codex_command?: string; // required if delegation_decision = codex
  review_required: boolean; // always true for codex delegations
}
```

**Validation rules:**
* `codex_command` required if delegation_decision = "codex"
* `rationale` must be ≤160 characters
* `review_required` = true for all Codex delegations

## Examples

**Example 1: Delegate to Codex (new scaffold)**

```yaml
input:
  task_description: "Create a REST API for user management with CRUD operations"
  task_type: generation
  existing_files: []

output:
  delegation_decision: codex
  rationale: "New boilerplate generation from scratch"
  codex_command: "codex exec --prompt 'Generate REST API for user management with CREATE, READ, UPDATE, DELETE endpoints using Express.js and TypeScript'"
  review_required: true
```

**Example 2: Keep in Claude (existing code modification)**

```yaml
input:
  task_description: "Fix authentication bug in login.py"
  task_type: modification
  existing_files: ["src/auth/login.py"]

output:
  delegation_decision: claude
  rationale: "Debugging existing code with security implications"
  review_required: false
```

## Quality Gates

**Token budgets (enforced):**
* T1 simple delegation: ≤2k tokens (covers all use cases)
* T2/T3 not used (complex validation should use separate agent)

**Delegation quality:**
* Rationale must be ≤160 chars and actionable
* Codex commands must be syntactically valid
* All Codex delegations require manual review (`review_required = true`)

**Safety:**
* Never execute Codex commands without user confirmation
* Validate all input parameters before generating commands
* Abort if pre-checks fail (CLI not installed, auth missing)

## Resources

**Official documentation:**
* Codex CLI repository: https://github.com/openai/codex (accessed 2025-10-26T01:18:52-04:00)
* Codex CLI docs: https://developers.openai.com/codex/cli/ (accessed 2025-10-26T01:18:52-04:00)
* Codex getting started: https://help.openai.com/en/articles/11096431 (accessed 2025-10-26T01:18:52-04:00)
* AI code generation best practices: https://getdx.com/blog/ai-code-enterprise-adoption/ (accessed 2025-10-26T01:18:52-04:00)

**Local resources:**
* Delegation decision matrix: `resources/delegation-decision-matrix.md` (for detailed scoring; use separate agent for complex validation)
* Codex command reference: `resources/codex-commands.md`
* Configuration template: `resources/codex-config-template.toml`
