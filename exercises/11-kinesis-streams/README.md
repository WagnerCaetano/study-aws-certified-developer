# Exercise 11: Kinesis Streams

## Learning goals

- Build `PutRecord` requests with partition keys and UTF-8 encoded data
- Decode base64 Kinesis records in Lambda event sources
- Size shard count from required ingest throughput (1 MB/s per shard)

## Problem

Fix the Kinesis producer and consumer helpers in `starter.py`.

The code should:

1. Use `PartitionKey` and encode string `Data` as bytes
2. Base64-decode the `data` field before parsing JSON in Lambda events
3. Return at least one shard (`max(1, …)`) for fractional throughput

## Exam tip

Kinesis Data Streams charges per shard-hour and per PUT payload unit (25 KB). Hot keys on a single partition key limit throughput to one shard’s capacity even if you provision more shards.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/11-kinesis-streams
python runner.py exercises/11-kinesis-streams --solution
```
