# AWS Certified Developer - Associate (DVA-C02) Study Book

Interactive study path for the AWS Certified Developer – Associate exam: chapters, 35 hands-on exercises, multi-service LocalStack labs, and practice exams.

## Exam overview

| | |
|---|---|
| **Exam code** | DVA-C02 |
| **Format** | 65 questions (50 scored + 15 unscored) |
| **Time** | 120 minutes |
| **Passing score** | 720 / 1000 |

### Domain weights

| Domain | Weight | Description |
|--------|--------|-------------|
| Domain 1 | 32% | Development with AWS Services |
| Domain 2 | 26% | Security |
| Domain 3 | 24% | Deployment |
| Domain 4 | 18% | Troubleshooting and Optimization |

## Quick start

1. Follow **[setup.md](setup.md)** (Python 3.11+, Docker, LocalStack, env vars).
2. Install deps: `pip install -r requirements.txt`
3. List exercises: `python runner.py --list`
4. Work an exercise (edit `starter.py`, then run tests):

```bash
python runner.py exercises/01-lambda-basics
python runner.py exercises/01-lambda-basics --solution   # validate answer key
python runner.py labs/01-serverless-api                 # needs LocalStack
```

## Chapters

### Domain 1: Development with AWS Services (32%)

| # | Topic | Chapter |
|---|-------|---------|
| 1 | AWS SDK & CLI | [dev-01-aws-sdk.md](chapters/dev-01-aws-sdk.md) |
| 2 | AWS Lambda | [dev-02-lambda.md](chapters/dev-02-lambda.md) |
| 3 | API Gateway | [dev-03-api-gateway.md](chapters/dev-03-api-gateway.md) |
| 4 | DynamoDB | [dev-04-dynamodb.md](chapters/dev-04-dynamodb.md) |
| 5 | S3 | [dev-05-s3.md](chapters/dev-05-s3.md) |
| 6 | SQS, SNS & EventBridge | [dev-06-sqs-sns.md](chapters/dev-06-sqs-sns.md) |
| 7 | Kinesis | [dev-07-kinesis.md](chapters/dev-07-kinesis.md) |
| 8 | ElastiCache | [dev-08-elasticache.md](chapters/dev-08-elasticache.md) |
| 9 | Step Functions | [dev-09-step-functions.md](chapters/dev-09-step-functions.md) |
| 10 | Containers (ECS / ECR / Fargate) | [dev-10-containers.md](chapters/dev-10-containers.md) |

### Domain 2: Security (26%)

| # | Topic | Chapter |
|---|-------|---------|
| 11 | IAM | [sec-01-iam.md](chapters/sec-01-iam.md) |
| 12 | Cognito | [sec-02-cognito.md](chapters/sec-02-cognito.md) |
| 13 | KMS & encryption | [sec-03-kms.md](chapters/sec-03-kms.md) |
| 14 | Secrets Manager & SSM | [sec-04-secrets.md](chapters/sec-04-secrets.md) |
| 15 | Security best practices | [sec-05-security-best-practices.md](chapters/sec-05-security-best-practices.md) |

### Domain 3: Deployment (24%)

| # | Topic | Chapter |
|---|-------|---------|
| 16 | CloudFormation | [dep-01-cloudformation.md](chapters/dep-01-cloudformation.md) |
| 17 | SAM | [dep-02-sam.md](chapters/dep-02-sam.md) |
| 18 | CI/CD (CodeCommit, CodeBuild, CodePipeline, CodeDeploy) | [dep-03-cicd.md](chapters/dep-03-cicd.md) |
| 19 | Elastic Beanstalk | [dep-04-elastic-beanstalk.md](chapters/dep-04-elastic-beanstalk.md) |
| 20 | CDK | [dep-05-cdk.md](chapters/dep-05-cdk.md) |

### Domain 4: Troubleshooting and Optimization (18%)

| # | Topic | Chapter |
|---|-------|---------|
| 21 | CloudWatch | [mon-01-cloudwatch.md](chapters/mon-01-cloudwatch.md) |
| 22 | CloudTrail | [mon-02-cloudtrail.md](chapters/mon-02-cloudtrail.md) |
| 23 | X-Ray | [mon-03-xray.md](chapters/mon-03-xray.md) |
| 24 | Troubleshooting & optimization | [mon-04-troubleshooting.md](chapters/mon-04-troubleshooting.md) |

## Exercises (35)

Each exercise folder has:

| File | Role |
|------|------|
| `starter.py` | Broken / incomplete — **you edit this** |
| `solution.py` | Correct answer key |
| `test.py` | Asserts against the module under test |
| `README.md` | Goals, exam tip, how to run |

```bash
python runner.py --list
python runner.py --all
python runner.py --progress
python runner.py --domain development
python runner.py --domain security
python runner.py --domain deployment
python runner.py --domain monitoring
python runner.py exercises/01-lambda-basics
python runner.py exercises/01-lambda-basics --solution
python runner.py labs/01-serverless-api
python runner.py labs/01-serverless-api --solution
```

Progress for **starter** passes is saved in `.progress.json` (gitignored).

Full catalog: **[exercises/README.md](exercises/README.md)** · Multi-service labs: **[labs/README.md](labs/README.md)**

### Chapter ↔ exercise index

| Chapter | Exercises |
|---------|-----------|
| [dev-01](chapters/dev-01-aws-sdk.md) / [dev-02](chapters/dev-02-lambda.md) | 01–03 |
| [dev-03](chapters/dev-03-api-gateway.md) | 04 |
| [dev-04](chapters/dev-04-dynamodb.md) | 05–06 |
| [dev-05](chapters/dev-05-s3.md) | 07–08 |
| [dev-06](chapters/dev-06-sqs-sns.md) | 09–10 |
| [dev-07](chapters/dev-07-kinesis.md) | 11 |
| [dev-08](chapters/dev-08-elasticache.md) | 12 |
| [dev-09](chapters/dev-09-step-functions.md) | 13 |
| [dev-10](chapters/dev-10-containers.md) | 14 |
| [sec-01](chapters/sec-01-iam.md) | 15–16 |
| [sec-02](chapters/sec-02-cognito.md) | 17 |
| [sec-03](chapters/sec-03-kms.md) | 18 |
| [sec-04](chapters/sec-04-secrets.md) | 19 |
| [sec-05](chapters/sec-05-security-best-practices.md) | 20 |
| [dep-01](chapters/dep-01-cloudformation.md) | 21–22 |
| [dep-02](chapters/dep-02-sam.md) | 23 |
| [dep-03](chapters/dep-03-cicd.md) | 24, 35 |
| [dep-04](chapters/dep-04-elastic-beanstalk.md) | 25 |
| [dep-05](chapters/dep-05-cdk.md) | 26 |
| [mon-01](chapters/mon-01-cloudwatch.md) | 27–28 |
| [mon-03](chapters/mon-03-xray.md) | 29 |
| [mon-04](chapters/mon-04-troubleshooting.md) | 30 |
| Multi-service (advanced) | 31–34 (offline) → [labs/](labs/) |

## Multi-service labs

LocalStack end-to-end scenarios (requires `docker compose up -d`):

| Lab | Pattern |
|-----|---------|
| [01-serverless-api](labs/01-serverless-api/) | API Gateway + Lambda + DynamoDB |
| [02-event-driven](labs/02-event-driven/) | SNS → SQS → Lambda + filter policy |
| [03-async-pipeline](labs/03-async-pipeline/) | S3 → Lambda → DynamoDB |
| [04-secure-config](labs/04-secure-config/) | Secrets Manager / SSM + KMS |

Details: **[labs/README.md](labs/README.md)**

## Quick Reference

| Sheet | Link |
|-------|------|
| Lambda limits | [references/lambda-limits.md](references/lambda-limits.md) |
| DynamoDB | [references/dynamodb-cheatsheet.md](references/dynamodb-cheatsheet.md) |
| API Gateway | [references/api-gateway-cheatsheet.md](references/api-gateway-cheatsheet.md) |
| Messaging (SQS / SNS / EventBridge) | [references/messaging-comparison.md](references/messaging-comparison.md) |

## Practice exams

| Exam | Link |
|------|------|
| Practice Exam 1 | [exams/exam-01.md](exams/exam-01.md) |
| Practice Exam 2 | [exams/exam-02.md](exams/exam-02.md) |
| Practice Exam 3 | [exams/exam-03.md](exams/exam-03.md) |
| Practice Exam 4 | [exams/exam-04.md](exams/exam-04.md) |
| Practice Exam 5 | [exams/exam-05.md](exams/exam-05.md) |

More: **[exams/README.md](exams/README.md)**

## 6-week study path

| Week | Focus | Chapters | Exercises / labs |
|------|-------|----------|------------------|
| 1 | Development core | [dev-01](chapters/dev-01-aws-sdk.md)–[dev-05](chapters/dev-05-s3.md) | 01–08 |
| 2 | Messaging & compute patterns | [dev-06](chapters/dev-06-sqs-sns.md)–[dev-10](chapters/dev-10-containers.md) | 09–14 |
| 3 | Security | [sec-01](chapters/sec-01-iam.md)–[sec-05](chapters/sec-05-security-best-practices.md) | 15–20 + [lab 04](labs/04-secure-config/) |
| 4 | Deployment | [dep-01](chapters/dep-01-cloudformation.md)–[dep-05](chapters/dep-05-cdk.md) | 21–26, 35 |
| 5 | Monitoring & advanced | [mon-01](chapters/mon-01-cloudwatch.md)–[mon-04](chapters/mon-04-troubleshooting.md) | 27–34 + [labs 01–03](labs/) |
| 6 | Practice exams | Review weak chapters | All 5 exams + redo failed starters |

After exercises 31–34 (offline concept checks), run the matching multi-service labs under **[labs/](labs/)**.

## Repo layout

```
chapters/          Study notes by domain
exercises/         35 starter / solution / test exercises
labs/              Multi-service LocalStack scenarios
exams/             Practice exams
references/        Exam quick sheets
common/            Shared LocalStack boto3 helpers
runner.py          Exercise + lab CLI
docker-compose.yml LocalStack
setup.md           Environment setup
```
