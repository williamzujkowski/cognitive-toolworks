---
name: Message Queue Pattern Designer
slug: integration-messagequeue-designer
description: Design message queue patterns for RabbitMQ, Kafka, SQS, Azure Service Bus with dead-letter queues, idempotency, ordering guarantees, and backpressure
capabilities:
  - Queue/topic topology design for distributed systems
  - Producer/consumer pattern implementation
  - Exactly-once and at-least-once semantics configuration
  - Dead-letter queue and retry strategies
  - Partition/shard strategy for ordering and throughput
  - Backpressure and consumer scaling patterns
inputs:
  queue_system:
    type: enum
    values: [rabbitmq, kafka, sqs, azure-servicebus, pubsub]
    required: true
  pattern:
    type: enum
    values: [publish-subscribe, work-queue, request-reply, saga]
    required: true
  guarantees:
    type: enum
    values: [at-least-once, at-most-once, exactly-once]
    required: true
  throughput_estimate:
    type: string
    description: "Expected message rate (e.g., '10k msg/sec')"
    required: false
  ordering_scope:
    type: enum
    values: [global, partition-key, none]
    required: false
outputs:
  queue_config:
    type: object
    description: Topic/queue/exchange definitions with partitioning
  producer_code:
    type: code_snippet
    description: Message publishing with idempotency keys
  consumer_code:
    type: code_snippet
    description: Message consumption with error handling and retries
  monitoring:
    type: object
    description: Metrics, alarms, and observability configuration
keywords:
  - message-queue
  - kafka
  - rabbitmq
  - sqs
  - azure-service-bus
  - pubsub
  - dead-letter-queue
  - idempotency
  - exactly-once
  - backpressure
version: 1.0.0
owner: william
license: MIT
security:
  risk_level: low
  notes: "Outputs infrastructure code; user must secure credentials separately"
links:
  - https://kafka.apache.org/documentation/
  - https://www.rabbitmq.com/getstarted.html
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://aws.amazon.com/sqs/
  - https://learn.microsoft.com/en-us/azure/service-bus-messaging/
---

---

## Purpose & When-To-Use

Use this skill when:

* Designing event-driven architectures with publish-subscribe or work-queue patterns
* Implementing saga orchestration, CQRS event sourcing, or async request-reply
* Ensuring message delivery guarantees (at-least-once, exactly-once) across distributed services
* Configuring dead-letter queues, retry policies, and idempotency for resilience
* Optimizing throughput and ordering via partitioning or consumer groups
* Migrating between queue systems (e.g., RabbitMQ → Kafka) or multi-cloud setups

**Do not use** for:

* Synchronous RPC (use gRPC, REST)
* In-memory queues (use language-native channels)
* Real-time streaming analytics requiring sub-100ms latency (consider Apache Flink or Spark Streaming)

---

## Pre-Checks

1. **Time normalization:** Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601).
2. **Input validation:**
   - `queue_system` must be one of: `rabbitmq`, `kafka`, `sqs`, `azure-servicebus`, `pubsub`
   - `pattern` must be one of: `publish-subscribe`, `work-queue`, `request-reply`, `saga`
   - `guarantees` must be one of: `at-least-once`, `at-most-once`, `exactly-once`
   - If `guarantees = exactly-once`, verify target system supports it (Kafka, SQS FIFO, Azure Service Bus sessions)
3. **Source freshness:** Confirm documentation links resolve and match claimed semantics (accessed `NOW_ET`).

---

## Procedure

### Tier 1 (≤2k tokens): Basic Queue/Topic Configuration

**Scope:** Single queue/topic with default reliability; common 80% case.

1. **Select topology:**
   - **Publish-Subscribe:** Topic/fanout exchange with multiple subscribers
   - **Work-Queue:** Single queue with competing consumers for load balancing
   - **Request-Reply:** Temporary reply-to queues or correlation IDs
   - **Saga:** Choreography via event topic or orchestration via command queues

2. **Configure queue/topic:**
   - **Kafka:** Create topic with `num.partitions` based on throughput and ordering scope
   - **RabbitMQ:** Declare exchange type (fanout, topic, direct) + queues with bindings
   - **SQS:** Standard queue (best-effort ordering) or FIFO queue (ordering + deduplication)
   - **Azure Service Bus:** Queue (point-to-point) or Topic/Subscription (pub-sub)
   - **Google Pub/Sub:** Topic with push/pull subscriptions

3. **Set retention/TTL:**
   - Kafka: `retention.ms` (default 7 days)
   - RabbitMQ: `x-message-ttl` and `x-expires` for queues
   - SQS: `MessageRetentionPeriod` (1 min to 14 days)
   - Azure Service Bus: `DefaultMessageTimeToLive`
   - Pub/Sub: `messageRetentionDuration` (default 7 days)

4. **Emit basic producer/consumer snippets** (idiomatic SDK usage).

**Output:** Minimal config + code for immediate deployment.

---

### Tier 2 (≤6k tokens): Advanced Patterns (DLQ, Idempotency, Ordering, Retry)

**Scope:** Production-grade reliability with error handling.

1. **Dead-Letter Queue (DLQ):**
   - **Kafka:** No native DLQ; implement via exception handler writing to separate topic
   - **RabbitMQ:** Set `x-dead-letter-exchange` on queue
   - **SQS:** Configure `RedrivePolicy` with `maxReceiveCount`
   - **Azure Service Bus:** Enable `DeadLetteringOnMessageExpiration` and `MaxDeliveryCount`
   - **Pub/Sub:** Set `deadLetterPolicy` on subscription

2. **Idempotency:**
   - **Producer:** Include unique `message-id` or `idempotency-key` header
   - **Consumer:** Store processed IDs in fast cache (Redis) or database with TTL
   - **Exactly-once (Kafka):** Enable `enable.idempotence=true` + transactional producer (`transactional.id`)
   - **SQS FIFO:** Use `MessageDeduplicationId` (5-minute dedup window)

3. **Ordering guarantees:**
   - **Global ordering:** Kafka single partition, SQS FIFO, Azure Service Bus sessions
   - **Partition-key ordering:** Kafka partition by key, Pub/Sub ordering key
   - **None:** Parallel consumers for max throughput

4. **Retry strategy:**
   - **Exponential backoff:** 1s → 2s → 4s → 8s → DLQ
   - **Visibility timeout (SQS):** Extend during processing to prevent duplicate delivery
   - **RabbitMQ:** Use `x-retry` plugin or TTL + DLX loop
   - **Kafka:** Manual commit after success; rewind offset on transient errors

5. **Cite sources** (accessed `NOW_ET`):
   - Kafka idempotence: https://kafka.apache.org/documentation/#producerconfigs_enable.idempotence (accessed 2025-10-26T02:31:20)
   - RabbitMQ DLQ: https://www.rabbitmq.com/dlx.html (accessed 2025-10-26T02:31:20)
   - Enterprise Integration Patterns: https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html (accessed 2025-10-26T02:31:20)
   - AWS SQS FIFO: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html (accessed 2025-10-26T02:31:20)

**Output:** Config + code with DLQ, idempotency, retry, and ordering.

---

### Tier 3 (≤12k tokens): Complex Scenarios (Backpressure, Consumer Scaling, Monitoring)

**Scope:** High-throughput, multi-region, or regulated environments.

1. **Backpressure handling:**
   - **Kafka:** Tune `fetch.min.bytes`, `fetch.max.wait.ms` to batch efficiently; monitor consumer lag
   - **RabbitMQ:** Use `prefetch_count` to limit unacknowledged messages per consumer
   - **SQS:** Implement exponential backoff when `ReceiveMessage` returns empty
   - **Azure Service Bus:** Set `MaxConcurrentCalls` on message receiver
   - **Pub/Sub:** Use flow control settings (`maxMessages`, `maxBytes`)

2. **Consumer scaling:**
   - **Kafka:** Add consumers to group up to `num.partitions`; beyond that, add partitions
   - **RabbitMQ:** Horizontal scaling via multiple workers on same queue
   - **SQS:** Spawn workers based on `ApproximateNumberOfMessages` metric
   - **Azure Service Bus:** Scale subscription consumers independently
   - **Autoscaling:** Trigger on queue depth or consumer lag (e.g., KEDA for Kubernetes)

3. **Monitoring and alerting:**
   - **Metrics to track:**
     - Queue depth / consumer lag (critical)
     - Message throughput (published vs. consumed)
     - DLQ message count
     - Processing latency (end-to-end)
     - Error rate (exceptions, retries)
   - **Tools:**
     - Kafka: Burrow, Confluent Control Center, Prometheus JMX exporter
     - RabbitMQ: Management UI, Prometheus plugin
     - SQS: CloudWatch metrics (`ApproximateNumberOfMessagesVisible`, `ApproximateAgeOfOldestMessage`)
     - Azure Service Bus: Azure Monitor metrics
     - Pub/Sub: Cloud Monitoring (Stackdriver)
   - **Alerts:**
     - Consumer lag > 10k messages for >5 minutes
     - DLQ depth > 100
     - Processing latency p95 > 30s

4. **Multi-region / disaster recovery:**
   - **Kafka:** MirrorMaker 2 or cluster linking for replication
   - **RabbitMQ:** Federation or Shovel plugin
   - **SQS:** Cross-region replication not native; use Lambda or custom replicator
   - **Azure Service Bus:** Geo-disaster recovery pairing
   - **Pub/Sub:** Regional topics; replicate via Dataflow

5. **Security and compliance:**
   - **Encryption in transit:** TLS/SSL for all systems
   - **Encryption at rest:** Kafka encrypted disks, SQS KMS, Azure Service Bus customer-managed keys
   - **Access control:** Kafka ACLs, RabbitMQ user permissions, IAM policies (SQS, Pub/Sub), Azure RBAC
   - **Audit logging:** Enable broker audit logs and consumer access logs

**Output:** Full architecture with scaling, monitoring, DR, and compliance.

---

## Decision Rules

* **If `guarantees = exactly-once` and system does not support it:** Warn user and downgrade to `at-least-once` with idempotency implementation.
* **If `ordering_scope = global` and `throughput_estimate > 10k msg/sec`:** Suggest partition-key ordering to parallelize.
* **If `pattern = saga` and no compensation logic provided:** Emit skeleton event handlers with `TODO: implement compensation`.
* **If DLQ depth exceeds threshold:** Alert and recommend manual review or automated replay with fixes.
* **Abort if:**
  - Required input (`queue_system`, `pattern`, `guarantees`) is missing or invalid.
  - Source documentation is unreachable or contradicts claimed semantics.

---

## Output Contract

```typescript
{
  queue_config: {
    system: string,               // e.g., "kafka"
    topology: {
      topics?: Array<{
        name: string,
        partitions: number,
        replication_factor: number,
        config: Record<string, any>
      }>,
      queues?: Array<{
        name: string,
        durable: boolean,
        dlq?: string,
        config: Record<string, any>
      }>,
      exchanges?: Array<{        // RabbitMQ
        name: string,
        type: string,
        bindings: Array<any>
      }>
    }
  },
  producer_code: string,          // Language-agnostic or specified language
  consumer_code: string,          // Includes error handling, retries, idempotency
  monitoring: {
    metrics: Array<string>,       // e.g., ["consumer_lag", "dlq_depth"]
    alerts: Array<{
      condition: string,
      threshold: number,
      action: string
    }>
  },
  sources: Array<{
    title: string,
    url: string,
    accessed: string              // ISO-8601 timestamp = NOW_ET
  }>
}
```

**Required fields:**
- `queue_config.system`
- `queue_config.topology` (non-empty)
- `producer_code`
- `consumer_code`
- `monitoring.metrics` (≥2)
- `sources` (≥2 for T2+)

---

## Examples

**Input:**
```yaml
queue_system: kafka
pattern: publish-subscribe
guarantees: exactly-once
throughput_estimate: 50k msg/sec
ordering_scope: partition-key
```

**Output (Kafka Topic Config with Partitioning):**
```json
{
  "queue_config": {
    "system": "kafka",
    "topology": {
      "topics": [{
        "name": "orders.events",
        "partitions": 12,
        "replication_factor": 3,
        "config": {
          "min.insync.replicas": 2,
          "retention.ms": 604800000,
          "compression.type": "snappy"
        }
      }]
    }
  },
  "producer_code": "props.put(\"enable.idempotence\", true);\nprops.put(\"transactional.id\", \"order-producer-1\");\nProducerRecord<String, Order> record = new ProducerRecord<>(\"orders.events\", order.getCustomerId(), order);",
  "consumer_code": "props.put(\"isolation.level\", \"read_committed\");\nconsumer.subscribe(\"orders.events\");\nwhile(true) {\n  records = consumer.poll(100);\n  for (record : records) {\n    processOrder(record.value());\n  }\n  consumer.commitSync();\n}",
  "monitoring": {
    "metrics": ["consumer_lag", "partition_throughput"],
    "alerts": [{"condition": "lag > 10000", "threshold": 10000, "action": "scale_consumers"}]
  }
}
```

---

## Quality Gates

1. **Token budgets:**
   - T1 response ≤ 2k tokens
   - T2 response ≤ 6k tokens
   - T3 response ≤ 12k tokens

2. **Safety:**
   - No hardcoded credentials in output
   - Warn if encryption-at-rest is disabled in production scenarios

3. **Auditability:**
   - All T2+ outputs include ≥2 sources with access dates = `NOW_ET`
   - Config includes version/schema metadata

4. **Determinism:**
   - Same inputs → same config structure (semantic equivalence)
   - Non-deterministic: partition count may vary based on throughput heuristic

5. **Example constraints:**
   - Example code ≤30 lines
   - Runnable or clear pseudo-code with language annotation

---

## Resources

* **Apache Kafka Documentation** (official): https://kafka.apache.org/documentation/ (accessed 2025-10-26T02:31:20)
* **RabbitMQ Getting Started** (official): https://www.rabbitmq.com/getstarted.html (accessed 2025-10-26T02:31:20)
* **Enterprise Integration Patterns** (Hohpe & Woolf): https://www.enterpriseintegrationpatterns.com/patterns/messaging/ (accessed 2025-10-26T02:31:20)
* **AWS SQS Developer Guide** (official): https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/ (accessed 2025-10-26T02:31:20)
* **Azure Service Bus Messaging** (official): https://learn.microsoft.com/en-us/azure/service-bus-messaging/ (accessed 2025-10-26T02:31:20)
* **Google Cloud Pub/Sub Documentation** (official): https://cloud.google.com/pubsub/docs (accessed 2025-10-26T02:31:20)
* **Kafka Idempotence and Transactions** (Confluent): https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/ (accessed 2025-10-26T02:31:20)
* **RabbitMQ Dead Letter Exchanges**: https://www.rabbitmq.com/dlx.html (accessed 2025-10-26T02:31:20)
* **SQS FIFO Queues**: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html (accessed 2025-10-26T02:31:20)
