"""Lab 04: Secure config — incomplete starter (edit this)."""

from __future__ import annotations

import json
from typing import Any, Dict


def create_kms_key(kms, description: str = "lab04-config") -> str:
    """Create a KMS CMK and return KeyId."""
    # TODO: kms.create_key(...)
    raise NotImplementedError("create_kms_key is not implemented")


def store_secret(
    secrets,
    name: str,
    secret_dict: Dict[str, Any],
    kms_key_id: str,
) -> str:
    """Create a Secrets Manager secret encrypted with kms_key_id; return ARN."""
    # TODO: CreateSecret with SecretString JSON and KmsKeyId
    raise NotImplementedError("store_secret is not implemented")


def put_secure_parameter(ssm, name: str, value: str, kms_key_id: str) -> None:
    """Put an SSM SecureString parameter using the KMS key."""
    # TODO: Type=SecureString, KeyId=kms_key_id
    raise NotImplementedError("put_secure_parameter is not implemented")


def load_app_config(
    secrets,
    ssm,
    secret_id: str,
    param_name: str,
) -> Dict[str, Any]:
    """Load secret JSON + decrypted SSM parameter.

    Return ``{"secret": dict, "param": str}``.
    """
    # TODO: get_secret_value + get_parameter WithDecryption=True
    return {"secret": {}, "param": ""}
