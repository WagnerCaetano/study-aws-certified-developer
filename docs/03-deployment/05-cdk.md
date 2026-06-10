# AWS CDK (Cloud Development Kit)

> **Domain 3: Deployment** | [← Elastic Beanstalk](04-elastic-beanstalk.md) | [Back to Index](../../README.md) | [Next: CloudWatch →](../04-monitoring/01-cloudwatch.md)

---

## Overview

AWS CDK lets you define infrastructure using **familiar programming languages** instead of YAML/JSON.

### Supported Languages
TypeScript, JavaScript, Python, Java, C#, Go

### CDK vs CloudFormation vs SAM

| Feature | CloudFormation | SAM | CDK |
|---------|---------------|-----|-----|
| Language | YAML/JSON | YAML | Python, TS, Java, etc. |
| Abstraction | Low | Medium (serverless) | **High** |
| Logic | Intrinsic functions | Transform macros | **Real code** |
| Testing | No | No | **Unit tests** |
| Reusability | Modules/Stacks | Templates | **Constructs** |

---

## CDK Concepts

| Concept | Description |
|---------|-------------|
| **App** | Root of your CDK application |
| **Stack** | Equivalent to a CloudFormation stack |
| **Construct** | Reusable component (building block) |
| **Synthesis** | CDK code → CloudFormation template |

---

## CDK Example (Python)

```python
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "ItemsTable",
            partition_key=dynamodb.Attribute(
                name="itemId",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Lambda Function
        handler = _lambda.Function(
            self, "GetItemsHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            },
        )

        # Grant permissions
        table.grant_read_data(handler)

        # API Gateway
        api = apigw.LambdaRestApi(
            self, "ItemsApi",
            handler=handler,
            rest_api_name="Items Service",
        )
```

---

## CDK CLI

```bash
# Initialize project
cdk init app --language python

# List stacks
cdk list

# Synthesize (generate CloudFormation template)
cdk synth

# Diff (compare with deployed stack)
cdk diff

# Deploy
cdk deploy

# Destroy
cdk destroy

# Bootstrap (first time - creates deployment resources)
cdk bootstrap
```

---

## Construct Levels

| Level | Description | Example |
|-------|-------------|---------|
| **L1** | Direct CFN resource mapping | `CfnBucket`, `CfnFunction` |
| **L2** | High-level with defaults | `Bucket`, `Function`, `Table` |
| **L3** | Patterns (multi-resource) | `LambdaRestApi` |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Define infra with real code | Use CDK |
| Generate CloudFormation from code | `cdk synth` |
| Reusable infrastructure component | Create a CDK Construct |
| Preview changes before deploy | `cdk diff` |
| Test infrastructure logic | Write unit tests for CDK stacks |
| Need high-level abstractions | Use L2/L3 constructs |

---

[← Elastic Beanstalk](04-elastic-beanstalk.md) | [Back to Index](../../README.md) | [Next: CloudWatch →](../04-monitoring/01-cloudwatch.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3 study guides (5 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>