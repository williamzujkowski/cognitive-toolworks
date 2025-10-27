---
name: Kafka Messaging Architect
slug: messaging-kafka-architect
description: Design Apache Kafka architectures with producer/consumer patterns, exactly-once semantics, Kafka Streams, ksqlDB, Schema Registry (Avro/Protobuf), performance tuning, and KRaft deployment.
capabilities:
  - Kafka topology design (topics, partitions, replication factor, KRaft vs ZooKeeper)
  - Producer patterns (idempotent, transactional, batching, compression, exactly-once)
  - Consumer patterns (consumer groups, offset management, manual commit, exactly-once)
  - Kafka Streams and ksqlDB (stateful processing, windowing, joins, aggregations)
  - Schema Registry integration (Avro, Protobuf, JSON Schema evolution)
  - Performance tuning (batch.size, linger.ms, buffer.memory, fetch.min.bytes, compression)
  - High availability and disaster recovery (replication, MirrorMaker 2, multi-DC)
  - Security (SASL, TLS, ACLs, encryption at rest)
  - Monitoring and observability (JMX metrics, lag monitoring, consumer group health)
  - Event-driven patterns (event sourcing, CQRS, saga, outbox pattern)
inputs:
  use_case:
    type: string
    description: Use case (event streaming, log aggregation, messaging, CDC, stream processing)
    required: true
  throughput:
    type: object
    description: Expected throughput (messages/sec, MB/sec, peak vs average)
    required: true
  data_schema:
    type: object
    description: Message schema (Avro, Protobuf, JSON) and evolution requirements
    required: false
  durability_requirements:
    type: string
    description: Durability level (at-most-once, at-least-once, exactly-once)
    required: false
  deployment_env:
    type: string
    description: Deployment environment (on-prem, cloud, managed service)
    required: false
outputs:
  kafka_topology:
    type: object
    description: Topic design, partitions, replication factor, retention policy
  producer_config:
    type: object
    description: Producer settings (idempotence, compression, batching, acks)
  consumer_config:
    type: object
    description: Consumer settings (group.id, auto.offset.reset, isolation.level)
  schema_registry_config:
    type: object
    description: Schema Registry setup with Avro/Protobuf schemas
  performance_tuning:
    type: object
    description: Tuned settings for throughput and latency targets
  monitoring_setup:
    type: object
    description: JMX metrics, lag alerts, consumer group health checks
keywords:
  - kafka
  - messaging
  - event-streaming
  - kafka-streams
  - ksqldb
  - schema-registry
  - avro
  - protobuf
  - exactly-once
  - consumer-groups
  - kraft
  - performance-tuning
  - event-driven
version: 1.0.0
owner: cognitive-toolworks
license: Apache-2.0
security:
  secrets: "Use SASL/SCRAM or mTLS for authentication; store credentials in secrets manager"
  compliance: "Encryption in transit (TLS), encryption at rest, audit logging for sensitive data"
links:
  - title: "Apache Kafka 3.9 Release Notes"
    url: "https://www.confluent.io/blog/introducing-apache-kafka-3-9/"
    accessed: "2025-10-26"
  - title: "Kafka Exactly-Once Semantics"
    url: "https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/"
    accessed: "2025-10-26"
  - title: "Confluent Schema Registry"
    url: "https://docs.confluent.io/platform/current/schema-registry/index.html"
    accessed: "2025-10-26"
  - title: "Kafka Performance Tuning"
    url: "https://docs.confluent.io/cloud/current/client-apps/optimizing/throughput.html"
    accessed: "2025-10-26"
  - title: "Kafka Streams Documentation"
    url: "https://kafka.apache.org/documentation/streams/"
    accessed: "2025-10-26"
---

## Purpose & When-To-Use

**Purpose:** Design Apache Kafka 3.9 architectures for event streaming, messaging, and stream processing with producer/consumer patterns (idempotent, transactional, exactly-once semantics), Kafka Streams/ksqlDB for stateful processing, Schema Registry (Avro, Protobuf) for schema evolution, performance tuning (batch.size, linger.ms, compression), and KRaft deployment (ZooKeeper deprecated in 3.9, final version with ZooKeeper support).

**When to Use:**
- You need **high-throughput event streaming** (millions of messages/sec, low latency <10ms).
- You require **exactly-once semantics** for financial transactions, order processing, or critical workflows.
- You're implementing **event-driven architecture** (event sourcing, CQRS, saga pattern).
- You need **stream processing** (real-time analytics, windowing, joins, aggregations with Kafka Streams/ksqlDB).
- You're migrating from **RabbitMQ, ActiveMQ, or traditional message queues** to distributed log architecture.
- You need **change data capture (CDC)** from databases (Debezium + Kafka Connect).
- You require **multi-datacenter replication** or disaster recovery (MirrorMaker 2).
- You're deploying **Kafka 3.9 with KRaft** (no ZooKeeper, dynamic quorum membership).

**Complements:**
- `integration-messagequeue-designer`: Covers RabbitMQ, SQS, Service Bus; this focuses on Kafka-specific patterns.
- `data-pipeline-designer`: Uses Kafka as data transport; this designs Kafka topology and tuning.
- `observability-stack-configurator`: Monitors Kafka with Prometheus JMX exporter, Grafana dashboards.

## Pre-Checks

**Mandatory Inputs:**
- `use_case`: At least one use case (event streaming, messaging, CDC, stream processing).
- `throughput`: Expected throughput (messages/sec or MB/sec).

**Validation Steps:**
1. **Compute NOW_ET** using NIST time.gov semantics (America/New_York, ISO-8601) for timestamp anchoring.
2. **Check use_case validity:** Must be one of: event streaming, log aggregation, messaging, CDC, stream processing.
3. **Validate throughput requirements:** Ensure realistic (Kafka can handle millions/sec, but check partition limits).
4. **Assess durability_requirements:** Default to at-least-once if not specified; warn if exactly-once requested (requires idempotent producers + transactions).
5. **Abort if:**
   - Zero use cases provided.
   - Throughput is unrealistic (e.g., billions of messages/sec on single broker).
   - Exactly-once requested without transactional support in clients.

## Procedure

### T1: Quick Kafka Topology Design (≤2k tokens, 80% use case)

**Goal:** Design basic Kafka topology with topic, partition count, replication factor, and producer/consumer configs for standard messaging use case.

**Steps:**
1. **Determine topic count and naming:**
   - Use case: Order events → Topic: `orders` (single topic for simplicity).
   - Naming convention: `<domain>.<entity>.<event-type>` (e.g., `ecommerce.orders.created`).
2. **Calculate partition count:**
   - **Formula:** Partitions = max(throughput_target / throughput_per_partition, consumer_parallelism)
   - **Throughput per partition:** ~10-50 MB/sec (depends on message size, replication).
   - **Example:** 100 MB/sec throughput ÷ 10 MB/sec per partition = 10 partitions.
   - **Rule:** Start with 10-30 partitions; add more if needed (can't decrease partitions later).
3. **Set replication factor:**
   - **Production:** replication.factor = 3 (tolerates 2 broker failures).
   - **Development:** replication.factor = 1 (no redundancy, faster).
   - **Formula:** min.insync.replicas = replication.factor - 1 (e.g., 3 replicas → min.insync.replicas = 2).
4. **Configure producer (basic):**
   ```properties
   acks=all                    # Wait for all replicas (strongest durability)
   retries=Integer.MAX_VALUE   # Retry indefinitely on transient errors
   enable.idempotence=true     # Prevent duplicates (requires acks=all)
   compression.type=lz4        # LZ4 is fastest; snappy, gzip also available
   ```
5. **Configure consumer (basic):**
   ```properties
   group.id=order-processor    # Consumer group for parallel processing
   enable.auto.commit=false    # Manual commit for at-least-once guarantees
   auto.offset.reset=earliest  # Start from beginning if no offset stored
   ```
6. **Set retention policy:**
   - **Time-based:** retention.ms = 604800000 (7 days default).
   - **Size-based:** retention.bytes = -1 (unlimited, relies on time-based).
   - **Compact topics:** cleanup.policy = compact (for state, keeps latest per key).
7. **Output:** Topic config, partition count, replication, basic producer/consumer settings.

**Token Budget:** ≤2k tokens (single topic, basic config).

### T2: Producer/Consumer Patterns with Exactly-Once Semantics (≤6k tokens)

**Goal:** Design Kafka architecture with idempotent producers, transactional writes, exactly-once consumers, and Schema Registry for Avro/Protobuf.

**Steps:**
1. **Implement idempotent producer:**
   - **Config:** `enable.idempotence=true` (requires acks=all, retries > 0, max.in.flight.requests.per.connection ≤ 5).
   - **Guarantees:** No duplicates per partition, in-order delivery, no message loss.
   - **Limitation:** Only within producer session (restart loses sequence number state).
   - **Use case:** Prevents duplicate writes if producer retries.
2. **Implement transactional producer (exactly-once, multi-partition):**
   ```java
   Properties props = new Properties();
   props.put("transactional.id", "order-producer-1");  // Unique per producer instance
   props.put("enable.idempotence", true);
   KafkaProducer<String, Order> producer = new KafkaProducer<>(props);
   producer.initTransactions();

   try {
       producer.beginTransaction();
       producer.send(new ProducerRecord<>("orders", order.getId(), order));
       producer.send(new ProducerRecord<>("inventory", order.getProductId(), inventoryUpdate));
       producer.commitTransaction();
   } catch (Exception e) {
       producer.abortTransaction();
   }
   ```
   - **Guarantees:** Atomic writes across multiple topics/partitions (all-or-nothing).
   - **Use case:** Saga pattern, multi-step workflows, dual writes (Kafka + database via outbox pattern).
3. **Implement exactly-once consumer (read-process-write):**
   ```java
   Properties props = new Properties();
   props.put("isolation.level", "read_committed");  // Only read committed transactions
   props.put("enable.auto.commit", false);          // Manual offset commit
   KafkaConsumer<String, Order> consumer = new KafkaConsumer<>(props);

   // Read-process-write pattern (consume → process → produce)
   KafkaProducer<String, OrderResult> producer = new KafkaProducer<>(producerProps);
   producer.initTransactions();

   while (true) {
       ConsumerRecords<String, Order> records = consumer.poll(Duration.ofMillis(100));
       producer.beginTransaction();
       for (ConsumerRecord<String, Order> record : records) {
           OrderResult result = processOrder(record.value());
           producer.send(new ProducerRecord<>("order-results", result.getId(), result));
       }
       producer.sendOffsetsToTransaction(getOffsets(records), consumer.groupMetadata());
       producer.commitTransaction();  // Atomically commit processed results + consumer offsets
   }
   ```
   - **Guarantees:** Exactly-once end-to-end (consume from topic A, process, produce to topic B, commit offsets).
   - **Performance:** ~2-3× slower than at-least-once (due to transactional overhead).
4. **Idempotent consumer (external state):**
   - **Pattern:** Store processed message IDs in database to detect duplicates.
   - **Implementation:**
     ```sql
     CREATE TABLE processed_messages (
         message_id VARCHAR(255) PRIMARY KEY,
         processed_at TIMESTAMP
     );

     -- Consumer logic:
     if (db.exists("SELECT 1 FROM processed_messages WHERE message_id = ?", record.key())) {
         continue;  // Skip duplicate
     }
     processMessage(record.value());
     db.insert("INSERT INTO processed_messages (message_id, processed_at) VALUES (?, NOW())", record.key());
     consumer.commitSync();  // Commit offset after DB insert
     ```
   - **Use case:** When writing to external systems (databases, APIs) that can't participate in Kafka transactions.
5. **Schema Registry integration (Avro):**
   - **Producer with Avro:**
     ```java
     props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
     props.put("schema.registry.url", "http://schema-registry:8081");

     Schema schema = new Schema.Parser().parse(new File("order.avsc"));
     GenericRecord order = new GenericData.Record(schema);
     order.put("orderId", "123");
     order.put("amount", 99.99);
     producer.send(new ProducerRecord<>("orders", order));
     ```
   - **Consumer with Avro:**
     ```java
     props.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
     props.put("schema.registry.url", "http://schema-registry:8081");

     for (ConsumerRecord<String, GenericRecord> record : records) {
         GenericRecord order = record.value();
         String orderId = order.get("orderId").toString();
         Double amount = (Double) order.get("amount");
     }
     ```
   - **Schema evolution:** Add fields with defaults (backward compatible), remove optional fields (forward compatible).
6. **Protobuf vs Avro comparison:**
   - **Avro:** Better for Kafka ecosystem (first-class Schema Registry support), faster deserialization, schema evolution via reader/writer schema.
   - **Protobuf:** Better for polyglot systems (Google standard), backward/forward compatible by design, supports gRPC.
   - **Recommendation:** Use Avro for Kafka-centric systems, Protobuf for gRPC + Kafka hybrid.
7. **Performance tuning (producer):**
   ```properties
   batch.size=16384            # Default 16KB; increase to 32KB-64KB for higher throughput
   linger.ms=10                # Wait 10ms to batch messages (trade latency for throughput)
   compression.type=lz4        # LZ4 fastest; snappy good balance; gzip highest compression
   buffer.memory=33554432      # 32MB buffer; increase if many partitions
   max.in.flight.requests.per.connection=5  # Max for idempotent producer
   ```
   - **Batch size:** Larger batches = higher throughput, higher latency (wait for batch to fill).
   - **Linger:** Wait linger.ms before sending batch (allows more messages to accumulate).
   - **Compression:** LZ4 fastest (2-3× compression), gzip highest (5-7× compression, slower).
8. **Performance tuning (consumer):**
   ```properties
   fetch.min.bytes=1           # Minimum data to fetch (increase to 10KB-50KB for higher throughput)
   fetch.max.wait.ms=500       # Max wait for fetch.min.bytes (trade latency for throughput)
   max.partition.fetch.bytes=1048576  # 1MB per partition per fetch
   max.poll.records=500        # Records per poll() call
   ```
   - **Fetch.min.bytes:** Larger values = fewer fetch requests, higher throughput, higher latency.
   - **Max.poll.records:** Tune based on processing time (too high → consumer timeout, too low → underutilization).
9. **Output:**
   - Producer config with idempotence, transactions, batching, compression.
   - Consumer config with exactly-once, manual commit, tuned fetch settings.
   - Schema Registry setup with Avro schema example.
   - Performance tuning recommendations (batch.size, linger.ms, fetch.min.bytes).

**Token Budget:** ≤6k tokens (exactly-once patterns, Schema Registry, performance tuning).

### T3: Kafka Streams, ksqlDB, and Enterprise Architecture (≤12k tokens)

**Goal:** Design stream processing application with Kafka Streams or ksqlDB, multi-DC replication, monitoring, and event-driven patterns (event sourcing, CQRS, saga).

**Steps:**
1. **Kafka Streams stateful processing:**
   ```java
   StreamsBuilder builder = new StreamsBuilder();
   KStream<String, Order> orders = builder.stream("orders");

   // Stateless: filter, map
   KStream<String, Order> largeOrders = orders.filter((key, order) -> order.getAmount() > 100);

   // Stateful: aggregation with windowing
   KTable<Windowed<String>, Long> orderCounts = orders
       .groupByKey()
       .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
       .count();

   // Join streams
   KStream<String, OrderResult> enrichedOrders = orders.join(
       users,  // KTable<String, User>
       (order, user) -> new OrderResult(order, user),
       Joined.with(Serdes.String(), orderSerde, userSerde)
   );
   ```
   - **Stateless ops:** filter, map, flatMap (no state store).
   - **Stateful ops:** aggregate, reduce, join (backed by RocksDB state store).
   - **Windowing:** Tumbling (fixed non-overlapping), Hopping (overlapping), Session (activity-based).
2. **ksqlDB for SQL-based stream processing:**
   ```sql
   -- Create stream from topic
   CREATE STREAM orders (orderId VARCHAR, userId VARCHAR, amount DOUBLE)
       WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='AVRO');

   -- Continuous query: filter and transform
   CREATE STREAM large_orders AS
       SELECT orderId, userId, amount
       FROM orders
       WHERE amount > 100
       EMIT CHANGES;

   -- Aggregation with windowing
   CREATE TABLE order_counts AS
       SELECT userId, COUNT(*) as order_count
       FROM orders
       WINDOW TUMBLING (SIZE 5 MINUTES)
       GROUP BY userId
       EMIT CHANGES;

   -- Stream-table join
   CREATE STREAM enriched_orders AS
       SELECT o.orderId, o.amount, u.userName, u.email
       FROM orders o
       LEFT JOIN users u ON o.userId = u.userId
       EMIT CHANGES;
   ```
   - **Advantages:** SQL interface, no Java code, auto-scaling with ksqlDB cluster.
   - **Limitations:** Less flexible than Kafka Streams (can't use custom Serdes, external lookups limited).
3. **Schema Registry with ksqlDB:**
   ```sql
   -- ksqlDB auto-retrieves schema from Schema Registry
   CREATE STREAM orders WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='AVRO');
   -- No need to define columns; inferred from Avro schema
   ```
4. **Event sourcing pattern:**
   - **Concept:** Store all state changes as events (immutable log), rebuild state by replaying events.
   - **Kafka implementation:**
     - Event topic: `account-events` (append-only, no deletion).
     - Events: AccountCreated, MoneyDeposited, MoneyWithdrawn.
     - State rebuild: Consume events, apply to in-memory state or database.
   - **Benefits:** Audit trail, time travel (replay to any point), event replay for new projections.
5. **CQRS (Command Query Responsibility Segregation):**
   - **Command side:** Write events to Kafka (AccountCreated, MoneyDeposited).
   - **Query side:** Consume events, build read-optimized views (materialized views, Elasticsearch, Redis).
   - **Kafka implementation:**
     - Commands → Kafka topic → Event handler → Events → Kafka topic.
     - Query service consumes events, updates read database (PostgreSQL, MongoDB, Elasticsearch).
6. **Saga pattern (distributed transactions):**
   - **Orchestration saga:**
     - Central orchestrator sends commands, listens for events.
     - Example: Order saga → CreateOrder → ReserveInventory → ChargePayment → ShipOrder.
     - Rollback: If ChargePayment fails → ReleaseInventory, CancelOrder.
   - **Choreography saga:**
     - Each service listens for events, publishes new events.
     - Example: OrderCreated event → Inventory service reserves → InventoryReserved event → Payment service charges.
   - **Kafka implementation:** Events published to Kafka topics, each service subscribes and publishes.
7. **Outbox pattern (dual write problem):**
   - **Problem:** Writing to database + Kafka not atomic (can write to DB but fail to send to Kafka).
   - **Solution:** Write to database + outbox table in same transaction, CDC connector reads outbox, publishes to Kafka.
   - **Implementation:**
     ```sql
     BEGIN TRANSACTION;
     INSERT INTO orders (order_id, amount) VALUES ('123', 99.99);
     INSERT INTO outbox (event_type, payload) VALUES ('OrderCreated', '{"orderId":"123","amount":99.99}');
     COMMIT;

     -- Debezium CDC connector reads outbox, publishes to Kafka, deletes outbox row
     ```
8. **Multi-datacenter replication (MirrorMaker 2):**
   - **Active-passive:** Primary DC writes, secondary DC replicates (disaster recovery).
   - **Active-active:** Both DCs write, bidirectional replication (conflict resolution needed).
   - **MirrorMaker 2 config:**
     ```properties
     clusters = primary, secondary
     primary.bootstrap.servers = primary-kafka:9092
     secondary.bootstrap.servers = secondary-kafka:9092
     primary->secondary.enabled = true
     primary->secondary.topics = orders.*, users.*
     replication.factor = 3
     ```
   - **Conflict resolution:** Last-write-wins (timestamp), application-level merge.
9. **Monitoring and observability:**
   - **JMX metrics:** Expose via Prometheus JMX exporter.
   - **Key metrics:**
     - **Producer:** record-send-rate, batch-size-avg, compression-rate-avg, request-latency-avg.
     - **Consumer:** records-consumed-rate, records-lag-max, fetch-latency-avg.
     - **Broker:** under-replicated-partitions (should be 0), offline-partitions (should be 0).
   - **Consumer lag monitoring:**
     ```bash
     kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group order-processor
     # Check LAG column; lag > 1000 = consumer falling behind
     ```
   - **Alerts:**
     - Under-replicated partitions > 0 (replication issue).
     - Consumer lag > threshold (slow consumer).
     - Disk usage > 80% (retention policy too long).
10. **KRaft deployment (Kafka 3.9, no ZooKeeper):**
    - **KRaft mode:** Kafka stores metadata in internal __cluster_metadata topic (no external ZooKeeper).
    - **Dynamic quorum membership (KIP-853):** Add/remove controller nodes without restart.
    - **Config:**
      ```properties
      process.roles=broker,controller  # Combined mode (or separate broker/controller nodes)
      node.id=1
      controller.quorum.voters=1@kafka1:9093,2@kafka2:9093,3@kafka3:9093
      ```
    - **Migration from ZooKeeper:** Kafka 3.9 is final version supporting ZooKeeper; migrate to KRaft before Kafka 4.0.
11. **Security:**
    - **SASL/SCRAM:** Username/password authentication.
    - **mTLS:** Client certificate authentication.
    - **ACLs:** Topic-level permissions (read, write, create).
    - **Encryption:** TLS in transit, encryption at rest (broker disk encryption).
12. **Output:**
    - Kafka Streams application code (stateful processing, windowing, joins).
    - ksqlDB queries (streams, tables, aggregations, joins).
    - Event-driven pattern implementations (event sourcing, CQRS, saga, outbox).
    - MirrorMaker 2 config for multi-DC replication.
    - Monitoring setup (JMX metrics, Prometheus, Grafana dashboards, lag alerts).
    - KRaft deployment guide (Kafka 3.9 without ZooKeeper).

**Token Budget:** ≤12k tokens (Streams, ksqlDB, event patterns, monitoring, KRaft).

## Decision Rules

**Ambiguity Resolution:**
1. **If `durability_requirements` not specified:**
   - Default to **at-least-once** (acks=all, enable.auto.commit=false).
   - Emit note: "Using at-least-once. For exactly-once, enable transactions and idempotent producer."
2. **If partition count not specified:**
   - Default to **10 partitions** (balances parallelism and overhead).
   - Emit note: "Using 10 partitions. Adjust based on throughput and consumer count."
3. **If replication factor not specified:**
   - Default to **3** for production, **1** for dev/test.
   - Emit note: "Using replication.factor=3 (production). Set min.insync.replicas=2."
4. **If Schema Registry format not specified:**
   - Default to **Avro** (best Kafka ecosystem support).
   - Emit note: "Using Avro. Consider Protobuf for gRPC + Kafka hybrid systems."
5. **If compression not specified:**
   - Default to **lz4** (fastest, good compression ratio).
   - Emit note: "Using lz4 compression. Use gzip for higher compression (slower)."

**Stop Conditions:**
- **Unrealistic throughput:** User requests billions of messages/sec → abort with error: "Throughput too high. Kafka handles millions/sec; consider partitioning across multiple clusters."
- **Exactly-once without transactions:** User requests exactly-once but client doesn't support transactions → emit error: "Exactly-once requires transactional producer (transactional.id) and read_committed consumer."
- **ZooKeeper on Kafka 4.0+:** User requests ZooKeeper on Kafka 4.0 → abort: "ZooKeeper removed in Kafka 4.0. Use KRaft mode (process.roles=broker,controller)."

**Thresholds:**
- **Partition count:** 1-2000 per broker (Kafka 3.9 handles thousands, but >2000 degrades performance).
- **Replication factor:** 2-5 (3 is standard; 5 for critical data).
- **Batch size:** 16KB (default) to 1MB (high throughput).
- **Linger.ms:** 0ms (low latency) to 100ms (high throughput).
- **Consumer lag:** Acceptable lag varies; alert if lag > 1000 and growing.

## Output Contract

**Required Fields:**

```typescript
{
  kafka_topology: {
    topics: Array<{
      name: string;              // orders, users, payments
      partitions: number;        // 10, 30, 100
      replication_factor: number; // 3 (production), 1 (dev)
      retention_ms: number;      // 604800000 (7 days)
      cleanup_policy: "delete" | "compact" | "compact,delete";
      min_insync_replicas: number; // replication_factor - 1
    }>;
    kafka_version: string;       // 3.9.1
    deployment_mode: "kraft" | "zookeeper";
  };
  producer_config: {
    acks: "all" | "1" | "0";
    retries: number;
    enable_idempotence: boolean;
    transactional_id?: string;   // For exactly-once multi-partition
    compression_type: "none" | "gzip" | "snappy" | "lz4" | "zstd";
    batch_size: number;          // bytes
    linger_ms: number;           // milliseconds
    buffer_memory: number;       // bytes
    max_in_flight_requests: number; // ≤5 for idempotent
  };
  consumer_config: {
    group_id: string;
    enable_auto_commit: boolean;
    auto_offset_reset: "earliest" | "latest" | "none";
    isolation_level: "read_uncommitted" | "read_committed";
    fetch_min_bytes: number;
    fetch_max_wait_ms: number;
    max_poll_records: number;
  };
  schema_registry_config?: {
    url: string;
    schemas: Array<{
      subject: string;           // orders-value, users-value
      format: "avro" | "protobuf" | "json";
      schema: string;            // Avro JSON or Protobuf definition
      evolution: "backward" | "forward" | "full" | "none";
    }>;
  };
  performance_tuning: {
    producer_throughput_mbps: number;
    consumer_throughput_mbps: number;
    latency_p99_ms: number;
    recommendations: Array<string>;
  };
  monitoring_setup: {
    jmx_metrics: Array<string>;  // kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec
    lag_alert_threshold: number; // 1000
    dashboards: Array<{
      name: string;              // Kafka Overview, Consumer Lag
      metrics: string[];
    }>;
  };
}
```

**Optional Fields:**
- `kafka_streams_app`: Kafka Streams application code (Java/Scala).
- `ksqldb_queries`: ksqlDB CREATE STREAM/TABLE statements.
- `event_driven_patterns`: Event sourcing, CQRS, saga implementations.
- `mirrormaker2_config`: Multi-DC replication setup.
- `security_config`: SASL, TLS, ACLs configuration.

**Format:** YAML or JSON for configs, Java/SQL for application code.

## Examples

### Example 1: E-commerce Order Processing with Exactly-Once (T2)

**Input:**
```yaml
use_case: "event streaming + messaging"
throughput: {messages_per_sec: 10000, peak_mbps: 50}
durability_requirements: "exactly-once"
data_schema: {format: "avro"}
```

**Output (T2 Summary):**
```yaml
Kafka Topology:
  Topics:
    - orders: 30 partitions, replication=3, retention=7d, min.insync.replicas=2
    - inventory: 30 partitions, replication=3, retention=7d
  Kafka Version: 3.9.1 (KRaft mode, no ZooKeeper)
Producer Config (Exactly-Once):
  enable.idempotence=true, transactional.id=order-producer-1, acks=all
  compression.type=lz4, batch.size=32KB, linger.ms=10ms
Consumer Config (Exactly-Once):
  group.id=order-processor, isolation.level=read_committed
  enable.auto.commit=false (manual commit in transaction)
Schema Registry:
  Format: Avro, Subject: orders-value
  Evolution: Backward compatible (add fields with defaults)
Performance:
  Producer: 50 MB/sec, Latency p99: 15ms
  Consumer: 50 MB/sec, Lag: <100 messages
Pattern: Read-process-write (consume orders → update inventory → produce confirmation)
```

**Link to Full Example:** See `skills/messaging-kafka-architect/examples/ecommerce-exactly-once.txt`

## Quality Gates

**Token Budget Compliance:**
- T1 output ≤2k tokens (basic topology, partition/replication).
- T2 output ≤6k tokens (exactly-once, Schema Registry, performance tuning).
- T3 output ≤12k tokens (Kafka Streams, ksqlDB, event patterns, monitoring).

**Validation Checklist:**
- [ ] Partition count supports throughput (throughput_target / throughput_per_partition).
- [ ] Replication factor ≥3 for production.
- [ ] min.insync.replicas = replication.factor - 1.
- [ ] Idempotent producer enabled for durability (enable.idempotence=true).
- [ ] Transactions configured if exactly-once required (transactional.id set).
- [ ] Compression enabled (lz4, snappy, gzip, or zstd).
- [ ] Consumer group.id unique per application.
- [ ] Schema Registry configured if Avro/Protobuf used.
- [ ] Monitoring includes consumer lag, under-replicated partitions, disk usage.
- [ ] KRaft mode for Kafka 3.9+ (no ZooKeeper).

**Safety & Auditability:**
- **No secrets in configs:** Use environment variables or secrets manager for SASL credentials.
- **Audit logging:** Enable broker audit logs for sensitive topics (PII, financial data).
- **Encryption:** TLS in transit, encryption at rest for compliance (GDPR, PCI-DSS).

**Determinism:**
- **Partition assignment:** Consistent partitioning by key (same key → same partition).
- **Offset commits:** Manual commits ensure deterministic processing (no auto-commit race conditions).

## Resources

**Official Documentation:**
- [Apache Kafka 3.9 Release Notes](https://www.confluent.io/blog/introducing-apache-kafka-3-9/) (accessed 2025-10-26)
  - KRaft dynamic quorums, tiered storage, final ZooKeeper support.
- [Kafka Exactly-Once Semantics](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/) (accessed 2025-10-26)
  - Idempotent producer, transactional producer, read-process-write pattern.
- [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html) (accessed 2025-10-26)
  - Avro, Protobuf, JSON Schema support and evolution.

**Performance Tuning:**
- [Kafka Performance Tuning](https://docs.confluent.io/cloud/current/client-apps/optimizing/throughput.html) (accessed 2025-10-26)
  - batch.size, linger.ms, compression, fetch.min.bytes tuning.

**Stream Processing:**
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)
  - Stateful processing, windowing, joins, state stores.
- [ksqlDB Documentation](https://docs.confluent.io/platform/current/ksqldb/)
  - SQL-based stream processing, auto-scaling.

**Complementary Skills:**
- `integration-messagequeue-designer`: Covers RabbitMQ, SQS, Service Bus patterns.
- `data-pipeline-designer`: Uses Kafka for data transport in ETL/ELT pipelines.
- `observability-stack-configurator`: Monitors Kafka with Prometheus JMX exporter.
