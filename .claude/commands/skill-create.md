Create a new skill following CLAUDE.md standards.

Arguments: $ARGUMENTS (skill topic or name)

Steps:
1. Determine appropriate slug using domain-first naming: `{domain}-{scope}-{action}`
2. Create directory: `skills/{slug}/`
3. Generate SKILL.md with required structure:
   - YAML frontmatter (name, slug, description ≤160 chars, capabilities, inputs, outputs, keywords, version, owner, license, security, links)
   - Required sections: Purpose & When-To-Use, Pre-Checks, Procedure (T1/T2/T3), Decision Rules, Output Contract, Examples (≤30 lines), Quality Gates, Resources
4. Create CHANGELOG.md with initial v1.0.0 entry
5. Create examples/ directory with one example file (≤30 lines)
6. Run validation: `python tooling/validate_skill.py skills/{slug}/`
7. Rebuild index: `python tooling/build_index.py`

Follow CLAUDE.md §3 for exact format requirements.
