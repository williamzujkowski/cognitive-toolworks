# Startup MVP Design System (Orchestrated Example)

## Brand Context
- **Company:** TaskFlow (productivity SaaS startup)
- **Brand Colors:** Blue primary (#007AFF), Purple accent (#5856D6)
- **Typography:** Inter font family
- **Target:** Web application (responsive)
- **Maturity:** Startup (MVP design system)

## Orchestration Plan

### Phase 1: Foundation (1 day)

**Design Tokens Defined:**

```yaml
# Color Tokens (8 total)
color-primary: "#007AFF"           # Brand blue
color-primary-hover: "#0051D5"     # Darker for hover states
color-secondary: "#5856D6"         # Accent purple
color-success: "#34C759"
color-error: "#FF3B30"
color-text: "#1C1C1E"
color-background: "#FFFFFF"
color-border: "#C6C6C8"

# Typography Tokens
font-family-base: "'Inter', -apple-system, sans-serif"
font-size-sm: "14px"
font-size-base: "16px"
font-size-lg: "18px"
font-size-xl: "24px"
font-size-2xl: "32px"
line-height-base: 1.5

# Spacing Tokens (5-point scale)
spacing-xs: "4px"
spacing-sm: "8px"
spacing-md: "16px"
spacing-lg: "24px"
spacing-xl: "32px"

# Shadow Tokens
shadow-sm: "0 1px 2px rgba(0,0,0,0.05)"
shadow-md: "0 4px 6px rgba(0,0,0,0.1)"

# Border Radius Tokens
radius-sm: "4px"
radius-md: "8px"
```

### Phase 2: Components (3 days)

**Component Inventory (8 core components):**

**Atoms (4 components):**

1. **Button**
   - Variants: size (sm, md, lg), color (primary, secondary, danger), style (solid, outline, ghost)
   - States: default, hover, focus, active, disabled, loading
   - Accessibility: 4.52:1 contrast, keyboard accessible, 44px touch target

2. **Input**
   - Variants: size (sm, md, lg), type (text, email, password, number)
   - States: default, focus, error, disabled
   - Accessibility: Associated label, error message announced, focus visible

3. **Label**
   - Variants: size (sm, md), required indicator
   - Associated with form inputs via htmlFor

4. **Badge**
   - Variants: color (primary, success, error, neutral), size (sm, md)
   - Use: Status indicators, counts, labels

**Molecules (2 components):**

5. **Form Field**
   - Composition: Label + Input + Error Message
   - Handles label/input association, error state propagation
   - Accessibility: Complete field with proper ARIA attributes

6. **Card**
   - Composition: Container with shadow, padding, optional header/footer
   - Variants: elevation (flat, raised), padding (compact, default, spacious)
   - Use: Content grouping, dashboard widgets

**Organisms (2 components):**

7. **Modal**
   - Composition: Overlay + Dialog with Header, Body, Footer
   - Behavior: Focus trap, ESC to close, click outside to close
   - Accessibility: ARIA dialog role, focus management

8. **Navigation**
   - Composition: Logo + Nav Links + User Menu
   - Responsive: Mobile hamburger menu, desktop horizontal nav
   - Accessibility: Keyboard navigation, skip links

**Skill Invocations:**
```
invoke ux-wireframe-designer for Button:
  - Generated wireframes for 3 sizes × 4 colors × 3 styles = 36 variants
  - All 6 states documented with hex color values
  - Accessibility: 4.52:1 contrast ratio validated
  - Touch targets: 32px (sm), 40px (md), 48px (lg) ✅ mobile guidelines

invoke ux-wireframe-designer for Form Field:
  - Generated composition pattern (Label above Input, Error below)
  - Error state: Red border + error icon + message
  - Focus state: Blue border + focus ring
  - Layout responsive: full-width on mobile, max-width on desktop
```

### Phase 3: Validation (1 day)

**Accessibility Audit (frontend-designsystem-validator):**

```
invoke frontend-designsystem-validator:
  - WCAG 2.1 AA compliance: 100% (all components pass)
  - Contrast ratios:
    - Button primary (white on #007AFF): 4.52:1 ✅
    - Text on background (black on white): 21:1 ✅
    - Border contrast (gray on white): 3.4:1 ✅
  - Keyboard navigation: All interactive elements accessible ✅
  - Focus indicators: 2px blue ring on all components ✅
  - Screen reader: ARIA labels present on complex components (Modal, Nav) ✅
```

**Consistency Check:**
- Token usage: 100% (no hard-coded colors/spacing)
- Naming conventions: Consistent kebab-case for tokens, PascalCase for components
- State coverage: All components define hover, focus, disabled states
- Documentation: All 8 components have usage guidelines ✅

### Phase 4: Integration (2 days)

**Documentation Site:**
- Platform: Storybook (interactive component playground)
- Sections:
  - Getting Started (installation, quick start)
  - Design Tokens (color, typography, spacing reference)
  - Components (8 component pages with live examples)
- Deployed to: taskflow-design-system.netlify.app

**React Component Library:**
```
@taskflow/design-system (NPM package)

Package structure:
src/
  tokens/
    colors.ts  # Export design tokens as CSS variables
    typography.ts
    spacing.ts
  components/
    Button/
      Button.tsx
      Button.module.css
      Button.test.tsx
      Button.stories.tsx
    Input/
      ...
  index.ts  # Public exports

Usage:
import { Button, Input, FormField } from '@taskflow/design-system';
import '@taskflow/design-system/dist/styles.css';

<Button size="md" color="primary">Get Started</Button>
```

**Framework Integration (frontend-framework-advisor):**
```
invoke frontend-framework-advisor:
  - Recommended: React (team already using React)
  - Package: NPM library with CSS Modules
  - Build: Rollup for tree-shaking
  - TypeScript: Full type definitions
  - Testing: Jest + React Testing Library
```

## Results

**Deliverables:**
- Design token system (8 colors, 5 spacing values, 2 shadows)
- 8 component specifications with full documentation
- React component library (@taskflow/design-system v1.0.0)
- Storybook documentation site (deployed)
- Migration guide for existing TaskFlow app

**Metrics:**
- Accessibility: 100% WCAG 2.1 AA compliance
- Token coverage: 100% (no hard-coded values)
- Documentation: 100% (all components documented)
- Component count: 8 (sufficient for MVP)

**Timeline:**
- Day 1: Foundation (design tokens)
- Days 2-4: Components (8 components designed and specified)
- Day 5: Validation (accessibility audit, consistency check)
- Days 6-7: Integration (React library, Storybook, deployment)

**Total:** 7 days from kickoff to production-ready design system

## Adoption Plan

**Phase 1: Pilot (Week 1):**
- Integrate design system into 2 pages (Login, Dashboard)
- Replace existing custom buttons/inputs with design system components
- Measure impact: 40% reduction in CSS, consistent UI

**Phase 2: Rollout (Weeks 2-4):**
- Migrate remaining pages to design system
- Train team on component usage and contribution
- Establish design system office hours

**Phase 3: Evolution (Month 2+):**
- Add 5 new components based on product needs (Tooltip, Dropdown, Tabs, Alert, Breadcrumb)
- Introduce dark mode theme
- Expand to mobile app (React Native library)
