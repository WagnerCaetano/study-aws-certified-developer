# 🏋️ AWS Developer Exercises

> Hands-on practice scenarios to prepare for the AWS Certified Developer exam

---

## How to Use

Each exercise follows the **Exercism-style** format:
1. 📖 Read the problem description in the exercise `README.md`
2. 🔧 Implement or fix **`starter.py`** (intentionally incomplete or buggy)
3. ✅ Run tests via `runner.py` (defaults to `starter.py`)
4. 📎 Compare with **`solution.py`** when stuck (`--solution` runs the reference implementation)

Tests load the module named by the `EXERCISE_MODULE` environment variable (the runner sets this to `starter` or `solution`).

### Running Exercises

```bash
# Run a single exercise (tests starter.py)
python runner.py exercises/01-lambda-basics

# Validate the reference solution
python runner.py exercises/01-lambda-basics --solution

# Run all exercises in a domain (development, security, deployment, monitoring)
python runner.py --domain monitoring

# List available exercise folders
python runner.py --list

# Run all exercises
python runner.py --all

# Check your progress (starter passes recorded in .progress.json)
python runner.py --progress
```

---

## Exercise Categories

### 🔷 Domain 1: Development with AWS Services

| # | Exercise | Topic | Difficulty |
|---|----------|-------|------------|
| 01 | [Lambda Basics](01-lambda-basics/) | Lambda handler, event parsing | ⭐ |
| 02 | [Lambda Advanced](02-lambda-advanced/) | Environment variables, error handling | ⭐⭐ |
| 03 | [Lambda Performance](03-lambda-performance/) | Cold starts, optimization | ⭐⭐⭐ |
| 04 | [API Gateway Config](04-api-gateway/) | REST API, routing, CORS | ⭐⭐ |
| 05 | [DynamoDB Operations](05-dynamodb-ops/) | CRUD operations, queries | ⭐⭐ |
| 06 | [DynamoDB Design](06-dynamodb-design/) | Partition keys, GSIs | ⭐⭐⭐ |
| 07 | [S3 File Operations](07-s3-operations/) | Upload, download, presigned URLs | ⭐ |
| 08 | [S3 Security](08-s3-security/) | Bucket policies, encryption | ⭐⭐ |
| 09 | [SQS Messaging](09-sqs-messaging/) | Send, receive, delete messages | ⭐⭐ |
| 10 | [SNS Pub/Sub](10-sns-pubsub/) | Topics, subscriptions, filtering | ⭐⭐ |
| 11 | [Kinesis Streams](11-kinesis-streams/) | Producer, consumer patterns | ⭐⭐⭐ |
| 12 | [ElastiCache Patterns](12-elasticache/) | Caching, session store | ⭐⭐ |
| 13 | [Step Functions](13-step-functions/) | State machines, ASL | ⭐⭐⭐ |
| 14 | [ECS & Fargate](14-ecs-fargate/) | Task definitions, services | ⭐⭐⭐ |

### 🔷 Domain 2: Security

| # | Exercise | Topic | Difficulty |
|---|----------|-------|------------|
| 15 | [IAM Policies](15-iam-policies/) | Policy evaluation, least privilege | ⭐⭐ |
| 16 | [IAM Roles & STS](16-iam-roles/) | Assume role, cross-account | ⭐⭐⭐ |
| 17 | [Cognito Auth](17-cognito-auth/) | User pools, JWT tokens | ⭐⭐ |
| 18 | [KMS Encryption](18-kms-encryption/) | Encrypt, decrypt, envelope | ⭐⭐⭐ |
| 19 | [Secrets Management](19-secrets/) | Secrets Manager, Parameter Store | ⭐⭐ |
| 20 | [Security Review](20-security-review/) | Identify security issues | ⭐⭐⭐ |

### 🔷 Domain 3: Deployment

| # | Exercise | Topic | Difficulty |
|---|----------|-------|------------|
| 21 | [CloudFormation Basics](21-cfn-basics/) | Template structure, resources | ⭐⭐ |
| 22 | [CloudFormation Advanced](22-cfn-advanced/) | Intrinsic functions, outputs | ⭐⭐⭐ |
| 23 | [SAM Templates](23-sam-templates/) | Serverless app definition | ⭐⭐ |
| 24 | [CI/CD Pipeline](24-cicd-pipeline/) | CodePipeline, CodeBuild | ⭐⭐⭐ |
| 25 | [Elastic Beanstalk](25-elastic-beanstalk/) | Deployment, configuration | ⭐⭐ |
| 26 | [CDK Constructs](26-cdk-constructs/) | Infrastructure as code | ⭐⭐⭐ |

### 🔷 Domain 4: Monitoring & Troubleshooting

| # | Exercise | Topic | Difficulty |
|---|----------|-------|------------|
| 27 | [CloudWatch Logs](27-cloudwatch-logs/) | Log analysis, Insights | ⭐⭐ |
| 28 | [CloudWatch Alarms](28-cloudwatch-alarms/) | Metrics, alarms, dashboards | ⭐⭐ |
| 29 | [X-Ray Tracing](29-xray-tracing/) | Traces, service maps | ⭐⭐⭐ |
| 30 | [Troubleshooting](30-troubleshooting/) | Diagnose and fix issues | ⭐⭐⭐ |

### 🔷 Advanced Scenarios

Offline concept checks — hands-on LocalStack versions live under **[labs/](../labs/)**.

| # | Exercise | Topic | Lab | Difficulty |
|---|----------|-------|-----|------------|
| 31 | [Serverless API](31-serverless-api/) | API Gateway proxy patterns | [labs/01](../labs/01-serverless-api/) | ⭐⭐⭐ |
| 32 | [Event-Driven Architecture](32-event-driven/) | SNS + SQS fan-out concepts | [labs/02](../labs/02-event-driven/) | ⭐⭐⭐ |
| 33 | [Data Pipeline](33-data-pipeline/) | S3 → Lambda → DynamoDB concepts | [labs/03](../labs/03-async-pipeline/) | ⭐⭐⭐ |
| 34 | [Multi-Service Auth](34-multi-auth/) | Cognito / JWT concepts | [labs/04](../labs/04-secure-config/) (secure config) | ⭐⭐⭐ |
| 35 | [Deployment Pipeline](35-deploy-pipeline/) | CodeCommit → CodeBuild → CodeDeploy | — | ⭐⭐⭐ |

---

## Scoring

- ⭐ Beginner: Core concept understanding
- ⭐⭐ Intermediate: Real-world scenario application
- ⭐⭐⭐ Advanced: Complex multi-service scenarios

---

[Back to Main Index](../README.md)
