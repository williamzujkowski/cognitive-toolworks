# Cognitive Toolworks - Skills Repository

A library of small, composable Skills using Anthropic's SKILL.md format, optimized for LLM consumption with progressive disclosure and minimal token usage.

## Purpose

This repository provides:

- **Reusable Skills**: Small, focused capabilities with clear triggers and outputs
- **Progressive Disclosure**: Tiered procedures (T1/T2/T3) that minimize token usage
- **Research Discipline**: Citations with access dates for all claims
- **Deterministic Structure**: Validated format, indexed for discovery
- **Safe Operations**: No secrets, PII-free, with CI gates

## Quick Start

### Adding a New Skill

1. Create a folder under `/skills/<skill-slug>/`
2. Write a `SKILL.md` following the template (see CLAUDE.md section 3)
3. Add one small example (≤30 lines) in `/skills/<skill-slug>/examples/`
4. Create 3-5 test scenarios in `/tests/evals_<slug>.yaml`
5. Run validation: `python tooling/validate_skill.py skills/<skill-slug>/SKILL.md`
6. Update index: `python tooling/build_index.py`

### Skill Structure (Required Sections)

Each SKILL.md must include in order:

1. **Purpose & When-To-Use** - Trigger conditions
2. **Pre-Checks** - Input validation, time normalization
3. **Procedure** - Tiered steps (T1 ≤2k, T2 ≤6k, T3 ≤12k tokens)
4. **Decision Rules** - Ambiguity handling, abort conditions
5. **Output Contract** - Explicit schema and required fields
6. **Examples** - One small example (≤30 lines)
7. **Quality Gates** - Token budgets, safety checks
8. **Resources** - Links only (no large quoted text)

### Progressive Disclosure Model

Skills use a three-tier approach to balance speed and depth:

- **T1 (≤2k tokens)**: Fast path for common 80% cases; minimal retrieval
- **T2 (≤6k tokens)**: Extended validation with 2-4 sources
- **T3 (≤12k tokens)**: Deep research, rationale, eval generation

LLMs load only the tier needed for the task, minimizing context consumption.

## Repository Layout

```
/index/
  skills-index.json         # Generated discovery manifest
  embeddings/               # Optional ANN vectors
/skills/
  <skill-slug>/
    SKILL.md                # Required (Anthropic format)
    examples/               # 1-2 tiny files (≤30 lines)
    resources/              # Small templates/schemas
    scripts/                # Optional helpers
    CHANGELOG.md
/tests/
  evals_<slug>.yaml         # 3-5 scenarios per skill
/tooling/
  validate_skill.py         # Schema/format/safety checks
  build_index.py            # Generates index
  lint_skill.py             # Heading/link verification
/.github/workflows/
  skills-ci.yaml            # CI pipeline
```

## Governance

- **CLAUDE.md**: Authoritative rules (single source of truth)
- **CONTRIBUTING.md**: How to contribute
- **CODE_OF_CONDUCT.md**: Community standards
- **LICENSE**: Apache-2.0

## Research & Citations

All nontrivial claims must include:

- Reputable source (official docs > standards > technical sources)
- Clickable hyperlink
- Access date in NOW_ET format (America/New_York, ISO-8601)

Priority: Official documentation > Standards/specs > Reputable technical sources > High-quality blogs

## Quality Gates (CI)

PRs must pass:

1. **Validation**: Required sections, token budgets, secret checks
2. **Lint**: Section order, links, headings
3. **Index**: Deterministic build, no duplicate slugs
4. **Evals**: Test scenarios pass

## Token Budget Enforcement

Every skill must declare and respect:

- T1 budget (≤2k tokens)
- T2 budget (≤6k tokens)
- T3 budget (≤12k tokens)

Examples must be ≤30 lines. Descriptions must be ≤160 characters.

## License

Apache-2.0 - See LICENSE file

## Owner

cloud.gov OCS

---

**Last Updated**: 2025-10-25
**Status**: Active Development
