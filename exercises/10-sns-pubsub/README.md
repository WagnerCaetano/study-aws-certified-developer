# Exercise 10: SNS Pub/Sub

## Learning goals

- Create topics and publish JSON messages with message attributes
- Subscribe an SQS queue (`Protocol: sqs`) and set a subscription filter policy
- Parse SNS notification records inside a Lambda event

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `sns`, `sqs`

**Cleanup:** tests delete temporary topics and queues. Use `docker compose down` when done.

## Problem

Fix the helpers in `starter.py`:

1. **create_topic** — return the topic ARN string
2. **publish_json** — JSON-serialize dicts; use `MessageAttributes` (plural)
3. **subscribe_queue** — `Protocol: sqs` with the queue ARN as endpoint
4. **set_filter_policy** — attribute name `FilterPolicy`
5. **parse_sns_event** — read `record['Sns']` (capital S, lowercase ns)

## Exam tip

SNS → SQS needs a queue policy allowing `sns.amazonaws.com` to `sqs:SendMessage`. Filter policies match message **attributes**, not the body.

## Run

```bash
docker compose up -d
python runner.py exercises/10-sns-pubsub
python runner.py exercises/10-sns-pubsub --solution
```
