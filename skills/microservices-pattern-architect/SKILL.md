---
name: "Microservices Pattern Architect"
slug: "microservices-pattern-architect"
description: "Apply microservices patterns (Saga, CQRS, Event Sourcing, Circuit Breaker, API Gateway, Service Discovery) with implementation guidance and templates."
capabilities:
  - Saga pattern for distributed transactions with choreography and orchestration
  - CQRS implementation with command/query separation and eventual consistency
  - Event Sourcing with event store design and event replay mechanisms
  - Circuit Breaker pattern for fault tolerance and graceful degradation
  - API Gateway pattern for request routing, composition, and protocol translation
  - Service Discovery with client-side and server-side approaches
  - Pattern composition recommendations for complex scenarios
  - Anti-pattern detection and remediation guidance
  - Event schema design and versioning strategies
  - Implementation templates for popular frameworks
inputs:
  - scenario: "distributed transaction, data consistency, fault tolerance, api composition, service location (string)"
  - architecture_context: "existing services, data stores, communication patterns (object)"
  - deployment_tier: "T1 (quick) | T2 (extended) (string, default: T1)"
  - framework_preference: "spring-boot, nodejs, .net, go, python (string, optional)"
  - scalability_requirements: "throughput, latency, availability SLOs (object, optional)"
outputs:
  - pattern_recommendation: "Primary pattern with justification and trade-offs"
  - implementation_template: "Code scaffolding or configuration for selected framework"
  - event_schemas: "Event definitions with versioning strategy (if applicable)"
  - integration_guidance: "Step-by-step implementation plan with decision points"
  - anti_patterns: "Common pitfalls and how to avoid them"
  - monitoring_strategy: "Observability requirements for the pattern (T2 only)"
keywords:
  - microservices
  - saga
  - cqrs
  - event-sourcing
  - circuit-breaker
  - api-gateway
  - service-discovery
  - distributed-transactions
  - eventual-consistency
  - fault-tolerance
  - resilience
  - choreography
  - orchestration
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://microservices.io/patterns/index.html
  - https://martinfowler.com/microservices/
  - https://learn.microsoft.com/en-us/azure/architecture/microservices/design/patterns
  - https://microservices.io/patterns/data/saga.html
  - https://microservices.io/patterns/data/event-sourcing.html
  - https://microservices.io/patterns/reliability/circuit-breaker.html
---

## Purpose & When-To-Use

**Trigger conditions:**
- Distributed transaction spans multiple microservices without 2PC/XA
- Need for separate read/write optimization in high-scale scenarios (CQRS)
- Audit trail, temporal queries, or event replay requirements (Event Sourcing)
- Service-to-service calls require fault tolerance and graceful degradation
- Multiple client types need unified API entry point with protocol translation
- Dynamic service instance discovery in cloud-native or container environments
- Migration from monolith to microservices requires pattern guidance
- Complex scenario requires multiple pattern composition
- Existing microservices architecture shows anti-patterns or performance issues

**Not for:**
- Single-service applications or true monoliths (use simpler patterns)
- ACID transaction requirements without compensation logic tolerance
- Real-time consistency requirements (patterns focus on eventual consistency)
- Greenfield projects without clear service boundaries (define domains first)
- Infrastructure concerns only (use cloud-native-deployment-orchestrator)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `scenario` must be one of: distributed transaction, data consistency, fault tolerance, api composition, service location, or a combination
- `architecture_context` must describe: existing services, communication patterns, data stores
- `deployment_tier` must be: T1 or T2
- `framework_preference` if specified must be: spring-boot, nodejs, .net, go, or python
- `scalability_requirements` if provided must include at least one SLO metric

**Source freshness:**
- Microservices.io Patterns (accessed 2025-10-25T21:30:36-04:00): https://microservices.io/patterns/index.html - Chris Richardson's pattern catalog, updated 2025
- Martin Fowler Microservices Guide (accessed 2025-10-25T21:30:36-04:00): https://martinfowler.com/microservices/ - foundational principles and patterns
- Microsoft Azure Microservices Patterns (accessed 2025-10-25T21:30:36-04:00): https://learn.microsoft.com/en-us/azure/architecture/microservices/design/patterns - updated September 2025
- Saga Pattern Reference (accessed 2025-10-25T21:30:36-04:00): https://microservices.io/patterns/data/saga.html - choreography vs orchestration guidance
- Event Sourcing Pattern (accessed 2025-10-25T21:30:36-04:00): https://microservices.io/patterns/data/event-sourcing.html - event store design principles
- Circuit Breaker Pattern (accessed 2025-10-25T21:30:36-04:00): https://microservices.io/patterns/reliability/circuit-breaker.html - fault tolerance mechanisms

**Abort conditions:**
- If `architecture_context` is missing or too vague, request service inventory with data flows
- If scenario requires strong ACID guarantees without compensation tolerance, recommend monolith or distributed DB
- If no clear service boundaries exist, invoke architecture-decision-framework skill first

---

## Procedure

### T1: Pattern Recommendation (≤2k tokens)

**Step 1: Scenario Analysis**
- Parse `scenario` to identify primary concern: transactions, consistency, resilience, routing, or discovery
- Map scenario to pattern family:
  - Distributed transaction → **Saga** (choreography or orchestration)
  - Data consistency + scale → **CQRS** with optional Event Sourcing
  - Audit/replay/temporal → **Event Sourcing** with CQRS
  - Fault tolerance → **Circuit Breaker** with Bulkhead and Timeout
  - API unification → **API Gateway** with BFF (Backend for Frontend) variant
  - Service location → **Service Discovery** (client-side or server-side)

**Step 2: Quick Pattern Selection**
- **Saga** if: Multi-service transaction with compensating actions acceptable
  - Choose **Choreography** if: loosely coupled, event-driven architecture preferred
  - Choose **Orchestration** if: centralized control, complex workflow, easier debugging
- **CQRS** if: Read/write workloads differ significantly (>10x scale difference)
  - Add Event Sourcing if: audit trail or temporal queries required
- **Circuit Breaker** if: Service calls to unreliable dependencies (external APIs, legacy services)
  - Configure: Failure threshold (e.g., 50% errors in 10s window), timeout (e.g., 2s), half-open retry
- **API Gateway** if: Multiple client types (web, mobile, IoT) or cross-cutting concerns (auth, rate limiting)
  - Use **BFF** variant if: client-specific optimizations needed
- **Service Discovery** if: Dynamic service instances (Kubernetes, AWS ECS, service mesh)
  - Client-side (Ribbon, Eureka client) vs Server-side (Consul, Kubernetes DNS)

**Step 3: Quick Recommendation Output**
- Pattern name and one-line justification
- Primary trade-off (e.g., "Saga: eventual consistency for distributed scalability")
- Implementation complexity estimate (low, medium, high)
- Link to pattern template in resources/ folder

**T1 Token Budget: ≤2k tokens**

---

### T2: Extended Implementation Guidance (≤6k tokens)

**Includes T1, plus:**

**Step 4: Pattern Deep-Dive**

**For Saga Pattern:**
- Design compensating transactions for each step (idempotent, retryable)
- Choreography: event schema design with event types (OrderCreated, PaymentProcessed, ShipmentScheduled)
  - Use message broker (Kafka, RabbitMQ, AWS EventBridge) for event bus
  - Each service subscribes to events and publishes new events
  - Example: Order Service → OrderCreated event → Payment Service → PaymentProcessed event
- Orchestration: central coordinator (state machine) manages saga workflow
  - Use orchestrator service (Temporal, Camunda, AWS Step Functions)
  - Maintains saga state and invokes services via commands/queries
  - Easier debugging with centralized logs and state visibility
- Failure handling: timeout, retry with exponential backoff, compensation trigger
- Monitoring: distributed tracing (OpenTelemetry) for saga correlation ID

**For CQRS Pattern:**
- Command model: write operations with domain validation and business logic
  - Commands: CreateOrder, UpdateInventory (imperative, intent-revealing)
  - Command handlers: validate, apply business rules, persist state, publish events
- Query model: read-optimized projections (denormalized, materialized views)
  - Queries: GetOrderDetails, SearchProducts (declarative, data retrieval)
  - Query handlers: read from projection store (Redis, Elasticsearch, read replicas)
- Synchronization: eventual consistency via events (Event Sourcing or CDC)
  - Command side publishes domain events → Query side consumes and updates projections
  - Acceptable staleness window (e.g., <1s for most cases)
- Data stores: Write store (PostgreSQL, DynamoDB) vs Read store (Redis, MongoDB, Elasticsearch)

**For Event Sourcing:**
- Event store design: append-only log of immutable events (EventStoreDB, Kafka, DynamoDB Streams)
  - Event schema: { eventId, aggregateId, eventType, timestamp, payload, metadata }
  - Versioning: semantic versioning for event types with upcasting for old versions
- Event replay: rebuild current state by replaying events from beginning or snapshot
  - Snapshots: periodic state snapshots to avoid full replay (e.g., every 100 events)
- CQRS integration: events feed into read models (projections)
  - Projection rebuilding: replay events to create new projections or fix corrupted ones
- Event schema evolution: use event versioning and transformers for backward compatibility

**For Circuit Breaker:**
- States: Closed (normal), Open (failing, reject requests), Half-Open (testing recovery)
  - Closed → Open: threshold (e.g., 5 failures in 10s) exceeded
  - Open → Half-Open: after timeout period (e.g., 30s)
  - Half-Open → Closed: successful request
  - Half-Open → Open: failure on test request
- Fallback strategies: cached response, default value, graceful degradation, error message
- Libraries: Resilience4j (Java), Polly (.NET), Hystrix (deprecated, use Resilience4j), opossum (Node.js)
- Monitoring: circuit state changes, failure rates, fallback invocations

**For API Gateway:**
- Responsibilities: routing, composition, protocol translation (REST→gRPC), auth, rate limiting
- Patterns:
  - **Gateway Routing**: simple request forwarding to backend services
  - **Gateway Aggregation**: combine multiple backend calls into single response (avoid N+1)
  - **Gateway Offloading**: cross-cutting concerns (SSL termination, auth, logging, CORS)
- BFF (Backend for Frontend): separate gateway per client type (web, mobile, IoT)
  - Web BFF: rich data with nested objects
  - Mobile BFF: minimal payloads, paginated responses
- Implementations: Kong, AWS API Gateway, Azure API Management, Spring Cloud Gateway, Envoy

**For Service Discovery:**
- Client-side: service calls discovery client (Eureka, Consul client) to get instance list, then load balances
  - Pros: eliminates network hop, faster
  - Cons: client complexity, SDK per language
- Server-side: service calls load balancer/DNS, which queries registry and routes
  - Pros: client simplicity, language-agnostic
  - Cons: extra network hop, single point of failure (mitigated with HA)
- Implementations: Kubernetes DNS (server-side), Consul, Eureka (Netflix OSS), etcd, Zookeeper
- Health checks: heartbeat, HTTP/gRPC health endpoint, container liveness probes

**Step 5: Implementation Template Generation**
- Provide code scaffolding for `framework_preference` (if specified)
- Spring Boot example: @Saga annotation, Axon Framework for CQRS/ES
- Node.js example: NestJS with CQRS module, event-driven microservices
- .NET example: MediatR for CQRS, MassTransit for Saga orchestration
- Go example: go-kit for microservices, NATS for event streaming
- Python example: FastAPI with event-driven patterns, Celery for async tasks

**Step 6: Anti-Patterns and Pitfalls**
- **Saga**: missing compensation logic, non-idempotent operations, unbounded retries
- **CQRS**: overuse for simple CRUD, ignoring eventual consistency UX implications
- **Event Sourcing**: no snapshots (slow replay), poor event schema versioning
- **Circuit Breaker**: timeout too long/short, no fallback, ignoring half-open testing
- **API Gateway**: monolithic gateway (becomes bottleneck), tight coupling to backends
- **Service Discovery**: stale registrations (insufficient health checks), no deregistration on shutdown

**Step 7: Observability and Monitoring Strategy**
- Distributed tracing: correlation IDs across service boundaries (OpenTelemetry, Jaeger, Zipkin)
- Metrics: pattern-specific metrics
  - Saga: saga duration, compensation rate, failure rate per step
  - CQRS: command latency, query latency, projection lag
  - Event Sourcing: event store write throughput, replay duration
  - Circuit Breaker: circuit state, failure rate, fallback invocation rate
  - API Gateway: request rate, latency percentiles (p50, p95, p99), error rate
  - Service Discovery: instance count, registration/deregistration rate, health check failures
- Logging: structured logs with context (service, correlation ID, pattern name)
- Alerting: pattern-specific alerts (e.g., circuit open >5min, projection lag >10s)

**Step 8: Integration with Deployment Patterns**
- Reference cloud-native-deployment-orchestrator for Kubernetes manifests
- Sidecar pattern for cross-cutting concerns (Envoy proxy for Circuit Breaker via Istio)
- Service mesh integration: Istio/Linkerd for traffic management, observability, resilience

**T2 Token Budget: ≤6k tokens (cumulative with T1)**

---

## Decision Rules

**Pattern Selection Decision Tree:**
1. **If distributed transaction required:**
   - Can tolerate eventual consistency? → **Saga** (choreography if loosely coupled, orchestration if complex workflow)
   - Require strong consistency? → Abort; recommend monolith or distributed database with 2PC
2. **If read/write scale mismatch (>10x):**
   - Need audit trail or temporal queries? → **CQRS + Event Sourcing**
   - Just need read optimization? → **CQRS** alone with CDC or polling
3. **If fault tolerance for external dependencies:**
   - Unpredictable failures, need graceful degradation? → **Circuit Breaker** + Bulkhead + Timeout
4. **If multiple client types or cross-cutting concerns:**
   - Client-specific optimizations? → **API Gateway** with **BFF** variant
   - Just routing/auth/rate limiting? → **API Gateway** (simple routing)
5. **If dynamic service instances in cloud/containers:**
   - Need language-agnostic discovery? → **Service Discovery** (server-side: Kubernetes DNS, Consul)
   - Can embed client library? → **Service Discovery** (client-side: Eureka, Ribbon)

**Composition Rules:**
- **Saga + Event Sourcing**: events from Event Store feed Saga choreography
- **CQRS + Event Sourcing**: events update both command model and query projections
- **API Gateway + Circuit Breaker**: gateway implements circuit breaker for backend calls
- **Service Discovery + API Gateway**: gateway discovers backend service instances dynamically

**Abort/Stop Conditions:**
- If `architecture_context` lacks service boundaries → invoke architecture-decision-framework
- If real-time consistency required without compensation → recommend alternative (monolith, distributed DB)
- If scenario is too vague → request clarification with specific services and data flows
- If no `framework_preference` and T2 requested → provide polyglot pseudo-code instead

---

## Output Contract

**Required fields (all tiers):**
```json
{
  "pattern_recommendation": {
    "primary_pattern": "Saga | CQRS | Event Sourcing | Circuit Breaker | API Gateway | Service Discovery",
    "variant": "choreography | orchestration | BFF | client-side | server-side (optional)",
    "justification": "Why this pattern fits the scenario (1-2 sentences)",
    "trade_offs": {
      "pros": ["list of advantages"],
      "cons": ["list of disadvantages and constraints"]
    },
    "complexity": "low | medium | high"
  },
  "implementation_template": {
    "language": "spring-boot | nodejs | .net | go | python | polyglot (string)",
    "code_scaffolding": "File path to resources/ template or inline code snippet",
    "dependencies": ["list of required libraries/frameworks"]
  },
  "anti_patterns": [
    {
      "name": "anti-pattern name",
      "description": "what to avoid",
      "mitigation": "how to avoid it"
    }
  ],
  "integration_guidance": {
    "steps": ["ordered list of implementation steps"],
    "decision_points": ["key decisions to make during implementation"]
  }
}
```

**Additional fields (T2 only):**
```json
{
  "event_schemas": [
    {
      "event_type": "EventName",
      "version": "1.0.0",
      "schema": { "json schema or example payload" },
      "versioning_strategy": "semantic | append-only | upcasting"
    }
  ],
  "monitoring_strategy": {
    "metrics": ["pattern-specific metrics to track"],
    "traces": "distributed tracing requirements",
    "alerts": ["recommended alert conditions"]
  },
  "deployment_integration": {
    "kubernetes_resources": "ConfigMap, Service, Deployment annotations",
    "service_mesh_config": "Istio VirtualService, DestinationRule (if applicable)"
  }
}
```

---

## Examples

**Example: Saga Pattern for Order Processing**

```yaml
# Input
scenario: distributed transaction
architecture_context:
  services:
    - OrderService: manages orders
    - PaymentService: processes payments
    - InventoryService: reserves stock
    - ShipmentService: schedules shipping
  communication: REST APIs
deployment_tier: T1

# Output
pattern_recommendation:
  primary_pattern: Saga
  variant: choreography
  justification: "Event-driven choreography allows loosely coupled services to coordinate order fulfillment with compensating transactions for failures."
  trade_offs:
    pros:
      - "Loosely coupled services"
      - "No single point of failure"
      - "Natural fit for event-driven architecture"
    cons:
      - "Harder to debug distributed flow"
      - "Eventual consistency requires UX consideration"
  complexity: medium
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2k tokens (pattern recommendation, quick template link)
- **T2**: ≤6k tokens (deep-dive, implementation templates, monitoring strategy)
- **T3**: Not implemented for this skill (T2 sufficient for pattern architecture guidance)

**Safety:**
- No secrets or credentials in templates
- All code examples use placeholder values (e.g., `your-api-key`, `localhost`)
- References to external tools include version constraints (e.g., Resilience4j 2.x)

**Auditability:**
- All pattern recommendations cite source (microservices.io, Martin Fowler, Microsoft)
- Decision tree explicitly documented in Decision Rules section
- Timestamp all source access dates with `NOW_ET`

**Determinism:**
- Same `scenario` + `architecture_context` → same primary pattern recommendation
- Framework templates deterministically selected based on `framework_preference`
- Pattern composition rules explicitly defined in Decision Rules

**Quality checks:**
- Pattern recommendation must include trade-offs (pros/cons)
- Implementation template must include dependencies list
- Anti-patterns section must cover top 3 pitfalls for selected pattern
- T2 must include observability strategy with metrics and alerts

---

## Resources

**Pattern Catalogs:**
- Microservices.io Patterns: https://microservices.io/patterns/index.html (comprehensive catalog by Chris Richardson)
- Martin Fowler Microservices Guide: https://martinfowler.com/microservices/ (foundational principles)
- Microsoft Azure Microservices Patterns: https://learn.microsoft.com/en-us/azure/architecture/microservices/design/patterns (cloud-native focus)

**Pattern-Specific References:**
- Saga Pattern: https://microservices.io/patterns/data/saga.html (choreography vs orchestration)
- CQRS Pattern: https://martinfowler.com/bliki/CQRS.html (command-query separation)
- Event Sourcing: https://microservices.io/patterns/data/event-sourcing.html (event store design)
- Circuit Breaker: https://microservices.io/patterns/reliability/circuit-breaker.html (fault tolerance)
- API Gateway: https://microservices.io/patterns/apigateway.html (routing and composition)
- Service Discovery: https://microservices.io/patterns/server-side-discovery.html (client-side vs server-side)

**Implementation Frameworks:**
- Axon Framework (Java): https://axoniq.io/ (CQRS, Event Sourcing, Saga)
- MassTransit (.NET): https://masstransit.io/ (Saga orchestration, message bus)
- Temporal (polyglot): https://temporal.io/ (workflow orchestration for sagas)
- Resilience4j (Java): https://resilience4j.readme.io/ (Circuit Breaker, Bulkhead, Retry)
- Polly (.NET): https://github.com/App-vNext/Polly (resilience and transient-fault-handling)

**Templates (see resources/ folder):**
- `saga-choreography-template.yaml`: Event-driven saga with compensations
- `saga-orchestration-template.yaml`: Central coordinator saga pattern
- `cqrs-event-sourcing-template.yaml`: Combined CQRS + Event Sourcing
- `circuit-breaker-config.yaml`: Resilience4j/Polly configuration examples
- `api-gateway-routes.yaml`: Kong/Spring Cloud Gateway route definitions
- `event-schemas/`: Sample event schemas with versioning

**Books and Courses:**
- "Microservices Patterns" by Chris Richardson (Manning, 2nd edition MEAP 2025)
- "Building Microservices" by Sam Newman (O'Reilly, 2nd edition)
- Event-Driven Microservices with CQRS, Saga, Event Sourcing (Udemy course)
