"""Secrets Manager + SSM unit checks and LocalStack store/get tests."""

from __future__ import annotations

import importlib
import json
import os
import uuid

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
build_secret_value = _mod.build_secret_value
parse_secret = _mod.parse_secret
build_ssm_parameter = _mod.build_ssm_parameter
recommend_secrets_service = _mod.recommend_secrets_service
build_ecs_secret_reference = _mod.build_ecs_secret_reference
store_secret = _mod.store_secret
get_secret_string = _mod.get_secret_string
put_parameter = _mod.put_parameter
get_parameter_value = _mod.get_parameter_value

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


def test_build_and_parse_secret():
    secret = build_secret_value("admin", "password123", "db.example.com", 5432, "mydb")
    parsed = parse_secret(secret)
    assert parsed["username"] == "admin"
    assert parsed["host"] == "db.example.com"
    assert parsed["port"] == "5432"


def test_ssm_secure_string():
    params = build_ssm_parameter(
        "/app/db-password", "secret123", "SecureString", "DB Password", "alias/my-key"
    )
    assert params["Type"] == "SecureString"
    assert params["KeyId"] == "alias/my-key"


def test_ssm_plain_string():
    params = build_ssm_parameter("/app/config", "value", "String", "Config")
    assert params["Type"] == "String"
    assert "KeyId" not in params


def test_recommend_secrets_manager():
    assert recommend_secrets_service({"auto_rotation": True}) == "secrets-manager"
    assert recommend_secrets_service({"is_database": True}) == "secrets-manager"


def test_recommend_parameter_store():
    assert recommend_secrets_service({"cost_sensitive": True}) == "parameter-store"


def test_ecs_secret_ref():
    ref = build_ecs_secret_reference(
        "DB_PASSWORD", "arn:aws:secretsmanager:us-east-1:123:secret:my-secret"
    )
    assert ref["name"] == "DB_PASSWORD"
    assert ref["valueFrom"] == "arn:aws:secretsmanager:us-east-1:123:secret:my-secret"


def test_secrets_manager_roundtrip():
    _require_localstack()
    sm = get_client("secretsmanager")
    name = f"ex19/secret-{uuid.uuid4().hex[:10]}"
    payload = build_secret_value("admin", "s3cret", "db.local", 5432, "app")
    arn = store_secret(sm, name, payload)
    assert isinstance(arn, str) and "secret" in arn.lower()
    try:
        got = get_secret_string(sm, name)
        assert parse_secret(got)["username"] == "admin"
        assert parse_secret(got)["port"] == "5432"
    finally:
        try:
            sm.delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
        except ClientError:
            pass


def test_ssm_parameter_roundtrip():
    _require_localstack()
    ssm = get_client("ssm")
    name = f"/ex19/config-{uuid.uuid4().hex[:10]}"
    params = build_ssm_parameter(name, "hello-localstack", "String", "test")
    put_parameter(ssm, params)
    try:
        assert get_parameter_value(ssm, name) == "hello-localstack"
    finally:
        try:
            ssm.delete_parameter(Name=name)
        except ClientError:
            pass
