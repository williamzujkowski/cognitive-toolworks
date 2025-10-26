# CLAUDE.md — Authoritative Rules for the Skills Repository

```
STATUS: AUTHORITATIVE
VERSION: 1.4.0
LAST_AUDIT: 2025-10-26T15:30:00-04:00
NEXT_REVIEW: 2026-01-24T15:30:00-05:00
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
* [ ] Index updated and deterministic; no duplicate slugs
* [ ] Evals added/updated and pass locally
* [ ] Commit message: clear, imperative, ≤72 chars first line

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
