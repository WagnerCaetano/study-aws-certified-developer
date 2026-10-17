# Exercise 02: Lambda Advanced

## Learning goals

- Read configuration from Lambda environment variables (`TABLE_NAME`, `STAGE`)
- Branch handler logic for different event sources (API Gateway vs SQS/SNS)
- Return structured JSON responses and handle exceptions safely

## Problem

Fix the Lambda function in `starter.py` to handle environment variables and multiple event shapes.

The function should:

1. Read the DynamoDB table name from `TABLE_NAME` (default `default-table`)
2. Read the deployment stage from `STAGE` (default `dev`)
3. For SQS/SNS-style events with a `Records` array, parse each record body and report how many messages were processed
4. For API Gateway events, include `table`, `stage`, and `operation` (HTTP method) in the response body
5. Catch unexpected errors and return status 500 with an error message

## Exam tip

Lambda environment variables are **encrypted at rest** and available via `os.environ`; use them for table names and stages instead of hard-coding resources—this pattern appears often on deployment and security questions.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/02-lambda-advanced
python runner.py exercises/02-lambda-advanced --solution
```
