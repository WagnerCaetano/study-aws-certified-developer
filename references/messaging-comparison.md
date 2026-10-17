# Messaging Comparison: SQS, SNS & EventBridge

When to pick which service on DVA-C02.

## At a glance

| | **SQS** | **SNS** | **EventBridge** |
|---|---------|---------|-----------------|
| Model | Queue (pull) | Pub/sub (push) | Event bus (push) |
| Delivery | Consumers poll | Push to subscribers | Push to targets |
| Fan-out | One queue → N workers (competing) | One message → many subscribers | One event → many rules/targets |
| Filtering | Limited (message attributes + filter on poll side) | Subscription filter policies | Rich event patterns |
| Ordering | FIFO queues (optional) | FIFO topics (optional) | Archive/replay; not FIFO like SQS |
| Replay | No (unless you store) | No | Event archive + replay |
| Schema | App-defined body | App-defined | Optional Schema Registry |
| Typical target | Lambda, ECS, EC2, pollers | Lambda, SQS, HTTP, email, SMS | Lambda, SQS, SNS, Step Functions, API Destinations |

## SQS essentials

| Topic | Key point |
|-------|-----------|
| Standard vs FIFO | Standard: at-least-once, best-effort order; FIFO: exactly-once + order per message group |
| Visibility timeout | Hide in-flight message while processing |
| Long polling | `WaitTimeSeconds` up to 20 s — prefer over short poll |
| DLQ | After `maxReceiveCount`, send to dead-letter queue |
| Delete | Must `DeleteMessage` with receipt handle after success |
| Delay / timer | Delay queues / per-message delay (standard) |

## SNS essentials

| Topic | Key point |
|-------|-----------|
| Topic → subscriptions | Fan-out to SQS, Lambda, HTTP(S), email, SMS, mobile |
| Filter policies | Attribute-based (and payload policies where supported) |
| SNS → SQS | Classic durable fan-out pattern |
| FIFO | Ordered, dedup; subscribers must support FIFO (e.g. SQS FIFO) |

## EventBridge essentials

| Topic | Key point |
|-------|-----------|
| Default bus | AWS service events |
| Custom bus | Your application events |
| Partner bus | SaaS integrations |
| Rules | Event pattern and/or schedule (`cron` / `rate`) |
| Targets | Many AWS services; input transformers |
| Archive / replay | Replay past events to rules |

## Choose one

| Need | Prefer |
|------|--------|
| Buffer work; competing consumers; backpressure | **SQS** |
| Notify many systems of the same message | **SNS** |
| Route on content; SaaS/AWS events; schedules; replay | **EventBridge** |
| Fan-out + durable processing | **SNS → SQS → workers** |
| Decouple microservices with schema/filter | **EventBridge** (or SNS filters) |

## Exam tips

- Lambda + SQS: event source mapping; partial batch failure reporting.
- Visibility timeout ≥ function timeout (with margin).
- EventBridge schedules replace many CloudWatch Events questions (same family).
- SQS is **pull**; SNS/EventBridge are **push**.

## Related

- Chapter: [dev-06-sqs-sns.md](../chapters/dev-06-sqs-sns.md)
- Exercises: [09-sqs-messaging](../exercises/09-sqs-messaging/), [10-sns-pubsub](../exercises/10-sns-pubsub/), [32-event-driven](../exercises/32-event-driven/)
- Lab (when available): [labs/02-event-driven](../labs/02-event-driven/)
