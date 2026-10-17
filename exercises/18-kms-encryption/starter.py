"""KMS helpers — fix policy builders and LocalStack encrypt/decrypt bugs."""

from __future__ import annotations

from typing import List, Optional


def build_kms_key_policy(account_id: str, allowed_roles: Optional[List[str]] = None) -> dict:
    """Build a KMS key policy for root + optional roles."""
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "EnableRootAccountAccess",
                "Effect": "Allow",
                "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                "Action": "kms:*",
                "Resource": "*",
            }
        ],
    }
    if allowed_roles:
        policy["Statement"].append(
            {
                "Sid": "AllowRoleAccess",
                "Effect": "Allow",
                "Principal": {"AWS": allowed_roles},
                # BUG: missing Encrypt/Decrypt/GenerateDataKey
                "Action": ["kms:DescribeKey"],
                "Resource": "*",
            }
        )
    return policy


def determine_encryption_method(data_size_kb: float) -> dict:
    """Direct KMS encrypt only for payloads ≤ 4 KB; else envelope encryption."""
    # BUG: threshold wrongly set to 4096 KB
    if data_size_kb <= 4096:
        return {
            "method": "direct",
            "description": "Use KMS Encrypt/Decrypt directly",
            "api": "kms.encrypt()",
        }
    return {
        "method": "envelope",
        "description": "Use envelope encryption with GenerateDataKey",
        "api": "kms.generate_data_key()",
    }


def build_s3_kms_config(kms_key_id: str) -> dict:
    """S3 default encryption with SSE-KMS and bucket keys."""
    return {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    # BUG: AES256 instead of aws:kms; BucketKeyEnabled false
                    "SSEAlgorithm": "AES256",
                    "KMSMasterKeyID": kms_key_id,
                },
                "BucketKeyEnabled": False,
            }
        ]
    }


def create_cmk(kms_client, description: str = "ex18-cmk") -> str:
    """Create a CMK; return KeyId."""
    # BUG: returns whole KeyMetadata
    return kms_client.create_key(Description=description)["KeyMetadata"]


def encrypt_text(kms_client, key_id: str, plaintext: str) -> bytes:
    """Encrypt UTF-8 text with KMS; return CiphertextBlob bytes."""
    # BUG: passes str without encoding; returns whole response
    return kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)


def decrypt_text(kms_client, ciphertext_blob: bytes) -> str:
    """Decrypt CiphertextBlob to UTF-8 text."""
    # BUG: returns raw Plaintext bytes without decode
    resp = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    return resp["Plaintext"]


def generate_data_key(kms_client, key_id: str, key_spec: str = "AES_256") -> dict:
    """Return {'plaintext': bytes, 'ciphertext': bytes} from GenerateDataKey."""
    resp = kms_client.generate_data_key(KeyId=key_id, KeySpec=key_spec)
    # BUG: wrong keys / CiphertextBlob name
    return {
        "plaintext": resp["Plaintext"],
        "ciphertext_blob": resp["CiphertextBlob"],
    }
