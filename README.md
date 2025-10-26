# cognitive-toolworks

30 production-ready Skills for Claude CLI. No fluff, no marketing nonsense.

## What This Is

A library of small, composable Skills using Anthropic's SKILL.md format. Each skill is:
- **Focused**: Does one thing, does it right
- **Tiered**: T1 (≤2k tokens) → T2 (≤6k) → T3 (≤12k) for progressive disclosure
- **Cited**: Every claim has a source with access date. No hallucinations.
- **Validated**: CI enforces format, checks secrets, verifies links

## Usage with Claude CLI

### 1. Clone and Point Claude at It

```bash
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
```

Tell Claude CLI about this repo by referencing `CLAUDE.md` in your conversations. Claude will read the skills you need and follow the rules.

### 2. Use a Skill

Just ask Claude to use a skill by name:

```
Use the microservices-pattern-architect skill to recommend patterns for my e-commerce checkout flow.
```

Claude loads only what it needs (T1 for simple cases, T2/T3 when you need depth).

### 3. Create a New Skill

```
Use the skill-creation skill to build a new skill for Kubernetes deployment validation.
```

The meta-skill generates everything: SKILL.md, examples, tests, index entry. Enforces CLAUDE.md rules automatically.

## What's Inside

**30 skills across 5 categories:**

- **Architecture** (8): Decision frameworks, microservices patterns, data pipelines, frontend frameworks, IaC, containers, databases, APIs
- **Operations** (8): Security assessment, compliance, code review, performance, testing, deployment, monitoring, cloud migration
- **Specialized** (12): MLOps, zero-trust, incident response, supply chain security, docs, cost optimization, SRE SLO, drift detection, UX design systems, chaos engineering, multi-cloud, edge computing
- **AI Delegation** (2): Gemini CLI (large context), Codex CLI (code generation)

Full list: `ls skills/` or check `index/skills-index.json`.

## Rules (Read CLAUDE.md)

CLAUDE.md is the authoritative rulebook. Key points:

- **Accuracy**: Zero tolerance for fabrication. Every claim needs a source.
- **Token budgets**: T1/T2/T3 are hard limits, not suggestions.
- **Examples**: ≤30 lines. No exceptions.
- **No secrets**: If you commit an API key, the validator will catch it and your PR fails.
- **Git workflow**: Feature branches only. Squash-merge to main. See CLAUDE.md §13.

## Contributing

1. Read CLAUDE.md (seriously, read it)
2. Branch from main: `git checkout -b feature/your-skill`
3. Build your skill following §3 format
4. Run validator: `python3 tooling/validate_skill.py`
5. Build index: `python3 tooling/build_index.py`
6. PR with `gh pr create` (see CLAUDE.md §13 for template)

CI runs validation, linting, indexing, and evals. If it fails, fix it. No hand-waving.

See CONTRIBUTING.md for details.

## Quality Gates

Every PR must pass:
1. Validation (format, token budgets, secrets check)
2. Linting (section order, links, headings)
3. Index build (deterministic, no duplicates)
4. Evals (test scenarios)

See CLAUDE.md §8 for what gets checked.

## Structure

```
skills/<slug>/SKILL.md      # The skill (required sections, cited sources)
skills/<slug>/examples/     # Small examples (≤30 lines each)
skills/<slug>/resources/    # Templates, schemas, configs
tests/evals_<slug>.yaml     # 3-5 test scenarios
index/skills-index.json     # Discovery manifest (generated)
```

## License

Apache-2.0

## Maintainer

Personal project - cognitive-toolworks

---

**Last Updated**: 2025-10-26T03:43:18-04:00
**CLAUDE.md Version**: 1.1.0
**Skills**: 30
**Status**: Production
