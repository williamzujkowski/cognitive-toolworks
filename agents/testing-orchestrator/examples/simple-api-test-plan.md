# Simple REST API Testing Plan (Orchestrated Example)

## Application Context
- **Type:** REST API service
- **Stack:** Python FastAPI + PostgreSQL
- **Deployment:** Daily deployments via GitHub Actions
- **Risk:** Medium (internal service with external dependencies)

## Orchestration Plan

### Phase 1: Analysis
**Application Profile:**
```yaml
endpoints: 12 REST endpoints (CRUD + search)
database: PostgreSQL with 8 tables
external_dependencies: 2 third-party APIs (payment, email)
current_coverage: 0% (greenfield)
```

### Phase 2: Strategy
**Test Pyramid (Target):**
- Unit tests: 75% (business logic, validators, utils)
- Integration tests: 20% (DB + external API mocking)
- E2E tests: 5% (critical API workflows)

**Framework Selection:**
- Unit: pytest + pytest-mock
- Integration: pytest + Testcontainers (PostgreSQL)
- E2E: pytest + httpx (API client testing)
- Contract: No consumer-driven contracts (internal service only)

### Phase 3: Implementation

**Skill Invocations:**

1. **testing-unit-generator**
   - Input: FastAPI route handlers, business logic, validators
   - Output: 45 test files, 78% coverage
   - Execution time: 4s

2. **testing-integration-designer**
   - Input: Database models, repository layer, external API clients
   - Output: 12 integration test files with Testcontainers setup
   - Coverage: 60% of integration code
   - Execution time: 35s

3. **e2e-testing-generator**
   - Input: 3 critical workflows (user creation, payment processing, report generation)
   - Output: 3 E2E test scenarios
   - Execution time: 15s

### Phase 4: CI/CD Integration

**GitHub Actions Pipeline:**
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/unit --cov --cov-report=xml
      - run: coverage report --fail-under=75

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration --maxfail=1

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    steps:
      - uses: actions/checkout@v4
      - run: docker-compose up -d
      - run: pytest tests/e2e
```

**Quality Gates:**
- Unit coverage ≥75%
- All integration tests pass
- E2E critical paths pass
- Total test execution <60s

## Results

**Generated Artifacts:**
- 45 unit test files (pytest)
- 12 integration test files (pytest + Testcontainers)
- 3 E2E test scenarios
- GitHub Actions workflow config
- pytest.ini and coverage configuration

**Coverage Achieved:**
- Unit: 78% (exceeds 75% target)
- Integration: 60% of integration code
- E2E: 3 critical workflows protected
- Total execution time: 54s (within budget)

**Test Pyramid Actual:**
- Unit: 76% (45 files, 200+ tests)
- Integration: 20% (12 files, 45 tests)
- E2E: 4% (3 files, 12 tests)

**Orchestration Duration:** 2 days (analysis, generation, review, CI setup)
