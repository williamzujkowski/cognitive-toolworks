---
name: "Integration Testing Designer"
slug: integration-testing-designer
description: "Design integration test scenarios with database fixtures, external service mocks, contract testing, and test environment setup for microservices and APIs."
capabilities:
  - design_integration_scenarios
  - generate_database_fixtures
  - configure_service_mocks
  - setup_test_containers
  - design_contract_tests
  - create_test_environment
inputs:
  services:
    type: array
    description: "List of services under test with their dependencies"
    required: true
  dependencies:
    type: object
    description: "External dependencies (databases, APIs, message queues, third-party services)"
    required: true
  test_scope:
    type: string
    enum: ["smoke", "happy-path", "edge-cases", "full"]
    description: "Scope of integration testing coverage"
    required: true
  tech_stack:
    type: array
    description: "Testing frameworks and tools (JUnit, pytest, Jest, TestContainers)"
    required: false
outputs:
  test_scenarios:
    type: array
    description: "Integration test cases with setup, execution, and validation steps"
  fixtures:
    type: object
    description: "Database fixtures, mock configurations, and seed data"
  environment_setup:
    type: code
    description: "Docker Compose, TestContainers, or infrastructure configuration"
  contract_tests:
    type: array
    description: "Consumer-driven contract test specifications (Pact, Spring Cloud Contract)"
keywords:
  - integration-testing
  - testcontainers
  - database-fixtures
  - service-mocks
  - wiremock
  - pact
  - contract-testing
  - docker-compose
  - test-environment
  - api-testing
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: recommended
links:
  - https://testcontainers.com/
  - https://wiremock.org/
  - https://pact.io/
  - https://docs.spring.io/spring-boot/reference/testing/index.html
  - https://pytest.org/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Designing integration tests for microservices that interact with databases and external APIs
- Validating API contracts between services in a distributed system
- Setting up isolated test environments with real database instances
- Mocking external third-party services (payment gateways, notification services, webhooks)
- Testing message-driven architectures (Kafka, RabbitMQ, SQS)
- Validating database transactions, migrations, and data consistency
- Replacing brittle end-to-end tests with focused integration tests

**Use this skill when** you need to test service boundaries, validate integration points, ensure contract compatibility, or create reproducible test environments with real infrastructure dependencies.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T02:31:19-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `services` is non-empty array with service names
   - `dependencies` includes keys: `databases`, `apis`, `queues`, or `caches`
   - `test_scope` is one of: smoke, happy-path, edge-cases, full
   - `tech_stack` (if provided) contains valid testing framework identifiers
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify links resolve
4. **Docker availability**: Confirm Docker/Podman is available for TestContainers usage
5. **Dependency compatibility**: Verify mock tools support required protocols (REST, gRPC, GraphQL)

**Abort conditions:**

- Services description lacks clear dependency relationships
- Dependencies include proprietary systems without mock/stub capabilities
- Test scope is contradictory (e.g., "full coverage" with "no database access")
- Infrastructure constraints prevent container usage

---

## Procedure

### T1: Fast Path (≤2k tokens)

**Goal**: Generate basic integration test structure with database fixture and API mock.

1. **Identify integration points**:
   - Database dependencies (PostgreSQL, MySQL, MongoDB, Redis)
   - External HTTP APIs (REST, GraphQL)
   - Message queues (Kafka, RabbitMQ, SQS)
   - Third-party services (Stripe, Twilio, SendGrid)

2. **Select testing strategy** (based on [TestContainers Patterns](https://testcontainers.com/, accessed 2025-10-26)):
   - **Database**: TestContainers (real DB instance) vs. in-memory (H2, SQLite)
   - **HTTP APIs**: WireMock for deterministic responses
   - **Queues**: TestContainers with real broker for integration, mock for unit-level
   - **Third-party**: Mock webhooks and API responses

3. **Generate basic test structure**:
   ```java
   // Example: Spring Boot integration test
   @SpringBootTest
   @Testcontainers
   class PaymentServiceIntegrationTest {
     @Container
     static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");

     @Test
     void processPayment_withValidCard_createsTransaction() {
       // Arrange: seed database, mock Stripe
       // Act: call PaymentService
       // Assert: verify database state and external call
     }
   }
   ```

4. **Output test scenario outline**:
   - Test case name and description
   - Required fixtures (database records)
   - Mock configurations (API endpoints)
   - Expected outcomes (database state, external calls)

**Token budget**: ≤2k tokens

---

### T2: Extended Analysis (≤6k tokens)

**Goal**: Generate complete test scenarios, fixtures, mocks, and environment setup.

5. **Create database fixtures** (following [pytest fixtures](https://pytest.org/, accessed 2025-10-26) and [Spring Test](https://docs.spring.io/spring-boot/reference/testing/index.html, accessed 2025-10-26) patterns):
   - Seed data SQL/JSON files for initial state
   - Factory functions for test data generation
   - Cleanup strategies (transaction rollback, container disposal)
   - Migration application in test environment

6. **Configure service mocks** (using [WireMock](https://wiremock.org/, accessed 2025-10-26)):
   - Stub external API responses (success, failure, timeout)
   - Webhook simulation for callbacks
   - Request matching and verification
   - State-based mocking for complex scenarios

7. **Setup test environment**:
   - **Docker Compose**: Multi-container setup for CI/local development
   - **TestContainers**: Programmatic container lifecycle in tests
   - **Environment variables**: Database URLs, API keys (test mode)
   - **Network configuration**: Service discovery, port mapping

8. **Design contract tests** (following [Pact](https://pact.io/, accessed 2025-10-26) consumer-driven contract testing):
   - Consumer-side pact generation
   - Provider-side verification
   - Contract versioning and evolution
   - Pact broker integration for sharing contracts

9. **Generate test scenarios**:
   - **Happy path**: Successful integration with all dependencies
   - **Error handling**: Database failures, API timeouts, invalid responses
   - **Edge cases**: Concurrent requests, large payloads, rate limiting
   - **Data consistency**: Transaction rollback, eventual consistency

**Token budget**: ≤6k tokens total (including T1)

---

### T3: Deep Dive (≤12k tokens)

**Goal**: Add advanced integration patterns, performance considerations, and CI/CD integration.

10. **Advanced testing patterns**:
    - **Saga testing**: Multi-service transaction coordination
    - **Event-driven testing**: Message production and consumption verification
    - **Cache invalidation**: Redis/Memcached interaction testing
    - **Schema evolution**: Database migration testing with Flyway/Liquibase

11. **Performance and reliability**:
    - Connection pool configuration for test databases
    - Test parallelization with isolated database schemas
    - Flaky test mitigation (retry policies, wait strategies)
    - Resource cleanup and leak detection

12. **CI/CD integration**:
    - Container registry pre-pulling for faster test execution
    - Parallel test execution with Gradle/Maven/pytest-xdist
    - Test result aggregation and reporting
    - Integration test stage in pipeline (post-unit, pre-E2E)

13. **Documentation and maintenance**:
    - Test data management strategy
    - Mock service update procedures
    - Contract versioning guidelines
    - Troubleshooting guide for common failures

**Token budget**: ≤12k tokens total (including T1 + T2)

---

## Decision Rules

**Test scope adjustments:**

- **Smoke**: 3-5 critical path tests with minimal fixtures
- **Happy-path**: 10-15 tests covering primary workflows
- **Edge-cases**: Add 20-30 tests for error scenarios, boundaries, concurrency
- **Full**: Include performance, security, and chaos scenarios

**Database strategy selection:**

- **Use TestContainers when**:
  - Testing database-specific features (JSON columns, full-text search)
  - Validating complex queries and transactions
  - Testing migrations and schema changes
  - Production database is PostgreSQL, MySQL, MongoDB, or supported DB

- **Use in-memory database when**:
  - Simple CRUD operations with standard SQL
  - Fast feedback required (unit test-like speed)
  - CI environment has resource constraints
  - Database is abstracted through ORM

**Mock vs. Real service:**

- **Mock external APIs**: Payment gateways, email providers, SMS services
- **Use real services (containerized)**: Databases, message queues, caches
- **Use contract tests**: For services you control in same organization
- **Use sandbox/test environments**: For third-party services with test modes

**Effort estimation** (per integration point):

- Basic integration test: 2-4 hours
- Complex multi-service scenario: 6-12 hours
- Contract test setup: 4-8 hours
- TestContainers environment: 1-3 hours (initial), 30min (per additional service)

**Stop conditions:**

- If no external dependencies exist: redirect to unit testing
- If only UI-level integration needed: redirect to E2E testing skill
- If services lack clear boundaries: recommend architecture refactoring first

---

## Output Contract

**Required fields** (all outputs):

```typescript
interface IntegrationTestDesign {
  test_scenarios: Array<{
    name: string;
    description: string;
    services_under_test: string[];
    dependencies: string[];
    test_steps: Array<{
      step: string;
      action: string;
      expected_outcome: string;
    }>;
    fixtures_required: string[];
    mocks_required: string[];
  }>;

  fixtures: {
    database_seeds: Array<{
      table: string;
      format: "sql" | "json" | "yaml";
      content: string;
    }>;
    factory_functions?: string;  // Code snippet
  };

  environment_setup: {
    format: "docker-compose" | "testcontainers" | "kubernetes";
    content: string;             // YAML or code
    setup_instructions: string;
  };

  contract_tests?: Array<{
    consumer: string;
    provider: string;
    contract_format: "pact" | "spring-cloud-contract" | "openapi";
    interactions: Array<{
      description: string;
      request: object;
      response: object;
    }>;
  }>;

  mock_configurations: Array<{
    service_name: string;
    tool: "wiremock" | "mockserver" | "nock" | "responses";
    stubs: Array<{
      endpoint: string;
      method: string;
      response_body: object;
      status_code: number;
    }>;
  }>;
}
```

**Format**:

- `test_scenarios`: Array of objects with consistent structure
- `fixtures`: SQL/JSON with valid syntax
- `environment_setup`: Valid Docker Compose YAML or TestContainers code
- `contract_tests`: Pact-compatible JSON or Spring Cloud Contract DSL

**Validation**:

- All referenced fixtures exist in fixtures section
- All mocked services are in dependencies
- Database schema matches application models
- Port mappings don't conflict

---

## Examples

### Example 1: Payment API Integration Test (T2)

```yaml
INPUT:
  services: ["payment-api"]
  dependencies: {databases: ["postgres"], apis: ["stripe"]}
  test_scope: "happy-path"

OUTPUT:
  test_scenarios:
    - name: "Process payment and store transaction"
      test_steps:
        - "Setup: Start PostgreSQL, seed users, stub Stripe API"
        - "Execute: POST /payments with valid card"
        - "Assert: 201 response, transaction in DB, Stripe called"

  fixtures:
    database_seeds:
      - table: "users"
        content: "INSERT INTO users (id, email) VALUES (1, 'test@example.com');"

  mock_configurations:
    - service_name: "stripe"
      tool: "wiremock"
      stubs: [{endpoint: "/v1/charges", status: 200}]
```

---

## Quality Gates

**Token budgets** (mandatory):

- T1 ≤ 2k tokens (basic integration test structure)
- T2 ≤ 6k tokens (complete fixtures + mocks + environment)
- T3 ≤ 12k tokens (advanced patterns + CI/CD integration)

**Safety checks**:

- [ ] No production credentials in fixtures or mocks
- [ ] No real external API calls (all mocked or sandboxed)
- [ ] Database containers use non-persistent volumes in tests
- [ ] Cleanup code prevents resource leaks

**Auditability**:

- [ ] All sources cited with access date = `NOW_ET`
- [ ] Test data generation is deterministic and reproducible
- [ ] Mock responses match actual API documentation
- [ ] Container versions are pinned (not `latest`)

**Determinism**:

- [ ] Tests pass consistently with same inputs
- [ ] Database state is reset between tests
- [ ] Time-dependent logic uses fixed test time
- [ ] Random data generation uses fixed seeds

**Validation checklist**:

- [ ] Output JSON validates against schema
- [ ] Docker Compose YAML is valid (`docker-compose config`)
- [ ] SQL fixtures execute without errors
- [ ] Mock endpoints match API documentation
- [ ] TestContainers code compiles

---

## Resources

**Primary sources** (accessed 2025-10-26):

1. **TestContainers**: https://testcontainers.com/
   Lightweight, throwaway instances of databases, message brokers, and other services for integration testing.

2. **WireMock**: https://wiremock.org/
   Flexible API mocking tool for HTTP-based services with request matching and response stubbing.

3. **Pact**: https://pact.io/
   Consumer-driven contract testing framework for validating API interactions between services.

4. **Spring Boot Testing**: https://docs.spring.io/spring-boot/reference/testing/index.html
   Official Spring Boot testing documentation covering @SpringBootTest, MockMvc, and TestContainers integration.

5. **pytest**: https://pytest.org/
   Python testing framework with powerful fixtures and parametrization for integration testing.

**Additional templates**:

- See `examples/payment-integration-test.java` for complete Java example
- See `resources/docker-compose-test.yml` for multi-service test environment
- See `resources/pact-contract-example.json` for contract test template

**Related skills**:

- `testing-strategy-composer` (for overall testing strategy)
- `api-design-validator` (for API contract design)
- `database-optimization-analyzer` (for test database performance)

---

**End of SKILL.md**
