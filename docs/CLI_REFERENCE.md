# CLI Reference

Complete reference for all cognitive-toolworks commands.

## Global Options

```bash
ct --help                    # Show help
ct --version                 # Show version
ct --install-completion      # Install shell completion
ct --show-completion         # Show completion script
```

## Commands Overview

| Command | Purpose |
|---------|---------|
| `generate` | Generate SKILL.md or AGENTS.md from sources |
| `validate` | Validate skills against platform specs |
| `analyze` | Analyze skill quality and token efficiency |
| `optimize` | Optimize skills for progressive disclosure |
| `introspect` | Extract information from sources (MCP, OpenAPI) |
| `security-scan` | Scan skills for security issues |
| `analyze-repo` | Analyze repository structure |
| `benchmark` | Performance benchmarking |

---

## generate

Generate agent artifacts from various sources.

### generate skill

Generate SKILL.md from MCP servers, OpenAPI specs, or README files.

```bash
ct generate skill [OPTIONS]
```

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--from-mcp` | PATH | MCP server config JSON | None |
| `--from-openapi` | TEXT | Path or URL to OpenAPI spec | None |
| `--from-readme` | PATH | Path to README file | None |
| `--from-analysis` | PATH | Path to introspection JSON | None |
| `--name, -n` | TEXT | Skill name (auto-detected if omitted) | None |
| `--platform, -p` | TEXT | Target platform: anthropic, openai, universal | universal |
| `--output, -o` | PATH | Output directory | generated-skill |
| `--examples, -e` | INT | Number of examples to generate | 3 |
| `--token-budget` | INT | Max tokens for Level 2 content | 5000 |
| `--optimize` | FLAG | Run optimization pass | True |
| `--orchestrated` | FLAG | Use claude-flow multi-agent orchestration | False |
| `--dry-run` | FLAG | Preview without writing files | False |

**Examples:**

```bash
# From MCP server
ct generate skill --from-mcp ./github-mcp.json

# From OpenAPI spec (URL)
ct generate skill --from-openapi https://api.example.com/openapi.json

# From OpenAPI spec (local file)
ct generate skill --from-openapi ./api-spec.yaml --name my-api

# From README
ct generate skill --from-readme ./README.md --name my-tool

# Custom output and platform
ct generate skill --from-mcp ./slack-mcp.json \
  --platform anthropic \
  --output ./skills/slack/ \
  --examples 5

# Preview without writing
ct generate skill --from-mcp ./config.json --dry-run

# Use multi-agent orchestration (requires claude-flow)
ct generate skill --from-mcp ./config.json --orchestrated
```

**MCP Config Format:**

```json
{
  "name": "server-name",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-name"],
  "env": {
    "API_KEY": "$API_KEY"
  }
}
```

### generate agents-md

Generate AGENTS.md for a repository.

```bash
ct generate agents-md [OPTIONS]
```

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--repo, -r` | PATH | Path to repository | . |
| `--output, -o` | PATH | Output path for AGENTS.md | AGENTS.md |
| `--with-llms-txt` | FLAG | Also generate llms.txt | False |
| `--dry-run` | FLAG | Preview without writing | False |

**Examples:**

```bash
# Generate for current directory
ct generate agents-md

# Generate for specific repo
ct generate agents-md --repo /path/to/repo --output /path/to/repo/AGENTS.md

# Include llms.txt
ct generate agents-md --with-llms-txt

# Preview only
ct generate agents-md --dry-run
```

---

## validate

Validate skills against platform specifications.

```bash
ct validate PATH [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PATH` | Path to skill directory or SKILL.md |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--platforms, -p` | TEXT | Comma-separated platforms to validate | anthropic,openai |
| `--fix` | FLAG | Attempt to auto-fix issues | False |
| `--verbose, -v` | FLAG | Show detailed validation output | False |

**Examples:**

```bash
# Validate against default platforms (Anthropic, OpenAI)
ct validate ./my-skill/

# Validate against specific platform
ct validate ./my-skill/ --platforms anthropic

# Auto-fix issues
ct validate ./my-skill/ --fix

# Verbose output
ct validate ./my-skill/ --verbose

# Multiple platforms
ct validate ./my-skill/ --platforms anthropic,openai,universal
```

**Validation Checks:**

- Frontmatter validity (required fields, YAML syntax)
- Description length (≤160 characters)
- Name format requirements
- Token budgets (T1 ≤2k, T2 ≤6k, T3 ≤12k)
- Platform-specific requirements
- Section structure and ordering
- Example size limits (≤30 lines)

**Exit Codes:**

- `0`: All checks passed
- `1`: Validation errors found
- `2`: File not found or invalid path

---

## analyze

Analyze skill quality, token efficiency, and security.

```bash
ct analyze PATH [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PATH` | Path to skill directory or SKILL.md |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--full-report` | FLAG | Generate comprehensive report | False |
| `--output, -o` | PATH | Output path for JSON report | None |
| `--json` | FLAG | Output as JSON | False |

**Examples:**

```bash
# Basic analysis
ct analyze ./my-skill/

# Full report
ct analyze ./my-skill/ --full-report

# Output JSON report
ct analyze ./my-skill/ --output report.json

# JSON to stdout
ct analyze ./my-skill/ --json
```

**Metrics Reported:**

- **Token Counts**: Tokens per tier (T1/T2/T3)
- **Efficiency Score**: 0-100 scale based on token budgets
- **Progressive Disclosure Score**: Quality of tier separation
- **Security Issues**: File access, network calls, shell injection
- **Cross-Platform Compatibility**: Platform-specific issues
- **Quality Gates**: Pass/fail for token budgets, section presence

**Sample Output:**

```
Skill Analysis: github-operations

Token Metrics:
  Level 1: 1,847 tokens (Target: ≤2,000) ✓
  Level 2: 5,234 tokens (Target: ≤6,000) ✓
  Level 3: 11,892 tokens (Target: ≤12,000) ✓

Efficiency Score: 92/100

Progressive Disclosure Score: 88/100
  - Clear tier separation
  - Minimal L1 footprint

Security Issues: None

Quality Gates: 8/8 passed
```

---

## optimize

Optimize skills for progressive disclosure and token efficiency.

```bash
ct optimize PATH [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PATH` | Path to skill directory or SKILL.md |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--tier, -t` | TEXT | Target tier: T1, T2, or T3 | T2 |
| `--dry-run` | FLAG | Preview changes without writing | False |
| `--in-place, -i` | FLAG | Modify file in place | False |
| `--legacy` | FLAG | Use whitespace-only optimization | False |

**Examples:**

```bash
# Preview T2 optimizations
ct optimize ./my-skill/ --tier T2 --dry-run

# Apply T1 optimizations (most aggressive)
ct optimize ./my-skill/ --tier T1 --in-place

# Apply T3 optimizations (gentle)
ct optimize ./my-skill/ --tier T3 --in-place

# Legacy whitespace-only optimization
ct optimize ./my-skill/ --legacy --in-place

# Preview and save to new file
ct optimize ./my-skill/ --tier T2 > optimized-skill.md
```

**Optimization Strategies:**

- **T1 (≤2k tokens)**: Aggressive trimming, move details to references
- **T2 (≤6k tokens)**: Balanced optimization, consolidate examples
- **T3 (≤12k tokens)**: Gentle optimization, preserve context
- **Legacy**: Whitespace removal only (no LLM)

**Techniques Applied:**

1. Remove redundant content
2. Use imperative voice (shorter)
3. Move detailed content to references
4. Consolidate similar examples
5. Restructure for progressive disclosure
6. Compress code examples

---

## introspect

Extract information from sources.

### introspect mcp

Introspect MCP server to extract tool definitions.

```bash
ct introspect mcp CONFIG [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `CONFIG` | Path to MCP config JSON |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--output, -o` | PATH | Output path for analysis JSON | None |
| `--raw` | FLAG | Output raw introspection data | False |

**Examples:**

```bash
# Introspect and display
ct introspect mcp ./github-mcp.json

# Save to file
ct introspect mcp ./github-mcp.json --output analysis.json

# Raw output
ct introspect mcp ./github-mcp.json --raw
```

**Output Fields:**

```json
{
  "server_name": "github",
  "tools": [
    {
      "name": "create_repository",
      "description": "Create a new GitHub repository",
      "input_schema": {...}
    }
  ],
  "resources": [...],
  "capabilities": [...]
}
```

### introspect openapi

Introspect OpenAPI specification.

```bash
ct introspect openapi SPEC [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPEC` | Path or URL to OpenAPI spec |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--output, -o` | PATH | Output path for analysis JSON | None |

**Examples:**

```bash
# From URL
ct introspect openapi https://api.example.com/openapi.json

# From file
ct introspect openapi ./api-spec.yaml --output analysis.json
```

---

## security-scan

Scan skills for security issues.

```bash
ct security-scan PATH [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `PATH` | Path to skill(s) to scan |

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--recursive, -r` | FLAG | Scan directories recursively | False |
| `--output, -o` | PATH | Output path for report | None |

**Examples:**

```bash
# Scan single skill
ct security-scan ./my-skill/

# Scan all skills recursively
ct security-scan ./skills/ --recursive

# Save report
ct security-scan ./skills/ --recursive --output security-report.json
```

**Security Checks:**

- **Unrestricted File Access**: File operations without path constraints
- **Network Calls**: HTTP requests without domain allowlisting
- **Shell Injection**: Unsafe command construction
- **Sensitive Data**: Hardcoded credentials, API keys, tokens
- **Path Traversal**: `../` patterns in file paths
- **Unsafe Deserialization**: Pickle, eval, exec usage

**Severity Levels:**

- **HIGH**: Critical security risk (credentials, injection)
- **MEDIUM**: Potential security issue (unrestricted access)
- **LOW**: Best practice violation (missing constraints)

**Sample Output:**

```
Security Scan Results

Skills Scanned: 12
Issues Found: 3

HIGH severity:
  - my-skill/SKILL.md:45: Hardcoded API key pattern

MEDIUM severity:
  - another-skill/SKILL.md:78: Unrestricted file write
  - another-skill/SKILL.md:92: Network call without allowlist
```

---

## analyze-repo

Analyze repository structure for agent configuration.

```bash
ct analyze-repo [OPTIONS]
```

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--repo, -r` | PATH | Path to repository | . |
| `--output, -o` | PATH | Output path for analysis JSON | None |

**Examples:**

```bash
# Analyze current directory
ct analyze-repo

# Analyze specific repo
ct analyze-repo --repo /path/to/repo

# Save analysis
ct analyze-repo --output analysis.json
```

**Analyzes:**

- Package configuration (package.json, pyproject.toml, etc.)
- Build tools (Makefile, build.gradle, etc.)
- CI/CD setup (.github/workflows, .gitlab-ci.yml, etc.)
- Testing setup (pytest.ini, jest.config.js, etc.)
- Documentation (README, docs/)
- Development scripts (scripts/, bin/)

---

## benchmark

Performance benchmarking for skill operations.

```bash
ct benchmark [OPTIONS]
```

**Options:**

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `--iterations` | INT | Number of iterations | 10 |
| `--skill` | PATH | Skill to benchmark | None |

**Examples:**

```bash
# Benchmark default operations
ct benchmark

# Benchmark specific skill
ct benchmark --skill ./my-skill/

# More iterations for accuracy
ct benchmark --iterations 100 --skill ./my-skill/
```

**Metrics:**

- Skill loading time
- Analysis time
- Validation time
- Token counting time
- Memory usage

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error (validation failed, generation failed, etc.) |
| `2` | Invalid arguments or file not found |

---

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Yes (for generate, optimize) | Anthropic API access |
| `GITHUB_TOKEN` | No | For GitHub MCP server |
| `OPENAI_API_KEY` | No | For OpenAI platform features |
| `CT_DEBUG` | No | Enable debug logging (true/false) |

---

## Output Formats

### JSON Report Format

All commands that support `--output` save JSON in this structure:

```json
{
  "command": "analyze",
  "timestamp": "2025-12-15T19:45:00-05:00",
  "path": "./my-skill/",
  "results": {
    "token_metrics": {...},
    "quality_score": 92,
    "issues": []
  }
}
```

### SKILL.md Format

Generated skills follow the Anthropic Skills format:

```yaml
---
name: skill-name
description: "Brief description ≤160 chars"
allowed-tools: Bash, Read, Write
---

# Skill Name

## When to Use This Skill
...

## Quick Reference
...
```

See: https://github.com/anthropics/skills

### AGENTS.md Format

Generated AGENTS.md follows the agents.md specification:

```markdown
# AGENTS.md

## Project Overview
...

## Dev Environment Setup
...

## Testing
...
```

See: https://agents.md/

---

## Shell Completion

Enable command completion for your shell:

```bash
# Bash
ct --install-completion bash

# Zsh
ct --install-completion zsh

# Fish
ct --install-completion fish
```

---

## Common Patterns

### Pipeline: MCP → Skill → Validate

```bash
ct introspect mcp ./mcp.json --output analysis.json && \
ct generate skill --from-analysis analysis.json && \
ct validate ./generated-skill/ && \
ct analyze ./generated-skill/ --full-report
```

### Batch Security Scan

```bash
find ./skills/ -name "SKILL.md" -exec ct security-scan {} \;
```

### Optimize All Skills

```bash
for skill in ./skills/*/; do
  ct optimize "$skill" --tier T2 --in-place
done
```

### CI/CD Validation

```bash
# In .github/workflows/validate-skills.yml
ct validate ./skills/ --platforms anthropic && \
ct security-scan ./skills/ --recursive && \
ct analyze ./skills/ --json > analysis.json
```

---

## Troubleshooting

**Command not found: ct**
- Ensure package is installed: `pip install cognitive-toolworks`
- Or install from source: `pip install -e .`

**Permission denied**
- Check file permissions: `chmod +r skill/SKILL.md`

**API rate limits**
- Anthropic API has rate limits. Add delays between bulk operations.

**Large token counts**
- Use `ct optimize` to reduce token usage
- Target T1 tier for aggressive optimization

**Validation fails but skill looks correct**
- Use `--verbose` to see detailed errors
- Try `--fix` to auto-fix common issues
- Check frontmatter YAML syntax

---

## Further Reading

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Project README**: [../README.md](../README.md)
- **Anthropic Skills**: https://github.com/anthropics/skills
- **AGENTS.md Spec**: https://agents.md/
- **MCP Specification**: https://modelcontextprotocol.io/
