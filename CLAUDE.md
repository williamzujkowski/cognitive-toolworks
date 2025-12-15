# CLAUDE.md — Authoritative Rules for the Skills Repository

```
STATUS: AUTHORITATIVE
VERSION: 1.7.0
LAST_AUDIT: 2025-12-14T19:45:00-05:00
NEXT_REVIEW: 2026-03-14T19:45:00-04:00
SCOPE: Personal/public Skills library (Anthropic Skills standard)
TOKEN_BUDGET: ≤6000 tokens (self-enforced)
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

## 0A) Context Budget Management (enforced limits)

**Philosophy**: Context is finite. Every token loaded reduces reasoning capacity. Load minimal, evict aggressively, measure constantly.

**Phase Budgets (strict)**

| Phase | Budget | Load |
|-------|--------|------|
| Discovery | ≤8k | Index files only (skills-index.json, agents-index.json) |
| Execution | ≤20k | Selected SKILL.md + minimal examples |
| Validation | ≤10k | Output schemas, quality gates, evals |
| Reporting | ≤5k | Output templates, summaries |

**Tier Budgets (per skill)**

* **T1**: ≤2k tokens (fast path, 80% of requests)
* **T2**: ≤6k tokens (extended validation)
* **T3**: ≤12k tokens (deep research)

**Violations**: P0 (abort): Discovery >8k, Execution >20k | P1 (warn): Validation >10k, Reporting >5k | P2 (log): Execution >15k

**Measurement**: `tiktoken` (cl100k_base) for all counts.

---

## 0B) Progressive Disclosure Strategy (load-on-demand)

**Never front-load. Load only what's needed.**

**Tier 0: Index-Only (Discovery)**
* `index/skills-index.json` + `index/agents-index.json` + user query
* **Total**: ≤1k tokens for routing decision

**Tier 1: Metadata + Fast Path (80% of requests)**
* Front-matter, Purpose, Pre-Checks, T1 Procedure, Output Contract
* **Skip**: examples, resources, T2/T3 procedures
* **Total**: ≤3k tokens

**Tier 2: Extended (15% of requests)**
* All T1 + T2 Procedure, Decision Rules, Quality Gates, **one** example
* **Total**: ≤8k tokens

**Tier 3: Deep Research (5% of requests)**
* All T2 + T3 Procedure, all examples, resources, evals
* **Total**: ≤15k tokens

**Disclosure Rules**
* Never load examples unless T2+ invoked
* Never load: resources (unless referenced), related skills (unless orchestrating), full citation text (URLs only)

---

## 0C) Context Efficiency Metrics (measurement)

**Track per skill/agent invocation:**
* Tokens per tier (T1/T2/T3 actual vs budget)
* Cache hit rate (T1 sufficient vs T2/T3 needed)
* Budget violations (P0/P1/P2 counts)
* Conversation turns to completion

**Efficiency Targets (95th percentile)**
* T1 completion rate: ≥80%
* Tokens per invocation: ≤10k (T1), ≤25k (T2), ≤50k (T3)
* Budget violations: ≤2%
* Conversation turns: ≤5

**Optimization Signals**: T1 <70% → split skill | Tokens >30k → trim | Violations >5% → adjust budgets | Turns >8 → improve triggers

**CI Enforcement**: `validate_skill.py` blocks if T1 >2k, T2 >6k, T3 >12k.

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

**Philosophy**: Technical precision over social niceties. Direct. Precise. No wasted words.

**Hard Rules (reference table):**

| Rule | ❌ Bad | ✅ Good |
|------|--------|---------|
| No preamble | "I'd be happy to help..." | "Bug in line 47. Mutex not released." |
| No hedging | "seems like might possibly..." | "Caused by X" or "Don't know. Check Y." |
| No apologizing | "Sorry, but there might be..." | "Won't work. Use Y instead." |
| No affirmations | "Great question!" | "Difference is X vs Y. Use X when Z." |
| No narration | "Now I'm going to search..." | [Just do it and report findings] |
| Challenge wrong assumptions | "interesting approach, though..." | "Won't work. System guarantees ¬X." |

**Smart Brevity**: One idea/sentence. Technical terms OK. Show > explain. Bullet points > prose. Active voice. Imperative for instructions.

**Politeness Boundaries**: Critique code, not people. Be blunt about waste. Express frustration with patterns. No profanity, insults, or mockery.

**Litmus Test**: Linus approves the rigor? HR approves the tone? Both must be yes.

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

**Tier Taxonomy**

| Tier | Prefix/Format | When to Use | Examples |
|------|---------------|-------------|----------|
| T1 Core | `core-*` | Meta-capabilities, LLM delegation, repository tooling | `core-skill-authoring`, `core-codex-delegator` |
| T2 Domain | `{domain}-{scope}-{action}` | Broad domain activities (security, testing, cloud, devops, compliance, frontend, data, observability, finops, resilience, documentation, quality, integration, tooling) | `security-appsec-validator`, `testing-unit-generator`, `cloud-aws-architect`, `devops-cicd-generator` |
| T3 Specialized | `{tech}-{scope}-{action}` | Technology-specific (Kubernetes, databases, API patterns, compliance frameworks) | `kubernetes-helm-builder`, `compliance-fedramp-validator`, `api-graphql-designer` |

**18 Standardized Action Suffixes (precedence order)**

| Suffix | Purpose | Suffix | Purpose |
|--------|---------|--------|---------|
| 1. orchestrator | multi-skill coordinator (agents) | 10. assessor | measures maturity/compliance |
| 2. architect | high-level design/structure | 11. calculator | computes metrics/values |
| 3. designer | detailed design/patterns | 12. optimizer | improves performance/cost |
| 4. composer | combines components | 13. detector | identifies issues/drift |
| 5. builder | constructs artifacts | 14. reviewer | evaluates quality/security |
| 6. generator | produces code/config | 15. configurator | sets up tools/systems |
| 7. validator | checks correctness | 16. integrator | connects platforms/services |
| 8. analyzer | evaluates/provides insights | 17. advisor | strategic guidance |
| 9. checker | verifies conditions | 18. delegator | routes to external systems |

**Agent Naming**: `{domain}-orchestrator` (exception: `agent-creator` for core agents). Examples: `cloud-aws-orchestrator`, `security-auditor`.

**Routing Strategy**: Domain prefix filtering → technology-specific tier preference → action suffix matching → fallback to domain/orchestrator.

**Renaming Checklist**: Update SKILL.md slug + rename directory + update index + cross-references + test file + validate + docs.

---

## 2B) Code Quality & TDD Standards (enforced)

**Philosophy**: Quality is non-negotiable. Production-grade standards for all code.

**TDD Rules**: Tests first → Red/Green/Refactor → ≥80% coverage → 3-5 evals per skill

**Tooling Summary:**

| Language | Format | Lint | Type Check | Config |
|----------|--------|------|------------|--------|
| Python | black (100 chars) | ruff | mypy --strict | pyproject.toml |
| TypeScript | prettier | eslint | tsc --noEmit | .eslintrc.json |
| Shell | shfmt -i 2 | shellcheck | N/A | N/A |

**Security Scanning**: pip-audit, npm audit, gitleaks, bandit. Run on every PR.

**Pre-Commit Hooks**: Install via `pre-commit install`. Config in `.pre-commit-config.yaml`.

**Enforcement Priorities:**

| Severity | Block Merge? | Examples |
|----------|--------------|----------|
| P0 | Yes | Lint errors, test failures, HIGH/CRITICAL vulns, secrets |
| P1 | Next release | Coverage <80%, medium vulns, deps >3mo old |
| P2 | Track | Complexity warnings, low vulns, doc gaps |

**Full configuration**: See `pyproject.toml` for all tool settings.

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

**Definition**: An **Agent** is a multi-step orchestrator that coordinates 2+ **Skills** through a command-driven workflow. Agents operate in separate context (system prompt), while Skills are invoked inline by the model.

**When to Use Agent vs Skill (Decision Framework)**

| Characteristic | Skill | Agent |
|----------------|-------|-------|
| Steps | ≤2 | 4 (orchestration) |
| Invocation | Model (natural language) | User (command) |
| Context | Shares main | Separate |
| Token budget | T1/T2/T3 (≤12k) | System prompt ≤1500 |
| Purpose | Single capability | Multi-skill coordination |

**Decision Rules**: Use a **Skill** when the task is self-contained, has ≤2 steps, and fits T1/T2/T3 token tiers. Use an **Agent** when the task requires orchestrating multiple skills, maintaining workflow state, or executing a standard 4-step pattern.

**Required AGENT.md Structure**: Metadata, Purpose & Trigger, System Prompt (≤1500 tokens with role/authority/constraints), Workflow (4-step pattern), Skill Integration (slug references only), Examples (≤30 lines, success/failure scenarios), Quality Gates, Resources (links only).

**4-Step Workflow Pattern (Standard)**

All agents must implement this structure:

1. **Plan** — Parse user request, identify required skills, validate inputs
2. **Execute** — Invoke skills in sequence, handle intermediate results
3. **Validate** — Check outputs against quality gates, verify success criteria
4. **Report** — Return structured results, log decisions, handle errors

**Skill Integration**: Reference skills by **slug only** (e.g., `oscal-ssp-validate`). Load `/index/skills-index.json` to resolve slug → path. Pass inputs/outputs explicitly; handle failures gracefully.

**Quality Gates**

* System prompt ≤1500 tokens (measured via `tiktoken` cl100k_base; includes role, decision authority, constraints, abort conditions)
* All skill references resolvable via index; 4-step workflow present and deterministic
* Examples (≤30 lines) show complete workflow and execute successfully (or marked as pseudo-code)
* No secrets or PII in agent definition or examples

---

## 4) Research & Citations

**Source Hierarchy**: Official docs > maintainer repos > named-author blogs > community (SO ≥10 votes). Never use: paywalled, link-rotted, unverifiable, or LLM-generated summaries without primary source.

**Every claim** that could change or be disputed must include a **clickable hyperlink** + **access date = `NOW_ET`**.

**Verification Requirements**: Use tier 1–3 sources only + accessible link + explicit claim (no inference leaps) + scope/method/context for metrics + version context for APIs/schemas + access date for time-sensitive content + note conflicts using most authoritative source.

**Technical Accuracy**

* **Versions/APIs/flags**: Copy exact syntax from docs or `--help`. Include version context: "as of v2.3.1 (accessed `NOW_ET`)". Mark uncertainty: `[TODO: verify X]`.
* **Code examples**: Test or mark pseudo-code. Include runtime version ("Python 3.11.5") and library imports with versions.
* **Quantitative claims**: Always cite measurement method and units ("≤2k tokens via `tiktoken` cl100k_base"). For benchmarks: specify environment, sample size, date, tooling.
* **Schemas**: Never invent field names. Copy from JSON Schema, OpenAPI spec, or authoritative docs. Mark subsets: "Partial schema; see <link>".

**Error Handling**: Cannot verify in ≤3 minutes? Do not include it. Mark ambiguity as `[TODO: confirm X with Y]` and stop or defer to T3. Never round up numbers to make docs cleaner.

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

**Philosophy**: Repository systems (indices, coverage, dependencies) must stay synchronized.

**Maintenance Commands (reference):**

| Task | Command | When |
|------|---------|------|
| Rebuild skills index | `python tooling/build_index.py` | After add/rename/delete skill |
| Rebuild agents index | `python tooling/build_agent_index.py` | After add/rename/delete agent |
| Rebuild coverage | `python tooling/analyze_coverage.py` | After any skill/agent change |
| Rebuild dependencies | `python tooling/analyze_agent_dependencies.py` | After agent changes |
| Validate skills | `python tooling/validate_skill.py` | Before commit |
| Check structure | `find skills/ agents/ -type d -empty` | Monthly audit |

**Post-Change Workflow (required):**

1. Validate: `python tooling/validate_skill.py`
2. Rebuild indices: `python tooling/build_index.py`
3. Update coverage: `python tooling/analyze_coverage.py`
4. Update gap analysis in `docs/COVERAGE_MATRIX.md` (manual)
5. Commit together: `git add skills/<slug>/ index/ docs/ && git commit`

**Monthly Audit (first Monday):**

1. Rebuild all indices
2. Validate all skills
3. Check for orphaned files: `find skills/ agents/ -name "*.md" ! -name "SKILL.md" ...`
4. Update `LAST_AUDIT` in CLAUDE.md header
5. Commit: `chore(audit): monthly maintenance`

**Required Files:**
* Every skill/agent dir: `SKILL.md` or `AGENT.md` + `CHANGELOG.md`
* Empty dirs: `.gitkeep` file
* Version-controlled: `index/*.json`, `docs/COVERAGE_MATRIX.md`, `docs/AGENT_DEPENDENCIES.md`

**CHANGELOG Format** (Keep-a-Changelog):
* `## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD`
* Major: breaking changes | Minor: features | Patch: fixes

**Commit Message Format**: `type(scope): description` (conventional commits)


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

**Content (§1-§4):**
* [ ] `NOW_ET` computed; access dates present
* [ ] No secrets/PII; examples ≤30 lines; token budgets (T1/T2/T3)
* [ ] All claims sourced (tier 1-3); links resolve; no `[TODO:]` markers

**Maintenance (§8A):**
* [ ] Indices rebuilt: `python tooling/build_index.py`
* [ ] Coverage updated: `python tooling/analyze_coverage.py`
* [ ] CHANGELOG.md updated; `.gitkeep` in empty dirs

**Quality (§2B):**
* [ ] Pre-commit passes (black, ruff, mypy, gitleaks)
* [ ] Evals pass; tests pass

**Git (§13):**
* [ ] Conventional commit: `type(scope): description`
* [ ] All artifacts committed (indices, coverage, deps)

---

## 11) Maintenance & Scope

**Cadence**: Update `LAST_AUDIT` on validation; set `NEXT_REVIEW = +90 days`. Remove unused rules.

**Out of Scope**: Website/11ty/SEO details, heavy orchestration boilerplate, large code samples (link instead).

---

## 13) Git & GitHub Workflow (Required)

**Branch Strategy**: Never commit to `main` directly. Branch from latest main.
* Feature: `feature/<skill-slug>` | Hotfix: `hotfix/<issue-id>`

**Commits**: Atomic, conventional format: `type(scope): description`
* Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
* Max 72 chars first line, imperative mood. Reference issues: `Fixes #123`

**Issue Tracking Strategy**:
* **When to create**: Multi-step tasks (>3 commits), bugs, feature requests, maintenance tasks
* **Templates**: Bug report (steps/expected/actual), feature request (problem/solution), task (checklist)
* **Labels**: `phase-1` (discovery), `phase-2` (execution), `priority-high/medium/low`, `type-bug/feature/task`
* **Reference format**: `#123` in commits; `Closes #123` or `Fixes #123` in PR body/commits

**Issue Management:**

| Action | Command | When |
|--------|---------|------|
| Create issue | `gh issue create -t "title" -b "body" -l "type-task,priority-medium"` | New task/bug/feature |
| List open | `gh issue list -s open` | Review backlog |
| Assign | `gh issue edit N --add-assignee @me` | Claim work |
| Close with PR | Include `Closes #123` in PR body | Task complete via PR |
| Close direct | `gh issue close N -c "reason"` | Resolved without PR |

**GitHub CLI Quick Reference:**

| Task | Command |
|------|---------|
| Create PR | `gh pr create --title "type: msg" --body "Closes #N\n\n..."` |
| Check status | `gh pr status` |
| Monitor CI | `gh pr checks` |
| Merge | `gh pr merge --squash` |

**PR Workflow**: Issue created → Branch → Commit → Push → `gh pr create` (link issue) → CI passes → Merge

**PR-Issue Integration**:
* Always link PRs to issues: `Closes #N`, `Fixes #N`, or `Resolves #N` in PR description
* Multi-issue PRs: `Closes #N, closes #M` (one line per issue for clarity)
* Partial work: `Part of #N` or `Contributes to #N` (does not auto-close)
### Final Word

Build **small, sharp Skills** with **clear triggers** and **tight outputs**. Cite precisely. Keep tokens down. When unsure, ask for inputs, list TODOs, and stop.
