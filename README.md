# AWS Certified Developer - Associate (DVA-C02) Study Book

> A comprehensive, interactive study guide for the AWS Certified Developer - Associate certification exam.

---

## 🎯 Exam Overview

- **Exam Code:** DVA-C02
- **Format:** 65 questions (50 scored + 15 unscored)
- **Time:** 120 minutes
- **Question Types:** Multiple choice, Multiple response
- **Passing Score:** 720/1000
- **Cost:** $150 USD

### Domain Weights

| Domain | Weight | Description |
|--------|--------|-------------|
| Domain 1 | 32% | Development with AWS Services |
| Domain 2 | 26% | Security |
| Domain 3 | 24% | Deployment |
| Domain 4 | 18% | Troubleshooting and Optimization |

---

## 📚 Study Guides

### Domain 1: Development with AWS Services (32%)

| # | Topic | Link |
|---|-------|------|
| 1 | AWS SDK & CLI Overview | [📖 Study](docs/01-development/01-aws-sdk.md) |
| 2 | AWS Lambda Deep Dive | [📖 Study](docs/01-development/02-lambda.md) |
| 3 | Amazon API Gateway | [📖 Study](docs/01-development/03-api-gateway.md) |
| 4 | Amazon DynamoDB | [📖 Study](docs/01-development/04-dynamodb.md) |
| 5 | Amazon S3 for Developers | [📖 Study](docs/01-development/05-s3.md) |
| 6 | SQS, SNS & EventBridge | [📖 Study](docs/01-development/06-sqs-sns.md) |
| 7 | Amazon Kinesis | [📖 Study](docs/01-development/07-kinesis.md) |
| 8 | Amazon ElastiCache | [📖 Study](docs/01-development/08-elasticache.md) |
| 9 | AWS Step Functions | [📖 Study](docs/01-development/09-step-functions.md) |
| 10 | Containers: ECS, ECR & Fargate | [📖 Study](docs/01-development/10-containers.md) |

### Domain 2: Security (26%)

| # | Topic | Link |
|---|-------|------|
| 11 | IAM for Developers | [📖 Study](docs/02-security/01-iam.md) |
| 12 | Amazon Cognito | [📖 Study](docs/02-security/02-cognito.md) |
| 13 | AWS KMS & Encryption | [📖 Study](docs/02-security/03-kms.md) |
| 14 | AWS Secrets Manager & SSM Parameter Store | [📖 Study](docs/02-security/04-secrets.md) |
| 15 | Security Best Practices | [📖 Study](docs/02-security/05-security-best-practices.md) |

### Domain 3: Deployment (24%)

| # | Topic | Link |
|---|-------|------|
| 16 | AWS CloudFormation | [📖 Study](docs/03-deployment/01-cloudformation.md) |
| 17 | AWS Elastic Beanstalk | [📖 Study](docs/03-deployment/02-elastic-beanstalk.md) |
| 18 | AWS CodePipeline (CI/CD) | [📖 Study](docs/03-deployment/03-codepipeline.md) |
| 19 | AWS CodeDeploy | [📖 Study](docs/03-deployment/04-codedeploy.md) |
| 20 | AWS CodeCommit & CodeArtifact | [📖 Study](docs/03-deployment/05-codecommit.md) |
| 21 | AWS CDK & SAM | [📖 Study](docs/03-deployment/06-cdk-sam.md) |

### Domain 4: Troubleshooting and Optimization (18%)

| # | Topic | Link |
|---|-------|------|
| 22 | Amazon CloudWatch | [📖 Study](docs/04-troubleshooting/01-cloudwatch.md) |
| 23 | AWS X-Ray | [📖 Study](docs/04-troubleshooting/02-xray.md) |
| 24 | AWS CloudTrail | [📖 Study](docs/04-troubleshooting/03-cloudtrail.md) |
| 25 | Performance Optimization | [📖 Study](docs/04-troubleshooting/04-optimization.md) |

---

## 🏋️ Interactive Exercises (55 Scenarios)

| Domain | Exercises | Topics |
|--------|-----------|--------|
| Development | 001–020 | Lambda, API Gateway, DynamoDB, S3, SQS, SNS, Step Functions |
| Security | 021–035 | IAM policies, Cognito, KMS, Secrets Manager |
| Deployment | 036–048 | CloudFormation, CodeDeploy, CodePipeline, SAM, CDK |
| Troubleshooting | 049–055 | CloudWatch, X-Ray, debugging, optimization |

👉 **[View All Exercises →](exercises/README.md)**

### Running Exercises

```bash
# Run all exercises
python exercises/runner.py --all

# Run a specific exercise
python exercises/runner.py --exercise 001

# Run exercises by domain
python exercises/runner.py --domain development
python exercises/runner.py --domain security
python exercises/runner.py --domain deployment
python exercises/runner.py --domain troubleshooting

# Show hints for an exercise
python exercises/runner.py --exercise 001 --hint

# Check overall progress
python exercises/runner.py --progress
```

---

## 📝 Practice Exams (5 Full-Length Exams)

| Exam | Questions | Focus | Link |
|------|-----------|-------|------|
| Practice Exam 1 | 65 | Mixed domains | [📝 Take Exam](practice-exams/exam-1.md) |
| Practice Exam 2 | 65 | Mixed domains | [📝 Take Exam](practice-exams/exam-2.md) |
| Practice Exam 3 | 65 | Mixed domains | [📝 Take Exam](practice-exams/exam-3.md) |
| Practice Exam 4 | 65 | Mixed domains | [📝 Take Exam](practice-exams/exam-4.md) |
| Practice Exam 5 | 65 | Mixed domains | [📝 Take Exam](practice-exams/exam-5.md) |

---

## 🗺️ Recommended Study Path

```
 START
   │
   ▼
 ┌──────────────────────────────────────┐
 │  Phase 1: Foundation (Week 1-2)      │
 │  └─ Docs 01-06 (Development core)    │
 │  └─ Exercises 001-012                │
 └──────────────┬───────────────────────┘
                │
                ▼
 ┌──────────────────────────────────────┐
 │  Phase 2: Security (Week 3)          │
 │  └─ Docs 11-15                       │
 │  └─ Exercises 021-035                │
 └──────────────┬───────────────────────┘
                │
                ▼
 ┌──────────────────────────────────────┐
 │  Phase 3: Deployment (Week 4)        │
 │  └─ Docs 16-21                       │
 │  └─ Exercises 036-048                │
 └──────────────┬───────────────────────┘
                │
                ▼
 ┌──────────────────────────────────────┐
 │  Phase 4: Troubleshooting (Week 5)   │
 │  └─ Docs 22-25                       │
 │  └─ Exercises 049-055                │
 └──────────────┬───────────────────────┘
                │
                ▼
 ┌──────────────────────────────────────┐
 │  Phase 5: Practice Exams (Week 6)    │
 │  └─ Take all 5 practice exams        │
 │  └─ Review weak areas                │
 │  └─ Re-do missed exercises           │
 └──────────────┬───────────────────────┘
                │
                ▼
            ✅ READY FOR EXAM
```

---

## 📋 Quick Reference Cards

- [Lambda Limits & Limits](docs/quick-references/lambda-limits.md)
- [DynamoDB Cheat Sheet](docs/quick-references/dynamodb-cheatsheet.md)
- [API Gateway Cheat Sheet](docs/quick-references/api-gateway-cheatsheet.md)
- [CLI Commands Reference](docs/quick-references/cli-commands.md)

---

*Built with ❤️ for AWS developers preparing for their certification.*
