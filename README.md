# 🔧 Cognitive Toolworks

> Generate cross-platform agent artifacts (SKILL.md, AGENTS.md) using LLM intelligence.

[![Version 2.0.0](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/williamzujkowski/cognitive-toolworks/releases/tag/v2.0.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Transform MCP servers and repositories into **SKILL.md** and **AGENTS.md** files compatible with Claude, Codex, and other agents.

> **Status**: Beta. MCP introspection and skill generation work. OpenAPI introspection functional. README support planned.

## 🎯 What It Does

**Working Features**:
- **Discover Skills**: Browse, search, and inspect skills with `ct ls`, `ct search`, and `ct show`
- **MCP Introspection**: Extract tool definitions from MCP servers (`ct introspect mcp`)
- **Skill Generation**: Generate SKILL.md from MCP servers with LLM assistance (`ct generate skill --from-mcp`)
- **Validation**: Check skills against Anthropic/OpenAI specs, token budgets, and security rules
- **Analysis**: Token counting, security scanning, quality gates

**Experimental**:
- **OpenAPI Introspection**: Extract endpoints from OpenAPI specs (`ct introspect openapi`)
- **Optimization**: LLM-powered skill trimming (`ct optimize`)

**Beta**:
- **AGENTS.md Generation**: Analyze repos and generate agent configs (`ct generate agents-md`, `ct analyze-repo`)

**Planned**:
- **README Source**: Generate skills from README files

## 🚀 Quick Start

**No API Key Required**:
```bash
# Install
pip install -e .

# Browse and discover skills
ct ls                           # List all skills
ct search kubernetes            # Search for skills
ct show api-graphql-designer    # View skill details

# Validate and analyze
ct validate ./my-skill/         # Check against specs
ct analyze ./my-skill/          # Quality and token analysis
ct security-scan ./skills/      # Security checks

# Introspect sources
ct introspect mcp config.json --output analysis.json
```

**Requires ANTHROPIC_API_KEY**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Generate skill from MCP
ct generate skill --from-mcp ./github-mcp.json --output ./github-skill/

# Generate AGENTS.md
ct generate agents-md --repo . --output ./AGENTS.md

# Optimize existing skills
ct optimize ./my-skill/ --tier T2 --in-place
```

## 📦 Installation

```bash
# Clone and install
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
pip install -e .

# With development dependencies
pip install -e ".[dev]"
```

**Requirements**:
- Python 3.11+
- `ANTHROPIC_API_KEY` for LLM-powered generation and optimization (not required for discovery, validation, or analysis)

## 📖 Usage

### Introspect and Generate from MCP

```bash
# Step 1: Create MCP config
cat > github-mcp.json << 'EOF'
{
  "name": "github",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {"GITHUB_TOKEN": "$GITHUB_TOKEN"}
}
EOF

# Step 2: Introspect to extract tool definitions (no API key)
ct introspect mcp github-mcp.json --output github-analysis.json

# Step 3: Generate SKILL.md with LLM (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
ct generate skill \
  --from-mcp github-mcp.json \
  --platform universal \
  --output ./github-skill/

# Or use pre-analyzed data
ct generate skill \
  --from-analysis github-analysis.json \
  --name github \
  --output ./github-skill/
```

### Discover & Browse Skills

```bash
# List all skills
ct ls

# List skills by domain
ct ls --domain security
ct ls --domain cloud

# Search for skills
ct search kubernetes
ct search "API security"

# Show skill details
ct show api-graphql-designer
ct show security-appsec-validator --full

# Output formats
ct ls --format json        # JSON output
ct ls --format simple      # Simple text
ct search graphql --format json
```

### Validate, Analyze & Optimize

```bash
# Validate skill structure and rules (no API key)
ct validate ./my-skill/
ct validate ./my-skill/ --platforms anthropic,openai --verbose

# Quality and token analysis (no API key)
ct analyze ./my-skill/ --full-report

# Security scanning (no API key)
ct security-scan ./skills/ --recursive

# LLM-powered optimization (requires ANTHROPIC_API_KEY)
ct optimize ./my-skill/ --tier T2 --dry-run   # Preview changes
ct optimize ./my-skill/ --tier T2 --in-place  # Apply changes
```

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

**Implementation Status**:

1. **Phase 1 (Stable)**: MCP introspection, skill generation with LLM fallback
2. **Phase 2 (Stable)**: Eval runner, quality gates, validation framework
3. **Phase 3 (Stable)**: Discovery commands (ls, search, show), skill browsing
4. **Beta**: AGENTS.md generation, repository analysis
5. **Future**: README source support, multi-agent orchestration

**Design Principles**:

- **Progressive Disclosure**: T1 (≤2k tokens) → T2 (≤6k tokens) → T3 (≤12k tokens)
- **Cross-Platform**: Generate once, validate for Anthropic and OpenAI
- **Security-First**: Pattern detection for credentials, shell injection, file access

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
# Required for LLM-powered features only (generate, optimize)
export ANTHROPIC_API_KEY=sk-ant-...

# Discovery, validation, analysis, and security scanning work without API key
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
