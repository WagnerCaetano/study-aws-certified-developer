# Exercise 12: ElastiCache Patterns

## Learning goals

- Implement **lazy loading** (cache-aside): read cache before the database
- Implement **write-through**: update cache and database on writes
- Use TTL-backed keys to limit stale data

## Problem

Implement the caching patterns in `starter.py` using the provided `SimpleCache`.

The code should:

1. On read, return a cache hit without querying the mock database
2. On write, persist to both the mock database and the cache under `user:{id}`

## Exam tip

Lazy loading avoids writing cache on every DB read but can stampede on expiry; write-through keeps cache warm but adds write latency. ElastiCache Redis supports TTL; Memcached is simpler but lacks persistence features Redis offers.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/12-elasticache
python runner.py exercises/12-elasticache --solution
```
