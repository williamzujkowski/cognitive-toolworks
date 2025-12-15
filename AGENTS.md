# AGENTS.md - Cognitive Toolworks

> Agent instructions for AI coding assistants working on this repository.

## Project Overview

Cognitive Toolworks is an LLM-powered platform for generating cross-platform agent artifacts (SKILL.md, AGENTS.md, llms.txt). It transforms MCP servers and repositories into skills compatible with Claude, Codex, and other agents.

> **Status**: MCP generation stable. OpenAPI/README sources planned but not yet implemented.

## Dev Environment

### Setup
```bash
# Clone and setup
git clone https://github.com/williamzujkowski/cognitive-toolworks.git
cd cognitive-toolworks

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Verify installation
ct --version
```

### Key Directories
- `src/cognitive_toolworks/` - Main source code
- `src/cognitive_toolworks/sources/` - Input adapters (MCP, OpenAPI, etc.)
- `src/cognitive_toolworks/generators/` - LLM-powered generators
- `src/cognitive_toolworks/analyzers/` - Quality analysis tools
- `src/cognitive_toolworks/validators/` - Platform spec validators
- `skills/` - Built-in skill library
- `tests/` - Test suite
- `.claude-flow/` - Multi-agent orchestration configs

### Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...     # Required for LLM generation
```

## Testing Instructions

### Run All Tests
```bash
# Full test suite
pytest

# With coverage
pytest --cov=cognitive_toolworks --cov-report=html

# Specific test file
pytest tests/unit/test_generators.py

# Specific test
pytest -k "test_skill_generation"
```

### Test Categories
```bash
# Unit tests only (fast)
pytest tests/unit/

# Integration tests (requires API keys)
pytest tests/integration/ --run-integration

# Validation tests
pytest tests/validators/
```

### Pre-commit Checks
```bash
# Run all checks
pre-commit run --all-files

# Individual checks
ruff check .
ruff format .
mypy src/
```

### Test Fixtures
- `tests/fixtures/mcp/` - Sample MCP server configs
- `tests/fixtures/openapi/` - Sample OpenAPI specs
- `tests/fixtures/skills/` - Reference skills for validation

## PR Instructions

### Title Format
`[component] Brief description`

Components: `sources`, `generators`, `analyzers`, `validators`, `cli`, `docs`, `tests`, `ci`

Examples:
- `[generators] Add OpenAPI to skill generation`
- `[validators] Fix Anthropic description length check`
- `[docs] Update API reference`

### Required Checks
All PRs must pass:
1. `pytest` - All tests pass
2. `ruff check` - No linting errors
3. `ruff format --check` - Code formatted
4. `mypy` - Type checking passes
5. Coverage >= 80% for new code

### PR Description Template
```markdown
## Summary
Brief description of changes

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Tests

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Type hints added
- [ ] CHANGELOG updated (if user-facing)
```

## Coding Conventions

### Python Style
- Python 3.11+ features allowed
- Type hints required for all public functions
- Docstrings in Google style
- Max line length: 100 chars
- Use `ruff` for formatting and linting

### File Organization
```python
# Standard library imports
import json
from pathlib import Path

# Third-party imports
import httpx
from anthropic import Anthropic

# Local imports
from cognitive_toolworks.models import SkillContent
from cognitive_toolworks.llm import LLMClient
```

### Error Handling
```python
# Use custom exceptions
from cognitive_toolworks.exceptions import (
    MCPIntrospectionError,
    ValidationError,
    TokenBudgetExceededError,
)

# Provide helpful error messages
raise ValidationError(
    f"Description exceeds Anthropic limit: {len(desc)} > 200 chars"
)
```

### Async Patterns
```python
# Use async for I/O operations
async def introspect_mcp(config: Path) -> MCPAnalysis:
    async with httpx.AsyncClient() as client:
        # ...

# Sync wrappers for CLI
def introspect_mcp_sync(config: Path) -> MCPAnalysis:
    return asyncio.run(introspect_mcp(config))
```

## Project-Specific Notes

### Adding New Source Types
1. Create adapter in `src/cognitive_toolworks/sources/`
2. Implement `SourceAdapter` protocol
3. Register in `sources/__init__.py`
4. Add tests in `tests/unit/test_sources.py`
5. Update CLI in `cli.py`

### Adding New Validators
1. Create validator in `src/cognitive_toolworks/validators/`
2. Implement `Validator` protocol  
3. Add to validation chain
4. Include test fixtures for edge cases

### LLM Prompt Changes
- Prompts live in `src/cognitive_toolworks/llm/prompts.py`
- Test with multiple inputs before committing
- Document expected outputs in docstrings
- Consider token costs

### Token Counting
```python
# Use tiktoken for accurate counts
from cognitive_toolworks.analyzers.tokens import count_tokens

tokens = count_tokens(content, model="claude-3-sonnet")
```

## Useful Commands

```bash
# Development
ct generate skill --from-mcp ./test.json --dry-run  # Preview without writing
ct analyze ./skill/ --json                           # Machine-readable output
ct validate ./skill/ --verbose                       # Detailed validation

# Debugging
CT_DEBUG=1 ct generate skill ...                     # Enable debug logging
ct introspect mcp ./config.json --raw               # Raw introspection output

# Benchmarking
ct benchmark ./skills/ --iterations 10              # Performance testing
```

## Architecture Notes

### Generation Pipeline
```
Source → Introspector → Analyzer → Generator → Validator → Optimizer → Output
           ↓              ↓           ↓           ↓            ↓
        MCPAnalysis   SemanticMap  RawSkill  ValidationReport  FinalSkill
```

### LLM Usage
- Anthropic Claude for generation (sonnet-4 default)
- Structured outputs via JSON mode
- Retry logic for transient failures
- Caching for repeated introspections

### Claude-Flow Integration
- Workflows in `.claude-flow/workflows/`
- Agent definitions in `.claude-flow/agents/`
- Use `--orchestrated` flag to enable multi-agent mode
