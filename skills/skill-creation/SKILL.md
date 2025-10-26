---
name: "Create a New Skill from Topic"
slug: "skill-creation"
description: "Generate a production-ready SKILL.md + tiny examples, evals, and an index entry aligned to Anthropic Skills."
capabilities:
  - "research authoritative sources"
  - "draft tiered procedures with decision rules"
  - "author SKILL.md metadata + examples"
  - "emit tests and index entries"
inputs:
  - name: "topic"
    type: "string"
    required: true
  - name: "constraints"
    type: "json"
    required: false
  - name: "org_context"
    type: "json"
    required: false
outputs:
  - name: "skill_folder"
    type: "file"
  - name: "index_entry"
    type: "json"
keywords: ["authoring", "generator", "skills.md", "progressive-disclosure"]
version: "1.0.0"
owner: "cognitive-toolworks"
license: "Apache-2.0"
security:
  pii: "none"
  secrets: "never embed; use env/cred mgr"
  audit: "include sources with titles/URLs; normalize NIST time"
links:
  docs:
    - "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview"
    - "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices"
    - "https://docs.claude.com/en/docs/claude-code/skills"
---

## Purpose & When-To-Use
Use when a developer specifies a new Skill topic and needs a compliant, token-efficient `SKILL.md` with a tiny example, tests, and an index entry.

## Pre-Checks
- **Authoritative time**: Set `NOW_ET` to ISO 8601 in `America/New_York` using NIST/time.gov semantics. Include `NOW_ET` in citations’ access dates.
- **Scope**: Extract intended users, inputs/outputs, success criteria, and token budgets.
- **Sources**: Identify primary standards/docs. Prefer authoritative sources; record title, URL, and access date (`NOW_ET`).
- **Footprint**: Default to Tier 1 unless ambiguity or regulation requires expansion.

## Procedure
### Tier 1 — Draft Minimal Skill (T1≤2000 tokens)
1. Write **METADATA**: concise `name`, `slug`, ≤160-char `description`, `capabilities`, `inputs`, `outputs`, `keywords`, `version`, `owner`, `license`, `security`, `links`.
2. Author compact sections: `Purpose & When-To-Use`, `Pre-Checks`, `Procedure (Tiered)`, `Decision Rules`, `Output Contract`, `Quality Gates`, `Resources`.
3. Add **one** short runnable example (≤30 lines) or precise pseudo-code.
4. Produce `index_entry` JSON for `index/skills-index.json`.

### Tier 2 — Source-Backed Enrichment (T2≤6000 tokens)
1. Gather 2–4 primary sources; add citations with titles, URLs, and `NOW_ET` access dates.
2. Add explicit **Decision Rules** (ambiguity thresholds, abort conditions).
3. Link small `resources/` artifacts (schemas/templates) without pasting large texts.

### Tier 3 — Deep Validation (T3≤12000 tokens)
1. Create `tests/evals_<slug>.yaml` with 3–5 scenarios (happy path, missing input, edge case).
2. Add security notes (secrets handling, PII posture, auditability).
3. Emit `CHANGELOG.md` (v1.0.0) and finalize `index_entry`.

## Decision Rules
- If regulated domains (NIST/OMB/FedRAMP) are involved → require Tier 2.
- If schemas/versions are unknown → emit TODO and **stop** with `needs-input`.
- If example exceeds 30 lines → **truncate** and link to `resources/`.

## Output Contract
- Create `skills/<slug>/` containing:
  - `SKILL.md` (this format)
  - `examples/<slug>-example.txt` (≤30 lines)
  - `resources/` (optional, linked)
  - `CHANGELOG.md`
- Emit `index_entry` JSON with: `slug`, `name`, `summary` (≤160 chars), `keywords`, `owner`, `version`, `entry`.

## Examples
**Minimal example (pseudo-code, ≤30 lines):**
```text
INPUT:
  topic: "OSCAL SSP validator for FedRAMP Moderate"
  constraints: { "strict": true }

OUTPUT (files):
  skills/oscal-ssp-validate/SKILL.md
  skills/oscal-ssp-validate/examples/oscal-ssp-validate-example.txt
  tests/evals_oscal-ssp-validate.yaml
  index_entry (JSON fragment)

INDEX_ENTRY:
  {
    "slug": "oscal-ssp-validate",
    "name": "OSCAL SSP Validator for FedRAMP Moderate",
    "summary": "Validates OSCAL SSP against FedRAMP Moderate baseline requirements.",
    "keywords": ["oscal", "ssp", "fedramp", "validation"],
    "owner": "cognitive-toolworks",
    "version": "1.0.0",
    "entry": "skills/oscal-ssp-validate/SKILL.md"
  }
```

## Quality Gates
- **Token budgets**: T1≤2k, T2≤6k, T3≤12k — enforce via `validate_skill.py`.
- **Example size**: ≤30 lines runnable/pseudo-code; longer samples → `resources/`.
- **Metadata**: `description` ≤160 chars; all required front-matter keys present.
- **Sources**: T2+ requires 2–4 authoritative links with titles/URLs and access dates (`NOW_ET`).
- **Safety**: No secrets, PII, or long pasted texts; `validate_skill.py` checks for secret patterns.
- **Determinism**: Index entries must be unique slugs; `build_index.py` enforces no duplicates.
- **Evals**: 3–5 scenarios in `tests/evals_<slug>.yaml`; must pass basic sanity checks.

## Resources
- **Anthropic Skills Overview** (accessed 2025-10-25): https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Anthropic Skills Best Practices** (accessed 2025-10-25): https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- **Claude Code Skills Documentation** (accessed 2025-10-25): https://docs.claude.com/en/docs/claude-code/skills
- **NIST Time Services** (accessed 2025-10-25): https://www.nist.gov/pml/time-and-frequency-division/time-services
- **ISO 8601 Date/Time Format** (accessed 2025-10-25): https://www.iso.org/iso-8601-date-and-time-format.html
