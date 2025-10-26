---
name: "GraphQL Schema Designer"
slug: "api-graphql-designer"
description: "Design GraphQL schemas with federation, resolvers, dataloaders, n+1 query prevention, and schema stitching patterns"
capabilities:
  - GraphQL SDL schema design and validation
  - Apollo Federation v2 subgraph configuration
  - Resolver pattern implementation guidance
  - DataLoader setup for n+1 prevention
  - Custom scalar type definitions
  - Schema stitching and composition
  - Query complexity analysis and cost limiting
  - Directive-based authorization
  - Subscription design patterns
  - Pagination (cursor-based and offset)
inputs:
  - schema_type: "standalone | federated | stitched (string, required)"
  - use_case: "api-gateway | microservices | mobile-bff (string, optional)"
  - optimization_level: "basic | production (string, default: basic)"
  - entities: "domain entities with fields and relationships (array, optional)"
  - federation_config: "federation version, shared types (object, optional for federated)"
outputs:
  - schema_definition: "GraphQL SDL with types, queries, mutations, subscriptions (string)"
  - resolver_patterns: "resolver implementation patterns and best practices (object)"
  - optimization_config: "DataLoader setup, caching, batching configuration (object)"
  - federation_config: "if federated, subgraph configuration and entity resolution (object)"
  - security_directives: "authorization directives and field-level security (array)"
keywords:
  - graphql
  - apollo-federation
  - schema-design
  - dataloaders
  - n+1-prevention
  - schema-stitching
  - resolvers
  - graphql-subscriptions
  - graphql-directives
  - query-optimization
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://spec.graphql.org/October2021/
  - https://www.apollographql.com/docs/federation/
  - https://github.com/graphql/dataloader
  - https://www.apollographql.com/docs/apollo-server/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Designing new GraphQL API schema from domain model
- Converting REST APIs to GraphQL
- Implementing Apollo Federation for microservices
- Optimizing GraphQL queries for n+1 problems
- Setting up schema stitching across multiple GraphQL services
- Implementing real-time subscriptions
- Adding field-level authorization and security
- Migrating monolithic GraphQL to federated architecture
- Designing BFF (Backend for Frontend) GraphQL layer

**Not for:**
- GraphQL client implementation (use Apollo Client, Relay, urql)
- GraphQL server deployment/infrastructure (use platform-specific tools)
- Database query optimization (use database-specific skills)
- Real-time transport protocols (WebSocket, SSE configuration)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T03:51:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `schema_type` must be exactly: "standalone", "federated", or "stitched"
- `use_case` if provided must be one of: "api-gateway", "microservices", "mobile-bff"
- `optimization_level` must be: "basic" or "production"
- `entities` if provided must be valid array of objects with name, fields, relationships
- `federation_config` required if `schema_type` is "federated"

**Source freshness:**
- GraphQL Specification October 2021 (accessed 2025-10-26T03:51:54-04:00): https://spec.graphql.org/October2021/
- Apollo Federation v2 Documentation (accessed 2025-10-26T03:51:54-04:00): https://www.apollographql.com/docs/federation/
- DataLoader GitHub (accessed 2025-10-26T03:51:54-04:00): https://github.com/graphql/dataloader
- GraphQL Best Practices (accessed 2025-10-26T03:51:54-04:00): https://graphql.org/learn/best-practices/

---

## Procedure

### T1: Basic Schema Design (≤2k tokens)

**Fast path for 80% of standalone GraphQL schema cases:**

1. **Define core types from entities:**
   - Create GraphQL object types from domain entities
   - Map field types to GraphQL scalars (Int, Float, String, Boolean, ID)
   - Add custom scalars for Date, DateTime, JSON, URL as needed
   - Mark non-nullable fields with `!` based on business rules

2. **Create Query and Mutation root types:**
   - Design query resolvers for single entities (by ID) and collections (list, filtered)
   - Design mutation resolvers for CRUD operations (create, update, delete)
   - Follow naming conventions: `getUser`, `listUsers`, `createUser`, `updateUser`, `deleteUser`
   - Add Input types for mutation arguments

3. **Implement basic pagination:**
   - Offset-based pagination for simple use cases: `limit`, `offset` arguments
   - Return `totalCount` for UI pagination controls

4. **Add basic error handling:**
   - Use union types for operation results: `type UserResult = User | NotFoundError | ValidationError`
   - Or use nullable fields with errors extension pattern

5. **Generate SDL output:**
   - Format schema using GraphQL SDL
   - Include comments for field descriptions
   - Group related types together

**Output:** Basic GraphQL schema SDL with queries, mutations, and types

**Token budget:** ≤2k tokens (type definitions + basic resolvers)

---

### T2: Production Optimization & Federation (≤6k tokens)

**Extended implementation with n+1 prevention and federation:**

1. **Apply T1 basic schema design first**

2. **Implement DataLoader patterns for n+1 prevention (accessed 2025-10-26T03:51:54-04:00):**
   - Create DataLoader instances for batch loading: `new DataLoader(batchLoadFn)`
   - Batch database queries by keys: `SELECT * FROM users WHERE id IN (?)`
   - Cache results per-request to avoid duplicate fetches
   - Handle one-to-many relationships with batching
   - Example resolver with DataLoader:
     ```javascript
     {
       User: {
         posts: (parent, args, { dataloaders }) =>
           dataloaders.postsByUserId.load(parent.id)
       }
     }
     ```

3. **Design cursor-based pagination (Relay-style):**
   - Implement Connection pattern with edges, pageInfo, cursor
   - Use base64-encoded cursors for opaque pagination
   - Support `first`, `after`, `last`, `before` arguments
   - Return `hasNextPage`, `hasPreviousPage` in pageInfo

4. **Add Apollo Federation v2 configuration (if federated) (accessed 2025-10-26T03:51:54-04:00):**
   - Mark entity types with `@key` directive: `type User @key(fields: "id") { id: ID! }`
   - Define reference resolvers for entity lookup: `__resolveReference(reference)`
   - Use `@shareable` for common types across subgraphs
   - Use `@external` and `@requires` for field dependencies
   - Design subgraph boundaries by domain (users, products, orders)

5. **Implement authorization directives:**
   - Create custom `@auth` directive for field-level security
   - Add role-based access: `@auth(requires: ADMIN)`
   - Implement in directive resolver or schema transformer

6. **Query complexity analysis:**
   - Calculate query cost based on depth and breadth
   - Set complexity limits to prevent abuse
   - Use query depth limiting (e.g., max depth 7)
   - Implement query cost analysis plugin

**Output:** Production-ready schema with federation, DataLoaders, pagination, and security

**Token budget:** ≤6k tokens (T1 + optimization patterns + federation setup)

---

### T3: Advanced Patterns & Subscriptions (≤12k tokens)

**Deep dive with schema stitching, subscriptions, and advanced optimization:**

1. **Apply T2 production optimization first**

2. **Schema stitching patterns (if stitched) (accessed 2025-10-26T03:51:54-04:00):**
   - Merge multiple GraphQL schemas into unified gateway
   - Use schema delegation for remote subschema queries
   - Implement type merging for common entities across services
   - Handle schema conflicts with type renaming or field aliasing
   - Configure batch execution for delegated queries

3. **GraphQL subscriptions design (accessed 2025-10-26T03:51:54-04:00):**
   - Define Subscription root type for real-time events
   - Use PubSub mechanism for event publishing: `pubsub.publish('USER_UPDATED', payload)`
   - Implement subscription resolvers with AsyncIterator
   - Filter subscriptions by user context or arguments
   - Example subscription:
     ```graphql
     type Subscription {
       userUpdated(userId: ID!): User
       newOrder: Order @auth(requires: ADMIN)
     }
     ```

4. **Advanced resolver patterns:**
   - Field-level resolver composition with middleware
   - Resolver caching strategies (in-memory, Redis)
   - Lazy loading for expensive computed fields
   - Custom scalar resolvers (DateTime, Email, URL validation)
   - Error handling middleware for consistent error responses

5. **Performance monitoring instrumentation:**
   - Add resolver timing metrics
   - Track DataLoader cache hit rates
   - Monitor query complexity scores
   - Log slow queries for optimization

6. **Advanced federation patterns:**
   - Implement extended service schemas for backward compatibility
   - Use `@override` for gradual service migration
   - Design for distributed tracing across subgraphs
   - Handle authentication/authorization propagation

7. **Schema evolution strategies:**
   - Add deprecation notices: `field: String @deprecated(reason: "Use newField")`
   - Version schema changes without breaking clients
   - Implement schema registry for federated governance

**Output:** Complete enterprise-grade GraphQL architecture with subscriptions, stitching, and monitoring

**Token budget:** ≤12k tokens (T2 + subscriptions + stitching + advanced patterns)

---

## Decision Rules

**When to use standalone vs. federated:**
- **Standalone:** Single domain, small team, monolithic backend, simple data model
- **Federated:** Multiple teams/services, domain-driven design, microservices architecture, independent deployment

**When to use schema stitching vs. federation:**
- **Stitching:** Integrating third-party GraphQL APIs, legacy schema integration, heterogeneous services
- **Federation:** Homogeneous subgraphs, shared entity model, strong type safety, Apollo ecosystem

**n+1 detection triggers:**
- Nested list queries returning multiple items
- One-to-many or many-to-many relationships in schema
- Resolver executes database query in a loop

**Pagination strategy selection:**
- **Offset:** Simple use cases, small datasets, admin interfaces
- **Cursor:** Large datasets, infinite scroll, real-time data, bi-directional pagination

**Stop conditions:**
- If `entities` is empty and no existing schema: ERROR "Cannot generate schema without entity definitions"
- If `federation_config` missing for federated type: ERROR "Federation config required for federated schema"
- If custom scalars lack validation logic: WARN "Custom scalar validation recommended"
- If query depth >10: WARN "Consider query depth limiting"

---

## Output Contract

**Required fields:**
```yaml
schema_definition: |
  # GraphQL SDL string with complete schema
  type Query { ... }
  type Mutation { ... }
  type User { ... }
resolver_patterns:
  dataloader_setup: "Code pattern for DataLoader initialization"
  batch_loading: "Batch loading function examples"
  error_handling: "Error handling middleware pattern"
optimization_config:
  dataloader_enabled: boolean
  query_complexity_limit: integer
  depth_limit: integer
  pagination_type: "offset | cursor"
  caching_strategy: "per-request | redis | none"
```

**Additional fields for federated:**
```yaml
federation_config:
  version: "v2"
  subgraph_name: string
  entities: array
  shared_types: array
  directives_used: ["@key", "@shareable", "@external"]
```

**Security directives (if production optimization):**
```yaml
security_directives:
  - name: "@auth"
    description: "Field-level authorization"
    locations: ["FIELD_DEFINITION", "OBJECT"]
  - name: "@rateLimit"
    description: "Rate limiting per field"
    locations: ["FIELD_DEFINITION"]
```

**Type definitions:**
- `schema_definition`: string (GraphQL SDL)
- `resolver_patterns`: object with code snippets
- `optimization_config`: object with configuration values
- `federation_config`: object (only if schema_type is "federated")
- `security_directives`: array of directive definitions

---

## Examples

**Example: Federated User Service Schema (≤30 lines)**

```graphql
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.0",
        import: ["@key", "@shareable"])

type User @key(fields: "id") {
  id: ID!
  email: String!
  posts: [Post!]! # Resolved via DataLoader
}

type Post @key(fields: "id") {
  id: ID!
  title: String!
  authorId: ID! @external
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

scalar DateTime
```

---

## Quality Gates

**Token budgets (enforced):**
- T1 basic schema: ≤2k tokens
- T2 production optimization: ≤6k tokens
- T3 advanced patterns: ≤12k tokens

**Schema validation:**
- [ ] SDL syntax valid (parse with graphql-js)
- [ ] All field types resolve to defined types or scalars
- [ ] No circular dependencies without proper resolution
- [ ] Query and Mutation root types present
- [ ] Input types for all mutation arguments

**Federation validation (if federated):**
- [ ] All entities have @key directive
- [ ] Reference resolvers implemented
- [ ] No conflicting @shareable types
- [ ] External fields properly marked

**Performance checks:**
- [ ] DataLoader configured for all relationship fields
- [ ] Pagination implemented for list queries
- [ ] Query complexity analysis enabled
- [ ] Depth limiting configured (max 7-10)

**Security gates:**
- [ ] No sensitive data in query arguments (use input types)
- [ ] Authorization directives on protected fields
- [ ] Input validation for custom scalars
- [ ] Error messages don't leak sensitive information

**Determinism:**
- Same inputs produce identical SDL output
- Directive ordering consistent
- Type definitions alphabetically sorted within groups

**Auditability:**
- All schema changes tracked with @deprecated notices
- Breaking changes documented
- Migration guides for deprecated fields

---

## Resources

**GraphQL Specification & Best Practices:**
- GraphQL Specification (October 2021): https://spec.graphql.org/October2021/
- GraphQL Best Practices: https://graphql.org/learn/best-practices/
- GraphQL Schema Design Guide: https://www.apollographql.com/docs/apollo-server/schema/schema/

**Apollo Federation:**
- Apollo Federation v2 Documentation: https://www.apollographql.com/docs/federation/
- Federation Subgraph Specification: https://www.apollographql.com/docs/federation/subgraph-spec/
- Managed Federation Guide: https://www.apollographql.com/docs/federation/managed-federation/overview/

**DataLoader & Optimization:**
- DataLoader GitHub Repository: https://github.com/graphql/dataloader
- Solving the n+1 Problem: https://www.apollographql.com/blog/backend/data-sources/a-deep-dive-on-apollo-data-sources/
- Query Complexity Analysis: https://github.com/slicknode/graphql-query-complexity

**Schema Stitching:**
- Schema Stitching Documentation: https://www.graphql-tools.com/docs/schema-stitching/stitch-combining-schemas
- GraphQL Tools: https://www.graphql-tools.com/

**Authentication & Authorization:**
- GraphQL Authorization Patterns: https://graphql.org/learn/authorization/
- Auth Directives Guide: https://www.apollographql.com/docs/apollo-server/security/authentication/

**Subscriptions:**
- GraphQL Subscriptions Spec: https://spec.graphql.org/October2021/#sec-Subscription
- Apollo Subscriptions: https://www.apollographql.com/docs/apollo-server/data/subscriptions/
