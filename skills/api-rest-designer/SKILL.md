---
name: REST API Designer
slug: api-rest-designer
description: Design RESTful APIs with OpenAPI 3.1/3.2, resource modeling, HTTP semantics, versioning, pagination, HATEOAS, and OWASP API Security.
capabilities:
  - OpenAPI 3.1/3.2 specification generation (JSON Schema 2020-12, webhooks)
  - Resource modeling and URI design (collection, singleton, controller patterns)
  - HTTP method semantics (GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD)
  - Richardson Maturity Model assessment (Level 0-3)
  - API versioning (URI, header, media type/content negotiation)
  - Pagination (offset-based, cursor-based, keyset)
  - Filtering, sorting, and search patterns
  - HATEOAS link generation (Level 3 REST)
  - Rate limiting and throttling strategies
  - OWASP API Security Top 10 2023 compliance
  - Error response design (RFC 7807 Problem Details)
  - Idempotency and safe method guarantees
inputs:
  domain_model:
    type: object
    description: Domain entities and relationships (e.g., User, Order, Product)
    required: true
  use_cases:
    type: array
    description: Key API use cases (CRUD, search, bulk operations, webhooks)
    required: true
  versioning_strategy:
    type: string
    description: Versioning approach (uri, header, media-type)
    required: false
  pagination_preference:
    type: string
    description: Preferred pagination method (offset, cursor, keyset)
    required: false
  security_requirements:
    type: object
    description: Auth (OAuth2, API key), rate limits, CORS, allowed origins
    required: false
  maturity_target:
    type: integer
    description: Richardson Maturity Model target level (0-3)
    required: false
outputs:
  openapi_spec:
    type: object
    description: OpenAPI 3.1/3.2 specification (YAML or JSON)
  resource_design:
    type: object
    description: Resource URIs, relationships, and HTTP method mappings
  versioning_config:
    type: object
    description: Versioning strategy with examples and migration guide
  pagination_config:
    type: object
    description: Pagination parameters, response format, and metadata
  security_recommendations:
    type: array
    description: OWASP API Security Top 10 mitigations and best practices
  hateoas_links:
    type: object
    description: Hypermedia links for resource navigation (Level 3 REST)
keywords:
  - rest-api
  - openapi
  - api-design
  - resource-modeling
  - http-methods
  - richardson-maturity-model
  - hateoas
  - api-versioning
  - pagination
  - api-security
  - owasp
  - swagger
  - api-gateway
version: 1.0.0
owner: cognitive-toolworks
license: Apache-2.0
security:
  secrets: "Never hardcode API keys or tokens in OpenAPI examples; use placeholder values"
  compliance: "OWASP API Security Top 10 2023, RFC 9110 (HTTP Semantics), RFC 7807 (Problem Details)"
links:
  - title: "OpenAPI Specification v3.2.0"
    url: "https://spec.openapis.org/oas/v3.2.0.html"
    accessed: "2025-10-26"
  - title: "OWASP API Security Top 10 2023"
    url: "https://owasp.org/API-Security/editions/2023/en/0x11-t10/"
    accessed: "2025-10-26"
  - title: "Richardson Maturity Model"
    url: "https://martinfowler.com/articles/richardsonMaturityModel.html"
    accessed: "2025-10-26"
  - title: "RFC 9110: HTTP Semantics"
    url: "https://www.rfc-editor.org/rfc/rfc9110.html"
    accessed: "2025-10-26"
  - title: "RFC 7807: Problem Details for HTTP APIs"
    url: "https://www.rfc-editor.org/rfc/rfc7807.html"
    accessed: "2025-10-26"
---

## Purpose & When-To-Use

**Purpose:** Design production-ready RESTful APIs following industry best practices with OpenAPI 3.1/3.2 specifications, resource-oriented architecture, HTTP semantics compliance, flexible pagination/filtering strategies, HATEOAS hypermedia support (Richardson Level 3), and OWASP API Security Top 10 2023 mitigations.

**When to Use:**
- You need to **design a new REST API** from scratch with clear resource models, URI conventions, and HTTP method semantics.
- You want to **generate OpenAPI 3.1/3.2 specifications** with JSON Schema validation, webhooks, and security schemes.
- You're migrating from **Level 0/1 APIs** (SOAP, RPC-style) to **Level 2+ REST** with proper HTTP verb usage.
- You need to implement **API versioning** (URI, header, or media type) without breaking existing clients.
- You require **pagination, filtering, and sorting** for large datasets (offset, cursor, or keyset pagination).
- You're implementing **HATEOAS** (Level 3 REST) with hypermedia links for discoverable APIs.
- You need **OWASP API Security** compliance (authentication, authorization, rate limiting, input validation).
- You're integrating with **API gateways** (AWS API Gateway, Kong, Apigee) for rate limiting and transformation.

**Complements:**
- `api-graphql-designer`: Use GraphQL for flexible client-driven queries; use REST for simple CRUD and public APIs.
- `api-contract-testing`: Validate OpenAPI specs with Pact or Spring Cloud Contract.
- `security-api-gateway-configurator`: Deploy REST APIs with gateway-level auth, throttling, and monitoring.

**Delegates to:**
- `api-design-validator`: Validates generated OpenAPI specs for schema compliance and security hardening.

## Pre-Checks

**Mandatory Inputs:**
- `domain_model`: At least one entity with attributes (e.g., User: {id, email, name}).
- `use_cases`: Minimum one use case (e.g., "List all users", "Create a new order").

**Validation Steps:**
1. **Compute NOW_ET** using NIST time.gov semantics (America/New_York, ISO-8601) for timestamp anchoring.
2. **Check domain_model completeness:** Verify entities have primary keys and relationships (one-to-many, many-to-many).
3. **Validate use_cases:** Ensure use cases map to HTTP methods (GET for retrieval, POST for creation, etc.).
4. **Assess maturity_target:** If `maturity_target` = 3, verify client can handle HATEOAS links (many clients only support Level 2).
5. **Abort if:**
   - Zero entities in `domain_model`.
   - Use cases conflict with HTTP semantics (e.g., "Delete user" mapped to GET).
   - Versioning strategy is "header" but API gateway doesn't support custom headers.

## Procedure

### T1: Quick REST API Design (≤2k tokens, 80% use case)

**Goal:** Generate a basic RESTful API with OpenAPI 3.1 spec for a single resource using standard CRUD operations.

**Steps:**
1. **Identify primary resource:** Select the main entity from `domain_model` (e.g., "User").
2. **Design resource URIs:**
   - Collection: `GET /users`, `POST /users`
   - Singleton: `GET /users/{id}`, `PUT /users/{id}`, `PATCH /users/{id}`, `DELETE /users/{id}`
3. **Map HTTP methods to operations:**
   - `GET /users`: List all users (paginate with `?limit=20&offset=0` by default).
   - `POST /users`: Create a new user (return `201 Created` with `Location` header).
   - `GET /users/{id}`: Retrieve a single user (return `200 OK` or `404 Not Found`).
   - `PUT /users/{id}`: Replace entire user (idempotent, return `200 OK`).
   - `PATCH /users/{id}`: Partial update (return `200 OK` or `204 No Content`).
   - `DELETE /users/{id}`: Delete user (idempotent, return `204 No Content`).
4. **Generate OpenAPI 3.1 spec (minimal):**
   ```yaml
   openapi: 3.1.0
   info:
     title: User API
     version: 1.0.0
   paths:
     /users:
       get:
         summary: List users
         parameters:
           - name: limit
             in: query
             schema: {type: integer, default: 20}
           - name: offset
             in: query
             schema: {type: integer, default: 0}
         responses:
           200:
             description: List of users
             content:
               application/json:
                 schema:
                   type: array
                   items: {$ref: '#/components/schemas/User'}
       post:
         summary: Create user
         requestBody:
           required: true
           content:
             application/json:
               schema: {$ref: '#/components/schemas/User'}
         responses:
           201:
             description: User created
             headers:
               Location: {schema: {type: string}}
   components:
     schemas:
       User:
         type: object
         required: [email, name]
         properties:
           id: {type: string, format: uuid}
           email: {type: string, format: email}
           name: {type: string}
   ```
5. **Output:** OpenAPI spec (YAML), Richardson Level 2 compliance confirmed.

**Token Budget:** ≤2k tokens (single resource, basic CRUD).

### T2: Multi-Resource API with Versioning and Pagination (≤6k tokens)

**Goal:** Design a multi-resource API with versioning, pagination (cursor or offset), filtering, and OWASP API Security mitigations.

**Steps:**
1. **Model all resources and relationships:**
   - Identify entities: User, Order, Product.
   - Map relationships: User has many Orders, Order has many Products (via OrderItems).
2. **Design nested and flat URIs:**
   - **Flat (preferred):** `GET /orders?userId=123` (query filtering).
   - **Nested:** `GET /users/{userId}/orders` (if relationship is always accessed via parent).
   - **Decision rule:** Use flat URIs unless relationship is always accessed through parent (e.g., `/users/{id}/settings` where settings don't exist independently).
3. **Apply versioning strategy (default: URI versioning):**
   - **URI versioning:** `/v1/users`, `/v2/users` (most common, clear, cacheable).
   - **Header versioning:** `X-API-Version: 2` (clean URIs, harder to test in browser).
   - **Media type:** `Accept: application/vnd.api.v2+json` (REST purist, complex for clients).
   - **Selection criteria:** Use URI versioning unless gateway mandates header-based routing.
4. **Implement pagination (choose based on `pagination_preference`):**
   - **Offset-based (default):**
     - Request: `GET /orders?limit=20&offset=40`
     - Response: `{data: [...], pagination: {total: 150, limit: 20, offset: 40}}`
     - **Pros:** Simple, stateless, supports random access (jump to page 5).
     - **Cons:** Slow for large offsets (DB scans first N rows), page drift (new items shift results).
   - **Cursor-based (recommended for real-time data):**
     - Request: `GET /orders?limit=20&after=cursorXYZ`
     - Response: `{data: [...], pagination: {nextCursor: "abc123", hasMore: true}}`
     - **Pros:** Efficient (no offset scan), consistent (no page drift), ideal for infinite scroll.
     - **Cons:** No random access, cursor is opaque (can't jump to page 5).
   - **Keyset-based (best performance):**
     - Request: `GET /orders?limit=20&afterId=1000&afterCreatedAt=2025-10-26T12:00:00Z`
     - Response: Uses indexed columns (id, createdAt) for WHERE clause.
     - **Pros:** Fast (index seek), deterministic, no drift.
     - **Cons:** Requires stable sort key, complex for clients.
5. **Add filtering and sorting:**
   - **Filtering:** `GET /orders?status=completed&minAmount=100`
   - **Sorting:** `GET /orders?sort=createdAt:desc,amount:asc` (multi-column).
   - **Rule:** Apply filters/sort BEFORE pagination; sort must be deterministic (add `id` as tiebreaker).
6. **Implement OWASP API Security Top 10 2023 mitigations:**
   - **API1: Broken Object Level Authorization (BOLA):** Validate `userId` matches authenticated user before returning `/users/{userId}`.
   - **API2: Broken Authentication:** Use OAuth2/JWT, validate tokens on every request.
   - **API3: Broken Object Property Level Authorization:** Don't expose internal fields (passwordHash, internalId) in responses.
   - **API4: Unrestricted Resource Consumption:** Rate limit (e.g., 100 req/min per user) via API gateway or middleware.
   - **API5: Broken Function Level Authorization:** Check permissions for admin-only endpoints (DELETE /users/{id} requires admin role).
   - **API6: Unrestricted Access to Sensitive Business Flows:** Throttle sensitive actions (password reset: 3 attempts/hour).
   - **API7: Server-Side Request Forgery (SSRF):** Validate all external URLs in requests (e.g., webhook callbacks).
   - **API8: Security Misconfiguration:** Disable verbose error messages in production (no stack traces in 500 responses).
   - **API9: Improper Inventory Management:** Document all endpoints in OpenAPI spec; deprecate old versions explicitly.
   - **API10: Unsafe Consumption of APIs:** Validate all data from upstream APIs (don't trust external sources).
7. **Generate OpenAPI 3.1 spec with security schemes:**
   ```yaml
   openapi: 3.1.0
   info:
     title: E-commerce API
     version: 2.0.0
   servers:
     - url: https://api.example.com/v2
   paths:
     /orders:
       get:
         summary: List orders
         parameters:
           - name: limit
             in: query
             schema: {type: integer, default: 20, maximum: 100}
           - name: after
             in: query
             schema: {type: string}
           - name: status
             in: query
             schema: {type: string, enum: [pending, completed, cancelled]}
         security:
           - bearerAuth: []
         responses:
           200:
             description: List of orders
             content:
               application/json:
                 schema:
                   type: object
                   properties:
                     data: {type: array, items: {$ref: '#/components/schemas/Order'}}
                     pagination:
                       type: object
                       properties:
                         nextCursor: {type: string}
                         hasMore: {type: boolean}
   components:
     securitySchemes:
       bearerAuth:
         type: http
         scheme: bearer
         bearerFormat: JWT
     schemas:
       Order:
         type: object
         required: [id, userId, status, total]
         properties:
           id: {type: string, format: uuid}
           userId: {type: string, format: uuid}
           status: {type: string, enum: [pending, completed, cancelled]}
           total: {type: number, format: decimal}
   ```
8. **Output:**
   - OpenAPI 3.1 spec with 3+ resources, versioning, pagination, security.
   - Resource design doc with URI patterns and relationship mappings.
   - Pagination config (chosen strategy + migration path from offset to cursor if needed).
   - OWASP API Security checklist (10 mitigations applied).

**Token Budget:** ≤6k tokens (multi-resource, versioning, pagination, security).

### T3: HATEOAS API with Advanced Patterns (≤12k tokens)

**Goal:** Design a Richardson Level 3 REST API with HATEOAS hypermedia links, webhooks, bulk operations, and advanced security.

**Steps:**
1. **Implement HATEOAS links (Richardson Level 3):**
   - Every resource includes `_links` section with `self`, `related`, and `action` links.
   - Example:
     ```json
     {
       "id": "order-123",
       "status": "pending",
       "total": 99.99,
       "_links": {
         "self": {"href": "/v2/orders/order-123"},
         "user": {"href": "/v2/users/user-456"},
         "items": {"href": "/v2/orders/order-123/items"},
         "cancel": {"href": "/v2/orders/order-123/cancel", "method": "POST"},
         "pay": {"href": "/v2/orders/order-123/pay", "method": "POST"}
       }
     }
     ```
   - **Benefit:** Clients discover actions dynamically (if status=pending, show "cancel" and "pay" links; if status=completed, hide those links).
2. **Add webhooks (OpenAPI 3.1 feature):**
   - Define outbound events (e.g., "order.created", "order.completed") that the API will POST to client-registered URLs.
   - OpenAPI 3.1 `webhooks` section:
     ```yaml
     webhooks:
       orderCreated:
         post:
           requestBody:
             content:
               application/json:
                 schema:
                   type: object
                   properties:
                     event: {type: string, example: "order.created"}
                     data: {$ref: '#/components/schemas/Order'}
           responses:
             200:
               description: Webhook received
     ```
3. **Design bulk operations:**
   - **Batch GET:** `GET /users?ids=1,2,3` (return array of users).
   - **Batch POST:** `POST /users/batch` with array of users in body (return array of created users).
   - **Batch PATCH:** `PATCH /users/batch` with array of `{id, changes}` objects.
   - **Idempotency:** Use `Idempotency-Key` header for POST/PATCH to prevent duplicate operations.
4. **Implement advanced filtering:**
   - **Range queries:** `?createdAt[gte]=2025-01-01&createdAt[lt]=2025-02-01`
   - **Full-text search:** `?q=laptop` (searches across multiple fields).
   - **Logical operators:** `?status[in]=pending,completed` (OR), `?status[ne]=cancelled` (NOT EQUAL).
5. **Add caching and ETag support:**
   - `GET /users/{id}` returns `ETag: "abc123"` header.
   - Client sends `If-None-Match: "abc123"` on next request.
   - Server returns `304 Not Modified` if resource unchanged (saves bandwidth).
6. **Error handling with RFC 7807 Problem Details:**
   ```json
   {
     "type": "https://api.example.com/errors/validation-error",
     "title": "Validation Error",
     "status": 400,
     "detail": "Email field is required",
     "instance": "/v2/users",
     "errors": [
       {"field": "email", "message": "Email is required"}
     ]
   }
   ```
7. **Rate limiting with standardized headers:**
   - Response headers:
     - `X-RateLimit-Limit: 100`
     - `X-RateLimit-Remaining: 95`
     - `X-RateLimit-Reset: 1698345600` (Unix timestamp)
   - Return `429 Too Many Requests` with `Retry-After` header.
8. **Versioning migration strategy:**
   - Maintain 2 versions simultaneously (v1, v2) for 6 months.
   - Add `Deprecation: true` and `Sunset: 2026-04-26` headers to v1 responses.
   - Provide migration guide in API docs showing v1 → v2 breaking changes.
9. **Generate comprehensive OpenAPI 3.2 spec:**
   - Full schemas with JSON Schema 2020-12 validation (pattern, format, min/max).
   - Security schemes (OAuth2 with flows, API key, mTLS).
   - Examples for all request/response bodies.
   - Webhooks definitions.
   - Links for HATEOAS navigation.
10. **Output:**
    - OpenAPI 3.2 spec (500-1000 lines) with HATEOAS, webhooks, bulk operations.
    - Resource design with all URI patterns, relationship graphs.
    - Versioning migration guide (v1 → v2 breaking changes, timeline).
    - Pagination comparison table (offset vs cursor vs keyset).
    - OWASP API Security Top 10 compliance report (all 10 mitigations documented).
    - Rate limiting config (limits per endpoint, throttling strategy).
    - Caching strategy (ETag, Cache-Control headers).

**Token Budget:** ≤12k tokens (HATEOAS, webhooks, bulk ops, advanced security, caching).

## Decision Rules

**Ambiguity Resolution:**
1. **If `versioning_strategy` not specified:**
   - Default to **URI versioning** (`/v1/`, `/v2/`) as it's most widely adopted and easiest to test.
   - Emit note: "Using URI versioning by default. Consider header versioning if clean URIs are required."
2. **If `pagination_preference` not specified:**
   - Default to **offset-based** for simplicity unless use case mentions "real-time", "feed", or "infinite scroll" (then use cursor).
   - Emit note: "Using offset pagination. Migrate to cursor pagination for real-time feeds to avoid page drift."
3. **If `maturity_target` not specified:**
   - Target **Richardson Level 2** (proper HTTP verbs, multiple resources) as Level 3 (HATEOAS) adds complexity most clients don't need.
   - Emit note: "Targeting Richardson Level 2. Add HATEOAS (Level 3) if API discoverability is required."
4. **If multiple resources share similar names:**
   - Use plural nouns for collections (`/users`, not `/user`).
   - Avoid verbs in URIs (`/createUser` is wrong; use `POST /users` instead).
5. **If relationship can be represented flat or nested:**
   - Prefer **flat URIs with filtering** (`GET /orders?userId=123`) for flexibility.
   - Use **nested URIs** only if relationship is exclusive (`GET /users/{id}/profile` where profile can't exist without user).

**Stop Conditions:**
- **Conflicting HTTP semantics:** User requests "GET /users/{id}/delete" → abort and suggest `DELETE /users/{id}`.
- **Security requirements impossible:** User requires OAuth2 but API gateway doesn't support it → emit error with alternatives (API key, mTLS).
- **Pagination strategy conflicts with data model:** User wants cursor pagination but entities lack stable sort key → abort and suggest keyset with `id + createdAt`.

**Thresholds:**
- **Pagination limits:** Max `limit=100` to prevent resource exhaustion. Return `400 Bad Request` if limit > 100.
- **Nested URI depth:** Max 2 levels (`/users/{id}/orders/{orderId}` is OK; `/users/{id}/orders/{orderId}/items/{itemId}` is too deep → flatten to `/order-items/{id}`).
- **Versioning concurrency:** Support max 2 versions simultaneously (e.g., v1 + v2). Deprecate v1 after 6 months.

## Output Contract

**Required Fields:**

```typescript
{
  openapi_spec: {
    openapi: "3.1.0" | "3.2.0";
    info: {
      title: string;
      version: string;         // Semantic version (1.0.0, 2.1.0)
      description?: string;
    };
    servers: Array<{
      url: string;             // https://api.example.com/v2
      description?: string;
    }>;
    paths: {
      [path: string]: {        // /users, /users/{id}, etc.
        [method: string]: {    // get, post, put, patch, delete
          summary: string;
          parameters?: Array<{
            name: string;
            in: "query" | "path" | "header";
            schema: object;    // JSON Schema
            required?: boolean;
          }>;
          requestBody?: {
            required: boolean;
            content: {
              "application/json": {
                schema: object;
              };
            };
          };
          responses: {
            [statusCode: string]: {
              description: string;
              content?: {
                "application/json": {
                  schema: object;
                };
              };
            };
          };
          security?: Array<object>;
        };
      };
    };
    components: {
      schemas: {
        [name: string]: object; // JSON Schema definitions
      };
      securitySchemes?: {
        [name: string]: {
          type: "http" | "apiKey" | "oauth2" | "openIdConnect" | "mutualTLS";
          scheme?: "bearer" | "basic";
          bearerFormat?: "JWT";
        };
      };
    };
    webhooks?: {               // OpenAPI 3.1+ only
      [name: string]: {
        post: object;          // Outbound webhook definition
      };
    };
  };
  resource_design: {
    resources: Array<{
      name: string;            // User, Order, Product
      uri_template: string;    // /users, /users/{id}
      http_methods: {
        GET?: string;          // Description (e.g., "List all users")
        POST?: string;
        PUT?: string;
        PATCH?: string;
        DELETE?: string;
      };
      relationships: Array<{
        related_resource: string;
        relationship_type: "one-to-many" | "many-to-many" | "one-to-one";
        uri_pattern: string;  // /users/{userId}/orders or /orders?userId={userId}
      }>;
    }>;
    richardson_level: 0 | 1 | 2 | 3;
  };
  versioning_config: {
    strategy: "uri" | "header" | "media-type";
    current_version: string;  // v2, 2.0.0
    supported_versions: string[]; // [v1, v2]
    deprecation_timeline?: {
      deprecated_version: string;
      sunset_date: string;    // ISO 8601
    };
    migration_guide: string;  // Breaking changes, timeline
  };
  pagination_config: {
    method: "offset" | "cursor" | "keyset";
    parameters: {
      limit: {
        default: number;      // 20
        max: number;          // 100
      };
      offset?: number;        // For offset-based
      cursor?: string;        // For cursor-based
      sortKey?: string;       // For keyset-based
    };
    response_format: {
      data_field: string;     // "data" or "items"
      metadata_field: string; // "pagination" or "meta"
      metadata_shape: object; // {total, limit, offset} or {nextCursor, hasMore}
    };
  };
  security_recommendations: Array<{
    owasp_category: string;   // API1: BOLA, API2: Broken Auth, etc.
    risk: "high" | "medium" | "low";
    mitigation: string;       // Specific action (e.g., "Validate userId matches JWT")
    implementation: string;   // Code snippet or config example
  }>;
  hateoas_links?: {           // Only if maturity_target >= 3
    link_relations: Array<{
      rel: string;            // self, related, action
      href_template: string;  // /users/{id}, /users/{id}/orders
      method?: string;        // POST, DELETE (for action links)
    }>;
    example_response: object; // JSON with _links section
  };
}
```

**Optional Fields:**
- `webhooks`: Array of webhook definitions (event name, payload schema, delivery guarantees).
- `caching_strategy`: Object with ETag usage, Cache-Control headers, max-age values.
- `rate_limiting`: Object with limits per endpoint, throttling algorithm (token bucket, leaky bucket).
- `bulk_operations`: Array of batch endpoints (/users/batch, etc.) with idempotency requirements.

**Format:** OpenAPI spec in YAML or JSON. Resource design and recommendations in Markdown.

## Examples

### Example 1: E-commerce API (T2 - Multi-Resource with Pagination)

**Input:**
```yaml
domain_model:
  User: {id: uuid, email: string, name: string}
  Order: {id: uuid, userId: uuid, status: enum, total: decimal}
  Product: {id: uuid, name: string, price: decimal}
use_cases:
  - "List all orders for a user"
  - "Create a new order"
  - "Search products by name"
versioning_strategy: "uri"
pagination_preference: "cursor"
security_requirements:
  auth: "OAuth2 (Bearer JWT)"
  rate_limit: "100 requests/minute per user"
```

**Output (T2 Summary):**
```yaml
Richardson Level: 2 (HTTP verbs + multiple resources)
Versioning: URI-based (/v1/, /v2/)
Pagination: Cursor-based (after parameter, nextCursor in response)
Resources:
  - /v1/users (GET, POST)
  - /v1/users/{id} (GET, PUT, PATCH, DELETE)
  - /v1/orders (GET, POST) + ?userId filter + ?after cursor
  - /v1/orders/{id} (GET, PUT, PATCH, DELETE)
  - /v1/products (GET, POST) + ?q=search query
Security: OAuth2 Bearer JWT, rate limit 100/min via X-RateLimit headers
OWASP Mitigations:
  - API1 BOLA: Validate userId in JWT matches /users/{id} access
  - API4 Rate Limit: 100 req/min via API gateway (429 response if exceeded)
  - API8 Misconfiguration: No stack traces in production (generic 500 message)
```

**Link to Full Example:** See `skills/api-rest-designer/examples/ecommerce-api-design.txt`

### Example 2: HATEOAS API with Webhooks (T3 Snippet)

**HATEOAS Response Example:**
```json
{
  "id": "order-456",
  "status": "pending",
  "total": 149.99,
  "_links": {
    "self": {"href": "/v2/orders/order-456"},
    "user": {"href": "/v2/users/user-789"},
    "items": {"href": "/v2/orders/order-456/items"},
    "cancel": {"href": "/v2/orders/order-456/cancel", "method": "POST"},
    "pay": {"href": "/v2/payments", "method": "POST", "body": {"orderId": "order-456"}}
  }
}
```

**Webhook Definition (OpenAPI 3.1):**
```yaml
webhooks:
  orderCompleted:
    post:
      summary: Notifies when an order is completed
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                event: {type: string, example: "order.completed"}
                timestamp: {type: string, format: date-time}
                data: {$ref: '#/components/schemas/Order'}
      responses:
        200:
          description: Webhook acknowledged
```

## Quality Gates

**Token Budget Compliance:**
- T1 output ≤2k tokens (single resource, basic CRUD).
- T2 output ≤6k tokens (multi-resource, versioning, pagination, security).
- T3 output ≤12k tokens (HATEOAS, webhooks, bulk ops, advanced security).

**Validation Checklist:**
- [ ] All paths use plural nouns for collections (`/users`, not `/user`).
- [ ] HTTP methods match semantics (GET is safe/idempotent, POST creates, PUT replaces, PATCH updates, DELETE removes).
- [ ] Pagination includes metadata (`total`, `nextCursor`, `hasMore`).
- [ ] All POST/PUT/PATCH endpoints return `201 Created` or `200 OK` with resource in body.
- [ ] All error responses use RFC 7807 Problem Details format.
- [ ] Security schemes defined (OAuth2, API key) and applied to protected endpoints.
- [ ] OWASP API Security Top 10 2023 mitigations documented (at least 5 for T2, all 10 for T3).
- [ ] OpenAPI spec validates against OpenAPI 3.1/3.2 schema (use `swagger-cli validate`).
- [ ] Versioning strategy is consistent across all endpoints.
- [ ] Richardson Maturity Level matches `maturity_target` (or Level 2 by default).

**Safety & Auditability:**
- **No secrets in spec:** Redact all API keys, tokens, passwords in OpenAPI examples.
- **Deprecation notices:** If deprecating endpoints, add `deprecated: true` in OpenAPI and `Sunset` header in responses.
- **CORS configuration:** Document `Access-Control-Allow-Origin` settings if API is public-facing.

**Determinism:**
- **Stable sorting:** All paginated endpoints must have deterministic sort order (add `id` as tiebreaker if primary sort isn't unique).
- **Idempotency:** POST endpoints support `Idempotency-Key` header to prevent duplicate resource creation.

## Resources

**Official Specifications:**
- [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html) (accessed 2025-10-26)
  - Latest spec with JSON Schema 2020-12, webhooks, streaming media types.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) (accessed 2025-10-26)
  - Definitive guide for HTTP method semantics (GET, POST, PUT, PATCH, DELETE).
- [RFC 7807: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807.html) (accessed 2025-10-26)
  - Standard error response format.

**Security:**
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) (accessed 2025-10-26)
  - API1: BOLA, API2: Broken Auth, API3: Broken Object Property, API4: Resource Consumption, API5: Function Auth, API6: Sensitive Flows, API7: SSRF, API8: Misconfiguration, API9: Inventory, API10: Unsafe Consumption.

**REST Design Patterns:**
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html) (accessed 2025-10-26)
  - Level 0: POX (Plain Old XML), Level 1: Resources, Level 2: HTTP Verbs, Level 3: HATEOAS.
- [REST API Design Best Practices](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/) (accessed 2025-10-26)
  - Filtering, sorting, pagination patterns.

**Pagination:**
- [API Pagination Best Practices](https://www.speakeasy.com/api-design/pagination) (accessed 2025-10-26)
  - Offset vs cursor vs keyset comparison.

**Versioning:**
- [API Versioning Strategies 2025](https://www.devzery.com/post/versioning-rest-api-strategies-best-practices-2025) (accessed 2025-10-26)
  - URI, header, media type versioning pros/cons.

**Complementary Skills:**
- `api-graphql-designer`: Alternative to REST for flexible client queries.
- `api-contract-testing`: Validate OpenAPI specs with Pact, Spring Cloud Contract.
- `security-api-gateway-configurator`: Deploy REST APIs with gateway-level auth, rate limiting, monitoring.
- `api-design-validator`: Automated OpenAPI spec validation and security hardening.
