# Amazon Kinesis

> **Domain 1: Development with AWS Services** | [← SQS/SNS](06-sqs-sns.md) | [Back to Index](../../README.md) | [Next: ElastiCache →](08-elasticache.md)

---

## Overview

Amazon Kinesis is a platform for **real-time processing** of streaming data at massive scale.

### Kinesis Services

| Service | Purpose |
|---------|---------|
| **Kinesis Data Streams** | Real-time data streaming |
| **Kinesis Data Firehose** | Data delivery to S3/Redshift/ES/etc. |
| **Kinesis Data Analytics** | SQL-based stream processing |
| **Kinesis Video Streams** | Video stream processing |

---

## Kinesis Data Streams

### Architecture

```
┌──────────┐     ┌──────────────────┐     ┌──────────────┐
│ Producers │────►│ Kinesis Data     │────►│ Consumers    │
│ (App,    │     │ Stream (Shards)  │     │ (Lambda,     │
│  IoT,   │     │                  │     │  KCL, Kinesis │
│  Lambda)│     │  Retention:      │     │  Analytics)  │
└──────────┘     │  1-365 days      │     └──────────────┘
                 └──────────────────┘
```

### Shards

- A stream is composed of **1 or more shards**
- Each shard provides:
  - **1 MB/s** data input
  - **1,000 records/s** data input
  - **2 MB/s** data output
- You can **increase or decrease** the number of shards (resharding)

### Data Flow

```
┌───────────────┐
│   Producer     │
│   PutRecord()  │────► Partition Key
│   PutRecords() │────► Hash of key → Shard assignment
└───────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  Stream: my-stream                │
│  ├── Shard 1: records with hash   │
│  ├── Shard 2: records with hash   │
│  └── Shard 3: records with hash   │
└───────────────────────────────────┘
        │
        ▼
┌───────────────┐
│   Consumer     │
│   GetRecords() │
└───────────────┘
```

### Code Examples

```python
import boto3

kinesis = boto3.client('kinesis')

# Put a single record
response = kinesis.put_record(
    StreamName='my-stream',
    Data=b'{"event": "page_view", "page": "/home"}',
    PartitionKey='user-123'  # Determines shard
)

# Put multiple records (batch)
response = kinesis.put_records(
    StreamName='my-stream',
    Records=[
        {'Data': b'event1', 'PartitionKey': 'key1'},
        {'Data': b'event2', 'PartitionKey': 'key2'},
    ]
)

# Get records (consumer)
response = kinesis.get_records(
    ShardIterator=shard_iterator,
    Limit=100
)
for record in response['Records']:
    data = record['Data'].decode('utf-8')
    print(data)
```

### Kinesis Client Library (KCL)

- Helps consume Kinesis streams
- Manages shard leasing and checkpointing
- Each worker instance handles one or more shards
- Supports DynamoDB for coordination

### Lambda with Kinesis

```python
def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded
        import base64
        data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        partition_key = record['kinesis']['partitionKey']
        sequence_number = record['kinesis']['sequenceNumber']
        process_event(data)
```

---

## Kinesis Data Firehose

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Producer  │────►│  Firehose    │────►│  S3 / OpenSearch│
│           │     │  (Auto-scale)│     │  / Redshift    │
└──────────┘     │  Transform:  │     │  / Splunk      │
                 │  Lambda      │     └────────────────┘
                 └──────────────┘
```

- **Fully managed** — No shards to manage
- **Auto-scales** based on throughput
- **Lambda transformation** — Modify records before delivery
- **Batching** — Groups records by size (1 MB) or time (60-900 seconds)
- **Data conversion** — JSON → Parquet/ORC for S3

```python
firehose = boto3.client('firehose')

# Create delivery stream to S3
firehose.create_delivery_stream(
    DeliveryStreamName='my-delivery-stream',
    DeliveryStreamType='DirectPut',
    S3DestinationConfiguration={
        'BucketARN': 'arn:aws:s3:::my-bucket',
        'RoleARN': 'arn:aws:iam::123456789012:role/firehose-role',
        'Prefix': 'firehose/',
        'BufferingHints': {'SizeInMBs': 64, 'IntervalInSeconds': 60}
    }
)

# Put record
firehose.put_record(
    DeliveryStreamName='my-delivery-stream',
    Record={'Data': b'{"event": "click", "user": "123"}'}
)
```

---

## Kinesis vs SQS

| Feature | Kinesis Data Streams | SQS |
|---------|---------------------|-----|
| Purpose | Real-time streaming | Message queuing |
| Retention | 1-365 days | 1-14 days |
| Replay | **Yes** | No |
| Consumers | Multiple (shared) | One per message |
| Ordering | Per shard | FIFO queue |
| Data size | 1 MB max | 256 KB max |
| Processing | Real-time analytics | Task processing |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Real-time data processing | Use Kinesis Data Streams |
| Deliver streaming data to S3 | Use Kinesis Firehose |
| Process clickstream data | Kinesis Streams + Lambda |
| Need to replay data | Kinesis (SQS cannot replay) |
| Transform data before S3 | Firehose + Lambda transformation |

---

## Quick Quiz

1. What is a shard in Kinesis Data Streams?
2. How does Kinesis Firehose differ from Kinesis Data Streams?
3. Can you replay data in SQS? What about Kinesis?
4. What are the throughput limits per shard?

---

[← SQS/SNS](06-sqs-sns.md) | [Back to Index](../../README.md) | [Next: ElastiCache →](08-elasticache.md)
