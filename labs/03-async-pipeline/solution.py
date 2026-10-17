"""Lab 03: Async S3 → Lambda → DynamoDB pipeline — reference solution."""

from __future__ import annotations

import json
from typing import Any, Dict, List
from urllib.parse import unquote_plus

TABLE_NAME = "lab03-records"
BUCKET_NAME = "lab03-ingest"


def transform_line(line: str) -> Dict[str, str]:
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) < 3:
        raise ValueError(f"Expected id,category,value got: {line!r}")
    record_id, category, value = parts[0], parts[1], parts[2]
    return {
        "pk": f"RECORD#{record_id}",
        "sk": f"DATA#{category}",
        "value": value,
        "status": "processed",
    }


def ensure_resources(s3, dynamodb_resource, bucket: str, table_name: str) -> None:
    existing_buckets = {b["Name"] for b in s3.list_buckets().get("Buckets", [])}
    if bucket not in existing_buckets:
        s3.create_bucket(Bucket=bucket)

    existing_tables = [t.name for t in dynamodb_resource.tables.all()]
    if table_name not in existing_tables:
        table = dynamodb_resource.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "pk", "KeyType": "HASH"},
                {"AttributeName": "sk", "KeyType": "RANGE"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
    else:
        dynamodb_resource.Table(table_name).wait_until_exists()


def pipeline_handler(
    event: Dict[str, Any],
    context: Any,
    *,
    s3=None,
    dynamodb=None,
    table_name: str = TABLE_NAME,
) -> Dict[str, Any]:
    if s3 is None:
        from common.aws_client import get_client

        s3 = get_client("s3")
    if dynamodb is None:
        from common.aws_client import get_resource

        dynamodb = get_resource("dynamodb")

    table = dynamodb.Table(table_name)
    processed = 0
    keys: List[str] = []

    for record in event.get("Records", []):
        s3info = record.get("s3", {})
        bucket = s3info.get("bucket", {}).get("name")
        key = unquote_plus(s3info.get("object", {}).get("key", ""))
        if not bucket or not key:
            continue
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read().decode("utf-8")
        for line in body.splitlines():
            line = line.strip()
            if not line:
                continue
            item = transform_line(line)
            table.put_item(Item=item)
            processed += 1
        keys.append(key)

    return {
        "statusCode": 200,
        "body": json.dumps({"processed": processed, "keys": keys}),
    }
