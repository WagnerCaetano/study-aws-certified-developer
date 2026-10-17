# Exercise 16: IAM Roles & STS

## Learning goals

- Write trust policies for AWS service principals (Lambda, ECS tasks)
- Grant `sts:AssumeRole` to assume a target role ARN
- Map STS `AssumeRole` credential fields to application-friendly keys

## Problem

Fix the STS AssumeRole and role configuration helpers in `starter.py`.

The code should:

1. Trust `lambda.amazonaws.com` and `ecs-tasks.amazonaws.com` (not EC2/ECS service names)
2. Keep `sts:AssumeRole` on the assume-role permission policy
3. Map `AccessKeyId`, `SecretAccessKey`, `SessionToken`, and `Expiration` to the expected output keys

## Exam tip

An IAM **role** has a trust policy (who can assume it) and permission policies (what it can do). Temporary credentials from STS always include a session token.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/16-iam-roles
python runner.py exercises/16-iam-roles --solution
```
