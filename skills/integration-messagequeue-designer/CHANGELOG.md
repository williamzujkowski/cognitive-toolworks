# Changelog

All notable changes to the Message Queue Pattern Designer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- Initial release of Message Queue Pattern Designer skill
- Support for 5 queue systems: Kafka, RabbitMQ, SQS, Azure Service Bus, Google Pub/Sub
- 4 messaging patterns: publish-subscribe, work-queue, request-reply, saga
- 3 delivery guarantees: at-least-once, at-most-once, exactly-once
- Tier 1 (≤2k tokens): Basic queue/topic configuration
- Tier 2 (≤6k tokens): DLQ, idempotency, ordering, retry strategies
- Tier 3 (≤12k tokens): Backpressure, consumer scaling, monitoring, DR
- Example: Kafka order processing with exactly-once semantics (≤30 lines)
- 5 evaluation scenarios covering common patterns
- Sources from official docs (Kafka, RabbitMQ, AWS, Azure, Google) with access dates
- Enterprise Integration Patterns citations
