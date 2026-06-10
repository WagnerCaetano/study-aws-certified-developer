# Troubleshooting & Optimization

> **Domain 4: Monitoring & Troubleshooting** | [← X-Ray](03-xray.md) | [Back to Index](../../README.md)

---

## Common Troubleshooting Scenarios

### Lambda Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| **Timeout** | Function runs too long | Increase timeout or optimize code |
| **Throttled** | Concurrent exec limit hit | Request limit increase or use SQS to buffer |
| **Permission denied** | Missing IAM permissions | Check execution role policies |
| **Cold start slow** | Large deployment package | Use Provisioned Concurrency, reduce package size |
| **Out of memory** | Memory too low | Increase memory (also increases CPU) |
| **Cannot connect to VPC** | Missing VPC config | Add VPC, subnet, security group settings |
| **Cannot reach internet** | Lambda in VPC without NAT | Add NAT Gateway or VPC endpoint |

### API Gateway Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| **403 Forbidden** | Auth failure or CORS | Check authorizer, enable CORS |
| **429 Too Many Requests** | Throttling | Increase rate limit or use caching |
| **502 Bad Gateway** | Lambda error | Check Lambda logs |
| **504 Timeout** | Lambda timeout | Increase Lambda timeout or API Gateway timeout |
| **CORS error** | Missing CORS headers | Enable CORS in API Gateway, add OPTIONS method |

### DynamoDB Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| **ProvisionedThroughputExceededException** | Exceeded RCUs/WCUs | Switch to on-demand or increase capacity |
| **ConditionalCheckFailedException** | Condition failed on write | Check your conditional expression logic |
| **Throttling** | Hot partition | Use better partition key design |
| **Slow queries** | Missing GSI | Create appropriate GSI |

### S3 Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| **AccessDenied** | Missing IAM/bucket policy | Check both IAM and bucket policies |
| **NoSuchBucket** | Wrong region or name | Verify bucket name and region |
| **BucketAlreadyExists** | Names are global | Choose a unique name |
| **Slow uploads** | Not using multipart | Use multipart upload for >5 MB files |

### SQS Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| **Messages not processed** | No consumers polling | Check Lambda event source mapping |
| **Duplicate processing** | At-least-once delivery | Make consumers idempotent |
| **Poison pill message** | Malformed message | Use DLQ for failed messages |
| **High age of oldest message** | Consumer too slow | Add more consumers or optimize |

---

## Performance Optimization

### Lambda Optimization
```python
# BAD: Initialize clients inside handler
def handler(event, context):
    s3 = boto3.client('s3')  # Created every invocation!
    s3.get_object(Bucket='bucket', Key='key')

# GOOD: Initialize outside handler
s3 = boto3.client('s3')  # Reused across invocations

def handler(event, context):
    s3.get_object(Bucket='bucket', Key='key')
```

### DynamoDB Optimization
- Use **Query** instead of **Scan** when possible
- Use **projection expressions** to get only needed attributes
- Use **DAX** for read-heavy workloads
- Use **batch operations** for multiple items

### S3 Optimization
- Use **S3 Transfer Acceleration** for global uploads
- Use **multipart upload** for files > 5 MB
- Use **S3 Select** to filter data server-side
- Use **CloudFront** for frequent reads

---

## Debugging Flow

```
1. CloudWatch Logs
   ├── Check Lambda function logs
   └── Check API Gateway access logs

2. CloudWatch Metrics
   ├── Check error rates
   ├── Check latency
   └── Check throttles

3. X-Ray Traces
   ├── Find slow segments
   ├── Find error segments
   └── View service map

4. CloudTrail Events
   ├── Check for permission errors
   └── Check for unexpected API calls
```

---

## Quick Diagnostic Commands

```bash
# Check Lambda function configuration
aws lambda get-function-configuration --function-name my-function

# Check recent Lambda invocations
aws logs filter-log-events --log-group-name /aws/lambda/my-function --limit 10

# Test API Gateway endpoint
curl -v https://api-id.execute-api.region.amazonaws.com/prod/path

# Check DynamoDB table status
aws dynamodb describe-table --table-name my-table

# List failed SQS messages in DLQ
aws sqs receive-message --queue-url https://sqs.region.amazonaws.com/account/dlq
```

---

[← X-Ray](03-xray.md) | [Back to Index](../../README.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3 study guides (5 files)
- [x] Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>