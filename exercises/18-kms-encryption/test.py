"""KMS policy unit checks + LocalStack encrypt/decrypt/data-key."""

from __future__ import annotations

import importlib
import os
import uuid

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
build_kms_key_policy = _mod.build_kms_key_policy
determine_encryption_method = _mod.determine_encryption_method
build_s3_kms_config = _mod.build_s3_kms_config
create_cmk = _mod.create_cmk
encrypt_text = _mod.encrypt_text
decrypt_text = _mod.decrypt_text
generate_data_key = _mod.generate_data_key

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


def test_key_policy_has_root():
    policy = build_kms_key_policy("123456789012")
    assert len(policy["Statement"]) >= 1
    assert "123456789012" in policy["Statement"][0]["Principal"]["AWS"]


def test_key_policy_with_roles():
    policy = build_kms_key_policy("123", ["arn:aws:iam::123:role/LambdaRole"])
    assert len(policy["Statement"]) == 2
    role_stmt = policy["Statement"][1]
    assert "kms:Encrypt" in role_stmt["Action"]


def test_direct_encryption_for_small_data():
    assert determine_encryption_method(2)["method"] == "direct"


def test_envelope_for_large_data():
    assert determine_encryption_method(100)["method"] == "envelope"


def test_s3_kms_config():
    config = build_s3_kms_config("alias/my-key")
    rule = config["Rules"][0]
    assert rule["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"] == "aws:kms"
    assert rule["BucketKeyEnabled"] is True


def test_encrypt_decrypt_roundtrip():
    _require_localstack()
    kms = get_client("kms")
    key_id = create_cmk(kms, description=f"ex18-{uuid.uuid4().hex[:8]}")
    assert isinstance(key_id, str)
    try:
        blob = encrypt_text(kms, key_id, "secret-payload")
        assert isinstance(blob, (bytes, bytearray))
        assert decrypt_text(kms, bytes(blob)) == "secret-payload"
    finally:
        try:
            kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
        except ClientError:
            pass


def test_generate_data_key():
    _require_localstack()
    kms = get_client("kms")
    key_id = create_cmk(kms, description=f"ex18-dk-{uuid.uuid4().hex[:8]}")
    try:
        keys = generate_data_key(kms, key_id)
        assert "plaintext" in keys and "ciphertext" in keys
        assert isinstance(keys["plaintext"], (bytes, bytearray))
        assert isinstance(keys["ciphertext"], (bytes, bytearray))
        # Decrypt the wrapped data key back
        plain = kms.decrypt(CiphertextBlob=keys["ciphertext"])["Plaintext"]
        assert plain == keys["plaintext"]
    finally:
        try:
            kms.schedule_key_deletion(KeyId=key_id, PendingWindowInDays=7)
        except ClientError:
            pass
