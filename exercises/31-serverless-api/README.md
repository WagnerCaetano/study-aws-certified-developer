# Exercise 31: Serverless API

## Learning goals

- Route API Gateway proxy events by HTTP method and path parameters
- Return correct status codes (200, 201, 400, 204, 404) for CRUD-style handlers
- Validate JSON request bodies on POST
- Build CORS-enabled proxy responses for browser clients

## Problem

Fix `build_api_handler` and `build_cors_response` in `starter.py`.

The API handler should:

- **GET** `/items` → 200 with an empty `items` list
- **GET** `/items/{id}` → 200 with the id in the body
- **POST** → 201 when `name` is present; **400** when missing
- **DELETE** `/items/{id}` → **204** with an empty body

`build_cors_response` must include `Access-Control-Allow-Origin: *` and allow common methods.

## Exam tip

For Lambda proxy integration, API Gateway passes `httpMethod`, `pathParameters`, and a string `body`. CORS requires OPTIONS on the API and appropriate response headers on actual methods.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/31-serverless-api
python runner.py exercises/31-serverless-api --solution
```

## Next: multi-service lab

This exercise is an **offline concept check**. For the LocalStack hands-on (API proxy handler + real DynamoDB CRUD), continue with:

**[labs/01-serverless-api](../../labs/01-serverless-api/)**
