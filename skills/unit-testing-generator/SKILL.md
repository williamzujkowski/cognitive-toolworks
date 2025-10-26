---
name: Unit Testing Framework Generator
slug: unit-testing-generator
description: Generate unit test scaffolding and test suites for Jest, PyTest, Go testing, JUnit, RSpec with mocking, assertions, and coverage configuration
capabilities:
  - Generate test file scaffolding for multiple frameworks
  - Create mock objects and stubs for dependencies
  - Configure coverage thresholds and reporting
  - Generate property-based testing patterns
  - Set up test fixtures and setup/teardown logic
inputs:
  framework:
    type: enum
    values: [Jest, PyTest, Go, JUnit, RSpec]
    required: true
  target_code:
    type: string
    description: File path or code description to test
    required: true
  test_type:
    type: enum
    values: [unit, integration, e2e]
    default: unit
  coverage_threshold:
    type: number
    description: Minimum coverage percentage
    default: 80
outputs:
  test_files:
    type: array
    description: Generated test file contents with paths
  config:
    type: object
    description: Framework configuration files
  coverage_setup:
    type: object
    description: Coverage configuration and thresholds
keywords:
  - testing
  - unit-tests
  - jest
  - pytest
  - junit
  - rspec
  - mocking
  - coverage
  - tdd
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: PUBLIC
links:
  - https://jestjs.io/docs/getting-started
  - https://docs.pytest.org/en/stable/
  - https://pkg.go.dev/testing
  - https://junit.org/junit5/docs/current/user-guide/
  - https://rspec.info/documentation/
---

# Unit Testing Framework Generator

## Purpose & When-To-Use

**Trigger conditions:**
- Need to create unit tests for existing code
- Setting up test infrastructure for a new project
- Generating mocks/stubs for external dependencies
- Establishing coverage baselines and CI gates
- Converting manual test cases to automated suites

**Use when:** You have code that needs test coverage with framework-specific patterns, mocking strategies, and coverage enforcement.

---

## Pre-Checks

**Required validations before proceeding:**

1. **Time normalization:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
2. **Input validation:**
   - `framework` is one of: Jest, PyTest, Go, JUnit, RSpec
   - `target_code` is either a valid file path or parseable description
   - `coverage_threshold` is 0-100
3. **Framework availability:** Verify target runtime/language compatibility
4. **Source freshness:** Documentation links valid as of `NOW_ET = 2025-10-26T02:31:24Z`

---

## Procedure

### T1: Basic Test Scaffolding (≤2k tokens)

**Fast path for 80% of cases:**

1. **Parse target code** to identify:
   - Functions/methods to test
   - Input parameters and types
   - Expected return values
2. **Generate test file** with:
   - Framework-specific imports
   - Describe/test blocks or equivalent
   - Basic assertions for happy path
   - One edge case (null/empty/zero)
3. **Output minimal config** (if missing):
   - Jest: `jest.config.js` with basic settings
   - PyTest: `pytest.ini` with test discovery
   - Go: standard `_test.go` naming
   - JUnit: `pom.xml` or `build.gradle` snippet
   - RSpec: `.rspec` and `spec_helper.rb`

**Token budget:** ≤2k tokens for code analysis + generation

---

### T2: Mocks + Coverage (≤6k tokens)

**Extended validation with dependency mocking:**

1. **Dependency analysis:**
   - Identify external calls (APIs, databases, file I/O)
   - Map to framework-specific mocking patterns
2. **Generate mocks:**
   - Jest: `jest.mock()` or `@jest/globals`
   - PyTest: `pytest-mock` fixtures or `unittest.mock`
   - Go: Interface-based test doubles
   - JUnit: Mockito or JUnit 5 mocking
   - RSpec: `allow()` and `expect()` stubs
3. **Coverage configuration:**
   - Set threshold from input (default 80%)
   - Configure reporters (JSON, LCOV, HTML)
   - Exclude patterns (vendor, generated code)
4. **Research verification (2-4 sources):**
   - Check current best practices for chosen framework (accessed `NOW_ET`)
   - Validate mocking patterns against official docs

**Token budget:** ≤6k tokens (includes retrieval + generation)

---

### T3: Advanced Patterns (≤12k tokens)

**Deep dive with property-based testing and fixtures:**

1. **Property-based testing:**
   - Jest: `fast-check` integration
   - PyTest: `hypothesis` strategies
   - Go: `testing/quick` package
   - JUnit: `jqwik` or `QuickTheories`
   - RSpec: `rantly` gem
2. **Fixture management:**
   - Shared setup/teardown across tests
   - Database seeding and cleanup
   - Factory patterns for test data
3. **Parameterized tests:**
   - Jest: `test.each()`
   - PyTest: `@pytest.mark.parametrize`
   - Go: table-driven tests
   - JUnit: `@ParameterizedTest`
   - RSpec: shared examples
4. **Generate eval scenarios:**
   - Create 3-5 test cases in `tests/evals_unit-testing-generator.yaml`
   - Include success, failure, and edge cases
5. **Full rationale document:**
   - Design decisions for mocking strategy
   - Coverage threshold justification
   - Framework-specific gotchas

**Token budget:** ≤12k tokens (includes research, generation, evals)

---

## Decision Rules

**Framework selection:**
- If `target_code` has file extension → auto-detect: `.js/.ts` → Jest, `.py` → PyTest, `.go` → Go, `.java` → JUnit, `.rb` → RSpec
- If ambiguous → prompt for explicit `framework` input

**Mocking strategy thresholds:**
- 0 external dependencies → skip T2 mocking, stay in T1
- 1-3 dependencies → T2 with explicit mocks
- 4+ dependencies → T3 with dependency injection patterns

**Abort conditions:**
- `target_code` is unparseable or empty → emit TODO and stop
- Framework not in supported list → error with alternatives
- Coverage threshold >100 or <0 → validation error

---

## Output Contract

**Required fields:**

```typescript
{
  test_files: [
    {
      path: string,          // e.g., "src/__tests__/service.test.js"
      content: string,        // Full test file code
      framework: string       // Jest|PyTest|Go|JUnit|RSpec
    }
  ],
  config: {
    file_name: string,       // e.g., "jest.config.js"
    content: string,         // Configuration code
    description: string      // What this configures
  },
  coverage_setup: {
    threshold: number,       // 0-100
    reporters: string[],     // ["json", "lcov", "text"]
    exclude_patterns: string[] // Globs to ignore
  },
  metadata: {
    generated_at: string,    // ISO-8601 timestamp
    token_tier: "T1"|"T2"|"T3",
    sources_consulted: [     // Only for T2+
      {
        title: string,
        url: string,
        accessed: string     // NOW_ET
      }
    ]
  }
}
```

**Validation:**
- All paths use forward slashes (portable)
- Code is syntactically valid for target framework
- Coverage threshold matches input or default

---

## Examples

**Input:**

```json
{
  "framework": "PyTest",
  "target_code": "class UserService:\n    def get_user(self, id): return db.query(User).get(id)",
  "test_type": "unit",
  "coverage_threshold": 90
}
```

**Output (T2 with mocking):**

```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock, patch
from myapp.services import UserService

@pytest.fixture
def mock_db():
    return Mock()

def test_get_user_success(mock_db):
    # Arrange
    user_service = UserService(db=mock_db)
    mock_db.query.return_value.get.return_value = {"id": 1, "name": "Alice"}

    # Act
    result = user_service.get_user(1)

    # Assert
    assert result["id"] == 1
    mock_db.query.assert_called_once()
```

_(Full output would include `pytest.ini` config and coverage setup; truncated for ≤30 line limit)_

---

## Quality Gates

**Token budgets (enforced):**
- T1: ≤2k tokens
- T2: ≤6k tokens
- T3: ≤12k tokens

**Safety:**
- No hardcoded credentials in test fixtures
- Mock external services (no live API calls in unit tests)
- Deterministic test data (no random values without seeds)

**Auditability:**
- All generated code includes framework version assumptions
- T2+ includes source links with access dates (`NOW_ET`)
- Mocking decisions documented in comments

**Determinism:**
- Same inputs → same test structure
- Randomized tests use explicit seeds
- Date/time mocks for time-dependent code

---

## Resources

**Official Documentation (accessed 2025-10-26T02:31:24Z):**
- [Jest - Getting Started](https://jestjs.io/docs/getting-started)
- [PyTest - Official Docs](https://docs.pytest.org/en/stable/)
- [Go Testing Package](https://pkg.go.dev/testing)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [RSpec - Documentation](https://rspec.info/documentation/)

**Mocking Libraries:**
- [Jest Mock Functions](https://jestjs.io/docs/mock-functions)
- [pytest-mock Plugin](https://pytest-mock.readthedocs.io/)
- [Mockito (Java)](https://site.mockito.org/)
- [RSpec Mocks](https://rspec.info/features/3-13/rspec-mocks/)

**Property-Based Testing:**
- [fast-check (Jest)](https://github.com/dubzzz/fast-check)
- [Hypothesis (Python)](https://hypothesis.readthedocs.io/)
- [testing/quick (Go)](https://pkg.go.dev/testing/quick)
- [jqwik (JUnit)](https://jqwik.net/)

**Coverage Tools:**
- [Istanbul (Jest)](https://istanbul.js.org/)
- [Coverage.py (PyTest)](https://coverage.readthedocs.io/)
- [go tool cover](https://go.dev/blog/cover)
- [JaCoCo (Java)](https://www.jacoco.org/jacoco/)
- [SimpleCov (Ruby)](https://github.com/simplecov-ruby/simplecov)
