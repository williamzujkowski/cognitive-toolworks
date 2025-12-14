# Cognitive Toolworks v2.0: Realignment Plan

## Executive Summary

**Vision**: Transform cognitive-toolworks from a static skills library into an **LLM-powered generation platform** for creating cross-platform agent artifacts (SKILL.md, AGENTS.md) aligned with the newly formed Agentic AI Foundation (AAIF) ecosystem.

**Timing**: Perfect convergence of industry events:
- Dec 9, 2025: AAIF founded (Anthropic MCP + OpenAI AGENTS.md + Block goose)
- Dec 13, 2025: OpenAI ships Skills framework mirroring Anthropic's format
- 60,000+ repos now using AGENTS.md; 10,000+ MCP servers published

**Gap Identified**: No LLM-powered tool exists for intelligent generation of skills and agent configs. Existing converters (mcp-to-skill-converter, skillz, etc.) are mechanical template-based transformers.

---

## Part 1: Strategic Positioning

### 1.1 Current State Analysis

**cognitive-toolworks (Oct 2025)**:
- "A library of small, composable Skills using Anthropic's SKILL.md format"
- Focused on progressive disclosure and minimal token usage
- Static skill library approach

**What's Changed**:
1. Skills are now "OOP for LLMs" - composable, cross-platform
2. OpenAI adopted the same format (Dec 13, 2025)
3. AAIF provides neutral governance for MCP, AGENTS.md, goose
4. Market needs intelligent generation, not just more static skills

### 1.2 New Value Proposition

```
cognitive-toolworks v2.0: The AI-Native Skill Forge

Generate → Validate → Optimize → Deploy

Cross-platform agent artifacts powered by LLM intelligence
```

**Differentiators**:
| Feature | Existing Tools | cognitive-toolworks v2.0 |
|---------|---------------|--------------------------|
| Generation Method | Template-based | LLM-powered synthesis |
| Output Formats | Single platform | Multi-platform (Anthropic + OpenAI) |
| Source Support | MCP only | MCP, OpenAPI, README, scripts, docs |
| Quality Analysis | None | Token efficiency, coverage, security |
| Examples | Manual | Auto-generated from semantic analysis |
| Progressive Disclosure | Manual structuring | Auto-optimized |
| Security | Basic | Built-in pattern detection |

### 1.3 Target Users

1. **MCP Server Authors** - Convert existing servers to Skills
2. **API Providers** - Generate Skills from OpenAPI specs
3. **Enterprise Teams** - Create internal skill libraries
4. **Open Source Projects** - Auto-generate AGENTS.md
5. **Security Teams** - Audit existing skills for vulnerabilities

---

## Part 2: Architecture Design

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    cognitive-toolworks v2.0                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Sources   │  │  Generators │  │   Outputs   │              │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤              │
│  │ • MCP Server│  │ • LLM Core  │  │ • SKILL.md  │              │
│  │ • OpenAPI   │→ │ • Analyzers │→ │ • AGENTS.md │              │
│  │ • README    │  │ • Optimizers│  │ • llms.txt  │              │
│  │ • Scripts   │  │ • Validators│  │ • Reports   │              │
│  │ • Docs      │  │             │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                          ↑                                       │
│                    ┌─────┴─────┐                                 │
│                    │ claude-flow │ (Multi-agent orchestration)   │
│                    └───────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Directory Structure

```
cognitive-toolworks/
├── SKILL.md                    # Meta-skill for the tool itself
├── AGENTS.md                   # Agent instructions for repo
├── README.md                   # Human documentation
├── pyproject.toml              # Python packaging
│
├── src/
│   └── cognitive_toolworks/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point
│       │
│       ├── sources/            # Input adapters
│       │   ├── __init__.py
│       │   ├── mcp.py          # MCP server introspection
│       │   ├── openapi.py      # OpenAPI spec parsing
│       │   ├── readme.py       # README extraction
│       │   ├── scripts.py      # Script analysis
│       │   └── docs.py         # Documentation parsing
│       │
│       ├── generators/         # LLM-powered generators
│       │   ├── __init__.py
│       │   ├── skill.py        # SKILL.md generation
│       │   ├── agents.py       # AGENTS.md generation
│       │   ├── llms_txt.py     # llms.txt generation
│       │   └── examples.py     # Example generation
│       │
│       ├── analyzers/          # Quality analysis
│       │   ├── __init__.py
│       │   ├── tokens.py       # Token efficiency
│       │   ├── coverage.py     # Instruction coverage
│       │   ├── security.py     # Security pattern detection
│       │   └── compatibility.py # Cross-platform checks
│       │
│       ├── optimizers/         # Optimization passes
│       │   ├── __init__.py
│       │   ├── progressive.py  # Progressive disclosure opt
│       │   ├── dedup.py        # Content deduplication
│       │   └── structure.py    # Structure optimization
│       │
│       ├── validators/         # Validation
│       │   ├── __init__.py
│       │   ├── anthropic.py    # Anthropic spec compliance
│       │   ├── openai.py       # OpenAI format compliance
│       │   └── aaif.py         # AAIF standards
│       │
│       ├── templates/          # Output templates
│       │   ├── skill_anthropic.md.j2
│       │   ├── skill_openai.md.j2
│       │   ├── agents.md.j2
│       │   └── llms_txt.j2
│       │
│       └── llm/                # LLM integration
│           ├── __init__.py
│           ├── client.py       # Multi-provider client
│           ├── prompts.py      # Prompt templates
│           └── chains.py       # LangChain/claude-flow integration
│
├── skills/                     # Built-in skills library
│   ├── skill-forge/           # Generate new skills
│   ├── agents-gen/            # Generate AGENTS.md
│   ├── mcp-analyzer/          # Analyze MCP servers
│   ├── skill-auditor/         # Security audit skills
│   └── token-optimizer/       # Optimize token usage
│
├── scripts/                    # Utility scripts
│   ├── validate-skill.py
│   ├── token-counter.py
│   └── security-scan.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/
│   ├── getting-started.md
│   ├── architecture.md
│   ├── api-reference.md
│   └── examples/
│
└── .claude-flow/               # Claude-flow orchestration
    ├── workflows/
    │   ├── generate-skill.yaml
    │   ├── analyze-repo.yaml
    │   └── full-pipeline.yaml
    └── agents/
        ├── analyzer.yaml
        ├── generator.yaml
        └── validator.yaml
```

### 2.3 Core Data Models

```python
# src/cognitive_toolworks/models.py

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class Platform(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    UNIVERSAL = "universal"  # Compatible with both

class SourceType(Enum):
    MCP_SERVER = "mcp"
    OPENAPI = "openapi"
    README = "readme"
    SCRIPT = "script"
    DOCUMENTATION = "docs"

@dataclass
class SkillMetadata:
    """YAML frontmatter for SKILL.md"""
    name: str                           # max 64 chars
    description: str                    # max 200 chars for Anthropic, 1024 for internal
    category: Optional[str] = None
    allowed_tools: Optional[list[str]] = None
    dependencies: Optional[list[str]] = None
    version: str = "1.0.0"

@dataclass
class SkillContent:
    """Full skill content structure"""
    metadata: SkillMetadata
    overview: str
    when_to_use: list[str]
    instructions: str
    examples: list[dict]
    guidelines: list[str]
    references: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)

@dataclass
class AgentsConfig:
    """AGENTS.md structure"""
    dev_environment: dict
    testing_instructions: dict
    pr_instructions: dict
    coding_conventions: dict
    project_specific: dict

@dataclass
class AnalysisReport:
    """Quality analysis output"""
    token_count: int
    token_efficiency: float  # 0-1 score
    coverage_score: float    # 0-1 score
    security_issues: list[str]
    compatibility: dict[Platform, bool]
    recommendations: list[str]
```

---

## Part 3: Core Workflows

### 3.1 MCP → Skill Generation

```python
# Pseudocode for the core generation flow

async def generate_skill_from_mcp(
    mcp_config: Path,
    llm: LLMClient,
    platform: Platform = Platform.UNIVERSAL
) -> SkillContent:
    """
    1. Introspect MCP server to extract tool definitions
    2. Use LLM to understand tool semantics and relationships
    3. Generate progressive disclosure structure
    4. Create examples from tool combinations
    5. Validate against platform spec
    """

    # Step 1: Extract MCP tool definitions
    tools = await mcp_introspector.get_tools(mcp_config)
    resources = await mcp_introspector.get_resources(mcp_config)

    # Step 2: LLM semantic analysis
    analysis = await llm.analyze(
        prompt=SEMANTIC_ANALYSIS_PROMPT,
        tools=tools,
        resources=resources
    )

    # Step 3: Generate structure with progressive disclosure
    structure = await llm.generate(
        prompt=STRUCTURE_GENERATION_PROMPT,
        analysis=analysis,
        constraints={
            "level1_tokens": 100,      # Metadata only
            "level2_tokens": 5000,     # Main SKILL.md
            "level3_tokens": "unbounded"  # Reference files
        }
    )

    # Step 4: Generate examples
    examples = await llm.generate(
        prompt=EXAMPLE_GENERATION_PROMPT,
        tools=tools,
        analysis=analysis,
        count=3
    )

    # Step 5: Validate
    skill = assemble_skill(structure, examples)
    await validator.validate(skill, platform)

    return skill
```

### 3.2 Repository → AGENTS.md Generation

```python
async def generate_agents_md(
    repo_path: Path,
    llm: LLMClient
) -> AgentsConfig:
    """
    Analyze repository and generate AGENTS.md
    """

    # Gather context
    readme = read_file(repo_path / "README.md")
    package_json = read_file(repo_path / "package.json")
    pyproject = read_file(repo_path / "pyproject.toml")
    ci_config = find_ci_config(repo_path)
    existing_claude_md = read_file(repo_path / "CLAUDE.md")

    # LLM analysis and generation
    agents_md = await llm.generate(
        prompt=AGENTS_MD_PROMPT,
        context={
            "readme": readme,
            "package_manager": detect_package_manager(repo_path),
            "test_framework": detect_test_framework(repo_path),
            "ci_config": ci_config,
            "existing_guidance": existing_claude_md
        }
    )

    return agents_md
```

### 3.3 Claude-Flow Orchestration

```yaml
# .claude-flow/workflows/generate-skill.yaml
name: skill-generation-workflow
description: Multi-agent skill generation pipeline

agents:
  - name: analyzer
    role: Introspect source and extract semantics
    model: claude-sonnet-4-20250514

  - name: generator  
    role: Generate skill content with progressive disclosure
    model: claude-sonnet-4-20250514

  - name: example-writer
    role: Create realistic usage examples
    model: claude-haiku-4-20250514

  - name: validator
    role: Validate against platform specs
    model: claude-haiku-4-20250514

  - name: optimizer
    role: Optimize token usage and structure
    model: claude-sonnet-4-20250514

workflow:
  - step: analyze
    agent: analyzer
    input: $source_config
    output: semantic_analysis

  - step: generate
    agent: generator
    input: $semantic_analysis
    output: raw_skill

  - step: examples
    agent: example-writer
    input:
      - $semantic_analysis
      - $raw_skill
    output: examples
    parallel: true

  - step: validate
    agent: validator
    input:
      - $raw_skill
      - $examples
    output: validation_report

  - step: optimize
    agent: optimizer
    input:
      - $raw_skill
      - $validation_report
    output: final_skill
    condition: validation_report.passed == true
```

---

## Part 4: The Meta-Skill (cognitive-toolworks itself as a Skill)

This is the SKILL.md that allows Claude to automatically use cognitive-toolworks:

```markdown
---
name: cognitive-toolworks
description: >
  Generate cross-platform agent artifacts (SKILL.md, AGENTS.md) from
  various sources using LLM intelligence. Use when users want to create
  skills from MCP servers, APIs, documentation, or analyze existing skills.
allowed-tools: Bash, Read, Write
dependencies:
  - python>=3.11
  - anthropic
  - httpx
  - pyyaml
  - jinja2
---

# Cognitive Toolworks: AI-Native Skill Forge

## Overview

Cognitive Toolworks generates high-quality, cross-platform agent artifacts
(SKILL.md for Claude/Codex, AGENTS.md for coding agents) from various
sources using LLM-powered analysis and generation.

## When to Use This Skill

- User wants to convert an MCP server to a Claude Skill
- User wants to generate AGENTS.md for a repository
- User wants to create a skill from API documentation
- User wants to analyze/audit existing skills for quality
- User wants to optimize skill token efficiency
- User mentions "cross-platform" skills or "universal" agent config

## Quick Reference

### Generate Skill from MCP Server
```bash
ct generate skill --from-mcp ./mcp-config.json --output ./my-skill/
```

### Generate AGENTS.md for Repository
```bash
ct generate agents-md --repo . --output ./AGENTS.md
```

### Analyze Existing Skill
```bash
ct analyze ./my-skill/SKILL.md --full-report
```

### Validate Against Platforms
```bash
ct validate ./my-skill/ --platforms anthropic,openai
```

## Detailed Workflows

### Workflow 1: MCP Server → Skill

1. **Introspect MCP Server**
   ```bash
   ct introspect mcp ./server-config.json --output analysis.json
   ```

2. **Generate Skill**
   ```bash
   ct generate skill \
     --from-analysis analysis.json \
     --platform universal \
     --examples 3 \
     --output ./generated-skill/
   ```

3. **Validate and Optimize**
   ```bash
   ct validate ./generated-skill/ --fix
   ct optimize ./generated-skill/ --target-tokens 5000
   ```

### Workflow 2: OpenAPI → Skill

1. **Parse OpenAPI Spec**
   ```bash
   ct introspect openapi https://api.example.com/openapi.json \
     --focus-endpoints /users,/projects
   ```

2. **Generate Skill**
   ```bash
   ct generate skill \
     --from-openapi openapi.json \
     --name "example-api" \
     --output ./api-skill/
   ```

### Workflow 3: Repository Analysis

1. **Full Analysis**
   ```bash
   ct analyze-repo . --generate-all
   ```

   This generates:
   - `AGENTS.md` - Coding agent instructions
   - `llms.txt` - LLM context file
   - `.claude/skills/` - Auto-detected skill opportunities

## Output Formats

### Anthropic SKILL.md
```yaml
---
name: skill-name
description: Description (max 200 chars for Claude)
---
```

### OpenAI Skills (Codex CLI)
```yaml
---
name: skill-name  
description: Description
# Stored in ~/.codex/skills/
---
```

### Universal Format
Generates both formats simultaneously with platform-specific optimizations.

## Quality Metrics

When analyzing skills, cognitive-toolworks reports:

- **Token Efficiency**: Ratio of useful content to total tokens
- **Progressive Disclosure Score**: How well content is layered
- **Coverage Score**: Instruction completeness
- **Security Score**: Detection of dangerous patterns
- **Cross-Platform Compatibility**: Works on Anthropic + OpenAI

## Security Patterns Detected

- Unrestricted file system access
- Network calls without allowlisting
- Shell command injection vectors
- Sensitive data exposure patterns
- Tool permission escalation

## Best Practices

1. **Keep Level 1 (metadata) under 100 tokens**
2. **Keep Level 2 (SKILL.md body) under 5,000 tokens**
3. **Use Level 3 (references/) for detailed docs**
4. **Include 2-3 concrete examples**
5. **Specify `allowed-tools` to scope permissions**
6. **Test with both Claude and Codex CLI**

## Troubleshooting

### MCP introspection fails
- Ensure MCP server is running: `npx @mcp/server-name`
- Check config format matches MCP spec

### Token budget exceeded
- Run `ct optimize --aggressive`
- Split into multiple skills if >10k tokens

### Platform validation fails
- Check `ct validate --verbose` for specific issues
- Common: description too long, invalid characters in name
```

---

## Part 5: Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal**: Core infrastructure and MCP→Skill generation

- [ ] Project scaffolding with modern Python (pyproject.toml, ruff, mypy)
- [ ] MCP server introspection module
- [ ] Basic LLM client (Anthropic SDK)
- [ ] SKILL.md template and generator
- [ ] CLI foundation with Typer
- [ ] Unit tests for core modules

**Deliverable**: `ct generate skill --from-mcp` working

### Phase 2: Multi-Source Support (Week 3-4)

**Goal**: Expand input sources

- [ ] OpenAPI spec parser
- [ ] README/documentation extractor
- [ ] Script analyzer (Python, TypeScript, Bash)
- [ ] AGENTS.md generator
- [ ] llms.txt generator

**Deliverable**: Generate from any common source

### Phase 3: Analysis & Optimization (Week 5-6)

**Goal**: Quality tooling

- [ ] Token counter and efficiency analyzer
- [ ] Coverage analyzer
- [ ] Security pattern scanner
- [ ] Cross-platform validator (Anthropic + OpenAI specs)
- [ ] Auto-optimizer with suggestions

**Deliverable**: `ct analyze` and `ct optimize` commands

### Phase 4: Claude-Flow Integration (Week 7-8)

**Goal**: Multi-agent orchestration

- [ ] Claude-flow workflow definitions
- [ ] Agent role definitions (analyzer, generator, validator)
- [ ] Parallel example generation
- [ ] Memory integration for iterative improvement
- [ ] Batch processing for skill libraries

**Deliverable**: `ct generate --orchestrated` with claude-flow

### Phase 5: Polish & Launch (Week 9-10)

**Goal**: Production ready

- [ ] Meta-skill (cognitive-toolworks SKILL.md)
- [ ] Documentation site
- [ ] PyPI package
- [ ] GitHub Actions for CI/CD
- [ ] Example skill library
- [ ] Blog post / announcement

**Deliverable**: Public v2.0 release

---

## Part 6: Claude-Flow Integration Details

### 6.1 Agent Definitions

```yaml
# .claude-flow/agents/analyzer.yaml
name: skill-analyzer
type: specialist
color: "#4A90D9"
description: Analyzes source materials to extract semantic meaning and tool relationships

capabilities:
  - MCP server introspection
  - OpenAPI schema parsing
  - Documentation comprehension
  - Relationship mapping

system_prompt: |
  You are an expert at analyzing technical artifacts to understand their
  purpose, capabilities, and usage patterns. Your goal is to extract
  structured semantic information that can be used to generate high-quality
  agent skills.

  When analyzing MCP servers, identify:
  - Core tools and their purposes
  - Tool input/output schemas
  - Common tool combinations (workflows)
  - Error handling patterns
  - Security considerations

  Output your analysis as structured JSON.

priority: high
```

```yaml
# .claude-flow/agents/generator.yaml
name: skill-generator
type: specialist
color: "#50C878"
description: Generates SKILL.md content with optimal progressive disclosure

capabilities:
  - Progressive disclosure optimization
  - Cross-platform format adaptation
  - Example synthesis
  - Instruction writing

system_prompt: |
  You are an expert at writing Claude Skills following Anthropic's
  progressive disclosure architecture. Your goal is to generate skills
  that are:

  1. Token-efficient (Level 1: ~100 tokens, Level 2: <5000 tokens)
  2. Action-oriented (imperative instructions)
  3. Example-rich (2-3 concrete examples)
  4. Well-structured (clear workflow sections)

  Follow the SKILL.md spec exactly. Never exceed description limits.
  Prefer concise, direct language over verbose explanations.

priority: high
```

### 6.2 Workflow Orchestration

```yaml
# .claude-flow/workflows/full-pipeline.yaml
name: full-skill-generation
description: Complete skill generation with analysis, generation, validation, and optimization

config:
  max_iterations: 3
  parallel_agents: 4
  memory_enabled: true

stages:
  - name: intake
    description: Parse and validate input source
    agent: analyzer
    timeout: 60s

  - name: semantic-analysis
    description: Deep analysis of tool semantics
    agent: analyzer
    depends_on: [intake]
    timeout: 120s

  - name: structure-generation
    description: Generate skill structure
    agent: generator
    depends_on: [semantic-analysis]
    timeout: 180s

  - name: example-generation
    description: Generate usage examples
    agent: example-writer
    depends_on: [semantic-analysis]
    parallel: true
    count: 3
    timeout: 60s

  - name: assembly
    description: Assemble skill from components
    agent: generator
    depends_on: [structure-generation, example-generation]
    timeout: 60s

  - name: validation
    description: Validate against platform specs
    agent: validator
    depends_on: [assembly]
    timeout: 30s

  - name: optimization
    description: Optimize token usage
    agent: optimizer
    depends_on: [validation]
    condition: "validation.issues.length > 0"
    timeout: 120s

  - name: final-validation
    description: Final compliance check
    agent: validator
    depends_on: [optimization]
    timeout: 30s

outputs:
  - skill_directory: generated skill folder
  - analysis_report: JSON analysis
  - validation_report: compliance status
```

---

## Part 7: Key Prompts Library

### 7.1 Semantic Analysis Prompt

```markdown
# MCP Server Semantic Analysis

You are analyzing an MCP server to understand its capabilities for skill generation.

## Input
MCP Server Tools:
{tools_json}

MCP Server Resources:
{resources_json}

## Task
Analyze these tools and provide structured semantic understanding:

1. **Purpose Summary** (1-2 sentences): What is this server's primary purpose?

2. **Tool Categories**: Group tools by function (e.g., CRUD operations, search, configuration)

3. **Tool Relationships**: Identify which tools are commonly used together
   - Workflows (sequential): tool_a -> tool_b -> tool_c
   - Parallel operations: tool_a + tool_b (independent)
   - Conditional: if tool_a returns X, use tool_b

4. **Input/Output Patterns**: Common data types and schemas

5. **Error Scenarios**: What can go wrong and how to handle it

6. **Security Considerations**: Any sensitive operations or data

7. **Recommended Use Cases**: When would someone use this server?

Output as JSON matching this schema:
{schema}
```

### 7.2 Skill Generation Prompt

```markdown
# SKILL.md Generation

Generate a Claude Skill following Anthropic's progressive disclosure architecture.

## Input
Semantic Analysis:
{analysis_json}

Target Platform: {platform}
Token Budget: Level 1: 100, Level 2: {level2_budget}

## Requirements

1. **Frontmatter** (YAML):
   - name: lowercase, hyphens, max 64 chars
   - description: max 200 chars, include trigger phrases

2. **Structure**:
   - Overview (2-3 sentences)
   - When to Use (bullet list of triggers)
   - Quick Reference (most common commands)
   - Detailed Workflows (step-by-step)
   - Examples (2-3 real scenarios)
   - Troubleshooting (common issues)

3. **Style**:
   - Imperative voice ("Run this command", not "You can run")
   - Concise (no filler words)
   - Action-oriented
   - Include code blocks for commands

4. **Progressive Disclosure**:
   - Keep main SKILL.md under {level2_budget} tokens
   - Reference external files for detailed docs: `See [reference.md](reference.md)`

Generate the complete SKILL.md content:
```

---

## Part 8: Success Metrics

### 8.1 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token Efficiency | >0.85 | useful_tokens / total_tokens |
| Platform Compatibility | 100% | passes both Anthropic + OpenAI validators |
| Example Quality | >4.0/5 | human evaluation of generated examples |
| Coverage Score | >0.90 | instructions cover all tool capabilities |
| Security Score | >0.95 | no dangerous patterns detected |

### 8.2 Usage Metrics

| Metric | Target (6 months) |
|--------|-------------------|
| PyPI Downloads | 1,000+ |
| GitHub Stars | 100+ |
| Skills Generated | 500+ |
| AGENTS.md Generated | 200+ |
| Community Contributions | 10+ PRs |

### 8.3 Ecosystem Integration

| Integration | Status |
|-------------|--------|
| Claude Code marketplace | Skill submitted |
| awesome-claude-skills | Listed |
| awesome-llm-skills | Listed |
| AAIF mention | Blog post citing |

---

## Part 9: Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Spec changes (Anthropic/OpenAI) | High | Abstract platform differences; watch changelogs |
| LLM output inconsistency | Medium | Structured outputs; validation loops; retries |
| Token costs for generation | Medium | Caching; smaller models for simple tasks |
| Security vulnerabilities in generated skills | High | Mandatory security scan; sandboxed testing |
| Low adoption | Medium | Strong docs; example library; blog posts |

---

## Part 10: Immediate Next Steps

### For This Session

1. ✅ Research completed
2. ✅ Architecture designed
3. ⬜ Create project scaffold
4. ⬜ Generate meta-skill SKILL.md
5. ⬜ Create claude-flow workflow files

### For Week 1

1. Initialize repository with modern Python tooling
2. Implement MCP introspection
3. Basic LLM client with Anthropic SDK
4. First working `ct generate skill --from-mcp`
5. Unit tests for core modules

---

## Appendix A: Reference Materials

### AAIF Ecosystem
- MCP Spec: https://modelcontextprotocol.io/
- AGENTS.md: https://agents.md/
- Anthropic Skills: https://github.com/anthropics/skills
- OpenAI Skills (Codex): https://developers.openai.com/codex/guides/

### Existing Tools (to learn from/differentiate)
- mcp-to-skill-converter: https://github.com/GBSOSS/-mcp-to-skill-converter
- skillz: https://github.com/intellectronica/skillz
- skills-mcp: https://github.com/skills-mcp/skills-mcp
- openskills: https://github.com/numman-ali/openskills
- skill-builder: https://github.com/metaskills/skill-builder

### Claude-Flow
- Repository: https://github.com/ruvnet/claude-flow
- Documentation: https://github.com/ruvnet/claude-flow/wiki

---

## Appendix B: Competitive Landscape

| Tool | Approach | Limitations |
|------|----------|-------------|
| mcp-to-skill-converter | Template-based MCP→Skill | No semantic understanding |
| skillz | Skill→MCP shim | Doesn't generate skills |
| skill-builder | Interactive Claude skill | Manual, single-skill |
| openskills | Universal loader | Doesn't generate |
| **cognitive-toolworks v2** | **LLM-powered generation** | **None of above limitations** |

---

*Document Version: 1.0*
*Created: December 14, 2025*
*Author: Claude (with William Zujkowski)*
