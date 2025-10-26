# Contributing to Cognitive Toolworks

Thank you for contributing to this Skills repository. This guide ensures consistency and quality.

## Before You Start

1. Read **CLAUDE.md** - the authoritative ruleset
2. Review existing skills in `/skills/` for examples
3. Check `/index/skills-index.json` to avoid duplicate slugs

## Contribution Process

### 1. Create or Edit a Skill

**For New Skills:**

- Use the skill-creation template from CLAUDE.md section 9A
- Follow the exact section order from CLAUDE.md section 3
- Keep the skill focused on one capability
- Token budgets: T1 ≤2k, T2 ≤6k, T3 ≤12k

**For Edits:**

- Prefer editing existing skills over creating new ones
- Maintain section order and token budgets
- Refresh citations with current NOW_ET (America/New_York, ISO-8601)
- Keep examples ≤30 lines

### 2. Required Deliverables

Every skill contribution must include:

```
/skills/<skill-slug>/
  SKILL.md               # Complete, validated skill
  examples/
    <slug>-example.txt   # ≤30 lines
  CHANGELOG.md           # Version history
/tests/
  evals_<slug>.yaml      # 3-5 test scenarios
```

Update `/index/skills-index.json` entry:
```json
{
  "slug": "skill-slug",
  "name": "Skill Name",
  "summary": "≤160 char description",
  "keywords": ["key1", "key2"],
  "owner": "cloud.gov OCS",
  "version": "1.0.0",
  "entry": "/skills/skill-slug/SKILL.md"
}
```

### 3. Research & Citations

Every claim must include:

- **Source priority**: Official docs > standards/specs > reputable technical sources > blogs
- **Clickable link** with the actual URL
- **Access date** = NOW_ET in ISO-8601 format (America/New_York)

**Example:**
> According to the Anthropic Skills specification (accessed 2025-10-25T21:04:34-04:00): [https://example.com/skill-spec](https://example.com/skill-spec)

### 4. Validation (Local)

Before submitting:

```bash
# Validate skill format
python tooling/validate_skill.py skills/<skill-slug>/SKILL.md

# Lint headings and links
python tooling/lint_skill.py skills/<skill-slug>/SKILL.md

# Rebuild index
python tooling/build_index.py

# Run evals (if implemented)
# pytest tests/evals_<slug>.yaml
```

### 5. Pull Request Checklist

- [ ] NOW_ET computed and used for all access dates
- [ ] No secrets, PII, or employer-internal material
- [ ] Required sections and front-matter keys present
- [ ] Example ≤30 lines; description ≤160 chars
- [ ] Token budgets declared (T1/T2/T3)
- [ ] All links resolve and match claims
- [ ] Index entry added/updated with no duplicate slugs
- [ ] Evals added (3-5 scenarios) and pass locally
- [ ] Commit message: imperative, ≤72 chars first line

**Example commit:**
```
Add skill for OSCAL profile validation

- Implements T1/T2/T3 tiered procedure
- Includes 4 test scenarios
- Cites NIST OSCAL 1.1.2 spec
```

### 6. CI Pipeline

Your PR will run:

1. **validate_skill.py** - Schema, format, secrets, token limits
2. **lint_skill.py** - Section order, links, headings
3. **build_index.py** - Deterministic index generation
4. **evals** - Test scenario execution

PRs must pass all gates to merge.

## What NOT to Do

- Embed secrets or private PII
- Create large code samples in SKILL.md (use `/resources/` or external repos)
- Fabricate claims without sources
- Bypass validation tools
- Save working files to repository root
- Create duplicate skills without checking the index

## Token Budget Guidelines

Keep skills lean:

- **T1 (≤2k tokens)**: Handle 80% of common cases with minimal retrieval
- **T2 (≤6k tokens)**: Add validation + 2-4 sources
- **T3 (≤12k tokens)**: Deep research, full rationale

Examples: ≤30 lines runnable code or precise pseudocode

## Getting Help

- Review existing skills: `/skills/*/SKILL.md`
- Check CLAUDE.md sections 3, 5, 9
- Open an issue with questions (be specific)

## License

By contributing, you agree that your contributions will be licensed under Apache-2.0.

---

**Maintained by**: cloud.gov OCS
**Last Updated**: 2025-10-25
