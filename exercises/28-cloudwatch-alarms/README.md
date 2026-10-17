# Exercise 28: CloudWatch Alarms

## Learning goals

- Build `PutMetricAlarm`-style configurations (threshold, period, statistic, evaluation periods)
- Wire SNS topics to `AlarmActions` and `OKActions` for notifications
- Choose operational responses based on metric severity
- Model dashboard widgets for multi-service visibility

## Problem

Fix the helpers in `starter.py` so they match CloudWatch alarm best practices.

1. **`build_alarm_config`**: Use the requested `period` and `statistic` defaults (`300`, `Sum`). When `sns_topic_arn` is set, attach it to both **`AlarmActions`** and **`OKActions`**.
2. **`recommend_alarm_action`**: For error-style metrics (`Errors`, `5XXError`, `Throttles`) with threshold exceeded, recommend **Page on-call immediately**.
3. **`build_dashboard_metrics`**: Create one metric widget per service name in the input list.

## Exam tip

CloudWatch alarms evaluate metrics over **periods** × **evaluation periods**. Use **Sum** or **Average** appropriately (e.g., Lambda errors often use Sum over 5 minutes). Pair alarms with SNS for paging and auto scaling for capacity metrics.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/28-cloudwatch-alarms
python runner.py exercises/28-cloudwatch-alarms --solution
```
