---
name: "Load Testing Scenario Designer"
slug: load-testing-designer
description: "Design load testing scenarios using k6, JMeter, Gatling, or Locust with ramp-up patterns, think time modeling, and performance SLI validation."
capabilities:
  - generate_load_test_scripts
  - design_ramp_up_patterns
  - model_think_time
  - validate_performance_sli
  - configure_distributed_load
inputs:
  target_service:
    type: string
    description: "URL or endpoint to test (e.g., https://api.example.com/checkout)"
    required: true
  test_type:
    type: enum
    description: "Type of load test to design"
    enum: ["load", "stress", "spike", "soak"]
    required: true
  sli_requirements:
    type: object
    description: "Performance SLI thresholds (p95_latency_ms, throughput_rps, error_rate_percent)"
    required: true
  tool:
    type: enum
    description: "Load testing tool to generate script for"
    enum: ["k6", "jmeter", "gatling", "locust"]
    required: false
    default: "k6"
  scenario_details:
    type: object
    description: "User count, duration, ramp-up time, think time distribution"
    required: false
outputs:
  test_script:
    type: code
    description: "Executable load test script for specified tool"
  test_config:
    type: json
    description: "Test configuration with VUs, duration, ramp-up, stages"
  assertions:
    type: json
    description: "SLI validation thresholds and success criteria"
  execution_plan:
    type: markdown
    description: "How to execute the test with prerequisites and validation steps"
keywords:
  - load-testing
  - performance-testing
  - k6
  - jmeter
  - gatling
  - locust
  - sli-validation
  - ramp-up
  - stress-testing
  - spike-testing
  - soak-testing
  - performance-engineering
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: recommended
links:
  - https://k6.io/docs/
  - https://grafana.com/docs/k6/latest/using-k6/
  - https://gatling.io/docs/
  - https://jmeter.apache.org/usermanual/
  - https://docs.locust.io/
  - https://sre.google/sre-book/monitoring-distributed-systems/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Validating application performance before production deployment
- Establishing performance baselines and capacity planning
- Testing system behavior under peak load, stress, or spike conditions
- Validating SLI/SLO compliance for latency, throughput, and error rates
- Simulating realistic user behavior with ramp-up and think time
- Testing distributed system resilience under sustained load (soak testing)

**Use this skill when** you need to design realistic, repeatable load testing scenarios with clear performance thresholds, appropriate ramp-up patterns, and tool-specific implementations for k6, JMeter, Gatling, or Locust.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T02:31:21-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `target_service` is a valid URL with protocol (http/https)
   - `test_type` is one of: load, stress, spike, soak
   - `sli_requirements` contains numeric values for at least one metric
   - `tool` (if provided) is one of: k6, jmeter, gatling, locust
   - `scenario_details` (if provided) has valid numeric ranges
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify links resolve
4. **Tool compatibility**: Confirm target service is accessible and testable

**Abort conditions:**

- Target service URL is unreachable or requires complex authentication not specified
- SLI requirements are contradictory (e.g., "10ms p95 latency" for external API)
- Test type and scenario details conflict (e.g., "spike test" with gradual ramp-up)
- Tool selection is incompatible with test requirements (e.g., complex distributed scenarios in basic Locust setup)

---

## Procedure

### T1: Fast Path (≤2k tokens)

**Goal**: Generate basic load test script with simple ramp-up and assertions.

1. **Parse inputs and apply defaults**:
   - Determine tool (default: k6)
   - Extract test type and map to pattern:
     - **load**: Gradual ramp-up to target VUs, sustain, ramp-down
     - **stress**: Gradual ramp-up beyond capacity to find breaking point
     - **spike**: Rapid jump to high VUs, sustain briefly, drop
     - **soak**: Low/moderate VUs sustained for extended duration
   - Parse SLI requirements (p95_latency_ms, throughput_rps, error_rate_percent)

2. **Generate basic test script** (k6 example per [k6 docs](https://k6.io/docs/, accessed 2025-10-26)):
   ```javascript
   import http from 'k6/http';
   import { check, sleep } from 'k6';

   export const options = {
     stages: [
       { duration: '2m', target: 100 },  // Ramp-up
       { duration: '5m', target: 100 },  // Sustain
       { duration: '2m', target: 0 },    // Ramp-down
     ],
     thresholds: {
       http_req_duration: ['p(95)<500'],  // 95% <500ms
       http_req_failed: ['rate<0.01'],     // <1% errors
     },
   };

   export default function () {
     const res = http.get('https://api.example.com/checkout');
     check(res, { 'status 200': (r) => r.status === 200 });
     sleep(1);  // Think time
   }
   ```

3. **Output initial configuration**:
   ```json
   {
     "test_config": {
       "tool": "k6",
       "virtual_users": 100,
       "duration_minutes": 9,
       "ramp_up_minutes": 2,
       "think_time_seconds": 1
     },
     "assertions": {
       "p95_latency_ms": 500,
       "error_rate_percent": 1
     }
   }
   ```

**Token budget**: ≤2k tokens

---

### T2: Extended Analysis (≤6k tokens)

**Goal**: Generate realistic scenarios with advanced patterns, distributed load, and comprehensive assertions.

4. **Design realistic ramp-up pattern** based on test type:
   - **Load test** (per [k6 Load Testing](https://grafana.com/docs/k6/latest/using-k6/, accessed 2025-10-26)):
     - Gradual ramp-up: 0 → target VUs over 10-20% of total test time
     - Sustain at target: 60-70% of total test time
     - Gradual ramp-down: 10-20% of total test time
   - **Stress test**:
     - Multi-stage ramp: 0 → 50% → 75% → 100% → 125% → 150% → find breaking point
     - Shorter sustain periods at each stage (2-3 minutes)
   - **Spike test**:
     - Instant jump: 0 → peak VUs in <30 seconds
     - Brief sustain: 1-2 minutes at peak
     - Instant drop: Return to baseline
   - **Soak test**:
     - Moderate VUs (50-70% of capacity)
     - Extended duration (2-24 hours)
     - Monitor for memory leaks, degradation

5. **Model think time distribution** (per [Google SRE Book - Load Testing](https://sre.google/sre-book/monitoring-distributed-systems/, accessed 2025-10-26)):
   - Use realistic user behavior patterns, not uniform sleep()
   - Apply randomization: `sleep(Math.random() * 3 + 1)` for 1-4s range
   - Consider page type: landing (5-10s), checkout (30-60s), browse (2-5s)
   - Add variance with percentile-based think time (p50: 3s, p90: 10s, p99: 30s)

6. **Map SLI requirements to tool-specific assertions**:
   - **k6**: Use `thresholds` object with percentile syntax
   - **JMeter**: Configure Assertions (Response Assertion, Duration Assertion)
   - **Gatling**: Use `assertions` DSL with percentile checks
   - **Locust**: Custom stats collection and failure conditions

7. **Generate tool-specific advanced script**:
   - Add request tagging/grouping for multi-endpoint scenarios
   - Include custom metrics (business transactions, funnel completion)
   - Configure distributed execution parameters if needed
   - Add data parameterization (CSV for users, JSON for payloads)
   - Reference [JMeter User Manual](https://jmeter.apache.org/usermanual/, accessed 2025-10-26) for JMeter-specific patterns
   - Reference [Gatling Documentation](https://gatling.io/docs/, accessed 2025-10-26) for Gatling DSL
   - Reference [Locust Documentation](https://docs.locust.io/, accessed 2025-10-26) for Locust class-based tests

**Token budget**: ≤6k tokens total (including T1)

---

### T3: Deep Dive (≤12k tokens)

**Goal**: Advanced patterns including distributed load, custom protocols, and comprehensive monitoring integration.

8. **Design distributed load generation**:
   - **k6 Cloud/Enterprise**: Configure multiple load zones (US-East, US-West, EU-West)
   - **JMeter Distributed**: Master-slave configuration with RMI
   - **Gatling Enterprise**: Inject distribution across multiple nodes
   - **Locust Distributed**: Master-worker architecture with load distribution

9. **Add advanced test patterns**:
   - **Breakpoint testing**: Incrementally increase load until system breaks
   - **Capacity testing**: Find maximum sustainable throughput
   - **Endurance patterns**: Multi-day soak with scheduled load variations
   - **Recovery testing**: Inject load spikes, measure recovery time

10. **Integrate with observability stack** (per [Google SRE - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/, accessed 2025-10-26)):
    - Configure Prometheus remote-write for k6 metrics
    - Set up Grafana dashboards for real-time visualization
    - Add CloudWatch/Datadog integration for cloud metrics correlation
    - Configure distributed tracing correlation (OpenTelemetry)

11. **Generate comprehensive execution plan**:
    - Pre-test validation: Smoke test, baseline collection
    - Test execution: Monitoring checklist, abort criteria
    - Post-test analysis: Report generation, SLI compliance validation
    - Iterative tuning: Adjust VUs/duration based on results

**Token budget**: ≤12k tokens total (including T1 + T2)

---

## Decision Rules

**Test type selection guidance:**

- **Load test**: Normal expected traffic + 20-50% headroom
- **Stress test**: 2-3x expected peak load to find breaking point
- **Spike test**: 5-10x sudden traffic surge (flash sale, DDoS simulation)
- **Soak test**: 50-70% capacity sustained 2-24 hours (memory leak detection)

**VU calculation** (requests per second → virtual users):

```
VUs = (target_RPS × response_time_seconds) / (1 - think_time_ratio)

Example:
- Target: 1000 RPS
- Response time: 200ms (0.2s)
- Think time: 1s per request
- VUs = (1000 × 0.2) / (1 - 0.83) = 200 / 0.17 ≈ 1176 VUs
```

**Tool selection matrix:**

| Feature | k6 | JMeter | Gatling | Locust |
|---------|-----|---------|---------|--------|
| Ease of use | High | Medium | Medium | High |
| Protocol support | HTTP/WebSocket/gRPC | Any (plugins) | HTTP/WebSocket/JMS | HTTP/Custom |
| Distributed | Cloud/Enterprise | Built-in (RMI) | Enterprise | Built-in |
| Scripting | JavaScript | GUI + Groovy | Scala DSL | Python |
| Best for | Modern APIs, DevOps | Legacy/complex protocols | JVM apps, high load | Python devs, simple APIs |

**SLI threshold recommendations** (from [Google SRE Book](https://sre.google/sre-book/monitoring-distributed-systems/, accessed 2025-10-26)):

- **Latency**: p50 <100ms, p95 <500ms, p99 <1s (API endpoints)
- **Throughput**: Based on capacity planning (RPS per instance × instance count)
- **Error rate**: <0.1% (four nines reliability), <1% (three nines)
- **Availability**: 99.9% (43.2 min/month downtime), 99.95% (21.6 min/month)

**Stop conditions:**

- If target service returns 5xx errors during smoke test: abort and fix service
- If SLI requirements are unattainable (require <10ms p95 for external API): renegotiate
- If test script complexity exceeds tool capabilities: recommend tool change

---

## Output Contract

**Required fields** (all outputs):

```typescript
interface LoadTestScript {
  tool: "k6" | "jmeter" | "gatling" | "locust";
  script_content: string;          // Executable test script
  script_language: string;         // "javascript", "xml", "scala", "python"
  entry_point: string;             // How to execute (e.g., "k6 run script.js")
}

interface TestConfig {
  tool: string;
  test_type: "load" | "stress" | "spike" | "soak";
  virtual_users: number | object;  // Number or stages array
  duration_minutes: number;
  ramp_up_pattern: Array<{
    stage: number;
    duration_seconds: number;
    target_vus: number;
  }>;
  think_time_config: {
    min_seconds: number;
    max_seconds: number;
    distribution: "uniform" | "normal" | "exponential";
  };
  distributed_config?: {
    enabled: boolean;
    load_zones?: string[];
    workers?: number;
  };
}

interface Assertions {
  latency_thresholds: {
    p50_ms?: number;
    p95_ms: number;
    p99_ms?: number;
  };
  throughput_threshold?: {
    min_rps: number;
  };
  error_rate_threshold: {
    max_percent: number;
  };
  custom_checks?: Array<{
    metric: string;
    operator: "lt" | "lte" | "gt" | "gte" | "eq";
    value: number;
  }>;
}

interface ExecutionPlan {
  prerequisites: string[];         // Required setup steps
  smoke_test_command: string;      // Pre-flight validation
  full_test_command: string;       // Main execution
  monitoring_checklist: string[];  // What to observe during test
  abort_criteria: string[];        // When to stop test early
  success_criteria: string[];      // How to validate results
  report_generation?: string;      // Post-test analysis steps
}
```

**Format**:

- `test_script`: Valid code for specified tool (JavaScript for k6, XML for JMeter, Scala for Gatling, Python for Locust)
- `test_config`: Valid JSON
- `assertions`: Valid JSON with numeric values
- `execution_plan`: Markdown with code blocks for commands

**Validation**:

- Script is syntactically valid for target tool
- VU counts and durations are positive integers
- Thresholds are achievable (p95 < p99, error_rate <100%)
- Think time min < max

---

## Examples

### Example 1: k6 E-Commerce Checkout Load Test (T2)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  stages: [
    { duration: '3m', target: 1000 },
    { duration: '10m', target: 1000 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<800'],
    http_req_failed: ['rate<0.005'],
    http_reqs: ['rate>500'],
  },
};
export default function () {
  const payload = JSON.stringify({
    cart_id: '123',
    payment: 'card'
  });
  const res = http.post(
    'https://api.example.com/checkout',
    payload,
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(res, {
    'status 200': (r) => r.status === 200,
    'checkout success': (r) => r.json('success')
  });
  sleep(Math.random() * 3 + 2);
}
```

---

## Quality Gates

**Token budgets** (mandatory):

- T1 ≤ 2k tokens (basic script + simple assertions)
- T2 ≤ 6k tokens (realistic scenarios + think time modeling)
- T3 ≤ 12k tokens (distributed load + monitoring integration)

**Safety checks**:

- [ ] No hardcoded credentials or API keys in test scripts
- [ ] No production data in test payloads (use synthetic/anonymized data)
- [ ] Load test targets are non-production environments (unless explicitly approved)
- [ ] Distributed tests include rate limiting to prevent accidental DDoS

**Auditability**:

- [ ] All sources cited with access date = `NOW_ET`
- [ ] VU calculations include methodology and assumptions
- [ ] SLI thresholds tied to business requirements or SRE standards
- [ ] Test results are reproducible with same script + config

**Determinism**:

- [ ] Same inputs produce same script structure (±10% VU variance acceptable)
- [ ] Ramp-up patterns follow documented heuristics
- [ ] Think time distributions use seeded randomness where possible

**Validation checklist**:

- [ ] Script executes without syntax errors
- [ ] Assertions align with SLI requirements
- [ ] VU count and duration are realistic for target infrastructure
- [ ] Think time modeling prevents unrealistic "robot" traffic

---

## Resources

**Primary sources** (accessed 2025-10-26):

1. **k6 Documentation**: https://k6.io/docs/
   Official k6 load testing tool documentation with test lifecycle, scripting, and thresholds.

2. **k6 Using Guide**: https://grafana.com/docs/k6/latest/using-k6/
   Comprehensive guide on test types, scenarios, executors, and distributed testing with k6.

3. **Gatling Documentation**: https://gatling.io/docs/
   Gatling load testing framework docs covering Scala DSL, simulation design, and reports.

4. **JMeter User Manual**: https://jmeter.apache.org/usermanual/
   Apache JMeter user manual with test plan creation, distributed testing, and protocols.

5. **Locust Documentation**: https://docs.locust.io/
   Locust Python-based load testing framework docs with distributed mode and custom tasks.

6. **Google SRE Book - Monitoring Distributed Systems**: https://sre.google/sre-book/monitoring-distributed-systems/
   Google SRE principles for SLI/SLO definition, load testing strategies, and performance validation.

**Additional templates**:

- See `examples/load-test-example.js` for complete k6 workflow example
- See `resources/jmeter-template.jmx` for JMeter test plan template
- See `resources/gatling-template.scala` for Gatling simulation template

**Related skills**:

- `sre-slo-calculator` (for defining SLI/SLO before load testing)
- `chaos-engineering-designer` (for resilience testing under load)
- `observability-stack-configurator` (for monitoring during load tests)

---

**End of SKILL.md**
