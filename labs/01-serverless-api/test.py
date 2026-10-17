"""LocalStack tests for lab 01 — serverless API."""

from __future__ import annotations

import json
import os
import importlib
import uuid

from common.aws_client import get_resource, is_localstack_up

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
api_handler = _mod.api_handler
cors_headers = _mod.cors_headers
ensure_table = _mod.ensure_table


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable. Run: docker compose up -d "
        "and set AWS_ENDPOINT_URL=http://localhost:4566"
    )


def test_cors_headers():
    headers = cors_headers()
    assert headers.get("Access-Control-Allow-Origin") == "*"
    methods = headers.get("Access-Control-Allow-Methods", "")
    assert "GET" in methods and "POST" in methods


def test_ensure_table_and_crud():
    _require_localstack()
    dynamodb = get_resource("dynamodb")
    table_name = f"lab01-items-{uuid.uuid4().hex[:8]}"

    ensure_table(dynamodb, table_name)
    assert table_name in [t.name for t in dynamodb.tables.all()]

    try:
        create = api_handler(
            {
                "httpMethod": "POST",
                "body": json.dumps({"name": "Widget"}),
                "pathParameters": None,
            },
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert create["statusCode"] == 201, create
        created = json.loads(create["body"])
        item_id = created["id"]
        assert created["name"] == "Widget"
        assert create["headers"].get("Access-Control-Allow-Origin") == "*"

        bad = api_handler(
            {"httpMethod": "POST", "body": json.dumps({}), "pathParameters": None},
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert bad["statusCode"] == 400

        listed = api_handler(
            {"httpMethod": "GET", "pathParameters": None},
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert listed["statusCode"] == 200
        items = json.loads(listed["body"])["items"]
        assert any(i.get("id") == item_id for i in items)

        got = api_handler(
            {"httpMethod": "GET", "pathParameters": {"id": item_id}},
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert got["statusCode"] == 200
        assert json.loads(got["body"])["id"] == item_id

        missing = api_handler(
            {"httpMethod": "GET", "pathParameters": {"id": "does-not-exist"}},
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert missing["statusCode"] == 404

        deleted = api_handler(
            {"httpMethod": "DELETE", "pathParameters": {"id": item_id}},
            None,
            dynamodb=dynamodb,
            table_name=table_name,
        )
        assert deleted["statusCode"] == 204
    finally:
        try:
            dynamodb.Table(table_name).delete()
        except Exception:
            pass
