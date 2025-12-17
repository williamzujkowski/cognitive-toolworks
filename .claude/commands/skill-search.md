Search the skills index for matching skills.

Arguments: $ARGUMENTS (search term)

Use the CLI to search skills:
```bash
ct search $ARGUMENTS
```

Or manually search the index:
1. Read index/skills-index.json
2. Match against name, summary, and keywords fields
3. Return top 5 most relevant results with:
   - slug
   - name
   - summary
   - entry path

For code-level search, use Grep to find patterns in SKILL.md files.
