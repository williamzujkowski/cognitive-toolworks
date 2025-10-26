---
name: Architecture Decision Framework
slug: architecture-decision-framework
description: Guide architecture decisions using ADRs, trade-off analysis, pattern catalogs, and C4 diagrams for layered, hexagonal, event-driven, and CQRS patterns.
capabilities:
  - Generate Architecture Decision Records (ADRs) in multiple formats
  - Analyze trade-offs across architectural patterns
  - Create C4 model diagrams (context, container, component)
  - Recommend pattern combinations and migrations
  - Evaluate decisions using ATAM and Y-statement frameworks
inputs:
  - decision_context: "Business/technical context requiring architecture decision"
  - constraints: "Non-functional requirements, compliance, budget, timeline"
  - current_architecture: "Existing system architecture (optional)"
  - stakeholders: "List of decision stakeholders and their concerns"
outputs:
  - adr_document: "ADR in Nygard, MADR, or Y-statement format"
  - trade_off_matrix: "ATAM analysis with sensitivity/tradeoff points"
  - c4_diagrams: "C4 model diagrams (context/container/component)"
  - pattern_recommendations: "Ranked pattern options with rationale"
keywords:
  - architecture-decision-records
  - ADR
  - trade-off-analysis
  - ATAM
  - C4-model
  - layered-architecture
  - hexagonal-architecture
  - event-driven
  - CQRS
  - Y-statements
version: 1.0.0
owner: cognitive-toolworks
license: CC-BY-4.0
security: public
links:
  - https://adr.github.io/
  - https://martinfowler.com/architecture
  - https://c4model.com/
  - https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
---

## Purpose & When-To-Use

**Invoke when:**
- New project requires architecture design from requirements
- Existing system needs architecture refactoring or migration
- Technical debt analysis reveals architectural anti-patterns
- Cross-team alignment needed on architecture direction
- Compliance/audit requires documented architecture decisions

**Outputs:** Complete ADR, trade-off analysis, C4 diagrams, pattern recommendations.

## Pre-Checks

1. **Normalize time:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601).
2. **Validate inputs:**
   - `decision_context` is non-empty and describes business/technical problem
   - `constraints` include at least one quality attribute (performance, security, scalability, maintainability)
   - `stakeholders` list includes technical decision-makers
3. **Source freshness:** Verify authoritative sources accessed at `NOW_ET`:
   - ADR templates from adr.github.io (accessed 2025-10-25T21:30:36-04:00)
   - Fowler architecture patterns (accessed 2025-10-25T21:30:36-04:00)
   - C4 model specification (accessed 2025-10-25T21:30:36-04:00)
   - ATAM from SEI/CMU (accessed 2025-10-25T21:30:36-04:00)

## Procedure

### T1: Quick Decision (≤2k tokens)

**When:** Clear pattern match, minimal trade-offs, single stakeholder concern.

1. **Pattern Match:** Map `decision_context` to one of:
   - **Layered:** UI/Business/Data separation, traditional monoliths
   - **Hexagonal (Ports & Adapters):** Domain isolation, testability focus
   - **Event-Driven:** Asynchronous workflows, decoupled services
   - **CQRS:** Read/write separation, complex domain models

2. **Quick ADR (Nygard format):**
   ```markdown
   # ADR-NNN: [Decision Title]

   Status: Proposed | Accepted | Deprecated | Superseded

   ## Context
   [Business/technical context in 2-3 sentences]

   ## Decision
   [Pattern/approach chosen]

   ## Consequences
   Positive: [1-2 benefits]
   Negative: [1-2 drawbacks]
   ```

3. **Stop if:** Decision is straightforward with clear pattern fit and < 3 alternatives.

### T2: Extended Analysis (≤6k tokens)

**When:** Multiple patterns viable, significant trade-offs, cross-team impact.

1. **Pattern Evaluation Matrix:**
   For each candidate pattern (Layered, Hexagonal, Event-Driven, CQRS):
   - **Quality Attributes (score 1-5):** Performance, Scalability, Maintainability, Testability, Security
   - **Fit to Context:** How well pattern addresses `decision_context`
   - **Migration Cost:** Effort to implement from `current_architecture`
   - **Team Skill Alignment:** Existing team expertise

2. **ATAM Trade-Off Analysis:**
   - **Scenarios:** Create 3-5 quality attribute scenarios (e.g., "System must handle 10k concurrent users with <500ms latency")
   - **Sensitivity Points:** Decisions heavily impacting quality attributes
   - **Trade-Off Points:** Conflicts between quality attributes (e.g., performance vs. maintainability)
   - **Risks:** Architectural decisions with uncertain outcomes
   - **Non-Risks:** Sound decisions with low uncertainty

3. **Y-Statement ADR (extended format):**
   ```
   In the context of [functional requirement or component],
   facing [non-functional requirement or quality concern],
   we decided for [chosen pattern/approach]
   and neglected [alternative 1], [alternative 2]
   to achieve [benefits and requirement satisfaction],
   accepting that [drawbacks and consequences].
   ```

4. **C4 Context Diagram (Level 1):**
   - System boundary and external dependencies
   - Primary users and external systems
   - Key interactions and data flows

5. **Pattern Combination Recommendations:**
   Common hybrid patterns:
   - **Layered + Hexagonal:** Traditional layers with domain isolation
   - **Event-Driven + CQRS:** Event sourcing with read/write separation
   - **Hexagonal + Event-Driven:** Ports/adapters with async messaging

### T3: Deep Dive (≤12k tokens)

**When:** Greenfield complex system, high-risk migration, multiple conflicting stakeholders.

1. **Full MADR (Markdown ADR):**
   Include: Context, Decision Drivers, Considered Options, Decision Outcome, Pros/Cons, Links, Technical Story.

2. **Complete C4 Model:**
   - **Level 1 Context:** System in environment
   - **Level 2 Container:** Runtime executables/databases
   - **Level 3 Component:** Internal component structure
   - Optional **Level 4 Code:** Class diagrams for critical components

3. **Comprehensive Trade-Off Analysis:**
   - **ATAM full workshop simulation:** Utility tree with prioritized quality attributes
   - **Cost-benefit matrix:** Implementation cost vs. benefit for each pattern
   - **Risk mitigation strategies:** For each identified risk
   - **Migration roadmap:** Phased approach if migrating from `current_architecture`

4. **Pattern Catalog Deep Dive:**
   For Layered, Hexagonal, Event-Driven, CQRS:
   - **When to use:** Detailed triggers and anti-triggers
   - **Reference implementations:** Links to open-source examples
   - **Common pitfalls:** Anti-patterns and failure modes
   - **Evolution paths:** How pattern adapts to changing requirements

## Decision Rules

1. **Pattern Selection Thresholds:**
   - **Layered:** Use when <= 3 quality attributes critical, monolith acceptable, team traditional
   - **Hexagonal:** Use when testability/domain isolation > deployment complexity
   - **Event-Driven:** Use when asynchrony required, loose coupling critical, eventual consistency acceptable
   - **CQRS:** Use when read/write patterns diverge significantly, complex domain model, scalability critical

2. **Abort Conditions:**
   - `decision_context` is vague or lacks quality attribute constraints → Request clarification
   - No authoritative sources available for claimed pattern benefits → Defer decision
   - Stakeholder consensus impossible on quality attribute priorities → Escalate

3. **Ambiguity Handling:**
   - If 2+ patterns score within 10% on evaluation matrix → Recommend hybrid or phased approach
   - If `current_architecture` migration cost > 2x implementation benefit → Recommend incremental strangler pattern

## Output Contract

**Required Fields:**

```json
{
  "adr": {
    "format": "nygard | madr | y-statement",
    "title": "ADR-NNN: [Title]",
    "status": "proposed | accepted | deprecated | superseded",
    "context": "string",
    "decision": "string",
    "consequences": ["array of strings"],
    "date": "ISO-8601",
    "author": "string"
  },
  "trade_off_analysis": {
    "method": "atam | cost-benefit | quality-attribute-matrix",
    "patterns_evaluated": ["array of pattern names"],
    "sensitivity_points": ["array"],
    "trade_off_points": ["array"],
    "risks": ["array"],
    "recommendation": "string"
  },
  "c4_diagrams": {
    "context": "PlantUML or Mermaid syntax",
    "container": "PlantUML or Mermaid syntax (optional)",
    "component": "PlantUML or Mermaid syntax (optional)"
  },
  "pattern_recommendation": {
    "primary": "pattern name",
    "rationale": "string (≤200 chars)",
    "alternatives": ["array of pattern names"],
    "migration_strategy": "greenfield | strangler | big-bang | phased"
  }
}
```

**Constraints:**
- ADR title ≤ 100 chars
- Context section ≤ 500 words
- C4 diagrams in PlantUML or Mermaid format
- All external references must have access date = `NOW_ET`

## Examples

```yaml
# T2 Example: Microservices API Gateway Decision
decision_context: "E-commerce platform migrating from monolith to microservices"
constraints:
  - performance: "< 200ms latency for 95th percentile"
  - scalability: "Handle 50k concurrent users"
  - maintainability: "Independent team deployment"

output:
  adr_format: y-statement
  content: |
    In the context of migrating monolithic e-commerce to microservices,
    facing the need for unified API entry point with <200ms latency,
    we decided for API Gateway pattern with event-driven backend
    and neglected direct client-to-service calls, service mesh only,
    to achieve centralized auth/rate-limiting and loose coupling,
    accepting that gateway becomes potential bottleneck requiring HA design.

  trade_off_analysis:
    patterns_evaluated: [hexagonal, event-driven, cqrs]
    recommendation: "Hexagonal (services) + Event-Driven (inter-service)"
    trade_offs:
      - "Performance vs Maintainability: Event async adds latency but improves decoupling"
      - "Complexity vs Scalability: More components but independent scaling"
```

## Quality Gates

1. **Token Budget:**
   - T1 ≤ 2,000 tokens (pattern match + simple ADR)
   - T2 ≤ 6,000 tokens (ATAM + Y-statement + C4 context)
   - T3 ≤ 12,000 tokens (full MADR + complete C4 + deep trade-off)

2. **Validation:**
   - All ADRs include: title, status, context, decision, consequences
   - Trade-off analysis cites specific quality attributes
   - Pattern recommendations linked to authoritative sources with `NOW_ET` dates
   - C4 diagrams validate with PlantUML/Mermaid parsers

3. **Auditability:**
   - Decision rationale traceable to `decision_context` and `constraints`
   - All claimed pattern benefits cite Fowler, SEI, or peer-reviewed sources
   - Rejected alternatives documented with rejection rationale

## Resources

**ADR Templates & Practices:**
- ADR GitHub Organization: https://adr.github.io/ (accessed 2025-10-25T21:30:36-04:00)
- MADR Templates: https://adr.github.io/adr-templates/ (accessed 2025-10-25T21:30:36-04:00)
- Y-Statements Guide: https://medium.com/olzzio/y-statements-10eb07b5a177 (accessed 2025-10-25T21:30:36-04:00)

**Architecture Patterns:**
- Martin Fowler Architecture: https://martinfowler.com/architecture (accessed 2025-10-25T21:30:36-04:00)
- Event-Driven Patterns: https://martinfowler.com/articles/201701-event-driven.html (accessed 2025-10-25T21:30:36-04:00)
- Hexagonal Architecture: https://alistair.cockburn.us/hexagonal-architecture (accessed 2025-10-25T21:30:36-04:00)

**C4 Model:**
- C4 Model Official Site: https://c4model.com/ (accessed 2025-10-25T21:30:36-04:00)
- C4 Diagrams Guide: https://c4model.com/diagrams (accessed 2025-10-25T21:30:36-04:00)

**Trade-Off Analysis:**
- ATAM (SEI/CMU): https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/ (accessed 2025-10-25T21:30:36-04:00)
- Architecture Decision Making: https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html (accessed 2025-10-25T21:30:36-04:00)
