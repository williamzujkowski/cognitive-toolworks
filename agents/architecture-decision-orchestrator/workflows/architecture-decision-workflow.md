# Architecture Decision Workflow

This workflow details the 4-step process orchestrated by the Architecture Decision Orchestrator agent.

## Workflow Overview

```
Discovery → Analysis → Synthesis → Documentation
```

**Total Steps**: 4
**Progressive Tiers**: T1 (Quick) | T2 (Standard) | T3 (Comprehensive)
**Primary Skill**: architecture-decision-framework

---

## Step 1: Discovery & Requirements

**Objective**: Gather decision context, quality attributes, constraints, and determine assessment tier.

**Inputs**:
- `decision_context`: Business/technical problem requiring architecture decision
- `constraints`: Non-functional requirements, compliance, budget, timeline
- `current_architecture`: Existing system description (optional, for migrations)
- `stakeholders`: List of decision-makers and their concerns

**Actions**:
1. Validate all required inputs present
2. Elicit quality attributes if not specified (performance, scalability, maintainability, security, etc.)
3. Identify system boundaries and integration points
4. Scan for existing ADRs using Glob (`docs/adr/*.md`, `architecture/decisions/*.md`)
5. Count existing ADRs and check for related decisions
6. Determine assessment tier based on complexity:
   - **T1**: < 3 quality attributes, clear pattern match, minimal trade-offs
   - **T2**: 3-5 quality attributes, multiple viable patterns, cross-team impact
   - **T3**: > 5 quality attributes, greenfield complex system, conflicting stakeholders

**Outputs**:
- Validated inputs with complete quality attribute list
- Existing ADR count and numbering for new ADR
- Assessment tier selection (T1/T2/T3)
- Stakeholder concern matrix

**Quality Gates**:
- Decision context is specific and actionable (not vague)
- At least 1 quality attribute identified
- If migration: current_architecture description provided

---

## Step 2: Analysis & Pattern Evaluation

**Objective**: Evaluate architectural patterns, perform trade-off analysis, score alternatives.

**Skill Invocation**:
```yaml
skill: architecture-decision-framework
inputs:
  decision_context: [from Step 1]
  constraints: [quality attributes + NFRs from Step 1]
  current_architecture: [from Step 1 if migration]
  stakeholders: [from Step 1]
tier: [T1/T2/T3 from Step 1]
```

**Actions (delegated to skill)**:
1. Evaluate candidate patterns: Layered, Hexagonal, Event-Driven, CQRS
2. Score each pattern against quality attributes (1-5 scale)
3. For T2/T3: Perform ATAM trade-off analysis
   - Create 3-5 quality attribute scenarios
   - Identify sensitivity points (decisions heavily impacting attributes)
   - Identify trade-off points (conflicting quality attributes)
   - Document risks and non-risks
4. Calculate pattern fit scores and rank alternatives
5. For migrations: Assess strangler vs big-bang vs phased approaches

**Outputs (from skill)**:
- Pattern evaluation matrix with scores and rationale
- ATAM analysis (T2/T3): scenarios, sensitivity/trade-off points, risks
- Ranked pattern recommendations
- Migration strategy recommendation (if applicable)

**Quality Gates**:
- All candidate patterns scored against quality attributes
- Trade-off points explicitly documented (T2/T3)
- Pattern recommendation justified with quantitative scores

---

## Step 3: Synthesis & ADR Generation

**Objective**: Generate ADR document, create C4 diagrams, produce decision artifacts.

**ADR Format Selection**:
- **T1**: Nygard format (concise, status-driven)
  - Sections: Status, Context, Decision, Consequences
- **T2**: Y-statement format (trade-off focused)
  - Format: "In context of X, facing Y, we decided for Z and neglected A, B to achieve benefits, accepting drawbacks"
- **T3**: MADR format (comprehensive)
  - Sections: Context, Decision Drivers, Considered Options, Decision Outcome, Pros/Cons, Links, Technical Story

**C4 Diagram Generation**:
- **T1**: Context diagram (Level 1) only
  - System boundary, external users, external systems
- **T2**: Context + Container diagrams (Levels 1-2)
  - Runtime executables, databases, communication protocols
- **T3**: Context + Container + Component diagrams (Levels 1-3)
  - Internal component structure, interfaces, dependencies

**Actions**:
1. Select ADR template based on tier
2. Populate ADR sections with analysis results from Step 2
3. Generate C4 diagrams in PlantUML or Mermaid format
4. Create trade-off matrix JSON with pattern scores
5. Generate pattern recommendation document
6. For complex systems: Create phased implementation roadmap

**Outputs**:
- Complete ADR in selected format (markdown)
- C4 diagrams (PlantUML/Mermaid files)
- Trade-off matrix (JSON)
- Pattern recommendation (JSON/markdown)
- Migration roadmap (markdown, T3 only)

**Quality Gates**:
- ADR includes all required sections for selected format
- ADR title ≤ 100 characters
- ADR context section ≤ 500 words
- C4 diagrams use valid PlantUML/Mermaid syntax
- Pattern recommendation includes primary + rationale ≤ 200 chars

---

## Step 4: Documentation & Validation

**Objective**: Validate artifacts, generate audit trail, write final files.

**Actions**:
1. Validate ADR completeness (all required sections present)
2. Validate C4 diagram syntax using Bash (PlantUML/Mermaid parser)
3. Verify quality attribute traceability:
   - Each quality attribute → pattern decision → rationale
4. Safety scan for embedded secrets/PII
5. Compute NOW_ET timestamp (NIST time.gov, America/New_York, ISO-8601)
6. Generate audit trail with sources and access dates
7. Write artifacts to designated paths:
   - ADR: `architecture/decisions/ADR-NNN-title.md` or `docs/adr/NNN-title.md`
   - C4 diagrams: `architecture/diagrams/` or `docs/diagrams/`
   - Analysis: `architecture/analysis/` or `docs/analysis/`

**Outputs**:
- Validated ADR document (markdown)
- Validated C4 diagrams (PlantUML/Mermaid)
- Audit trail with NOW_ET timestamps
- File paths for all generated artifacts

**Quality Gates**:
- ADR passes completeness check (required sections present)
- C4 diagrams pass syntax validation (PlantUML/Mermaid)
- Quality attributes traceable from decision to rationale
- No secrets detected (API keys, tokens, credentials)
- All timestamps use NOW_ET format
- All external references include access date

---

## Error Handling & Decision Rules

### Missing Requirements
- **Symptom**: decision_context vague or quality attributes missing
- **Action**: Emit TODO list with required fields and stop
- **Example TODO**: "Specify at least 3 quality attributes (performance, scalability, maintainability, security, etc.)"

### Pattern Scoring Ties
- **Symptom**: Multiple patterns score within 10% of each other
- **Action**: Recommend hybrid pattern or phased approach
- **Rationale**: Document why hybrid is better than single pattern

### Diagram Syntax Errors
- **Symptom**: PlantUML/Mermaid parser returns syntax error
- **Action**: Report specific error, suggest correction, retry validation
- **Escalation**: If retry fails, deliver ADR without diagrams and flag issue

### Token Overflow
- **Symptom**: Approaching token budget limits
- **Action**: Split analysis by pattern family
  - Batch 1: Layered + Hexagonal
  - Batch 2: Event-Driven + CQRS
- **Output**: Multiple ADRs or phased decision approach

### Stakeholder Conflicts
- **Symptom**: Quality attribute priorities conflict across stakeholders
- **Action**: Generate decision matrix showing trade-offs, escalate for policy decision
- **Output**: ADR documents conflict, recommends stakeholder workshop

---

## Example Execution Trace

```
Input:
  decision_context: "E-commerce platform needs architecture for new order processing system"
  constraints: ["performance: <200ms", "scalability: 50k users", "maintainability: high"]
  current_architecture: null (greenfield)
  stakeholders: [{role: "CTO", concern: "cost"}, {role: "Dev Lead", concern: "testability"}]

Step 1 (Discovery):
  ✓ Validated inputs
  ✓ Quality attributes: performance, scalability, maintainability, testability
  ✓ Existing ADRs: 5 found
  ✓ Next ADR number: ADR-006
  ✓ Tier selection: T3 (4 quality attributes, greenfield, multiple stakeholders)

Step 2 (Analysis):
  ✓ Invoked architecture-decision-framework skill (T3 tier)
  ✓ Patterns evaluated: Layered, Hexagonal, Event-Driven, CQRS
  ✓ Scores: Event-Driven=4.2, Hexagonal=4.5, CQRS=3.8, Layered=3.1
  ✓ ATAM: 4 scenarios, 3 sensitivity points, 2 trade-off points, 1 risk
  ✓ Recommendation: Hexagonal + Event-Driven hybrid

Step 3 (Synthesis):
  ✓ ADR format: MADR (T3 tier)
  ✓ C4 diagrams: Context, Container, Component (3 files)
  ✓ Trade-off matrix: JSON with scores and rationale
  ✓ Migration roadmap: Not applicable (greenfield)

Step 4 (Documentation):
  ✓ ADR validated: 1247 words, all sections present
  ✓ C4 diagrams validated: PlantUML syntax correct
  ✓ Quality attributes traced: 4/4 traceable
  ✓ No secrets detected
  ✓ Timestamp: 2025-10-26T01:55:50-04:00
  ✓ Files written:
    - /architecture/decisions/ADR-006-order-processing-hexagonal-event-driven.md
    - /architecture/diagrams/adr-006-c4-context.puml
    - /architecture/diagrams/adr-006-c4-container.puml
    - /architecture/diagrams/adr-006-c4-component.puml
    - /architecture/analysis/adr-006-trade-off-matrix.json
```

---

## Progressive Disclosure Rules

**Tier Selection Logic**:
```
IF quality_attributes.count < 3 AND pattern_match_clear AND trade_offs_minimal:
  → T1 (Quick)
ELSE IF quality_attributes.count >= 3 AND quality_attributes.count <= 5 AND patterns_multiple:
  → T2 (Standard)
ELSE IF quality_attributes.count > 5 OR greenfield_complex OR stakeholders_conflicting:
  → T3 (Comprehensive)
```

**Token Budget Enforcement**:
- **T1**: ≤ 2,000 tokens (pattern match + Nygard ADR + context diagram)
- **T2**: ≤ 6,000 tokens (ATAM + Y-statement + context/container diagrams)
- **T3**: ≤ 12,000 tokens (full MADR + complete C4 + comprehensive analysis)

**Skill Invocation Tiers**:
- All tiers invoke architecture-decision-framework skill
- Tier parameter passed to skill to control analysis depth
- Skill returns appropriate outputs based on tier

---

## Related Skills

- **architecture-decision-framework** (primary): Pattern evaluation, ATAM analysis, ADR generation, C4 diagrams
- **oscal-ssp-validate** (optional): If architecture decisions impact compliance requirements
- **security-assessment-framework** (optional): If security is primary quality attribute
