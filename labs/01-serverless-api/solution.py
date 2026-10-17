"""Lab 01: Serverless API — reference solution."""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional

TABLE_NAME = "lab01-items"


def cors_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
    }


def ensure_table(dynamodb_resource, table_name: str = TABLE_NAME) -> str:
    """Create table with partition key ``id`` (S) if missing; return name."""
    existing = [t.name for t in dynamodb_resource.tables.all()]
    if table_name not in existing:
        table = dynamodb_resource.create_table(
            TableName=table_name,
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
    else:
        dynamodb_resource.Table(table_name).wait_until_exists()
    return table_name


def _response(status: int, body: Any = None) -> Dict[str, Any]:
    resp: Dict[str, Any] = {
        "statusCode": status,
        "headers": cors_headers(),
    }
    if body is None and status == 204:
        resp["body"] = ""
    else:
        resp["body"] = json.dumps(body) if not isinstance(body, str) else body
    return resp


def api_handler(
    event: Dict[str, Any],
    context: Any,
    *,
    dynamodb=None,
    table_name: str = TABLE_NAME,
) -> Dict[str, Any]:
    """API Gateway Lambda proxy handler backed by DynamoDB."""
    if dynamodb is None:
        from common.aws_client import get_resource

        dynamodb = get_resource("dynamodb")

    ensure_table(dynamodb, table_name)
    table = dynamodb.Table(table_name)

    method = event.get("httpMethod", "GET")
    path_params = event.get("pathParameters") or {}
    item_id: Optional[str] = path_params.get("id")

    if method == "GET" and not item_id:
        items = table.scan().get("Items", [])
        return _response(200, {"items": items})

    if method == "GET" and item_id:
        result = table.get_item(Key={"id": item_id})
        item = result.get("Item")
        if not item:
            return _response(404, {"error": "Not found"})
        return _response(200, item)

    if method == "POST":
        raw = event.get("body") or "{}"
        body = json.loads(raw) if isinstance(raw, str) else raw
        name = body.get("name")
        if not name:
            return _response(400, {"error": "name is required"})
        new_id = str(uuid.uuid4())
        table.put_item(Item={"id": new_id, "name": str(name)})
        return _response(201, {"id": new_id, "name": name})

    if method == "DELETE" and item_id:
        result = table.get_item(Key={"id": item_id})
        if not result.get("Item"):
            return _response(404, {"error": "Not found"})
        table.delete_item(Key={"id": item_id})
        return _response(204)

    return _response(404, {"error": "Not found"})
