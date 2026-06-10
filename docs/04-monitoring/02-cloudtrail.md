# AWS CloudTrail

> **Domain 4: Monitoring & Troubleshooting** | [← CloudWatch](01-cloudwatch.md) | [Back to Index](../../README.md) | [Next: X-Ray →](03-xray.md)

---

## Overview

AWS CloudTrail records **API calls** made in your AWS account — who did what, when, and from where.

### What CloudTrail Logs

```
Who: IAM user/role identity
What: API action (e.g., s3:GetObject)
When: Timestamp
Where: Source IP, user agent
Which: Resource affected
Result: Success or error code
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Trail** | Configuration for logging API calls |
| **Event** | Single API call record |
| **Event History** | 90 days of management events (free) |
| **Management Events** | Control plane operations (create/delete resources) |
| **Data Events** | Data plane operations (S3 GetObject, Lambda Invoke) |
| **Insights** | Unusual API activity detection |

---

## Trail Configuration

### Management vs Data Events

| Type | Examples | Default Logged |
|------|----------|---------------|
| **Management** | CreateBucket, DeleteFunction, PutBucketPolicy | ✅ Yes |
| **Data** | GetObject, PutObject, Lambda Invoke | ❌ No (must enable) |
| **Insights** | Unusual spike in `TerminateInstance` calls | ❌ No (must enable) |

### Multi-Region Trail

- **Recommended:** Create a trail that applies to all regions
- Log to a **single S3 bucket** for centralized logging
- Can send to **CloudWatch Logs** for querying with Logs Insights

---

## CloudTrail Log Example

```json
{
  "eventVersion": "1.08",
  "userIdentity": {
    "type": "AssumedRole",
    "principalId": "ABCDEF:my-session",
    "arn": "arn:aws:sts::123456789012:assumed-role/MyRole/my-session",
    "accountId": "123456789012"
  },
  "eventTime": "2024-01-15T10:30:00Z",
  "eventSource": "s3.amazonaws.com",
  "eventName": "GetObject",
  "awsRegion": "us-east-1",
  "sourceIPAddress": "203.0.113.1",
  "userAgent": "aws-sdk-python/1.34.0",
  "requestParameters": {
    "bucketName": "my-bucket",
    "key": "data/file.csv"
  },
  "responseElements": null,
  "eventID": "abc123-def456",
  "readOnly": true,
  "eventType": "AwsApiCall"
}
```

---

## CloudTrail with CloudWatch Logs

```python
# Query CloudTrail events in CloudWatch Logs Insights
fields @timestamp, eventName, userIdentity.arn, sourceIPAddress
| filter eventSource = "s3.amazonaws.com"
| filter eventName = "DeleteBucket"
| sort @timestamp desc
| limit 50
```

---

## Security Use Cases

| Use Case | How |
|----------|-----|
| **Audit** | Who deleted a resource? Check CloudTrail |
| **Compliance** | Track all IAM changes |
| **Security investigation** | Find unauthorized API calls |
| **Operational troubleshooting** | Find failed API calls |
| **Data events** | Track who accessed sensitive S3 objects |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Find who deleted an S3 bucket | Query CloudTrail event history |
| Track all IAM changes | Enable CloudTrail management events |
| Log S3 object-level access | Enable data events for S3 |
| Unusual API activity detected | Enable CloudTrail Insights |
| Retain logs > 90 days | Create a Trail logging to S3 |
| Query API call history | CloudTrail + CloudWatch Logs Insights |

---

[← CloudWatch](01-cloudwatch.md) | [Back to Index](../../README.md) | [Next: X-Ray →](03-xray.md)
