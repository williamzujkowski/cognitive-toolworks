---
name: RabbitMQ Architecture Designer
slug: messaging-rabbitmq-architect
description: Design RabbitMQ architectures with exchanges, quorum queues, routing patterns, clustering, dead letter exchanges, and AMQP best practices.
capabilities:
  - Exchange type selection and routing pattern design
  - Queue type selection (classic, quorum, streams)
  - Publisher confirms and consumer acknowledgments
  - Clustering topology with quorum queue replication
  - Dead letter exchange (DLX) error handling patterns
  - Message durability and persistence strategies
  - Prefetch tuning and consumer concurrency
  - AMQP protocol best practices
inputs:
  - Message flow requirements (publishers, consumers, routing logic)
  - Exchange types (direct, topic, fanout, headers, consistent hashing)
  - Queue requirements (durability, replication, ordering, priority)
  - Clustering needs (high availability, replication factor)
  - Error handling patterns (DLX, retry, TTL)
  - Performance requirements (throughput, latency, consumer count)
outputs:
  - RabbitMQ topology design (exchanges, queues, bindings)
  - Queue type recommendations (classic vs quorum vs streams)
  - Publisher/consumer configuration (confirms, acks, prefetch)
  - Clustering configuration (node count, replication)
  - DLX error handling setup
  - AMQP connection and channel management patterns
keywords:
  - rabbitmq
  - amqp
  - message-queue
  - exchange
  - routing
  - quorum-queues
  - clustering
  - dead-letter-exchange
  - publisher-confirms
  - consumer-acknowledgments
  - message-broker
  - event-driven
version: "1.0.0"
owner: cognitive-toolworks
license: MIT
security: "Never include credentials in topology definitions. Use environment variables for AMQP URIs. Enable TLS for production. Avoid hardcoding queue/exchange names with sensitive data."
links:
  - title: "RabbitMQ 4.1.0 Release (April 2025)"
    url: "https://www.rabbitmq.com/blog/2025/04/15/rabbitmq-4.1.0-is-released"
    accessed: "2025-10-26"
  - title: "Quorum Queues Documentation"
    url: "https://www.rabbitmq.com/docs/quorum-queues"
    accessed: "2025-10-26"
  - title: "RabbitMQ Exchanges"
    url: "https://www.rabbitmq.com/docs/exchanges"
    accessed: "2025-10-26"
  - title: "Clustering Guide"
    url: "https://www.rabbitmq.com/docs/clustering"
    accessed: "2025-10-26"
  - title: "Dead Letter Exchanges"
    url: "https://www.rabbitmq.com/docs/dlx"
    accessed: "2025-10-26"
---

# RabbitMQ Architecture Designer

## Purpose & When-To-Use

**Trigger conditions:**

* You need to design a RabbitMQ topology with exchanges, queues, and routing patterns
* You need to select queue types (classic, quorum, streams) based on durability and replication needs
* You need to configure publisher confirms or consumer acknowledgments for reliability
* You need to set up clustering for high availability with quorum queue replication
* You need to implement dead letter exchange (DLX) error handling or retry patterns
* You need to optimize consumer prefetch or concurrent processing

**Complements:**

* `integration-messagequeue-designer`: For generic message queue pattern selection (RabbitMQ vs Kafka vs SQS)
* `messaging-kafka-architect`: For Kafka-specific event streaming architectures
* `microservices-pattern-architect`: For saga, CQRS, event sourcing patterns that use RabbitMQ

**Out of scope:**

* RabbitMQ installation and OS-level configuration (use infrastructure automation)
* Monitoring and alerting setup (use `observability-stack-configurator`)
* Client library integration code (use language-specific AMQP client docs)
* Long-term message retention (use Kafka Streams or database for archival)

---

## Pre-Checks

**Time normalization:**

* Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
* Use `NOW_ET` for all access dates in citations

**Verify inputs:**

* ✅ **Required:** At least one message flow definition (publisher → exchange → queue → consumer)
* ✅ **Required:** RabbitMQ version specified (recommend 4.2+ for Khepri metadata store and quorum queue enhancements)
* ⚠️ **Optional:** Exchange type preferences (default to topic for flexibility)
* ⚠️ **Optional:** Queue type (classic, quorum, streams) - default to quorum for durability
* ⚠️ **Optional:** Clustering requirements (node count, replication factor)
* ⚠️ **Optional:** Error handling strategy (DLX, retry backoff, TTL)

**Validate requirements:**

* If high availability needed → quorum queues (since RabbitMQ 3.8, replicated via Raft)
* If ordering required → single active consumer (SAC) or stream queues
* If priorities needed → quorum queues support 2 priorities (high/normal) in RabbitMQ 4.0+
* If broadcasting → fanout exchange
* If complex routing → topic exchange with wildcards

**Source freshness:**

* RabbitMQ 4.2 latest (2025, Khepri metadata store, stream filters) (accessed `NOW_ET`)
* Quorum queues introduced in 3.8, enhanced in 4.0 (priorities, consumer priority for SAC)
* Classic mirrored queues removed in 4.0 (replaced by quorum queues)

**Abort if:**

* No message flow specified → **EMIT TODO:** "Define at least one publisher → exchange → queue → consumer flow"
* Queue type unclear → **EMIT TODO:** "Specify queue requirements: durability (classic/quorum), replication (quorum), or high throughput (streams)"
* Clustering without quorum queues → **EMIT TODO:** "Use quorum queues for replicated, highly available queues (classic queues are single-node in RabbitMQ 4.x)"

---

## Procedure

### T1: Basic RabbitMQ Topology (≤2k tokens, 80% use case)

**Scenario:** Single exchange, single queue, direct routing, no clustering, basic error handling.

**Steps:**

1. **Exchange Type Selection:**
   * **Direct:** Exact routing key match (e.g., `order.created` → `order-processing-queue`)
   * **Topic:** Pattern matching with `*` (1 word) and `#` (0+ words) (e.g., `audit.events.#` matches `audit.events.users.signup`)
   * **Fanout:** Broadcast to all queues (ignore routing key)
   * **T1 recommendation:** Use **topic** exchange for flexibility even if only using exact routing initially

2. **Queue Type Selection:**
   * **Classic:** Single node, non-replicated (use only for dev/test)
   * **Quorum:** Replicated (Raft consensus), durable, data safety (use for production)
   * **Streams:** High throughput, append-only log (use for event streaming)
   * **T1 recommendation:** Use **quorum queue** with `x-queue-type=quorum` argument

3. **Publisher Configuration:**
   * Enable **publisher confirms** for reliability (wait for broker acknowledgment)
   * Set **delivery mode = 2** for persistent messages (survive broker restart)
   * **T1 recommendation:** Use streaming confirms (handle confirms as they arrive)

4. **Consumer Configuration:**
   * Use **manual acknowledgments** (ack after successful processing)
   * Set **prefetch count = 10** (balance between throughput and backpressure)
   * **T1 recommendation:** Ack after processing, nack+requeue on transient errors

5. **Basic Topology:**
   * 1 topic exchange (`events`)
   * 1 quorum queue (`order-processing-queue`)
   * 1 binding (`order.created` → `order-processing-queue`)
   * Publisher → `events` exchange with routing key `order.created`
   * Consumer → `order-processing-queue` with manual ack + prefetch=10

**Output:**

* Topology diagram: 1 exchange, 1 queue, 1 binding
* Publisher config: confirms enabled, persistent messages
* Consumer config: manual ack, prefetch=10

**Token budget:** ≤2000 tokens

---

### T2: Multi-Exchange Routing + DLX Error Handling (≤6k tokens)

**Scenario:** Multiple exchanges with complex routing, dead letter exchange for errors, quorum queues, retry with backoff.

**Steps:**

1. **Multi-Exchange Topology:**

   **Pattern:** Separate exchanges for different message types or bounded contexts
   * **Example:**
     * `orders-exchange` (topic) → routes to `order-processing-queue`, `order-audit-queue`
     * `payments-exchange` (topic) → routes to `payment-processing-queue`
     * `notifications-exchange` (fanout) → broadcasts to all notification queues

2. **Topic Exchange Routing Patterns:**

   **Wildcards:**
   * `*` matches exactly one word (e.g., `order.*.created` matches `order.online.created` but not `order.created`)
   * `#` matches zero or more words (e.g., `audit.#` matches `audit.users`, `audit.users.signup`, `audit`)

   **Example bindings:**
   * `order.created` → `order-processing-queue` (exact match)
   * `order.#` → `order-audit-queue` (all order events)
   * `payment.processed` → `payment-processing-queue`
   * `notification.*` → `notification-email-queue`, `notification-sms-queue` (broadcast via topic)

3. **Dead Letter Exchange (DLX) Setup:**

   **Use cases:**
   * Handle messages rejected by consumers (nack without requeue)
   * Handle messages exceeding TTL (time-to-live)
   * Handle messages exceeding delivery limit (quorum queues default limit=20)

   **Configuration via policy (recommended):**
   ```json
   {
     "pattern": "order-processing-queue",
     "definition": {
       "dead-letter-exchange": "dlx-exchange",
       "dead-letter-routing-key": "order.processing.failed",
       "message-ttl": 86400000,
       "delivery-limit": 20
     }
   }
   ```

   **DLX topology:**
   * Main queue: `order-processing-queue` (quorum)
   * Dead letter exchange: `dlx-exchange` (topic)
   * Dead letter queue: `dlx-order-processing-queue` (quorum, for manual inspection)
   * Binding: `order.processing.failed` → `dlx-order-processing-queue`

4. **Retry with Backoff Pattern:**

   **Pattern:** Use TTL + DLX to implement delayed retries
   * **Step 1:** Consumer nacks message without requeue → DLX routes to `retry-queue-5s` (TTL=5s)
   * **Step 2:** After 5s, message expires → routes back to main queue via DLX
   * **Step 3:** Repeated failures trigger delivery limit → routes to final DLX for manual handling

   **Example:**
   * Main queue: `order-processing-queue`
   * Retry queue 1: `retry-order-5s` (TTL=5s, DLX=`orders-exchange`)
   * Retry queue 2: `retry-order-30s` (TTL=30s, DLX=`orders-exchange`)
   * Final DLX: `dlx-order-processing-queue` (manual inspection)

5. **Quorum Queue Configuration:**

   **Arguments:**
   * `x-queue-type=quorum` (replicated queue)
   * `x-quorum-initial-group-size=3` (replication factor, odd number for Raft consensus)
   * `x-delivery-limit=20` (max redeliveries before DLX, default in RabbitMQ 4.0+)
   * `x-max-priority=2` (RabbitMQ 4.0+ supports exactly 2 priorities: normal and high)

   **Publisher priority:**
   * Publish with `priority=5` (high priority, delivered 2:1 ratio vs normal)
   * Publish with `priority=0` or no priority (normal priority)

6. **Consumer Acknowledgment Strategies:**

   **Manual ack (recommended):**
   * Process message → `basic.ack` (remove from queue)
   * Transient error (network timeout) → `basic.nack` + `requeue=true` (redelivery)
   * Permanent error (invalid data) → `basic.nack` + `requeue=false` (send to DLX)

   **Prefetch tuning:**
   * Low prefetch (1-10): Better fairness, lower throughput
   * High prefetch (50-100): Higher throughput, risk of consumer overload
   * **Recommendation:** Start with prefetch=10, tune based on processing time and consumer count

**Output:**

* Multi-exchange topology (orders, payments, notifications)
* Topic routing patterns with wildcards
* DLX error handling with retry backoff
* Quorum queue configuration
* Publisher/consumer config (confirms, acks, prefetch)

**Token budget:** ≤6000 tokens

---

### T3: Clustering + Streams + Advanced Patterns (≤12k tokens)

**Scenario:** Multi-node cluster with quorum queue replication, stream queues for high throughput, federation for multi-DC.

**Steps:**

1. **Clustering Topology:**

   **Best practices:**
   * **Odd number of nodes:** 3, 5, or 7 nodes (Raft consensus requires majority)
   * **Equal peers:** All nodes are equal (no leader/follower at cluster level, but quorum queues use Raft leader election)
   * **Network requirements:** Nodes must resolve hostnames, ports 4369 (epmd), 25672 (inter-node), 5672 (AMQP) open
   * **Avoid 2-node clusters:** No clear majority during network partitions

   **Example 3-node cluster:**
   * Node 1: `rabbit@node1.example.com`
   * Node 2: `rabbit@node2.example.com`
   * Node 3: `rabbit@node3.example.com`
   * Erlang cookie: same on all nodes (authentication)

   **Quorum queue replication:**
   * Quorum queues replicate across 3 nodes (configurable via `x-quorum-initial-group-size`)
   * Raft leader elected automatically (handles writes)
   * Followers replicate data (handle reads if leader down)
   * Survives minority node failures (e.g., 1 node down in 3-node cluster)

2. **Stream Queues for High Throughput:**

   **Use case:** Event streaming, audit logs, high-volume data ingestion (millions of messages/sec)

   **Characteristics:**
   * Append-only log (like Kafka topics)
   * Multiple consumers can read from same offset
   * Retention based on size or time (not per-consumer)
   * RabbitMQ 4.2: SQL filter expressions (4M+ msg/sec filtering with Bloom filters)

   **Configuration:**
   ```json
   {
     "x-queue-type": "stream",
     "x-max-age": "7D",
     "x-stream-max-segment-size-bytes": 500000000
   }
   ```

   **Consumer offset tracking:**
   * Consumer specifies offset: `first`, `last`, `next`, or timestamp
   * Offset stored server-side (like Kafka consumer groups)

3. **Consistent Hashing Exchange (Plugin):**

   **Use case:** Shard messages across multiple queues for horizontal scaling

   **Pattern:**
   * Consistent hashing exchange routes based on routing key hash
   * Messages with same routing key always go to same queue (ordering guarantee)
   * Add/remove queues with minimal redistribution

   **Example:**
   * Exchange: `sharded-orders` (type=`x-consistent-hash`)
   * Queues: `orders-shard-0`, `orders-shard-1`, `orders-shard-2`
   * Routing key: `user-123` → always routes to same shard

4. **Federation for Multi-DC:**

   **Use case:** Replicate messages across datacenters without clustering (clusters require low-latency networks)

   **Pattern:**
   * Upstream (DC1): `orders-exchange`
   * Downstream (DC2): `orders-exchange-federated` (receives messages from DC1)
   * Federation link: DC2 pulls messages from DC1 `orders-exchange`

   **Benefits:**
   * Survives WAN latency and network partitions (unlike clustering)
   * Independent RabbitMQ clusters in each DC
   * Messages flow one-way (upstream → downstream)

5. **Advanced Publisher Patterns:**

   **Transactional publishing (avoid, heavyweight):**
   * AMQP transactions (`tx.select`, `tx.commit`) → very slow, blocks channel
   * **Use publisher confirms instead** (asynchronous, higher throughput)

   **Batch publishing:**
   * Publish multiple messages, then wait for confirms in batch
   * Higher throughput than individual confirms
   * Risk: larger batch = longer recovery time on failure

6. **Single Active Consumer (SAC) for Ordering:**

   **Use case:** Ensure messages processed in order by allowing only one consumer at a time

   **Configuration:**
   * Queue argument: `x-single-active-consumer=true`
   * RabbitMQ selects one consumer as active, others wait
   * Automatic failover to standby consumer if active consumer dies
   * **RabbitMQ 4.0+:** Consumer priority for SAC (higher priority consumers selected first)

7. **Message Priority in Quorum Queues:**

   **RabbitMQ 4.0+ feature:**
   * Quorum queues support exactly **2 priorities**: high and normal
   * No upfront declaration needed (unlike classic queues)
   * Consumers receive **2:1 ratio** of high to normal priority messages (avoid starvation)
   * Publish with `priority=5` (high) or `priority=0`/unset (normal)

**Output:**

* 3-node cluster topology with quorum queue replication
* Stream queue configuration for high-throughput use cases
* Consistent hashing exchange for sharding
* Federation setup for multi-DC replication
* SAC and message priority patterns

**Token budget:** ≤12000 tokens

---

## Decision Rules

**Exchange type selection:**

* **Direct:** Exact routing, one-to-one (e.g., task queues, RPC)
* **Topic:** Pattern matching, one-to-many with hierarchical routing (e.g., event bus, audit logs)
* **Fanout:** Broadcast, one-to-all (e.g., notifications, cache invalidation)
* **Headers:** Route by message headers (rare, use topic instead)

**Queue type selection:**

* **Classic:** Dev/test only (single node, non-replicated in RabbitMQ 4.x)
* **Quorum:** Production (replicated, durable, Raft consensus, survives node failures)
* **Streams:** High throughput + retention (append-only, multi-consumer reads, event streaming)

**Clustering decisions:**

* **Single node:** Dev/test, <1000 msg/sec
* **3-node cluster:** Production, high availability, survives 1 node failure
* **5-node cluster:** Mission-critical, survives 2 node failures
* **7+ node cluster:** Rare (Raft consensus overhead increases, consider federation instead)

**Prefetch tuning:**

* **1-10:** Low throughput, fair distribution, consumer processing time >100ms
* **10-50:** Medium throughput, balanced, consumer processing time 10-100ms
* **50-100:** High throughput, consumer processing time <10ms

**Error handling strategy:**

* **Transient errors:** `nack + requeue=true` (network timeout, downstream unavailable)
* **Permanent errors:** `nack + requeue=false → DLX` (invalid data, schema mismatch)
* **Retry with backoff:** DLX → TTL queue → re-route to main queue after delay
* **Poison messages:** Delivery limit (default=20) → DLX for manual inspection

**Abort conditions:**

* Quorum queue replication factor >cluster size → reduce to match node count
* Prefetch >1000 → risk of consumer memory exhaustion
* Classic queues in production → migrate to quorum queues for durability

---

## Output Contract

**Topology schema:**

```yaml
exchanges:
  - name: <exchange_name>
    type: direct|topic|fanout|headers
    durable: true|false
    auto_delete: true|false

queues:
  - name: <queue_name>
    type: classic|quorum|stream
    durable: true|false
    arguments:
      x-queue-type: quorum
      x-quorum-initial-group-size: 3
      x-delivery-limit: 20
      x-max-priority: 2  # RabbitMQ 4.0+ only
      x-single-active-consumer: true|false

bindings:
  - exchange: <exchange_name>
    queue: <queue_name>
    routing_key: <pattern>  # e.g., order.created, order.#, *

policies:
  - name: <policy_name>
    pattern: <queue_regex>
    definition:
      dead-letter-exchange: <dlx_exchange>
      dead-letter-routing-key: <dlx_routing_key>
      message-ttl: <milliseconds>
      delivery-limit: 20
```

**Publisher config:**

```python
# Publisher confirms
channel.confirm_delivery()

# Persistent messages
channel.basic_publish(
    exchange='orders-exchange',
    routing_key='order.created',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # persistent
        priority=5        # high priority (RabbitMQ 4.0+)
    )
)
```

**Consumer config:**

```python
# Manual ack + prefetch
channel.basic_qos(prefetch_count=10)

def callback(ch, method, properties, body):
    try:
        process(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except TransientError:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    except PermanentError:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # → DLX

channel.basic_consume(queue='order-processing-queue', on_message_callback=callback)
```

**Required fields:**

* Topology: `exchanges[]`, `queues[]`, `bindings[]`
* Exchange: `name`, `type`
* Queue: `name`, `type` (classic/quorum/stream)
* Binding: `exchange`, `queue`, `routing_key`

---

## Examples

### Example: E-commerce Order Processing with DLX

**Topology:**

* Exchange: `orders-exchange` (topic)
* Queue: `order-processing-queue` (quorum, x-quorum-initial-group-size=3)
* DLX: `dlx-exchange` (topic)
* DLX Queue: `dlx-order-processing-queue` (quorum, manual inspection)
* Binding: `order.created` → `order-processing-queue`
* DLX Binding: `order.processing.failed` → `dlx-order-processing-queue`

**Policy (DLX config):**

```json
{
  "pattern": "order-processing-queue",
  "definition": {
    "dead-letter-exchange": "dlx-exchange",
    "dead-letter-routing-key": "order.processing.failed",
    "delivery-limit": 20
  }
}
```

**Publisher:**

```python
channel.basic_publish(
    exchange='orders-exchange',
    routing_key='order.created',
    body=json.dumps(order),
    properties=pika.BasicProperties(delivery_mode=2)
)
```

**Consumer:**

```python
def process_order(ch, method, properties, body):
    try:
        order = json.loads(body)
        # Process order (may fail)
        charge_payment(order)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except PaymentGatewayDown:  # Transient error
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    except InvalidPaymentMethod:  # Permanent error
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # → DLX
```

---

## Quality Gates

**Token budgets:**

* **T1:** ≤2000 tokens (single exchange + queue + basic config)
* **T2:** ≤6000 tokens (multi-exchange + DLX + routing patterns)
* **T3:** ≤12000 tokens (clustering + streams + federation)

**Safety:**

* ❌ **Never:** Hardcode credentials in topology definitions
* ❌ **Never:** Use classic queues for production (single node, no replication)
* ✅ **Always:** Enable publisher confirms for reliability
* ✅ **Always:** Use manual acks for consumers (process then ack)
* ✅ **Always:** Use quorum queues for durability (replicated, Raft consensus)

**Auditability:**

* All topology definitions in version control (Git)
* Policies defined via management API or config (not hardcoded queue arguments)
* DLX queues monitored for poison messages
* Consumer ack/nack rates tracked (avoid excessive requeues)

**Determinism:**

* Same topology definition = same exchange/queue/binding creation
* Quorum queue leader election deterministic (Raft)
* Topic routing deterministic (same routing key → same queue)

**Performance:**

* Prefetch tuned for consumer processing time (avoid memory exhaustion)
* Quorum queue replication factor ≤ node count
* Stream queues for >10k msg/sec throughput
* Publisher confirms in batches for higher throughput (not individual)

---

## Resources

**Official Documentation:**

* RabbitMQ 4.1.0 release (Khepri metadata store, quorum queue enhancements): https://www.rabbitmq.com/blog/2025/04/15/rabbitmq-4.1.0-is-released (accessed `NOW_ET`)
* Quorum queues: https://www.rabbitmq.com/docs/quorum-queues (accessed `NOW_ET`)
* Exchanges and routing: https://www.rabbitmq.com/docs/exchanges (accessed `NOW_ET`)
* Clustering: https://www.rabbitmq.com/docs/clustering (accessed `NOW_ET`)
* Dead letter exchanges: https://www.rabbitmq.com/docs/dlx (accessed `NOW_ET`)
* Publishers: https://www.rabbitmq.com/docs/publishers (accessed `NOW_ET`)
* Consumers: https://www.rabbitmq.com/docs/consumers (accessed `NOW_ET`)

**Client Libraries:**

* Python: pika (AMQP 0-9-1 client)
* Java: amqp-client (official Java client)
* Node.js: amqplib
* Go: amqp091-go

**Related Skills:**

* `integration-messagequeue-designer`: Generic message queue pattern selection
* `messaging-kafka-architect`: Kafka-specific event streaming
* `microservices-pattern-architect`: Saga, CQRS, event sourcing with RabbitMQ
* `observability-stack-configurator`: Monitoring RabbitMQ with Prometheus + Grafana
