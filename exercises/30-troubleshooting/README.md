# Exercise 30: Troubleshooting

## Learning goals

- Map Lambda symptoms (VPC, throttling, permissions, cold starts) to likely fixes
- Interpret API Gateway HTTP status codes (403 CORS vs auth, 502/504 backend timeouts)
- Match DynamoDB exception types to remediation steps

## Problem

Fix the diagnostic helpers in `starter.py` so each symptom returns the specific guidance expected by the tests (not generic “check logs” for every case).

Cover at least:

- Lambda in **VPC without NAT** when external calls time out
- **Throttling** → concurrency limits or SQS buffering
- API **502** → backend/Lambda errors; **403 + CORS** → enable CORS and OPTIONS
- DynamoDB **throughput exceeded** and **conditional check failed** messages

## Exam tip

502/504 from API Gateway usually mean the integration (Lambda) failed or timed out—check Lambda logs and timeout settings (REST API integration max 29s). VPC Lambdas need NAT Gateway or VPC endpoints for AWS APIs and the internet.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/30-troubleshooting
python runner.py exercises/30-troubleshooting --solution
```
