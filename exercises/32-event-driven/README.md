# Exercise 32: Event-Driven Architecture

## Learning goals

- Model SNS → SQS **fan-out** subscriptions
- Build SNS message **filter policies** (attribute names → list of allowed values)
- Structure domain **event payloads** with type, source, data, and timestamp
- Route events to handlers with a **default** fallback

## Problem

Fix the event-driven helpers in `starter.py`.

1. **`build_fanout_config`**: SQS queue subscriptions use protocol **`sqs`**.
2. **`build_sns_filter_policy`**: Each filter value must be a **list** in the JSON policy.
3. **`build_event_payload`**: Include the `data` dict on the payload.
4. **`route_event`**: Unknown event types should use the **`default`** handler when present.

## Exam tip

SNS filter policies reduce Lambda/SQS invocations by matching message attributes at publish time. Fan-out to multiple SQS queues requires queue policies allowing SNS to send messages.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/32-event-driven
python runner.py exercises/32-event-driven --solution
```

## Next: multi-service lab

This exercise is an **offline concept check**. For the LocalStack hands-on (SNS → SQS fan-out + filter policies), continue with:

**[labs/02-event-driven](../../labs/02-event-driven/)**
