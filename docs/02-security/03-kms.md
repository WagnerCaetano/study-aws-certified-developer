# AWS KMS & Encryption

> **Domain 2: Security** | [← Cognito](02-cognito.md) | [Back to Index](../../README.md) | [Next: Secrets Manager →](04-secrets.md)

---

## Overview

AWS Key Management Service (KMS) creates and manages **cryptographic keys** used to encrypt data across AWS services.

---

## Key Types

| Key Type | Management | Use Case |
|----------|-----------|----------|
| **AWS Managed Keys** | AWS manages (free) | `aws/s3`, `aws/dynamodb`, etc. |
| **Customer Managed Keys** | You manage ($1/month) | Custom key policies, rotation |
| **AWS Owned Keys** | AWS owns and manages | Shared across accounts |

### Customer Managed Key (CMK)

```python
import boto3

kms = boto3.client('kms')

# Create a customer managed key
response = kms.create_key(
    Description='My application encryption key',
    KeyUsage='ENCRYPT_DECRYPT',
    Origin='AWS_KMS',
    Policy='...'  # Custom key policy
)
key_id = response['KeyMetadata']['KeyId']

# Create an alias
kms.create_alias(
    AliasName='alias/my-app-key',
    TargetKeyId=key_id
)

# Enable key rotation (automatic, yearly)
kms.enable_key_rotation(KeyId=key_id)

# Encrypt data
response = kms.encrypt(
    KeyId='alias/my-app-key',
    Plaintext=b'Sensitive data here'
)
ciphertext = response['CiphertextBlob']

# Decrypt data
response = kms.decrypt(CiphertextBlob=ciphertext)
plaintext = response['Plaintext']
```

---

## Envelope Encryption

```
┌────────────────────────────────────────────────────┐
│                Envelope Encryption                  │
│                                                    │
│  1. Generate Data Key from KMS                    │
│     ├── Plaintext Data Key (used to encrypt data) │
│     └── Encrypted Data Key (stored with data)     │
│                                                    │
│  2. Encrypt data with Plaintext Data Key          │
│                                                    │
│  3. Discard Plaintext Data Key                    │
│                                                    │
│  4. Store: encrypted data + encrypted data key    │
│                                                    │
│  To decrypt:                                       │
│  5. Send encrypted data key to KMS                │
│  6. KMS returns plaintext data key                │
│  7. Decrypt data with plaintext data key          │
└────────────────────────────────────────────────────┘
```

**Why?** KMS has a 4 KB limit for direct encryption. Envelope encryption handles data of any size.

---

## KMS with AWS Services

### S3 (SSE-KMS)
```python
s3.put_object(
    Bucket='my-bucket',
    Key='secret.txt',
    Body=b'secret data',
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='alias/my-app-key'
)
```

### DynamoDB
```python
# At table creation
dynamodb.create_table(
    TableName='Users',
    SSESpecification={'Enabled': True, 'SSEType': 'KMS', 'KMSMasterKeyId': 'alias/my-key'}
)
```

---

## KMS Key Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Enable IAM User Permissions",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "Allow Lambda to encrypt/decrypt",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789012:role/LambdaRole"},
      "Action": ["kms:Encrypt", "kms:Decrypt", "kms:GenerateDataKey"],
      "Resource": "*"
    }
  ]
}
```

**⚠️ Key policies are NOT like IAM policies.** The default policy gives the account root full access. You must explicitly grant access to other principals.

---

## API Call Limits

- **Shared quota:** 5,500/second per region (shared across calling services)
- **GenerateDataKey:** Most common for encryption operations
- **Throttling:** Can occur with high-volume encryption workloads

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Need to control who can decrypt | Use customer managed key with key policy |
| Encrypt data > 4 KB | Use envelope encryption (GenerateDataKey) |
| Automatic key rotation | Enable on customer managed key (annual) |
| Audit key usage | Use CloudTrail (KMS logs all API calls) |
| Cross-account encryption | Update key policy to allow other account |
| Lambda can't decrypt S3 object | Check KMS key policy grants access |

---

[← Cognito](02-cognito.md) | [Back to Index](../../README.md) | [Next: Secrets Manager →](04-secrets.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2: 01-iam.md
- [x] Domain 2: 02-cognito.md
- [x] Domain 2: 03-kms.md
- [ ] Domain 2: 04-secrets.md
- [ ] Domain 2: 05-security-best-practices.md
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>