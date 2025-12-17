# Cognitive Toolworks

> Generate cross-platform agent artifacts (SKILL.md, AGENTS.md) using LLM intelligence.

[![Version 2.0.0](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/williamzujkowski/cognitive-toolworks/releases/tag/v2.0.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Transform MCP servers and repositories into **SKILL.md** and **AGENTS.md** files compatible with Claude, Codex, Gemini, and other AI agents.

## What's Included

This repository contains:
- **81 production-ready skills** covering security, cloud, DevOps, testing, and more
- **18 orchestrator agents** that coordinate multiple skills for complex workflows
- **CLI tooling** to generate, validate, and manage your own skills

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- (Optional) `ANTHROPIC_API_KEY` for LLM-powered generation

### Installation

```bash
# Clone the repository
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install
pip install -e .

# Verify installation
ct --version
```

### Your First Commands

```bash
# Explore available skills (no API key needed)
ct ls                           # List all 81 skills
ct search kubernetes            # Search for skills
ct show security-appsec-validator  # View skill details

# Validate a skill
ct validate ./skills/api-design-validator/

# Generate a skill from a README (no API key needed)
ct generate skill --from-readme ./README.md --name my-skill --output ./my-skill/
```

## Feature Status

| Feature | Status | API Key Required |
|---------|--------|------------------|
| Skill Discovery (`ct ls`, `ct search`, `ct show`) | Stable | No |
| MCP Introspection (`ct introspect mcp`) | Stable | No |
| OpenAPI Introspection (`ct introspect openapi`) | Stable | No |
| README Source (`ct generate skill --from-readme`) | Stable | No |
| Skill Validation (`ct validate`) | Stable | No |
| Security Scanning (`ct security-scan`) | Stable | No |
| Skill Generation (`ct generate skill --from-mcp`) | Stable | Yes |
| Skill Optimization (`ct optimize`) | Stable | Yes |
| AGENTS.md Generation (`ct generate agents-md`) | Beta | Yes |

## Using Skills & Agents

### How Skills Work

Skills are self-contained instruction sets that teach AI agents how to perform specific tasks. Each skill follows the [Anthropic SKILL.md format](https://github.com/anthropics/skills) with:

- **Trigger conditions**: When the skill should activate
- **Procedures**: Step-by-step instructions (T1/T2/T3 tiers)
- **Quality gates**: Validation rules and constraints

### Browsing Skills

```bash
# List all skills
ct ls

# Filter by domain
ct ls --domain security    # 11 security skills
ct ls --domain cloud       # 8 cloud architecture skills
ct ls --domain testing     # 5 testing skills

# Search across all skills
ct search "API design"
ct search kubernetes

# View full skill details
ct show api-graphql-designer --full
```

### How Agents Work

Agents are orchestrators that coordinate multiple skills to complete complex workflows. They follow a 4-step pattern:

1. **Plan**: Parse request, identify required skills
2. **Execute**: Invoke skills in sequence
3. **Validate**: Check outputs against quality gates
4. **Report**: Return structured results

```bash
# List all agents
ct ls --agents

# View agent details
ct show cloud-aws-orchestrator --full
```

## CLI Integration

Make skills available to your AI coding assistants:

### Claude Code

Claude Code discovers skills from `~/.claude/skills/` (personal) or `.claude/skills/` (project).

```bash
# Option 1: Personal installation (available in all projects)
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills"/* ~/.claude/skills/

# Option 2: Project-level (committed to repo)
mkdir -p .claude/skills
# Copy specific skills you need
cp -r skills/security-appsec-validator .claude/skills/
```

Verify: Ask Claude Code "What skills are available?"

### Codex CLI

Codex CLI uses AGENTS.md for project instructions and supports fallback files.

```bash
# This repo already includes AGENTS.md - Codex will discover it automatically

# To also support CLAUDE.md, add to ~/.codex/config.toml:
# project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md"]
```

### Gemini CLI

Gemini CLI uses GEMINI.md hierarchy with configurable context files.

```bash
# Option 1: Create settings to recognize AGENTS.md
mkdir -p ~/.gemini
cat > ~/.gemini/settings.json << 'EOF'
{
  "context": {
    "fileName": ["AGENTS.md", "GEMINI.md"]
  }
}
EOF

# Option 2: Create project-level GEMINI.md
cp AGENTS.md GEMINI.md
```

## CLI Reference

### Discovery Commands

```bash
ct ls                              # List all skills
ct ls --domain <domain>            # Filter by domain
ct ls --agents                     # List agents instead
ct ls --format json                # JSON output

ct search <term>                   # Search skills/agents
ct search <term> --format json     # JSON output

ct show <slug>                     # View skill summary
ct show <slug> --full              # View complete skill
```

### Generation Commands

```bash
# Generate skill from MCP server (requires API key)
ct generate skill --from-mcp config.json --output ./my-skill/

# Generate skill from README (no API key)
ct generate skill --from-readme README.md --name my-skill --output ./my-skill/

# Generate skill from OpenAPI spec (requires API key)
ct generate skill --from-openapi spec.json --output ./my-skill/

# Generate AGENTS.md for a repository (requires API key)
ct generate agents-md --repo . --output ./AGENTS.md
```

### Validation Commands

```bash
ct validate ./path/to/skill/       # Validate skill structure
ct validate ./skill/ --verbose     # Verbose output
ct validate ./skill/ --platforms anthropic,openai  # Multi-platform

ct analyze ./path/to/skill/        # Token and quality analysis
ct analyze ./skill/ --full-report  # Detailed report

ct security-scan ./skills/         # Scan for security issues
ct security-scan ./skills/ --recursive  # Recursive scan
```

### Optimization Commands

```bash
# Preview optimization (requires API key)
ct optimize ./my-skill/ --tier T2 --dry-run

# Apply optimization in-place
ct optimize ./my-skill/ --tier T2 --in-place
```

### Introspection Commands

```bash
# Extract tool definitions from MCP server
ct introspect mcp config.json --output analysis.json

# Extract endpoints from OpenAPI spec
ct introspect openapi spec.json --output analysis.json
```

## Architecture

```
Sources          →   LLM Analysis   →   Generation   →   Validation
─────────────────────────────────────────────────────────────────────
• MCP Server         Semantic           SKILL.md        Anthropic
• OpenAPI Spec       Analysis           AGENTS.md       OpenAI
• README             Workflows          llms.txt
```

**Design Principles**:

- **Progressive Disclosure**: T1 (≤2k tokens) → T2 (≤6k tokens) → T3 (≤12k tokens)
- **Cross-Platform**: Generate once, validate for Anthropic and OpenAI
- **Security-First**: Pattern detection for credentials, shell injection, file access

## Security

Built-in security scanning detects:
- Unrestricted file system access
- Network calls without allowlisting
- Shell command injection vectors
- Sensitive data exposure

```bash
ct security-scan ./skills/ --recursive
```

## Claude Code Integration

This repository includes Claude Code slash commands:

```bash
# Available in Claude Code CLI
/skill-validate   # Validate a skill against CLAUDE.md standards
/skill-create     # Create a new skill with proper structure
/skill-search     # Search skills index
/generate-skill   # Generate skill from various sources
/rebuild-index    # Rebuild skills and agents indices
/run-maintenance  # Run full maintenance workflow
```

Slash commands are defined in `.claude/commands/`.

See [llms.txt](./llms.txt) for LLM-friendly project overview.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Setup development environment
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run linting
ruff check . && ruff format . && mypy src/
```

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built for the AI agent ecosystem:
- [Anthropic Skills](https://github.com/anthropics/skills)
- [AGENTS.md](https://agents.md/)
- [llms.txt](https://llmstxt.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Made by [William Zujkowski](https://williamzujkowski.github.io)**
