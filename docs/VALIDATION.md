# Skill Validation & Quality Gates

This document describes the validation workflow and quality gates for cognitive-toolworks skills.

## Overview

Skills undergo multiple validation phases:

1. **Basic Validation** - Structural requirements (blocking)
2. **Quality Gates** - Code quality and best practices (non-blocking)
3. **Lint** - Formatting and style (blocking)
4. **Evaluations** - Scenario-based testing (non-blocking)

## Validation Levels

### Basic Validation (Blocking)

Checks fundamental requirements that must pass before merge:

- Front matter structure (YAML format)
- Required metadata keys (name, slug, description, etc.)
- Description length (≤160 chars)
- Required sections (Purpose, Pre-Checks, Procedure, etc.)
- Token budgets (T1/T2/T3) present
- Example size (≤30 lines)
- Code block size (≤200 lines)
- Secret patterns

**Usage:**
```bash
python tooling/validate_skill.py --root .
```

**Exit codes:**
- 0: Success
- 1: Validation errors found
- 2: System error (skills dir not found)

### Quality Gates (Non-blocking)

Additional quality checks enabled via flags:

#### Syntax Validation (`--check-syntax`)

Validates code syntax in examples for supported languages:

- **Python**: Uses `ast.parse()` to check syntax
- Other languages: Pass-through (planned)

Example:
```bash
python tooling/validate_skill.py --root . --check-syntax
```

#### TODO Markers (`--check-todos`)

Fails if `[TODO: ...]` markers found in committed skills:

```bash
python tooling/validate_skill.py --root . --check-todos
```

#### Link Validation (`--check-links`)

Validates HTTP/HTTPS URLs return 200 status:

- Uses HEAD requests for efficiency
- 5-second timeout per URL
- Returns warnings (not errors) for failed links
- Useful for detecting link rot

Example:
```bash
python tooling/validate_skill.py --root . --check-links
```

**Note:** Link validation can be slow for skills with many URLs.

#### Strict Mode (`--strict`)

Enables all quality gates and fails on warnings:

```bash
python tooling/validate_skill.py --root . --strict
```

Equivalent to:
```bash
python tooling/validate_skill.py --root . \
  --check-syntax \
  --check-todos \
  --check-links \
  --fail-on-warnings
```

### JSON Output

All validation modes support JSON output for CI integration:

```bash
python tooling/validate_skill.py --root . --json
```

Output format:
```json
{
  "status": "success" | "failed",
  "skills_checked": 81,
  "errors": 0,
  "warnings": 0,
  "files": {
    "/path/to/skill/SKILL.md": [
      {
        "severity": "error" | "warning",
        "message": "Description of issue"
      }
    ]
  }
}
```

## Evaluation Runner

Validates eval file structure and scenarios:

```bash
python tooling/run_evals.py
```

Checks:
- Valid YAML structure
- Required fields (id, description, expected, pass_criteria)
- Test coverage (3-5 scenarios recommended)
- Field types (lists, strings, dicts)

**Note:** This performs structural validation only. It does NOT execute skills or make LLM calls.

## CI Workflow

The GitHub Actions workflow runs all validation steps:

### Pipeline Steps

1. **Basic Validation** (blocking)
   - Runs: `validate_skill.py --json`
   - Blocks merge on errors
   - Generates `validation-basic.json`

2. **Quality Gates** (non-blocking)
   - Runs: `validate_skill.py --check-syntax --check-todos --json`
   - Reports issues as warnings
   - Generates `validation-quality.json`
   - Does not block merge

3. **Lint** (blocking)
   - Runs: `lint_skill.py`
   - Checks section order, heading format
   - Blocks merge on errors

4. **Build Index** (blocking)
   - Runs: `build_index.py`
   - Generates `index/skills-index.json`
   - Blocks merge on errors

5. **Evaluations** (non-blocking)
   - Runs: `run_evals.py`
   - Validates eval file structure
   - Reports issues as warnings
   - Does not block merge

### Summary Report

CI generates a summary in GitHub Actions with:

- Validation status for each step
- Error/warning counts
- Quality gate issues
- Total skills checked

## Local Development

### Pre-commit Workflow

Before committing:

```bash
# Basic validation (required)
python tooling/validate_skill.py --root .

# Optional: Check code syntax
python tooling/validate_skill.py --root . --check-syntax

# Optional: Full strict mode
python tooling/validate_skill.py --root . --strict
```

### Fixing Common Issues

**Example too long:**
```
# Move example to resources/
mv skills/my-skill/examples/example.py skills/my-skill/resources/
# Link to it from SKILL.md
```

**TODO markers:**
```
# Either resolve the TODO or remove the marker
# TODOs are not allowed in committed skills
```

**Python syntax errors:**
```
# Check the code block syntax
python -c "import ast; ast.parse('''
# your code here
''')"
```

**Link validation failures:**
```
# Check if URL is accessible
curl -I https://example.com

# Update broken links or mark as [TODO: verify link]
```

## Configuration

Validation thresholds in `tooling/validate_skill.py`:

```python
MAX_DESCRIPTION_LEN = 160      # Characters
MAX_EXAMPLE_LINES = 30         # Lines
MAX_CODEBLOCK_LINES = 200      # Lines
```

Secret patterns in `SECRET_PATTERNS`:
- AWS access keys
- Private keys
- SSH keys
- Password/secret assignments

## Future Enhancements

Planned quality gates:

- [ ] JavaScript/TypeScript syntax validation
- [ ] Shell script validation (shellcheck)
- [ ] Markdown link checker (internal references)
- [ ] Token budget enforcement (tiktoken)
- [ ] Citation format validation
- [ ] Version number validation
- [ ] Breaking change detection
