# Exercise 27: CloudWatch Logs

## Learning goals

- Build CloudWatch Logs Insights queries with `filter`, `stats`, `sort`, and `limit` (pipe-separated)
- Define metric filters with `filterPattern` and `metricTransformations`
- Name log groups using the `/aws/{service}/{name}` convention

## Problem

Fix the CloudWatch Logs helpers in `starter.py`.

Insights queries should join stages with newline-pipe (`\n| `). Metric filters must use `filterPattern` and transformation fields `metricName`, `metricNamespace`, and `metricValue`. Lambda log groups live at `/aws/lambda/{function-name}`.

## Exam tip

**Logs Insights** is for ad hoc analysis; **metric filters** turn log patterns into CloudWatch metrics for alarms. Lambda automatically writes to `/aws/lambda/<function>`—know retention and encryption settings for compliance questions.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/27-cloudwatch-logs
python runner.py exercises/27-cloudwatch-logs --solution
```
