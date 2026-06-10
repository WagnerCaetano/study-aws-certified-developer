# Amazon ElastiCache

> **Domain 1: Development with AWS Services** | [← Kinesis](07-kinesis.md) | [Back to Index](../../README.md) | [Next: Step Functions →](09-step-functions.md)

---

## Overview

Amazon ElastiCache is a fully managed **in-memory caching** service that supports Redis and Memcached.

### Why Caching?
- **Reduce database load** — Serve frequent reads from cache
- **Lower latency** — Sub-millisecond response times
- **Session storage** — Store user sessions
- **Leaderboards** — Redis sorted sets
- **Rate limiting** — Track request counts

---

## Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data structures | Strings, Lists, Sets, Sorted Sets, Hashes | Strings only |
| Multi-AZ | **Yes** (with replication) | No |
| Persistence | **Yes** (snapshot/AOF) | No |
| Replication | **Yes** (read replicas) | No |
| Clustering | **Yes** (sharding) | Yes (partitioning) |
| Pub/Sub | **Yes** | No |
| Auth | **Yes** (Redis AUTH) | No |
| Sorted Sets | **Yes** | No |
| Use case | Complex caching, sessions, leaderboards | Simple key-value caching |

---

## ElastiCache Patterns

### 1. Lazy Loading (Cache-Aside)

```
┌────────┐    1. Get     ┌────────┐
│  App   │──────────────►│ Cache  │
│        │◄──────────────│        │
└────────┘   2. Miss     └────────┘
     │
     │ 3. Get from DB
     ▼
┌────────┐    4. Write   ┌────────┐
│  DB    │──────────────►│ Cache  │
└────────┘               └────────┘
```

```python
import boto3
import json

# Pseudo-code for lazy loading pattern
def get_user(user_id):
    # 1. Try cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. Cache miss — get from database
    user = dynamodb.get_item(Key={'userId': user_id})
    
    # 3. Write to cache
    cache.set(f"user:{user_id}", json.dumps(user), ttl=3600)
    
    return user
```

### 2. Write-Through

```
┌────────┐   1. Write   ┌────────┐
│  App   │──────────────►│ Cache  │
│        │──────────────►│ DB     │
└────────┘   2. Write   └────────┘
```

```python
def save_user(user_id, user_data):
    # Write to both cache and DB
    cache.set(f"user:{user_id}", json.dumps(user_data))
    dynamodb.put_item(Item=user_data)
```

### 3. TTL (Time-to-Live)

```python
# Set cache with 1-hour TTL
cache.set("session:abc123", session_data, ttl=3600)

# Redis automatically removes expired keys
```

---

## ElastiCache for Redis Use Cases

### Session Store
```python
# Store session
session_id = "sess_abc123"
cache.hmset(f"session:{session_id}", {
    "user_id": "usr001",
    "role": "admin",
    "last_activity": "2024-01-15T10:30:00Z"
})
cache.expire(f"session:{session_id}", 1800)  # 30 min TTL

# Retrieve session
session = cache.hgetall(f"session:{session_id}")
```

### Leaderboard
```python
# Add score
cache.zadd("leaderboard:daily", {"player_1": 1500, "player_2": 2000})

# Get top 10
top_10 = cache.zrevrange("leaderboard:daily", 0, 9, withscores=True)

# Get player rank
rank = cache.zrevrank("leaderboard:daily", "player_1")
```

### Rate Limiting
```python
import time

def check_rate_limit(user_id, limit=100, window=60):
    key = f"rate_limit:{user_id}"
    current = cache.incr(key)
    if current == 1:
        cache.expire(key, window)
    return current <= limit
```

---

## Redis Cluster Modes

### Cluster Mode Disabled
- Single shard with up to 5 read replicas
- All data in one node (partition)
- Good for: Simple caching, session storage

### Cluster Mode Enabled
- Up to 500 shards (nodes)
- Data partitioned across shards
- Good for: Large datasets, high throughput

---

## Connecting from Lambda/EC2

```python
import redis

# Connect to ElastiCache Redis
r = redis.Redis(
    host='my-cluster.xxxxxx.use1.cache.amazonaws.com',
    port=6379,
    decode_responses=True
)

# Basic operations
r.set('key', 'value')
value = r.get('key')
r.delete('key')

# With TTL
r.setex('session:abc', 3600, 'user_data')
```

**⚠️ Lambda must be in the same VPC as ElastiCache.** ElastiCache is a VPC-only service.

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Reduce DynamoDB read load | Use ElastiCache as read-through cache |
| Need session storage | Use Redis with TTL |
| Real-time leaderboard | Use Redis Sorted Sets |
| Cache invalidation | Use TTL or write-through pattern |
| Need pub/sub messaging | Use Redis pub/sub |
| Need data persistence | Use Redis (not Memcached) |
| Multi-AZ failover | Use Redis with Multi-AZ |
| Lambda can't connect to cache | Ensure Lambda is in same VPC |

---

## Quick Quiz

1. When would you choose Redis over Memcached?
2. What is the lazy loading pattern?
3. How do you handle cache invalidation?
4. What Redis data structure would you use for a leaderboard?

---

[← Kinesis](07-kinesis.md) | [Back to Index](../../README.md) | [Next: Step Functions →](09-step-functions.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Create doc 01-aws-sdk.md
- [x] Create doc 02-lambda.md
- [x] Create doc 03-api-gateway.md
- [x] Create doc 04-dynamodb.md
- [x] Create doc 05-s3.md
- [x] Create doc 06-sqs-sns.md
- [x] Create doc 07-kinesis.md
- [x] Create doc 08-elasticache.md
- [ ] Create doc 09-step-functions.md
- [ ] Create doc 10-containers.md
- [ ] Create Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>