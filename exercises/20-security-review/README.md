# Exercise 20: Security Review

## Learning goals

- Spot common Lambda misconfigurations (long-lived access keys, secrets in environment variables)
- Review S3 settings: encryption, versioning, and public access
- Check API Gateway for authorization, throttling, and WAF
- Produce a secure Lambda configuration baseline

## Problem

Fix the security review helpers in `starter.py` so they flag risky settings and emit a safe Lambda template.

Review functions should detect access keys, secrets in env vars, missing S3 encryption, public buckets, and missing API authorization. The secure template must use Secrets Manager, forbid access keys, and avoid passwords in environment variables.

## Exam tip

On DVA-C02, **IAM roles** (not access keys) grant AWS service access from Lambda, ECS, and EC2. Prefer **Secrets Manager** or **SSM Parameter Store** over environment variables for credentials. Enable **S3 encryption** and **Block Public Access** by default.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/20-security-review
python runner.py exercises/20-security-review --solution
```
