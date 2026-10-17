"""Lab 03: Async S3 → Lambda → DynamoDB pipeline — incomplete starter."""

from __future__ import annotations

import json
from typing import Any, Dict

TABLE_NAME = "lab03-records"
BUCKET_NAME = "lab03-ingest"


def transform_line(line: str) -> Dict[str, str]:
    """Parse CSV id,category,value into a DynamoDB item dict."""
    # TODO: pk=RECORD#{id}, sk=DATA#{category}, status=processed
    parts = line.strip().split(";")
    return {
        "pk": parts[0] if parts else "",
        "sk": parts[1] if len(parts) > 1 else "",
        "value": parts[2] if len(parts) > 2 else "",
        "status": "pending",
    }


def ensure_resources(s3, dynamodb_resource, bucket: str, table_name: str) -> None:
    """Create S3 bucket and DynamoDB table (pk/sk) if missing."""
    # TODO: create_bucket + create_table with pk HASH, sk RANGE
    raise NotImplementedError("ensure_resources is not implemented")


def pipeline_handler(
    event: Dict[str, Any],
    context: Any,
    *,
    s3=None,
    dynamodb=None,
    table_name: str = TABLE_NAME,
) -> Dict[str, Any]:
    """Process S3 ObjectCreated event records into DynamoDB."""
    if s3 is None:
        from common.aws_client import get_client

        s3 = get_client("s3")
    if dynamodb is None:
        from common.aws_client import get_resource

        dynamodb = get_resource("dynamodb")

    # TODO: for each Records[].s3 — GetObject, transform lines, put_item
    return {"statusCode": 500, "body": json.dumps({"processed": 0, "keys": []})}
