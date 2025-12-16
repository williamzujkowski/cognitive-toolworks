---
name: Frontend Accessibility Validator
slug: frontend-accessibility-validator
description: Validate WCAG 2.2 compliance (A/AA/AAA) with ARIA, color contrast, keyboard navigation, screen readers, and automated testing via axe-core/Pa11y.
capabilities:
  - WCAG 2.2 compliance validation (Level A, AA, AAA with 9 new success criteria)
  - ARIA attributes and roles verification (landmarks, widgets, live regions)
  - Color contrast analysis (4.5:1 for AA, 7:1 for AAA)
  - Keyboard navigation testing (focus management, skip links, tab order)
  - Screen reader compatibility (NVDA, JAWS, VoiceOver, ORCA)
  - Semantic HTML validation (proper heading hierarchy, form labels)
  - Focus indicator visibility and contrast (WCAG 2.4.11, 2.4.13)
  - Automated testing integration (axe-core, Pa11y, Lighthouse)
  - Alternative text and image accessibility
  - Form accessibility (labels, fieldsets, error messages, autocomplete)
  - Touch target sizing (WCAG 2.5.8: 24×24 CSS pixels minimum)
  - Accessible authentication (WCAG 3.3.7, 3.3.8)
inputs:
  web_pages:
    type: array
    description: URLs or HTML files to validate
    required: true
  wcag_level:
    type: string
    description: Target WCAG level (A, AA, AAA)
    required: false
  automated_tools:
    type: array
    description: Tools to use (axe-core, Pa11y, Lighthouse)
    required: false
  manual_checks:
    type: boolean
    description: Include manual testing checklist
    required: false
  screen_readers:
    type: array
    description: Screen readers to test (NVDA, JAWS, VoiceOver)
    required: false
outputs:
  wcag_compliance_report:
    type: object
    description: WCAG 2.2 compliance status by success criterion
  violations:
    type: array
    description: List of accessibility violations with severity and remediation
  automated_test_results:
    type: object
    description: Results from axe-core, Pa11y, Lighthouse (% of issues detected)
  manual_test_checklist:
    type: array
    description: Manual testing items (keyboard nav, screen reader, contrast)
  aria_issues:
    type: array
    description: ARIA attribute and role violations
  color_contrast_report:
    type: object
    description: Contrast ratios for text, focus indicators, UI components
keywords:
  - accessibility
  - a11y
  - wcag
  - wcag-2.2
  - aria
  - screen-reader
  - keyboard-navigation
  - color-contrast
  - semantic-html
  - axe-core
  - pa11y
  - lighthouse
  - ada-compliance
  - section-508
version: 1.0.0
owner: cognitive-toolworks
license: Apache-2.0
security:
  secrets: "N/A"
  compliance: "WCAG 2.2 (Oct 2023), ADA, Section 508, ARIA 1.3, EN 301 549"
links:
  - title: "WCAG 2.2 - What's New"
    url: "https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/"
    accessed: "2025-10-26"
  - title: "ARIA 1.3 Specification"
    url: "https://w3c.github.io/aria/"
    accessed: "2025-10-26"
  - title: "axe-core GitHub"
    url: "https://github.com/dequelabs/axe-core"
    accessed: "2025-10-26"
  - title: "Pa11y Documentation"
    url: "https://pa11y.org/"
    accessed: "2025-10-26"
  - title: "WebAIM: Contrast and Color Accessibility"
    url: "https://webaim.org/articles/contrast/"
    accessed: "2025-10-26"
---

## Purpose & When-To-Use

**Purpose:** Validate web application accessibility against WCAG 2.2 standards (released October 2023) using automated testing (axe-core, Pa11y, Lighthouse) and manual verification for keyboard navigation, screen reader compatibility, color contrast (4.5:1 for AA, 7:1 for AAA), ARIA attributes, semantic HTML, and the 9 new WCAG 2.2 success criteria (focus visibility, target sizing, accessible authentication, redundant entry).

**When to Use:**
- You need to **validate WCAG 2.2 compliance** for legal requirements (ADA, Section 508, EN 301 549).
- You're implementing **accessible components** (forms, modals, carousels, data tables) and need validation.
- You require **automated accessibility testing** in CI/CD pipelines (axe-core, Pa11y-ci).
- You're **auditing existing sites** for accessibility violations before remediation.
- You need **color contrast analysis** to meet 4.5:1 (AA) or 7:1 (AAA) ratios.
- You're validating **keyboard navigation** (tab order, focus indicators, skip links).
- You're ensuring **screen reader compatibility** (NVDA, JAWS, VoiceOver, ORCA).
- You're implementing **WCAG 2.2 new criteria** (Focus Not Obscured, Target Size, Accessible Authentication).

**Complements:**
- `frontend-designsystem-validator`: Validates design tokens, component consistency; this validates runtime accessibility.
- `testing-accessibility-automation`: Integrates axe-core/Pa11y into CI/CD; this provides audit reports and recommendations.
- `frontend-performance-optimizer`: Validates Core Web Vitals; this validates a11y (both are Lighthouse metrics).

## Pre-Checks

**Mandatory Inputs:**
- `web_pages`: At least one URL or HTML file to validate.

**Validation Steps:**
1. **Compute NOW_ET** using NIST time.gov semantics (America/New_York, ISO-8601) for timestamp anchoring.
2. **Check web_pages accessibility:** Verify URLs return 200 OK or HTML files exist.
3. **Validate wcag_level:** If specified, must be "A", "AA", or "AAA". Default: AA (most common legal requirement).
4. **Check automated_tools availability:** If specified, verify axe-core, Pa11y, or Lighthouse are installed.
5. **Abort if:**
   - Zero web pages provided.
   - URLs return 404 or HTML files don't exist.
   - wcag_level is invalid (not A, AA, or AAA).

## Procedure

### T1: Quick Automated Accessibility Scan (≤2k tokens, 80% use case)

**Goal:** Run automated accessibility testing on a single page using axe-core to detect ~57% of issues with zero false positives.

**Steps:**
1. **Select primary page:** Choose the most critical page (e.g., homepage, checkout form).
2. **Run axe-core scan:**
   ```bash
   npx axe-core <URL>
   # Or use browser extension: Axe DevTools in Chrome/Firefox
   ```
3. **Analyze results:**
   - **Violations:** Issues that fail WCAG (e.g., missing alt text, insufficient contrast).
   - **Incomplete:** Items needing manual review (e.g., "Ensure this link text is descriptive").
   - **Passes:** Successfully validated checks.
4. **Categorize by WCAG level:**
   - Level A (critical): Missing form labels, keyboard traps, non-text contrast.
   - Level AA (standard): Color contrast <4.5:1, missing focus indicators.
   - Level AAA (enhanced): Color contrast <7:1, enhanced focus appearance.
5. **Generate summary:**
   - Total violations: X
   - Critical (Level A): Y
   - Needs Review (Incomplete): Z
   - Automated detection rate: ~57% (axe-core detects 57% of all WCAG issues)
6. **Output:** Violation list with WCAG references, severity (critical/serious/moderate/minor), and remediation steps.

**Token Budget:** ≤2k tokens (single page, automated scan only).

### T2: Comprehensive WCAG 2.2 Compliance Audit (≤6k tokens)

**Goal:** Validate multiple pages against WCAG 2.2 Level AA with automated testing (axe-core + Pa11y) and manual checks for keyboard navigation, screen reader, and new WCAG 2.2 criteria.

**Steps:**
1. **Run multi-tool automated scan:**
   - **axe-core:** `npx @axe-core/cli <URL>` (57% detection, zero false positives).
   - **Pa11y:** `npx pa11y <URL>` (uses axe-core or HTML_CodeSniffer engine).
   - **Lighthouse:** `lighthouse <URL> --only-categories=accessibility` (uses axe-core, provides 0-100 score).
   - **Combined detection:** axe + Pa11y catch ~35% of issues together (not 57% + 57% due to overlap).
2. **Validate WCAG 2.2 new success criteria (9 new):**
   - **2.4.11 Focus Not Obscured (Minimum) - AA:** When element receives focus, at least part is visible (not hidden by sticky headers, modals).
   - **2.4.12 Focus Not Obscured (Enhanced) - AAA:** Focus is never fully hidden.
   - **2.4.13 Focus Appearance - AAA:** Focus indicator ≥3:1 contrast against adjacent colors, size ≥ perimeter of focused element.
   - **2.5.7 Dragging Movements - AA:** Provide alternatives to drag-and-drop (double-tap, buttons).
   - **2.5.8 Target Size (Minimum) - AA:** Touch targets ≥24×24 CSS pixels (except inline text links, controlled by user agent).
   - **3.2.6 Consistent Help - A:** Help mechanisms (contact, chat) in consistent order across pages.
   - **3.3.7 Redundant Entry - A:** Auto-populate previously entered data (e.g., shipping = billing).
   - **3.3.8 Accessible Authentication (Minimum) - AA:** Don't require cognitive function tests (CAPTCHA alternatives, SMS code paste, password managers).
   - **3.3.9 Accessible Authentication (Enhanced) - AAA:** No cognitive tests at all (biometric, token-based).
3. **Manual keyboard navigation testing:**
   - **Tab order:** Logical, follows visual flow, no keyboard traps.
   - **Focus indicators:** Visible (not `outline: 0`), ≥3:1 contrast, size adequate.
   - **Skip links:** "Skip to main content" link present, functional.
   - **Modal dialogs:** Focus trapped, Esc closes, focus returns to trigger on close.
   - **Dropdown menus:** Arrow keys navigate, Enter/Space selects, Esc closes.
4. **Color contrast validation:**
   - **Normal text:** ≥4.5:1 (AA), ≥7:1 (AAA).
   - **Large text (18pt or 14pt bold):** ≥3:1 (AA), ≥4.5:1 (AAA).
   - **UI components (buttons, form borders):** ≥3:1 (AA).
   - **Focus indicators:** ≥3:1 against adjacent colors (WCAG 2.4.13).
   - **Tools:** WebAIM Contrast Checker, Chrome DevTools Contrast Ratio.
5. **ARIA validation:**
   - **Landmarks:** `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>` or `role="main"`, `role="navigation"`.
   - **Widget roles:** `role="button"`, `role="tab"`, `role="dialog"` with required states (`aria-expanded`, `aria-selected`).
   - **Live regions:** `aria-live="polite"` for status messages, `aria-live="assertive"` for errors.
   - **Labels:** `aria-label` or `aria-labelledby` for all interactive elements without visible labels.
   - **First rule of ARIA:** Use semantic HTML first (`<button>` instead of `<div role="button">`).
6. **Semantic HTML validation:**
   - **Heading hierarchy:** No skipped levels (h1 → h2 → h3, not h1 → h3).
   - **Form labels:** Every `<input>`, `<textarea>`, `<select>` has `<label for="id">` or `aria-label`.
   - **Alt text:** All `<img>` have `alt` attribute (empty `alt=""` for decorative images).
   - **Tables:** `<th scope="col|row">` for data tables, `<caption>` for table description.
7. **Screen reader testing (sample):**
   - **NVDA (Windows):** Test 1 critical page (e.g., checkout form).
   - **VoiceOver (macOS):** Test landmark navigation (Cmd+Opt+U for rotor).
   - **Mobile screen readers:** TalkBack (Android), VoiceOver (iOS) for touch target sizing.
8. **Generate comprehensive report:**
   - WCAG 2.2 compliance: X% (by level A, AA, AAA).
   - Violations by severity: Critical (A), Serious (AA), Moderate (AAA).
   - Automated findings: axe (57%), Pa11y (35% combined), Lighthouse score (0-100).
   - Manual findings: Keyboard nav issues, screen reader issues, contrast failures.
   - Remediation plan: Priority 1 (Level A), Priority 2 (AA), Priority 3 (AAA).
9. **Output:**
   - WCAG 2.2 compliance report (by success criterion: pass/fail/needs review).
   - Violation list with WCAG reference, severity, impact, remediation.
   - Color contrast report (all text/component pairs with ratios).
   - ARIA issues (missing labels, incorrect roles, invalid states).
   - Manual test checklist (keyboard, screen reader, touch targets).

**Token Budget:** ≤6k tokens (multi-page, multi-tool, manual checks, WCAG 2.2 new criteria).

### T3: Enterprise Accessibility Audit with Remediation Plan (≤12k tokens)

**Goal:** Perform a full enterprise accessibility audit across multiple pages/templates with automated testing in CI/CD, manual testing across screen readers/browsers, and a prioritized remediation roadmap.

**Steps:**
1. **Inventory pages and templates:**
   - Identify page types: Homepage, product listing, product detail, checkout, account, search results.
   - Map WCAG success criteria to pages (e.g., 3.3.7 Redundant Entry applies to multi-step forms).
2. **Set up automated CI/CD testing:**
   - **axe-core in Jest/Cypress:**
     ```javascript
     import { axe, toHaveNoViolations } from 'jest-axe';
     expect.extend(toHaveNoViolations);
     it('should have no accessibility violations', async () => {
       const { container } = render(<MyComponent />);
       const results = await axe(container);
       expect(results).toHaveNoViolations();
     });
     ```
   - **Pa11y-ci in CI pipeline:**
     ```json
     {
       "urls": ["http://localhost:3000", "http://localhost:3000/products"],
       "defaults": {"timeout": 5000, "wait": 500, "runners": ["axe"]},
       "threshold": 0
     }
     ```
   - **Lighthouse CI:**
     ```bash
     lhci autorun --collect.url=http://localhost:3000 --assert.assertions.accessibility=0.95
     ```
3. **Comprehensive manual testing:**
   - **Keyboard navigation:** Test all interactive elements on all page types.
   - **Screen readers:** NVDA (Windows), JAWS (Windows enterprise), VoiceOver (macOS/iOS), ORCA (Linux), TalkBack (Android).
   - **Browser matrix:** Chrome, Firefox, Safari, Edge (all with latest screen readers).
   - **Zoom testing:** 200% zoom (WCAG 1.4.4 Resize Text), 400% zoom (WCAG 1.4.10 Reflow).
   - **Mobile:** Touch target sizing (≥24×24 CSS pixels), orientation (portrait/landscape).
4. **WCAG 2.2 full compliance matrix:**
   - Create spreadsheet with all success criteria (78 total: 30 Level A, 24 Level AA, 24 Level AAA).
   - Mark status for each: Pass, Fail, Not Applicable, Needs Review.
   - Include evidence: Automated test pass, manual test pass, screenshot, code snippet.
5. **Advanced ARIA patterns:**
   - **Disclosure widgets (accordions):** `aria-expanded` toggles, focus management.
   - **Tab panels:** `role="tablist"`, `aria-selected`, arrow key navigation.
   - **Carousels:** `aria-live` for auto-advance, pause button, keyboard nav.
   - **Data tables:** `aria-sort`, `aria-rowcount`, `aria-colcount` for virtualized tables.
   - **Toast notifications:** `aria-live="polite"`, auto-dismiss with manual dismiss option.
6. **Color and visual design validation:**
   - **Contrast analysis:** Scan all color combinations (text/background, button/background, link/background).
   - **Non-color information:** Ensure error states not indicated by color alone (use icons, text).
   - **Focus indicators:** Test on all backgrounds (light, dark, images) for 3:1 contrast.
7. **Form accessibility deep dive:**
   - **Labels:** Explicit `<label for>` or `aria-labelledby`, not placeholder-only.
   - **Fieldsets:** `<fieldset>` + `<legend>` for radio/checkbox groups.
   - **Error messages:** `aria-invalid="true"`, `aria-describedby` linking to error, inline + summary.
   - **Required fields:** `required` attribute + `aria-required="true"` + visual indicator (not color only).
   - **Autocomplete:** `autocomplete` attributes for user data (name, email, address).
8. **Document accessibility (if applicable):**
   - **PDFs:** Tagged PDFs, logical reading order, alt text for images.
   - **Office docs:** Proper heading structure, alt text, accessible tables.
   - **ARIA in PDFs:** Use PDF/UA (ISO 14289) standard.
9. **Assistive technology compatibility matrix:**
   - Test combinations: NVDA + Chrome, JAWS + Edge, VoiceOver + Safari, ORCA + Firefox.
   - Document known issues (e.g., "JAWS 2024 doesn't announce `aria-describedby` on Safari").
10. **Generate remediation roadmap:**
    - **Phase 1 (0-30 days):** Level A violations (blocking, highest priority).
    - **Phase 2 (30-60 days):** Level AA violations (legal requirement for most jurisdictions).
    - **Phase 3 (60-90 days):** Level AAA violations (enhanced accessibility, competitive advantage).
    - **Quick wins:** Low-effort, high-impact fixes (missing alt text, form labels, heading order).
    - **Complex fixes:** High-effort items (keyboard trap refactor, custom widget ARIA).
11. **Ongoing monitoring:**
    - Automated tests run on every PR (axe-core, Pa11y-ci).
    - Monthly accessibility audits (sample of key pages).
    - Annual comprehensive audit (all pages, all screen readers).
12. **Output:**
    - WCAG 2.2 full compliance matrix (78 success criteria × pages).
    - Violation inventory by severity, page, and WCAG criterion.
    - Automated test integration guide (CI/CD setup, failure thresholds).
    - Manual testing guide (keyboard, screen reader, browser matrix).
    - Remediation roadmap (3 phases, effort estimates, owner assignments).
    - Accessibility statement (public-facing compliance documentation).

**Token Budget:** ≤12k tokens (enterprise audit, CI/CD setup, full manual testing, remediation roadmap).

## Decision Rules

**Ambiguity Resolution:**
1. **If `wcag_level` not specified:**
   - Default to **Level AA** (industry standard, legal requirement in US/EU).
   - Emit note: "Validating against WCAG 2.2 Level AA. Use Level AAA for enhanced accessibility."
2. **If `automated_tools` not specified:**
   - Default to **axe-core** (highest detection rate 57%, zero false positives).
   - Emit note: "Using axe-core. Consider Pa11y for alternative engine or Lighthouse for scoring."
3. **If `manual_checks` not specified:**
   - Default to **true** for T2/T3 (automated tools only catch 35-57% of issues).
   - Emit note: "Manual testing required. Automated tools detect ~57% of WCAG issues."
4. **If color contrast is borderline (e.g., 4.49:1):**
   - Mark as **fail** (be conservative; 4.5:1 is minimum, not target).
   - Suggest: "Increase to 4.6:1 or higher for safety margin."
5. **If `aria-label` conflicts with visible text:**
   - Prefer **visible text + aria-labelledby** over aria-label (WCAG 2.5.3 Label in Name).
   - Emit warning: "aria-label 'Submit Form' conflicts with visible 'Send'. Use 'Send' in aria-label."

**Stop Conditions:**
- **Zero pages accessible:** All URLs return 404 or HTML files don't exist → abort with error.
- **WCAG level invalid:** User specifies "Level B" → abort with error: "WCAG levels are A, AA, or AAA."
- **Critical Level A failures:** If >10 Level A violations → emit warning: "Site is not minimally accessible. Prioritize Level A fixes immediately."

**Thresholds:**
- **Color contrast:**
  - AA normal text: ≥4.5:1
  - AA large text: ≥3:1
  - AAA normal text: ≥7:1
  - AAA large text: ≥4.5:1
  - UI components/focus: ≥3:1
- **Touch targets:** ≥24×24 CSS pixels (WCAG 2.5.8), ≥44×44 pixels recommended (iOS HIG, Material Design).
- **Focus indicator:** ≥3:1 contrast, ≥2px outline or equivalent area (WCAG 2.4.13 AAA).
- **Lighthouse score:** <90 = needs improvement, 90-94 = good, 95-100 = excellent.

## Output Contract

**Required Fields:**

```typescript
{
  wcag_compliance_report: {
    level: "A" | "AA" | "AAA";
    overall_status: "pass" | "fail" | "needs_review";
    success_criteria: Array<{
      id: string;              // 1.1.1, 2.4.11, 3.3.7, etc.
      name: string;            // Non-text Content, Focus Not Obscured, Redundant Entry
      level: "A" | "AA" | "AAA";
      status: "pass" | "fail" | "not_applicable" | "needs_review";
      automated: boolean;      // True if automated tools can detect
      evidence: string;        // "axe-core passed", "Manual test: keyboard nav OK"
      new_in_22: boolean;      // True for 9 new WCAG 2.2 criteria
    }>;
    compliance_percentage: {
      level_a: number;         // % of Level A criteria passing
      level_aa: number;
      level_aaa: number;
    };
  };
  violations: Array<{
    id: string;                // axe-rule-id or wcag-criterion
    wcag_criterion: string;    // 1.4.3 Contrast (Minimum)
    level: "A" | "AA" | "AAA";
    severity: "critical" | "serious" | "moderate" | "minor";
    impact: string;            // "Users with low vision cannot read text"
    element: string;           // CSS selector or HTML snippet
    remediation: string;       // "Increase contrast to 4.6:1 by darkening text"
    page_url: string;
  }>;
  automated_test_results: {
    axe_core: {
      violations: number;
      incomplete: number;      // Needs manual review
      passes: number;
      detection_rate: "~57%";  // axe detects 57% of WCAG issues
    };
    pa11y?: {
      errors: number;
      warnings: number;
      engine: "axe" | "htmlcs";
    };
    lighthouse?: {
      score: number;           // 0-100
      audits_passed: number;
      audits_failed: number;
    };
  };
  manual_test_checklist: Array<{
    category: "keyboard" | "screen_reader" | "color_contrast" | "aria" | "semantic_html" | "touch_targets";
    item: string;              // "Tab order is logical"
    status: "pass" | "fail" | "not_tested";
    notes?: string;
  }>;
  aria_issues: Array<{
    element: string;
    issue: string;             // "Missing aria-label on button"
    recommendation: string;    // "Add aria-label='Close dialog'"
  }>;
  color_contrast_report: {
    failures: Array<{
      foreground: string;      // #333333
      background: string;      // #CCCCCC
      ratio: number;           // 2.8
      required: number;        // 4.5 (for AA normal text)
      element: string;
      location: string;        // "Homepage, product title"
    }>;
    summary: {
      total_checks: number;
      failures: number;
      aa_compliant: boolean;
      aaa_compliant: boolean;
    };
  };
}
```

**Optional Fields:**
- `screen_reader_results`: Object with findings from NVDA, JAWS, VoiceOver testing.
- `remediation_roadmap`: Array of phases (Phase 1/2/3) with effort estimates and priorities.
- `ci_cd_integration`: Object with axe-core, Pa11y-ci, Lighthouse CI setup examples.
- `accessibility_statement`: Markdown template for public compliance statement.

**Format:** JSON for structured data, Markdown for remediation plan and manual checklist.

## Examples

### Example 1: E-commerce Checkout Accessibility Audit (T2)

**Input:**
```yaml
web_pages:
  - "https://example.com/checkout"
wcag_level: "AA"
automated_tools: ["axe-core", "Pa11y"]
manual_checks: true
```

**Output (T2 Summary):**
```yaml
WCAG 2.2 Level AA Compliance: 78% (45/58 success criteria passing)
Automated Tests:
  axe-core: 12 violations, 3 incomplete, 87 passes (57% detection rate)
  Pa11y: 15 errors, 8 warnings (using axe engine)
Manual Tests:
  Keyboard: ✅ Tab order logical, ⚠️ Focus indicator low contrast (2.2:1, need 3:1)
  Screen Reader (NVDA): ⚠️ Error messages not announced (missing aria-live)
Top Violations:
  1. Color Contrast (1.4.3, AA): 8 failures (text 3.1:1, need 4.5:1) - CRITICAL
  2. Form Labels (3.3.2, A): 3 inputs missing labels - CRITICAL
  3. Focus Visible (2.4.7, AA): Focus indicator contrast 2.2:1 (need 3:1) - SERIOUS
  4. Accessible Auth (3.3.8, AA): CAPTCHA has no alternative - SERIOUS (NEW in 2.2)
  5. Target Size (2.5.8, AA): "Edit" button 20×20px (need 24×24px) - MODERATE (NEW in 2.2)
Remediation Priority:
  Phase 1 (7 days): Fix Level A violations (form labels, keyboard traps)
  Phase 2 (14 days): Fix AA violations (contrast, focus indicators, CAPTCHA alternative)
```

**Link to Full Example:** See `skills/frontend-accessibility-validator/examples/ecommerce-checkout-audit.txt`

### Example 2: WCAG 2.2 New Criteria Validation (T2 Snippet)

**WCAG 2.2 New Success Criteria Status:**
```yaml
2.4.11 Focus Not Obscured (Minimum) - AA: ⚠️ FAIL
  Issue: Sticky header hides focused button when tabbing
  Fix: Adjust scroll position or reduce header height
2.5.8 Target Size (Minimum) - AA: ⚠️ FAIL
  Issue: Mobile menu icons 18×18px (need 24×24px)
  Fix: Increase touch targets to 24×24px minimum
3.3.7 Redundant Entry - A: ✅ PASS
  Evidence: Shipping address auto-fills to billing address
3.3.8 Accessible Authentication (Minimum) - AA: ⚠️ FAIL
  Issue: CAPTCHA with no alternative (audio, SMS, email)
  Fix: Add audio CAPTCHA or SMS verification option
```

## Quality Gates

**Token Budget Compliance:**
- T1 output ≤2k tokens (single page, axe-core only).
- T2 output ≤6k tokens (multi-page, multi-tool, manual checks).
- T3 output ≤12k tokens (enterprise audit, CI/CD, remediation roadmap).

**Validation Checklist:**
- [ ] All WCAG 2.2 Level AA success criteria evaluated (58 total: 30 A + 24 AA + 4 AA removed from prior).
- [ ] Automated tests run (axe-core minimum, Pa11y/Lighthouse optional).
- [ ] Manual keyboard testing performed (tab order, focus indicators, skip links).
- [ ] Color contrast checked for all text/component pairs (4.5:1 AA, 7:1 AAA).
- [ ] ARIA attributes validated (landmarks, labels, live regions, widget roles).
- [ ] Semantic HTML verified (headings, labels, alt text, tables).
- [ ] WCAG 2.2 new criteria assessed (9 new success criteria).
- [ ] Violations categorized by severity (critical/serious/moderate/minor).
- [ ] Remediation plan provided with effort estimates.

**Safety & Auditability:**
- **No PII in reports:** Redact user data if testing production sites with real accounts.
- **Evidence preservation:** Screenshot violations, save axe/Pa11y JSON reports for audit trail.
- **Version tracking:** Document WCAG version (2.2), tool versions (axe-core 4.x, Pa11y 8.x), test date.

**Determinism:**
- **Consistent thresholds:** 4.5:1 for AA text, 7:1 for AAA, 3:1 for components (no "approximately").
- **Reproducible tests:** Automated tests produce same results on same HTML (no flakiness).

## Resources

**Official Standards:**
- [WCAG 2.2 - What's New](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) (accessed 2025-10-26)
  - 9 new success criteria, 1 removed (4.1.1 Parsing).
- [ARIA 1.3 Specification](https://w3c.github.io/aria/) (accessed 2025-10-26)
  - Roles, states, properties for accessible widgets.
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
  - All 78 success criteria with techniques and failures.

**Automated Testing Tools:**
- [axe-core GitHub](https://github.com/dequelabs/axe-core) (accessed 2025-10-26)
  - 57% detection rate, zero false positives, integrates with Jest, Cypress, Playwright.
- [Pa11y Documentation](https://pa11y.org/) (accessed 2025-10-26)
  - CLI and CI-friendly, uses axe or HTML_CodeSniffer.
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
  - Accessibility score (0-100), uses axe-core, Chrome DevTools integration.

**Color Contrast:**
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
  - Check foreground/background pairs for AA/AAA compliance.
- [WebAIM: Contrast and Color Accessibility](https://webaim.org/articles/contrast/) (accessed 2025-10-26)
  - 4.5:1 AA normal, 3:1 AA large, 7:1 AAA normal, 4.5:1 AAA large.

**Screen Readers:**
- [NVDA (Windows)](https://www.nvaccess.org/) - Free, most popular.
- [JAWS (Windows)](https://www.freedomscientific.com/products/software/jaws/) - Enterprise standard.
- [VoiceOver (macOS/iOS)](https://www.apple.com/accessibility/voiceover/) - Built-in.
- [ORCA (Linux)](https://help.gnome.org/users/orca/stable/) - GNOME default.

**Complementary Skills:**
- `frontend-designsystem-validator`: Validates design tokens, component library consistency.
- `testing-accessibility-automation`: Integrates axe-core/Pa11y into CI/CD pipelines.
- `frontend-performance-optimizer`: Validates Core Web Vitals (LCP, FID, CLS) alongside accessibility.
