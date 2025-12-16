# 🔧 Cognitive Toolworks

> Generate cross-platform agent artifacts (SKILL.md, AGENTS.md) using LLM intelligence.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/cognitive-toolworks.svg)](https://pypi.org/project/cognitive-toolworks/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/williamzujkowski/cognitive-toolworks/workflows/tests/badge.svg)](https://github.com/williamzujkowski/cognitive-toolworks/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Transform MCP servers and repositories into **SKILL.md** and **AGENTS.md** files compatible with Claude, Codex, and other agents.

> **Status**: Active development. MCP generation is stable; other sources (OpenAPI, README) are planned.

## 🎯 What It Does

- **Generate SKILL.md from MCP servers**: Introspect MCP server capabilities and generate structured skill files
- **Generate AGENTS.md from repos**: Analyze repositories and create agent configuration files
- **Validate cross-platform**: Check skills against Anthropic and OpenAI specifications
- **Analyze & optimize**: Token counting, security scanning, coverage analysis

## 🚀 Quick Start

```bash
# Install from PyPI
pip install cognitive-toolworks

# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Generate skill from MCP server
ct generate skill --from-mcp ./github-mcp.json --output ./github-skill/

# Generate AGENTS.md for your repo
ct generate agents-md --repo . --output ./AGENTS.md

# Analyze existing skill
ct analyze ./my-skill/ --full-report
```

**Full walkthrough**: [docs/QUICKSTART.md](docs/QUICKSTART.md)

## 📦 Installation

```bash
# From PyPI (recommended)
pip install cognitive-toolworks

# With development dependencies (for contributors)
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
pip install -e ".[dev]"
```

**Requirements**:
- Python 3.11+
- `ANTHROPIC_API_KEY` environment variable for LLM generation

## 📖 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)**: Get started in 5 minutes
- **[CLI Reference](docs/CLI_REFERENCE.md)**: Complete command documentation
- **[Coverage Matrix](docs/COVERAGE_MATRIX.md)**: Feature coverage and roadmap

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

# Generate skill
ct generate skill \
  --from-mcp github-mcp.json \
  --platform universal \
  --output ./github-skill/
```

### Generate AGENTS.md

```bash
# Analyze repo and generate AGENTS.md
ct generate agents-md --repo . --output ./AGENTS.md

# Also generate llms.txt
ct generate agents-md --repo . --with-llms-txt
```

### Analyze & Validate

```bash
# Full quality analysis
ct analyze ./my-skill/ --full-report

# Validate against platforms
ct validate ./my-skill/ --platforms anthropic,openai

# Optimize for progressive disclosure (LLM-powered)
ct optimize ./my-skill/ --tier T2 --dry-run

# Optimize in-place
ct optimize ./my-skill/ --tier T2 --in-place

# Legacy whitespace-only optimization
ct optimize ./my-skill/ --legacy

# Security scan
ct security-scan ./skills/ --recursive
```

**See full CLI reference**: [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md)

## 📁 Output Formats

### SKILL.md

```yaml
---
name: github-operations
description: "GitHub repository management."
allowed-tools: Bash, Read
---

# GitHub Operations

## When to Use This Skill
- User mentions GitHub repos, issues, or pull requests
- User wants to search code across repositories

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
```

## 🏗️ Architecture

```
Sources          →   LLM Analysis   →   Generation   →   Validation
─────────────────────────────────────────────────────────────────────
• MCP Server         Semantic           SKILL.md        Anthropic
• Repository         Analysis           AGENTS.md       OpenAI
                     Workflows          llms.txt
```

**Design Principles**:

1. **Progressive Disclosure**: Level 1 (~100 tokens) → Level 2 (<5k tokens) → Level 3 (unbounded)
2. **Cross-Platform**: Generate once, validate for multiple platforms
3. **Security-First**: Built-in pattern detection for credentials, shell injection, file access

## 🔒 Security

Built-in security scanning detects:
- ⚠️ Unrestricted file system access
- ⚠️ Network calls without allowlisting
- ⚠️ Shell command injection vectors
- ⚠️ Sensitive data exposure

```bash
ct security-scan ./skills/ --recursive
```

## 🔧 Configuration

```bash
# Required
export ANTHROPIC_API_KEY=sk-ant-...
```

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

Built for the AI agent ecosystem:
- [Anthropic Skills](https://github.com/anthropics/skills)
- [AGENTS.md](https://agents.md/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Made by [William Zujkowski](https://williamzujkowski.github.io)**
