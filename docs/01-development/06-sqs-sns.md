# SQS, SNS & EventBridge

> **Domain 1: Development with AWS Services** | [← S3](05-s3.md) | [Back to Index](../../README.md) | [Next: Kinesis →](07-kinesis.md)

---

## Overview: Messaging Patterns

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Producer   │────►│   Message    │────►│   Consumer   │
│              │     │   Service    │     │              │
└──────────────┘     └──────────────┘     └──────────────┘

SQS:          Producer → Queue → Consumer (point-to-point)
SNS:          Producer → Topic → Subscribers (pub/sub)
EventBridge:  Producer → Bus → Rules → Targets (event routing)
```

---

## Amazon SQS (Simple Queue Service)

### Overview
- Fully managed **message queuing** service
- Decouples components in a microservices architecture
- **At-least-once** delivery (Standard) or **exactly-once** (FIFO)

### Queue Types

| Feature | Standard Queue | FIFO Queue |
|---------|---------------|------------|
| Delivery | At-least-once | Exactly-once |
| Ordering | Best-effort | **Guaranteed** (FIFO) |
| Throughput | Nearly unlimited | 300 TPS (per message group) |
| Deduplication | No | **Yes** (5 min window) |
| Queue name | Any | Must end in `.fifo` |

### Key Concepts

```
┌──────────────────────────────────────────────────────┐
│                    SQS Queue                          │
│                                                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ Msg 1   │ │ Msg 2   │ │ Msg 3   │ │ Msg 4   │  │
│  │ Visible │ │ Hidden  │ │ Visible │ │ Visible │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
│                   ▲                                  │
│            Visibility Timeout                       │
│         (msg being processed)                       │
└──────────────────────────────────────────────────────┘
```

### Visibility Timeout
- When a consumer receives a message, it becomes **invisible** to others
- Default: **30 seconds**
- Range: **0–12 hours**
- If message is not deleted within timeout, it becomes visible again
- **Important:** Set timeout > processing time to avoid duplicate processing

### Code Examples

```python
import boto3

sqs = boto3.resource('sqs')

# Create a queue
queue = sqs.create_queue(
    QueueName='my-queue',
    Attributes={'VisibilityTimeout': '120'}
)

# Create a FIFO queue
fifo_queue = sqs.create_queue(
    QueueName='my-queue.fifo',
    Attributes={
        'FifoQueue': 'true',
        'ContentBasedDeduplication': 'true'
    }
)

# Send a message
response = queue.send_message(
    MessageBody='Hello World',
    MessageAttributes={
        'Priority': {
            'StringValue': 'high',
            'DataType': 'String'
        }
    },
    DelaySeconds=10  # Optional delay
)

# Send message to FIFO queue
response = fifo_queue.send_message(
    MessageBody='Ordered message',
    MessageGroupId='group-1',  # Required for FIFO
    MessageDeduplicationId='unique-id-123'  # Optional if content-based dedup
)

# Receive messages
messages = queue.receive_messages(
    MaxNumberOfMessages=10,  # 1-10
    WaitTimeSeconds=20,      # Long polling
    VisibilityTimeout=60
)

# Process and delete
for message in messages:
    process(message.body)
    message.delete()  # Must delete after processing!

# Change visibility timeout
message.change_visibility(VisibilityTimeout=300)

# Purge queue (delete all messages)
queue.purge()
```

### Long Polling vs Short Polling

| Feature | Short Polling | Long Polling |
|---------|-------------|--------------|
| Returns | Immediately (even if empty) | Waits for messages up to timeout |
| Cost | More API calls | Fewer API calls |
| Recommended | No | **Yes** |
| `WaitTimeSeconds` | 0 | 1–20 |

**⚠️ Always use long polling** (`WaitTimeSeconds >= 1`) to reduce costs and improve response times.

### FIFO Queue Deduplication

```
Content-Based Deduplication:
  SQS uses SHA-256 hash of message body as dedup ID
  Duplicate messages within 5-min window are discarded

Explicit Deduplication ID:
  You provide MessageDeduplicationId
  Same ID within 5-min window → discarded
```

### Message Groups in FIFO

```
Queue: orders.fifo
├── Group: "customer-A" ──► Msg1, Msg2, Msg3 (ordered)
├── Group: "customer-B" ──► Msg4, Msg5 (ordered)
└── Group: "customer-C" ──► Msg6 (ordered)

Groups are processed in parallel, messages within group are ordered
```

### SQS Limits

| Limit | Value |
|-------|-------|
| Message size | **256 KB** (use S3 for larger) |
| Message retention | **1 minute – 14 days** (default 4 days) |
| Queue name length | Up to 80 characters |
| Batch size | Up to 10 messages |
| Delay delivery | Up to 15 minutes |

### SQS Extended Client Library

For messages > 256 KB:

```python
# Use S3 for payload, SQS for reference
# Extended Client Library handles this automatically

# 1. Large payload uploaded to S3
# 2. SQS message contains pointer to S3 object
# 3. Consumer downloads from S3 using pointer
```

---

## Amazon SNS (Simple Notification Service)

### Overview
- Fully managed **pub/sub messaging** service
- One message → Multiple subscribers (fanout)
- **Push-based** delivery (immediate push to subscribers)

### SNS Architecture

```
                    ┌──► SQS Queue 1
Producer ──► SNS ───┼──► SQS Queue 2 (Fanout pattern)
   Topic ───────────┼──► Lambda Function
                    ├──► HTTP/S Endpoint
                    ├──► Email
                    └──► SMS
```

### Topic Types
- **Standard** — Best-effort ordering, at-least-once delivery
- **FIFO** — Guaranteed ordering, exactly-once delivery (must end in `.fifo`)

### Code Examples

```python
import boto3
import json

sns = boto3.client('sns')

# Create topic
topic = sns.create_topic(Name='my-topic')

# Subscribe endpoints
sns.subscribe(
    TopicArn=topic['TopicArn'],
    Protocol='sqs',
    Endpoint='arn:aws:sqs:us-east-1:123456789012:my-queue'
)

sns.subscribe(
    TopicArn=topic['TopicArn'],
    Protocol='lambda',
    Endpoint='arn:aws:lambda:us-east-1:123456789012:function:processor'
)

sns.subscribe(
    TopicArn=topic['TopicArn'],
    Protocol='https',
    Endpoint='https://api.example.com/webhook'
)

# Publish message
sns.publish(
    TopicArn=topic['TopicArn'],
    Message=json.dumps({'event': 'order_created', 'orderId': '123'}),
    Subject='New Order',
    MessageAttributes={
        'eventType': {'DataType': 'String', 'StringValue': 'order'},
        'priority': {'DataType': 'Number', 'StringValue': '1'}
    }
)

# Direct message to phone
sns.publish(
    PhoneNumber='+15551234567',
    Message='Alert: Server down!'
)
```

### SNS + SQS Fanout Pattern

```
                ┌──► SNS ──► SQS Queue A ──► Lambda (process orders)
Order Service ──┤
                └──► SNS ──► SQS Queue B ──► Lambda (send notifications)

Both queues receive ALL messages independently
```

```python
# Subscribe SQS to SNS — ensure SQS policy allows SNS
sns.subscribe(
    TopicArn='arn:aws:sns:us-east-1:123456789012:orders',
    Protocol='sqs',
    Endpoint='arn:aws:sqs:us-east-1:123456789012:order-processing'
)
```

### SNS Message Filtering

```python
# Subscribe with filter policy
sns.subscribe(
    TopicArn='arn:aws:sns:us-east-1:123456789012:events',
    Protocol='sqs',
    Endpoint='arn:aws:sqs:us-east-1:123456789012:high-priority',
    Attributes={
        'FilterPolicy': json.dumps({
            'priority': [{'numeric': ['>=', 3]}],
            'eventType': ['order', 'payment']
        })
    }
)
```

### SNS Delivery Status

- Can log delivery status to CloudWatch Logs
- Supports: HTTP, Lambda, SQS, mobile push
- Track: success/failure, latency, retries

---

## Amazon EventBridge

### Overview
- **Serverless event bus** service
- Routes events between AWS services and your applications
- Built on CloudWatch Events (enhanced version)

### EventBridge Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Event      │────►│   Event      │────►│   Target      │
│   Source     │     │   Bus        │     │   (Lambda,    │
│ (AWS/service)│     │   + Rules    │     │    SQS, etc)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Event Buses

| Type | Description |
|------|-------------|
| **Default** | Your account's AWS events |
| **Custom** | Your custom events |
| **Partner** | SaaS partner events (Datadog, Auth0, etc.) |

### Event Structure

```json
{
    "version": "0",
    "id": "abc-123",
    "detail-type": "EC2 Instance State-change Notification",
    "source": "aws.ec2",
    "account": "123456789012",
    "time": "2024-01-15T10:30:00Z",
    "region": "us-east-1",
    "resources": ["arn:aws:ec2:us-east-1:123456789012:instance/i-123456"],
    "detail": {
        "instance-id": "i-123456",
        "state": "running"
    }
}
```

### Rules and Targets

```python
import boto3
import json

events = boto3.client('events')

# Create a rule matching specific events
events.put_rule(
    Name='ProcessOrders',
    EventPattern=json.dumps({
        "source": ["custom.myapp"],
        "detail-type": ["Order Created"],
        "detail": {
            "amount": [{"numeric": [">", 100]}]
        }
    })
)

# Add target (Lambda)
events.put_targets(
    Rule='ProcessOrders',
    Targets=[{
        'Id': '1',
        'Arn': 'arn:aws:lambda:us-east-1:123456789012:function:processOrder',
        'InputTransformer': {
            'InputPathsMap': {
                'orderId': '$.detail.orderId',
                'amount': '$.detail.amount'
            },
            'InputTemplate': '{"id": <orderId>, "total": <amount>}'
        }
    }]
)

# Put custom event
events.put_events(
    Entries=[{
        'Source': 'custom.myapp',
        'DetailType': 'Order Created',
        'Detail': json.dumps({
            'orderId': 'ORD-123',
            'amount': 150.00
        }),
        'EventBusName': 'custom-event-bus'
    }]
)
```

### Schedule Expressions

```python
# Cron-based schedule
events.put_rule(
    Name='DailyCleanup',
    ScheduleExpression='cron(0 2 * * ? *)',  # Every day at 2 AM UTC
)

# Rate-based schedule
events.put_rule(
    Name='Every5Minutes',
    ScheduleExpression='rate(5 minutes)'
)
```

### EventBridge vs SNS

| Feature | EventBridge | SNS |
|---------|-------------|-----|
| Pattern | Event routing (content-based) | Pub/sub (topic-based) |
| Filtering | Advanced JSON pattern matching | Simple attribute filtering |
| Schema | Schema registry available | No schema registry |
| Targets | 20+ AWS services | 6 protocols |
| Replay | **Yes** (archive & replay) | No |
| Transform | Input transformers | Raw delivery |
| Cross-account | **Yes** (resource policies) | Yes (cross-account) |

---

## Comparison: SQS vs SNS vs EventBridge

| Feature | SQS | SNS | EventBridge |
|---------|-----|-----|-------------|
| Pattern | Point-to-point | Pub/Sub | Event routing |
| Consumer pull/push | **Pull** | Push | Push |
| Persistence | **Yes** (retention up to 14 days) | No (delivers immediately) | Configurable |
| Filtering | No | Basic attributes | Advanced JSON patterns |
| Ordering | FIFO option | FIFO option | Per-source ordering |
| Replay | No | No | **Yes** |
| Use case | Task queues, decoupling | Fanout notifications | Event-driven architecture |

---

## Dead Letter Queues (DLQ)

```python
# Set DLQ for SQS
sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={
        'RedrivePolicy': json.dumps({
            'deadLetterTargetArn': dlq_arn,
            'maxReceiveCount': '5'  # After 5 receives, move to DLQ
        })
    }
)

# Set DLQ for Lambda (async invocations)
lambda_client.put_function_event_invoke_config(
    FunctionName='myFunction',
    MaximumRetryAttempts=2,
    DestinationConfig={
        'OnFailure': {
            'Destination': dlq_arn
        }
    }
)
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Decouple two services reliably | Use SQS between them |
| Send one message to multiple systems | Use SNS fanout to SQS queues |
| Need guaranteed message ordering | Use FIFO SQS queue |
| Filter events by content | Use EventBridge rules |
| Process messages > 256 KB | Use SQS Extended Client Library with S3 |
| Avoid duplicate processing | Use FIFO queue with deduplication |
| Need message persistence | Use SQS (SNS doesn't persist) |
| Fanout to multiple queues | SNS → multiple SQS subscriptions |
| Route events based on JSON content | Use EventBridge |
| Schedule periodic Lambda execution | Use EventBridge scheduled rules |
| Consumer needs time to process | Adjust Visibility Timeout |
| Reduce SQS API costs | Use Long Polling |

---

## Quick Quiz

1. What is the maximum message size in SQS?
2. What's the difference between Standard and FIFO queues?
3. How does the fanout pattern work with SNS and SQS?
4. When would you choose EventBridge over SNS?
5. What is a Dead Letter Queue and when is it used?

---

[← S3](05-s3.md) | [Back to Index](../../README.md) | [Next: Kinesis →](07-kinesis.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Create doc 01-aws-sdk.md
- [x] Create doc 02-lambda.md
- [x] Create doc 03-api-gateway.md
- [x] Create doc 04-dynamodb.md
- [x] Create doc 05-s3.md
- [x] Create doc 06-sqs-sns.md
- [ ] Create remaining Domain 1 study guides (4 files)
- [ ] Create Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>