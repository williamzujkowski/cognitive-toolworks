Run the full repository maintenance workflow per CLAUDE.md §8A.

Execute these commands in order:

```bash
# 1. Validate all skills
python tooling/validate_skill.py

# 2. Rebuild skills index
python tooling/build_index.py

# 3. Rebuild agents index
python tooling/build_agent_index.py

# 4. Update coverage analysis
python tooling/analyze_coverage.py

# 5. Run pre-commit hooks
pre-commit run --all-files

# 6. Run tests
pytest tests/ -v
```

After maintenance:
1. Review any validation warnings
2. Check for orphaned files: `find skills/ agents/ -type d -empty`
3. Update CLAUDE.md LAST_AUDIT date if needed
4. Commit all changes: `git add index/ docs/ && git commit -m "chore(maintenance): rebuild indices and coverage"`
