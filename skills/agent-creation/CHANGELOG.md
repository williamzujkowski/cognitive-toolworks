# Changelog — agent-creation skill

All notable changes to the agent-creation skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of agent-creation skill
- AGENT.md generation with YAML frontmatter
- 8 required sections following CLAUDE.md standards
- System prompt design (≤1500 tokens)
- Tool restriction specifications
- Workflow pattern templates
- Skills integration guidelines
- T1/T2/T3 tiered procedures
- Agent vs skill decision rules
- Example agent: security-auditor
- Template resource: agent-template.md
- Output contract with TypeScript interface
- Quality gates: frontmatter, system prompt length, examples, tools validation
- Citations: Claude Code docs, MCP specs, agent design patterns

### Metadata
- **Tier**: T2 (≤6000 tokens)
- **Token budget**: T1≤2k, T2≤6k, T3≤12k
- **Sources**: 5 authoritative links with access dates
- **Example**: cost-optimizer agent creation
- **Owner**: cognitive-toolworks
- **License**: Apache-2.0
