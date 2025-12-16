# Quick Start Guide

Get started with cognitive-toolworks in 5 minutes.

## Installation

### From PyPI (Recommended)

```bash
pip install cognitive-toolworks
```

### From Source

```bash
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks
pip install -e .
```

## Prerequisites

**Python 3.11+** is required.

Set your Anthropic API key for LLM-powered features:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Get your API key from: https://console.anthropic.com/

## Basic Usage

### 1. Generate Skill from MCP Server

Create a skill definition from an MCP (Model Context Protocol) server:

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
ct generate skill --from-mcp github-mcp.json --output ./github-skill/
```

Output: `./github-skill/SKILL.md` with structured agent instructions.

### 2. Generate AGENTS.md for Your Repository

Analyze your repository and create agent configuration:

```bash
ct generate agents-md --repo . --output ./AGENTS.md
```

This analyzes:
- Package configuration (package.json, pyproject.toml, etc.)
- CI/CD setup (.github/workflows, .gitlab-ci.yml, etc.)
- Build tools (Makefile, scripts, etc.)
- Existing documentation

### 3. Validate Skill Quality

Check a skill against platform specifications:

```bash
ct validate ./github-skill/ --platforms anthropic,openai
```

Checks:
- Frontmatter validity
- Description length (≤160 chars)
- Token budgets (T1 ≤2k, T2 ≤6k, T3 ≤12k)
- Platform-specific requirements

### 4. Analyze Skill Metrics

Get quality and efficiency metrics:

```bash
ct analyze ./github-skill/ --full-report
```

Reports:
- Token counts per tier (T1/T2/T3)
- Progressive disclosure score
- Security issues
- Cross-platform compatibility

### 5. Optimize for Token Efficiency

Reduce token usage while maintaining quality:

```bash
# Preview changes
ct optimize ./github-skill/ --tier T2 --dry-run

# Apply optimizations
ct optimize ./github-skill/ --tier T2 --in-place
```

Target tiers:
- **T1**: ≤2k tokens (fast path, 80% of requests)
- **T2**: ≤6k tokens (extended validation)
- **T3**: ≤12k tokens (deep research)

## Common Workflows

### Workflow 1: MCP Server → Skill

```bash
# 1. Introspect MCP server
ct introspect mcp ./mcp-config.json --output analysis.json

# 2. Generate skill
ct generate skill --from-analysis analysis.json --output ./skill/

# 3. Validate
ct validate ./skill/ --platforms anthropic

# 4. Optimize if needed
ct optimize ./skill/ --tier T1 --dry-run
```

### Workflow 2: Repository → AGENTS.md

```bash
# 1. Generate AGENTS.md
ct generate agents-md --repo . --with-llms-txt

# 2. Review output
cat AGENTS.md

# 3. Commit to repository
git add AGENTS.md llms.txt
git commit -m "docs: add agent configuration"
```

### Workflow 3: Security Audit

```bash
# Scan all skills
ct security-scan ./skills/ --recursive --output security-report.json

# Review issues
cat security-report.json | jq '.issues'
```

## What Gets Generated?

### SKILL.md Structure

```yaml
---
name: github-operations
description: "GitHub repository management via MCP server."
allowed-tools: Bash, Read
---

# GitHub Operations

## When to Use This Skill
- User mentions GitHub repos, issues, or pull requests
- User wants to search code across repositories

## Quick Reference
**Common Operations:**
- `create_repository`: Create new GitHub repo
- `search_code`: Search across repositories
...
```

### AGENTS.md Structure

```markdown
# AGENTS.md

## Project Overview
This is a Python CLI tool for generating AI agent skills.

## Dev Environment Setup
```bash
pip install -e ".[dev]"
pre-commit install
```

## Testing
Run tests: `pytest`
Coverage: `pytest --cov`
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes (for generation) | Anthropic API access for LLM-powered features |
| `GITHUB_TOKEN` | No | For GitHub MCP server (if using) |

## Next Steps

- **Detailed CLI Reference**: See [CLI_REFERENCE.md](CLI_REFERENCE.md)
- **Platform-Specific Details**: Check platform docs (Anthropic Skills, AAIF)
- **Advanced Topics**: See [/docs/EXPANSION_ROADMAP.md](/docs/EXPANSION_ROADMAP.md)

## Troubleshooting

**"ModuleNotFoundError: No module named 'cognitive_toolworks'"**
- Install package: `pip install cognitive-toolworks`
- Or install from source: `pip install -e .`

**"Missing ANTHROPIC_API_KEY"**
- Set environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`
- Get key from: https://console.anthropic.com/

**"MCP server connection failed"**
- Verify MCP config JSON format
- Check server command is installed: `npx @modelcontextprotocol/server-github --version`
- Ensure environment variables are set (e.g., `GITHUB_TOKEN`)

**Validation errors**
- Use `--fix` flag to auto-fix common issues: `ct validate ./skill/ --fix`
- Check description length: must be ≤160 characters
- Verify frontmatter YAML syntax
