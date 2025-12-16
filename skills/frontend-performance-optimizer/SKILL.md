---
name: Frontend Performance Optimizer
slug: frontend-performance-optimizer
description: Analyzes and optimizes frontend performance using Core Web Vitals, bundle analysis, lazy loading, image optimization, and caching strategies
capabilities:
  - Core Web Vitals measurement and optimization (LCP, FID, CLS)
  - JavaScript bundle size analysis and code splitting
  - Image optimization and modern format recommendations
  - Lazy loading strategy implementation
  - Browser caching and CDN configuration
  - Resource prioritization and preloading
  - Performance budget definition and tracking
inputs:
  - Application URL or codebase path
  - Framework type (React, Vue, Angular, vanilla)
  - Target performance metrics (optional)
  - Existing bundle analyzer output (optional)
outputs:
  - Performance audit report with Core Web Vitals scores
  - Prioritized optimization recommendations
  - Code examples for fixes
  - Performance budget thresholds
keywords:
  - performance
  - frontend
  - web-vitals
  - optimization
  - bundle-analysis
  - lazy-loading
  - caching
  - LCP
  - FID
  - CLS
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security:
  - no-secrets: true
  - no-pii: true
  - read-only-analysis: true
links:
  - title: "Web Vitals"
    url: "https://web.dev/vitals/"
    accessed: "2025-12-15T19:35:37-05:00"
  - title: "Lighthouse Performance Scoring"
    url: "https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/"
    accessed: "2025-12-15T19:35:37-05:00"
  - title: "webpack Bundle Analyzer"
    url: "https://github.com/webpack-contrib/webpack-bundle-analyzer"
    accessed: "2025-12-15T19:35:37-05:00"
---

# frontend-performance-optimizer

## Purpose & When-To-Use

**Trigger conditions:**

- Core Web Vitals scores below recommended thresholds (LCP >2.5s, FID >100ms, CLS >0.1)
- Page load time exceeds 3 seconds on 3G networks
- JavaScript bundle size >500KB (gzipped)
- User reports of slow initial page render or interaction delays
- Preparing for production launch or performance audit
- Investigating performance regression after deployment

**Use this skill when** you need systematic frontend performance analysis and actionable optimization recommendations based on industry-standard metrics.

## Pre-Checks

**Time normalization:**
```python
NOW_ET = "2025-12-15T19:35:37-05:00"  # NIST/time.gov semantics
```

**Input validation:**

- Application URL is accessible or codebase path exists
- Framework type is specified or detectable from package.json/file structure
- If bundle analyzer output provided, verify JSON format validity
- Web Vitals measurement tools available (Lighthouse CLI, WebPageTest API access)

**Source freshness:**

- Web Vitals thresholds: accessed 2025-12-15 (refresh if >90 days)
- Browser support data: caniuse.com accessed within 30 days
- Framework-specific optimization guides: accessed within 90 days

## Procedure

### T1: Fast Path (≤2k tokens, 80% of requests)

**Goal:** Quick performance assessment with high-impact recommendations.

**Steps:**

1. **Measure Core Web Vitals** using Lighthouse or WebPageTest API
   - Extract LCP, FID (or INP), CLS scores
   - Identify if any metric fails "Good" threshold

2. **Analyze bundle size** (if build artifacts available)
   - Check total JavaScript size (target: <500KB gzipped)
   - Identify largest chunks

3. **Generate top 3 recommendations** based on worst metrics:
   - LCP issues → image optimization, resource preloading, server response time
   - FID/INP issues → reduce JavaScript execution time, code splitting
   - CLS issues → explicit size attributes, font loading strategy

**Output:** Performance score summary + prioritized 3-item action list.

**Abort conditions:** URL unreachable, no performance data available.

### T2: Extended Analysis (≤6k tokens, 15% of requests)

**Goal:** Comprehensive audit with framework-specific optimizations.

**Steps:**

1. **All T1 steps** plus detailed metric breakdown

2. **Framework-specific analysis:**
   - React: Check React.lazy usage, code splitting at route level, memo/useCallback patterns
   - Vue: Analyze async components, dynamic imports, keep-alive usage
   - Angular: Review lazy loading modules, AOT compilation, tree-shaking effectiveness

3. **Resource optimization:**
   - Image audit: format (WebP/AVIF), sizing, lazy loading, responsive images
   - Font strategy: font-display, preload, variable fonts
   - CSS: unused styles, critical CSS extraction

4. **Caching strategy review:**
   - Service worker implementation
   - Cache-Control headers for static assets
   - CDN configuration (if applicable)

5. **Performance budget definition:**
   - Set thresholds for JavaScript, CSS, images, total page weight
   - Recommend CI integration (Lighthouse CI, bundlesize)

**Output:** Detailed audit report + code examples + performance budget config.

### T3: Deep Dive (≤12k tokens, 5% of requests)

**Goal:** Root cause analysis with custom optimizations and benchmarking.

**Steps:**

1. **All T2 steps** plus root cause investigation

2. **Waterfall analysis:**
   - Request chain dependencies
   - Render-blocking resources
   - Third-party script impact

3. **JavaScript execution profiling:**
   - Long tasks (>50ms) identification
   - Main thread blocking analysis
   - Heavy computation offloading opportunities (Web Workers)

4. **Custom optimization strategies:**
   - Component-level lazy loading (intersection observer patterns)
   - Resource hints (preconnect, dns-prefetch, prefetch)
   - Module federation for micro-frontends

5. **Benchmarking plan:**
   - Synthetic monitoring setup (Lighthouse CI)
   - Real User Monitoring (RUM) integration
   - A/B testing framework for optimization validation

**Output:** Root cause analysis + custom optimization plan + monitoring setup guide.

## Decision Rules

**Tier escalation:**

- T1 → T2: User requests framework-specific recommendations OR bundle size >1MB
- T2 → T3: Performance regression investigation OR custom optimization needed OR micro-frontend architecture

**Ambiguity thresholds:**

- Cannot measure Web Vitals (no URL, blocked by auth): Request staging URL or Lighthouse JSON export
- Framework not detected: Ask user to specify or analyze as vanilla JavaScript
- Bundle analyzer unavailable: Provide generic code splitting guidance, recommend webpack-bundle-analyzer setup

**Abort conditions:**

- URL returns 403/404/500 and no alternative provided
- No build artifacts and no URL (cannot analyze)
- User requests backend optimization (out of scope)

## Output Contract

**Required fields:**

```typescript
interface PerformanceReport {
  metrics: {
    lcp: { value: number; rating: "good" | "needs-improvement" | "poor" };
    fid: { value: number; rating: "good" | "needs-improvement" | "poor" };
    cls: { value: number; rating: "good" | "needs-improvement" | "poor" };
  };
  recommendations: Array<{
    priority: "high" | "medium" | "low";
    category: "images" | "javascript" | "css" | "caching" | "fonts" | "third-party";
    issue: string;
    solution: string;
    estimatedImpact: string; // e.g., "0.5s LCP improvement"
    codeExample?: string;
  }>;
  performanceBudget?: {
    javascript: string; // e.g., "500KB"
    css: string;
    images: string;
    total: string;
  };
  nextSteps: string[];
}
```

**Format:** Structured JSON or Markdown report with code blocks.

**Constraints:**

- Code examples ≤30 lines
- Recommendations ranked by estimated impact
- All metrics include rating against Web Vitals thresholds

## Examples

### Example 1: T1 Quick Audit

**Input:**
```
URL: https://example.com/app
Framework: React
```

**Output:**
```markdown
## Performance Audit Summary

**Core Web Vitals:**
- LCP: 4.2s (poor) — Target: <2.5s
- FID: 85ms (good)
- CLS: 0.15 (needs improvement) — Target: <0.1

**Top 3 Recommendations:**

1. **HIGH: Optimize hero image (3.5MB PNG)**
   - Convert to WebP/AVIF
   - Use responsive images with srcset
   - Estimated impact: 1.5s LCP improvement

2. **HIGH: Reduce layout shift in header**
   - Add explicit width/height to logo
   - Reserve space for dynamic content
   - Estimated impact: 0.12 CLS reduction

3. **MEDIUM: Enable text compression**
   - Configure gzip/brotli for text assets
   - Estimated impact: 0.3s LCP improvement
```

## Quality Gates

**Token budgets:**

- T1 procedure + output: ≤2k tokens (measured via tiktoken cl100k_base)
- T2 procedure + output: ≤6k tokens
- T3 procedure + output: ≤12k tokens

**Safety:**

- No execution of user code (analysis only)
- Read-only access to public URLs
- No storage of user content beyond session

**Auditability:**

- All recommendations cite Web Vitals or framework docs
- Metric thresholds sourced from https://web.dev/vitals/ (accessed 2025-12-15)
- Tool versions specified in output (Lighthouse v11.x, webpack v5.x)

**Determinism:**

- Same URL + framework → consistent recommendations (within tool variance)
- Performance scores may vary ±5% due to network/server conditions
- Note measurement conditions (device type, throttling) in report

## Resources

**Official Documentation:**

- [Web Vitals](https://web.dev/vitals/) — Core metrics and thresholds
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/) — Audit methodology
- [React Code Splitting](https://react.dev/reference/react/lazy) — Framework-specific optimization
- [Next.js Image Optimization](https://nextjs.org/docs/pages/building-your-application/optimizing/images) — Modern image handling

**Tools:**

- [webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer) — Bundle visualization
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) — Automated auditing
- [WebPageTest](https://www.webpagetest.org/) — Detailed waterfall analysis
- [Chrome DevTools Coverage](https://developer.chrome.com/docs/devtools/coverage/) — Unused code detection

**Performance Budgets:**

- [Performance Budget Calculator](https://www.performancebudget.io/) — Budget recommendations
- [bundlesize](https://github.com/siddharthkp/bundlesize) — CI integration for size tracking
