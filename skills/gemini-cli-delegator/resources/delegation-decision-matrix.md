# Delegation Decision Matrix

**Version:** 1.0.0
**Last Updated:** 2025-10-25T23:14:09-04:00
**Purpose:** Deterministic routing rules for Claude vs Gemini task delegation

---

## Primary Decision Table

| Task Type | File Count | File Size | Estimated Tokens | Recommended Tool | Confidence |
|-----------|------------|-----------|------------------|------------------|------------|
| Analysis | 1 | >100KB | >25k | Gemini | High |
| Analysis | 1 | <50KB | <12.5k | Claude | High |
| Analysis | 1 | 50-100KB | 12.5k-25k | Gemini | Medium |
| Analysis | >20 | Any | >150k | Gemini | High |
| Analysis | 5-20 | Any | 50k-150k | Gemini | Medium |
| Review | >50 | Any | >200k | Gemini | High |
| Review | 10-50 | Any | 50k-200k | Gemini | Medium |
| Review | <10 | <500KB total | <125k | Claude | Low |
| Edit/Refactor | Any | Any | Any | Claude | High |
| Debug | 1-3 | <200KB | <50k | Claude | High |
| Debug | >3 | >200KB | >50k | Split: Gemini analyze → Claude fix | High |
| Summarize | 1 | >500KB | >125k | Gemini | High |
| Summarize | 1 | <100KB | <25k | Claude | Medium |
| Code Testing | Any | Any | Any | Gemini (sandbox-test) | High |
| Dependency Analysis | >10 files | Any | >50k | Gemini | High |

---

## Context Size Thresholds

| Threshold | Value | Rationale | Source |
|-----------|-------|-----------|--------|
| Single file - Small | <50KB | Claude handles efficiently | Empirical |
| Single file - Medium | 50-100KB | Borderline; consider task type | Empirical |
| Single file - Large | >100KB | Gemini preferred for deep analysis | Empirical |
| Multi-file - Few | <10 files | Claude context sufficient | Claude 200k window |
| Multi-file - Many | 10-50 files | Approaching Claude limits | Claude 200k window |
| Multi-file - Massive | >50 files | Exceeds Claude optimal use | Claude 200k window |
| Token estimate - Low | <50k tokens | Claude excellent | Claude specs |
| Token estimate - Medium | 50k-150k tokens | Claude acceptable; Gemini better for analysis | Claude vs Gemini comparison |
| Token estimate - High | >150k tokens | Gemini 1M window advantage | Gemini long-context docs |

---

## Task Type Strengths

### Claude Strengths
- **Precise editing**: Code refactoring, targeted fixes
- **Interactive debugging**: Step-by-step problem solving
- **Tool integration**: API calls, file operations, git commands
- **Iterative refinement**: Back-and-forth clarification
- **Small-medium context**: Up to 150k tokens

### Gemini Strengths
- **Large document comprehension**: PDFs, lengthy codebases
- **Holistic analysis**: Multi-file dependency tracking
- **Context caching**: Efficient repeated queries on same large context
- **Sandbox execution**: Safe code testing
- **Massive context**: Up to 1M tokens

---

## Special Cases

### Case 1: Mixed Task (Understanding + Modification)
**Example:** "Understand the authentication flow and fix the bug"

**Strategy:**
1. Delegate analysis to Gemini: "analyze @src/auth/ and map the authentication flow"
2. Receive Gemini's summary
3. Use Claude for precise fix based on summary

**Rationale:** Leverage Gemini's comprehension + Claude's precision

### Case 2: Iterative Codebase Exploration
**Example:** User asks follow-up questions about large codebase

**Strategy:**
1. First query: Delegate to Gemini with context caching
2. Subsequent queries: Continue with Gemini (cached context)
3. Transition to Claude only when switching to editing mode

**Rationale:** Gemini's context caching reduces cost/latency for repeated queries

### Case 3: Security-Sensitive Code
**Example:** Analysis of authentication or encryption logic

**Strategy:**
1. Screen for secrets (API keys, credentials)
2. If secrets detected: Abort; prompt user to sanitize
3. If clean: Delegate to Gemini sandbox for isolated analysis
4. Never expose secrets to either tool

**Rationale:** Sandbox isolation + secret screening prevents leaks

---

## Abort Conditions

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Secrets detected | Abort delegation; return error | Prevent credential exposure |
| >500 files | Prompt user to narrow scope | Risk of timeout/performance degradation |
| MCP unavailable | Return setup instructions; do not proceed | Required infrastructure missing |
| PII in files | Warn user; require explicit confirmation | Privacy protection |

---

## Version History

- **1.0.0** (2025-10-25): Initial decision matrix with empirical thresholds

---

## References

- Claude context window: ~200k tokens (effective), 500k max (official)
- Gemini context window: 1M tokens (Gemini 1.5/2.0 Pro)
- Token estimation: ~4 bytes/token (rough approximation)
- Sources: Claude docs, Gemini API docs (accessed 2025-10-25T23:14:09-04:00)
