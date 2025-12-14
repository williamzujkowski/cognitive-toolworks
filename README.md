# 🔧 Cognitive Toolworks

> **AI-Native Skill Forge**: Generate cross-platform agent artifacts using LLM intelligence.

[![PyPI version](https://badge.fury.io/py/cognitive-toolworks.svg)](https://badge.fury.io/py/cognitive-toolworks)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Transform MCP servers, APIs, and documentation into high-quality **SKILL.md** and **AGENTS.md** files compatible with the [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) ecosystem (Claude, Codex, Gemini CLI).

## 🎯 Why Cognitive Toolworks?

The AI agent ecosystem is converging on shared standards:
- **Anthropic Skills** (`SKILL.md`) - Progressive disclosure architecture for Claude
- **OpenAI Skills** (`~/.codex/skills/`) - Same format, adopted Dec 2025
- **AGENTS.md** - Universal coding agent instructions (60k+ repos)
- **MCP** - Model Context Protocol (10k+ servers)

**Problem**: Converting between these formats and generating high-quality artifacts is manual and error-prone.

**Solution**: LLM-powered generation that understands semantics, not just templates.

| Feature | Template Tools | Cognitive Toolworks |
|---------|---------------|---------------------|
| Generation | Mechanical | LLM-powered semantic analysis |
| Sources | MCP only | MCP, OpenAPI, README, scripts |
| Output | Single platform | Universal (Anthropic + OpenAI) |
| Quality | Basic | Token optimization, security scan |
| Examples | Manual | Auto-generated |

## 🚀 Quick Start

```bash
# Install
pip install cognitive-toolworks

# Generate skill from MCP server
ct generate skill --from-mcp ./github-mcp.json --output ./github-skill/

# Generate AGENTS.md for your repo
ct generate agents-md --repo . --output ./AGENTS.md

# Analyze existing skill
ct analyze ./my-skill/SKILL.md --full-report
```

## 📦 Installation

```bash
# Basic installation
pip install cognitive-toolworks

# With claude-flow orchestration support
pip install cognitive-toolworks[claude-flow]

# Development installation
pip install cognitive-toolworks[dev]
```

**Requirements**:
- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable for LLM generation

## 📖 Usage

### Generate Skill from MCP Server

```bash
# Create MCP config
cat > github-mcp.json << 'EOF'
{
  "name": "github",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {"GITHUB_TOKEN": "$GITHUB_TOKEN"}
}
EOF

# Generate universal skill (works with Claude + Codex)
ct generate skill \
  --from-mcp github-mcp.json \
  --platform universal \
  --output ./github-skill/
```

### Generate from OpenAPI

```bash
ct generate skill \
  --from-openapi https://api.example.com/openapi.json \
  --name "example-api" \
  --focus-endpoints /users,/projects
```

### Generate AGENTS.md

```bash
# Analyze repo and generate AGENTS.md
ct generate agents-md --repo . --output ./AGENTS.md

# Also generate llms.txt
ct generate agents-md --repo . --with-llms-txt
```

### Analyze & Optimize

```bash
# Full quality analysis
ct analyze ./my-skill/ --full-report

# Validate against platforms
ct validate ./my-skill/ --platforms anthropic,openai

# Optimize token usage
ct optimize ./my-skill/ --target-tokens 5000

# Security scan
ct security-scan ./skills/ --recursive
```

### Multi-Agent Orchestration

For complex generation with parallel agents:

```bash
# Install claude-flow
pip install cognitive-toolworks[claude-flow]

# Run orchestrated generation
ct generate skill \
  --from-mcp ./config.json \
  --orchestrated \
  --examples 5
```

## 📁 Output Formats

### SKILL.md (Universal)

```yaml
---
name: github-operations
description: "GitHub repository management. Use when users reference repos, issues, or PRs."
allowed-tools: Bash, Read
dependencies:
  - "@modelcontextprotocol/server-github"
---

# GitHub Operations

## When to Use This Skill
- User mentions GitHub repos, issues, or pull requests
- User wants to search code across repositories
- User needs to manage GitHub workflows

## Quick Reference
...
```

### AGENTS.md

```markdown
# AGENTS.md

## Dev Environment
- Setup: `npm install && npm run build`
- Test: `npm test`

## Testing Instructions
- Run `npm test` before opening PRs
- Coverage must be >= 80%

## PR Instructions
- Title format: `[component] Brief description`
- Required: Tests, types, docs
```

## 🏗️ Architecture

```
Sources          →   LLM Analysis   →   Generation   →   Validation   →   Output
─────────────────────────────────────────────────────────────────────────────────
• MCP Server         Semantic           SKILL.md        Anthropic        Universal
• OpenAPI            Analysis           AGENTS.md       OpenAI           Skills
• README             Relationships      llms.txt        AAIF
• Scripts            Workflows
• Docs
```

**Key Design Principles**:

1. **Progressive Disclosure**: Level 1 (~100 tokens) → Level 2 (<5k tokens) → Level 3 (unbounded)
2. **Cross-Platform**: Generate once, use everywhere
3. **Security-First**: Built-in pattern detection
4. **LLM-Native**: Semantic understanding, not string templates

## 🔒 Security

Cognitive Toolworks includes built-in security scanning:

```bash
ct security-scan ./skills/ --recursive
```

**Detects**:
- ⚠️ Unrestricted file system access
- ⚠️ Network calls without allowlisting
- ⚠️ Shell command injection vectors
- ⚠️ Sensitive data exposure
- ⚠️ Tool permission escalation

## 🔧 Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...     # Required for LLM generation
CT_DEFAULT_PLATFORM=universal    # Default output platform
CT_TOKEN_BUDGET=5000             # Default Level 2 token budget
CT_CACHE_DIR=~/.cache/ct         # Cache directory
CT_MODEL=claude-sonnet-4-20250514  # Default model
```

### Config File

```yaml
# ~/.config/cognitive-toolworks/config.yaml
default_platform: universal
token_budget: 5000
example_count: 3
security_scan: true
models:
  analysis: claude-sonnet-4-20250514
  generation: claude-sonnet-4-20250514
  examples: claude-haiku-4-20250514
```

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Architecture Overview](docs/architecture.md)
- [Claude-Flow Integration](docs/claude-flow.md)
- [Security Best Practices](docs/security.md)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Setup development environment
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run linting
ruff check . && ruff format . && mypy src/
```

## 📜 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built for the [Agentic AI Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) ecosystem:
- [Anthropic Skills](https://github.com/anthropics/skills)
- [AGENTS.md](https://agents.md/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude-Flow](https://github.com/ruvnet/claude-flow)

---

**Made with 🧠 by [William Zujkowski](https://williamzujkowski.github.io)**
