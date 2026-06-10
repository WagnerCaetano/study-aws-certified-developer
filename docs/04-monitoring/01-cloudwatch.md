# Amazon CloudWatch

> **Domain 4: Monitoring & Troubleshooting** | [← CDK](../03-deployment/05-cdk.md) | [Back to Index](../../README.md) | [Next: CloudTrail →](02-cloudtrail.md)

---

## Overview

Amazon CloudWatch is a monitoring and observability service for AWS resources and applications.

### Key Features
- **Metrics** — Collect and track performance data
- **Logs** — Collect, monitor, and analyze logs
- **Alarms** — Trigger notifications or actions based on metrics
- **Dashboards** — Visualize metrics and logs
- **Events/EventBridge** — React to state changes in AWS resources

---

## CloudWatch Metrics

### Namespace, Metric, Dimension

```
Namespace: AWS/Lambda
  └── Metric: Duration
       └── Dimension: FunctionName = "my-function"
```

### Key Metrics by Service

| Service | Key Metrics |
|---------|------------|
| **Lambda** | Duration, Invocations, Errors, Throttles, ConcurrentExecutions |
| **API Gateway** | Count, Latency, 4XXError, 5XXError |
| **DynamoDB** | ConsumedReadCapacityUnits, ConsumedWriteCapacityUnits, ThrottledRequests |
| **SQS** | NumberOfMessagesSent, ApproximateNumberOfMessagesVisible, AgeOfOldestMessage |
| **S3** | BucketSizeBytes, NumberOfObjects, AllRequests, GetRequests, PutRequests |
| **ECS** | CPUUtilization, MemoryUtilization, RunningTaskCount |

### Custom Metrics

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Put custom metric
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'OrdersProcessed',
            'Value': 42,
            'Unit': 'Count',
            'Dimensions': [
                {'Name': 'Environment', 'Value': 'production'}
            ]
        }
    ]
)

# Using Embedded Metric Format (EMF) in Lambda
import json

def lambda_handler(event, context):
    # Do work...
    order_count = 42
    
    # Emit metric via structured log
    print(json.dumps({
        "_aws": {
            "CloudWatchMetrics": [{
                "Namespace": "MyApp",
                "Dimensions": [["Environment"]],
                "Metrics": [{"Name": "OrdersProcessed", "Unit": "Count"}]
            }],
            "Timestamp": int(time.time() * 1000)
        },
        "Environment": "production",
        "OrdersProcessed": order_count,
        "message": "Orders processed successfully"
    }))
```

---

## CloudWatch Logs

### Log Groups and Streams

```
Log Group: /aws/lambda/my-function
  ├── Log Stream: 2024/01/15/[$LATEST]abc123
  ├── Log Stream: 2024/01/15/[$LATEST]def456
  └── Log Stream: 2024/01/16/[$LATEST]ghi789
```

### Lambda Logging (Python)

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Processing event: %s", json.dumps(event))
    logger.error("Something went wrong!")
    logger.warning("This is a warning")
```

### Log Insights (Query Language)

```
# Find Lambda errors in last hour
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20

# Calculate average Lambda duration
stats avg(@duration) as avgDuration
| bin(1h)

# Find slow requests (>1 second)
filter @duration > 1000
| stats count() as slowRequests by bin(5m)
```

### Metric Filters

```python
# Create metric filter from logs
logs = boto3.client('logs')

logs.put_metric_filter(
    logGroupName='/aws/lambda/my-function',
    filterName='ErrorCount',
    filterPattern='ERROR',
    metricTransformations=[{
        'metricName': 'LambdaErrors',
        'metricNamespace': 'MyApp',
        'metricValue': '1'
    }]
)
```

---

## CloudWatch Alarms

```python
cloudwatch.put_metric_alarm(
    AlarmName='HighErrorRate',
    AlarmDescription='Lambda error rate > 5%',
    MetricName='Errors',
    Namespace='AWS/Lambda',
    Statistic='Sum',
    Period=300,       # 5 minutes
    EvaluationPeriods=1,
    Threshold=5,
    ComparisonOperator='GreaterThanThreshold',
    Dimensions=[{'Name': 'FunctionName', 'Value': 'my-function'}],
    AlarmActions=['arn:aws:sns:us-east-1:123456789012:alerts'],
    OKActions=['arn:aws:sns:us-east-1:123456789012:alerts']
)
```

---

## CloudWatch EventBridge

### Scheduled Events (Cron)

```python
events = boto3.client('events')

# Schedule Lambda to run daily at 9 AM UTC
events.put_rule(
    Name='DailyReportTrigger',
    ScheduleExpression='cron(0 9 * * ? *)',
    State='ENABLED'
)

# Lambda event pattern
events.put_rule(
    Name='S3ObjectCreated',
    EventPattern=json.dumps({
        "source": ["aws.s3"],
        "detail-type": ["AWS API Call via CloudTrail"],
        "detail": {
            "eventSource": ["s3.amazonaws.com"],
            "eventName": ["PutObject"]
        }
    })
)
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Monitor Lambda errors | CloudWatch Metrics + Alarms |
| Search through logs | CloudWatch Logs Insights |
| Extract metrics from logs | Use Metric Filters |
| Schedule Lambda execution | EventBridge scheduled rule |
| React to S3 events | EventBridge event pattern |
| Visualize application metrics | CloudWatch Dashboards |
| Custom application metrics | `put_metric_data` or Embedded Metric Format |
| Alert on high error rate | CloudWatch Alarm + SNS notification |

---

[← CDK](../03-deployment/05-cdk.md) | [Back to Index](../../README.md) | [Next: CloudTrail →](02-cloudtrail.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3 study guides (5 files)
- [x] Domain 4: 01-cloudwatch.md
- [ ] Domain 4: 02-cloudtrail.md, 03-xray.md, 04-troubleshooting.md
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>