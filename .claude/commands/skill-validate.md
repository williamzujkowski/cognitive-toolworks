Validate a skill against CLAUDE.md standards.

Run the validation tooling on the specified skill directory:

```bash
python tooling/validate_skill.py $ARGUMENTS
```

Check for:
1. Required YAML frontmatter fields (name, slug, description, etc.)
2. Description length (must be ≤160 characters)
3. Example length (must be ≤30 lines)
4. Required body sections in correct order
5. Token budget compliance (T1 ≤2k, T2 ≤6k, T3 ≤12k)
6. No secret patterns or TODO markers

Report all validation errors and warnings.
