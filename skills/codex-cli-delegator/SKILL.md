---
name: "Codex CLI Delegation & Code Generation Routing"
slug: codex-cli-delegator
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
version: 1.0.0
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
NOW_ET = 2025-10-25T23:27:14-04:00
```

**Input validation:**

1. Verify `task_description` is non-empty and specific
2. Confirm `task_type` is one of: generation, modification, analysis, testing
3. Check `existing_files` list for valid paths if task_type = modification
4. Validate Codex CLI availability: `which codex` returns valid path
5. Confirm Codex authentication: check `~/.codex/config.toml` exists or user is authenticated

**Source freshness:**

* Codex CLI repo (https://github.com/openai/codex, accessed 2025-10-25T23:27:14-04:00)
* Codex documentation (https://developers.openai.com/codex/cli/, accessed 2025-10-25T23:27:14-04:00)
* Codex getting started guide (https://help.openai.com/en/articles/11096431, accessed 2025-10-25T23:27:14-04:00)
* AI code generation best practices (https://getdx.com/blog/ai-code-enterprise-adoption/, accessed 2025-10-25T23:27:14-04:00)

## Procedure

### T1: Fast-Path Simple Delegation (≤2k tokens)

**Use when:** task_type = generation AND complexity = simple AND existing_files is empty

1. Match task against delegation matrix (see Resources)
2. If match → boilerplate/scaffold:
   * delegation_decision = codex
   * execution_mode = non-interactive
   * Generate `codex exec --prompt "<task_description>"`
3. If match → modification with context:
   * delegation_decision = claude
   * Abort T1, explain why Claude is better suited
4. Return delegation_decision with one-line rationale

**Token budget: ≤2k**

### T2: Extended Routing with Validation (≤6k tokens)

**Use when:** complexity = moderate OR complex OR existing_files is not empty

1. **Analyze task characteristics:**
   * New file creation? → +1 Codex score
   * Existing file modification? → +1 Claude score
   * Requires business logic context? → +1 Claude score
   * Repetitive patterns? → +1 Codex score
   * Security-sensitive? → +1 Claude score
   * Boilerplate/templates? → +2 Codex score

2. **Apply decision thresholds:**
   * Codex score ≥ 3 AND Claude score ≤ 1 → delegate to Codex
   * Claude score ≥ 3 → keep in Claude
   * Scores within 1 point → hybrid (Codex generates, Claude reviews)

3. **Generate Codex command:**
   * Interactive mode: `codex "<natural_language_prompt>"`
   * Non-interactive mode: `codex exec --prompt "<prompt>"`
   * With file context: `codex --file <filepath> "<prompt>"`

4. **Define quality checks:**
   * Lint generated code (language-specific linters)
   * Run tests if test files exist
   * Security scan for common vulnerabilities
   * Code review checklist (see Resources)

5. **Return full delegation contract:**
   ```json
   {
     "delegation_decision": "codex|claude|hybrid",
     "codex_command": "codex exec --prompt '...'",
     "rationale": "...",
     "execution_mode": "interactive|non-interactive",
     "quality_checks": ["lint", "test", "security_scan"],
     "estimated_files": 3,
     "review_required": true
   }
   ```

**Token budget: ≤6k**

## Decision Rules

### When to Delegate to Codex

**Always delegate:**
* Generate new boilerplate code from scratch
* Create project scaffolds (REST APIs, web apps, CLIs)
* Generate test suites from existing code
* Convert specifications/diagrams to code
* Create repetitive code patterns (CRUD operations, data models)

**Prefer delegate (score ≥3):**
* Multi-file project initialization
* Code completion for large sections
* Pseudocode to implementation conversion
* Template-based code generation

**Thresholds:**
* New file count ≥ 3 → always Codex
* Repetitive pattern count ≥ 5 → always Codex
* Zero existing files → prefer Codex
* Natural language spec completeness ≥ 80% → prefer Codex

### When to Keep in Claude

**Always keep:**
* Debugging existing code with business context
* Security-sensitive modifications (auth, encryption, data handling)
* Code review and architecture analysis
* Refactoring with complex dependencies

**Prefer keep (score ≥3):**
* Bug fixes requiring context understanding
* Performance optimization with profiling
* API integration requiring domain knowledge
* Database migrations with data preservation

**Thresholds:**
* Existing file modification count ≥ 2 → prefer Claude
* Security sensitivity = high → always Claude
* Business logic complexity ≥ moderate → prefer Claude
* User requires interactive problem-solving → always Claude

### Hybrid Mode

**Use when:**
* Scores within 1 point of each other
* Large code generation requiring thorough review
* New feature with security implications
* Unfamiliar language/framework combination

**Process:**
1. Codex generates initial implementation
2. Claude reviews for logic, security, and best practices
3. Claude proposes refinements
4. User approves final version

## Output Contract

**Required fields:**
```typescript
interface DelegationResult {
  delegation_decision: "codex" | "claude" | "hybrid";
  rationale: string; // ≤160 chars
  codex_command?: string; // if delegation_decision includes codex
  execution_mode: "interactive" | "non-interactive";
  quality_checks: string[]; // ["lint", "test", "security_scan", "review"]
  estimated_files?: number;
  estimated_tokens?: number;
  review_required: boolean;
  abort_conditions?: string[]; // conditions to stop and escalate to user
}
```

**Validation rules:**
* `codex_command` required if delegation_decision ∈ {codex, hybrid}
* `quality_checks` must include at least ["lint", "review"]
* `review_required` = true for all hybrid and security-sensitive tasks
* `abort_conditions` populated if pre-checks fail

## Examples

**Example 1: Simple REST API Generation (Delegate to Codex)**

```yaml
input:
  task_description: "Create a REST API for user management with CRUD operations"
  task_type: generation
  existing_files: []
  complexity: simple

output:
  delegation_decision: codex
  rationale: "New boilerplate generation, zero existing files, clear spec"
  codex_command: "codex exec --prompt 'Generate REST API for user management with CREATE, READ, UPDATE, DELETE endpoints using Express.js and TypeScript'"
  execution_mode: non-interactive
  quality_checks: [lint, test, security_scan, review]
  estimated_files: 5
  review_required: true
```

## Quality Gates

**Token budgets (enforced):**
* T1 fast-path: ≤2k tokens (80% of simple delegations)
* T2 extended: ≤6k tokens (complex routing with validation)
* T3 not applicable (code generation delegation doesn't require deep research paths)

**Code quality validation:**
* All generated code must pass language-specific linters
* Security scan for OWASP Top 10 vulnerabilities
* Test coverage ≥ 70% if tests generated
* No hardcoded secrets or credentials

**Delegation quality:**
* Rationale must be ≤160 chars and actionable
* Codex commands must be valid and tested
* Quality checks must include minimum: [lint, review]
* Abort conditions clearly defined for failure scenarios

**Auditability:**
* Log all delegation decisions with timestamps
* Record Codex commands executed and outputs
* Track quality check results
* Maintain decision matrix scores for continuous improvement

**Safety:**
* Never execute Codex commands automatically without user confirmation in interactive mode
* Always review generated code before committing
* Validate all file paths before write operations
* Check for destructive operations (rm, drop, delete) in generated code

## Resources

**Official documentation:**
* Codex CLI repository: https://github.com/openai/codex (accessed 2025-10-25T23:27:14-04:00)
* Codex CLI docs: https://developers.openai.com/codex/cli/ (accessed 2025-10-25T23:27:14-04:00)
* Codex getting started: https://help.openai.com/en/articles/11096431 (accessed 2025-10-25T23:27:14-04:00)
* AI code generation best practices: https://getdx.com/blog/ai-code-enterprise-adoption/ (accessed 2025-10-25T23:27:14-04:00)

**Local resources:**
* Delegation decision matrix: `resources/delegation-decision-matrix.md`
* Codex command reference: `resources/codex-commands.md`
* Configuration template: `resources/codex-config-template.toml`

**Integration guides:**
* GitHub Action: https://github.com/openai/codex#github-action
* TypeScript SDK: https://github.com/openai/codex#typescript-sdk
* VS Code extension: search "Codex" in VS Code marketplace
