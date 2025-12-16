# Release Checklist for cognitive-toolworks v2.0.0

## Pre-Release Validation ✅

- [x] **Package Structure**
  - [x] `src/cognitive_toolworks/` layout verified
  - [x] All `__init__.py` files present
  - [x] `py.typed` marker created
  - [x] Version in `__init__.py` matches pyproject.toml (2.0.0)

- [x] **Package Metadata (pyproject.toml)**
  - [x] Name: cognitive-toolworks
  - [x] Version: 2.0.0
  - [x] Description accurate
  - [x] Author email: william.zujkowski@gmail.com
  - [x] License: Apache-2.0
  - [x] Python >=3.11
  - [x] Dependencies minimal and necessary
  - [x] Classifiers appropriate
  - [x] URLs correct (Homepage, Docs, Repo, Issues, Changelog)
  - [x] Entry points: ct, cognitive-toolworks

- [x] **Documentation**
  - [x] README.md shows PyPI installation
  - [x] README.md has PyPI badge
  - [x] CHANGELOG.md created with v2.0.0 entry
  - [x] PYPI_RELEASE.md guide created
  - [x] All installation examples updated

- [x] **Code Quality**
  - [x] No hardcoded paths
  - [x] No secrets (gitleaks clean)
  - [x] __pycache__ cleaned
  - [x] Type hints present
  - [x] Templates included

- [x] **Build & Distribution**
  - [x] `python -m build` succeeds
  - [x] `python -m twine check dist/*` passes
  - [x] Wheel: 91KB (cognitive_toolworks-2.0.0-py3-none-any.whl)
  - [x] Source: 727KB (cognitive_toolworks-2.0.0.tar.gz)
  - [x] All files included in distributions
  - [x] CHANGELOG.md, README.md, LICENSE in sdist

- [x] **Installation Testing**
  - [x] Local wheel install works
  - [x] CLI accessible: `ct version`
  - [x] CLI help works: `ct --help`
  - [x] Module import works: `import cognitive_toolworks`
  - [x] Version accessible: `cognitive_toolworks.__version__`

## Release Steps 🚀

### 1. Commit Changes
```bash
git add .
git commit -m "chore(release): prepare v2.0.0 for PyPI

- Add py.typed marker for type support
- Update README with PyPI installation
- Add CHANGELOG.md with release history
- Update author email in pyproject.toml
- Include CHANGELOG, README, LICENSE in sdist
- Add PYPI_RELEASE.md guide

Closes #35"
```

### 2. Tag Release
```bash
git tag -a v2.0.0 -m "Release v2.0.0 - PyPI initial release"
git push origin feature/phase2e-phase3
git push origin v2.0.0
```

### 3. Upload to TestPyPI (Optional but Recommended)
```bash
# Setup ~/.pypirc with TestPyPI token
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ cognitive-toolworks
ct version
```

### 4. Upload to PyPI
```bash
# Setup ~/.pypirc with PyPI token
python -m twine upload dist/*

# Verify on PyPI
open https://pypi.org/project/cognitive-toolworks/

# Test install
pip install cognitive-toolworks
ct version
```

### 5. Create GitHub Release
- Go to https://github.com/williamzujkowski/cognitive-toolworks/releases/new
- Tag: v2.0.0
- Title: cognitive-toolworks v2.0.0
- Description: Copy from CHANGELOG.md
- Attach: dist/cognitive_toolworks-2.0.0.tar.gz

### 6. Verify & Announce
- [ ] PyPI page displays correctly
- [ ] Installation works: `pip install cognitive-toolworks`
- [ ] README renders on PyPI
- [ ] All badges work
- [ ] Update any dependent projects
- [ ] Close issue #35

## Files Added/Modified

### Added
- `src/cognitive_toolworks/py.typed` - Type support marker
- `CHANGELOG.md` - Version history
- `PYPI_RELEASE.md` - Release guide
- `PYPI_PREP_SUMMARY.md` - Preparation summary
- `RELEASE_CHECKLIST.md` - This file

### Modified
- `pyproject.toml` - Updated email, added sdist includes
- `README.md` - Updated installation instructions, added PyPI badge

### Built
- `dist/cognitive_toolworks-2.0.0-py3-none-any.whl`
- `dist/cognitive_toolworks-2.0.0.tar.gz`

## Rollback Plan

If issues are found after upload:

1. **Cannot delete from PyPI** - versions are immutable
2. **Yank the release** (makes it non-installable by default):
   ```bash
   # Login to PyPI and yank the release
   # Or use: twine yank cognitive-toolworks -v 2.0.0
   ```
3. **Fix issues and release v2.0.1**

## Post-Release Monitoring

- [ ] Check PyPI download stats (24h, 7d, 30d)
- [ ] Monitor GitHub issues for installation problems
- [ ] Check CI/CD still works with published package
- [ ] Update documentation site if needed

---

**Ready for PyPI Release: ✅ YES**

All checks passed. Package is production-ready.
