# Codex CLI Command Reference

## Installation

```bash
# Via npm
npm i -g @openai/codex

# Via Homebrew (macOS)
brew install --cask codex

# Upgrade existing installation
codex --upgrade
```

## Authentication

```bash
# First run - prompts for authentication
codex

# Sign in with ChatGPT account (recommended)
# Follow browser prompt to authenticate

# Alternative: Set API key in config
# Edit ~/.codex/config.toml:
# [auth]
# api_key = "sk-proj-YOUR_KEY_HERE"
```

## Interactive Mode (Default)

```bash
# Start interactive session in current directory
codex

# Start with initial prompt
codex "create a todo app using React"

# Specify working directory
codex --workdir /path/to/project

# Use specific model
codex --model gpt-5-codex

# Pass screenshot or diagram as input
codex --image diagram.png "implement this architecture"
```

### Interactive Commands (within Codex session)

```
/model <model-name>     # Switch model (e.g., gpt-5-codex)
/help                   # Show available commands
/reset                  # Reset conversation
/undo                   # Undo last change
/exit                   # Exit Codex session
```

## Non-Interactive Mode (Exec)

```bash
# Execute single prompt and exit
codex exec --prompt "create REST API with Express.js"

# With file context
codex exec --file src/models.py --prompt "generate migration script"

# Multiple file context
codex exec --file api.ts --file types.ts --prompt "add error handling"

# Redirect output to file
codex exec --prompt "generate Dockerfile for Node.js app" > Dockerfile

# Pipe input from another command
cat requirements.txt | codex exec --prompt "create setup.py from these dependencies"
```

## Common Usage Patterns

### 1. Generate New Project Scaffold

```bash
# Interactive
codex "create a Python CLI tool with Click, including setup.py, README, and tests"

# Non-interactive
codex exec --prompt "scaffold a FastAPI project with PostgreSQL, Docker, and pytest"
```

### 2. Generate Tests from Existing Code

```bash
# Interactive (with file context)
codex --file src/calculator.py "generate comprehensive pytest tests"

# Non-interactive
codex exec --file api/routes.py --prompt "create integration tests with pytest and httpx"
```

### 3. Add Feature to Existing Codebase

```bash
# Interactive (Codex reads directory)
codex "add authentication middleware to this Express app"

# Non-interactive with context
codex exec --file server.js --prompt "add rate limiting middleware"
```

### 4. Convert or Translate Code

```bash
# Interactive
codex "convert this JavaScript code to TypeScript with full type definitions"

# Non-interactive
codex exec --file script.js --prompt "rewrite in Python 3.12"
```

### 5. Generate Configuration Files

```bash
# Non-interactive
codex exec --prompt "create GitHub Actions CI/CD for Python project with pytest and coverage"

codex exec --prompt "generate docker-compose.yml for React frontend, Node backend, PostgreSQL"
```

### 6. Create Data Models and Schemas

```bash
# Interactive
codex "create SQLAlchemy models for e-commerce: User, Product, Order, OrderItem"

# Non-interactive
codex exec --prompt "generate Pydantic schemas for user registration and authentication"
```

### 7. Generate API Endpoints

```bash
# Interactive
codex "create CRUD endpoints for blog posts using FastAPI and SQLAlchemy"

# Non-interactive
codex exec --file models.py --prompt "generate REST API routes for these models"
```

## Advanced Options

```bash
# Specify token limit
codex --max-tokens 8192 "generate comprehensive API documentation"

# Set temperature (0.0-1.0, lower = more deterministic)
codex --temperature 0.1 "generate production-ready error handling"

# Enable verbose output
codex --verbose "debug why this async function fails"

# Dry run (show what would be done without executing)
codex --dry-run "refactor this class hierarchy"

# Output JSON for programmatic use
codex exec --format json --prompt "analyze this codebase structure"
```

## GitHub Action Integration

```yaml
# .github/workflows/codex-generate.yml
name: Generate with Codex
on: [workflow_dispatch]

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: openai/codex-action@v1
        with:
          api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt: "generate API documentation from code comments"
```

## TypeScript SDK Usage

```typescript
import { Codex } from '@openai/codex';

const codex = new Codex({
  apiKey: process.env.OPENAI_API_KEY,
  model: 'gpt-5-codex'
});

// Generate code
const result = await codex.generate({
  prompt: 'create REST API for user management',
  workdir: '/path/to/project',
  files: ['src/models.ts']
});

console.log(result.generatedFiles);
```

## Best Practices

### 1. Be Specific in Prompts

```bash
# Less effective
codex "make an API"

# More effective
codex "create a REST API using FastAPI with endpoints for user CRUD operations, PostgreSQL database, Pydantic schemas, and JWT authentication"
```

### 2. Provide Context with Files

```bash
# Good: Give Codex context
codex --file src/models.py --file src/database.py "add user authentication"

# Better: Be specific about what to add
codex --file src/models.py "add User model with email, hashed_password, created_at fields using SQLAlchemy"
```

### 3. Use Non-Interactive for Automation

```bash
# In scripts or CI/CD
codex exec --prompt "generate OpenAPI schema from FastAPI app" > openapi.json

# Chain with other tools
codex exec --prompt "create requirements.txt" | sort | uniq > requirements.txt
```

### 4. Review Generated Code

```bash
# Generate to temporary location first
codex exec --prompt "create Kubernetes manifests" > k8s-manifests.yaml

# Review before applying
cat k8s-manifests.yaml
# Then: kubectl apply -f k8s-manifests.yaml
```

### 5. Iterate in Interactive Mode

```bash
# Start interactive session
codex "create a CLI tool for file management"

# Within session, refine iteratively:
# > "add progress bar for large files"
# > "add --verbose flag for detailed output"
# > "create comprehensive help text"
```

## Troubleshooting

```bash
# Check Codex version
codex --version

# Check authentication status
codex --check-auth

# View logs
tail -f ~/.codex/codex.log

# Reset configuration
rm ~/.codex/config.toml
codex  # Will prompt to reconfigure

# Clear cache
rm -rf ~/.codex/cache/
```

## Configuration Locations

- **Config:** `~/.codex/config.toml`
- **Logs:** `~/.codex/codex.log`
- **Cache:** `~/.codex/cache/`
- **Session history:** `~/.codex/history/`

## Model Selection Guide

| Model | Use Case | Strengths |
|-------|----------|-----------|
| gpt-5-codex | Code generation (default for Codex) | Fast, optimized for coding tasks |
| gpt-5 | Complex reasoning | Better for architecture, analysis |
| gpt-4-turbo | Legacy support | Stable, well-tested |

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Authentication error
- `3` - Network error
- `4` - Invalid command or prompt
- `5` - File operation error
