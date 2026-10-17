"""Live S3 tests against LocalStack (create / exercise / teardown)."""

from __future__ import annotations

import importlib
import json
import os
import uuid
from contextlib import contextmanager

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
upload_json = _mod.upload_json
download_text = _mod.download_text
list_keys = _mod.list_keys
generate_presigned_get = _mod.generate_presigned_get
parse_s3_event = _mod.parse_s3_event

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


@contextmanager
def temp_bucket():
    _require_localstack()
    s3 = get_client("s3")
    name = f"ex07-{uuid.uuid4().hex[:10]}"
    s3.create_bucket(Bucket=name)
    try:
        yield s3, name
    finally:
        try:
            for obj in s3.list_objects_v2(Bucket=name).get("Contents", []) or []:
                s3.delete_object(Bucket=name, Key=obj["Key"])
            s3.delete_bucket(Bucket=name)
        except ClientError:
            pass


def test_upload_and_download_dict():
    with temp_bucket() as (s3, bucket):
        upload_json(s3, bucket, "data.json", {"hello": "world"})
        text = download_text(s3, bucket, "data.json")
        assert json.loads(text) == {"hello": "world"}


def test_upload_string():
    with temp_bucket() as (s3, bucket):
        upload_json(s3, bucket, "note.txt", "plain-text", content_type="text/plain")
        assert download_text(s3, bucket, "note.txt") == "plain-text"


def test_list_keys_with_prefix():
    with temp_bucket() as (s3, bucket):
        upload_json(s3, bucket, "uploads/a.json", {"a": 1})
        upload_json(s3, bucket, "uploads/b.json", {"b": 2})
        upload_json(s3, bucket, "other/c.json", {"c": 3})
        keys = list_keys(s3, bucket, "uploads/")
        assert sorted(keys) == ["uploads/a.json", "uploads/b.json"]


def test_presigned_get_url():
    with temp_bucket() as (s3, bucket):
        upload_json(s3, bucket, "file.pdf", "pdf-bytes")
        url = generate_presigned_get(s3, bucket, "file.pdf", expires_in=7200)
        assert isinstance(url, str)
        assert bucket in url
        assert "file.pdf" in url or "file%2Epdf" in url or "X-Amz" in url


def test_parse_s3_event():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "my-bucket"},
                    "object": {"key": "uploads/file.csv"},
                },
                "eventName": "ObjectCreated:Put",
            }
        ]
    }
    result = parse_s3_event(event)
    assert len(result) == 1
    assert result[0]["bucket"] == "my-bucket"
    assert result[0]["key"] == "uploads/file.csv"
    assert result[0]["event"] == "ObjectCreated:Put"


def test_parse_empty_event():
    assert parse_s3_event({}) == []
