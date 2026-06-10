# IAM for Developers

> **Domain 2: Security** | [← Containers](../01-development/10-containers.md) | [Back to Index](../../README.md) | [Next: Cognito →](02-cognito.md)

---

## Overview

AWS Identity and Access Management (IAM) enables you to manage access to AWS services and resources securely.

### Key Concepts
- **Users** — Individual people or applications
- **Groups** — Collection of users with shared permissions
- **Roles** — Temporary credentials for AWS services or cross-account access
- **Policies** — JSON documents defining permissions
- **Identity Providers** — Federation with external identity systems

---

## IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": ["10.0.0.0/8"]
        }
      }
    }
  ]
}
```

### Policy Elements

| Element | Description | Example |
|---------|-------------|---------|
| **Version** | Policy language version | `"2012-10-17"` |
| **Effect** | Allow or Deny | `"Allow"` / `"Deny"` |
| **Action** | AWS API calls | `"s3:GetObject"`, `"dynamodb:Query"` |
| **Resource** | ARN of resource | `"arn:aws:s3:::bucket/*"` |
| **Condition** | When the policy applies | Source IP, time, MFA, etc. |

### Policy Evaluation Logic

```
1. Explicit DENY → Always wins
2. Explicit ALLOW → Granted
3. Default → Implicit DENY (no permission)
```

**⚠️ Deny always overrides Allow!**

---

## IAM Roles for AWS Services

### Lambda Execution Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/Users"
    }
  ]
}
```

### ECS Task Role vs Execution Role

| Role | What it does |
|------|-------------|
| **Task Role** | Permissions for your app code (like Lambda role) |
| **Execution Role** | Pull images from ECR, write logs to CloudWatch |

### IAM Role Trust Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

---

## IAM Best Practices

1. **Never use root account** for everyday tasks
2. **Use roles instead of access keys** for EC2, Lambda, ECS
3. **Follow least privilege** — Grant minimum permissions needed
4. **Use IAM Groups** to assign permissions to users
5. **Enable MFA** for all users
6. **Rotate credentials** regularly
7. **Use IAM Access Analyzer** to identify overly permissive policies
8. **Never embed credentials** in code

---

## STS (Security Token Service)

### Key Operations

```python
import boto3

sts = boto3.client('sts')

# Assume a role (cross-account or within account)
response = sts.assume_role(
    RoleArn='arn:aws:iam::999999999999:role/CrossAccountRole',
    RoleSessionName='MySession'
)

# Use temporary credentials
credentials = response['Credentials']
client = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Get current identity
identity = sts.get_caller_identity()
```

### STS for Cross-Account Access

```
Account A (111111111111)          Account B (999999999999)
┌──────────────────┐             ┌──────────────────┐
│  User/Role       │────────────►│  Target Role     │
│  with permission │  AssumeRole │  (trust policy   │
│  to assume       │             │   allows Acct A) │
└──────────────────┘             └──────────────────┘
```

---

## Resource-Based Policies vs IAM Policies

| Feature | Identity-based (IAM) | Resource-based |
|---------|----------------------|----------------|
| Attached to | User, Group, Role | S3 bucket, SQS, SNS, Lambda |
| Specifies | What the identity can do | Who can access the resource |
| Cross-account | Requires both sides | Only resource policy needed |

**Example:** Lambda function policy allowing API Gateway to invoke:

```json
{
  "Sid": "AllowAPIGatewayInvoke",
  "Effect": "Allow",
  "Principal": {"Service": "apigateway.amazonaws.com"},
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:us-east-1:123456789012:function:myFunction"
}
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Lambda needs S3 access | Attach IAM role with S3 permissions |
| Cross-account access | Use STS AssumeRole |
| Temporary credentials for external user | Use STS with IAM role |
| Least privilege not applied | Use IAM Access Analyzer |
| EC2 needs AWS credentials | Use IAM Role (not access keys) |
| Service needs permissions | Use service-linked role |

---

## Quick Quiz

1. What is the policy evaluation order?
2. When should you use a role vs. an access key?
3. What does STS AssumeRole do?
4. What is least privilege?

---

[← Containers](../01-development/10-containers.md) | [Back to Index](../../README.md) | [Next: Cognito →](02-cognito.md)
