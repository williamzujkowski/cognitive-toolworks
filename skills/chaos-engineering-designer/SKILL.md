---
name: Chaos Engineering Experiment Designer
slug: chaos-engineering-designer
description: Design chaos engineering experiments to test system resilience with controlled failure injection, hypothesis formulation, and blast radius control.
capabilities:
  - Define steady-state hypotheses for distributed systems
  - Design controlled chaos experiments with measurable outcomes
  - Configure blast radius limits to minimize production impact
  - Generate experiment specifications for Chaos Mesh, LitmusChaos, and Chaos Monkey
  - Implement progressive failure injection strategies
  - Create experiment reports with resilience metrics
inputs:
  - system_architecture: "Description of target system components, dependencies, and deployment topology"
  - resilience_goals: "Specific reliability objectives (e.g., RTO, RPO, availability targets)"
  - experiment_scope: "Boundaries for chaos testing (services, regions, blast radius)"
  - existing_monitoring: "Available observability tools and steady-state metrics"
outputs:
  - experiment_plan: "Complete chaos experiment specification with hypothesis, variables, and success criteria"
  - implementation_config: "Tool-specific configuration (Chaos Mesh YAML, LitmusChaos CRDs, etc.)"
  - safety_controls: "Blast radius limits, abort conditions, and rollback procedures"
  - reporting_template: "Experiment execution report structure with resilience metrics"
keywords:
  - chaos engineering
  - resilience testing
  - failure injection
  - steady state hypothesis
  - blast radius
  - chaos mesh
  - litmuschaos
  - chaos monkey
  - SRE
  - distributed systems
version: 1.0.0
owner: cognitive-toolworks
license: CC-BY-SA-4.0
security: Public - no sensitive data
links:
  - https://principlesofchaos.org/
  - https://chaos-mesh.org/
  - https://litmuschaos.io/
  - https://netflix.github.io/chaosmonkey/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Resilience testing needed for distributed system or microservices architecture
- Disaster recovery validation beyond traditional testing
- SRE practice adoption requiring systematic failure experimentation
- Production confidence gaps in system behavior under failure conditions
- Pre-deployment validation of fault tolerance mechanisms
- Post-incident chaos engineering to prevent recurrence

**Use this skill to:**
- Design hypothesis-driven chaos experiments with measurable outcomes
- Define steady-state baselines and deviation thresholds
- Configure controlled failure injection with progressive escalation
- Generate tool-specific experiment configurations (Chaos Mesh, LitmusChaos, Chaos Monkey)
- Establish blast radius controls and abort conditions
- Create reproducible experiment workflows integrated with CI/CD

**Do NOT use for:**
- Traditional load or performance testing (use testing-strategy-composer)
- Security penetration testing (use security-assessment-framework)
- Functional correctness testing (use testing-strategy-composer)
- One-off manual fault injection without hypothesis or measurement

## Pre-Checks

**Time normalization:**
```
NOW_ET = 2025-10-25T21:30:36-04:00
```

**Required inputs validation:**
- [ ] `system_architecture` includes component diagram with dependencies
- [ ] `resilience_goals` specify quantitative targets (e.g., 99.9% availability)
- [ ] `experiment_scope` defines clear boundaries (services, environments, regions)
- [ ] `existing_monitoring` lists available metrics, dashboards, and alerting

**Source freshness checks:**
- Principles of Chaos Engineering (accessed 2025-10-25T21:30:36-04:00): https://principlesofchaos.org/
- Chaos Mesh v2.x documentation (accessed 2025-10-25T21:30:36-04:00): https://chaos-mesh.org/
- LitmusChaos 3.x framework (accessed 2025-10-25T21:30:36-04:00): https://litmuschaos.io/
- Netflix Chaos Monkey practices (accessed 2025-10-25T21:30:36-04:00): https://netflix.github.io/chaosmonkey/

**Abort conditions:**
- If `system_architecture` lacks dependency information → request clarification
- If no monitoring baseline exists → emit TODO: establish steady-state metrics first
- If production environment lacks rollback capabilities → restrict to non-prod only

## Procedure

### Tier 1: Quick Experiment Design (≤2k tokens)

**Fast path for common scenarios:**

1. **Validate experiment readiness**
   - Check monitoring baseline exists
   - Verify rollback capabilities
   - Confirm blast radius boundaries

2. **Define steady-state hypothesis**
   - Identify key user-facing metrics (latency, error rate, throughput)
   - Establish normal operating ranges from historical data
   - Example: "P95 latency < 200ms AND error rate < 0.1% during business hours"

3. **Select failure scenario** (common patterns)
   - Pod/instance termination (Chaos Monkey pattern)
   - Network latency/partition injection
   - Resource exhaustion (CPU, memory, I/O)
   - Cloud region/availability zone failure

4. **Configure minimal experiment**
   - Start with 1-5% traffic/instances
   - 5-minute duration maximum
   - Auto-abort if steady state violated by >20%
   - Single service scope

5. **Output T1 experiment spec**
   ```yaml
   experiment_name: "<service>-<failure-type>-v1"
   hypothesis: "<steady-state-assertion>"
   scope: "<service-name> in <environment>"
   blast_radius: "<percentage> of instances"
   duration: "5m"
   abort_conditions: "<steady-state-threshold>"
   ```

**T1 deliverable:** Minimal experiment specification ready for review.

---

### Tier 2: Production-Ready Experiment (≤6k tokens)

**Extended validation with tool-specific configuration:**

1. **Enhanced steady-state definition**
   - Define multiple observability signals (Golden Signals: latency, traffic, errors, saturation)
   - Specify SLO-aligned thresholds
   - Include downstream dependency health checks
   - Configure Prometheus/Datadog queries for real-time validation

2. **Advanced failure scenario design**
   - Select from chaos engineering taxonomy (accessed 2025-10-25T21:30:36-04:00): https://principlesofchaos.org/
     - Infrastructure failures: instance termination, disk failure, network partition
     - Application failures: process crash, memory leak simulation, database connection pool exhaustion
     - Dependency failures: upstream service degradation, third-party API timeout
   - Define progressive escalation path: 1% → 5% → 25% → 50%

3. **Blast radius and safety controls**
   - Geographic boundaries: single AZ, multi-AZ, or multi-region
   - Service boundaries: leaf services before core platform services
   - Time boundaries: off-peak hours, maintenance windows
   - Automated abort triggers:
     - Steady state deviation > configured threshold (e.g., 15%)
     - Customer-facing SLO breach
     - Manual kill switch activation
   - Rollback procedures: immediate fault injection termination, traffic rerouting, instance replacement

4. **Generate tool-specific configuration**

   **For Kubernetes + Chaos Mesh:**
   - PodChaos for instance termination
   - NetworkChaos for latency/partition injection
   - StressChaos for resource exhaustion
   - IOChaos for disk failure simulation

   **For Kubernetes + LitmusChaos:**
   - ChaosExperiment CRD definition
   - ChaosEngine linking workload to fault
   - Probes for steady-state validation
   - ChaosResult for metrics export

   **For AWS + Chaos Monkey:**
   - ASG-scoped termination policies
   - Conformity Monkey for architectural validation
   - Simian Army integration

5. **Monitoring and reporting setup**
   - Pre-experiment baseline capture (15-30 minutes)
   - During-experiment real-time dashboards
   - Post-experiment comparison analysis
   - Prometheus metrics export for:
     - `chaos_experiment_duration_seconds`
     - `chaos_steady_state_deviation_percent`
     - `chaos_blast_radius_instances_affected`

6. **Experiment execution workflow**
   ```
   1. Baseline collection (pre-experiment)
   2. Fault injection start
   3. Continuous steady-state monitoring
   4. Auto-abort on threshold breach OR manual intervention
   5. Fault injection termination
   6. Recovery validation (post-experiment)
   7. Results analysis and report generation
   ```

**T2 deliverable:** Production-ready experiment with tool configs, safety controls, and monitoring integration.

**T2 sources:**
- Chaos Mesh fault types (accessed 2025-10-25T21:30:36-04:00): https://chaos-mesh.org/ - supports PodChaos, NetworkChaos, IOChaos, TimeChaos, StressChaos
- LitmusChaos CRD architecture (accessed 2025-10-25T21:30:36-04:00): https://litmuschaos.io/ - uses ChaosExperiment, ChaosEngine, ChaosResult custom resources
- Netflix best practices (accessed 2025-10-25T21:30:36-04:00): Start small (single node), enable monitoring first, gradual escalation, automate over time
- Google Cloud chaos engineering (accessed 2025-10-25T21:30:36-04:00): Build hypothesis around steady state, replicate real-world conditions, minimize blast radius

---

### Tier 3: Advanced Experiment Suite (≤12k tokens)

**Comprehensive resilience validation (use only when explicitly requested):**

1. **Multi-dimensional experiment matrix**
   - Combine failure modes: network partition + instance termination
   - Cascade scenarios: upstream dependency failure → downstream impact
   - Time-based variations: gradual degradation vs sudden failure
   - Geographic distribution: multi-region failover validation

2. **Automated experiment pipelines**
   - CI/CD integration for continuous chaos testing
   - GameDay automation with scheduled experiment runs
   - Regression testing for resilience (post-deployment validation)

3. **Advanced metrics and analysis**
   - MTTR (Mean Time To Recovery) calculation
   - Blast radius expansion rate
   - Failure propagation graph
   - Resilience score calculation

4. **Org-wide chaos engineering program**
   - Skill development and training plans
   - Runbook generation from experiments
   - Blameless postmortem templates
   - Chaos engineering maturity assessment

**T3 deliverable:** Enterprise-scale chaos engineering program with automation, metrics, and cultural integration.

## Decision Rules

**Experiment scope selection:**
- If system is new (<6 months in production) → T1 minimal experiment, non-production only
- If system has established monitoring + SLOs → T2 production experiment with 1-5% blast radius
- If mature resilience practice exists → T2 with progressive escalation to 25-50%
- If multi-team coordination needed → T3 with GameDay orchestration

**Tool selection:**
- If Kubernetes-native deployment → prefer Chaos Mesh or LitmusChaos
- If AWS EC2/ASG workloads → consider Chaos Monkey or AWS Fault Injection Simulator
- If multi-cloud or hybrid → Chaos Mesh (cloud-agnostic) or Gremlin (SaaS)
- If budget constraints → open-source LitmusChaos or Chaos Mesh over commercial Gremlin

**Safety thresholds:**
- **Abort if:** Steady-state deviation >15% OR customer SLO breach OR manual intervention
- **Start conservatively:** 1-5% blast radius, 5-minute duration
- **Escalate gradually:** 2x blast radius per iteration if previous experiment passed
- **Production readiness gate:** 3+ successful non-production experiments before production testing

**Ambiguity handling:**
- If steady-state metrics unclear → work with SRE/ops to define; emit TODO list
- If blast radius boundaries ambiguous → default to most conservative (1%, single AZ, leaf services)
- If rollback procedures undefined → restrict to non-production until procedures documented

## Output Contract

**Primary output: `experiment_plan` (JSON)**
```json
{
  "experiment_id": "string (unique identifier)",
  "hypothesis": {
    "steady_state": "string (measurable assertion)",
    "metrics": [
      {
        "name": "string (e.g., p95_latency_ms)",
        "baseline": "number (historical average)",
        "threshold": "number (max acceptable deviation)"
      }
    ]
  },
  "failure_injection": {
    "type": "string (pod-kill|network-delay|cpu-stress|region-failure)",
    "target": "string (service/component name)",
    "parameters": "object (tool-specific config)"
  },
  "blast_radius": {
    "scope": "string (service|AZ|region)",
    "percentage": "number (1-100)",
    "max_instances": "number"
  },
  "duration": "string (ISO 8601 duration, e.g., PT5M)",
  "abort_conditions": [
    "string (condition triggering experiment termination)"
  ],
  "rollback_procedure": "string (steps to restore normal state)"
}
```

**Secondary output: `implementation_config` (tool-specific YAML/JSON)**
- Chaos Mesh: PodChaos, NetworkChaos, or StressChaos YAML manifest
- LitmusChaos: ChaosExperiment, ChaosEngine CRDs
- Chaos Monkey: Configuration properties or API payloads

**Tertiary output: `safety_controls` (checklist)**
- [ ] Monitoring dashboards configured
- [ ] Alerting thresholds set
- [ ] Rollback runbook accessible
- [ ] Stakeholder notification plan
- [ ] Manual abort procedure documented
- [ ] Post-experiment cleanup steps defined

**Required fields:** All JSON schema fields above are mandatory. Missing fields → skill emits TODO and stops.

## Examples

**Example: Pod termination experiment for payment service**

```yaml
# Input
system_architecture: "Payment service (3 replicas) → Database (RDS)"
resilience_goals: "99.9% availability, P95 latency <200ms"
experiment_scope: "Payment service pods in staging, 1 pod max"
existing_monitoring: "Prometheus + Grafana, payment_request_duration_ms"

# Output (Chaos Mesh PodChaos)
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: payment-pod-kill-exp
  namespace: staging
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces:
      - staging
    labelSelectors:
      app: payment-service
  duration: 5m
  scheduler:
    cron: "@every 1h"  # Automated GameDay
```

## Quality Gates

**Token budgets (enforced):**
- T1: ≤2000 tokens (minimal experiment spec)
- T2: ≤6000 tokens (production-ready with tool config)
- T3: ≤12000 tokens (advanced suite + program design)

**Safety requirements:**
- Every experiment MUST define abort conditions
- Blast radius MUST be explicitly bounded
- Production experiments REQUIRE successful non-prod validation first

**Auditability:**
- All experiments logged with timestamp, executor, and results
- Changes to experiment parameters tracked in version control
- Results exported to observability platform (Prometheus/Datadog)

**Determinism:**
- Same experiment specification → reproducible results (within statistical variance)
- Randomized failure injection uses seeded RNG for replay capability

**Quality checklist:**
- [ ] Steady-state hypothesis is measurable and falsifiable
- [ ] Failure injection reflects real-world scenarios
- [ ] Blast radius minimizes customer impact
- [ ] Monitoring captures experiment success/failure
- [ ] Rollback procedure tested and documented

## Resources

**Official documentation:**
- Principles of Chaos Engineering (accessed 2025-10-25T21:30:36-04:00): https://principlesofchaos.org/
- Chaos Mesh documentation (accessed 2025-10-25T21:30:36-04:00): https://chaos-mesh.org/
- LitmusChaos framework (accessed 2025-10-25T21:30:36-04:00): https://litmuschaos.io/
- Netflix Chaos Monkey (accessed 2025-10-25T21:30:36-04:00): https://netflix.github.io/chaosmonkey/

**Templates and examples:**
- See `resources/experiment-template.yaml` for full experiment specification
- See `resources/blast-radius-config.json` for safety boundary examples

**Related skills:**
- `cloud-native-deployment-orchestrator` - for understanding Kubernetes deployment topology
- `devops-pipeline-architect` - for CI/CD integration of chaos experiments
- `sre-slo-calculator` - for defining steady-state thresholds aligned with SLOs
