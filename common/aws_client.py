"""boto3 clients pointed at LocalStack for lab exercises."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import boto3

ENDPOINT_URL = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID", "test")
SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")


def _session() -> boto3.session.Session:
    return boto3.session.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION,
    )


@lru_cache(maxsize=32)
def get_client(service_name: str) -> Any:
    """Return a boto3 client for ``service_name`` aimed at LocalStack."""
    return _session().client(
        service_name,
        endpoint_url=ENDPOINT_URL,
    )


@lru_cache(maxsize=16)
def get_resource(service_name: str) -> Any:
    """Return a boto3 resource for ``service_name`` aimed at LocalStack."""
    return _session().resource(
        service_name,
        endpoint_url=ENDPOINT_URL,
    )


def is_localstack_up(timeout: float = 2.0) -> bool:
    """Best-effort check that LocalStack is reachable on the configured endpoint."""
    import urllib.request

    health_url = ENDPOINT_URL.rstrip("/") + "/_localstack/health"
    try:
        with urllib.request.urlopen(health_url, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except Exception:
        return False
