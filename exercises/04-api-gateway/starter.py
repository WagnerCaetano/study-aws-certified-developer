"""API Gateway handler + REST helpers — fix bugs for unit + LocalStack tests."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


def build_api_response(status_code: int, body, headers: Optional[dict] = None) -> dict:
    """Build a Lambda proxy integration response with CORS headers."""
    # BUG: missing CORS headers
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body) if isinstance(body, dict) else body,
    }


def handler(event, context):
    """Lambda proxy handler for REST-style /items routes."""
    http_method = event.get("httpMethod", "")
    path = event.get("path", "")

    if http_method == "OPTIONS":
        # BUG: 204 and no CORS via build_api_response
        return {"statusCode": 204, "body": ""}

    if http_method == "GET" and "/items" in path:
        item_id = (
            event.get("pathParameters", {}).get("id")
            if event.get("pathParameters")
            else None
        )
        if item_id:
            return build_api_response(200, {"id": item_id, "name": "Item " + item_id})
        return build_api_response(200, {"items": [{"id": "1", "name": "Item 1"}]})

    if http_method == "POST" and "/items" in path:
        # BUG: treats body as already-parsed dict; returns 200 instead of 201
        body = event.get("body", {})
        if not body.get("name"):
            return build_api_response(400, {"error": "name is required"})
        return build_api_response(200, {"id": "new-1", "name": body["name"]})

    return build_api_response(404, {"error": "Not found"})


def create_rest_api(apigw, name: str) -> str:
    """Create a REST API; return api id."""
    # BUG: returns whole response
    return apigw.create_rest_api(name=name)


def put_mock_get_method(apigw, api_id: str, path_part: str = "items") -> Dict[str, Any]:
    """Create /{path_part} with a MOCK GET that returns 200."""
    resources = apigw.get_resources(restApiId=api_id)["items"]
    root_id = next(r["id"] for r in resources if r["path"] == "/")
    resource = apigw.create_resource(
        restApiId=api_id, parentId=root_id, pathPart=path_part
    )
    resource_id = resource["id"]
    # BUG: missing put_method / put_integration — only creates the resource
    return {"resource_id": resource_id, "http_method": "GET", "path_part": path_part}
