---
name: "API Design Validator"
slug: "api-design-validator"
description: "Design and validate REST and GraphQL APIs with OpenAPI/GraphQL schema generation, security hardening, and OWASP API Security compliance."
capabilities:
  - OpenAPI 3.x schema generation and validation
  - GraphQL schema design and validation
  - OWASP API Security Top 10 compliance checking
  - API versioning strategy design
  - Pagination and filtering pattern recommendations
  - Rate limiting and throttling guidance
  - Authentication and authorization design
  - Error handling standardization
  - API documentation generation
inputs:
  - api_type: "REST | GraphQL (string, required)"
  - api_spec: "existing API specification or design document (string/object, optional)"
  - validation_tier: "T1 (schema) | T2 (security hardening) (string, default: T1)"
  - security_requirements: "authentication, authorization, rate-limiting flags (object, optional)"
  - versioning_strategy: "none | path | header | query (string, optional)"
outputs:
  - schema: "OpenAPI 3.x or GraphQL SDL schema (object)"
  - validation_report: "findings with severity levels (array)"
  - security_recommendations: "OWASP API Security mappings (array)"
  - design_patterns: "pagination, filtering, error handling patterns (object)"
keywords:
  - api-design
  - rest-api
  - graphql
  - openapi
  - swagger
  - api-security
  - owasp-api-security
  - schema-validation
  - api-versioning
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://spec.openapis.org/oas/v3.1.0
  - https://graphql.org/learn/
  - https://owasp.org/API-Security/
  - https://swagger.io/specification/
  - https://graphql.org/learn/best-practices/
  - https://www.rfc-editor.org/rfc/rfc9110.html
---

## Purpose & When-To-Use

**Trigger conditions:**
- Designing new REST or GraphQL API endpoints
- Validating existing API against security best practices
- Generating OpenAPI 3.x or GraphQL schema documentation
- API security audit or OWASP API Security Top 10 compliance check
- Designing backwards-compatible API versioning strategy
- Standardizing pagination, filtering, or error handling patterns
- Pre-deployment API quality gate

**Not for:**
- API performance load testing (use specialized tools)
- Real-time API monitoring (use APM solutions)
- API gateway configuration (infrastructure-specific)
- Client SDK generation (use code generation tools)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-25T21:30:36-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `api_type` must be exactly "REST" or "GraphQL"
- `api_spec` if provided must be valid JSON/YAML for REST or SDL string for GraphQL
- `validation_tier` must be: T1 or T2
- `security_requirements` if provided must be valid object with boolean flags
- `versioning_strategy` must be one of: none, path, header, query (for REST only)

**Source freshness:**
- OpenAPI 3.1.0 Specification (accessed 2025-10-25T21:30:36-04:00): https://spec.openapis.org/oas/v3.1.0
- GraphQL Specification (accessed 2025-10-25T21:30:36-04:00): https://spec.graphql.org/October2021/
- OWASP API Security Top 10 2023 (accessed 2025-10-25T21:30:36-04:00): https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- HTTP Semantics RFC 9110 (accessed 2025-10-25T21:30:36-04:00): https://www.rfc-editor.org/rfc/rfc9110.html

---

## Procedure

### T1: Schema Validation (≤2k tokens)

**Fast path for 80% of schema validation cases:**

1. **Parse input specification:**
   - If `api_spec` provided: parse and validate syntax
   - If not provided: prepare empty schema template

2. **Validate core schema elements (REST):**
   - OpenAPI version ≥ 3.0.0
   - Info object (title, version, description) present
   - Paths object with at least one endpoint
   - HTTP methods use standard verbs (GET, POST, PUT, PATCH, DELETE)
   - Request/response schemas defined with JSON Schema
   - Status codes follow RFC 9110 semantics

3. **Validate core schema elements (GraphQL):**
   - Schema Definition Language (SDL) syntax valid
   - Query type defined
   - Object types have fields with valid scalars or references
   - No circular dependencies without proper resolution
   - Input types for mutations properly defined
   - Nullable/non-nullable annotations appropriate

4. **Quick security checks:**
   - Authentication mentioned in schema (securitySchemes for REST, directives for GraphQL)
   - Sensitive data (passwords, tokens) not in query parameters (REST)
   - HTTPS enforced (servers array for REST)

5. **Generate validation report:**
   - Syntax errors (critical)
   - Missing required elements (high)
   - Best practice violations (medium)
   - Recommendations (low)

**Output:** Schema validation report with severity-ranked findings

**Token budget:** ≤2k tokens (schema parsing + basic validation rules)

---

### T2: Security Hardening & Design Patterns (≤6k tokens)

**Extended validation with OWASP API Security Top 10 compliance:**

1. **Apply T1 validation first**

2. **OWASP API Security Top 10 2023 checks (accessed 2025-10-25T21:30:36-04:00):**
   - **API1:2023 Broken Object Level Authorization:** Check for resource ID exposure without authorization checks
   - **API2:2023 Broken Authentication:** Validate authentication scheme (OAuth 2.0, JWT, API keys)
   - **API3:2023 Broken Object Property Level Authorization:** Verify sensitive fields have access controls
   - **API4:2023 Unrestricted Resource Consumption:** Check for rate limiting, pagination, max page size
   - **API5:2023 Broken Function Level Authorization:** Validate role-based access controls
   - **API6:2023 Unrestricted Access to Sensitive Business Flows:** Check for business logic flow protection
   - **API7:2023 Server Side Request Forgery:** Validate URL input sanitization
   - **API8:2023 Security Misconfiguration:** Check security headers, CORS, error verbosity
   - **API9:2023 Improper Inventory Management:** Verify API versioning and deprecation strategy
   - **API10:2023 Unsafe Consumption of APIs:** Validate third-party API input validation

3. **REST-specific design patterns (accessed 2025-10-25T21:30:36-04:00):**
   - **Pagination:** Cursor-based (recommended) vs offset-based
     - Cursor: `/resources?cursor=xyz&limit=20`
     - Offset: `/resources?offset=40&limit=20`
     - HAL links for navigation: `_links.next.href`
   - **Filtering:** Query parameters with standardized operators
     - `/users?filter[status]=active&filter[role]=admin`
   - **Sorting:** `?sort=-created_at,name` (- prefix for descending)
   - **Field selection:** `?fields=id,name,email` (sparse fieldsets)
   - **Error handling:** RFC 9457 Problem Details for HTTP APIs
   - **Versioning:**
     - Path: `/v1/resources` (most common, cache-friendly)
     - Header: `Accept: application/vnd.api.v1+json` (flexible)
     - Query: `/resources?version=1` (least recommended)

4. **GraphQL-specific design patterns (accessed 2025-10-25T21:30:36-04:00):**
   - **Pagination:** Relay cursor connections specification
     - `edges`, `node`, `pageInfo` structure
     - `hasNextPage`, `hasPreviousPage`, `startCursor`, `endCursor`
   - **Filtering:** Input objects with typed arguments
   - **Authorization:** `@auth` directives or resolver-level checks
   - **Error handling:** Errors array with extensions for error codes
   - **Batching:** DataLoader pattern for N+1 query prevention
   - **Depth limiting:** Max query depth to prevent DoS
   - **Cost analysis:** Complexity scoring for expensive queries

5. **Generate comprehensive outputs:**
   - **Schema:** Valid OpenAPI 3.x or GraphQL SDL with security annotations
   - **Validation report:** OWASP API Security Top 10 mappings with remediation steps
   - **Design patterns:** Pagination, filtering, error handling implementations
   - **Security recommendations:** Prioritized action items with source citations

**Output:** Complete API design package with security-hardened schema and implementation guidance

**Token budget:** ≤6k tokens (T1 + OWASP checks + design patterns + 4-6 authoritative sources)

---

### T3: Not Implemented

This skill implements T1 and T2 tiers only. For advanced scenarios requiring:
- Multi-API orchestration and gateway design
- Custom compliance framework mappings beyond OWASP
- API federation architecture (GraphQL Federation, API Gateway mesh)
- Advanced threat modeling specific to API attack vectors

**Defer to:**
- `security-assessment-framework` (T3) for comprehensive threat modeling
- `microservices-pattern-architect` for API gateway patterns
- `GraphQL-federation-architect` (Phase 3) for federated GraphQL schemas

**Token budget:** N/A (not implemented in this skill)

---

## Decision Rules

**Ambiguity thresholds:**
- If `api_type` not specified: ABORT with error "api_type is required: REST or GraphQL"
- If schema syntax invalid: ABORT T2, return T1 syntax errors only
- If security requirements unclear: Default to strictest (authentication required, HTTPS enforced)

**Tier selection:**
- Use T1 if: Quick schema validation needed, no security audit required
- Use T2 if: Production-ready API, security compliance required, design patterns needed

**Abort conditions:**
- Invalid JSON/YAML structure for REST OpenAPI spec
- Invalid SDL syntax for GraphQL schema
- API type not recognized (not REST or GraphQL)

**When to invoke dependent skills:**
- If compliance framework mapping needed: Invoke `security-assessment-framework` (ref CLAUDE.md §3)
- If authentication architecture design needed: Defer to `security-assessment-framework` IAM domain

---

## Output Contract

**Schema types:**

```typescript
interface ValidationReport {
  api_type: "REST" | "GraphQL";
  tier: "T1" | "T2";
  status: "pass" | "fail" | "warning";
  findings: Finding[];
  schema?: object | string;  // OpenAPI object or GraphQL SDL string
  security_recommendations?: SecurityRecommendation[];
  design_patterns?: DesignPatterns;
}

interface Finding {
  severity: "critical" | "high" | "medium" | "low";
  category: "syntax" | "security" | "best-practice" | "performance";
  message: string;
  location?: string;  // JSON path or GraphQL type/field
  remediation?: string;
  owasp_mapping?: string;  // e.g., "API1:2023"
}

interface SecurityRecommendation {
  owasp_id: string;  // API1:2023 through API10:2023
  title: string;
  description: string;
  current_status: "compliant" | "non-compliant" | "unknown";
  action_items: string[];
  references: string[];
}

interface DesignPatterns {
  pagination?: object;
  filtering?: object;
  sorting?: object;
  error_handling?: object;
  versioning?: object;
}
```

**Required fields:**
- `api_type`, `tier`, `status`, `findings` (always)
- `schema` (if T2 or generation requested)
- `security_recommendations`, `design_patterns` (if T2)

**Data validation:**
- All severity levels must be from enum
- OWASP mappings must match 2023 edition identifiers
- References must be accessible URLs with access date = NOW_ET

---

## Examples

**Example 1: REST API validation (T1)**

```yaml
Input:
  api_type: "REST"
  api_spec:
    openapi: "3.1.0"
    info:
      title: "User API"
      version: "1.0"
    paths:
      /users:
        get:
          parameters:
            - name: password
              in: query
          responses:
            200:
              description: OK

Output:
  status: "fail"
  findings:
    - severity: "critical"
      category: "security"
      message: "Sensitive parameter 'password' in query string"
      location: "/paths/~1users/get/parameters/0"
      remediation: "Move to request body or header"
      owasp_mapping: "API8:2023"
```

---

## Quality Gates

**Token budgets (mandatory enforcement):**
- T1: ≤2k tokens - Schema validation only, no heavy retrieval
- T2: ≤6k tokens - OWASP checks + design patterns + 4-6 authoritative sources
- T3: N/A - Not implemented (defer to dependent skills for advanced scenarios)

**Safety:**
- No API keys, credentials, or secrets in examples
- All external URLs verified accessible at NOW_ET
- No execution of untrusted API specifications

**Auditability:**
- All OWASP mappings cite 2023 edition with access date
- Design pattern recommendations cite authoritative sources (OpenAPI spec, GraphQL spec, RFCs)
- Schema generation follows official specifications only

**Determinism:**
- Same input specification produces same findings
- Severity rankings consistent across runs
- Schema validation rules non-probabilistic

---

## Resources

**Authoritative specifications (accessed 2025-10-25T21:30:36-04:00):**
- OpenAPI 3.1.0: https://spec.openapis.org/oas/v3.1.0
- GraphQL Spec Oct 2021: https://spec.graphql.org/October2021/
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- HTTP Semantics RFC 9110: https://www.rfc-editor.org/rfc/rfc9110.html
- RFC 9457 Problem Details: https://www.rfc-editor.org/rfc/rfc9457.html
- Relay Cursor Connections: https://relay.dev/graphql/connections.htm

**Best practices (accessed 2025-10-25T21:30:36-04:00):**
- GraphQL Best Practices: https://graphql.org/learn/best-practices/
- Swagger/OpenAPI Best Practices: https://swagger.io/docs/specification/about/
- REST API Design: https://restfulapi.net/

**Templates and schemas:**
- See `/skills/api-design-validator/resources/templates/` for OpenAPI starter templates
- See `/skills/api-design-validator/resources/schemas/` for GraphQL schema examples

**Security references:**
- OWASP API Security Project: https://owasp.org/www-project-api-security/
- OWASP Cheat Sheet - REST Security: https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- OWASP Cheat Sheet - GraphQL: https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
