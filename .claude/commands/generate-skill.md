Generate a new skill from various sources.

Arguments: $ARGUMENTS (source type and path)

## From MCP Server
```bash
ct generate skill --from-mcp <config.json> --name <skill-name> --output ./skills/<slug>/
```

## From README
```bash
ct generate skill --from-readme <README.md> --name <skill-name> --output ./skills/<slug>/
```

## From OpenAPI Spec
```bash
ct generate skill --from-openapi <openapi.json> --name <skill-name> --output ./skills/<slug>/
```

## Options
- `--platform anthropic|openai|universal` - Target platform (default: universal)
- `--dry-run` - Preview without writing files
- `--examples N` - Number of examples to generate (default: 3)

After generation:
1. Review generated SKILL.md for accuracy
2. Validate: `python tooling/validate_skill.py skills/<slug>/`
3. Add CHANGELOG.md if not generated
4. Rebuild index: `python tooling/build_index.py`
