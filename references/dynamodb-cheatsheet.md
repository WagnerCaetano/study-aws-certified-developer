# DynamoDB Cheatsheet

Quick reference for Amazon DynamoDB on the DVA-C02 exam.

## Keys & access patterns

| Concept | Meaning |
|---------|---------|
| Partition key (PK / HASH) | Required; distributes data |
| Sort key (SK / RANGE) | Optional; enables Query ranges on same PK |
| Item | Up to **400 KB** |
| Primary key | PK alone or PK + SK |

## API operations

| API | Use when |
|-----|----------|
| `GetItem` | Exact primary key |
| `PutItem` | Insert / overwrite item |
| `UpdateItem` | Partial update; conditional writes |
| `DeleteItem` | Remove by key |
| `Query` | Same PK (+ optional SK condition); can use indexes |
| `Scan` | Full table/index; avoid in hot paths |
| `BatchGetItem` | Up to 100 items / 16 MB |
| `BatchWriteItem` | Up to 25 Put/Delete |
| `TransactWriteItems` | All-or-nothing (up to 100 actions) |
| `TransactGetItems` | Consistent multi-item read |

## Indexes

| Index | Notes |
|-------|-------|
| LSI | Same PK, different SK; created with table; shares capacity |
| GSI | Alternate PK/SK; eventually consistent; own RCU/WCU (or on-demand) |
| Projection | `KEYS_ONLY`, `INCLUDE`, `ALL` |

## Capacity & consistency

| Mode | Notes |
|------|-------|
| Provisioned | Set RCU/WCU; auto-scaling optional |
| On-demand | Pay per request; spikes OK |
| Eventually consistent read | Default; 0.5 RCU per 4 KB |
| Strongly consistent read | 1 RCU per 4 KB; not on GSI |
| Write | 1 WCU per 1 KB |

## Streams & TTL

| Feature | Exam point |
|---------|------------|
| DynamoDB Streams | Ordered change log per shard; Lambda event source |
| TTL | Attribute epoch seconds; deletes are eventually removed; appear in Streams |

## Common patterns

| Pattern | Approach |
|---------|----------|
| 1:N relationship | PK = parent, SK = child id / type |
| Many access patterns | Single-table design + GSIs |
| Idempotent writes | Conditional expression (`attribute_not_exists`) |
| Optimistic locking | Version attribute + condition |

## Related

- Chapter: [dev-04-dynamodb.md](../chapters/dev-04-dynamodb.md)
- Exercises: [05-dynamodb-ops](../exercises/05-dynamodb-ops/), [06-dynamodb-design](../exercises/06-dynamodb-design/)
