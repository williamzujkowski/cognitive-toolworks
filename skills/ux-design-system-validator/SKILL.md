---
name: UX Design System Validator
slug: ux-design-system-validator
description: Validate design systems for accessibility (WCAG), responsive design, and component consistency with design token analysis.
capabilities:
  - WCAG 2.2 AA/AAA compliance validation
  - Responsive design pattern verification
  - Design token consistency audit
  - Component library accessibility checks
  - Design system governance assessment
inputs:
  - design_system_url: URL or path to design system documentation
  - component_library: Component source code or Figma/Sketch files
  - design_tokens: JSON/YAML design token definitions
  - target_wcag_level: AA or AAA (default AA)
  - platforms: Array of target platforms (web, iOS, Android, etc.)
outputs:
  - validation_report: Structured JSON with findings by category
  - wcag_violations: Array of accessibility issues with severity
  - token_inconsistencies: Mismatches in design token usage
  - remediation_plan: Prioritized action items with references
  - compliance_score: Numerical score (0-100) per dimension
keywords:
  - accessibility
  - WCAG
  - design-systems
  - responsive-design
  - design-tokens
  - component-library
  - a11y
  - UX
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: Public; no PII or credentials required
links:
  - https://w3.org/WAI/WCAG22
  - https://m3.material.io
  - https://developer.apple.com/design/human-interface-guidelines
  - https://designsystemsrepo.com
---

## Purpose & When-To-Use

**Trigger conditions:**
- Design system audit or compliance review requested
- WCAG 2.2 AA/AAA compliance verification needed before launch
- Component library validation for accessibility and consistency
- Responsive design breakpoint review across devices
- Design token governance assessment
- Preparation for European Accessibility Act (EAA) 2025 compliance

**Use this skill when:**
- You need to validate that a design system meets accessibility standards
- Component libraries require consistency checks across platforms
- Design tokens need validation against brand guidelines
- Responsive design patterns must work across breakpoints
- Cross-platform design systems (web, iOS, Android) need alignment

**Do NOT use when:**
- Only generating new designs (use design tools instead)
- Conducting user research or usability testing
- Implementing code (this validates design artifacts, not implementation)

## Pre-Checks

**Time normalization:**
```
NOW_ET = 2025-10-25T21:30:36-04:00 (NIST/time.gov semantics)
```

**Required inputs validation:**
1. At least one of: `design_system_url`, `component_library`, or `design_tokens` must be provided
2. If `target_wcag_level` specified, must be "AA" or "AAA"
3. If `platforms` array provided, validate against supported platforms: [web, iOS, Android, react-native, flutter]

**Source freshness checks:**
- WCAG 2.2 is current standard (released October 2023, accessed 2025-10-25)
- Material Design 3 Expressive is latest version (2025, accessed 2025-10-25)
- Apple HIG unified guidelines current (2025 Liquid Glass update, accessed 2025-10-25)
- W3C Design Tokens Community Group spec is active standard (accessed 2025-10-25)

**Abort conditions:**
- No design artifacts provided for validation
- Design system format is proprietary and cannot be parsed
- Requested WCAG level is invalid

## Procedure

### T1: Quick Accessibility & Token Scan (≤2k tokens)

**Fast-path for 80% of cases: basic WCAG and token checks**

1. **Parse design artifacts:**
   - Extract component definitions from provided source
   - Load design tokens (JSON/YAML) if available
   - Identify platform-specific guidelines (Material/HIG/custom)

2. **Run automated WCAG 2.2 Level AA checks:**
   - Color contrast ratios (1.4.3 Contrast Minimum: 4.5:1 text, 3:1 large text)
   - Focus indicators (2.4.7 Focus Visible, 2.4.11 Focus Not Obscured Minimum)
   - Touch target sizes (2.5.8 Target Size Minimum: 24x24 CSS pixels)
   - Text spacing (1.4.12 Text Spacing)
   - Dragging alternatives (2.5.7 Dragging Movements)

3. **Design token consistency scan:**
   - Verify token naming follows W3C spec (color, dimension, number, typography)
   - Check for conflicting token values across files
   - Validate semantic token references (e.g., `color.button.primary` references `color.brand.blue`)

4. **Generate quick report:**
   - Critical violations (blockers for AA compliance)
   - Token inconsistencies count
   - Compliance score estimate
   - Top 3 remediation priorities

**Output:** JSON summary with violation counts and quick-win recommendations.

**Decision point:** If critical violations > 5 OR user requests comprehensive audit → proceed to T2.

### T2: Extended Design System Validation (≤6k tokens)

**Includes T1 + responsive design + component library audit + design token validation**

5. **Responsive design pattern analysis:**
   - Verify breakpoints follow industry standards (320px, 768px, 1024px, 1440px)
   - Check fluid typography scales (1rem base, 1.25 scale ratio)
   - Validate touch-friendly controls across devices (min 44x44 iOS, 48x48 Material)
   - Test grid system consistency (12-column, 8pt/4pt spacing grid)
   - Review viewport meta tags and fluid layout patterns

6. **Component library deep audit:**
   - **Buttons:** States (default, hover, focus, active, disabled), ARIA labels, keyboard navigation
   - **Forms:** Labels, error messages, required field indicators, autocomplete attributes
   - **Navigation:** Skip links, landmark roles, breadcrumb semantics
   - **Modals/Dialogs:** Focus trapping, ESC key handling, ARIA roles (dialog, alertdialog)
   - **Images:** Alt text guidance, decorative vs informative classification
   - Cross-reference against Material Design 3 and Apple HIG patterns (accessed 2025-10-25)

7. **Design token validation (W3C spec compliance):**
   - **Type validation:** Ensure color tokens use hex/rgb/hsl, dimensions use px/rem/em
   - **Semantic layering:** Verify 3-tier structure (core → semantic → component)
   - **Accessibility tokens:** Check contrast tokens meet WCAG thresholds
   - **Documentation:** Validate each token has use-case and constraints
   - **Version control:** Confirm tokens are versioned and change-logged
   - Reference: W3C Design Tokens Community Group (accessed 2025-10-25)

8. **WCAG 2.2 Level AA comprehensive check:**
   - All 50 Level A criteria + 20 Level AA criteria
   - New 2.2 criteria: Focus Not Obscured (Minimum), Focus Appearance, Dragging Movements, Target Size (Minimum), Consistent Help, Redundant Entry, Accessible Authentication (Minimum)
   - Reference: WCAG 2.2 (https://w3.org/WAI/WCAG22, accessed 2025-10-25)

9. **Generate detailed remediation plan:**
   - Prioritize by impact (critical/high/medium/low)
   - Group by category (color, typography, layout, interaction)
   - Include code snippets or design token changes
   - Estimate effort (quick win / medium / complex)
   - Link to authoritative sources (WCAG, Material, HIG)

**Output:** Comprehensive validation report with prioritized remediation plan.

**Decision point:** If AAA compliance requested OR multi-platform alignment needed → optionally proceed to T3 (not implemented in this T2 skill).

### T3: Not implemented (skill is T2)

T3 would include: full AAA audit, automated testing integration, cross-platform design system federation, advanced token tooling recommendations.

## Decision Rules

**Ambiguity thresholds:**
- If color contrast is 4.4:1 (just below 4.5:1 threshold), flag as WARNING not ERROR
- If component has partial ARIA support, detail what's missing vs blanket fail
- If design tokens use custom naming (not W3C spec), flag as INFO not ERROR

**Severity classification:**
- **CRITICAL:** WCAG Level A violations (e.g., missing alt text, no keyboard access)
- **HIGH:** WCAG Level AA violations (e.g., contrast 3.5:1 for text, focus not visible)
- **MEDIUM:** Design token inconsistencies, non-standard breakpoints
- **LOW:** Documentation gaps, minor naming convention deviations
- **INFO:** Recommendations for AAA compliance, advanced patterns

**Abort/stop conditions:**
- Cannot parse design system format after 3 attempts → return error with format requirements
- Design system has 0 components defined → return error "No components found to validate"
- WCAG checks yield 0 results → likely parsing issue, return diagnostic report

## Output Contract

**Required fields (JSON schema):**
```json
{
  "validation_report": {
    "timestamp": "ISO-8601 timestamp",
    "wcag_level_tested": "AA | AAA",
    "overall_compliance_score": "0-100 integer",
    "dimensions": {
      "accessibility": {"score": 0-100, "violations": []},
      "responsive_design": {"score": 0-100, "issues": []},
      "design_tokens": {"score": 0-100, "inconsistencies": []},
      "component_library": {"score": 0-100, "findings": []}
    }
  },
  "wcag_violations": [
    {
      "criterion": "1.4.3 Contrast (Minimum)",
      "level": "AA",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "component": "Primary Button",
      "description": "Text contrast is 3.2:1, needs 4.5:1",
      "remediation": "Increase text color darkness or lighten background",
      "wcag_reference": "https://w3.org/WAI/WCAG22/Understanding/contrast-minimum"
    }
  ],
  "token_inconsistencies": [
    {
      "token_name": "color.button.primary",
      "issue": "Defined as #FF5733 in tokens.json but #FF5734 in components.css",
      "recommendation": "Synchronize to single source of truth"
    }
  ],
  "remediation_plan": {
    "quick_wins": ["Fix button contrast", "Add focus indicators"],
    "prioritized_actions": [
      {
        "priority": "CRITICAL | HIGH | MEDIUM | LOW",
        "category": "accessibility | responsive | tokens | components",
        "action": "Description of fix needed",
        "effort": "quick | medium | complex",
        "references": ["URL to WCAG/Material/HIG"]
      }
    ]
  }
}
```

**Types:**
- `validation_report`: Object (required)
- `wcag_violations`: Array of objects (required, may be empty)
- `token_inconsistencies`: Array of objects (required, may be empty)
- `remediation_plan`: Object (required)
- `compliance_score`: Integer 0-100 per dimension (required)

## Examples

**Example: Basic WCAG validation (T1)**

```json
INPUT:
{
  "design_system_url": "https://example.com/design-system",
  "target_wcag_level": "AA",
  "platforms": ["web"]
}

OUTPUT:
{
  "validation_report": {
    "timestamp": "2025-10-25T21:30:36-04:00",
    "wcag_level_tested": "AA",
    "overall_compliance_score": 72,
    "dimensions": {
      "accessibility": {"score": 65, "violations": 8}
    }
  },
  "wcag_violations": [
    {
      "criterion": "1.4.3 Contrast (Minimum)",
      "level": "AA",
      "severity": "HIGH",
      "component": "Secondary Button",
      "description": "Contrast ratio 3.8:1 (need 4.5:1)"
    }
  ],
  "remediation_plan": {
    "quick_wins": ["Darken secondary button text"]
  }
}
```

## Quality Gates

**Token budgets (enforced):**
- T1 procedure: ≤2000 tokens (quick scan + report generation)
- T2 procedure: ≤6000 tokens (comprehensive audit + detailed remediation)
- T3 procedure: Not implemented (would be ≤12000 tokens)

**Safety checks:**
- Do not execute code from design system; parse declaratively only
- Do not store PII from design artifacts
- Redact any API keys or secrets found in token files (flag as security issue)

**Auditability:**
- Log all WCAG criteria checked with timestamps
- Include source references (URL + access date) for every guideline cited
- Version design system artifacts analyzed (git SHA, file hash, or timestamp)

**Determinism:**
- Same design system input → same validation output (no randomness)
- WCAG criteria are deterministic (contrast calculation, token parsing)
- If using LLM for component classification, use temperature=0

**Quality metrics:**
- Validation must complete in <30 seconds for T1, <2 minutes for T2
- False positive rate <5% (manual spot-check 20 random findings)
- Coverage: All WCAG 2.2 Level AA criteria (70 total success criteria)

## Resources

**Standards and specifications:**
- WCAG 2.2 Guidelines: https://w3.org/WAI/WCAG22 (accessed 2025-10-25T21:30:36-04:00)
- WCAG 2.2 Understanding Docs: https://w3.org/WAI/WCAG22/Understanding (accessed 2025-10-25T21:30:36-04:00)
- W3C Design Tokens Community Group: https://github.com/design-tokens/community-group (accessed 2025-10-25T21:30:36-04:00)
- European Accessibility Act (EAA): https://ec.europa.eu/social/main.jsp?catId=1202 (accessed 2025-10-25T21:30:36-04:00)

**Design system references:**
- Material Design 3: https://m3.material.io (accessed 2025-10-25T21:30:36-04:00)
- Material Design 3 Expressive: https://m3.material.io/blog/material-3-expressive (accessed 2025-10-25T21:30:36-04:00)
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines (accessed 2025-10-25T21:30:36-04:00)
- Design Systems Repo: https://designsystemsrepo.com (accessed 2025-10-25T21:30:36-04:00)

**Tools and validators:**
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker (accessed 2025-10-25T21:30:36-04:00)
- axe DevTools: https://deque.com/axe/devtools (accessed 2025-10-25T21:30:36-04:00)
- Style Dictionary (design tokens): https://amzn.github.io/style-dictionary (accessed 2025-10-25T21:30:36-04:00)
- Figma Tokens Plugin: https://tokens.studio (accessed 2025-10-25T21:30:36-04:00)

**Additional reading:**
- WCAG 2.2 What's New: https://accessibe.com/blog/knowledgebase/wcag-two-point-two (accessed 2025-10-25T21:30:36-04:00)
- Design Tokens Best Practices 2025: https://howik.com/design-tokens-best-practices (accessed 2025-10-25T21:30:36-04:00)
