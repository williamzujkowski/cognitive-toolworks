---
name: "Python Tooling Specialist"
slug: "python-tooling-specialist"
description: "Generate Python project scaffolding with Poetry/pipenv, pytest configuration, type hints (mypy), linting (ruff/black), and packaging (setuptools/flit)."
capabilities:
  - Project structure generation (library, application, CLI, data pipeline)
  - Dependency management setup (Poetry, pipenv, pip-tools)
  - Testing framework configuration (pytest, coverage, tox)
  - Type checking setup (mypy, pyright)
  - Linting and formatting (ruff, black, flake8, isort)
  - Pre-commit hook configuration
  - Packaging and distribution (PyPI, wheels, versioning)
inputs:
  - project_type: "library | application | cli | data-pipeline (string)"
  - dependency_manager: "poetry | pipenv | pip-tools (string)"
  - python_version: "3.9 | 3.10 | 3.11 | 3.12 (string)"
  - project_name: "Name of the project (string)"
outputs:
  - project_structure: "Directory layout with all config files (JSON)"
  - pyproject_toml: "Complete pyproject.toml configuration (TOML)"
  - pre_commit_config: "Pre-commit hooks configuration (YAML)"
  - makefile: "Common development commands (Makefile)"
keywords:
  - python
  - tooling
  - poetry
  - pytest
  - mypy
  - ruff
  - black
  - packaging
  - pre-commit
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://python-poetry.org/docs/
  - https://docs.pytest.org/
  - https://mypy.readthedocs.io/
  - https://docs.astral.sh/ruff/
  - https://packaging.python.org/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Starting a new Python project requiring modern tooling
- Migrating legacy Python projects to contemporary best practices
- Standardizing tooling across multiple Python projects
- Setting up CI/CD pipelines with proper quality gates
- Onboarding developers to Python development workflows

**Not for:**
- Django/Flask-specific project templates (use framework CLIs)
- Jupyter notebook environments (use JupyterLab/conda)
- Simple scripts without dependencies or testing needs

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `project_type` must be one of: library, application, cli, data-pipeline
- `dependency_manager` must be one of: poetry, pipenv, pip-tools
- `python_version` must be one of: 3.9, 3.10, 3.11, 3.12 (string format)
- `project_name` must be valid Python package name (lowercase, hyphens allowed)

**Source freshness:**
- Poetry docs must be accessible [accessed 2025-10-26T02:31:27-04:00](https://python-poetry.org/docs/)
- pytest docs must be accessible [accessed 2025-10-26T02:31:27-04:00](https://docs.pytest.org/)
- mypy docs must be accessible [accessed 2025-10-26T02:31:27-04:00](https://mypy.readthedocs.io/)
- Ruff docs must be accessible [accessed 2025-10-26T02:31:27-04:00](https://docs.astral.sh/ruff/)

---

## Procedure

### T1: Basic Project Structure (≤2k tokens)

**Fast path for common cases:**

1. **Directory Layout Generation**
   - Create standard Python project structure:
     ```
     project_name/
       src/project_name/     # for library/cli
         __init__.py
         py.typed              # PEP 561 marker
       project_name/          # for application/data-pipeline
         __init__.py
       tests/
         __init__.py
         conftest.py
       docs/
       .gitignore
       README.md
       pyproject.toml
     ```

2. **Core pyproject.toml Generation**
   - Project metadata (name, version, description, authors)
   - Python version constraint (from `python_version` input)
   - Basic tool configuration placeholders
   - License and repository links

3. **Basic .gitignore**
   - Python-specific ignores (__pycache__, *.pyc, .pytest_cache, .mypy_cache)
   - Environment files (.env, .venv)
   - Build artifacts (dist/, build/, *.egg-info)

**Decision:** If only basic scaffolding needed → STOP at T1; otherwise proceed to T2.

---

### T2: Full Tooling Setup (≤6k tokens)

**Extended configuration with all tools:**

1. **Dependency Manager Configuration**

   **Poetry (pyproject.toml)** [accessed 2025-10-26T02:31:27-04:00](https://python-poetry.org/docs/pyproject/)
   ```toml
   [tool.poetry]
   name = "project-name"
   version = "0.1.0"
   description = ""
   authors = ["Your Name <you@example.com>"]

   [tool.poetry.dependencies]
   python = "^3.11"

   [tool.poetry.group.dev.dependencies]
   pytest = "^7.4.0"
   pytest-cov = "^4.1.0"
   mypy = "^1.5.0"
   ruff = "^0.1.0"
   black = "^23.9.0"
   ```

   **pipenv (Pipfile)** [accessed 2025-10-26T02:31:27-04:00](https://pipenv.pypa.io/en/latest/)
   - Generate Pipfile with dev/prod separation
   - Configure pipenv scripts for common tasks

   **pip-tools (requirements.in)** [accessed 2025-10-26T02:31:27-04:00](https://pip-tools.readthedocs.io/)
   - Create requirements.in and requirements-dev.in
   - Add Makefile targets for pip-compile

2. **Testing Configuration (pytest)** [accessed 2025-10-26T02:31:27-04:00](https://docs.pytest.org/en/7.4.x/reference/customize.html)
   ```toml
   [tool.pytest.ini_options]
   minversion = "7.0"
   addopts = "-ra -q --strict-markers --cov=src"
   testpaths = ["tests"]
   pythonpath = ["src"]
   markers = [
       "slow: marks tests as slow",
       "integration: marks tests as integration tests",
   ]
   ```

3. **Type Checking (mypy)** [accessed 2025-10-26T02:31:27-04:00](https://mypy.readthedocs.io/en/stable/config_file.html)
   ```toml
   [tool.mypy]
   python_version = "3.11"
   strict = true
   warn_return_any = true
   warn_unused_configs = true
   disallow_untyped_defs = true
   ```

4. **Linting and Formatting**

   **Ruff (all-in-one linter/formatter)** [accessed 2025-10-26T02:31:27-04:00](https://docs.astral.sh/ruff/configuration/)
   ```toml
   [tool.ruff]
   target-version = "py311"
   line-length = 100
   select = ["E", "F", "I", "N", "W", "UP"]
   ignore = ["E501"]
   ```

   **Black (code formatter)** [accessed 2025-10-26T02:31:27-04:00](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
   ```toml
   [tool.black]
   line-length = 100
   target-version = ['py311']
   ```

5. **Pre-commit Hooks** [accessed 2025-10-26T02:31:27-04:00](https://pre-commit.com/#plugins)
   - Generate `.pre-commit-config.yaml`
   - Include: ruff, black, mypy, pytest
   - Add trailing-whitespace, end-of-file-fixer

6. **Makefile for Common Commands**
   ```makefile
   .PHONY: test lint format typecheck install

   install:
       poetry install

   test:
       pytest

   lint:
       ruff check .

   format:
       black .
       ruff check --fix .

   typecheck:
       mypy src
   ```

---

### T3: Packaging and Distribution (≤12k tokens)

**Deep configuration for publishable packages:**

1. **PyPI Publishing Setup** [accessed 2025-10-26T02:31:27-04:00](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
   - Configure `[tool.poetry.build-system]` or `[build-system]`
   - Add classifiers and keywords for PyPI
   - Set up MANIFEST.in for non-Python files
   - Configure package data inclusion

2. **Versioning Strategy** [accessed 2025-10-26T02:31:27-04:00](https://python-poetry.org/docs/cli/#version)
   - Poetry: `poetry version` integration
   - Semantic versioning enforcement
   - Git tag automation via Makefile/CI

3. **Wheel Building Configuration** [accessed 2025-10-26T02:31:27-04:00](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
   - Universal vs platform-specific wheels
   - Namespace package handling
   - C extension compilation (if applicable)

4. **Entry Points and Scripts** (for CLI projects)
   ```toml
   [tool.poetry.scripts]
   my-cli = "project_name.cli:main"
   ```

5. **GitHub Actions CI/CD**
   - Matrix testing across Python versions
   - Coverage reporting (codecov/coveralls)
   - Automated PyPI publishing on tag push
   - Security scanning (bandit, safety)

6. **Documentation Setup**
   - Sphinx configuration for library projects
   - MkDocs configuration for application projects
   - Docstring style enforcement (pydocstyle)

---

## Decision Rules

**Dependency Manager Selection:**
- **Poetry:** Best for libraries and packages destined for PyPI (default recommendation)
- **pipenv:** Good for applications with deployment focus (Heroku, Docker)
- **pip-tools:** Minimal overhead, best for simple projects or constrained environments

**Project Type Structure:**
- **library:** src-layout with `src/package_name/`, includes py.typed, strict mypy
- **application:** flat layout with `package_name/`, relaxed typing, focus on integration tests
- **cli:** src-layout with entry points, includes shell completion, argparse/click/typer
- **data-pipeline:** flat layout, includes Jupyter support, pandas/numpy stubs

**Abort Conditions:**
- Invalid `project_name` (contains uppercase, special chars) → error "Invalid package name"
- Unsupported `python_version` → error "Python version must be 3.9+"
- Conflicting configuration requests → error with suggested alternatives

**Tool Version Selection:**
- Use latest stable versions as of `NOW_ET`
- For libraries: pin dev dependencies, use caret ranges for runtime deps
- For applications: pin all dependencies for reproducibility

---

## Output Contract

**Schema (JSON):**

```json
{
  "project_name": "string",
  "project_type": "library | application | cli | data-pipeline",
  "python_version": "string",
  "dependency_manager": "poetry | pipenv | pip-tools",
  "structure": {
    "directories": ["string"],
    "files": {
      "path/to/file": "file content (string)"
    }
  },
  "commands": {
    "install": "string",
    "test": "string",
    "lint": "string",
    "format": "string",
    "publish": "string (optional)"
  },
  "next_steps": ["string"],
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- `project_name`, `project_type`, `python_version`, `dependency_manager`, `structure`, `commands`, `next_steps`, `timestamp`

**File Contents:**
- All generated files must be syntactically valid (TOML/YAML/Makefile)
- Include inline comments explaining non-obvious configuration choices
- Reference official documentation in comments

---

## Examples

**Example 1: Library with Poetry**

```
INPUT: {
  project_type: "library",
  dependency_manager: "poetry",
  python_version: "3.11",
  project_name: "my-awesome-lib"
}

OUTPUT:
structure:
  - src/my_awesome_lib/__init__.py
  - src/my_awesome_lib/py.typed
  - tests/test_core.py
  - pyproject.toml (with Poetry, pytest, mypy, ruff)
  - .pre-commit-config.yaml
  - Makefile

pyproject.toml excerpt:
[tool.poetry.dependencies]
python = "^3.11"

[tool.mypy]
strict = true

commands:
  install: "poetry install"
  test: "poetry run pytest"
  publish: "poetry publish --build"
```

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (basic structure + core pyproject.toml)
- **T2:** ≤6k tokens (full tooling: pytest, mypy, ruff, pre-commit, Makefile)
- **T3:** ≤12k tokens (packaging, versioning, CI/CD, documentation)

**Safety:**
- No credential generation or storage
- .gitignore always includes .env and credential files
- pre-commit hooks check for secrets (detect-secrets)

**Auditability:**
- All tool configurations cite official documentation
- Version constraints are explicit (no floating versions in examples)
- Generated files include generation timestamp and tool versions

**Determinism:**
- Same inputs → identical file structure and configuration
- Tool versions pinned to major.minor (e.g., "^1.5" for mypy)
- No randomness in file generation

**Performance:**
- T1 generation: <1 second
- T2 generation: <3 seconds (includes all configs)
- T3 generation: <5 seconds (includes CI/CD templates)

---

## Resources

**Official Documentation (accessed 2025-10-26T02:31:27-04:00):**
1. [Poetry Documentation](https://python-poetry.org/docs/) - Dependency management and packaging
2. [pytest Documentation](https://docs.pytest.org/) - Testing framework
3. [mypy Documentation](https://mypy.readthedocs.io/) - Static type checking
4. [Ruff Documentation](https://docs.astral.sh/ruff/) - Fast Python linter
5. [Python Packaging User Guide](https://packaging.python.org/) - Official packaging guide
6. [Black Documentation](https://black.readthedocs.io/) - Code formatter
7. [pre-commit Documentation](https://pre-commit.com/) - Git hook framework

**Tool Configurations:**
- `/resources/pyproject-templates/` - Complete pyproject.toml templates by project type
- `/resources/pre-commit-configs/` - Pre-commit configurations for different tool combinations
- `/resources/makefile-templates/` - Makefile templates for poetry/pipenv/pip-tools

**Best Practices:**
- [Python Application Layouts](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) - src vs flat layout
- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface
- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml specification
- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml

**Community Resources:**
- [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) - Modern tooling guide
- [Real Python Packaging Guide](https://realpython.com/pypi-publish-python-package/) - PyPI publishing tutorial
