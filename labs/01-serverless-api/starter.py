"""Lab 01: Serverless API — incomplete starter (edit this)."""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional

TABLE_NAME = "lab01-items"


def cors_headers() -> Dict[str, str]:
    # TODO: include Access-Control-Allow-Origin: * and Allow-Methods
    return {"Content-Type": "application/json"}


def ensure_table(dynamodb_resource, table_name: str = TABLE_NAME) -> str:
    """Create DynamoDB table with pk ``id`` (S) if missing; return table name."""
    # TODO: create_table if missing, wait_until_exists
    raise NotImplementedError("ensure_table is not implemented")


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
    """API Gateway Lambda proxy handler backed by DynamoDB.

    Tests inject ``dynamodb`` (boto3 resource) and ``table_name``.
    """
    if dynamodb is None:
        from common.aws_client import get_resource

        dynamodb = get_resource("dynamodb")

    ensure_table(dynamodb, table_name)
    table = dynamodb.Table(table_name)

    method = event.get("httpMethod", "GET")
    path_params = event.get("pathParameters") or {}
    item_id: Optional[str] = path_params.get("id")

    # TODO: implement GET list, GET by id, POST (validate name), DELETE
    if method == "GET" and not item_id:
        return _response(500, {"error": "not implemented"})
    if method == "GET" and item_id:
        return _response(404, {"error": "Not found"})
    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        return _response(200, {"id": str(uuid.uuid4()), "name": body.get("name")})
    if method == "DELETE" and item_id:
        return _response(200, {"deleted": item_id})
    return _response(404, {"error": "Not found"})
