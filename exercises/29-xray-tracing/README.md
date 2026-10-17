# Exercise 29: X-Ray Tracing

## Learning goals

- Define X-Ray **sampling rules** (priority, fixed rate, reservoir, path/method filters)
- Distinguish traces, segments, and subsegments from document shape
- Build annotation filter expressions for trace search
- Enable tracing on Lambda, API Gateway, and ECS workloads

## Problem

Fix the X-Ray helpers in `starter.py`.

1. **`build_sampling_rule`**: Honor the `fixed_rate` argument (do not hard-code `0.0`).
2. **`identify_trace_component`**: Documents with `trace_id` / `TraceId` are **traces**; documents with `subsegments` are **segments**.
3. **`build_annotation_search`**: Filter expression must use the `annotation.<key>` prefix.
4. **`recommend_tracing_config`**: For Lambda, return **`ActiveTracing`: True** (and a default sampling rule).

## Exam tip

Lambda active tracing sends segments to X-Ray automatically when enabled on the function. Sampling rules control cost—lower priority numbers run first; fixed rate applies after the reservoir is consumed.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/29-xray-tracing
python runner.py exercises/29-xray-tracing --solution
```
