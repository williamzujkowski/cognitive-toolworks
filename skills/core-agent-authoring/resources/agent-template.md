# AGENT.md Template

Use this template when creating new agents. Replace placeholders with actual values.

```yaml
---
name: "<agent-slug>"
description: "<≤160 char description of agent's purpose and trigger conditions>"
model: "inherit"  # or "sonnet" | "opus" | "haiku"
tools: ["Read", "Write", "Bash"]  # Restrict to needed tools only
persona: "<Role description: e.g., 'Senior DevOps engineer specializing in CI/CD pipelines'>"
version: "1.0.0"
owner: "cognitive-toolworks"
keywords: ["<tag1>", "<tag2>", "<tag3>"]
---

## Purpose & When-To-Use

Invoke when user requests: "<exact trigger phrase>".

Handles multi-step workflows:
1. <Step 1>
2. <Step 2>
3. <Step 3>

Use this agent when: <specific conditions>
Do NOT use when: <contraindications>

## System Prompt

You are a <role>. Your responsibilities:
1. <Primary objective>
2. <Secondary objective>
3. <Tertiary objective>

Invoke skills: <skill-slug-1>, <skill-slug-2>.

Guidelines:
- <Behavioral guideline 1>
- <Behavioral guideline 2>
- Always enforce CLAUDE.md accuracy and citation rules

System prompt length: <token count> tokens (must be ≤1500)

## Tool Usage Guidelines

**Read**: <When and why to use>
**Write**: <When and why to use>
**Bash**: <When and why to use>
**[Other tools]**: <When and why to use>

Decision rules:
- If <condition> → use <tool>
- If <condition> → avoid <tool> (rationale)

## Workflow Patterns

### Standard Flow
1. **Discovery**: <What to discover and how>
2. **Analysis**: <What to analyze and which skills to invoke>
3. **Report**: <What to generate and format>

### Error Handling
- If <error condition> → <recovery action>
- If unrecoverable → emit TODO and stop

### Branching Logic
- If <condition A> → <path 1>
- Else if <condition B> → <path 2>
- Else → <default path>

## Skills Integration

- `<skill-slug-1>` (T<tier>): <When to invoke and expected output>
- `<skill-slug-2>` (T<tier>): <When to invoke and expected output>

Composition patterns:
- Chain: <skill-1> output → <skill-2> input
- Parallel: Invoke <skill-1> and <skill-2> concurrently → aggregate results

## Examples

**Example 1: Happy Path**
```
User: "orchestrator <trigger phrase>"

Agent workflow:
1. Discovery: [specific actions]
2. Analysis: [skill invocations]
3. Report: [outputs generated]

Expected output: [format and content]
```

**Example 2: Error Handling**
```
User: "<incomplete request>"

Agent workflow:
1. Validation: Detect missing <input>
2. Request clarification: "<specific question>"
3. Wait for user input

Expected output: [clarification request]
```

## Quality Gates

- [ ] All <metrics> collected successfully
- [ ] <Validation check 1> passes
- [ ] <Validation check 2> passes
- [ ] Report generated in <format>
- [ ] All citations include access dates (NOW_ET)
- [ ] No secrets or PII in outputs

Success criteria:
- <Quantitative metric 1>: <threshold>
- <Quantitative metric 2>: <threshold>

## Resources

- **<Resource 1 Title>** (accessed <NOW_ET>): <URL>
- **<Resource 2 Title>** (accessed <NOW_ET>): <URL>
- **<Resource 3 Title>** (accessed <NOW_ET>): <URL>
```

## Template Usage Guidelines

1. **Fill all placeholders** in angle brackets `<...>`
2. **Validate system prompt length** (≤1500 tokens via tiktoken)
3. **Test tool restrictions** (ensure all listed tools are approved)
4. **Add 1–2 examples** (≤30 lines each) in `/agents/<slug>/examples/`
5. **Create CHANGELOG.md** starting at v1.0.0
6. **Generate index entry** for `/index/agents-index.json`
7. **Run validation** via `tooling/validate_agent.py` (if available)

## Approved MCP Tools

- Read, Write, Edit
- Bash, BashOutput, KillShell
- Glob, Grep
- Task (for sub-agent delegation)
- WebFetch, WebSearch
- TodoWrite
- NotebookEdit
- SlashCommand
- mcp__* (context7, sequential-thinking, playwright, github)

## Common Pitfalls

- ❌ System prompt >1500 tokens → Extract to workflows/ or resources/
- ❌ Pasting full skill content in system prompt → Reference by slug only
- ❌ Overly broad tool permissions → Restrict to minimum necessary
- ❌ Missing error handling → Add abort conditions and recovery procedures
- ❌ Examples >30 lines → Trim to essential interaction only
