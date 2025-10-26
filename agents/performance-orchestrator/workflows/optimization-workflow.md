# Performance Optimization Workflow

## Overview
4-step systematic workflow for performance optimization.

## Workflow Diagram
```
┌─────────────────────────────────────────────────────────┐
│               PERFORMANCE ORCHESTRATOR                  │
└─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         v               v               v
┌────────────────┐ ┌────────────┐ ┌─────────────────┐
│  1. PROFILING  │ │ 2. ANALYSIS│ │ 3. OPTIMIZATION │
│                │ │            │ │                 │
│ • Observability│ │ • Database │ │ • Quick wins    │
│ • CPU profiling│ │ • Caching  │ │ • DB indexes    │
│ • Memory trace │ │ • App code │ │ • App caching   │
│ • I/O analysis │ │ • Infra    │ │ • Rightsizing   │
└────────┬───────┘ └─────┬──────┘ └────────┬────────┘
         │               │                 │
         └───────────────┼─────────────────┘
                         │
                         v
              ┌──────────────────┐
              │  4. VALIDATION   │
              │                  │
              │ • Load testing   │
              │ • Metrics compare│
              │ • Monitoring     │
              │ • CI/CD tests    │
              └──────────────────┘
```

## Step 1: Profiling (≤3k tokens)

**Inputs:**
- Target system architecture
- Current performance metrics (baseline)
- Observability stack (or configure via skill)

**Process:**
1. Configure observability if needed (observability-stack-configurator)
2. Collect baseline metrics (latency, throughput, error rate, resource usage)
3. Identify bottleneck layers (database, application, infrastructure)
4. Profile bottlenecks with appropriate tools

**Outputs:**
- Bottleneck inventory with impact scores
- Profiling data (flame graphs, execution plans, traces)
- Top 3 optimization targets

## Step 2: Analysis (≤4k tokens)

**Inputs:**
- Bottleneck inventory from Step 1
- Profiling data

**Process:**
1. Database analysis (if DB bottleneck):
   - Invoke database-optimization-analyzer
   - Analyze query plans, identify N+1 queries, missing indexes
2. Caching analysis (if cache misses high):
   - Identify cacheable data
   - Design cache strategy (cache-aside, write-through)
3. Application analysis (if CPU/memory bottleneck):
   - Analyze hot paths, algorithmic inefficiencies
4. Infrastructure analysis (if resource constrained):
   - Invoke cost-optimization-analyzer for rightsizing

**Outputs:**
- Root cause analysis report
- Quantified impact estimates
- Implementation priority (high/medium/low)

## Step 3: Optimization (≤4k tokens)

**Inputs:**
- Root cause analysis from Step 2
- Optimization recommendations

**Process:**
1. Quick wins (0-1 day):
   - Add database indexes
   - Enable caching
   - Compression
2. Database optimizations (1-3 days):
   - Query rewrites
   - Read replicas
   - Connection pooling
3. Application optimizations (2-5 days):
   - Refactor hot paths
   - Batch processing
   - Async operations
4. Infrastructure optimizations (1-3 days):
   - Rightsizing
   - Auto-scaling
   - Caching layer deployment

**Outputs:**
- Implementation plan
- Code changes (DDL, configs, patches)
- Deployment sequence
- Rollback plan

## Step 4: Validation (≤4k tokens)

**Inputs:**
- Optimizations from Step 3
- Performance targets

**Process:**
1. Load testing (k6, JMeter, Gatling):
   - Baseline traffic pattern
   - Peak load (2x average)
   - Stress test (find breaking point)
   - Soak test (1-4 hours)
2. Compare before/after metrics
3. Configure regression prevention:
   - Continuous monitoring (alerts, dashboards)
   - CI/CD performance tests
4. Cost-performance analysis (ROI)

**Outputs:**
- Load testing report (before/after comparison)
- Performance dashboard configured
- CI/CD integration enabled
- Optimization summary with ROI

## Decision Points

### After Step 1 (Profiling)
- **Single bottleneck** → Quick optimization (T1)
- **Multiple bottlenecks** → Full workflow (T2/T3)
- **No bottleneck** → Targets met, abort

### After Step 2 (Analysis)
- **Quick fix available** → Implement and validate (T2)
- **Complex optimization** → Full implementation (T3)
- **Architecture limitation** → Escalate (T4)

### After Step 4 (Validation)
- **Targets met** → Success, document and close
- **Partial success (≥80%)** → Acceptable, monitor
- **Targets not met** → Escalate to architecture redesign

## Skill Coordination

| Step | Skills Invoked |
|------|----------------|
| Profiling | observability-stack-configurator (if needed) |
| Analysis | database-optimization-analyzer, cost-optimization-analyzer, edge-computing-architect |
| Optimization | container-image-optimizer (for container perf) |
| Validation | observability-stack-configurator (monitoring) |

## Example Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Profiling | 1-2 days | Observability setup, data collection, analysis |
| Analysis | 2-3 days | Root cause investigation, skill invocations |
| Optimization | 5-10 days | Implement fixes, test on staging |
| Validation | 2-3 days | Load testing, monitoring setup |
| **Total** | **10-18 days** | End-to-end workflow |
