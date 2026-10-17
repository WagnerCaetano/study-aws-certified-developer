"""LocalStack tests for lab 03 — async S3 pipeline."""

from __future__ import annotations

import json
import os
import importlib
import uuid

from common.aws_client import get_client, get_resource, is_localstack_up

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
transform_line = _mod.transform_line
ensure_resources = _mod.ensure_resources
pipeline_handler = _mod.pipeline_handler


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable. Run: docker compose up -d "
        "and set AWS_ENDPOINT_URL=http://localhost:4566"
    )


def test_transform_line():
    item = transform_line("42,orders,99.5")
    assert item["pk"] == "RECORD#42"
    assert item["sk"] == "DATA#orders"
    assert item["value"] == "99.5"
    assert item["status"] == "processed"


def test_pipeline_s3_to_dynamodb():
    _require_localstack()
    s3 = get_client("s3")
    dynamodb = get_resource("dynamodb")
    suffix = uuid.uuid4().hex[:8]
    bucket = f"lab03-ingest-{suffix}"
    table_name = f"lab03-records-{suffix}"
    key = "uploads/batch.csv"

    ensure_resources(s3, dynamodb, bucket, table_name)

    csv_body = "1,orders,10\n2,inventory,5\n"
    s3.put_object(Bucket=bucket, Key=key, Body=csv_body.encode("utf-8"))

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": bucket},
                    "object": {"key": key},
                }
            }
        ]
    }

    try:
        result = pipeline_handler(
            event,
            None,
            s3=s3,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert result["statusCode"] == 200, result
        body = result["body"]
        if isinstance(body, str):
            body = json.loads(body)
        assert body["processed"] == 2
        assert key in body["keys"]

        table = dynamodb.Table(table_name)
        item1 = table.get_item(Key={"pk": "RECORD#1", "sk": "DATA#orders"}).get("Item")
        assert item1 is not None
        assert item1["value"] == "10"
        assert item1["status"] == "processed"
    finally:
        try:
            s3.delete_object(Bucket=bucket, Key=key)
            s3.delete_bucket(Bucket=bucket)
        except Exception:
            pass
        try:
            dynamodb.Table(table_name).delete()
        except Exception:
            pass
