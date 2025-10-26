---
name: Edge Computing Architecture Designer
slug: edge-computing-architect
description: Design edge computing solutions with CDN integration, edge functions, IoT device management, and latency-optimized deployment patterns.
capabilities:
  - Design edge function architectures for Cloudflare Workers, AWS Lambda@Edge, Azure Functions
  - Configure CDN caching strategies and origin shield patterns
  - Architect IoT edge computing deployments with Azure IoT Edge and AWS IoT Greengrass
  - Optimize for edge constraints (latency, bandwidth, intermittent connectivity)
  - Implement edge-cloud hybrid architectures with state synchronization
  - Design multi-CDN strategies with failover and load balancing
inputs:
  - latency_requirements: "Target latency in milliseconds (e.g., <100ms)"
  - deployment_scope: "Geographic distribution (global, regional, single-region)"
  - workload_type: "edge_function | cdn_acceleration | iot_gateway | hybrid"
  - platform_preference: "cloudflare | aws | azure | multi-cloud | platform-agnostic"
  - state_requirements: "stateless | edge_cache | distributed_state | event_sourced"
  - connectivity_model: "always_connected | intermittent | offline_first"
outputs:
  - architecture_diagram: "Edge topology with PoP locations and data flow"
  - deployment_manifest: "Platform-specific configuration (Cloudflare Workers, Lambda@Edge, etc.)"
  - caching_strategy: "Cache hierarchy, TTLs, invalidation patterns"
  - state_sync_design: "CRDT/event sourcing patterns for edge-cloud consistency"
  - performance_estimates: "Expected latency reduction and bandwidth savings"
  - cost_model: "Edge compute and bandwidth cost projections"
keywords:
  - edge-computing
  - cdn
  - cloudflare-workers
  - lambda-edge
  - azure-functions
  - iot-edge
  - content-delivery
  - latency-optimization
  - edge-functions
  - distributed-cache
version: 1.0.0
owner: william
license: CC0-1.0
security: public
links:
  - url: https://workers.cloudflare.com/
    title: Cloudflare Workers Documentation
    access_date: 2025-10-25T21:30:36-04:00
  - url: https://aws.amazon.com/lambda/edge/
    title: AWS Lambda@Edge
    access_date: 2025-10-25T21:30:36-04:00
  - url: https://learn.microsoft.com/en-us/azure/cdn/
    title: Azure Front Door and CDN
    access_date: 2025-10-25T21:30:36-04:00
  - url: https://learn.microsoft.com/en-us/azure/iot-edge/about-iot-edge
    title: Azure IoT Edge Architecture
    access_date: 2025-10-25T21:30:36-04:00
  - url: https://dev.to/karander/edge-computing-in-2025-new-frontiers-for-developers-obo
    title: Edge Computing in 2025 - New Frontiers
    access_date: 2025-10-25T21:30:36-04:00
  - url: https://cloud.google.com/architecture/hybrid-multicloud-patterns-and-practices/edge-hybrid-pattern
    title: Google Cloud Edge Hybrid Pattern
    access_date: 2025-10-25T21:30:36-04:00
---

## Purpose & When-To-Use

Use this skill when you need to design edge computing architectures that bring computation and data closer to users or devices. Trigger conditions include:

- **Latency-critical applications** requiring <100ms response times globally
- **Global content distribution** with CDN acceleration and edge caching
- **IoT device management** with local processing and intermittent connectivity
- **Edge AI inference** for privacy, bandwidth, or real-time requirements
- **Bandwidth optimization** to reduce origin load and transfer costs
- **Geo-distributed workloads** requiring regional data residency

Edge computing reduces latency by 80% for global applications (accessed 2025-10-25T21:30:36-04:00: https://dev.to/karander/edge-computing-in-2025-new-frontiers-for-developers-obo). Common use cases include dynamic web applications, real-time image transformation, A/B testing, bot mitigation, and IoT device orchestration.

## Pre-Checks

**Time normalization:**
```
NOW_ET = 2025-10-25T21:30:36-04:00 (NIST/time.gov semantics)
```

**Input validation:**
- `latency_requirements` must be realistic (10ms-1000ms range)
- `deployment_scope` must specify target regions or "global"
- `workload_type` must be one of: edge_function, cdn_acceleration, iot_gateway, hybrid
- `platform_preference` must align with organizational capabilities
- For IoT workloads, verify `connectivity_model` matches device characteristics

**Constraint checks:**
- Edge functions have size limits (1MB Cloudflare Workers, 50MB Lambda@Edge)
- Edge environments lack full language runtime (JavaScript/WebAssembly preferred)
- Cold start requirements may favor Cloudflare Workers over Lambda@Edge
- IoT edge requires containerized workloads and local orchestration

**Dependency verification:**
- If using cloud-native-deployment-orchestrator patterns, ensure compatibility with edge constraints
- CDN providers must support target regions
- Verify origin infrastructure can handle cache misses and purge traffic

## Procedure

### T1: Fast Path (≤2k tokens) — Quick Edge Pattern Recommendation

**Scenario:** User needs immediate edge architecture guidance for common patterns.

**Steps:**
1. **Classify workload type** from inputs:
   - **edge_function:** Cloudflare Workers or Lambda@Edge for request/response manipulation
   - **cdn_acceleration:** Multi-tier caching with CDN PoPs and origin shield
   - **iot_gateway:** Azure IoT Edge or AWS IoT Greengrass for device orchestration
   - **hybrid:** Combination of edge functions + CDN + cloud backend

2. **Select platform** based on `platform_preference` and workload:
   - **Cloudflare Workers:** Global (330+ cities), minimal cold starts, 50ms to 95% of population (accessed 2025-10-25T21:30:36-04:00: https://workers.cloudflare.com/)
   - **AWS Lambda@Edge:** CloudFront integration, 4 event types (viewer request/response, origin request/response) (accessed 2025-10-25T21:30:36-04:00: https://aws.amazon.com/lambda/edge/)
   - **Azure Functions + Front Door:** Enterprise hybrid scenarios, integrated with Azure IoT Edge (accessed 2025-10-25T21:30:36-04:00: https://learn.microsoft.com/en-us/azure/cdn/)

3. **Generate baseline architecture:**
   ```
   [User] → [CDN PoP] → [Edge Function] → [Origin/API]
              ↓
         [Edge Cache]
   ```

4. **Recommend caching strategy:**
   - **Static assets:** Long TTL (1 day - 1 year), cache-control headers
   - **Dynamic content:** Short TTL (1-60 seconds), stale-while-revalidate
   - **Personalized content:** Edge function with cache partitioning by user segment

5. **Estimate performance:**
   - **Latency reduction:** 80% typical for global distribution
   - **Origin offload:** 90%+ cache hit ratio for static assets
   - **Cost savings:** 60-80% bandwidth reduction vs direct origin

**Output:** Platform recommendation, baseline architecture diagram, caching TTLs, expected latency/cost improvements.

**Abort if:** Latency requirements <10ms (edge can't achieve this) or workload requires stateful operations unsuitable for edge.

### T2: Extended Path (≤6k tokens) — Platform-Specific Architecture Design

**Scenario:** User needs production-ready edge architecture with security, state management, and monitoring.

**Steps:**
1. **Execute T1** to establish baseline.

2. **Design edge function architecture** based on platform:

   **Cloudflare Workers pattern:**
   ```javascript
   // Edge function with KV storage
   addEventListener('fetch', event => {
     event.respondWith(handleRequest(event.request))
   })

   async function handleRequest(request) {
     const cacheKey = new Request(request.url, request)
     const cache = caches.default
     let response = await cache.match(cacheKey)

     if (!response) {
       response = await fetch(request)
       event.waitUntil(cache.put(cacheKey, response.clone()))
     }
     return response
   }
   ```

   **AWS Lambda@Edge pattern:**
   - **Viewer Request:** Auth, URL rewrites, A/B testing (lightweight, <1ms overhead)
   - **Origin Request:** Dynamic content generation, backend routing
   - **Origin Response:** Header manipulation, response caching
   - **Viewer Response:** Compression, security headers

   **Azure IoT Edge pattern (for iot_gateway workload):**
   - **edgeAgent:** Container lifecycle management
   - **edgeHub:** Message routing between modules, devices, and cloud
   - **Custom modules:** Containerized workloads for local processing

3. **Configure CDN caching hierarchy** (accessed 2025-10-25T21:30:36-04:00: https://dev.to/karander/edge-computing-in-2025-new-frontiers-for-developers-obo):
   ```
   Layer 1: Edge PoP (300+ locations) - Cache static assets
   Layer 2: Regional Edge (10-20 locations) - Cache dynamic content
   Layer 3: Origin Shield (2-5 locations) - Protect origin from cache miss storms
   Layer 4: Origin/Cloud - Generate uncached responses
   ```

4. **Design state synchronization** for `distributed_state` or `event_sourced`:
   - **CRDTs (Conflict-free Replicated Data Types):** Local writes, async sync to cloud, automatic conflict resolution
   - **Event Sourcing:** Append-only event log at edge, replay for consistency
   - **Vector Clocks:** Causal consistency across edge nodes

5. **Implement security hardening:**
   - **End-to-end encryption:** TLS 1.3 at edge, mTLS to origin
   - **DDoS protection:** Rate limiting at edge PoP (10k req/s typical)
   - **Bot mitigation:** Challenge-response at edge before reaching origin
   - **WAF rules:** OWASP Top 10 filtering at CDN edge

6. **Configure monitoring and observability:**
   - **Metrics:** Cache hit ratio, edge latency (p50/p95/p99), error rates
   - **Logs:** Request/response logs with sampling (1-10% for cost control)
   - **Tracing:** Distributed traces across edge → origin → backend
   - **Alerts:** Latency SLO violations, cache purge failures, origin health

7. **Design multi-CDN strategy** (if `multi-cloud` or high availability):
   - **Primary CDN:** 80% traffic via DNS/Anycast routing
   - **Secondary CDN:** 20% traffic or automatic failover on primary degradation
   - **DNS-based routing:** GeoDNS with health checks and latency-based selection

8. **Generate deployment manifest:**
   - Cloudflare: `wrangler.toml` with Workers KV bindings
   - AWS: CloudFormation template with Lambda@Edge + CloudFront distribution
   - Azure: ARM template with Front Door + IoT Edge module deployment

**Output:** Production-ready architecture with security, monitoring, state sync patterns, deployment manifests, and runbook for operations.

**Decision point:** If IoT workload detected, branch to IoT-specific orchestration; otherwise continue with edge function optimization.

### T3: Deep Dive (not implemented for T2 skill)

For T3 requirements (cost modeling across multiple providers, chaos engineering for edge resilience, geo-replication strategies), escalate to multicloud-strategy-advisor or cost-optimization-analyzer.

## Decision Rules

**Platform selection criteria:**
- **Cloudflare Workers:** Global reach, minimal cold starts, WebAssembly support, best for <1MB functions
- **AWS Lambda@Edge:** CloudFront integration required, 4-event model, Java/Python/.NET support
- **Azure Functions + Front Door:** Enterprise hybrid, Azure IoT Edge integration, private networking

**Caching decision tree:**
- **Static assets (images, CSS, JS):** Cache at edge PoP, TTL 1 day - 1 year
- **API responses:** Cache at regional edge, TTL 1-60 seconds, vary by query params
- **Personalized content:** Edge function with cache partitioning, user-segment based keys
- **Never cache:** PII, payment data, real-time stock quotes, user-specific dashboards

**State synchronization thresholds:**
- **Stateless (80% of cases):** No edge state, pure request/response transformation
- **Edge cache (15%):** KV store for session data, TTL-based expiration
- **Distributed state (5%):** CRDTs or event sourcing for complex consistency

**Abort conditions:**
- Latency requirement <10ms (edge can't achieve, need colocation)
- Workload requires >50MB code size (exceeds Lambda@Edge limit)
- Strict ACID transactions needed (use cloud database, not edge)
- Regulatory prohibition on data leaving origin region

## Output Contract

**Required fields:**
```json
{
  "platform": "cloudflare | aws | azure | multi-cdn",
  "architecture": {
    "layers": ["cdn_pop", "regional_edge", "origin_shield", "origin"],
    "edge_function_pattern": "viewer_request | origin_request | iot_gateway",
    "caching_hierarchy": {
      "static_assets": {"ttl": "1d-1y", "locations": ["edge_pop"]},
      "dynamic_content": {"ttl": "1s-60s", "locations": ["regional_edge"]}
    }
  },
  "deployment_manifest": "Platform-specific config (wrangler.toml, CFN, ARM)",
  "state_synchronization": "stateless | kv_cache | crdt | event_sourcing",
  "performance_estimates": {
    "latency_reduction_pct": 80,
    "cache_hit_ratio_pct": 90,
    "origin_offload_pct": 85
  },
  "security": {
    "encryption": "TLS 1.3",
    "ddos_protection": true,
    "waf_enabled": true,
    "rate_limiting": "10k req/s per IP"
  },
  "monitoring": {
    "metrics": ["cache_hit_ratio", "edge_latency_p95", "error_rate"],
    "log_sampling_pct": 5,
    "tracing_enabled": true
  }
}
```

**Optional fields:**
- `multi_cdn_config`: Secondary provider and failover rules
- `iot_deployment`: Azure IoT Edge or AWS Greengrass module definitions
- `cost_projection`: Monthly edge compute and bandwidth costs

## Examples

**Example: Global API acceleration with Cloudflare Workers**

```yaml
# Input
latency_requirements: <100ms
deployment_scope: global
workload_type: edge_function
platform_preference: cloudflare
state_requirements: edge_cache

# Output Architecture
platform: cloudflare
edge_function:
  runtime: cloudflare-workers
  kv_namespace: api-cache
  caching:
    static: {ttl: 86400, edge_pop: true}
    api: {ttl: 60, regional: true, stale_while_revalidate: 300}
deployment:
  wrangler.toml: |
    name = "api-accelerator"
    type = "javascript"
    kv_namespaces = [{binding="CACHE", id="abc123"}]
performance:
  latency_reduction: 82%
  cache_hit_ratio: 91%
```

## Quality Gates

**Token budgets:**
- **T1:** ≤2k tokens — Platform selection + baseline architecture
- **T2:** ≤6k tokens — Security, monitoring, deployment manifests, state sync

**Validation:**
- All platform recommendations must cite official documentation (Cloudflare, AWS, Azure)
- Cache TTLs must be justified by content type and update frequency
- Security controls must address OWASP edge security risks
- Performance estimates must be within industry norms (70-90% latency reduction)

**Determinism:**
- Same inputs produce same platform recommendation
- Caching strategies are reproducible based on workload classification

**Safety:**
- No secrets in deployment manifests (use environment variables)
- Rate limiting prevents edge function abuse
- Cost controls via budget alerts and traffic shaping

## Resources

**Official Documentation:**
- Cloudflare Workers: https://workers.cloudflare.com/ (accessed 2025-10-25T21:30:36-04:00)
- AWS Lambda@Edge: https://aws.amazon.com/lambda/edge/ (accessed 2025-10-25T21:30:36-04:00)
- Azure Front Door: https://learn.microsoft.com/en-us/azure/cdn/ (accessed 2025-10-25T21:30:36-04:00)
- Azure IoT Edge: https://learn.microsoft.com/en-us/azure/iot-edge/about-iot-edge (accessed 2025-10-25T21:30:36-04:00)
- Google Cloud Edge Hybrid: https://cloud.google.com/architecture/hybrid-multicloud-patterns-and-practices/edge-hybrid-pattern (accessed 2025-10-25T21:30:36-04:00)

**Architecture Patterns:**
- Edge Computing 2025 Patterns: https://dev.to/karander/edge-computing-in-2025-new-frontiers-for-developers-obo (accessed 2025-10-25T21:30:36-04:00)
- CDN vs Edge Server Design: https://www.geeksforgeeks.org/system-design/cdn-vs-edge-server-system-design/ (accessed 2025-10-25T21:30:36-04:00)

**Templates:**
- See `/skills/edge-computing-architect/resources/` for Cloudflare Workers, Lambda@Edge, and IoT Edge deployment templates
