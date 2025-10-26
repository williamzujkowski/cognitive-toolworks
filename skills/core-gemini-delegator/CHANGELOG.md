# Changelog - Gemini CLI Delegator Skill

All notable changes to the `gemini-cli-delegator` skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-25

### Added
- Initial release of gemini-cli-delegator skill
- Core delegation decision logic with T1 (≤2k tokens) and T2 (≤6k tokens) tiers
- Decision matrix for task routing between Claude and Gemini
- Security pre-checks for secrets and PII detection
- Context size estimation (file count, total size KB, estimated tokens)
- MCP configuration template for gemini-mcp-tool integration
- Comprehensive decision matrix with 15+ routing rules
- 30-line example demonstrating delegation decision tree
- Support for task types: analysis, review, edit, debug, test, summarize
- Thresholds: >100KB file size, >20 file count, >150k tokens → delegate to Gemini
- Sandbox code testing integration via Gemini MCP
- Output contract with TypeScript-style schema
- Quality gates: token budgets, security checks, determinism requirements

### Documentation
- SKILL.md with complete Anthropic Skills standard compliance
- Front-matter with all required keys (name, slug, description, capabilities, etc.)
- 8 required sections in specified order
- 4 primary sources with access dates (2025-10-25T23:14:09-04:00)
- MCP configuration template (mcp-config-template.json)
- Delegation decision matrix (delegation-decision-matrix.md)
- Example file with decision tree walkthrough

### Testing
- 5 evaluation scenarios in tests/evals_gemini-cli-delegator.yaml
- Coverage: large PDF, codebase review, small file, multi-file analysis, sandbox testing

### References
- Gemini MCP Tool: https://github.com/jamubc/gemini-mcp-tool
- Gemini Long Context: https://ai.google.dev/gemini-api/docs/long-context
- MCP Specification: https://docs.claude.com/en/docs/mcp
- MCP Announcement: https://www.anthropic.com/news/model-context-protocol

---

## [2.0.0] - 2025-10-26

### Changed (BREAKING)
- **Simplified to T1 only** (≤2k tokens): Removed T2 extended analysis tier
- Reduced procedure from 8 steps to 2 steps
- Simplified decision logic: file size >100KB OR task type = analysis/review → delegate
- Removed complex multi-file orchestration (now out of scope)
- Streamlined output contract: removed `context_estimate` field
- Reduced from 4 sources to 3 sources
- Decision matrix moved to `resources/` as static reference (not computed)

### Removed
- T2 multi-file codebase analysis (5 steps)
- File counting and total size aggregation logic
- Token estimation formulas
- Complex ambiguity handling rules
- MCP availability pre-check (assumed configured)

### Improved
- Token budget reduced from ~8k (T1+T2) to ~2k (T1 only)
- Faster decision path: 2 steps vs 8 steps
- Clearer scope: simple delegation only
- Added second example showing "keep in Claude" case

### Migration Notes
- Multi-file orchestration should use separate orchestration agent
- Existing trigger patterns remain backward compatible
- If you need complex codebase analysis, use a dedicated orchestration skill

---

## [Unreleased]

### Planned
- Performance metrics logging (optional)
- Integration with orchestration agent for multi-file workflows
