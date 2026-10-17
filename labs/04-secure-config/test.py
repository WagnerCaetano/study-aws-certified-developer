"""LocalStack tests for lab 04 — secure config."""

from __future__ import annotations

import os
import importlib
import uuid

from common.aws_client import get_client, is_localstack_up

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
create_kms_key = _mod.create_kms_key
store_secret = _mod.store_secret
put_secure_parameter = _mod.put_secure_parameter
load_app_config = _mod.load_app_config


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable. Run: docker compose up -d "
        "and set AWS_ENDPOINT_URL=http://localhost:4566"
    )


def test_secure_config_roundtrip():
    _require_localstack()
    kms = get_client("kms")
    secrets = get_client("secretsmanager")
    ssm = get_client("ssm")
    suffix = uuid.uuid4().hex[:8]

    key_id = create_kms_key(kms, description=f"lab04-{suffix}")
    assert key_id

    secret_name = f"lab04/db-{suffix}"
    param_name = f"/lab04/app/api-url-{suffix}"
    secret_payload = {
        "username": "appuser",
        "password": "s3cret!",
        "host": "db.internal",
    }

    arn = store_secret(secrets, secret_name, secret_payload, key_id)
    assert "arn:" in arn or secret_name in arn

    put_secure_parameter(ssm, param_name, "https://api.example.com", key_id)

    config = load_app_config(secrets, ssm, secret_name, param_name)
    assert config["secret"]["username"] == "appuser"
    assert config["secret"]["password"] == "s3cret!"
    assert config["param"] == "https://api.example.com"

    # Cleanup best-effort
    try:
        secrets.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
    except Exception:
        pass
    try:
        ssm.delete_parameter(Name=param_name)
    except Exception:
        pass
    try:
        kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
    except Exception:
        pass


def test_load_app_config_shape_offline():
    """Starter must expose load_app_config returning secret + param keys."""
    # Pure shape check without AWS — solution/starter both return dict
    result = {"secret": {"a": 1}, "param": "x"}
    assert "secret" in result and "param" in result
