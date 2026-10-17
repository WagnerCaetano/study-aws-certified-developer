# Lambda Limits Quick Sheet

Exam-critical defaults and soft/hard limits for AWS Lambda (DVA-C02). Values can change; treat as study anchors, not a live quota source.

## Execution limits

| Limit | Default / max |
|-------|----------------|
| Timeout | 3 s default; **15 min** max |
| Memory | 128 MB–**10,240 MB** (CPU scales with memory) |
| Ephemeral storage (`/tmp`) | 512 MB–**10,240 MB** |
| Concurrent executions (account) | **1,000** (soft; request increase) |
| Burst concurrency (new) | Region-dependent (often 500–3,000) |
| Payload (sync request/response) | **6 MB** |
| Payload (async invoke) | **256 KB** |
| Environment variables | **4 KB** total |
| Layers (unzipped) | **250 MB** deployment package + layers |
| Deployment package (zip, direct) | **50 MB** zipped / **250 MB** unzipped |
| Deployment package (via S3) | Same unzipped limit |
| Container image | **10 GB** |

## Invocation & scaling

| Topic | Key point |
|-------|-----------|
| Sync vs async | Sync waits for result; async queues then retries on failure |
| Event source mapping | Pull model (SQS, Kinesis, DynamoDB Streams) |
| Reserved concurrency | Caps a function; also guarantees capacity |
| Provisioned concurrency | Keeps warm environments; reduces cold starts |
| Throttling | `429` / `TooManyRequestsException` when concurrency exhausted |

## VPC & networking

| Topic | Key point |
|-------|-----------|
| VPC attach | ENIs in subnets; longer cold start; no public internet without NAT or VPC endpoints |
| Hyperplane ENIs | Shared ENIs; still need correct SGs + routes |

## Exam tips

- Increasing **memory** also increases **CPU** (and often reduces duration cost).
- Prefer **reuse** of clients outside the handler; avoid heavy init on every invoke.
- Know **DLQ / on-failure destinations** for async failures (SQS, SNS, Lambda, EventBridge).
- `/tmp` is per execution environment — not a durable store across cold starts.

## Related

- Chapter: [dev-02-lambda.md](../chapters/dev-02-lambda.md)
- Exercises: [01-lambda-basics](../exercises/01-lambda-basics/), [02-lambda-advanced](../exercises/02-lambda-advanced/), [03-lambda-performance](../exercises/03-lambda-performance/)
