# Exercise 03: Lambda Performance

## Learning goals

- Initialize module-level configuration outside the handler for reuse across invocations
- Validate batch items and fail fast with clear errors
- Return early for empty workloads and respect remaining execution time

## Problem

Optimize the Lambda function in `starter.py` for typical performance and reliability patterns.

The function should:

1. Define `CONFIG` at **module scope** with `table_name` from `TABLE_NAME`, `max_retries` of 3, and a timeout hint
2. Implement `process_item` to require an `id` field or raise `ValueError`
3. Return `{processed: 0}` immediately when the incoming `items` list is empty
4. Process each item in `event['items']` and return counts plus the configured table name
5. Return status 500 when processing raises an exception

## Exam tip

**Reuse connections and clients outside the handler**—initializing boto3 clients or heavy config in the global scope reduces cold-start and warm-invocation latency; exam scenarios often contrast this with creating clients inside `handler`.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/03-lambda-performance
python runner.py exercises/03-lambda-performance --solution
```
