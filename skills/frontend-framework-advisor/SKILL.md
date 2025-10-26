---
name: "Frontend Framework Advisor"
slug: "frontend-framework-advisor"
description: "Guide React, Vue, and mobile (iOS/Android/React Native) development with component architecture, state management, and performance optimization patterns."
capabilities:
  - Component architecture design and hierarchy planning
  - State management pattern recommendations (Redux, Zustand, Pinia, Context)
  - Performance optimization (rendering, bundle size, lazy loading)
  - Cross-platform mobile strategy guidance (native vs hybrid)
  - Framework selection decision support
  - Platform-specific best practices (React hooks, Vue composition API, SwiftUI, Jetpack Compose)
  - Accessibility implementation (WCAG compliance)
  - Testing strategy integration (unit, component, e2e)
inputs:
  - platform: "react | vue | ios | android | react-native (string, required)"
  - project_type: "new | refactor | migration (string, required)"
  - tier: "T1 (quick guidance) | T2 (detailed architecture) (string, default: T1)"
  - state_complexity: "simple | moderate | complex (string, optional)"
  - performance_requirements: "standard | high-performance | low-bandwidth (string, optional)"
  - accessibility_level: "basic | WCAG-AA | WCAG-AAA (string, optional)"
outputs:
  - architecture_plan: "component hierarchy and file structure (object)"
  - state_management_recommendation: "recommended approach with rationale (object)"
  - performance_patterns: "optimization techniques and code patterns (array)"
  - platform_scaffolding: "starter templates and configuration (string)"
  - testing_integration: "test strategy aligned with testing-strategy-composer (object)"
keywords:
  - react
  - vue
  - ios
  - android
  - react-native
  - frontend-architecture
  - state-management
  - component-design
  - mobile-development
  - performance-optimization
  - swiftui
  - jetpack-compose
  - hooks
  - composition-api
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://react.dev/
  - https://vuejs.org/guide/
  - https://developer.apple.com/swift/
  - https://developer.android.com/kotlin
  - https://reactnative.dev/
  - https://developer.apple.com/design/human-interface-guidelines/
  - https://m3.material.io/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Designing component architecture for new frontend/mobile project
- Choosing between React, Vue, or mobile platforms (iOS/Android/React Native)
- Refactoring component hierarchy or state management approach
- Optimizing rendering performance or bundle size
- Planning cross-platform mobile strategy (native vs React Native)
- Implementing accessibility features (WCAG compliance)
- Migrating from one framework/platform to another
- Establishing testing strategy for frontend components

**Not for:**
- Backend API design (use api-design-validator)
- Infrastructure deployment (use cloud-native-deployment-orchestrator)
- CSS framework selection or styling implementation
- Low-level browser compatibility issues
- Native platform-specific APIs beyond component architecture

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `platform` must be exactly one of: react, vue, ios, android, react-native
- `project_type` must be one of: new, refactor, migration
- `tier` must be: T1 or T2
- `state_complexity` if provided must be: simple, moderate, complex
- `performance_requirements` if provided must be: standard, high-performance, low-bandwidth
- `accessibility_level` if provided must be: basic, WCAG-AA, WCAG-AAA

**Source freshness:**
- React Documentation (accessed 2025-10-25T21:30:36-04:00): https://react.dev/learn
- Vue.js 3 Guide (accessed 2025-10-25T21:30:36-04:00): https://vuejs.org/guide/introduction.html
- Apple Developer Swift Documentation (accessed 2025-10-25T21:30:36-04:00): https://developer.apple.com/documentation/swift
- Android Kotlin Development (accessed 2025-10-25T21:30:36-04:00): https://developer.android.com/kotlin/first
- React Native Documentation (accessed 2025-10-25T21:30:36-04:00): https://reactnative.dev/docs/getting-started
- Apple Human Interface Guidelines (accessed 2025-10-25T21:30:36-04:00): https://developer.apple.com/design/human-interface-guidelines

---

## Procedure

### T1: Quick Guidance (≤2k tokens)

**Fast path for 80% of component architecture decisions:**

1. **Platform-specific starter recommendation:**
   - **React:** Functional components + hooks, avoid class components
   - **Vue:** Composition API (Vue 3) over Options API for new projects
   - **iOS:** SwiftUI for iOS 15+ projects, UIKit for legacy support
   - **Android:** Jetpack Compose for new projects, XML layouts for legacy
   - **React Native:** Functional components + hooks, platform-specific files (.ios.tsx, .android.tsx)

2. **State management quick decision:**
   - **Simple (forms, UI toggles):** Local state (useState/ref)
   - **Moderate (app-wide theme, auth):** Context API (React), Provide/Inject (Vue), @StateObject/@EnvironmentObject (SwiftUI), ViewModel (Android)
   - **Complex (global cache, real-time sync):** Redux Toolkit (React), Pinia (Vue), Combine (iOS), Flow/LiveData (Android)

3. **Component hierarchy pattern:**
   - Follow container/presentational pattern
   - Keep components small (≤200 lines)
   - One component per file
   - Props flow down, events flow up
   - Avoid prop drilling beyond 2-3 levels

4. **Performance quick wins:**
   - React: React.memo for expensive components, useMemo/useCallback for heavy computations
   - Vue: v-once for static content, computed properties for derived state
   - iOS: LazyVStack/LazyHStack for lists, @ViewBuilder for composition
   - Android: LazyColumn/LazyRow, remember for expensive operations
   - React Native: FlatList over ScrollView, memo for list items

5. **Output T1 recommendation:**
   - Architecture pattern (component hierarchy sketch)
   - State management choice with rationale
   - Top 3 performance optimizations
   - Testing approach (reference testing-strategy-composer)

### T2: Detailed Architecture (≤6k tokens)

**Extended guidance for complex component architectures:**

1. **Comprehensive architecture design:**
   - **File structure convention:**
     - React/Vue: `/components`, `/hooks` or `/composables`, `/store`, `/utils`, `/types`
     - iOS: Group by feature, Models/Views/ViewModels separation
     - Android: MVVM or MVI pattern, package by feature
     - React Native: `/src/components`, `/src/screens`, `/src/navigation`, `/src/services`

   - **Component categorization:**
     - Layout components (navigation, grids, containers)
     - UI primitives (buttons, inputs, cards)
     - Feature components (user profile, checkout flow)
     - HOCs/Renderless components (logic encapsulation)

2. **State management deep dive:**
   - **React advanced patterns:**
     - Redux Toolkit with RTK Query for API state
     - Zustand for lightweight global state
     - Jotai/Recoil for atomic state management
     - Context + useReducer for feature-scoped state

   - **Vue advanced patterns:**
     - Pinia stores with composition API
     - VueUse composables for reusable logic
     - Provide/Inject for dependency injection
     - ref/reactive pattern selection guide

   - **iOS state management:**
     - @State for view-local state
     - @StateObject for owned observable objects
     - @ObservedObject for passed observable objects
     - @EnvironmentObject for app-wide state
     - Combine publishers for async state

   - **Android state management:**
     - ViewModel with StateFlow/LiveData
     - Repository pattern for data layer
     - Hilt for dependency injection
     - Room for local persistence

   - **React Native considerations:**
     - Same as React + AsyncStorage for persistence
     - Realm for complex offline-first apps
     - Redux Persist for state hydration

3. **Performance optimization strategies:**
   - **React:**
     - Code splitting with React.lazy() and Suspense
     - Virtual lists for long data (react-window, react-virtualized)
     - Optimize re-renders with React DevTools Profiler
     - Bundle analysis with webpack-bundle-analyzer

   - **Vue:**
     - Async components with defineAsyncComponent
     - Virtual scrolling with vue-virtual-scroller
     - Lazy hydration for SSR
     - Vite bundle analysis

   - **iOS:**
     - Image optimization (SF Symbols, Asset Catalogs)
     - Background task optimization
     - Instruments profiling (Time Profiler, Allocations)
     - SwiftUI lazy loading modifiers

   - **Android:**
     - R8 code shrinking and obfuscation
     - Image optimization (WebP, vector drawables)
     - Baseline profiles for app startup
     - Compose recomposition optimization

   - **React Native:**
     - Hermes JavaScript engine
     - Native module optimization
     - Image caching (react-native-fast-image)
     - FlatList optimization (getItemLayout, keyExtractor)

4. **Accessibility implementation:**
   - **WCAG-AA compliance:**
     - Semantic HTML/native components (React/Vue)
     - ARIA labels and roles where needed
     - Keyboard navigation support
     - Color contrast ratios ≥4.5:1 for text
     - Focus management

   - **Platform-specific:**
     - React: react-aria library for accessible components
     - Vue: vue-announcer for screen reader announcements
     - iOS: VoiceOver support with .accessibilityLabel()
     - Android: TalkBack support with contentDescription
     - React Native: accessibilityLabel, accessibilityRole

5. **Testing integration (leverage testing-strategy-composer):**
   - **Unit tests:**
     - React: Jest + React Testing Library
     - Vue: Vitest + Vue Test Utils
     - iOS: XCTest for ViewModels and business logic
     - Android: JUnit + MockK for ViewModels
     - React Native: Jest + React Native Testing Library

   - **Component/Integration tests:**
     - React/Vue: Component tests with user interaction simulation
     - iOS: XCTest with XCUITest for SwiftUI previews
     - Android: Espresso for UI tests
     - React Native: Detox for e2e mobile tests

   - **Visual regression:**
     - Storybook + Chromatic (React/Vue/React Native)
     - Snapshot tests (all platforms)

6. **Output T2 detailed plan:**
   - Complete file structure with naming conventions
   - State management architecture diagram
   - Performance optimization checklist (prioritized)
   - Accessibility implementation guide
   - Testing strategy with tool recommendations
   - Migration path (if project_type=migration)
   - Code scaffolding templates (reference resources/)

---

## Decision Rules

**Framework/platform selection guidance:**
- Choose **React** if: large ecosystem, flexible architecture, strong typing (TypeScript), hiring availability priority
- Choose **Vue** if: gentler learning curve, integrated tooling (Vite), single-file components preferred
- Choose **iOS native** if: iOS-only app, need platform-specific APIs, best performance required
- Choose **Android native** if: Android-only app, need platform-specific APIs, Material Design 3 alignment
- Choose **React Native** if: code sharing across iOS/Android >70%, JavaScript team, faster iteration priority

**State management escalation:**
- Start with local state; escalate to context/global only when prop drilling exceeds 3 levels
- Prefer built-in solutions (Context API, Composition API) before external libraries
- Only introduce Redux/Pinia when state logic becomes complex (>5 interconnected actions)

**Performance optimization priorities:**
1. Measure first (profiling tools) before optimizing
2. Optimize critical render path (initial load <3s)
3. Lazy load routes/screens
4. Optimize images and assets
5. Reduce bundle size (code splitting, tree shaking)

**Abort conditions:**
- If platform not in supported list → reject request
- If migration involves unsupported source/target → request clarification
- If state complexity undefined and project is large → request user input
- If accessibility requirements exceed platform capabilities → flag limitation

---

## Output Contract

**Schema:**
```json
{
  "architecture_plan": {
    "file_structure": ["string", "array of directory/file paths"],
    "component_hierarchy": "string (ASCII diagram or description)",
    "pattern": "string (container/presentational, MVVM, etc.)"
  },
  "state_management_recommendation": {
    "approach": "string (e.g., 'Redux Toolkit', 'Pinia', 'SwiftUI @StateObject')",
    "rationale": "string (why this choice)",
    "libraries": ["string", "array of package names"],
    "setup_steps": ["string", "array of implementation steps"]
  },
  "performance_patterns": [
    {
      "pattern": "string (e.g., 'React.memo', 'LazyVStack')",
      "use_case": "string",
      "code_example_ref": "string (path to resources/)"
    }
  ],
  "platform_scaffolding": "string (starter code or template reference)",
  "testing_integration": {
    "unit_testing_tools": ["string"],
    "component_testing_tools": ["string"],
    "e2e_testing_tools": ["string"],
    "coverage_target": "number (percentage)"
  },
  "accessibility_checklist": ["string", "array of WCAG requirements"],
  "migration_notes": "string (if project_type=migration, else null)"
}
```

**Required fields:** `architecture_plan`, `state_management_recommendation`, `performance_patterns`, `testing_integration`

**Optional fields:** `accessibility_checklist` (if accessibility_level provided), `migration_notes` (if project_type=migration)

---

## Examples

**Example: React component architecture for moderate state complexity**

Input:
```json
{
  "platform": "react",
  "project_type": "new",
  "tier": "T1",
  "state_complexity": "moderate",
  "performance_requirements": "standard"
}
```

Output:
```json
{
  "architecture_plan": {
    "pattern": "container/presentational",
    "component_hierarchy": "App > Layout > [Header, Main(Router), Footer]"
  },
  "state_management_recommendation": {
    "approach": "Context API + useReducer",
    "rationale": "Moderate complexity fits Context; avoid Redux overhead"
  },
  "performance_patterns": [
    {"pattern": "React.memo", "use_case": "expensive list items"},
    {"pattern": "Code splitting", "use_case": "route-based chunks"}
  ]
}
```

---

## Quality Gates

**Token budgets:**
- **T1 ≤ 2k tokens:** Platform detection, state decision, 3-5 quick wins
- **T2 ≤ 6k tokens:** Full architecture, performance deep dive, accessibility guide, 4-6 authoritative sources
- **T3 not implemented:** This skill operates at T1/T2 only; complex multi-framework migrations requiring deep research should use architecture-decision-framework

**Safety:**
- No framework-specific exploits or anti-patterns
- Recommend only stable, well-maintained libraries
- Flag deprecated patterns (e.g., React class components, Vue Options API for new projects)
- Accessibility: ensure compliance with WCAG guidelines

**Auditability:**
- All platform-specific recommendations cite official documentation (React.dev, Vue.js, Apple, Android, React Native docs)
- Performance claims reference framework-specific profiling tools
- State management recommendations backed by framework maintainer guidance

**Determinism:**
- Same input → same architectural recommendation
- Version-aware (React 18+, Vue 3+, iOS 15+, Android API 31+)
- Stable library recommendations (prefer framework built-ins over third-party when equivalent)

---

## Resources

**Official documentation:**
- React: https://react.dev/learn, https://react.dev/reference/react
- Vue: https://vuejs.org/guide/, https://vuejs.org/api/
- iOS: https://developer.apple.com/documentation/swiftui, https://developer.apple.com/documentation/uikit
- Android: https://developer.android.com/jetpack/compose, https://developer.android.com/kotlin
- React Native: https://reactnative.dev/docs/components-and-apis

**State management:**
- Redux Toolkit: https://redux-toolkit.js.org/
- Pinia: https://pinia.vuejs.org/
- Zustand: https://github.com/pmndrs/zustand
- VueUse: https://vueuse.org/

**Performance:**
- React DevTools Profiler: https://react.dev/learn/react-developer-tools
- Vue DevTools: https://devtools.vuejs.org/
- Xcode Instruments: https://developer.apple.com/xcode/features/
- Android Profiler: https://developer.android.com/studio/profile

**Testing:**
- React Testing Library: https://testing-library.com/react
- Vue Test Utils: https://test-utils.vuejs.org/
- Detox (React Native): https://wix.github.io/Detox/

**Accessibility:**
- React ARIA: https://react-spectrum.adobe.com/react-aria/
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- iOS Accessibility: https://developer.apple.com/accessibility/
- Android Accessibility: https://developer.android.com/guide/topics/ui/accessibility

**Templates:** See `resources/component-templates/` for platform-specific scaffolding
