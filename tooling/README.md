# Tooling

Validation and build scripts for the cognitive-toolworks skills repository.

## Scripts

### validate_skill.py

Validates skill SKILL.md files against CLAUDE.md standards.

**Usage:**
```bash
python3 tooling/validate_skill.py [--root ROOT]
```

**Checks:**
- Required front-matter keys present
- Description ≤160 characters
- Required sections in correct order
- Token budgets visible
- No secret patterns
- Code block size limits

### lint_skill.py

Lints skill SKILL.md files for common issues.

**Usage:**
```bash
python3 tooling/lint_skill.py [--root ROOT] [--validate-links]
```

**Checks:**
- Section heading order and formatting
- Link validity (if --validate-links)
- Consistent formatting

### validate_examples.py

Validates example files in `skills/*/examples/` directories.

**Usage:**
```bash
python3 tooling/validate_examples.py [--root ROOT] [--strict]
```

**Checks:**
- Line count limits (≤30 soft, ≤60 hard)
- No hardcoded secrets or credentials
- Allowed file extensions
- File naming conventions

**Options:**
- `--strict`: Enforce strict 30-line limit (errors instead of warnings)

**Line Limits:**
- **Soft limit**: 30 lines (CLAUDE.md target) - warning if exceeded
- **Hard limit**: 60 lines (absolute maximum) - error if exceeded

### build_index.py

Generates `index/skills-index.json` from all skills.

**Usage:**
```bash
python3 tooling/build_index.py [--root ROOT]
```

**Output:**
- `index/skills-index.json`: Minimal discovery manifest with slug, name, summary, keywords
- Optional: `index/embeddings/`: Vector embeddings for ANN search

## Pre-commit Hooks

All validators run automatically via pre-commit hooks. Install with:

```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

## Development

### Adding a New Validator

1. Create script in `tooling/` directory
2. Add CLI interface with argparse
3. Return exit code 0 (success) or 1 (failure)
4. Add to `.pre-commit-config.yaml` as local hook
5. Document in this README

### Validation Flow

```
validate_skill.py  → Check SKILL.md structure and content
      ↓
lint_skill.py      → Check formatting and style
      ↓
validate_examples.py → Check example files
      ↓
build_index.py     → Generate index from validated skills
```
