"""Lab 04: Secure config — reference solution."""

from __future__ import annotations

import json
from typing import Any, Dict


def create_kms_key(kms, description: str = "lab04-config") -> str:
    resp = kms.create_key(
        Description=description,
        KeyUsage="ENCRYPT_DECRYPT",
        Origin="AWS_KMS",
    )
    return resp["KeyMetadata"]["KeyId"]


def store_secret(
    secrets,
    name: str,
    secret_dict: Dict[str, Any],
    kms_key_id: str,
) -> str:
    resp = secrets.create_secret(
        Name=name,
        SecretString=json.dumps(secret_dict),
        KmsKeyId=kms_key_id,
    )
    return resp["ARN"]


def put_secure_parameter(ssm, name: str, value: str, kms_key_id: str) -> None:
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type="SecureString",
        KeyId=kms_key_id,
        Overwrite=True,
    )


def load_app_config(
    secrets,
    ssm,
    secret_id: str,
    param_name: str,
) -> Dict[str, Any]:
    secret_resp = secrets.get_secret_value(SecretId=secret_id)
    secret = json.loads(secret_resp["SecretString"])

    param_resp = ssm.get_parameter(Name=param_name, WithDecryption=True)
    param_value = param_resp["Parameter"]["Value"]

    return {"secret": secret, "param": param_value}
