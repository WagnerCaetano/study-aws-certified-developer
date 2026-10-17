# Exercise 07: S3 File Operations

## Learning goals

- Call real S3 `put_object` / `get_object` / `list_objects_v2` against LocalStack
- Generate presigned GET URLs with `ExpiresIn`
- Parse S3 event notification records from Lambda triggers

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `s3`

**Cleanup:** tests create a temporary bucket, empty it, and delete it. Use `docker compose down` to stop LocalStack.

## Problem

Fix the helpers in `starter.py`:

1. **upload_json** — `Bucket`/`Key`/`Body` (JSON-serialize dicts) and `ContentType`
2. **download_text** — read and decode the streaming body
3. **list_keys** — use capital `Prefix`; return key strings
4. **generate_presigned_get** — `generate_presigned_url(..., ExpiresIn=...)`
5. **parse_s3_event** — read nested `Records[].s3.bucket.name` / `object.key`

## Exam tip

S3 event notifications wrap object details under **`Records[].s3`**, not at the top level of each record.

## Run

```bash
docker compose up -d
python runner.py exercises/07-s3-operations
python runner.py exercises/07-s3-operations --solution
```
