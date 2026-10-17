# Exercise 05: DynamoDB Operations

## Learning goals

- Perform real `put_item` / `get_item` / `query` / `update_item` / `delete_item` against DynamoDB
- Use `ConditionExpression` for conditional writes and deletes
- Build `UpdateExpression` with `ExpressionAttributeNames` / `ExpressionAttributeValues`

## LocalStack

**Prerequisite:** from the repo root, start LocalStack:

```bash
docker compose up -d
```

See [setup.md](../../setup.md) for env vars (`AWS_ENDPOINT_URL`, dummy credentials).

**Services used:** `dynamodb`

**Cleanup:** each test creates a temporary table and deletes it. Stop LocalStack with `docker compose down` when finished.

## Problem

Implement the helpers in `starter.py` so they work against a boto3 DynamoDB **Table** resource (LocalStack).

1. **put_item** — `ConditionExpression` `attribute_not_exists(pk)`
2. **get_item** — return `Item` (or `None`), not the raw response
3. **query_by_pk** — use `boto3.dynamodb.conditions.Key(...).eq(...)`
4. **update_item** — `SET` with name/value placeholders for every attribute
5. **delete_item** — `ConditionExpression` `attribute_exists(pk)`

## Exam tip

DynamoDB **Query** requires a partition key in `KeyConditionExpression`; you cannot query on arbitrary attributes without a GSI.

## Run

```bash
docker compose up -d
python runner.py exercises/05-dynamodb-ops
python runner.py exercises/05-dynamodb-ops --solution
```
