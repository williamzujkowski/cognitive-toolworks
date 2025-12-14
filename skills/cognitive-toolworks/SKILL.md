---
name: cognitive-toolworks
description: "Generate cross-platform agent artifacts (SKILL.md, AGENTS.md, llms.txt) from MCP servers, APIs, or documentation. Use when creating skills, analyzing existing skills, or generating repository agent configs."
allowed-tools: Bash, Read, Write
dependencies:
  - python>=3.11
  - anthropic
  - httpx
  - pyyaml
  - jinja2
  - tiktoken
---

# Cognitive Toolworks: AI-Native Skill Forge

Generate high-quality, cross-platform agent artifacts using LLM-powered analysis.

## When to Use This Skill

- Convert MCP server to Claude/Codex Skill
- Generate AGENTS.md for a repository  
- Create skill from API documentation or OpenAPI spec
- Analyze/audit existing skills for quality and security
- Optimize skill token efficiency
- Validate skills against Anthropic/OpenAI specs

## Quick Reference

```bash
# Install
pip install cognitive-toolworks

# Generate skill from MCP server
ct generate skill --from-mcp ./mcp-config.json

# Generate AGENTS.md for current repo
ct generate agents-md --repo .

# Analyze existing skill
ct analyze ./my-skill/SKILL.md

# Validate against platforms
ct validate ./my-skill/ --platforms anthropic,openai

# Optimize token usage
ct optimize ./my-skill/ --target-tokens 5000
```

## Core Workflows

### 1. MCP Server → Skill

**Step 1: Introspect MCP server**
```bash
ct introspect mcp ./server-config.json --output analysis.json
```

The introspector:
- Connects to running MCP server
- Extracts tool definitions and schemas
- Identifies resources and capabilities
- Outputs structured analysis

**Step 2: Generate skill**
```bash
ct generate skill \
  --from-analysis analysis.json \
  --platform universal \
  --output ./generated-skill/
```

Options:
- `--platform`: `anthropic`, `openai`, or `universal` (both)
- `--examples N`: Number of examples to generate (default: 3)
- `--optimize`: Run token optimization pass

**Step 3: Validate**
```bash
ct validate ./generated-skill/ --fix
```

### 2. OpenAPI → Skill

```bash
# From URL
ct generate skill \
  --from-openapi https://api.example.com/openapi.json \
  --name "example-api" \
  --focus-endpoints /users,/projects

# From local file
ct generate skill \
  --from-openapi ./openapi.yaml \
  --output ./api-skill/
```

### 3. Repository → AGENTS.md

```bash
# Analyze repo and generate AGENTS.md
ct generate agents-md --repo . --output ./AGENTS.md

# Include llms.txt generation
ct generate agents-md --repo . --with-llms-txt

# Full analysis with skill suggestions
ct analyze-repo . --generate-all
```

This generates:
- `AGENTS.md` - Coding agent instructions
- `llms.txt` - LLM context file (optional)
- Skill opportunity report (what skills could be created)

### 4. Skill Analysis

```bash
# Basic analysis
ct analyze ./my-skill/SKILL.md

# Full report with recommendations
ct analyze ./my-skill/SKILL.md --full-report --output report.json
```

**Report includes**:
- Token count per level (metadata, body, references)
- Token efficiency score (0-1)
- Progressive disclosure score
- Coverage analysis (do instructions cover all capabilities?)
- Security scan results
- Cross-platform compatibility

### 5. Security Audit

```bash
ct security-scan ./skills/ --recursive
```

**Detects**:
- Unrestricted file system access patterns
- Network calls without allowlisting
- Shell command injection vectors
- Sensitive data exposure patterns
- Tool permission escalation risks

## Output Formats

### Anthropic SKILL.md
```yaml
---
name: skill-name
description: "Max 200 chars for Claude. Include trigger phrases."
allowed-tools: Bash, Read
dependencies:
  - package-name
---
# Skill content...
```

### OpenAI Skills (Codex CLI)
```yaml
---
name: skill-name
description: "Description for ~/.codex/skills/"
---
# Skill content...
```

### Universal Format
Generates both simultaneously with platform-specific optimizations:
- Anthropic: Strict 200-char description, progressive disclosure
- OpenAI: Flexible description, flat structure acceptable

## Token Budget Guidelines

| Level | Purpose | Budget |
|-------|---------|--------|
| Level 1 | Metadata (frontmatter) | ~100 tokens |
| Level 2 | Main SKILL.md body | <5,000 tokens |
| Level 3 | Reference files | Unbounded |

**Optimization strategies**:
- Move detailed docs to `references/` directory
- Use imperative voice (shorter)
- Avoid redundant explanations
- Link to external docs when appropriate

## Progressive Disclosure Structure

```
my-skill/
├── SKILL.md          # Levels 1-2: Always loaded
├── references/       # Level 3: Loaded on-demand
│   ├── api-docs.md
│   └── examples.md
├── scripts/          # Executable helpers
│   └── helper.py
└── assets/           # Templates, configs
    └── template.json
```

**In SKILL.md, reference Level 3 content**:
```markdown
For detailed API documentation, see [api-docs.md](references/api-docs.md).
```

## Validation Rules

### Anthropic Spec
- `name`: max 64 chars, lowercase + hyphens only
- `description`: max 200 chars, no XML tags
- Must have YAML frontmatter
- Body must be valid Markdown

### OpenAI Spec  
- `name`: max 64 chars
- `description`: max 1024 chars
- Located in `~/.codex/skills/` or `~/.agent/skills/`

### AAIF Universal
- Passes both Anthropic and OpenAI validators
- Works with Claude Code, Codex CLI, Gemini CLI

## Examples

### Example 1: GitHub MCP → Skill
```bash
# Config for GitHub MCP server
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

# Result: Universal skill for GitHub operations
```

### Example 2: FastAPI → Skill
```bash
# Generate from running FastAPI app
ct generate skill \
  --from-openapi http://localhost:8000/openapi.json \
  --name "my-api" \
  --focus-endpoints /items,/users
```

### Example 3: Bulk Repository Analysis
```bash
# Analyze multiple repos
for repo in ~/projects/*/; do
  ct analyze-repo "$repo" --output "$repo/AGENTS.md"
done
```

## Troubleshooting

### MCP introspection fails
- Verify server is running: `npx @server/name` should start
- Check JSON config matches MCP spec
- Ensure required env vars are set

### Token budget exceeded
- Run `ct optimize --aggressive`
- Move content to `references/` directory
- Split into multiple skills if >10k tokens
- Use `--analyze-only` to see breakdown

### Platform validation fails
```bash
ct validate ./skill/ --verbose
```
Common issues:
- Description too long (Anthropic: 200 chars)
- Invalid characters in name
- Missing required frontmatter fields

### Generated examples are poor quality
- Provide more context: `--context "This API is for..."`
- Increase examples: `--examples 5` then curate
- Edit manually - LLM generation is starting point

## Integration with Claude-Flow

For complex generation with multi-agent orchestration:

```bash
# Install claude-flow
npm install -g claude-flow@alpha

# Run orchestrated generation
ct generate skill \
  --from-mcp ./config.json \
  --orchestrated \
  --workflow full-pipeline
```

This uses parallel agents for:
- Semantic analysis
- Structure generation  
- Example writing
- Validation
- Optimization

## Best Practices

1. **Start with analysis**: `ct analyze` before modifying
2. **Use universal format**: Maximum portability
3. **Test both platforms**: Claude Code + Codex CLI
4. **Keep Level 2 lean**: <5k tokens for main content
5. **Security scan**: Always audit generated skills
6. **Version control**: Track skill changes in git
7. **Document triggers**: Clear description of when to use

## See Also

- [AAIF Standards](https://agentic-ai.foundation/)
- [Anthropic Skills Spec](https://github.com/anthropics/skills)
- [AGENTS.md Spec](https://agents.md/)
- [MCP Documentation](https://modelcontextprotocol.io/)
