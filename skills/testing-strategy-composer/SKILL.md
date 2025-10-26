---
name: "Testing Strategy Composer"
slug: testing-strategy-composer
description: "Compose comprehensive testing strategies spanning unit, integration, e2e, and performance tests with optimal coverage."
capabilities:
  - analyze_system_architecture
  - recommend_test_type_distribution
  - generate_test_scaffolding
  - identify_coverage_gaps
  - create_execution_plans
inputs:
  system_description:
    type: string
    description: "Text or architecture diagram describing the system under test"
    required: true
  tech_stack:
    type: array
    description: "List of technologies, frameworks, and languages"
    required: true
  constraints:
    type: object
    description: "Budget, time, or resource limitations"
    required: false
  existing_coverage:
    type: object
    description: "Current test metrics (lines covered, test count, types)"
    required: false
outputs:
  test_strategy:
    type: markdown
    description: "Complete testing strategy document with test pyramid recommendations"
  test_scaffolding:
    type: code
    description: "Framework-specific code templates for each test type"
  coverage_gaps:
    type: json
    description: "Identified untested areas and risk assessment"
  execution_plan:
    type: markdown
    description: "Phased rollout timeline with effort estimates"
keywords:
  - testing
  - test-pyramid
  - unit-tests
  - integration-tests
  - e2e-tests
  - performance-tests
  - test-strategy
  - coverage
  - quality-assurance
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: recommended
links:
  - https://testing.googleblog.com/
  - https://martinfowler.com/testing/
  - https://martinfowler.com/articles/practical-test-pyramid.html
  - https://learn.microsoft.com/en-us/dotnet/core/testing/
  - https://www.istqb.org/certifications/certified-tester-foundation-level
---

## Purpose & When-To-Use

**Trigger conditions:**

- Starting a new project that needs a comprehensive testing approach
- Existing codebase with insufficient or imbalanced test coverage
- Technical debt remediation requiring systematic test improvement
- Architecture changes necessitating test strategy reassessment
- Team onboarding requiring clear testing guidelines

**Use this skill when** you need to establish or improve testing practices with clear ROI, balanced coverage across the test pyramid, and framework-specific implementation guidance.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-25T21:30:36-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `system_description` is non-empty string or parseable diagram
   - `tech_stack` contains at least one technology identifier
   - `constraints` (if provided) includes valid keys: `budget`, `time`, `team_size`
   - `existing_coverage` (if provided) has numeric metrics
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify links resolve
4. **Framework compatibility**: Confirm tech_stack technologies have known testing frameworks

**Abort conditions:**

- System description is too vague to identify testable components
- Tech stack includes only proprietary/undocumented technologies
- Constraints are contradictory (e.g., "zero budget" + "100% coverage")

---

## Procedure

### T1: Fast Path (≤2k tokens)

**Goal**: Analyze system and recommend test type distribution.

1. **Parse system description**:
   - Identify architecture pattern (monolith, microservices, serverless, mobile, etc.)
   - Extract key components (API, database, UI, services, jobs)
   - Determine complexity level (simple/moderate/complex)

2. **Apply test pyramid heuristics** (based on [Martin Fowler's Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html), accessed 2025-10-25):
   - **Unit tests (70%)**: Business logic, utilities, pure functions
   - **Integration tests (20%)**: Database, API contracts, external services
   - **E2E tests (10%)**: Critical user journeys, smoke tests
   - Adjust ratios based on architecture (e.g., API-only systems: 60/30/10)

3. **Output initial recommendation**:
   ```json
   {
     "test_distribution": {
       "unit": 70,
       "integration": 20,
       "e2e": 10
     },
     "priority_areas": ["auth", "payment", "data-sync"],
     "estimated_effort_hours": 40
   }
   ```

**Token budget**: ≤2k tokens

---

### T2: Extended Analysis (≤6k tokens)

**Goal**: Generate test scaffolding, calculate gaps, and create execution plan.

4. **Map tech stack to testing frameworks**:
   - JavaScript/Node.js → Jest, Mocha, Supertest, Playwright
   - Python → pytest, unittest, Selenium
   - Java → JUnit, Mockito, RestAssured
   - C# → xUnit, NUnit, SpecFlow
   - Consult [Microsoft Testing Patterns](https://learn.microsoft.com/en-us/dotnet/core/testing/, accessed 2025-10-25)

5. **Generate framework-specific scaffolding**:
   - Unit test template with arrange-act-assert pattern
   - Integration test template with setup/teardown
   - E2E test template for critical path
   - Performance test baseline (if applicable)
   - Reference [Google Testing Blog](https://testing.googleblog.com/, accessed 2025-10-25) for best practices

6. **Identify coverage gaps**:
   - Compare `existing_coverage` to targets
   - Calculate gap percentage per test type
   - Prioritize by risk (auth > payments > admin)
   - Output JSON with specific untested modules

7. **Create phased execution plan**:
   - Phase 1 (Week 1): High-risk unit tests
   - Phase 2 (Week 2): Integration tests for data layer
   - Phase 3 (Week 3): E2E critical paths
   - Phase 4 (Week 4): Performance baselines + refactor
   - Apply ISTQB Foundation principles ([ISTQB](https://www.istqb.org/certifications/certified-tester-foundation-level, accessed 2025-10-25))

**Token budget**: ≤6k tokens total (including T1)

---

### T3: Deep Dive (not implemented for this skill)

**T3 is not required** for this P0 skill; T2 provides sufficient depth for most testing strategies.

---

## Decision Rules

**Test distribution adjustments:**

- **Microservices**: Increase integration to 30%, decrease unit to 60%
- **Mobile apps**: Increase E2E to 20% (UI-critical), decrease integration to 15%
- **API-only**: Integration to 35%, unit to 55%, E2E to 10%
- **ML/Data pipelines**: Add performance tests (10%), adjust others proportionally

**Effort estimation** (per 1000 LOC):

- Unit tests: 4-8 hours
- Integration tests: 8-16 hours
- E2E tests: 16-24 hours
- Performance tests: 20-40 hours

**Coverage thresholds** (from [Martin Fowler Testing](https://martinfowler.com/testing/, accessed 2025-10-25)):

- Minimum acceptable: 60%
- Target for production: 80%
- Aspirational: 90%+ (diminishing returns above 85%)

**Stop conditions:**

- If constraints allow <10 hours: recommend T1 fast path only (unit tests for critical paths)
- If no testable components identified: emit TODO and request clarification
- If tech_stack is purely manual/visual testing: redirect to exploratory testing skill

---

## Output Contract

**Required fields** (all outputs):

```typescript
interface TestStrategy {
  strategy: string;              // Markdown document (200-800 words)
  test_distribution: {
    unit: number;                // Percentage (0-100)
    integration: number;
    e2e: number;
    performance?: number;
  };
  priority_areas: string[];      // Top 3-5 high-risk components
  estimated_effort_hours: number;
}

interface TestScaffolding {
  framework: string;             // e.g., "Jest", "pytest"
  unit_template: string;         // Code snippet
  integration_template: string;
  e2e_template: string;
  setup_instructions: string;    // Installation/config steps
}

interface CoverageGaps {
  current_coverage_percent: number;
  target_coverage_percent: number;
  gap_percent: number;
  untested_modules: Array<{
    name: string;
    risk: "high" | "medium" | "low";
    estimated_effort_hours: number;
  }>;
}

interface ExecutionPlan {
  phases: Array<{
    phase_number: number;
    duration_weeks: number;
    focus_area: string;
    deliverables: string[];
    success_criteria: string;
  }>;
  total_duration_weeks: number;
  dependencies: string[];        // External blockers
}
```

**Format**:

- `test_strategy`: Markdown with headings (## Overview, ## Test Types, ## Rationale)
- `test_scaffolding`: Code blocks with language hints (```javascript)
- `coverage_gaps`: Valid JSON
- `execution_plan`: Markdown with tables or numbered lists

**Validation**:

- All percentages sum to 100 (±2% rounding tolerance)
- Effort estimates are positive integers
- Phase dependencies are acyclic

---

## Examples

### Example 1: REST API System (T2)

```yaml
INPUT:
  system_description: "REST API with Node.js/Express, PostgreSQL, Redis"
  tech_stack: ["node.js", "express", "jest", "supertest"]
  existing_coverage: {unit: 45, integration: 10, e2e: 0}

OUTPUT:
  test_distribution: {unit: 65, integration: 25, e2e: 10}

  scaffolding:
    # Unit test (Jest)
    describe('UserService', () => {
      it('hashes password', () => {
        expect(hashPassword('secret')).not.toBe('secret');
      });
    });

    # Integration test
    describe('POST /users', () => {
      it('creates user in DB', async () => {
        const res = await request(app).post('/users').send({name: 'Alice'});
        expect(res.status).toBe(201);
      });
    });

  coverage_gaps:
    - {module: "AuthService", risk: "high", effort_hours: 8}
```

---

## Quality Gates

**Token budgets** (mandatory):

- T1 ≤ 2k tokens (recommendation only)
- T2 ≤ 6k tokens (full strategy + scaffolding)
- T3 not implemented

**Safety checks**:

- [ ] No hardcoded credentials in test templates
- [ ] No PII in example data
- [ ] Framework versions are recent (within 2 years)

**Auditability**:

- [ ] All sources cited with access date = `NOW_ET`
- [ ] Effort estimates include methodology reference
- [ ] Test distribution rationale tied to architecture pattern

**Determinism**:

- [ ] Same inputs produce same percentage recommendations (±5%)
- [ ] Scaffolding templates are idempotent
- [ ] Gap calculations are reproducible

**Validation checklist**:

- [ ] Output JSON validates against schema
- [ ] Markdown renders without errors
- [ ] Code snippets are syntactically valid
- [ ] Total effort ≤ constraint time budget

---

## Resources

**Primary sources** (accessed 2025-10-25):

1. **Google Testing Blog**: https://testing.googleblog.com/
   Best practices, case studies, and emerging patterns from Google's testing infrastructure team.

2. **Martin Fowler - Testing**: https://martinfowler.com/testing/
   Canonical testing patterns, pyramid model, and test doubles taxonomy.

3. **Practical Test Pyramid**: https://martinfowler.com/articles/practical-test-pyramid.html
   Detailed guide on test distribution, anti-patterns, and framework examples.

4. **Microsoft Testing Patterns**: https://learn.microsoft.com/en-us/dotnet/core/testing/
   Official guidance for unit, integration, and performance testing in .NET ecosystems.

5. **ISTQB Foundation Level**: https://www.istqb.org/certifications/certified-tester-foundation-level
   International standard for testing terminology, lifecycle, and techniques.

**Additional templates**:

- See `resources/test-pyramid-template.md` for Markdown strategy template
- See `examples/strategy-example.txt` for complete workflow example

**Related skills** (future):

- `performance-test-designer` (for load/stress testing deep dive)
- `mutation-testing-analyzer` (for assessing test effectiveness)
- `flaky-test-investigator` (for debugging unstable tests)

---

**End of SKILL.md**
