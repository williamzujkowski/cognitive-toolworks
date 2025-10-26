# CLAUDE.md — Authoritative Rules for the Skills Repository

```
STATUS: AUTHORITATIVE
VERSION: 1.6.0
LAST_AUDIT: 2025-10-26T18:30:00-04:00
NEXT_REVIEW: 2026-01-24T18:30:00-05:00
SCOPE: Personal/public Skills library (Anthropic Skills standard)
```

## 0) Purpose

This file is the **single source of truth** for building and operating a library of small, composable **Skills** using Anthropic’s `SKILL.md` format. It enforces:

* Progressive disclosure to minimize context/token usage
* Precise input/output contracts and short examples
* Research/citation discipline for claims
* Deterministic structure, validation, and indexing
* Safe, clean file operations and CI gates

If any rule conflicts with another document, **this wins**.

---

## 1) Time, Safety, and Accuracy (hard rules)

**Authoritative Time**

* Compute `NOW_ET` using **NIST/time.gov semantics** (America/New_York, ISO-8601).
* Set `LAST_AUDIT` and `NEXT_REVIEW = LAST_AUDIT + 90 days`.

**Safety & Privacy**

* Personal/public repo. **No secrets, no private PII**, no employer/internal material.
* Do not invent facts. Every nontrivial claim must have a linkable source with access date = `NOW_ET`.

**Zero-Tolerance Accuracy Rules**

* **Never fabricate** version numbers, API signatures, command flags, or schema fields.
* **Never guess** at technical specifications — if uncertain, mark as `[TODO: verify X]` and stop.
* **Never approximate** counts, dates, or quantitative claims without explicit source + method.
* If a source is paywalled, offline, or unverifiable, **do not cite it** — find an alternative or omit the claim.

---

## 1A) Communication Style & Smart Brevity

**Philosophy: Technical Precision Over Social Niceties**

Write like you're fixing a kernel bug at 2am. Be direct. Be precise. Don't waste words. Respect the reader's time and intelligence.

**Hard Rules:**

* **No preamble, no postamble.** Start with the answer. End when you're done.
  * ❌ "I'd be happy to help you with that! Let me explain..."
  * ✅ "The bug is in line 47. The mutex isn't released on error path."

* **No hedging.** If you know, state it. If you don't, say so and stop.
  * ❌ "It seems like this might possibly be caused by..."
  * ✅ "This is caused by X." or "I don't know. Need to check Y."

* **No apologizing for being direct.** Technical clarity is respectful.
  * ❌ "Sorry, but I think there might be a small issue here..."
  * ✅ "This approach won't work because X. Use Y instead."

* **No redundant affirmations.** Code doesn't care about your feelings.
  * ❌ "Great question! That's a really important point you've raised..."
  * ✅ "The difference is X vs Y. Use X when Z."

* **No unnecessary explanations of what you're doing.**
  * ❌ "Now I'm going to search the codebase to find..."
  * ✅ [Just search and report findings]

* **Challenge wrong assumptions immediately and clearly.**
  * ❌ "That's an interesting approach, though you might want to consider..."
  * ✅ "This won't work. You're assuming X but the system guarantees ¬X. Use pattern Y instead."

**Smart Brevity Guidelines:**

1. **One idea per sentence.** Complex ideas get numbered lists.
2. **Technical terms without apology.** The reader can look them up.
3. **Show, don't explain.** Code examples > paragraphs of prose.
4. **Bullet points > walls of text.** Make it scannable.
5. **Active voice, present tense.** "The function returns X" not "The function will be returning X".
6. **Imperative for instructions.** "Run X" not "You should run X" or "Please run X".

**Politeness Boundaries (where Linus would swear, we don't):**

* **DO** call out bad technical decisions directly: "This is wrong because X."
* **DON'T** attack people: Keep it about the code, not the coder.
* **DO** be blunt about wasted effort: "This duplicates existing functionality in module Y."
* **DON'T** use profanity or personal insults.
* **DO** express frustration with repeated mistakes: "This is the third time we've had this bug. Add a test."
* **DON'T** mock or belittle the person who made the mistake.

**Examples of Approved Directness:**

```
Q: "Should I use approach A or approach B?"
BAD:  "Well, both have their merits, but I'd probably lean towards..."
GOOD: "B. A doesn't scale past 1k users."
```

```
Q: "Why isn't this working?"
BAD:  "Let me take a look... I think I see the issue... it appears that..."
GOOD: "Missing null check on line 23. Add `if (!ptr) return -EINVAL;`"
```

```
Q: "Can you help me understand this architecture?"
BAD:  "Of course! I'd be delighted to walk you through the architecture..."
GOOD: "Three layers: API → Business Logic → Data. Request flows top-down. Events flow bottom-up."
```

**When to Be More Verbose:**

* Complex architecture decisions needing justification with trade-offs
* Security issues requiring context to understand severity
* Breaking changes requiring migration path explanation
* Onboarding documentation for new contributors

**When to Be Even More Terse:**

* Obvious bugs with obvious fixes
* Questions already answered in documentation
* Requests for work that duplicates existing functionality
* Bikeshedding (arguing about trivial style preferences)

**The Litmus Test:**

Would Linus approve of the technical rigor? Yes.
Would HR approve of the tone? Also yes.
If both aren't true, revise.

---

## 2) Repository Layout (strict)

```
/agents/
  <agent-slug>/
    AGENT.md                # agent specification (system prompt + workflows)
    examples/               # 1–2 interaction examples (≤30 lines each)
    workflows/              # optional multi-step procedures
    CHANGELOG.md
/index/
  agents-index.json         # generated; agent discovery manifest
  skills-index.json         # generated; minimal discovery manifest
  embeddings/               # optional ANN vectors (tiny)
/skills/
  <skill-slug>/
    SKILL.md                # required (Anthropic format)
    examples/               # 1–2 tiny files (≤30 lines each)
    resources/              # small linked templates/schemas
    scripts/                # optional helpers
    CHANGELOG.md
/tests/
  evals_<slug>.yaml         # 3–5 tiny scenarios per skill
  evals_agent_<slug>.yaml   # 3–5 scenarios per agent
/tooling/
  validate_skill.py         # schema/format/secret/token checks
  validate_agent.py         # agent spec validation
  build_index.py            # generates skills index; optional embeddings
  build_agent_index.py      # generates agents index
  lint_skill.py             # headings/order/links (optional)
/.github/workflows/
  skills-ci.yaml            # validate → lint → index → evals
  agents-ci.yaml            # validate → build agent index → run agent evals
```

Rules:

* **One skill per folder** with a single `SKILL.md`.
* **One agent per folder** with a single `AGENT.md`.
* Always include a **`.gitkeep`** in otherwise-empty directories.
* Prefer **editing** existing skills/agents over creating new ones.

---

## 2A) Naming Convention Standards (3-Tier Taxonomy)

**Slug Format: `{domain}-{scope}-{action}` (domain-first)**

All skills and agents must follow a **domain-first naming convention** for discoverability, hierarchy, and intelligent routing.

**Tier 1: Core/Foundation Skills**

Skills that are meta-capabilities or cross-cutting infrastructure.

* **Prefix**: `core-*`
* **When to use**: Skill/agent authoring, LLM delegation, repository tooling
* **Examples**: `core-skill-authoring`, `core-agent-authoring`, `core-codex-delegator`, `core-gemini-delegator`

**Tier 2: Domain Skills**

Skills that apply to high-level domain activities.

* **Format**: `{domain}-{scope}-{action}`
* **Domains**: `security`, `testing`, `cloud`, `devops`, `compliance`, `frontend`, `data`, `observability`, `finops`, `resilience`, `documentation`, `quality`, `integration`, `tooling`
* **Examples**:
  * Security: `security-appsec-validator`, `security-cloud-analyzer`, `security-iam-reviewer`
  * Testing: `testing-unit-generator`, `testing-integration-designer`, `testing-load-designer`
  * Cloud: `cloud-aws-architect`, `cloud-multicloud-advisor`, `cloud-edge-architect`
  * DevOps: `devops-cicd-generator`, `devops-iac-generator`, `devops-drift-detector`

**Tier 3: Specialized/Technology-Specific Skills**

Skills requiring deep expertise in specific technologies.

* **Format**: `{technology}-{scope}-{action}` or `{domain}-{technology}-{action}`
* **When to use**: Kubernetes, database, API patterns, specific compliance frameworks
* **Examples**:
  * Kubernetes: `kubernetes-helm-builder`, `kubernetes-servicemesh-configurator`
  * Compliance: `compliance-fedramp-validator`, `compliance-oscal-validator`
  * API: `api-graphql-designer`
  * Database: `database-migration-generator`

**18 Standardized Action Suffixes (in precedence order)**

Use these suffixes consistently. Prefer higher-precedence suffixes when ambiguous:

1. `orchestrator` — multi-skill coordinator (agents only)
2. `architect` — high-level design and structure
3. `designer` — detailed design and patterns
4. `composer` — combines multiple components
5. `builder` — constructs artifacts from specifications
6. `generator` — produces code/config from inputs
7. `validator` — checks correctness against rules
8. `analyzer` — evaluates and provides insights
9. `checker` — verifies specific conditions
10. `assessor` — measures maturity/compliance level
11. `calculator` — computes metrics/values
12. `optimizer` — improves performance/cost
13. `detector` — identifies issues/drift
14. `reviewer` — evaluates quality/security
15. `configurator` — sets up tools/systems
16. `integrator` — connects platforms/services
17. `advisor` — provides strategic guidance
18. `delegator` — routes work to external systems

**Agent Naming Convention**

* **Format**: `{domain}-orchestrator` (always ends in `-orchestrator`)
* **Exception**: Core agents like `agent-creator` may use different patterns
* **Examples**: `cloud-aws-orchestrator`, `security-auditor`, `devops-pipeline-orchestrator`

**Naming Decision Matrix**

| If skill... | Use tier | Format | Example |
|-------------|----------|--------|---------|
| Creates/manages skills/agents | Tier 1 | `core-{action}` | `core-skill-authoring` |
| Delegates to external LLMs | Tier 1 | `core-{system}-delegator` | `core-codex-delegator` |
| Applies to broad domain | Tier 2 | `{domain}-{scope}-{action}` | `security-appsec-validator` |
| Technology-specific | Tier 3 | `{tech}-{scope}-{action}` | `kubernetes-helm-builder` |
| Compliance framework | Tier 3 | `compliance-{framework}-{action}` | `compliance-fedramp-validator` |

**Routing Strategy**

The naming convention enables intelligent skill selection:

1. **Domain matching**: Extract domain from user request → filter skills by domain prefix
2. **Scope narrowing**: Identify specific technology (e.g., Kubernetes) → prefer Tier 3 specialized skills
3. **Action selection**: Match user intent to action suffix (e.g., "validate" → `*-validator` skills)
4. **Fallback**: If no specialized skill exists, route to domain-level skill or orchestrator agent

**Discoverability Rules**

* All security skills start with `security-*` → easily grep/filter
* All testing skills start with `testing-*` → quick test tooling discovery
* All Kubernetes skills contain `kubernetes-` → technology-specific grouping
* All orchestrators end with `-orchestrator` → instant agent identification

**Renaming Checklist** (when standardizing existing skills)

* [ ] Update skill slug in SKILL.md front-matter
* [ ] Rename directory: `skills/{old-slug}/ → skills/{new-slug}/`
* [ ] Update `index/skills-index.json` entry
* [ ] Update all cross-references in other SKILL.md/AGENT.md files
* [ ] Rename test file: `tests/evals_{old-slug}.yaml → tests/evals_{new-slug}.yaml`
* [ ] Run `python tooling/validate_skill.py` to verify
* [ ] Update any README or documentation referencing the old slug

---

## 2B) Code Quality & TDD Standards (enforced)

**Philosophy: Quality is Non-Negotiable**

All code in this repository — whether Python validation scripts, skill examples, or agent workflows — must meet production-grade standards. No exceptions.

### TDD (Test-Driven Development)

**Hard Rules:**

1. **Tests first.** Write the test before the implementation.
2. **Red → Green → Refactor.** Prove the test fails, make it pass, clean up the code.
3. **100% coverage for tooling scripts.** Every validation script, build tool, and CI helper must have tests.
4. **3-5 test scenarios minimum** for every skill/agent (in `tests/evals_*.yaml`).

**Test Organization:**

```
/tests/
  unit/                    # Fast, isolated tests (pytest, jest, etc.)
    test_validate_skill.py
    test_build_index.py
  integration/             # Multi-component tests
    test_skill_workflow.py
  evals_<slug>.yaml        # Skill/agent evaluation scenarios
```

**Test Quality Gates:**

* **Coverage**: ≥80% for tooling scripts (measured by pytest-cov, coverage.py)
* **Speed**: Unit tests complete in <5s total
* **Isolation**: No network calls, no file I/O without mocks
* **Determinism**: Tests pass reliably, no flaky tests tolerated

### Linting & Formatting

**Python (for validation scripts, build tools):**

* **Formatter**: `black` (line length: 100)
* **Linter**: `ruff` (replaces flake8, pylint, isort)
* **Type checker**: `mypy --strict`
* **Import sorter**: Built into `ruff`

**Configuration** (`pyproject.toml`):

```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP", "S", "B", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "PYI", "Q", "RSE", "RET", "SIM", "TID", "ARG", "PLE", "PLW", "RUF"]
ignore = ["E501"]  # Black handles line length

[tool.mypy]
strict = true
warn_unused_configs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

**JavaScript/TypeScript (for skill examples):**

* **Formatter**: `prettier`
* **Linter**: `eslint` with TypeScript plugin
* **Type checker**: `tsc --noEmit` (strict mode)

**Configuration** (`.eslintrc.json`):

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/strict",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

**Shell Scripts:**

* **Linter**: `shellcheck`
* **Formatter**: `shfmt -i 2 -ci`

### Security Scanning

**Python Dependencies:**

```bash
# Run on every PR
pip-audit --strict
safety check --json
```

**JavaScript/TypeScript Dependencies:**

```bash
npm audit --audit-level=moderate
# OR
pnpm audit --prod
```

**Secret Detection:**

```bash
# Pre-commit hook
gitleaks detect --no-git --verbose
```

**Code Scanning:**

* **Python**: `bandit -r tooling/ -ll`  # Only high/medium severity
* **JavaScript**: ESLint security plugins automatically enabled

**Container Images** (if applicable):

```bash
docker scout cves <image>
trivy image --severity HIGH,CRITICAL <image>
```

### Dependency Management

**Latest Stable Versions:**

* Pin **major versions** in production dependencies
* Allow **minor/patch updates** via lockfiles
* Review updates **monthly** via Dependabot or Renovate

**Python** (`pyproject.toml`):

```toml
[project]
dependencies = [
  "pyyaml>=6.0,<7.0",      # Allow minor updates
  "pydantic>=2.0,<3.0",    # Pin major version
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "black>=24.0",
  "ruff>=0.3",
  "mypy>=1.9",
]
```

**JavaScript** (`package.json`):

```json
{
  "dependencies": {
    "react": "^18.3.0",        // Caret allows minor updates
    "typescript": "~5.5.0"     // Tilde allows patch updates
  },
  "devDependencies": {
    "eslint": "^8.57.0",
    "prettier": "^3.2.0"
  }
}
```

**Lockfile Discipline:**

* **Python**: Commit `uv.lock` or `poetry.lock`
* **JavaScript**: Commit `pnpm-lock.yaml` or `package-lock.json`
* **Never** commit `node_modules/` or `__pycache__/`
* **Always** run `pip install` or `npm ci` (not `npm install`) in CI

### Pre-Commit Hooks

**Configuration** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-pyyaml]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.2
    hooks:
      - id: gitleaks

  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: v0.10.0
    hooks:
      - id: shellcheck
```

**Install**:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Verify setup
```

### CI/CD Quality Gates

**GitHub Actions Workflow** (`.github/workflows/quality.yaml`):

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  python-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -e .[dev]

      - name: Lint
        run: ruff check tooling/ tests/

      - name: Type check
        run: mypy tooling/ tests/

      - name: Format check
        run: black --check tooling/ tests/

      - name: Test
        run: pytest --cov=tooling --cov-report=xml --cov-fail-under=80

      - name: Security scan
        run: |
          pip-audit --strict
          bandit -r tooling/ -ll

  typescript-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm eslint

      - name: Type check
        run: pnpm tsc --noEmit

      - name: Test
        run: pnpm test --coverage

      - name: Security scan
        run: pnpm audit --prod
```

### Code Review Checklist (Beyond Auto-Checks)

Before merging **any** PR:

* [ ] Tests exist and pass (both unit and evals)
* [ ] Coverage ≥80% for new tooling code
* [ ] No linting errors (ruff, eslint)
* [ ] Type checking passes (mypy --strict, tsc --noEmit)
* [ ] Security scan clean (pip-audit, npm audit, gitleaks)
* [ ] Dependencies are latest stable versions
* [ ] Lockfiles committed (uv.lock, pnpm-lock.yaml)
* [ ] Code follows Smart Brevity style (no preamble/postamble)
* [ ] Examples are ≤30 lines
* [ ] All claims have sources with access dates
* [ ] No secrets or PII in code/config/comments

### Enforcement Priorities

**P0 (Block merge):**
* Linting errors
* Type checking failures
* Test failures
* Security vulnerabilities (HIGH/CRITICAL)
* Secrets detected

**P1 (Must fix before next release):**
* Coverage <80%
* Medium security vulnerabilities
* Outdated dependencies (>3 months old)

**P2 (Technical debt, track but don't block):**
* Code complexity warnings
* Low security vulnerabilities
* Minor documentation gaps

### Tools Installation

**Quick setup** (run once per development environment):

```bash
# Python tooling
pip install uv
uv pip install black ruff mypy pytest pytest-cov pip-audit bandit pre-commit

# JavaScript tooling (if working with TS/JS examples)
npm install -g pnpm
pnpm add -D eslint prettier typescript @typescript-eslint/parser

# Security scanning
pip install gitleaks

# Pre-commit hooks
pre-commit install
```

**Verify setup**:

```bash
black --version     # Should be ≥24.0
ruff --version      # Should be ≥0.3
mypy --version      # Should be ≥1.9
pytest --version    # Should be ≥8.0
```

---

## 3) What a Good Skill Looks Like (LLM-optimized)

**Front-matter (required keys)**
`name, slug, description (≤160), capabilities, inputs, outputs, keywords, version, owner, license, security, links`

**Body (required sections in this order)**

1. `## Purpose & When-To-Use` — trigger conditions; crisp
2. `## Pre-Checks` — `NOW_ET`, input schema sanity, source freshness checks
3. `## Procedure` — **Tiered**: T1 fast path → T2 extended → T3 deep dive
4. `## Decision Rules` — ambiguity thresholds, abort/stop conditions
5. `## Output Contract` — explicit schema/types + required fields
6. `## Examples` — **≤30 lines** runnable or precise pseudo-code
7. `## Quality Gates` — token budgets, safety, auditability, determinism
8. `## Resources` — **links only**, no long paste-ins

**Token budgets (mandatory)**

* **T1 ≤ 2k tokens** — common 80% case; no heavy retrieval
* **T2 ≤ 6k tokens** — extra validation + 2–4 sources
* **T3 ≤ 12k tokens** — deep research, rationale, and eval generation

**Examples**

* One small, representative I/O example (≤30 lines).
* Longer samples live in `resources/` or external repos.

**Progressive disclosure**

* Keep metadata tiny. Put heavy details under Procedure/Resources and load only when needed.

---

## 3A) What a Good Agent Looks Like (Orchestrator Pattern)

**Definition**

An **Agent** is a multi-step orchestrator that coordinates 2+ **Skills** through a command-driven workflow. Agents operate in separate context (system prompt), while Skills are invoked inline by the model.

**When to Use Agent vs Skill (Decision Framework)**

| Characteristic | Skill | Agent |
|----------------|-------|-------|
| Steps | ≤2 | 4 (orchestration) |
| Invocation | Model (natural language) | User (command) |
| Context | Shares main | Separate |
| Token budget | T1/T2/T3 (≤12k) | System prompt ≤1500 |
| Purpose | Single capability | Multi-skill coordination |

**Decision Rules:**

* **Use a Skill** when the task is self-contained, has ≤2 steps, and fits T1/T2/T3 token tiers.
* **Use an Agent** when the task requires orchestrating multiple skills, maintaining workflow state, or executing a standard 4-step pattern.

**Required AGENT.md Structure (8 sections)**

1. `## Agent Metadata` — name, slug, description (≤160), version, owner, license
2. `## Purpose & Trigger` — when to invoke this agent (command pattern)
3. `## System Prompt` — **≤1500 tokens**, role definition, decision authority, constraints
4. `## Workflow` — standard 4-step pattern (see below)
5. `## Skill Integration` — which skills to call, reference by slug only, invocation pattern
6. `## Examples` — **≤30 lines** per example, 1–2 representative interactions
7. `## Quality Gates` — system prompt token budget, workflow determinism, safety
8. `## Resources` — links only, no embedded content

**System Prompt Requirements**

* **≤1500 tokens** (measured via `tiktoken` cl100k_base)
* Define role, decision authority, and constraints
* Include abort conditions and error handling
* Specify output format and success criteria

**4-Step Workflow Pattern (Standard)**

All agents must implement this structure:

1. **Plan** — Parse user request, identify required skills, validate inputs
2. **Execute** — Invoke skills in sequence, handle intermediate results
3. **Validate** — Check outputs against quality gates, verify success criteria
4. **Report** — Return structured results, log decisions, handle errors

**Skill Integration**

* Reference skills by **slug only** (e.g., `oscal-ssp-validate`, not inline code)
* Use skill routing: load `/index/skills-index.json` to resolve slug → path
* Pass skill inputs/outputs explicitly (no implicit context sharing)
* Handle skill failures gracefully (retry logic, fallbacks)

**Examples Requirements**

* **≤30 lines** per interaction example
* Show complete workflow: user command → plan → execute → validate → report
* Include both success and failure scenarios
* Longer examples in `examples/` directory

**Required Directory Structure**

```
/agents/<agent-slug>/
  AGENT.md                # agent specification
  examples/               # 1–2 interaction examples (≤30 lines each)
  workflows/              # optional multi-step procedure definitions
  CHANGELOG.md            # version history
```

**Quality Gates**

* System prompt ≤1500 tokens (strict)
* All skill references resolvable via index
* 4-step workflow present and deterministic
* Examples execute successfully (or marked as pseudo-code)
* No secrets or PII in agent definition or examples

---

## 4) Research & Citations

**Source Hierarchy (strict precedence)**

1. **Primary/official**: product docs, RFCs, NIST publications, W3C specs
2. **Authoritative secondary**: GitHub repos (official maintainers), Apache/Linux Foundation docs
3. **Reputable technical**: high-quality blogs with named authors, established tutorial sites
4. **Community**: Stack Overflow (with vote threshold ≥10), Reddit (with caution)

**Never acceptable**: paywalled sources, link-rotted URLs, unverifiable claims, LLM-generated summaries without primary source.

**Every claim** that could change or be disputed must include a **clickable hyperlink** + **access date = `NOW_ET`**.

**Verification checklist (expanded)**:

* [ ] Source is from tier 1–3 in hierarchy above
* [ ] Link works and content is publicly accessible
* [ ] Source explicitly states what you claim (no inference leaps)
* [ ] Numbers/metrics include scope, method, and context
* [ ] If version-specific (API, schema, etc.), version is captured
* [ ] If time-sensitive, access date = `NOW_ET` is present
* [ ] If multiple sources conflict, note the conflict and use the most authoritative

**Example (inline):**

> "OSCAL profile validation requires schema/version alignment (accessed `NOW_ET`): <link>"

---

## 4A) Technical Accuracy Requirements

**For version numbers, API signatures, command flags:**

* Copy **exact** syntax from official docs or `--help` output.
* Include version context: "as of v2.3.1 (accessed `NOW_ET`)" or "in Python 3.11+".
* If a feature varies across versions, specify the range or mark uncertainty: `[TODO: verify flag support in v1.x vs v2.x]`.

**For code examples:**

* All runnable examples must be **tested** or marked as pseudo-code.
* Provide interpreter/runtime version: "Tested with Python 3.11.5" or "Node.js 20.x".
* If using library-specific syntax, include import statements and library version.

**For quantitative claims:**

* Always cite the measurement method: "≤2k tokens (measured via `tiktoken` cl100k_base)".
* If benchmarking, specify: environment, sample size, date, and tooling.
* Avoid vague terms like "fast," "small," or "efficient" without numbers or context.

**For schema/data structures:**

* Never invent field names. Copy from official JSON Schema, OpenAPI spec, or authoritative docs.
* If showing a subset, mark clearly: "Partial schema; see <link> for full spec".
* Validate examples against schema if available (or note: "Schema validation pending").

**Error-handling stance:**

* If you cannot verify a claim in ≤3 minutes, **do not include it**.
* Mark ambiguity: `[TODO: confirm X with source Y]` and stop or defer to T3 research.
* Never "round up" version numbers, dates, or counts to make documentation cleaner.

---

## 5) The Skill-Creation Skill (meta-skill expectations)

When invoked to create a new skill from a topic, the meta-skill must:

* Generate **complete** `skills/<slug>/SKILL.md` using §3 format.
* Output **one** short example and **tests/evals_<slug>.yaml** (3–5 scenarios).
* Emit an **index entry JSON** for `/index/skills-index.json`.
* Include **2–4 sources** for T2+ with titles, URLs, and access dates.
* Refuse to proceed and emit **TODOs** if required inputs or schemas are missing.

---

## 6) Indexing & Routing (minimal)

* `/index/skills-index.json` contains: `slug, name, summary (≤160), keywords, owner, version, entry`.
* Optional embeddings over `name+summary+keywords` in `/index/embeddings/`.
* **Routing rule**: select **≤2** candidate skills per request. Do **not** shotgun-load the whole repo.

---

## 7) File Operations (agents must comply)

**Before write/edit**

1. Plan (1–3 bullets).
2. Check for existing targets; **no duplicates**.
3. Confirm paths under allowed tree (see §2).
4. Cite sources and compute `NOW_ET`.

**On uncertainty**

* Emit short **TODO** list with missing fields/schemas and **stop**.

**Never**

* Embed secrets or large quoted texts.
* Save working debris to root.
* Bypass validator.

---

## 8) CI Gates (merge blockers)

1. **Validation:** `tooling/validate_skill.py`

   * Required front-matter and sections present
   * `description ≤ 160`, example ≤ 30 lines
   * Token budgets T1/T2/T3 visible
   * Secret patterns check
   * Codeblock sane limits
   * **Accuracy checks**:
     * All URLs return HTTP 200 (or mark as `[TODO: verify link]`)
     * No bare version numbers without context (e.g., reject "v2.0" without source/date)
     * No `[TODO: ...]` markers in committed skills (must be resolved or removed)
     * All quantitative claims have units and method

2. **Lint:** `tooling/lint_skill.py` (order, links, headings)

3. **Index:** `tooling/build_index.py` (deterministic; no duplicate slugs)

4. **Evals:** run `tests/evals_<slug>.yaml` (basic pass/fail)

PRs fail if any step fails. Keep the pipeline fast.

---

## 8A) Repository Maintenance Standards (mandatory workflows)

**Philosophy: The Repository is a Living System**

Skills and agents are not static artifacts. The repository has interconnected systems (indices, coverage analysis, dependency graphs) that must be kept synchronized. Every addition, modification, or deletion triggers maintenance workflows.

### Coverage Matrix & Gap Analysis (required after changes)

**When to Update:**

* After adding **any** new skill or agent
* After deleting or deprecating skills/agents
* After major domain expansion (e.g., adding 3+ skills in new domain)
* At minimum: **monthly** audit cycle

**Rebuild Process:**

```bash
# Rebuild coverage matrix
python tooling/analyze_coverage.py

# Review output
cat docs/COVERAGE_MATRIX.md

# Update gap analysis manually if needed
# (The script updates counts, you update strategic gaps in "Gap Analysis" section)
```

**Coverage Matrix Requirements:**

* **Total counts accurate**: Skills, agents, per-domain breakdowns
* **Tier percentages current**: Core, Domain, Specialized distribution
* **Heat map reflects reality**: Top 10 domains by count
* **Gap analysis updated**: Mark completed high-priority items with ✅, add new gaps
* **Recent additions section**: Document what was added in latest expansion (with date)

**Gap Analysis Standards:**

* **Completed items stay visible**: Show what was recently addressed (builds momentum)
* **Priority triaging**: High (P0 gaps), Medium (P1), Low (P2) based on user demand + strategic value
* **Specific, actionable**: Not "improve testing" but "add mutation testing skill (Stryker, PIT)"
* **Technology-specific**: Call out exact tools/frameworks (Datadog, not "APM tool")

**Commit Requirements:**

```bash
git add docs/COVERAGE_MATRIX.md
git commit -m "docs(coverage): rebuild matrix after <expansion-name>

Updates:
- Total skills: <old> → <new> (+X)
- <Domain> expanded: <old> → <new> skills
- Gap analysis: marked <item> as completed
- Added <new-gap> to high priority
"
```

### Index Rebuilding (required after skill/agent changes)

**When to Rebuild:**

* After creating new skill → rebuild `skills-index.json`
* After creating new agent → rebuild `agents-index.json`
* After renaming skill/agent → rebuild both indices
* After deleting skill/agent → rebuild and verify no dangling references

**Rebuild Commands:**

```bash
# Skills index (always run after skill changes)
python tooling/build_index.py
# Output: index/skills-index.json updated

# Agents index (implicit via agent tooling, or manual)
# Usually auto-updated when agent added to agents/ directory
# Verify: cat index/agents-index.json | jq length

# With embeddings (optional, for semantic search)
python tooling/build_index.py --with-embeddings
```

**Index Validation:**

```bash
# Verify no duplicate slugs
jq -r '.[].slug' index/skills-index.json | sort | uniq -d
# Should be empty

jq -r '.[].slug' index/agents-index.json | sort | uniq -d
# Should be empty

# Verify all skills/agents present
ls -1 skills/ | wc -l  # Should match jq length of skills-index.json
ls -1 agents/ | wc -l  # Should match jq length of agents-index.json
```

**Commit Index Updates:**

* **Always commit index updates** in the same commit as skill/agent additions
* Indices are **generated artifacts** but **version controlled** (enables fast routing without rebuild)

### Agent Dependency Analysis (required after agent changes)

**When to Run:**

* After creating new agent
* After modifying agent's skill references
* After renaming or deleting skills (to find broken agent references)
* **Monthly** as part of audit cycle

**Analysis Command:**

```bash
python tooling/analyze_agent_dependencies.py
# Generates: docs/AGENT_DEPENDENCIES.md
```

**Dependency Graph Outputs:**

* **Agent → Skill mapping**: Which skills each agent orchestrates
* **Skill usage**: Which agents reference each skill (reverse mapping)
* **Orphaned skills**: Skills not referenced by any agent (user-invoked or routing-based)
* **Heavily referenced skills**: Skills used by multiple agents (critical dependencies)
* **Mermaid diagram**: Visual dependency graph

**Orphaned Skill Triage:**

Orphaned skills are **not necessarily bad**:

* ✅ **Expected orphans**: Direct user-invoked skills (testing-unit-generator, rust-analyzer)
* ✅ **Routing-based**: Skills selected by routing logic, not hardcoded in agents
* ⚠️ **Potential gaps**: If a skill should be orchestrated but isn't, consider creating an agent

**Broken Reference Detection:**

```bash
# Find skills referenced in agents but don't exist
python tooling/analyze_agent_dependencies.py 2>&1 | grep -i "not found"

# Manual check: search for backtick-slugs in AGENT.md files
grep -r '`[a-z-]*`' agents/ | grep -v ".git"
```

**Commit Dependency Updates:**

```bash
git add docs/AGENT_DEPENDENCIES.md
git commit -m "docs(deps): rebuild agent dependency graph

Updates:
- <agent-name> now orchestrates <skill-1>, <skill-2>
- <skill-name> used by <count> agents
- Orphaned skills: <count> (reviewed, intentional)
"
```

### Directory Structure Validation

**Required Empty Directory Markers:**

Every otherwise-empty directory **must** contain a `.gitkeep` file:

```bash
# Check for missing .gitkeep files
find skills/ agents/ -type d -empty ! -path "*/\.*"
# Should be empty (all empty dirs have .gitkeep)

# Auto-fix missing .gitkeep
find skills/ agents/ -type d -empty -exec touch {}/.gitkeep \;
```

**Standard Directory Structure Per Skill:**

```
skills/<slug>/
  SKILL.md              # Required
  CHANGELOG.md          # Required
  examples/             # Optional (but .gitkeep if empty)
    .gitkeep
  resources/            # Optional (but .gitkeep if empty)
    .gitkeep
  scripts/              # Optional (but .gitkeep if empty)
    .gitkeep
```

**Standard Directory Structure Per Agent:**

```
agents/<slug>/
  AGENT.md              # Required
  CHANGELOG.md          # Required
  examples/             # Optional (but .gitkeep if empty)
    .gitkeep
  workflows/            # Optional (but .gitkeep if empty)
    .gitkeep
  resources/            # Optional (but .gitkeep if empty)
    .gitkeep
  scripts/              # Optional (but .gitkeep if empty)
    .gitkeep
```

### CHANGELOG Standards

**Required Format** (Keep-a-Changelog style):

```markdown
# Changelog

## [Unreleased]

### Added
- New capability X
- Support for Y

### Changed
- Improved Z performance

### Deprecated
- Feature W will be removed in v2.0

### Removed
- Obsolete feature V

### Fixed
- Bug in edge case Q

## [1.2.0] - 2025-10-26

### Added
- Feature A
- Feature B
```

**Version Bumping Rules:**

* **Major (X.0.0)**: Breaking changes to inputs, outputs, or behavior
* **Minor (1.X.0)**: New features, new capabilities, backward-compatible
* **Patch (1.2.X)**: Bug fixes, documentation improvements, no functional changes

**Changelog Update Timing:**

* Update CHANGELOG.md **in the same commit** as the feature/fix
* Move `[Unreleased]` section to versioned section on release
* Always keep `[Unreleased]` header present for next changes

### Post-Addition Workflow (checklist after adding skill/agent)

**After adding a new skill:**

```bash
# 1. Validate
python tooling/validate_skill.py

# 2. Rebuild skills index
python tooling/build_index.py

# 3. Rebuild coverage matrix
python tooling/analyze_coverage.py

# 4. Update gap analysis in COVERAGE_MATRIX.md (manual)
#    - Mark completed items with ✅
#    - Add new gaps discovered
#    - Re-prioritize if needed

# 5. Verify directory structure
ls -la skills/<slug>/  # Should have SKILL.md, CHANGELOG.md, .gitkeep in empty dirs

# 6. Commit all updates together
git add skills/<slug>/ tests/evals_<slug>.yaml index/skills-index.json docs/COVERAGE_MATRIX.md
git commit -m "feat(skill): add <slug> skill

<Description>

Validation: All checks pass
Coverage: <domain> expanded from <X> to <Y> skills
"
```

**After adding a new agent:**

```bash
# 1. Validate agent spec (if validator exists)
python tooling/validate_agent.py  # If available

# 2. Rebuild agents index
# (Usually auto-updated, verify manually)
cat index/agents-index.json | jq '.[] | select(.slug=="<slug>")'

# 3. Rebuild agent dependency graph
python tooling/analyze_agent_dependencies.py

# 4. Rebuild coverage matrix
python tooling/analyze_coverage.py

# 5. Update gap analysis (manual)

# 6. Verify directory structure
ls -la agents/<slug>/  # Should have AGENT.md, CHANGELOG.md, .gitkeep in empty dirs

# 7. Commit all updates together
git add agents/<slug>/ index/agents-index.json docs/AGENT_DEPENDENCIES.md docs/COVERAGE_MATRIX.md
git commit -m "feat(agent): add <slug> orchestrator

<Description>

Dependencies: Orchestrates <skill-1>, <skill-2>, ...
Coverage: <domain> orchestrators expanded
"
```

**After renaming skill/agent:**

```bash
# 1. Rename directory
mv skills/<old-slug> skills/<new-slug>

# 2. Update SKILL.md front-matter slug

# 3. Update all cross-references (search repo)
grep -r "<old-slug>" skills/ agents/ docs/

# 4. Rename test file
mv tests/evals_<old-slug>.yaml tests/evals_<new-slug>.yaml

# 5. Rebuild indices
python tooling/build_index.py

# 6. Rebuild dependency graph (if agent)
python tooling/analyze_agent_dependencies.py

# 7. Rebuild coverage matrix
python tooling/analyze_coverage.py

# 8. Verify no dangling references
grep -r "<old-slug>" skills/ agents/ docs/ index/
# Should be empty

# 9. Commit with clear rename message
git add -A
git commit -m "refactor(<domain>): rename <old-slug> to <new-slug>

Rationale: <why>

Updated:
- Skill/agent slug and directory
- Test file
- All cross-references
- Indices and coverage matrix
"
```

**After deleting skill/agent:**

```bash
# 1. Check for dependencies (if agent)
python tooling/analyze_agent_dependencies.py
# Ensure no agents reference this skill

# 2. Remove directory
rm -rf skills/<slug>  # or agents/<slug>

# 3. Remove test file
rm tests/evals_<slug>.yaml

# 4. Rebuild indices
python tooling/build_index.py

# 5. Rebuild dependency graph
python tooling/analyze_agent_dependencies.py

# 6. Rebuild coverage matrix
python tooling/analyze_coverage.py

# 7. Update gap analysis
#    - If skill addressed a gap, move gap back to "Missing"
#    - Document deprecation reason

# 8. Commit with deprecation note
git add -A
git commit -m "chore(<domain>): deprecate <slug>

Reason: <why deprecated>

Impact:
- <domain> skills reduced from <X> to <Y>
- Gap analysis updated
- No dependent agents affected (verified)
"
```

### Cross-Reference Validation

**Agent → Skill Reference Rules:**

* Agents reference skills by **slug only** (backtick-enclosed: `skill-slug`)
* All skill references **must resolve** via skills-index.json
* **No inline skill definitions** in agents (always use skill routing)

**Validation Process:**

```bash
# Extract all backtick-slugs from agents
grep -ohr '`[a-z0-9-]\+`' agents/ | sort -u > /tmp/agent-refs.txt

# Extract all skill slugs from index
jq -r '.[].slug' index/skills-index.json | sort > /tmp/skill-slugs.txt

# Find unresolved references (agent refs not in skill index)
comm -23 /tmp/agent-refs.txt /tmp/skill-slugs.txt
# Investigate anything that looks like a skill slug (has hyphens, lowercase)
```

**Broken Reference Remediation:**

* If skill was renamed: update agent to use new slug
* If skill was deleted: remove reference or add skill back
* If typo: fix slug in agent
* If skill doesn't exist yet: create skill or mark as `[TODO: create <slug> skill]`

### Documentation Completeness

**Required Documentation Files:**

```
/docs/
  COVERAGE_MATRIX.md       # Domain coverage analysis
  AGENT_DEPENDENCIES.md    # Agent→skill dependency graph
  ARCHITECTURE.md          # (Optional) High-level repo architecture
  CONTRIBUTING.md          # (Optional) Contributor onboarding
```

**Documentation Quality Standards:**

* **Auto-generated docs** (COVERAGE_MATRIX.md, AGENT_DEPENDENCIES.md) are **committed** (not gitignored)
* All docs use **Smart Brevity** style (see §1A)
* Stats/counts in docs must be **current** (rebuild after changes)
* Links in docs must **resolve** (no 404s, no link rot)

### Audit Cycle (monthly maintenance)

**Monthly Audit Checklist** (first Monday of month):

```bash
# 1. Rebuild all indices
python tooling/build_index.py
python tooling/build_index.py --with-embeddings  # If using semantic search

# 2. Rebuild coverage matrix
python tooling/analyze_coverage.py

# 3. Rebuild agent dependencies
python tooling/analyze_agent_dependencies.py

# 4. Validate all skills
python tooling/validate_skill.py

# 5. Check for orphaned files
find skills/ agents/ -name "*.md" ! -name "SKILL.md" ! -name "AGENT.md" ! -name "CHANGELOG.md" ! -name "README.md"
# Investigate unexpected .md files

# 6. Check for missing CHANGELOGs
find skills/ agents/ -mindepth 1 -maxdepth 1 -type d ! -exec test -e '{}/CHANGELOG.md' \; -print
# Should be empty

# 7. Verify .gitkeep presence
find skills/ agents/ -type d -empty ! -name ".git" ! -exec test -e '{}/.gitkeep' \; -print
# Should be empty

# 8. Update LAST_AUDIT timestamp in CLAUDE.md
# Update to NOW_ET, set NEXT_REVIEW = +90 days

# 9. Commit audit results
git add -A
git commit -m "chore(audit): monthly repository maintenance

Audit date: $(date -I)

Updated:
- Skills index
- Coverage matrix
- Agent dependency graph
- Validated all skills (X passing)
- Verified directory structure
- Updated CLAUDE.md audit timestamps
"
```

### Version-Controlled vs Generated Files

**Version Controlled (commit these):**

* ✅ `index/skills-index.json` (enables fast routing)
* ✅ `index/agents-index.json` (enables agent discovery)
* ✅ `docs/COVERAGE_MATRIX.md` (shows project health)
* ✅ `docs/AGENT_DEPENDENCIES.md` (shows orchestration map)
* ⚠️ `index/embeddings/` (optional, can be regenerated)

**Gitignored (regenerate on demand):**

* ❌ `__pycache__/` (Python bytecode)
* ❌ `node_modules/` (JS dependencies)
* ❌ `.pytest_cache/` (Test cache)
* ❌ `.coverage` (Coverage data)
* ❌ `*.pyc` (Python compiled)

### Enforcement in CI

**Pre-Commit Hooks (local enforcement):**

```yaml
# .pre-commit-config.yaml additions for repo maintenance

- repo: local
  hooks:
    - id: validate-directory-structure
      name: Validate skill/agent directory structure
      entry: bash -c 'find skills/ agents/ -type d -empty ! -path "*/\.*" -exec test -e {}/.gitkeep \; || exit 1'
      language: system
      pass_filenames: false

    - id: rebuild-indices
      name: Rebuild indices if skills/agents changed
      entry: bash -c 'git diff --cached --name-only | grep -qE "^(skills|agents)/" && python tooling/build_index.py || exit 0'
      language: system
      pass_filenames: false
```

**GitHub Actions (CI enforcement):**

```yaml
# .github/workflows/repo-maintenance.yaml

name: Repository Maintenance

on:
  pull_request:
    paths:
      - 'skills/**'
      - 'agents/**'

jobs:
  validate-repo-state:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check indices are current
        run: |
          python tooling/build_index.py --check
          # --check flag: rebuild in temp, diff with committed, fail if different

      - name: Check for missing .gitkeep
        run: |
          missing=$(find skills/ agents/ -type d -empty ! -path "*/\.*" ! -exec test -e {}/.gitkeep \; -print)
          if [ -n "$missing" ]; then
            echo "Missing .gitkeep files in: $missing"
            exit 1
          fi

      - name: Validate cross-references
        run: |
          python tooling/validate_cross_references.py  # If tool exists
```

---

## 9) Small, Reusable Agent Prompts

**A) Author a new Skill**

```
Goal: Create a new Skill for <TOPIC>.

Rules:
- Normalize time to NOW_ET (NIST/time.gov semantics).
- Use the exact section order in CLAUDE.md §3.
- Keep metadata tiny; one example ≤30 lines.
- Include token budgets (T1/T2/T3) and 2–4 sources (with access dates) for T2+.
- Emit index_entry JSON and tests/evals_<slug>.yaml.
- If required inputs/schemas are missing, output TODOs and stop.

Deliverables:
- skills/<slug>/SKILL.md
- skills/<slug>/examples/<slug>-example.txt
- tests/evals_<slug>.yaml
- index_entry (JSON)
```

**B) Edit an existing Skill**

```
Goal: Improve <slug> without increasing token footprint.

Rules:
- Prefer edits over new files.
- Maintain section order and token budgets.
- Strengthen decision rules and examples; keep example ≤30 lines.
- Verify/refresh citations with NOW_ET.

Deliverable:
- Diff-ready patch + concise commit message.
```

**C) Router (selection)**

```
Goal: Pick ≤2 relevant skills for "<USER_TASK>".

Input: index/skills-index.json (and optional embeddings).
Output: the best 1–2 slugs with a one-line justification each.
Do not open SKILL.md unless requested.
```

---

## 10) PR Checklist (must self-certify)

**Content Quality:**

* [ ] `NOW_ET` computed; used for access dates
* [ ] No secrets or PII; no long pasted sources
* [ ] Required sections and front-matter keys present
* [ ] Example ≤30 lines; token budgets present (T1/T2/T3)
* [ ] **Accuracy requirements (§4A)**:
  * [ ] All version numbers include context (source, date, or version range)
  * [ ] All code examples specify runtime/interpreter version
  * [ ] All quantitative claims cite measurement method and units
  * [ ] All schema fields copied from authoritative source (no invention)
  * [ ] No `[TODO: ...]` markers in committed content
* [ ] **Citations (§4)**:
  * [ ] All links resolve and return HTTP 200
  * [ ] All claims traceable to tier 1–3 sources (see §4 hierarchy)
  * [ ] All sources explicitly state what is claimed (no inference leaps)
  * [ ] Access dates = `NOW_ET` for all time-sensitive or version-specific content

**Repository Maintenance (§8A):**

* [ ] **Indices rebuilt** (if adding/modifying/deleting skills or agents):
  * [ ] `python tooling/build_index.py` executed
  * [ ] `index/skills-index.json` and/or `index/agents-index.json` updated
  * [ ] No duplicate slugs (verified via `jq -r '.[].slug' index/*.json | sort | uniq -d`)
* [ ] **Coverage matrix updated** (if adding/deleting skills or agents):
  * [ ] `python tooling/analyze_coverage.py` executed
  * [ ] `docs/COVERAGE_MATRIX.md` counts accurate (total skills, per-domain)
  * [ ] Gap analysis section updated (mark completed items with ✅, add new gaps)
  * [ ] Recent additions section includes this PR's changes
* [ ] **Agent dependencies updated** (if adding/modifying agents or deleting skills):
  * [ ] `python tooling/analyze_agent_dependencies.py` executed
  * [ ] `docs/AGENT_DEPENDENCIES.md` reflects current agent→skill mappings
  * [ ] No broken references (all agent-referenced skills exist)
* [ ] **Directory structure compliant**:
  * [ ] CHANGELOG.md present in skill/agent directory
  * [ ] `.gitkeep` present in empty directories (examples/, resources/, scripts/)
  * [ ] No orphaned files or unexpected directory structure
* [ ] **CHANGELOG updated** (in same commit):
  * [ ] Version bumped appropriately (major/minor/patch)
  * [ ] Changes documented under correct version section
  * [ ] Follows Keep-a-Changelog format

**Code Quality (§2B):**

* [ ] Evals added/updated and pass locally
* [ ] Pre-commit hooks pass (black, ruff, mypy, gitleaks)
* [ ] No linting errors, type errors, or security warnings
* [ ] Tests pass (if applicable)

**Git & Commit:**

* [ ] Commit message: clear, imperative, ≤72 chars first line
* [ ] Conventional Commits format: `type(scope): description`
* [ ] All generated artifacts committed (indices, coverage matrix, dependency graph)

---

## 11) Maintenance Cadence

* Update `LAST_AUDIT` during successful validation runs; set `NEXT_REVIEW = +90 days`.
* If a rule never triggers or isn’t useful, remove it. Keep this concise and enforceable.

---

## 12) Explicitly Out of Scope

* Website/11ty details, UI theming, and page-level SEO.
* Heavy multi-agent orchestration boilerplate.
* Large code samples in `SKILL.md` (link or place in `resources/` instead).

---

## 13) Git & GitHub Workflow (Required)

**Branch Strategy**

* **Never commit directly to `main`** — main branch is protected.
* Feature branch naming: `feature/<skill-slug>` or `feature/<component>`
  * Examples: `feature/oscal-ssp-validate`, `feature/index-builder`
* Hotfix branch naming: `hotfix/<issue-id>` (e.g., `hotfix/42`)
* Always branch from latest main: `git checkout main && git pull && git checkout -b feature/<name>`

**Commit Practices**

* **Atomic commits**: one logical change per commit.
* **Conventional Commits format**: `type(scope): description`
  * **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  * **Examples**:
    * `feat(skill): add oscal-ssp-validate skill`
    * `fix(validator): correct front-matter parsing`
    * `docs(readme): update quick start guide`
    * `test(evals): add edge cases for routing skill`
    * `chore(ci): update workflow timeout settings`
* **First line**: max 72 chars, imperative mood ("add", not "added")
* **Body** (optional): blank line separator, explain why/context
* **Reference issues/PRs**: use `Fixes #123` or `Relates to #456` in body

**GitHub CLI Integration**

* Create PR: `gh pr create --title "feat(skill): add new skill" --body "$(cat <<'EOF' ...)`
* Check PR status: `gh pr status`
* Monitor CI: `gh pr checks`
* Merge after approval: `gh pr merge --squash`
* View PR diff: `gh pr diff`

**PR Workflow (step-by-step)**

1. **Create feature branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/my-skill
   ```

2. **Make atomic commits**:
   ```bash
   # Work on skill
   git add skills/my-skill/SKILL.md
   git commit -m "feat(skill): add my-skill core structure"

   # Add examples
   git add skills/my-skill/examples/
   git commit -m "docs(skill): add my-skill examples"
   ```

3. **Push to remote**:
   ```bash
   git push -u origin feature/my-skill
   ```

4. **Create PR** (with template):
   ```bash
   gh pr create --title "feat(skill): add my-skill" --body "$(cat <<'EOF'
   ## Summary
   Adds my-skill for <purpose>. Implements T1/T2/T3 tiers with <token-budget>.

   ## Test Plan
   - [ ] Validator passes
   - [ ] Linter passes
   - [ ] Index builds
   - [ ] Evals run successfully

   ## Checklist (from §10)
   - [ ] NOW_ET computed and used
   - [ ] No secrets or PII
   - [ ] Required sections present
   - [ ] Example ≤30 lines
   - [ ] Token budgets visible
   - [ ] Links resolve
   - [ ] Index updated
   EOF
   )"
   ```

5. **Wait for CI** — all quality gates must pass (see §8)

6. **Review & merge**:
   * Self-review or request review
   * Address feedback with new commits
   * Squash-merge to main: `gh pr merge --squash`

**Quality Gates Before Merge** (automated in CI, see §8)

* All skills pass `tooling/validate_skill.py`
* All skills pass `tooling/lint_skill.py`
* Index builds successfully via `tooling/build_index.py`
* All evals have valid YAML syntax
* No secrets detected (pattern scan)
* PR template checklist completed

**Release Process**

* **Tag format**: `v<major>.<minor>.<patch>` (semantic versioning)
  * Breaking changes → bump major
  * New skills/features → bump minor
  * Fixes/docs → bump patch
* **Create annotated tag**:
  ```bash
  git tag -a v0.1.0 -m "Release v0.1.0: initial skills collection"
  git push origin v0.1.0
  ```
* **Create GitHub release**:
  ```bash
  gh release create v0.1.0 --title "v0.1.0" --notes "$(cat CHANGELOG.md)"
  ```

**Common Commands Quick Reference**

```bash
# Start new feature
git checkout main && git pull && git checkout -b feature/my-feature

# Amend last commit (before push)
git add . && git commit --amend --no-edit

# Sync feature branch with main
git checkout main && git pull
git checkout feature/my-feature
git rebase main

# View what will be pushed
git log origin/main..HEAD --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

### Final Word

Build **small, sharp Skills** with **clear triggers** and **tight outputs**. Cite precisely. Keep tokens down. When unsure, ask for inputs, list TODOs, and stop.
