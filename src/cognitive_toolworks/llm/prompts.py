"""
Prompt templates for LLM-powered generation.

Contains prompts for:
- Semantic analysis
- Skill generation
- Example synthesis
- Optimization
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PromptTemplate:
    """A prompt template with placeholders."""

    name: str
    template: str
    description: str = ""

    def format(self, **kwargs: Any) -> str:
        """Format the template with provided values."""
        return self.template.format(**kwargs)


# --- Semantic Analysis Prompts ---

SEMANTIC_ANALYSIS_SYSTEM = """You are an expert at analyzing technical artifacts to understand their
purpose, capabilities, and usage patterns. Your goal is to extract structured semantic information
that can be used to generate high-quality agent skills.

Always output valid JSON matching the requested schema."""

SEMANTIC_ANALYSIS_PROMPT = """# MCP Server Semantic Analysis

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

Output as JSON:
```json
{{
  "purpose": "string",
  "tool_categories": {{"category_name": ["tool1", "tool2"]}},
  "workflows": [
    {{"name": "string", "steps": ["tool1", "tool2"], "description": "string"}}
  ],
  "error_scenarios": ["string"],
  "security_considerations": ["string"],
  "recommended_use_cases": ["string"]
}}
```"""

# --- Skill Generation Prompts ---

SKILL_GENERATION_SYSTEM = """You are an expert at writing Claude Skills following Anthropic's
progressive disclosure architecture. Your goal is to generate skills that are:

1. Token-efficient (Level 1: ~100 tokens, Level 2: <5000 tokens)
2. Action-oriented (imperative instructions)
3. Example-rich (2-3 concrete examples)
4. Well-structured (clear workflow sections)

Follow the SKILL.md spec exactly. Never exceed description limits.
Prefer concise, direct language over verbose explanations.

Always output valid markdown."""

SKILL_GENERATION_PROMPT = """# SKILL.md Generation

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

Generate the complete SKILL.md content:"""

# --- Example Generation Prompts ---

EXAMPLE_GENERATION_SYSTEM = """You are an expert at creating realistic, educational examples
for agent skills. Your examples should be:

1. Practical and commonly needed
2. Complete with all required inputs
3. Show expected outputs
4. Demonstrate key features"""

EXAMPLE_GENERATION_PROMPT = """# Example Generation

Generate {count} realistic examples for the following skill:

## Skill Overview
{skill_overview}

## Available Tools
{tools_json}

## Workflows
{workflows_json}

## Requirements
- Each example should be a complete, runnable scenario
- Include user intent, commands, and expected output
- Cover different use cases (simple, intermediate, edge case)
- Keep each example under 20 lines

Generate examples as JSON:
```json
[
  {{
    "title": "Example Title",
    "description": "What this example demonstrates",
    "user_intent": "What the user wants to accomplish",
    "code": "The command or code to run",
    "language": "bash",
    "expected_output": "What the user should see"
  }}
]
```"""

# --- AGENTS.md Generation Prompts ---

AGENTS_MD_SYSTEM = """You are an expert at writing AGENTS.md files that help AI coding agents
understand and work with repositories effectively. Your output should be:

1. Complete but concise
2. Focused on what agents need to know
3. Following the AAIF AGENTS.md specification"""

AGENTS_MD_PROMPT = """# AGENTS.md Generation

Generate an AGENTS.md file for the following repository:

## Repository Information
- Name: {repo_name}
- Primary Language: {language}
- Package Manager: {package_manager}
- Test Framework: {test_framework}

## README Content
{readme_content}

## Existing Guidance
{existing_guidance}

## CI/CD Configuration
{ci_config}

## Requirements
Generate a complete AGENTS.md with these sections:
1. Project Overview (brief description, key directories)
2. Dev Environment (setup commands, dependencies)
3. Testing Instructions (how to run tests, coverage requirements)
4. PR Instructions (commit format, checklist)
5. Coding Conventions (style, patterns to follow)

Keep the total under 1500 tokens."""

# --- Security Analysis Prompts ---

SECURITY_ANALYSIS_SYSTEM = """You are a security expert analyzing agent skills for potential
vulnerabilities. Look for:

1. Unrestricted file system access
2. Network calls without allowlisting
3. Shell command injection vectors
4. Sensitive data exposure patterns
5. Tool permission escalation"""

SECURITY_ANALYSIS_PROMPT = """# Security Analysis

Analyze the following skill for security issues:

{content}

Check for:
1. File system operations without path restrictions
2. Network calls to arbitrary URLs
3. Shell commands with user input interpolation
4. Exposure of API keys, tokens, or credentials
5. Excessive tool permissions

Output as JSON:
```json
{{
  "issues": [
    {{
      "severity": "high|medium|low",
      "type": "category",
      "description": "string",
      "line": number,
      "recommendation": "string"
    }}
  ],
  "score": 0.0-1.0,
  "summary": "string"
}}
```"""

# --- Optimization Prompts ---

OPTIMIZATION_SYSTEM = """You are an expert at optimizing agent skills for token efficiency
while maintaining clarity and usefulness. Techniques include:

1. Removing redundant content
2. Using imperative voice
3. Consolidating examples
4. Moving detailed content to references"""

OPTIMIZATION_PROMPT = """# Skill Optimization

Optimize the following skill to reduce token count while maintaining usefulness:

Current Token Count: {current_tokens}
Target Token Count: {target_tokens}

## Content
{content}

## Optimization Strategies
1. Remove redundant phrases and filler words
2. Convert passive voice to imperative
3. Merge similar examples
4. Move detailed documentation to reference files
5. Use tables instead of verbose lists
6. Remove obvious/unnecessary troubleshooting items

Output the optimized SKILL.md content."""

# --- Prompt Registry ---

_PROMPTS: dict[str, PromptTemplate] = {
    "semantic_analysis_system": PromptTemplate(
        name="semantic_analysis_system",
        template=SEMANTIC_ANALYSIS_SYSTEM,
        description="System prompt for semantic analysis",
    ),
    "semantic_analysis": PromptTemplate(
        name="semantic_analysis",
        template=SEMANTIC_ANALYSIS_PROMPT,
        description="Prompt for MCP server semantic analysis",
    ),
    "skill_generation_system": PromptTemplate(
        name="skill_generation_system",
        template=SKILL_GENERATION_SYSTEM,
        description="System prompt for skill generation",
    ),
    "skill_generation": PromptTemplate(
        name="skill_generation",
        template=SKILL_GENERATION_PROMPT,
        description="Prompt for SKILL.md generation",
    ),
    "example_generation_system": PromptTemplate(
        name="example_generation_system",
        template=EXAMPLE_GENERATION_SYSTEM,
        description="System prompt for example generation",
    ),
    "example_generation": PromptTemplate(
        name="example_generation",
        template=EXAMPLE_GENERATION_PROMPT,
        description="Prompt for example synthesis",
    ),
    "agents_md_system": PromptTemplate(
        name="agents_md_system",
        template=AGENTS_MD_SYSTEM,
        description="System prompt for AGENTS.md generation",
    ),
    "agents_md": PromptTemplate(
        name="agents_md",
        template=AGENTS_MD_PROMPT,
        description="Prompt for AGENTS.md generation",
    ),
    "security_analysis_system": PromptTemplate(
        name="security_analysis_system",
        template=SECURITY_ANALYSIS_SYSTEM,
        description="System prompt for security analysis",
    ),
    "security_analysis": PromptTemplate(
        name="security_analysis",
        template=SECURITY_ANALYSIS_PROMPT,
        description="Prompt for security analysis",
    ),
    "optimization_system": PromptTemplate(
        name="optimization_system",
        template=OPTIMIZATION_SYSTEM,
        description="System prompt for optimization",
    ),
    "optimization": PromptTemplate(
        name="optimization",
        template=OPTIMIZATION_PROMPT,
        description="Prompt for skill optimization",
    ),
}


def get_prompt(name: str) -> str:
    """Get a prompt template by name."""
    if name not in _PROMPTS:
        raise KeyError(f"Unknown prompt: {name}")
    return _PROMPTS[name].template


def get_prompt_template(name: str) -> PromptTemplate:
    """Get a PromptTemplate object by name."""
    if name not in _PROMPTS:
        raise KeyError(f"Unknown prompt: {name}")
    return _PROMPTS[name]


def list_prompts() -> list[str]:
    """List all available prompt names."""
    return list(_PROMPTS.keys())
