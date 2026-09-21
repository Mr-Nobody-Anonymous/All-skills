# ADR: Use Kafka (Anti-Pattern Example)

> [!WARNING]
> This is an example of a **flawed ADR**. Do not follow this pattern. It illustrates the common pitfalls: missing context, lack of concrete alternatives, no quantified trade-offs, and vague decision criteria.

## Status
Approved

## Context
We need something fast and scalable for sending messages between services. Kafka is very popular and Netflix uses it.

## Decision
We decided to rewrite all internal services to send events through Apache Kafka.

## Consequences
- **Pros**: It is super fast and web scale.
- **Cons**: None identified.

---

### Critique & Anti-Pattern Analysis
1. **Missing Problem Statement**: Does not articulate throughput numbers, latency targets, or delivery semantics (at-least-once vs exactly-once).
2. **Cargo Culting**: Cites "Netflix uses it" instead of specific engineering constraints.
3. **No Viable Alternatives Evaluated**: Did not compare against RabbitMQ, AWS SQS/SNS, Redis Streams, or internal Go channels.
4. **Dishonest Trade-offs**: Stating "None identified" ignores massive operational complexity, ZooKeeper/KRaft cluster management, partition rebalancing, and message retention sizing.
