# Exercise 33: Data Pipeline

## Learning goals

- Parse CSV rows for S3-triggered ingestion
- Transform raw rows into DynamoDB-style keys (`RECORD#`, `DATA#`)
- Batch writes respecting DynamoDB batch limits (25 items)
- Handle S3 event records in a Lambda processor

## Problem

Fix the pipeline helpers in `starter.py`.

1. **`parse_csv_line`**: Split on **commas**, not semicolons.
2. **`transform_record`**: Set `pk` to `RECORD#{id}`, `sk` to `DATA#{sort key}`, and `status` to **`processed`**.
3. **`batch_records`**: Chunk records using the full `batch_size` stride (e.g., 10 → three batches of 10 for 30 items).
4. **`build_pipeline_processor`**: Return **statusCode 200** after processing S3 notification records.

## Exam tip

S3 event notifications can trigger Lambda directly; large files often use S3 → SQS → Lambda for backpressure. DynamoDB `BatchWriteItem` accepts at most 25 items per request.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/33-data-pipeline
python runner.py exercises/33-data-pipeline --solution
```

## Next: multi-service lab

This exercise is an **offline concept check**. For the LocalStack hands-on (S3 event → Lambda → DynamoDB), continue with:

**[labs/03-async-pipeline](../../labs/03-async-pipeline/)**
