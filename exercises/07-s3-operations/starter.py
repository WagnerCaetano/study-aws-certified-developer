"""S3 helpers — fix the bugs so tests pass against LocalStack."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Union


def upload_json(client, bucket: str, key: str, data: Union[dict, str], content_type: str = "application/json") -> None:
    """Put an object; JSON-serialize dict bodies."""
    # BUG: wrong param casing (bucket/key) and no ContentType / JSON encode
    client.put_object(bucket=bucket, key=key, Body=data)


def download_text(client, bucket: str, key: str) -> str:
    """Get object body as UTF-8 text."""
    # BUG: returns raw StreamingBody without reading/decoding
    resp = client.get_object(Bucket=bucket, Key=key)
    return resp["Body"]


def list_keys(client, bucket: str, prefix: str = "") -> List[str]:
    """Return object keys under ``prefix`` (empty prefix = whole bucket)."""
    params: Dict[str, Any] = {"Bucket": bucket}
    if prefix:
        params["prefix"] = prefix  # BUG: should be Prefix
    resp = client.list_objects_v2(**params)
    return [obj["Key"] for obj in resp.get("Contents", [])]


def generate_presigned_get(client, bucket: str, key: str, expires_in: int = 3600) -> str:
    """Return a presigned GET URL string."""
    # BUG: wrong kwarg name Expiration vs ExpiresIn; wrong ClientMethod shape
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        Expiration=expires_in,
    )


def parse_s3_event(event: dict) -> List[dict]:
    """Parse S3 event notification records (exam-style Lambda trigger)."""
    results = []
    for record in event.get("Records", []):
        # BUG: looks at top-level bucket/object instead of record['s3']
        results.append(
            {
                "bucket": record.get("bucket", {}).get("name"),
                "key": record.get("object", {}).get("key"),
                "event": record.get("eventName", ""),
            }
        )
    return results
