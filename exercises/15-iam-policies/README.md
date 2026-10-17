# Exercise 15: IAM Policies

## Learning goals

- Author least-privilege IAM policies for Lambda accessing S3 and DynamoDB
- Detect wildcard actions and resources that violate least privilege
- Build a cross-account role trust policy

## Problem

Fix and create IAM policies in `starter.py` following least privilege.

The code should:

1. Scope S3 access to `GetObject` and `ListBucket` on the target bucket and objects
2. Scope DynamoDB actions to the table ARN (no `Resource: *`)
3. Use `sts:AssumeRole` in cross-account trust policies

## Exam tip

Identity-based policies attach to users, groups, and roles; resource-based policies attach to resources (S3 bucket policy, SNS topic policy). Prefer specific actions over `service:*` wildcards on the exam.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/15-iam-policies
python runner.py exercises/15-iam-policies --solution
```
