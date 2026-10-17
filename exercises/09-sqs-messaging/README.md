# Exercise 09: SQS Messaging

## Learning goals

- Send / receive / delete messages on a live SQS queue (LocalStack)
- JSON-serialize bodies; add FIFO `MessageGroupId` + `MessageDeduplicationId`
- Configure a DLQ with a JSON-string `RedrivePolicy`
- Parse Lambda SQS event records

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `sqs`

**Cleanup:** tests create and delete temporary queues (including DLQ pairs). Stop LocalStack with `docker compose down`.

## Problem

Fix the helpers in `starter.py`:

1. **send_json_message** — `json.dumps` for dicts; FIFO fields when `group_id` is set
2. **receive_messages** — parse JSON bodies when possible
3. **delete_message** — use `ReceiptHandle` (not `ReceiptHandleId`)
4. **build_dlq_redrive_policy** — return a **JSON string** with string `maxReceiveCount`
5. **process_sqs_event** — `json.loads` each record body

## Exam tip

After receive, the message is invisible for the **visibility timeout**; if you do not delete it, it reappears until **maxReceiveCount** sends it to the DLQ.

## Run

```bash
docker compose up -d
python runner.py exercises/09-sqs-messaging
python runner.py exercises/09-sqs-messaging --solution
```
