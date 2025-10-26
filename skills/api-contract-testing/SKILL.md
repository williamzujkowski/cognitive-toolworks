---
name: "API Contract Testing Validator"
slug: api-contract-testing
description: "Generate and validate API contract tests using Pact, Spring Cloud Contract, or OpenAPI with consumer-driven contracts and schema drift detection."
capabilities:
  - generate_consumer_tests
  - generate_provider_verification
  - validate_contract_schema
  - detect_breaking_changes
  - integrate_ci_pipeline
inputs:
  api_spec:
    type: object
    description: "OpenAPI/Swagger spec, service description, or contract DSL"
    required: true
  role:
    type: enum
    description: "consumer | provider"
    required: true
  framework:
    type: enum
    description: "pact | spring-contract | openapi"
    required: true
  language:
    type: string
    description: "Target language (e.g., java, javascript, python, go)"
    required: false
outputs:
  contract_tests:
    type: code
    description: "Consumer or provider test implementation"
  contract_spec:
    type: json
    description: "Pact JSON contract or contract DSL"
  ci_integration:
    type: yaml
    description: "Pipeline configuration for contract verification"
  validation_report:
    type: markdown
    description: "Schema compatibility and breaking change analysis"
keywords:
  - api-testing
  - contract-testing
  - consumer-driven-contracts
  - pact
  - spring-cloud-contract
  - openapi
  - schema-validation
  - breaking-changes
  - integration-testing
  - microservices
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: recommended
links:
  - https://docs.pact.io/
  - https://spring.io/projects/spring-cloud-contract
  - https://spec.openapis.org/oas/v3.1.0
  - https://swagger.io/docs/specification/about/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Microservices communicating via REST/GraphQL APIs requiring contract guarantees
- Mobile or web frontend consuming backend APIs with version safety requirements
- API provider needing to verify backward compatibility before deployment
- CI/CD pipeline requiring automated contract verification gates
- Team transitioning from manual integration tests to consumer-driven contracts
- Schema evolution requiring breaking change detection

**Use this skill when** you need to establish or validate API contracts between consumers and providers, detect schema drift, prevent breaking changes, and integrate contract testing into CI/CD pipelines.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T06:31:34-04:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `api_spec` is valid OpenAPI 3.x JSON/YAML, service description, or contract DSL
   - `role` is exactly "consumer" or "provider"
   - `framework` is exactly "pact", "spring-contract", or "openapi"
   - `language` (if provided) is supported by chosen framework
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify links resolve
4. **Framework availability**: Confirm framework tooling available for target language

**Abort conditions:**

- `api_spec` is invalid JSON/YAML or missing required fields (paths, operations)
- `framework` and `language` combination not supported (e.g., Pact with COBOL)
- No clear consumer-provider relationship identifiable from spec
- Circular contract dependencies detected

---

## Procedure

### T1: Basic Contract Test Generation (≤2k tokens)

**Scope**: Generate minimal consumer or provider contract test for single endpoint.

**Steps**:

1. **Parse `api_spec`**: Extract endpoint path, method, request/response schema
2. **Select template**: Choose framework-specific test template (Pact DSL, Spring Contract DSL, or OpenAPI validator)
3. **Generate test code**:
   - **Consumer (Pact)**: Mock provider, define interaction, verify request/response
   - **Provider (Pact)**: Verify against published consumer contracts
   - **OpenAPI**: Generate request/response validation using OpenAPI schema
4. **Output**: Minimal runnable test file with single interaction

**Example output**: Pact consumer test for GET /users/:id endpoint (JavaScript).

---

### T2: Multi-Endpoint Verification with CI Integration (≤6k tokens)

**Scope**: Generate comprehensive contract tests for 3-5 endpoints with CI pipeline integration.

**Steps**:

1. **Endpoint analysis**: Identify all consumer-provider interactions from `api_spec`
2. **Generate test suite**:
   - **Consumer**: Full test suite covering happy path, edge cases, error responses
   - **Provider**: Verification tests against all published consumer contracts
3. **Breaking change detection**:
   - Compare new `api_spec` against existing contract (if available)
   - Flag removed endpoints, changed response schemas, new required fields
4. **CI integration**:
   - Generate pipeline YAML (GitHub Actions, GitLab CI, Jenkins)
   - Include contract publish/verify steps, Pact Broker integration
   - Add gates for breaking change detection
5. **Output**: Test suite + CI config + compatibility report

**Sources** (accessed 2025-10-26T06:31:34-04:00):

- Pact documentation: [Consumer-Driven Contracts](https://docs.pact.io/getting_started/what_is_pact)
- Spring Cloud Contract: [Contract DSL Reference](https://spring.io/projects/spring-cloud-contract#overview)
- OpenAPI Specification: [Schema Object](https://spec.openapis.org/oas/v3.1.0#schema-object)
- Pact Broker: [Sharing Pacts](https://docs.pact.io/pact_broker)

---

### T3: Schema Evolution and Advanced Validation (≤12k tokens)

**Scope**: Deep analysis of schema evolution, versioning strategies, and contract governance.

**Steps**:

1. **Historical contract analysis**: Load previous contract versions, compute diff
2. **Breaking change taxonomy**:
   - **Critical**: Removed endpoints, deleted required fields, type changes
   - **Warning**: New required fields without defaults, renamed fields
   - **Safe**: New optional fields, added endpoints, relaxed constraints
3. **Versioning strategy**:
   - Recommend approach: URL versioning, header versioning, or content negotiation
   - Generate migration path for breaking changes
4. **Contract governance**:
   - Define approval workflow (provider must verify consumer contracts before deploy)
   - Set up Pact Broker webhooks for contract change notifications
   - Generate compatibility matrix (which consumer versions work with which provider versions)
5. **Advanced testing scenarios**:
   - State-based testing (Pact provider states)
   - Message queue contracts (Pact for async messaging)
   - GraphQL schema stitching contracts
6. **Output**: Comprehensive report + versioning plan + governance workflow + advanced test examples

**Additional sources** (accessed 2025-10-26T06:31:34-04:00):

- Pact versioning: [Versioning with Pact](https://docs.pact.io/getting_started/versioning_in_the_pact_broker)
- API evolution best practices: [Zalando API Guidelines - Compatibility](https://opensource.zalando.com/restful-api-guidelines/#deprecation)

---

## Decision Rules

**Framework selection**:

- **Use Pact** when: Consumer-driven workflow, polyglot environment, Pact Broker available
- **Use Spring Cloud Contract** when: Spring Boot ecosystem, provider-driven workflow preferred
- **Use OpenAPI validation** when: Spec-first design, simple request/response validation sufficient

**Test generation depth**:

- **T1 only** when: Single endpoint, proof-of-concept, immediate feedback needed
- **T2** when: Production system, CI integration required, 3-10 endpoints
- **T3** when: Complex versioning, multiple consumers, governance required, >10 endpoints

**Breaking change severity**:

- **Block deployment** if: Removed endpoints used by active consumers, required field deleted
- **Warn but allow** if: New optional field, added endpoint, relaxed validation
- **Auto-approve** if: Only documentation changes, no schema modifications

**Ambiguity thresholds**:

- If `api_spec` has >20 endpoints, request focus on specific consumer-provider pair
- If breaking changes detected but no previous contract available, emit warning and proceed
- If circular dependencies detected (A depends on B, B depends on A), emit error and abort

---

## Output Contract

**Required fields** (all tiers):

```json
{
  "contract_tests": {
    "type": "code",
    "language": "javascript|java|python|go",
    "framework": "pact|spring-contract|openapi",
    "file_path": "path/to/test/file",
    "content": "// Full test code..."
  },
  "contract_spec": {
    "type": "json|yaml",
    "format": "pact_v3|spring_contract_dsl|openapi_3.1",
    "content": "{ ... contract JSON ... }"
  }
}
```

**T2+ additional fields**:

```json
{
  "ci_integration": {
    "type": "yaml",
    "pipeline": "github_actions|gitlab_ci|jenkins",
    "content": "# Pipeline config..."
  },
  "validation_report": {
    "type": "markdown",
    "breaking_changes": [
      {
        "severity": "critical|warning|safe",
        "description": "Removed endpoint /users/:id",
        "affected_consumers": ["mobile-app", "web-ui"]
      }
    ],
    "compatibility_matrix": "table of consumer/provider version compatibility"
  }
}
```

**T3 additional fields**:

```json
{
  "versioning_plan": {
    "type": "markdown",
    "strategy": "url|header|content_negotiation",
    "migration_steps": ["step 1", "step 2"]
  },
  "governance_workflow": {
    "type": "markdown",
    "approval_process": "description",
    "pact_broker_config": "webhook and notification setup"
  }
}
```

---

## Examples

**Example 1: Pact Consumer Test (JavaScript, ≤30 lines)**

```javascript
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { getUserById } = require('./api-client');
const provider = new PactV3({ consumer: 'mobile-app', provider: 'user-service' });
describe('User API Contract', () => {
  it('gets user by ID', () => {
    provider
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest({
        method: 'GET',
        path: '/users/123',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: MatchersV3.like(123),
          name: MatchersV3.like('Alice'),
          email: MatchersV3.email('alice@example.com'),
        },
      });
    return provider.executeTest(async (mockServer) => {
      const user = await getUserById(mockServer.url, 123);
      expect(user.name).toBe('Alice');
    });
  });
});
```

See `/skills/api-contract-testing/resources/` for Spring Cloud Contract and OpenAPI examples.

---

## Quality Gates

**Token budgets** (strict):

- T1: ≤2000 tokens (single endpoint test generation)
- T2: ≤6000 tokens (multi-endpoint + CI + breaking change detection)
- T3: ≤12000 tokens (schema evolution + governance + versioning)

**Safety requirements**:

- All generated tests must be runnable or marked as pseudo-code
- No hardcoded secrets or production API keys in test code
- All URLs in contract specs must be localhost or mock servers

**Auditability**:

- All breaking changes must be logged with severity and affected consumers
- Contract evolution history must be traceable via Pact Broker or version control
- CI integration must include contract verification as blocking gate

**Determinism**:

- Same `api_spec` + `role` + `framework` must generate identical contract tests
- Breaking change detection must be idempotent (same input = same output)

**Validation**:

- Generated Pact JSON must validate against Pact JSON Schema v3
- OpenAPI contracts must validate against OpenAPI 3.1 spec
- Spring Contract DSL must compile without errors

---

## Resources

**Official Documentation** (accessed 2025-10-26T06:31:34-04:00):

- [Pact Documentation](https://docs.pact.io/) - Consumer-driven contract testing
- [Pact Specification v3](https://github.com/pact-foundation/pact-specification/tree/version-3) - Pact JSON format
- [Spring Cloud Contract Reference](https://docs.spring.io/spring-cloud-contract/reference/) - Provider-driven contracts
- [OpenAPI Specification 3.1.0](https://spec.openapis.org/oas/v3.1.0) - API schema standard
- [Swagger API Validation](https://swagger.io/docs/specification/about/) - OpenAPI validation tools

**Tools and Libraries**:

- [Pact Broker](https://docs.pact.io/pact_broker) - Contract storage and verification
- [pactflow.io](https://pactflow.io/) - Managed Pact Broker service
- [openapi-validator](https://www.npmjs.com/package/express-openapi-validator) - Express.js OpenAPI validation
- [jest-pact](https://github.com/pact-foundation/jest-pact) - Jest integration for Pact

**Best Practices**:

- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) - API versioning and evolution
- [Microsoft API Design Guidance](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design) - Breaking change management
- [Martin Fowler: Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html) - Contract testing patterns

**Example Repositories**:

- [Pact Examples (Node.js)](https://github.com/pact-foundation/pact-js/tree/master/examples)
- [Spring Cloud Contract Samples](https://github.com/spring-cloud-samples/spring-cloud-contract-samples)
