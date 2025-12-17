Rebuild the skills and agents indices.

Run the index building scripts:

```bash
python tooling/build_index.py
python tooling/build_agent_index.py
```

This will:
1. Scan all skills/ directories for SKILL.md files
2. Extract frontmatter metadata from each skill
3. Generate index/skills-index.json with entries for all skills
4. Scan all agents/ directories for AGENT.md files
5. Extract metadata from each agent
6. Generate index/agents-index.json with entries for all agents

After rebuilding, verify the indices:
- Check skills count matches directory count
- Check agents count matches directory count
- Ensure no duplicate slugs exist
