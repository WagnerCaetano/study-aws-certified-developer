"""Secrets Manager + SSM helpers for LocalStack, plus recommendation helpers."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


def build_secret_value(username, password, host, port, database) -> str:
    """JSON secret string for database credentials (port as string)."""
    return json.dumps(
        {
            "username": username,
            "password": password,
            "host": host,
            "port": str(port),
            "database": database,
            "engine": "postgres",
        }
    )


def parse_secret(secret_string: str) -> dict:
    return json.loads(secret_string)


def build_ssm_parameter(
    name: str,
    value: str,
    param_type: str = "String",
    description: str = "",
    kms_key_id: Optional[str] = None,
) -> dict:
    params: Dict[str, Any] = {
        "Name": name,
        "Value": value,
        "Type": param_type,
        "Description": description,
        "Overwrite": True,
    }
    if kms_key_id and param_type == "SecureString":
        params["KeyId"] = kms_key_id
    return params


def recommend_secrets_service(requirements: dict) -> str:
    if requirements.get("auto_rotation"):
        return "secrets-manager"
    if requirements.get("is_database"):
        return "secrets-manager"
    if requirements.get("cost_sensitive"):
        return "parameter-store"
    if requirements.get("needs_encryption") and not requirements.get("auto_rotation"):
        return "parameter-store"
    return "secrets-manager"


def build_ecs_secret_reference(name: str, secret_arn: str) -> dict:
    return {"name": name, "valueFrom": secret_arn}


def store_secret(sm_client, name: str, secret_string: str) -> str:
    """Create a secret; return ARN."""
    return sm_client.create_secret(Name=name, SecretString=secret_string)["ARN"]


def get_secret_string(sm_client, secret_id: str) -> str:
    """Return SecretString for a secret id/ARN/name."""
    return sm_client.get_secret_value(SecretId=secret_id)["SecretString"]


def put_parameter(ssm_client, params: dict) -> None:
    """Call put_parameter with a params dict from build_ssm_parameter."""
    ssm_client.put_parameter(**params)


def get_parameter_value(ssm_client, name: str, decrypt: bool = True) -> str:
    """Return parameter Value (WithDecryption for SecureString)."""
    resp = ssm_client.get_parameter(Name=name, WithDecryption=decrypt)
    return resp["Parameter"]["Value"]
