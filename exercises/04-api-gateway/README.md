# Exercise 04: API Gateway Configuration

## Learning goals

- Route HTTP methods/paths in a Lambda **proxy** handler (status codes, JSON body, CORS)
- Create a REST API resource + MOCK GET on LocalStack (stable subset of API Gateway)

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `apigateway`

**Cleanup:** the LocalStack test deletes the temporary REST API. Use `docker compose down` to stop LocalStack.

> **Hybrid design:** routing/CORS are unit-tested (exam-critical). Live LocalStack coverage uses a **MOCK** integration — more reliable than Lambda proxy deploy on LocalStack Community — while still practicing `create_rest_api`, resources, methods, and integrations.

## Problem

Fix `starter.py`:

1. **build_api_response** — include CORS headers (`Access-Control-Allow-Origin: *`, …)
2. **handler** — OPTIONS → 200 with CORS; POST parses JSON body and returns **201**
3. **create_rest_api** — return the API `id` string
4. **put_mock_get_method** — create `/{path_part}`, `put_method` GET, MOCK `put_integration` (+ responses)

## Exam tip

Browsers need CORS on real responses **and** OPTIONS preflight. Missing `Access-Control-Allow-Origin` is a common “works in curl, fails in browser” trap.

## Run

```bash
docker compose up -d
python runner.py exercises/04-api-gateway
python runner.py exercises/04-api-gateway --solution
```
