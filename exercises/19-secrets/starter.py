"""Secrets/SSM helpers — fix builders and LocalStack store/get bugs."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


def build_secret_value(username, password, host, port, database) -> str:
    """JSON secret string for database credentials (port as string)."""
    # BUG: port left as int
    return json.dumps(
        {
            "username": username,
            "password": password,
            "host": host,
            "port": port,
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
    # BUG: ignores param_type and KeyId
    return {
        "Name": name,
        "Value": value,
        "Type": "String",
        "Description": description,
        "Overwrite": True,
    }


def recommend_secrets_service(requirements: dict) -> str:
    # BUG: inverted recommendations
    if requirements.get("auto_rotation"):
        return "parameter-store"
    if requirements.get("is_database"):
        return "parameter-store"
    if requirements.get("cost_sensitive"):
        return "secrets-manager"
    return "parameter-store"


def build_ecs_secret_reference(name: str, secret_arn: str) -> dict:
    # BUG: value instead of valueFrom
    return {"name": name, "value": secret_arn}


def store_secret(sm_client, name: str, secret_string: str) -> str:
    """Create a secret; return ARN."""
    # BUG: returns whole response
    return sm_client.create_secret(Name=name, SecretString=secret_string)


def get_secret_string(sm_client, secret_id: str) -> str:
    """Return SecretString for a secret id/ARN/name."""
    # BUG: returns whole response
    return sm_client.get_secret_value(SecretId=secret_id)


def put_parameter(ssm_client, params: dict) -> None:
    """Call put_parameter with a params dict from build_ssm_parameter."""
    # BUG: wrong method name
    ssm_client.put_param(**params)


def get_parameter_value(ssm_client, name: str, decrypt: bool = True) -> str:
    """Return parameter Value (WithDecryption for SecureString)."""
    # BUG: missing WithDecryption; returns Parameter object
    resp = ssm_client.get_parameter(Name=name)
    return resp["Parameter"]
