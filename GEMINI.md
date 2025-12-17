# GEMINI.md - Cognitive Toolworks

> Gemini CLI instructions for AI coding assistants working on this repository.

@./AGENTS.md

## Gemini CLI Configuration

### Memory Management

Use `/memory refresh` to reload context after editing AGENTS.md or this file.

### Settings Configuration

To enable automatic loading of both files, add to `~/.gemini/settings.json`:

```json
{
  "context": {
    "fileName": ["AGENTS.md", "GEMINI.md"]
  }
}
```

### Hierarchy Notes

Gemini CLI loads instruction files in this order:
1. Global: `~/.gemini/GEMINI.md`
2. Project ancestors: From `.git` root down to current directory
3. Subdirectories: Check `skills/`, `agents/` for local overrides

### Available Commands

- `/memory show` - Display loaded context
- `/memory refresh` - Reload all instruction files
- `/memory add <text>` - Append to global GEMINI.md
- `/init` - Generate starter GEMINI.md for a project
