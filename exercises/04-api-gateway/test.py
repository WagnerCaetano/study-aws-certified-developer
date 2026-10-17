"""Handler unit tests + LocalStack REST API (MOCK) setup/teardown."""

from __future__ import annotations

import importlib
import json
import os
import uuid

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
handler = _mod.handler
create_rest_api = _mod.create_rest_api
put_mock_get_method = _mod.put_mock_get_method

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


def test_get_items():
    event = {"httpMethod": "GET", "path": "/items"}
    result = handler(event, None)
    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert "items" in body


def test_get_item_by_id():
    event = {
        "httpMethod": "GET",
        "path": "/items/123",
        "pathParameters": {"id": "123"},
    }
    result = handler(event, None)
    assert result["statusCode"] == 200
    assert json.loads(result["body"])["id"] == "123"


def test_post_item():
    event = {
        "httpMethod": "POST",
        "path": "/items",
        "body": json.dumps({"name": "New Item"}),
    }
    result = handler(event, None)
    assert result["statusCode"] == 201


def test_post_item_missing_name():
    event = {"httpMethod": "POST", "path": "/items", "body": json.dumps({})}
    result = handler(event, None)
    assert result["statusCode"] == 400


def test_cors_preflight():
    event = {"httpMethod": "OPTIONS", "path": "/items"}
    result = handler(event, None)
    assert result["statusCode"] == 200
    assert "Access-Control-Allow-Origin" in result["headers"]


def test_cors_headers_present():
    event = {"httpMethod": "GET", "path": "/items"}
    result = handler(event, None)
    assert result["headers"]["Access-Control-Allow-Origin"] == "*"


def test_not_found():
    event = {"httpMethod": "DELETE", "path": "/unknown"}
    result = handler(event, None)
    assert result["statusCode"] == 404


def test_localstack_rest_api_mock_get():
    """Create REST API + MOCK GET /items on LocalStack (stable subset of APIGW)."""
    _require_localstack()
    apigw = get_client("apigateway")
    name = f"ex04-{uuid.uuid4().hex[:10]}"
    api_id = create_rest_api(apigw, name)
    assert isinstance(api_id, str) and api_id
    try:
        meta = put_mock_get_method(apigw, api_id, "items")
        resources = apigw.get_resources(restApiId=api_id)["items"]
        paths = {r.get("path") for r in resources}
        assert "/items" in paths
        methods = apigw.get_method(
            restApiId=api_id,
            resourceId=meta["resource_id"],
            httpMethod="GET",
        )
        assert methods["httpMethod"] == "GET"
        integration = apigw.get_integration(
            restApiId=api_id,
            resourceId=meta["resource_id"],
            httpMethod="GET",
        )
        assert integration["type"] == "MOCK"
    finally:
        try:
            apigw.delete_rest_api(restApiId=api_id)
        except ClientError:
            pass
