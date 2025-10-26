---
name: End-to-End Testing Framework Generator
slug: e2e-testing-generator
description: Generate e2e test suites using Playwright, Cypress, or Selenium with page objects, accessibility checks, visual regression, and cross-browser testing
capabilities:
  - Playwright test suite generation with page object model
  - Cypress component and integration test scaffolding
  - Selenium WebDriver multi-browser test creation
  - Accessibility validation using axe-core integration
  - Visual regression testing configuration
  - Parallel execution and CI/CD integration
inputs:
  framework:
    type: enum
    values: [playwright, cypress, selenium]
    required: true
  application_type:
    type: enum
    values: [web, spa, mobile-web]
    required: true
  test_scope:
    type: enum
    values: [smoke, critical-path, full-regression]
    required: true
  features:
    type: array
    description: List of application features to test
    required: false
  accessibility_level:
    type: enum
    values: [none, wcag-a, wcag-aa, wcag-aaa]
    default: wcag-aa
outputs:
  test_suite:
    type: object
    description: Generated e2e test files
    schema:
      files: array
      framework_config: object
      test_count: integer
  page_objects:
    type: object
    description: Reusable page models and selectors
    schema:
      models: array
      helpers: array
  ci_config:
    type: object
    description: Parallel execution and CI integration
    schema:
      pipeline_file: string
      parallelization_strategy: string
      browser_matrix: array
  a11y_checks:
    type: object
    description: Accessibility validation configuration
    schema:
      rules: array
      compliance_level: string
      reporter: string
keywords:
  - e2e testing
  - playwright
  - cypress
  - selenium
  - page object model
  - accessibility testing
  - visual regression
  - cross-browser testing
  - test automation
  - CI/CD integration
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  data_sensitivity: low
  pii_handling: none
  secrets_management: environment_variables_only
links:
  - title: Playwright Documentation
    url: https://playwright.dev/docs/intro
    accessed: 2025-10-26T02:31:27-0400
  - title: Cypress Best Practices
    url: https://docs.cypress.io/guides/references/best-practices
    accessed: 2025-10-26T02:31:27-0400
  - title: Selenium WebDriver Documentation
    url: https://www.selenium.dev/documentation/webdriver/
    accessed: 2025-10-26T02:31:27-0400
  - title: axe-core Accessibility Rules
    url: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
    accessed: 2025-10-26T02:31:27-0400
---

## Purpose & When-To-Use

**Trigger conditions:**

* You need a complete e2e test suite for a web application or SPA
* You want page object pattern implementation for maintainability
* You require accessibility validation (WCAG A/AA/AAA) in automated tests
* You need cross-browser testing configuration (Chrome, Firefox, Safari, Edge)
* You're setting up visual regression testing for UI components
* You want parallel test execution in CI/CD pipelines

**Scope:** Generates production-ready test suites with framework-specific best practices, reusable page models, accessibility checks, and CI integration. Supports Playwright (recommended), Cypress, and Selenium WebDriver.

**Not for:** Unit tests, API tests (use dedicated skills), performance testing, or load testing.

## Pre-Checks

**Required before execution:**

1. **Time normalization:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
2. **Input validation:**
   - `framework` must be one of: playwright, cypress, selenium
   - `application_type` must be one of: web, spa, mobile-web
   - `test_scope` must be one of: smoke, critical-path, full-regression
   - `features` array must not be empty (if provided)
   - `accessibility_level` valid for WCAG standards
3. **Source freshness checks:**
   - Playwright docs version ≥1.40 (accessed `NOW_ET`)
   - Cypress docs version ≥13.x (accessed `NOW_ET`)
   - Selenium WebDriver version ≥4.x (accessed `NOW_ET`)
   - axe-core version ≥4.8 (accessed `NOW_ET`)
4. **Framework availability:** Verify target framework installation instructions are current

**Abort if:** Framework choice conflicts with application_type (e.g., Selenium for component testing), or accessibility_level requirements exceed framework capabilities.

## Procedure

### Tier 1: Basic E2E Test Suite (≤2k tokens)

**Fast path for 80% of common cases:**

1. **Framework selection:**
   - **Playwright:** Default for modern web/SPA with built-in cross-browser support
   - **Cypress:** For component testing and developer-friendly debugging
   - **Selenium:** For legacy browser support or existing infrastructure

2. **Generate base configuration:**
   - Framework config file (playwright.config.ts, cypress.config.js, or wdio.conf.js)
   - Base URL, timeouts, retry logic
   - Browser launch options

3. **Create page object foundation:**
   - Base Page class with common methods (click, type, waitFor, navigate)
   - Locator strategies (data-testid preferred, CSS fallback)
   - Example page object for login/authentication

4. **Generate smoke test:**
   - Single critical path test (e.g., login → dashboard → logout)
   - Uses page objects
   - Basic assertions (visible, text content, navigation)

**Output:** Working test suite with 1-3 smoke tests, reusable page object pattern, runnable locally.

### Tier 2: Advanced Patterns (≤6k tokens)

**Extended validation with accessibility and visual regression:**

1. **Expand page object library:**
   - Create page objects for all major application sections
   - Add custom commands/helpers (e.g., `loginAsAdmin()`, `createEntity()`)
   - Implement waiting strategies (network idle, specific elements)

2. **Accessibility integration:**
   - Install and configure axe-core or @axe-core/playwright
   - Add accessibility checks to critical user flows
   - Configure WCAG level (A, AA, AAA) and violation reporting
   - Example: `await expect(page).toPassA11yChecks({ wcagLevel: 'AA' })`

3. **Visual regression setup:**
   - Configure screenshot comparison (Percy, Playwright screenshots, Cypress snapshots)
   - Define baseline images for key UI states
   - Set pixel diff thresholds and ignore regions

4. **Cross-browser testing:**
   - Configure browser matrix (Chromium, Firefox, WebKit/Safari)
   - Mobile viewport emulation for responsive testing
   - Device-specific test scenarios

5. **Test data management:**
   - Fixture files or API-based test data setup
   - Cleanup strategies (database resets, API teardown)
   - Isolated test execution (no shared state)

**Output:** Comprehensive test suite with 10-20 tests covering critical paths, accessibility validation, visual regression, and multi-browser support.

### Tier 3: CI Integration & Parallel Execution (≤12k tokens)

**Deep dive for production deployment:**

1. **CI/CD pipeline configuration:**
   - GitHub Actions, GitLab CI, CircleCI, or Jenkins pipeline
   - Docker container setup for consistent test environments
   - Artifact storage (screenshots, videos, traces)
   - Test result reporting (JUnit XML, HTML reports)

2. **Parallelization strategy:**
   - Playwright: Shard tests across workers (`--shard=1/4`)
   - Cypress: Parallel execution with Cypress Dashboard or split by spec
   - Selenium: Grid configuration for distributed execution

3. **Flaky test mitigation:**
   - Retry logic configuration (max 2-3 retries)
   - Wait strategy refinement (avoid hard sleeps)
   - Network stubbing/mocking for deterministic tests
   - Screenshot/video on failure for debugging

4. **Advanced accessibility testing:**
   - Full page scans + component-level checks
   - Custom axe rules for organization-specific requirements
   - Accessibility regression tracking (fail on new violations)

5. **Monitoring and alerting:**
   - Test duration trending
   - Failure rate dashboards
   - Slack/email notifications for critical test failures

**Output:** Production-ready test suite with CI integration, parallel execution, comprehensive reporting, and flaky test handling. Ready for continuous deployment pipelines.

## Decision Rules

**Framework selection matrix:**

| Requirement | Playwright | Cypress | Selenium |
|------------|-----------|---------|----------|
| Modern web/SPA | ✓ Best | ✓ Good | ○ OK |
| Component testing | ○ Limited | ✓ Best | ✗ No |
| Cross-browser (built-in) | ✓ Yes | ○ Chromium-only free | ✓ Yes |
| Mobile emulation | ✓ Excellent | ✓ Good | ○ Limited |
| Network interception | ✓ Built-in | ✓ Built-in | ✗ Requires proxy |
| Debugging DX | ✓ Excellent | ✓ Excellent | ○ Basic |
| Legacy browser support | ○ Limited | ✗ No | ✓ Yes |

**Test scope thresholds:**

* **Smoke:** 3-5 tests covering authentication and primary user flow (T1 sufficient)
* **Critical-path:** 10-20 tests covering all major features and user journeys (T2 required)
* **Full-regression:** 50+ tests with edge cases, error states, and accessibility (T3 required)

**Accessibility validation thresholds:**

* **WCAG A:** Basic compliance (keyboard nav, alt text) - 15 rules
* **WCAG AA:** Standard compliance (color contrast, labels) - 38 rules
* **WCAG AAA:** Enhanced compliance (extended contrast, minimal flashing) - 61 rules

**Abort conditions:**

* Framework does not support required features (e.g., Cypress for multi-tab flows)
* Application requires authentication flows that cannot be automated safely
* Visual regression baseline images cannot be generated (missing UI states)

## Output Contract

**Required fields:**

```typescript
{
  test_suite: {
    files: string[],              // Array of generated test file paths
    framework_config: object,     // Framework-specific config object
    test_count: number,           // Total number of test scenarios
    coverage_areas: string[]      // List of tested features
  },
  page_objects: {
    models: Array<{               // Page object classes
      name: string,
      path: string,
      methods: string[]
    }>,
    helpers: Array<{              // Utility functions
      name: string,
      description: string
    }>
  },
  ci_config: {
    pipeline_file: string,        // Path to CI config (e.g., .github/workflows/e2e.yml)
    parallelization_strategy: string,  // "sharding" | "splitting" | "grid"
    browser_matrix: string[],     // ["chromium", "firefox", "webkit"]
    estimated_duration_minutes: number
  },
  a11y_checks: {
    rules: Array<{                // axe-core rules configuration
      id: string,
      impact: "critical" | "serious" | "moderate" | "minor"
    }>,
    compliance_level: "wcag-a" | "wcag-aa" | "wcag-aaa",
    reporter: string,             // HTML, JSON, or custom
    violation_handling: "fail" | "warn" | "log"
  }
}
```

**Optional fields:**

* `visual_regression`: Screenshot comparison configuration
* `test_data`: Fixture file paths and seeding strategies
* `environment_config`: Environment-specific variables (staging, production)

## Examples

**Example 1: Playwright Admin Dashboard Test (≤30 lines)**

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';
import { DashboardPage } from '../pages/dashboard-page';
import { injectAxe, checkA11y } from 'axe-playwright';
test.describe('Admin Dashboard E2E', () => {
  test('authenticated user can view and create entities with WCAG AA compliance', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.navigate();
    await loginPage.login('admin@example.com', process.env.ADMIN_PASSWORD);
    const dashboard = new DashboardPage(page);
    await expect(dashboard.welcomeMessage).toContainText('Welcome, Admin');
    await injectAxe(page);
    await checkA11y(page, null, { detailedReport: true, wcagLevel: 'AA' });
    await dashboard.clickCreateButton();
    await dashboard.fillEntityForm({ name: 'Test Entity', type: 'Standard' });
    await dashboard.submitForm();
    await expect(dashboard.successToast).toBeVisible();
    await expect(dashboard.entityList).toContainText('Test Entity');
    await expect(page).toHaveScreenshot('dashboard-with-entity.png');
  });
});
```

See `/skills/e2e-testing-generator/examples/` for additional patterns and page object implementations.

## Quality Gates

**Token budgets (enforced):**

* **T1:** ≤2k tokens — Basic test suite with page objects (smoke tests)
* **T2:** ≤6k tokens — Accessibility, visual regression, cross-browser (critical-path)
* **T3:** ≤12k tokens — CI integration, parallelization, monitoring (full-regression)

**Safety checks:**

* No hardcoded credentials in test files (use environment variables)
* No secrets in version control (use .env files with .gitignore)
* Page objects must not expose internal DOM structure to tests
* Accessibility violations must be surfaced in test reports

**Auditability requirements:**

* All generated tests must have descriptive names
* Test failures must include screenshots and/or videos
* CI pipeline must store artifacts for 30+ days
* Test execution traces must be available for debugging

**Determinism checks:**

* No `cy.wait(5000)` or `page.waitForTimeout(5000)` without justification
* Prefer explicit waits (element visibility, network idle) over arbitrary timeouts
* Flaky test retry limit: max 3 attempts before failing the build
* Visual regression thresholds: ≤0.1% pixel difference for exact matches

**Performance criteria:**

* Smoke suite must complete in ≤5 minutes
* Critical-path suite must complete in ≤20 minutes
* Full regression suite must complete in ≤60 minutes with parallelization

## Resources

**Official Documentation:**

* [Playwright API Reference](https://playwright.dev/docs/api/class-playwright) (accessed 2025-10-26T02:31:27-0400)
* [Cypress API Commands](https://docs.cypress.io/api/table-of-contents) (accessed 2025-10-26T02:31:27-0400)
* [Selenium WebDriver W3C Standard](https://www.w3.org/TR/webdriver2/) (accessed 2025-10-26T02:31:27-0400)
* [axe-core Rules and Impact Levels](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md) (accessed 2025-10-26T02:31:27-0400)

**Best Practices and Patterns:**

* [Page Object Model Pattern (Martin Fowler)](https://martinfowler.com/bliki/PageObject.html) (accessed 2025-10-26T02:31:27-0400)
* [Playwright Best Practices - Locators](https://playwright.dev/docs/best-practices) (accessed 2025-10-26T02:31:27-0400)
* [Cypress Network Stubbing Guide](https://docs.cypress.io/guides/guides/network-requests) (accessed 2025-10-26T02:31:27-0400)
* [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/) (accessed 2025-10-26T02:31:27-0400)

**CI/CD Integration Examples:**

* [Playwright GitHub Actions Setup](https://playwright.dev/docs/ci-intro) (accessed 2025-10-26T02:31:27-0400)
* [Cypress Parallelization Guide](https://docs.cypress.io/guides/guides/parallelization) (accessed 2025-10-26T02:31:27-0400)
* [Selenium Grid 4 Configuration](https://www.selenium.dev/documentation/grid/) (accessed 2025-10-26T02:31:27-0400)

**Visual Regression Tools:**

* [Percy Visual Testing](https://docs.percy.io/) (accessed 2025-10-26T02:31:27-0400)
* [Playwright Screenshots and Visual Comparisons](https://playwright.dev/docs/screenshots) (accessed 2025-10-26T02:31:27-0400)
