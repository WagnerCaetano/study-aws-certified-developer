"""S3 helpers for LocalStack (upload, download, list, presign) + event parsing."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Union


def upload_json(client, bucket: str, key: str, data: Union[dict, str], content_type: str = "application/json") -> None:
    """Put an object; JSON-serialize dict bodies."""
    body = json.dumps(data) if isinstance(data, dict) else data
    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
    )


def download_text(client, bucket: str, key: str) -> str:
    """Get object body as UTF-8 text."""
    resp = client.get_object(Bucket=bucket, Key=key)
    return resp["Body"].read().decode("utf-8")


def list_keys(client, bucket: str, prefix: str = "") -> List[str]:
    """Return object keys under ``prefix`` (empty prefix = whole bucket)."""
    params: Dict[str, Any] = {"Bucket": bucket}
    if prefix:
        params["Prefix"] = prefix
    resp = client.list_objects_v2(**params)
    return [obj["Key"] for obj in resp.get("Contents", [])]


def generate_presigned_get(client, bucket: str, key: str, expires_in: int = 3600) -> str:
    """Return a presigned GET URL string."""
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )


def parse_s3_event(event: dict) -> List[dict]:
    """Parse S3 event notification records (exam-style Lambda trigger)."""
    results = []
    for record in event.get("Records", []):
        s3 = record.get("s3", {})
        results.append(
            {
                "bucket": s3.get("bucket", {}).get("name"),
                "key": s3.get("object", {}).get("key"),
                "event": record.get("eventName", ""),
            }
        )
    return results
