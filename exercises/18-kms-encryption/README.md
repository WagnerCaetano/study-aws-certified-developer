# Exercise 18: KMS Encryption

## Learning goals

- Structure KMS key policies and choose direct vs envelope encryption
- Configure S3 default encryption with SSE-KMS + bucket keys
- Call live KMS `encrypt` / `decrypt` / `generate_data_key` on LocalStack

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `kms`

**Cleanup:** tests schedule CMK deletion (`PendingWindowInDays=7`). Stop LocalStack with `docker compose down` (ephemeral data is discarded when persistence is off).

## Problem

Fix `starter.py`:

1. Role statement actions: `kms:Encrypt`, `kms:Decrypt`, `kms:GenerateDataKey`
2. Direct encryption only when size ≤ **4** KB
3. S3 config: `SSEAlgorithm: aws:kms`, `BucketKeyEnabled: true`
4. **create_cmk** — return `KeyId` string
5. **encrypt_text** / **decrypt_text** — encode/decode UTF-8; return blob / text
6. **generate_data_key** — return `{'plaintext', 'ciphertext'}`

## Exam tip

KMS `Encrypt` accepts up to 4 KB; larger payloads use envelope encryption (`GenerateDataKey`).

## Run

```bash
docker compose up -d
python runner.py exercises/18-kms-encryption
python runner.py exercises/18-kms-encryption --solution
```
