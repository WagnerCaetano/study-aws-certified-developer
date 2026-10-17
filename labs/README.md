# Multi-service LocalStack labs

End-to-end scenarios that combine several AWS services. Use these after the related single-service exercises.

Each lab folder has:

| File | Role |
|------|------|
| `starter.py` | Incomplete — **you edit this** |
| `solution.py` | Reference answer key |
| `test.py` | LocalStack-backed tests |
| `README.md` | Architecture, goals, exam tips |

## Prerequisites

1. Follow **[setup.md](../setup.md)** (Python deps + env vars).
2. Start LocalStack:

```bash
docker compose up -d
curl http://localhost:4566/_localstack/health
```

## Labs

| Lab | Pattern | Maps from |
|-----|---------|-----------|
| [01-serverless-api](01-serverless-api/) | API Gateway proxy + Lambda + DynamoDB CRUD | [exercises/31](../exercises/31-serverless-api/) |
| [02-event-driven](02-event-driven/) | SNS → SQS fan-out + filter policies | [exercises/32](../exercises/32-event-driven/) |
| [03-async-pipeline](03-async-pipeline/) | S3 event → Lambda → DynamoDB | [exercises/33](../exercises/33-data-pipeline/) |
| [04-secure-config](04-secure-config/) | Secrets Manager + SSM + KMS | [exercises/19](../exercises/19-secrets/) / [34](../exercises/34-multi-auth/) |

## Run

```bash
# From repo root
python runner.py labs/01-serverless-api
python runner.py labs/02-event-driven
python runner.py labs/03-async-pipeline
python runner.py labs/04-secure-config

# Validate answer keys
python runner.py labs/01-serverless-api --solution

# List everything (exercises + labs)
python runner.py --list
```

Exercises **31–34** remain lighter offline concept checks; do the matching lab here for the hands-on multi-service version.
