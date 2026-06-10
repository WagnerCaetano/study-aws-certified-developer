# Amazon S3 for Developers

> **Domain 1: Development with AWS Services** | [← DynamoDB](04-dynamodb.md) | [Back to Index](../../README.md) | [Next: SQS, SNS & EventBridge →](06-sqs-sns.md)

---

## Overview

Amazon S3 (Simple Storage Service) is an object storage service offering industry-leading scalability, data availability, security, and performance.

### Key Characteristics
- **Unlimited storage** — Store any amount of data
- **Objects up to 5 TB** — Single object size limit
- **99.999999999% (11 9s) durability**
- **99.99% availability**
- **Buckets** — Containers for objects (globally unique names)
- **Objects** — Files + metadata (key, value, version, etc.)

---

## S3 Architecture

```
┌────────────────────────────────────────────────────┐
│  Bucket: my-app-assets                             │
│  ├── uploads/                                      │
│  │   ├── images/photo.jpg   ← Key: uploads/images/ │
│  │   └── docs/report.pdf                           │
│  ├── config/                                       │
│  │   └── settings.json                             │
│  └── index.html                                    │
│                                                    │
│  Each Object:                                      │
│  ├── Key (name/path)                               │
│  ├── Value (data, up to 5 TB)                      │
│  ├── Version ID                                    │
│  ├── Metadata (user + system)                      │
│  └── ACLs / Policies                               │
└────────────────────────────────────────────────────┘
```

---

## S3 Storage Classes

| Storage Class | Use Case | Access Frequency | Cost |
|--------------|----------|-----------------|------|
| **S3 Standard** | General purpose | Frequent | Base |
| **S3 Intelligent-Tiering** | Unknown/changing | Auto-optimized | Auto |
| **S3 Standard-IA** | Long-lived, infrequent | < monthly | Lower storage, higher retrieval |
| **S3 One Zone-IA** | Infrequent, re-creatable | < monthly | Lowest storage |
| **S3 Glacier Instant** | Archive, rare access | Few/year | Very low |
| **S3 Glacier Flexible** | Archive | 1-2x/year | Minimal |
| **S3 Glacier Deep Archive** | Long-term archive | 1-2x/year | Absolute minimum |

### Lifecycle Rules

```json
{
    "Rules": [
        {
            "ID": "MoveToIA",
            "Status": "Enabled",
            "Transition": {
                "Days": 90,
                "StorageClass": "STANDARD_IA"
            }
        },
        {
            "ID": "MoveToGlacier",
            "Status": "Enabled",
            "Transition": {
                "Days": 365,
                "StorageClass": "GLACIER"
            }
        },
        {
            "ID": "DeleteOldVersions",
            "Status": "Enabled",
            "NoncurrentVersionExpiration": {
                "NoncurrentDays": 30
            }
        }
    ]
}
```

---

## S3 Security

### 1. Bucket Policies (Resource-based)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::123456789012:role/LambdaRole"},
            "Action": ["s3:GetObject", "s3:PutObject"],
            "Resource": "arn:aws:s3:::my-bucket/*"
        }
    ]
}
```

### 2. Access Control Lists (ACLs)

- Legacy (not recommended)
- Can control at object level
- Bucket policies are preferred

### 3. IAM Policies (Identity-based)

```json
{
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": "arn:aws:s3:::my-bucket/*"
}
```

### 4. Block Public Access

- Account-level and bucket-level settings
- **Always enable** unless you need public access
- Overrides bucket policies and ACLs

### 5. Pre-signed URLs

```python
import boto3

s3 = boto3.client('s3')

# Generate a pre-signed URL for download (valid for 1 hour)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'private-file.pdf'},
    ExpiresIn=3600
)

# Generate a pre-signed URL for upload
url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket': 'my-bucket', 'Key': 'uploads/new-file.pdf'},
    ExpiresIn=3600
)
```

**⚠️ Pre-signed URLs use the credentials of the person who generated them.**

### 6. S3 Object Lambda

- Transform objects on-the-fly during retrieval
- Use cases: redacting PII, converting formats, watermarking images

---

## S3 Encryption

### Encryption at Rest

| Method | Key Management | Description |
|--------|---------------|-------------|
| **SSE-S3** | AWS manages | Default encryption. Uses AES-256 |
| **SSE-KMS** | AWS KMS | You control key policy. Audit via CloudTrail |
| **SSE-C** | Customer provides | You manage keys, AWS uses them |

### Encryption in Transit

- Use HTTPS (TLS) for all S3 operations
- Bucket policy can enforce HTTPS:

```json
{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": "arn:aws:s3:::my-bucket/*",
    "Condition": {
        "Bool": {"aws:SecureTransport": "false"}
    }
}
```

---

## S3 Versioning

```
Bucket: my-bucket (versioning enabled)

file.txt (v1) → "Hello"     ← DELETE adds delete marker
file.txt (v2) → "World"     ← Latest version
file.txt (v3) → "Updated"   ← Can roll back to any version
```

- Once enabled, **cannot be disabled** (only suspended)
- Delete marker is a "soft delete"
- Permanently delete: specify version ID
- Protects against accidental deletes
- Required for **Cross-Region Replication**

---

## S3 Event Notifications

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  S3      │────►│  SNS / SQS   │────►│  Lambda      │
│  Event   │     │  EventBridge │     │  Processing  │
└──────────┘     └──────────────┘     └──────────────┘
```

### Event Types
- `s3:ObjectCreated:*`
- `s3:ObjectRemoved:*`
- `s3:ObjectRestore:*`
- `s3:Replication:*`

### Supported Destinations
1. **SNS** — Simple notifications
2. **SQS** — Queue-based processing
3. **Lambda** — Direct function invocation
4. **EventBridge** — Advanced event routing

```python
# S3 event in Lambda
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        size = record['s3']['object']['size']
        print(f"New object: s3://{bucket}/{key} ({size} bytes)")
```

---

## S3 Multipart Upload

For files > 100 MB, use multipart upload (required for > 5 GB):

```python
import boto3

s3 = boto3.client('s3')

# Upload large file with multipart
s3.upload_file(
    'large-file.zip',
    'my-bucket',
    'uploads/large-file.zip',
    Config=boto3.s3.transfer.TransferConfig(
        multipart_threshold=8388608,  # 8 MB
        max_concurrency=10,
        multipart_chunksize=8388608
    )
)
```

**Multipart upload limits:**
- Min part size: **5 MB** (except last part)
- Max part size: **5 GB**
- Max number of parts: **10,000**
- Max object size: **5 TB**

---

## S3 Select

Retrieve only a subset of data using SQL-like queries:

```python
response = s3.select_object_content(
    Bucket='my-bucket',
    Key='data/users.csv',
    ExpressionType='SQL',
    Expression="SELECT * FROM s3object s WHERE s.age > '25'",
    InputSerialization={'CSV': {}},
    OutputSerialization={'CSV': {}}
)
```

- Reduces data transfer and processing time
- Works with CSV, JSON, Parquet
- Can use GZIP compression

---

## Cross-Origin Resource Sharing (CORS)

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT"],
        "AllowedOrigins": ["https://myapp.com"],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3600
    }
]
```

---

## S3 Performance Optimization

| Technique | Description |
|-----------|-------------|
| **Multi-part upload** | Parallel uploads for large files |
| **S3 Transfer Acceleration** | Uses CloudFront edge locations |
| **S3 Byte-Range Fetches** | Parallel downloads of specific ranges |
| **Prefix optimization** | Use different prefixes for parallel reads |
| **S3 Select** | Server-side filtering |

### Prefix Performance
```
Good:     my-bucket/prefix1/, my-bucket/prefix2/ (different prefixes)
Bad:      my-bucket/all-in-one-prefix/ (single prefix, limited scaling)
```

S3 supports **3,500 PUT/COPY/POST/DELETE** and **5,500 GET** requests per second per prefix.

---

## Common Developer Operations (boto3)

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# Download file
s3.download_file('my-bucket', 'remote.txt', 'local.txt')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket', Prefix='uploads/')
for obj in response.get('Contents', []):
    print(obj['Key'], obj['Size'])

# Copy object
s3.copy_object(
    Bucket='dest-bucket',
    Key='copy.txt',
    CopySource={'Bucket': 'src-bucket', 'Key': 'original.txt'}
)

# Delete objects
s3.delete_objects(
    Bucket='my-bucket',
    Delete={'Objects': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]}
)

# Get object metadata (without downloading)
response = s3.head_object(Bucket='my-bucket', Key='file.txt')
print(response['ContentType'], response['ContentLength'])
```

---

## Static Website Hosting

```
Bucket: my-website
├── index.html      ← Index document
├── error.html      ← Error document
├── css/
│   └── style.css
└── js/
    └── app.js

Endpoint: http://my-website.s3-website-us-east-1.amazonaws.com
```

**For HTTPS:** Use CloudFront in front of S3.

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Temporarily share private file | Generate pre-signed URL |
| Encrypt with customer-managed keys | Use SSE-KMS |
| Reduce S3 costs over time | Use Lifecycle rules |
| Process uploads in real-time | S3 Events → Lambda/SQS |
| Upload large files efficiently | Use Multipart Upload |
| Need version control of objects | Enable Versioning |
| Browser can't load S3 resources | Configure CORS |
| Enforce HTTPS-only access | Bucket policy with `aws:SecureTransport` |
| Query subset of data | Use S3 Select |
| Replicate bucket to another region | Cross-Region Replication |

---

## Quick Quiz

1. What are the three server-side encryption options?
2. What is a pre-signed URL and when would you use it?
3. How do you enforce HTTPS for S3 access?
4. What is the maximum object size in S3?
5. How do lifecycle rules help optimize costs?

---

[← DynamoDB](04-dynamodb.md) | [Back to Index](../../README.md) | [Next: SQS, SNS & EventBridge →](06-sqs-sns.md)
