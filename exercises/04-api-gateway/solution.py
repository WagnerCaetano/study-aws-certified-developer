"""API Gateway Lambda proxy handler + LocalStack REST API helpers."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


def build_api_response(status_code: int, body, headers: Optional[dict] = None) -> dict:
    """Build a Lambda proxy integration response with CORS headers."""
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
    if headers:
        default_headers.update(headers)
    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(body) if isinstance(body, dict) else body,
    }


def handler(event, context):
    """Lambda proxy handler for REST-style /items routes."""
    http_method = event.get("httpMethod", "")
    path = event.get("path", "")

    if http_method == "OPTIONS":
        return build_api_response(200, "")

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
        body = json.loads(event.get("body") or "{}")
        if not body.get("name"):
            return build_api_response(400, {"error": "name is required"})
        return build_api_response(201, {"id": "new-1", "name": body["name"]})

    return build_api_response(404, {"error": "Not found"})


def create_rest_api(apigw, name: str) -> str:
    """Create a REST API; return api id."""
    return apigw.create_rest_api(name=name)["id"]


def put_mock_get_method(apigw, api_id: str, path_part: str = "items") -> Dict[str, Any]:
    """
    Create /{path_part} with a MOCK GET that returns 200.

    Uses LocalStack-stable MOCK integration instead of Lambda proxy deploy.
    Returns dict with resource_id and http_method.
    """
    resources = apigw.get_resources(restApiId=api_id)["items"]
    root_id = next(r["id"] for r in resources if r["path"] == "/")
    resource = apigw.create_resource(
        restApiId=api_id, parentId=root_id, pathPart=path_part
    )
    resource_id = resource["id"]
    apigw.put_method(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod="GET",
        authorizationType="NONE",
    )
    apigw.put_method_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod="GET",
        statusCode="200",
        responseModels={"application/json": "Empty"},
    )
    apigw.put_integration(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod="GET",
        type="MOCK",
        requestTemplates={"application/json": '{"statusCode": 200}'},
    )
    apigw.put_integration_response(
        restApiId=api_id,
        resourceId=resource_id,
        httpMethod="GET",
        statusCode="200",
        responseTemplates={
            "application/json": '{"message": "ok", "path": "/' + path_part + '"}'
        },
    )
    return {"resource_id": resource_id, "http_method": "GET", "path_part": path_part}
