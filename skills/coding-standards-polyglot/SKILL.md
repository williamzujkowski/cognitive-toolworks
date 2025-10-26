---
name: "Polyglot Coding Standards Analyzer"
slug: "coding-standards-polyglot"
description: "Evaluate code quality across 8+ languages using language-agnostic principles and language-specific best practices."
capabilities:
  - Multi-language code analysis (Go, JavaScript, Kotlin, Python, Rust, Shell, Swift, TypeScript)
  - Universal principle validation (DRY, SOLID, naming conventions)
  - Language-specific style guide enforcement
  - Automated fix suggestions
  - Quality scoring and metrics
inputs:
  - code_path: "file or directory path (string)"
  - language: "auto-detect or explicit (string, optional)"
  - ruleset: "universal | language-specific | both (string, default: both)"
  - severity_threshold: "error | warning | info (string, default: warning)"
outputs:
  - quality_report: "JSON with issues categorized by severity"
  - fix_suggestions: "Markdown with actionable recommendations"
  - metrics: "Code quality score 0-100 (integer)"
keywords:
  - code-quality
  - linting
  - style-guide
  - polyglot
  - static-analysis
  - best-practices
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://google.github.io/styleguide/
  - https://kotlinlang.org/docs/coding-conventions.html
  - https://go.dev/doc/effective_go
  - https://peps.python.org/pep-0008/
  - https://rust-lang.github.io/api-guidelines/
  - https://github.com/airbnb/javascript
---

## Purpose & When-To-Use

**Trigger conditions:**
- Reviewing code quality before merge/commit
- Establishing baseline standards for multi-language codebases
- Training developers on language-agnostic and language-specific best practices
- Automated code review workflows requiring consistent quality gates

**Not for:**
- Runtime debugging or performance profiling
- Vulnerability scanning (use dedicated security tools)
- Complete rewrite automation (provides suggestions only)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `code_path` must exist and be readable
- `language` must be one of: go, javascript, kotlin, python, rust, shell, swift, typescript, or null (auto-detect)
- `ruleset` must be: "universal", "language-specific", or "both"
- `severity_threshold` must be: "error", "warning", or "info"

**Source freshness:**
- Style guide links must be accessible (HTTP 200)
- If language-specific rules reference versioned specs, verify version matches target language version

---

## Procedure

### T1: Universal Principles (≤2k tokens)

**Fast path for common cases:**

1. **Language Detection** (if not provided)
   - Use file extension and shebang analysis
   - Fallback to syntax pattern matching

2. **Universal Rules Application**
   - **DRY (Don't Repeat Yourself):** Flag duplicate code blocks >5 lines
   - **SOLID Principles:** Detect single-responsibility violations (functions >50 lines)
   - **Naming Conventions:** Check snake_case, camelCase, PascalCase per language norms
   - **Magic Numbers:** Identify hardcoded constants without explanation
   - **Documentation:** Require docstrings/comments for public APIs

3. **Quick Score**
   - Calculate preliminary score: `100 - (errors×10 + warnings×3 + info×1)`

**Decision:** If `ruleset == "universal"` → STOP at T1; otherwise proceed to T2.

---

### T2: Language-Specific Rules (≤6k tokens)

**Extended validation with style guides:**

1. **Route to Language Module** (see `resources/language-rules.json`)

   - **Python:** PEP 8 compliance (line length ≤79, import order, naming) [accessed 2025-10-25T21:30:36-04:00](https://peps.python.org/pep-0008/)
   - **Go:** Effective Go patterns (error handling, receiver names, package comments) [accessed 2025-10-25T21:30:36-04:00](https://go.dev/doc/effective_go)
   - **JavaScript/TypeScript:** Airbnb style (const/let, arrow functions, template literals) [accessed 2025-10-25T21:30:36-04:00](https://github.com/airbnb/javascript)
   - **Kotlin:** Official conventions (property declarations, lambda syntax) [accessed 2025-10-25T21:30:36-04:00](https://kotlinlang.org/docs/coding-conventions.html)
   - **Rust:** API guidelines (method naming, trait bounds, error types) [accessed 2025-10-25T21:30:36-04:00](https://rust-lang.github.io/api-guidelines/)
   - **Swift:** Google Swift style (access control, guard clauses) [accessed 2025-10-25T21:30:36-04:00](https://google.github.io/styleguide/swift.html)
   - **Shell:** Google Shell guide (quoting, function names, error handling) [accessed 2025-10-25T21:30:36-04:00](https://google.github.io/styleguide/shellguide.html)

2. **Automated Fix Generation**
   - Provide diff-ready patches for mechanical issues (formatting, imports)
   - Surface manual-review items for logic/architecture changes

3. **Final Scoring**
   - Adjust score based on language-specific violations
   - Apply severity weights: `critical=15, error=10, warning=3, info=1`
   - Cap score at 0 (minimum)

---

### T3: Deep Dive (not implemented in v1.0.0)

Reserved for:
- Cross-file dependency analysis
- Architecture pattern validation
- Performance anti-pattern detection

---

## Decision Rules

**Language Detection Confidence:**
- If confidence <80%, return error requesting explicit `language` parameter

**Abort Conditions:**
- `code_path` not readable → error "File/directory not accessible"
- Unsupported language → error "Language not in supported set"
- Parse failure (syntax errors) → return partial results with "unparseable code" warning

**Severity Filtering:**
- Only include issues at or above `severity_threshold` in final report
- Always compute full score regardless of threshold (for metrics consistency)

**Ambiguity Handling:**
- Mixed-language directories: analyze per-file, aggregate scores
- Conflicting rules (e.g., line length): prefer language-specific over universal

---

## Output Contract

**Schema (JSON):**

```json
{
  "code_path": "string",
  "language": "string",
  "score": "integer (0-100)",
  "issues": [
    {
      "file": "string",
      "line": "integer",
      "column": "integer (optional)",
      "severity": "error | warning | info",
      "rule": "string (e.g., 'PEP8-E501')",
      "message": "string",
      "fix": "string (optional, diff or instruction)"
    }
  ],
  "metrics": {
    "total_lines": "integer",
    "error_count": "integer",
    "warning_count": "integer",
    "info_count": "integer"
  },
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- `code_path`, `language`, `score`, `issues`, `metrics`, `timestamp`

**Fix Suggestions (Markdown):**
- Grouped by severity
- Max 5 suggestions per severity level (prioritize high-impact fixes)
- Include code snippets and references to style guides

---

## Examples

**Example 1: Python PEP 8 Analysis**

```
INPUT: {code_path: "src/calc.py", language: "python", ruleset: "both"}

T1 (Universal):
- ✗ Function exceeds 50 lines (42-105)
- ✗ Magic number: 86400 (line 57)
- ✗ Missing docstrings: 4 functions

T2 (PEP 8):
- ✗ E501: Line too long (12 instances)
- ✗ N806: Variable 'X' should be lowercase

OUTPUT:
{
  "score": 68,
  "issues": [{
    "line": 57,
    "rule": "UNIVERSAL-MAGIC",
    "message": "Magic number 86400",
    "fix": "SECONDS_PER_DAY = 86400"
  }],
  "metrics": {"warnings": 17}
}
```

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (language detection + universal rules)
- **T2:** ≤6k tokens (language-specific analysis + fix generation)

**Safety:**
- No code execution; static analysis only
- Sandbox file reads (no writes without explicit user consent)
- Redact any accidentally detected secrets before output

**Auditability:**
- Log all rule applications with source citations
- Include style guide versions in output metadata
- Emit deterministic results (same input → same output)

**Performance:**
- T1 response time: <2 seconds for files ≤1000 lines
- T2 response time: <5 seconds for files ≤1000 lines
- Fail fast on files >10,000 lines (recommend splitting)

---

## Resources

**Language-Specific Rule Mappings:**
- `/resources/language-rules.json` - Complete rule ID to description mappings

**Official Style Guides (accessed 2025-10-25T21:30:36-04:00):**
1. [Google Style Guides (multi-language)](https://google.github.io/styleguide/)
2. [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
3. [Effective Go](https://go.dev/doc/effective_go)
4. [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
5. [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
6. [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

**Community Standards:**
- [Swift.org API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/)

**Tool Integration Guides:**
- ESLint, Pylint, golangci-lint, ktlint, Clippy configuration templates in `resources/tool-configs/`
