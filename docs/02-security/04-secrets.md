# AWS Secrets Manager & SSM Parameter Store

> **Domain 2: Security** | [← KMS](03-kms.md) | [Back to Index](../../README.md) | [Next: Security Best Practices →](05-security-best-practices.md)

---

## Overview

AWS provides two main services for storing and managing secrets and configuration data.

| Feature | Secrets Manager | SSM Parameter Store |
|---------|----------------|---------------------|
| Purpose | Secrets (passwords, API keys) | Configuration + secrets |
| Encryption | **KMS** (mandatory) | KMS (optional) |
| Automatic rotation | **Yes** (Lambda-based) | No (manual) |
| Cross-account | **Yes** | Yes |
| Cost | $0.40/secret/month | Free (Standard) |
| Versioning | **Yes** | Yes |
| Max size | 10 KB (plaintext) | 4 KB (Standard), 8 KB (Advanced) |

---

## AWS Secrets Manager

### Create and Retrieve Secrets

```python
import boto3
import json

client = boto3.client('secretsmanager')

# Create a secret
client.create_secret(
    Name='prod/database/credentials',
    Description='Database credentials',
    SecretString=json.dumps({
        'username': 'admin',
        'password': 'SuperSecret123!',
        'host': 'db.example.com',
        'port': 5432
    })
)

# Retrieve a secret
response = client.get_secret_value(SecretId='prod/database/credentials')
secret = json.loads(response['SecretString'])
db_password = secret['password']
```

### Automatic Rotation

```
┌───────────────────┐     ┌──────────────┐     ┌──────────────┐
│  Secrets Manager  │────►│   Lambda     │────►│   Database   │
│  (triggers on     │     │   (rotates   │     │   (password  │
│   schedule)       │     │   password)  │     │    changed)  │
└───────────────────┘     └──────────────┘     └──────────────┘
```

- Rotation schedules: 1 day to 365 days
- Built-in templates for: RDS, Aurora, DocumentDB, Redshift
- Custom Lambda functions for other services

### Cross-Account Access

```python
# Account A: Create resource policy
client.put_resource_policy(
    SecretId='prod/database/credentials',
    ResourcePolicy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::999999999999:root"},
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "*"
        }]
    })
)
```

---

## SSM Parameter Store

### Parameter Types

| Type | Description | Encrypted |
|------|-------------|-----------|
| **String** | Plain text | No |
| **StringList** | Comma-separated list | No |
| **SecureString** | Encrypted with KMS | **Yes** |

### Code Examples

```python
import boto3

ssm = boto3.client('ssm')

# Put a parameter
ssm.put_parameter(
    Name='/my-app/database-url',
    Value='jdbc:postgresql://db.example.com:5432/mydb',
    Type='String',
    Description='Database URL'
)

# Put a secure parameter (secret)
ssm.put_parameter(
    Name='/my-app/database-password',
    Value='SuperSecret123!',
    Type='SecureString',
    KeyId='alias/my-kms-key'
)

# Get a parameter
response = ssm.get_parameter(
    Name='/my-app/database-url'
)
value = response['Parameter']['Value']

# Get a secure parameter (decrypted)
response = ssm.get_parameter(
    Name='/my-app/database-password',
    WithDecryption=True
)
password = response['Parameter']['Value']

# Get parameters by path (hierarchical)
response = ssm.get_parameters_by_path(
    Path='/my-app/',
    Recursive=True,
    WithDecryption=True
)
for param in response['Parameters']:
    print(param['Name'], param['Value'])
```

### Parameter Hierarchy

```
/my-app/
├── /my-app/dev/
│   ├── /my-app/dev/database-url
│   └── /my-app/dev/api-key
├── /my-app/prod/
│   ├── /my-app/prod/database-url
│   └── /my-app/prod/api-key
```

---

## Using Secrets in Lambda

```python
import boto3
import json
import os

# Cache secrets outside handler
_secrets_cache = {}

def get_secret(secret_name):
    if secret_name not in _secrets_cache:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        _secrets_cache[secret_name] = json.loads(response['SecretString'])
    return _secrets_cache[secret_name]

def lambda_handler(event, context):
    # Retrieve secret (cached after first call)
    secret = get_secret(os.environ['SECRET_NAME'])
    db_password = secret['password']
    
    # Use the secret...
```

---

## Using Secrets in ECS

```json
{
  "containerDefinitions": [{
    "name": "my-app",
    "image": "...",
    "secrets": [
      {
        "name": "DB_PASSWORD",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/db-password"
      },
      {
        "name": "API_KEY",
        "valueFrom": "arn:aws:ssm:us-east-1:123456789012:parameter/my-app/api-key"
      }
    ]
  }]
}
```

---

## When to Use What

| Scenario | Use |
|----------|-----|
| Database credentials with auto-rotation | **Secrets Manager** |
| API keys, tokens | Secrets Manager or Parameter Store |
| Application configuration | **Parameter Store** |
| Non-secret config (feature flags) | **Parameter Store (String)** |
| Need automatic rotation | **Secrets Manager** |
| Cost-sensitive | **Parameter Store** (free tier) |
| RDS credentials | **Secrets Manager** (built-in rotation) |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Rotate database password automatically | Secrets Manager with rotation Lambda |
| Store non-secret config | SSM Parameter Store (String type) |
| Access secret in Lambda | Use Secrets Manager SDK, cache outside handler |
| ECS container needs secret | Reference in task definition `secrets` section |
| Cross-account secret access | Secrets Manager resource policy |
| Need to track secret versions | Secrets Manager (built-in versioning) |

---

[← KMS](03-kms.md) | [Back to Index](../../README.md) | [Next: Security Best Practices →](05-security-best-practices.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2: 01-iam.md, 02-cognito.md, 03-kms.md, 04-secrets.md
- [ ] Domain 2: 05-security-best-practices.md
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>