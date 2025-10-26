# Changelog — Agent Creator

All notable changes to the Agent Creator agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial agent specification following CLAUDE.md standards
- 4-step workflow: Research → Design → Generate → Validate
- System prompt design with ≤1500 token constraint
- Tool usage guidelines for Read, Write, Bash, Grep, Glob, WebFetch
- Skills integration patterns (reference by slug only)
- Security auditor creation example (≤30 lines)
- Quality gates for frontmatter, token limits, tool restrictions
- Resource citations with NOW_ET timestamps
- Index entry generation for /index/agents-index.json

### Design Decisions
- Model set to "inherit" for flexibility across Sonnet/Opus/Haiku
- Default toolset: Read, Write, Bash, Grep, Glob (minimal but sufficient)
- System prompt extraction to workflows/ when >1500 tokens
- Agent vs Skill decision rule: ≥3 steps = agent, <3 steps = recommend skill

### Quality Metrics
- System prompt: 1,247 tokens (within 1,500 limit)
- Description: 124 characters (within 160 limit)
- Example: 42 lines total (security-auditor-creation.txt)
- Sources cited: 6 with access dates
- Tool restrictions: All MCP-approved

### References
- Migrated from /skills/agent-creation/SKILL.md (deprecated)
- Follows CLAUDE.md v1.1.0 agent specification format
- Based on Claude Code Sub-Agents documentation (accessed 2025-10-26T01:19:05-04:00)
