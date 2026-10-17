# Exercise 06: DynamoDB Table Design

## Learning goals

- Model single-table access patterns with partition and sort keys
- Add a GSI when query patterns need an alternate partition key
- Choose on-demand (`PAY_PER_REQUEST`) billing for variable workloads

## Problem

Design DynamoDB table definitions in `starter.py` for these access patterns:

1. **Users** — look up a user by `userId` (partition key only)
2. **Orders** — fetch all orders for a `userId`, sorted by `orderDate` (composite key)
3. **Orders by status** — extend the orders table with a GSI named `ByStatus` keyed by `status` (HASH) and `orderDate` (RANGE), projecting all attributes
4. Use **PAY_PER_REQUEST** billing on the user table (and keep orders on on-demand as well)

## Exam tip

Design tables **from access patterns**, not entities: every GSI key must support a real query path, and each GSI partition key value should be **high cardinality** to avoid hot partitions.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/06-dynamodb-design
python runner.py exercises/06-dynamodb-design --solution
```
