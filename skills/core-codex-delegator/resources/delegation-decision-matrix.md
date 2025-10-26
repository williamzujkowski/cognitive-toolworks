# Delegation Decision Matrix

## Task Type → Recommendation

| Task Type | Codex Score | Claude Score | Recommendation | Rationale |
|-----------|-------------|--------------|----------------|-----------|
| **New boilerplate generation** | +2 | 0 | CODEX | Codex excels at generating standard patterns from scratch |
| **Project scaffolding** | +2 | 0 | CODEX | Multi-file initialization with clear structure |
| **Test suite generation** | +2 | 0 | CODEX | Generate tests from existing code/specs |
| **CRUD API creation** | +2 | 0 | CODEX | Repetitive patterns with standard conventions |
| **CLI tool generation** | +2 | 0 | CODEX | Boilerplate with argument parsing and commands |
| **Data model/schema creation** | +1 | 0 | CODEX | Structured definitions from specifications |
| **Migration script generation** | +1 | +1 | HYBRID | Generate with Codex, review data safety with Claude |
| **Code completion (>50 lines)** | +1 | 0 | CODEX | Large-scale completion from context |
| **Pseudocode → implementation** | +1 | 0 | CODEX | Direct conversion with clear logic |
| **Bug fix (simple)** | 0 | +1 | CLAUDE | Requires understanding existing context |
| **Bug fix (complex)** | 0 | +2 | CLAUDE | Deep context and debugging required |
| **Refactoring** | 0 | +2 | CLAUDE | Architectural understanding needed |
| **Code review** | 0 | +2 | CLAUDE | Analysis of patterns, security, best practices |
| **Security audit** | 0 | +2 | CLAUDE | Deep security analysis required |
| **Performance optimization** | 0 | +2 | CLAUDE | Profiling analysis and context understanding |
| **API integration** | 0 | +1 | CLAUDE | Domain knowledge and error handling |
| **Database query optimization** | 0 | +2 | CLAUDE | Requires understanding of data patterns and indexes |
| **Architecture design** | 0 | +2 | CLAUDE | Strategic decisions requiring domain expertise |
| **Legacy code modernization** | +1 | +2 | HYBRID | Generate modern patterns, but review carefully |
| **Documentation generation** | +1 | +1 | HYBRID | Codex generates, Claude ensures accuracy |

## Scoring Rules

### Codex Points (+)
- **+2 (Always Codex):** New file generation, boilerplate, scaffolds, templates
- **+1 (Prefer Codex):** Code completion, pseudocode conversion, repetitive patterns

### Claude Points (+)
- **+2 (Always Claude):** Security, architecture, refactoring, debugging complex issues
- **+1 (Prefer Claude):** Bug fixes, API integration, existing code modifications

### Decision Thresholds
- **Codex score ≥3 AND Claude score ≤1:** Delegate to Codex
- **Claude score ≥3:** Keep in Claude
- **Scores within 1 point:** Hybrid mode (Codex generates, Claude reviews)
- **Equal scores:** Default to Claude for safety

## Complexity Adjustments

| Complexity | Adjustment | Notes |
|------------|-----------|-------|
| Simple | No change | Follow base scores |
| Moderate | +1 to higher score | Amplify the leading recommendation |
| Complex | Claude +1 | Complex tasks benefit from Claude's reasoning |

## Context Requirements

| Context Type | Impact | Recommendation |
|--------------|--------|----------------|
| Zero existing files | Codex +1 | Fresh start favors generation |
| 1-3 existing files | No change | Base scoring applies |
| 4+ existing files | Claude +1 | Extensive context benefits Claude |
| Business logic heavy | Claude +2 | Domain expertise required |
| Security-sensitive | Claude +2 | Manual review critical |

## Examples

### Example 1: "Create a REST API for user management"
- Task: New boilerplate → Codex +2
- Files: 0 existing → Codex +1
- Pattern: CRUD operations → Codex +1
- **Total: Codex 4, Claude 0 → CODEX**

### Example 2: "Fix the authentication bug in login.py"
- Task: Bug fix → Claude +1
- Files: 1 existing → No change
- Security: Auth-related → Claude +2
- **Total: Codex 0, Claude 3 → CLAUDE**

### Example 3: "Generate integration tests for payment.py"
- Task: Test generation → Codex +2
- Files: 1 existing (context needed) → Claude +1
- Security: Payment processing → Claude +1
- **Total: Codex 2, Claude 2 → HYBRID**

## File Count Heuristics

- **0 files:** Codex favored (new project)
- **1-2 files:** Neutral (use task-based scoring)
- **3-5 files:** Slight Claude favor (context matters)
- **6+ files:** Strong Claude favor (comprehensive context)

## Language-Specific Considerations

| Language | Codex Strength | Claude Strength |
|----------|----------------|-----------------|
| Python | Boilerplate, scripts, data processing | Complex async, performance, security |
| JavaScript/TypeScript | React components, API routes | State management, refactoring |
| Rust | Basic structs/traits | Memory safety, concurrency |
| SQL | Schema generation | Query optimization, migrations |
| Shell | Script generation | Complex pipelines, error handling |

## Quality Gate Integration

All delegations must pass:
1. **Pre-execution:** Validate Codex CLI installed and authenticated
2. **Post-generation:** Lint, format, and security scan
3. **Pre-commit:** Manual review required for hybrid/security-sensitive tasks
