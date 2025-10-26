# Changelog - Codex CLI Delegator

All notable changes to the Codex CLI Delegator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-10-26

### Changed
- **BREAKING:** Removed T2 extended validation workflow entirely
- Simplified Procedure to T1 only (≤2k tokens)
- Reduced delegation decision from 9 steps to 2 steps
- Simplified Output Contract to 4 required fields (from 9 fields)
- Removed hybrid mode (recommend separate validation agent instead)
- Updated Decision Rules to simple criteria lists (removed complex scoring)
- Streamlined Quality Gates to focus on essential safety checks
- Updated Examples to show simple delegation only (removed complex scenarios)

### Removed
- T2 scoring matrix workflow (moved to separate agent concern)
- Hybrid delegation mode (codex generates + claude reviews)
- Complex threshold calculations (file counts, pattern counts, etc.)
- Extended quality checks (lint/test/security now handled by separate agents)
- Multi-step validation and quality check definitions
- Estimated files/tokens fields from output contract
- Execution mode field (always non-interactive for simplicity)

### Rationale
- T1-only design reduces skill token footprint by ~60%
- Simple binary decision (codex vs claude) is faster and clearer
- Complex validation workflows should be handled by dedicated validation agents
- Maintains backward compatibility for basic delegation use cases
- Aligns with CLAUDE.md progressive disclosure principle

## [1.0.0] - 2025-10-25

### Added
- Initial release of Codex CLI Delegator skill
- Intelligent task routing between Claude and OpenAI Codex CLI
- T1 fast-path delegation for simple boilerplate generation (≤2k tokens)
- T2 extended routing with scoring system and validation (≤6k tokens)
- Comprehensive decision matrix for delegation decisions
- Support for interactive and non-interactive Codex execution modes
- Hybrid mode for Codex generation + Claude review
- Quality gates including linting, testing, and security scanning
- Pre-checks for Codex CLI availability and authentication
- Output contract with required fields and validation rules
- Example delegation decision tree
- Configuration template for ~/.codex/config.toml
- Delegation decision matrix with task type recommendations
- Complete Codex CLI command reference
- 5 evaluation scenarios covering common delegation use cases

### Documentation
- Front-matter with all required keys per CLAUDE.md specification
- 8 required sections in correct order
- Token budgets visible in Procedure section
- 4 authoritative sources with access dates (2025-10-25T23:27:14-04:00)
- Example kept to ≤30 lines including fences
- Links to official Codex documentation and best practices

### Resources
- codex-config-template.toml - Configuration template with security defaults
- delegation-decision-matrix.md - Comprehensive task routing matrix
- codex-commands.md - Complete CLI command reference and patterns
- delegation-example.txt - Sample decision tree walkthrough

### Security
- No secrets or API keys in examples (placeholders only)
- Security scanning required for all generated code
- Manual review required for hybrid and security-sensitive tasks
- Blocked dangerous commands in configuration template
- Validation of file paths before operations

### Quality Assurance
- Token budgets enforced: T1 ≤2k, T2 ≤6k
- Lint and review required for all delegations
- Test coverage ≥70% for generated tests
- Decision matrix scores tracked for continuous improvement
- Audit trail for all delegation decisions

---

## Version Notes

**Version 1.0.0** establishes the foundational delegation framework for routing code generation tasks between Claude and Codex CLI. The skill focuses on progressive disclosure (T1 fast-path for 80% of cases, T2 extended for complex scenarios) and maintains strict quality gates while keeping token usage minimal.

Future versions may add:
- T3 deep-dive tier for multi-repository orchestration
- Integration with additional code generation tools
- Enhanced hybrid mode workflows
- ML-based delegation scoring improvements
- Performance metrics and optimization recommendations
