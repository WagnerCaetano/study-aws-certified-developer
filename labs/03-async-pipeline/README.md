# Lab 03: Async Pipeline

S3 object-created event → Lambda processor → DynamoDB on LocalStack.

## Architecture

```mermaid
flowchart LR
  Upload[Client PutObject] --> S3[(S3 bucket)]
  S3 -->|s3:ObjectCreated| Lambda
  Lambda -->|GetObject + PutItem| DDB[(Records table)]
```

## Learning goals

- Parse S3 event notification records (`bucket`, `key`)
- Read object bytes from S3 and transform lines into DynamoDB items
- Write with `pk` / `sk` keys suitable for access patterns
- Return a successful Lambda response summarizing processed keys

## Problem

Edit `starter.py`:

1. **`ensure_resources(s3, dynamodb, bucket, table_name)`** — create bucket (if missing) and DynamoDB table with keys `pk` (HASH) + `sk` (RANGE).
2. **`transform_line(line: str) -> dict`** — CSV `id,category,value` → `{ "pk": "RECORD#{id}", "sk": "DATA#{category}", "value": value, "status": "processed" }`.
3. **`pipeline_handler(event, context, *, s3=None, dynamodb=None, table_name=...)`** — for each S3 record: get object, split lines, transform, put items; return `{ "statusCode": 200, "body": {"processed": N, "keys": [...] } }` where body may be a dict or JSON string.

## Exam tips

- S3 → Lambda can overwhelm concurrency; production often uses **S3 → SQS → Lambda** for backpressure.
- Make processors **idempotent** (same object re-delivered → same DynamoDB keys / overwrite).
- DynamoDB `BatchWriteItem` max is **25** items — batch large files.

## Prerequisites

```bash
docker compose up -d
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
```

## Run

```bash
python runner.py labs/03-async-pipeline
python runner.py labs/03-async-pipeline --solution
```

Offline concept check: [exercises/33-data-pipeline](../exercises/33-data-pipeline/).
