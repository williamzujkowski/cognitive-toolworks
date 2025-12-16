# PyPI Release Guide

This guide covers releasing cognitive-toolworks to PyPI.

## Pre-Release Checklist

- [ ] All tests pass: `pytest tests/`
- [ ] Linting passes: `ruff check . && mypy src/`
- [ ] Version updated in `pyproject.toml` and `src/cognitive_toolworks/__init__.py`
- [ ] CHANGELOG.md updated with release date and changes
- [ ] README.md accurate and up-to-date
- [ ] No secrets or hardcoded paths in source code
- [ ] All __pycache__ directories cleaned

## Build Process

1. Clean previous builds:
```bash
rm -rf dist/ build/ *.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} +
```

2. Install/upgrade build tools:
```bash
python -m pip install --upgrade build twine
```

3. Build distributions:
```bash
python -m build
```

4. Verify build:
```bash
python -m twine check dist/*
```

5. Check wheel contents:
```bash
python -m zipfile -l dist/cognitive_toolworks-*.whl | less
```

## Testing Locally

Install the built wheel to verify it works:
```bash
python -m pip install --force-reinstall dist/cognitive_toolworks-*.whl
ct version
ct --help
```

## Upload to TestPyPI (Optional)

Test the release process on TestPyPI first:

1. Create account at https://test.pypi.org/

2. Configure API token in `~/.pypirc`:
```ini
[testpypi]
username = __token__
password = pypi-...
```

3. Upload to TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

4. Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ cognitive-toolworks
```

## Upload to PyPI

1. Create account at https://pypi.org/

2. Configure API token in `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-...
```

3. Upload to PyPI:
```bash
python -m twine upload dist/*
```

4. Verify at https://pypi.org/project/cognitive-toolworks/

5. Test installation:
```bash
pip install cognitive-toolworks
```

## Post-Release

1. Tag release in git:
```bash
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0
```

2. Create GitHub release with changelog

3. Update documentation site if applicable

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

## Common Issues

### Build fails with "no such file"
- Ensure all required files are present
- Check `pyproject.toml` `[tool.hatch.build.targets.*]` config

### Twine upload fails
- Verify API token is correct
- Check network connectivity
- Ensure version doesn't already exist on PyPI

### Import fails after installation
- Check package structure in wheel: `python -m zipfile -l dist/*.whl`
- Verify `py.typed` marker is included
- Check `__init__.py` exports

### Missing dependencies
- Verify all dependencies listed in `pyproject.toml` `[project.dependencies]`
- Test in clean virtual environment

## Security Notes

- Never commit API tokens or credentials
- Use API tokens, not username/password
- Store tokens in `~/.pypirc` with restricted permissions: `chmod 600 ~/.pypirc`
- Use `--repository` flag to avoid accidental uploads
- Review `gitleaks` output before committing
