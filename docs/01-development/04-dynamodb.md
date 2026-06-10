# Amazon DynamoDB

> **Domain 1: Development with AWS Services** | [← API Gateway](03-api-gateway.md) | [Back to Index](../../README.md) | [Next: S3 →](05-s3.md)

---

## Overview

Amazon DynamoDB is a fully managed **NoSQL database** service that provides fast, predictable performance with seamless scalability.

### Key Characteristics
- **Key-value and document** data model
- **Single-digit millisecond** latency at any scale
- **Auto-scaling** — Automatically adjusts throughput capacity
- **Fully managed** — No servers to manage, patch, or upgrade
- **Durable** — Data replicated across 3 AZs

---

## Core Concepts

### Table Structure

```
┌────────────────────────────────────────────────────────────┐
│                    Table: Users                             │
├──────────┬──────────────┬──────────┬───────────────────────┤
│ userId   │ email (GSI)  │  name    │ createdAt             │
│ (PK)     │              │          │                       │
├──────────┼──────────────┼──────────┼───────────────────────┤
│ "usr001" │ "john@..."  │ "John"   │ "2024-01-15"          │
│ "usr002" │ "jane@..."  │ "Jane"   │ "2024-01-16"          │
└──────────┴──────────────┴──────────┴───────────────────────┘
     ▲
  Partition Key (required)
```

### Key Types

| Key Type | Description | Example |
|----------|-------------|---------|
| **Partition Key (PK)** | Required. Determines physical partition. | `userId` |
| **Partition Key + Sort Key** | PK + SK allows multiple items per partition | `userId` + `orderId` |
| **Composite Key** | Together, PK+SK uniquely identify an item | `userId=GSI1`, `orderId=ORD001` |

### How Partition Key Works

```
hash(PK) % N_partitions → Physical Partition

Example: hash("usr001") % 5 → Partition 3
         hash("usr002") % 5 → Partition 1
```

**⚠️ Choose a partition key with high cardinality** to avoid hot partitions!

---

## Data Types

| Category | Types | Description |
|----------|-------|-------------|
| **Scalar** | S, N, B, BOOL, NULL | String, Number, Binary, Boolean, Null |
| **Document** | M, L | Map (object), List (array) |
| **Set** | SS, NS, BS | Set of Strings, Numbers, or Binaries |

### Example Item (Python)

```python
{
    'userId': 'usr001',              # S (String)
    'age': 30,                       # N (Number)
    'active': True,                  # BOOL
    'address': {                     # M (Map)
        'street': '123 Main St',
        'city': 'Seattle'
    },
    'tags': ['admin', 'premium'],    # L (List)
    'phoneNumbers': {'555-1234', '555-5678'},  # SS (String Set)
    'metadata': None                 # NULL
}
```

---

## Read/Write Capacity Modes

### Provisioned (Default)

```
┌─────────────────────────────────────────────┐
│  Provisioned Throughput                     │
│  ├── Read Capacity Units (RCU)              │
│  └── Write Capacity Units (WCU)             │
│  + Optional Auto Scaling                    │
└─────────────────────────────────────────────┘
```

| Operation | Capacity Consumed |
|-----------|------------------|
| 1 Strong Consistent Read of 4 KB | **1 RCU** |
| 1 Eventually Consistent Read of 4 KB | **0.5 RCU** |
| 1 Transactional Read of 4 KB | **2 RCU** |
| 1 Write of 1 KB | **1 WCU** |
| 1 Transactional Write of 1 KB | **2 WCU** |

**RCU Calculation Examples:**
```
Item size: 20 KB
Eventually Consistent Read:
  → ceil(20/4) × 0.5 = 5 × 0.5 = 2.5 → 3 RCU

Strongly Consistent Read:
  → ceil(20/4) × 1 = 5 × 1 = 5 RCU
```

**WCU Calculation Examples:**
```
Item size: 15 KB
Standard Write:
  → ceil(15/1) = 15 WCU

Transactional Write:
  → ceil(15/1) × 2 = 30 WCU
```

### On-Demand

- No capacity planning needed
- Pay per request
- Instantly accommodates workloads as they ramp up/down
- **2.5x more expensive** than provisioned (at baseline)
- Good for: unpredictable workloads, new applications

---

## Query vs Scan

### Query

```python
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

# Query by partition key
response = table.query(
    KeyConditionExpression='userId = :uid',
    ExpressionAttributeValues={
        ':uid': 'usr001'
    }
)

# Query with sort key condition
response = table.query(
    KeyConditionExpression='userId = :uid AND orderId > :oid',
    ExpressionAttributeValues={
        ':uid': 'usr001',
        ':oid': 'ORD100'
    }
)

# Query with filter (applied AFTER the read)
response = table.query(
    KeyConditionExpression='userId = :uid',
    FilterExpression='status = :s',
    ExpressionAttributeValues={
        ':uid': 'usr001',
        ':s': 'COMPLETED'
    }
)
```

**⚠️ FilterExpression reduces results but NOT consumed capacity!**

### Scan

```python
# Scan entire table (expensive!)
response = table.scan()

# Scan with filter
response = table.scan(
    FilterExpression='age > :min_age',
    ExpressionAttributeValues={
        ':min_age': 25
    }
)

# Parallel scan for large tables
response = table.scan(
    Segment=0,
    TotalSegments=4
)
```

| Feature | Query | Scan |
|---------|-------|------|
| Efficiency | **High** (uses key) | **Low** (reads entire table) |
| Input | PK required (+ optional SK) | No key required |
| Filter | After key selection | After full scan |
| Use | Targeted data retrieval | Full table operations |

---

## Indexes

### Local Secondary Index (LSI)

```
Table: PK=userId, SK=orderId
  └── LSI: PK=userId, SK=createdAt (alternative sort key)

  Must be defined at table creation time!
  Max 5 LSIs per table
  Shares RCU/WCU with the table
  Max item projection: 10 GB per partition
```

### Global Secondary Index (GSI)

```
Table: PK=userId, SK=orderId
  └── GSI: PK=email, SK=createdAt (different PK + SK)

  Can be added after table creation!
  Max 20 GSIs per table
  Has its own RCU/WCU (separate from table)
  Can project attributes (ALL, KEYS_ONLY, INCLUDE)
```

| Feature | LSI | GSI |
|---------|-----|-----|
| Key | Same PK, different SK | Different PK and/or SK |
| When created | **Table creation only** | **Any time** |
| Capacity | Shares table's RCU/WCU | **Own capacity** |
| Max per table | 5 | 20 |
| Projection | ALL, KEYS_ONLY, INCLUDE | ALL, KEYS_ONLY, INCLUDE |

**⚠️ GSI reads are eventually consistent by default. Strong consistency is NOT supported on GSIs.**

### GSI Example

```python
# Create table with GSI
table = dynamodb.create_table(
    TableName='Users',
    KeySchema=[
        {'AttributeName': 'userId', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'userId', 'AttributeType': 'S'},
        {'AttributeName': 'email', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST',
    GlobalSecondaryIndexes=[{
        'IndexName': 'EmailIndex',
        'KeySchema': [
            {'AttributeName': 'email', 'KeyType': 'HASH'}
        ],
        'Projection': {'ProjectionType': 'ALL'},
    }]
)

# Query the GSI
response = table.query(
    IndexName='EmailIndex',
    KeyConditionExpression='email = :email',
    ExpressionAttributeValues={':email': 'john@example.com'}
)
```

---

## Conditional Operations

```python
# Only put item if it doesn't exist
table.put_item(
    Item={'userId': 'usr001', 'name': 'John'},
    ConditionExpression='attribute_not_exists(userId)'
)

# Only update if condition is met
table.update_item(
    Key={'userId': 'usr001'},
    UpdateExpression='SET age = :new_age',
    ConditionExpression='age < :max_age',
    ExpressionAttributeValues={
        ':new_age': 31,
        ':max_age': 100
    }
)

# Atomic counter
table.update_item(
    Key={'userId': 'usr001'},
    UpdateExpression='SET loginCount = loginCount + :inc',
    ExpressionAttributeValues={':inc': 1}
)
```

---

## Transactions

```python
# TransactWriteItems — ACID for up to 100 items
dynamodb.transact_write_items(
    TransactItems=[
        {
            'Update': {
                'TableName': 'Accounts',
                'Key': {'accountId': {'S': 'acc001'}},
                'UpdateExpression': 'SET balance = balance - :amount',
                'ConditionExpression': 'balance >= :amount',
                'ExpressionAttributeValues': {':amount': {'N': '100'}}
            }
        },
        {
            'Update': {
                'TableName': 'Accounts',
                'Key': {'accountId': {'S': 'acc002'}},
                'UpdateExpression': 'SET balance = balance + :amount',
                'ExpressionAttributeValues': {':amount': {'N': '100'}}
            }
        }
    ]
)

# TransactReadItems — read up to 100 items consistently
dynamodb.transact_get_items(
    TransactItems=[
        {'Get': {'TableName': 'Users', 'Key': {'userId': {'S': 'usr001'}}}},
        {'Get': {'TableName': 'Users', 'Key': {'userId': {'S': 'usr002'}}}}
    ]
)
```

**Transaction Limits:**
- Up to **100 items** per transaction
- Up to **4 MB** per transaction
- Transactional writes consume **2x WCU**
- Transactional reads consume **2x RCU**

---

## DynamoDB Streams

```
Table ──► Streams ──► Lambda/EC2/KCL
                    (24-hour retention)
```

| Stream View Type | What's captured |
|-----------------|----------------|
| KEYS_ONLY | Only the key attributes |
| NEW_IMAGE | Entire item after modification |
| OLD_IMAGE | Entire item before modification |
| NEW_AND_OLD_IMAGES | Both before and after |

```python
# Lambda processing DynamoDB Stream
def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            new_item = record['dynamodb']['NewImage']
            process_new_item(new_item)
        elif record['eventName'] == 'MODIFY':
            old = record['dynamodb']['OldImage']
            new = record['dynamodb']['NewImage']
            process_update(old, new)
```

---

## DynamoDB API Operations (boto3)

```python
# Put item (create or replace)
table.put_item(Item={'userId': 'usr001', 'name': 'John'})

# Get item
response = table.get_item(Key={'userId': 'usr001'})

# Update item
table.update_item(
    Key={'userId': 'usr001'},
    UpdateExpression='SET #n = :name',
    ExpressionAttributeNames={'#n': 'name'},
    ExpressionAttributeValues={':name': 'John Updated'}
)

# Delete item
table.delete_item(Key={'userId': 'usr001'})

# Batch write (up to 25 items)
dynamodb.batch_write_item(
    RequestItems={
        'Users': [
            {'PutRequest': {'Item': {'userId': 'usr001', 'name': 'John'}}},
            {'PutRequest': {'Item': {'userId': 'usr002', 'name': 'Jane'}}}
        ]
    }
)

# Batch get (up to 100 items)
response = dynamodb.batch_get_item(
    RequestItems={
        'Users': {
            'Keys': [
                {'userId': 'usr001'},
                {'userId': 'usr002'}
            ]
        }
    }
)
```

---

## Query Operators for Sort Key

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal | `orderId = :id` |
| `<` | Less than | `orderId < :id` |
| `<=` | Less than or equal | `orderId <= :id` |
| `>` | Greater than | `orderId > :id` |
| `>=` | Greater than or equal | `orderId >= :id` |
| `BETWEEN` | Range | `orderId BETWEEN :a AND :b` |
| `begins_with` | Prefix match | `begins_with(orderId, :prefix)` |

---

## Consistency Models

| Type | Description | RCU Cost |
|------|-------------|----------|
| **Eventually Consistent** | May return stale data (within ~1 sec) | 0.5 RCU per 4 KB |
| **Strongly Consistent** | Returns most up-to-date data | 1 RCU per 4 KB |
| **Transactional** | ACID-compliant, serializable | 2 RCU per 4 KB |

```python
# Strongly consistent read
response = table.get_item(
    Key={'userId': 'usr001'},
    ConsistentRead=True
)

# Eventually consistent read (default)
response = table.get_item(
    Key={'userId': 'usr001'}
)
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Need to query by different attribute | Create a GSI |
| Need alternative sort key on same partition | Create an LSI |
| Atomic increment/decrement | Use `UpdateExpression` with `SET count = count + :val` |
| Prevent duplicate inserts | Use `ConditionExpression='attribute_not_exists(PK)'` |
| ACID across multiple items | Use `TransactWriteItems` |
| Need to process changes in real-time | Enable DynamoDB Streams + Lambda |
| Hot partition problem | Choose high-cardinality partition key |
| Large scan operation | Use Parallel Scan |
| Filter reduces results but not cost | FilterExpression applied AFTER read |
| Access patterns need different keys | Design GSIs for each access pattern |

---

## Quick Quiz

1. How many RCUs for a strongly consistent read of a 12 KB item?
2. What's the difference between Query and Scan?
3. When must an LSI be created?
4. What are the limitations of GSI consistency?
5. How do atomic counters work in DynamoDB?

---

[← API Gateway](03-api-gateway.md) | [Back to Index](../../README.md) | [Next: S3 →](05-s3.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Create doc 01-aws-sdk.md
- [x] Create doc 02-lambda.md
- [x] Create doc 03-api-gateway.md
- [x] Create doc 04-dynamodb.md
- [ ] Create remaining Domain 1 study guides (6 files)
- [ ] Create Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>