# Exercise 01: Lambda Basics

## Learning goals

- Parse JSON request bodies from API Gateway proxy integration events
- Return Lambda proxy responses with `statusCode`, `headers`, and stringified `body`
- Validate input and return appropriate HTTP status codes (200 vs 400)

## Problem

Fix the Lambda handler in `starter.py` so it correctly processes API Gateway events.

The function should:

1. Parse the JSON body from the event (`event['body']`)
2. Extract the `name` field from that body
3. Return status code 200 with a greeting when `name` is present
4. Return status code 400 when `name` is missing or the body is empty
5. Include `Content-Type: application/json` in response headers

## Exam tip

On the DVA-C02 exam, remember that API Gateway **Lambda proxy integration** passes the full request in a single event object and expects your handler to return a dict with `statusCode`, `headers`, and `body` (body must be a string, often JSON).

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/01-lambda-basics
python runner.py exercises/01-lambda-basics --solution
```
