# CLAUDE.md — Authoritative Rules for the Skills Repository

```
STATUS: AUTHORITATIVE
VERSION: 1.0.0
LAST_AUDIT: 2025-10-25T21:04:34-04:00
NEXT_REVIEW: 2026-01-23T21:04:34-05:00
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

## 1) Time, Safety, and Non-Fabrication (hard rules)

**Authoritative Time**

* Compute `NOW_ET` using **NIST/time.gov semantics** (America/New_York, ISO-8601).
* Set `LAST_AUDIT` and `NEXT_REVIEW = LAST_AUDIT + 90 days`.

**Safety & Privacy**

* Personal/public repo. **No secrets, no private PII**, no employer/internal material.
* Do not invent facts. Every nontrivial claim must have a linkable source with access date = `NOW_ET`.

---

## 2) Repository Layout (strict)

```
/index/
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
/tooling/
  validate_skill.py         # schema/format/secret/token checks
  build_index.py            # generates index; optional embeddings
  lint_skill.py             # headings/order/links (optional)
/.github/workflows/
  skills-ci.yaml            # validate → lint → index → evals
```

Rules:

* **One skill per folder** with a single `SKILL.md`.
* Always include a **`.gitkeep`** in otherwise-empty directories.
* Prefer **editing** existing skills over creating new ones.

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

## 4) Research & Citations

**Priority:** official docs → standards/specs → reputable technical sources → high-quality blogs.
**Every claim** that could change or be disputed must include a **clickable hyperlink** + **access date = `NOW_ET`**.
**Verification checklist**:

* [ ] Source is reputable and says what you claim
* [ ] Link works
* [ ] Numbers have scope/method/context
* [ ] If time-sensitive, capture version/date

**Example (inline):**

> “OSCAL profile validation requires schema/version alignment (accessed `NOW_ET`): <link>”

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
* [ ] Links resolve; claims match sources
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
