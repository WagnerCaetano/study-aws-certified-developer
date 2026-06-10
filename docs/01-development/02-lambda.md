# AWS Lambda Deep Dive

> **Domain 1: Development with AWS Services** | [← SDK](01-aws-sdk.md) | [Back to Index](../../README.md) | [Next: API Gateway →](03-api-gateway.md)

---

## Overview

AWS Lambda is a **serverless compute service** that runs your code in response to events. It automatically manages the underlying compute resources.

### Key Characteristics
- **Event-driven** — Triggered by AWS services, HTTP requests, or schedules
- **Stateless** — Each invocation is independent
- **Auto-scaling** — Automatically scales from zero to thousands of concurrent executions
- **Pay-per-use** — Charged per request and compute duration (in 1ms increments)

---

## Lambda Execution Model

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Event     │────►│  Lambda      │────►│  Your Code      │
│   Source    │     │  Service     │     │  (Handler)      │
└─────────────┘     └──────────────┘     └─────────────────┘
                          │                      │
                    ┌─────┴──────┐         ┌─────┴──────┐
                    │ Execution  │         │ Runtime    │
                    │ Environment│         │ (Python,   │
                    │ (Container)│         │  Node.js,  │
                    └────────────┘         │  Java, etc)│
                                           └────────────┘
```

### Cold Starts vs Warm Starts

| Aspect | Cold Start | Warm Start |
|--------|-----------|------------|
| When? | First invocation or after idle period | Subsequent invocations |
| Latency | Higher (container creation + code load) | Lower (container reused) |
| Duration | 100ms–several seconds | Minimal |
| Impact | Varies by runtime & deployment package size | Negligible |

**Cold Start Mitigation:**
- Use **Provisioned Concurrency** to pre-initialize instances
- Keep deployment packages small
- Use simpler runtimes (Python, Node.js start faster than Java/.NET)
- Use **SnapStart** for Java (snapshot-based initialization)

---

## Supported Runtimes

| Runtime | Version | Handler Format |
|---------|---------|---------------|
| Node.js | 18.x, 20.x | `exports.handler = async (event) => {}` |
| Python | 3.10, 3.11, 3.12 | `def lambda_handler(event, context):` |
| Java | 11, 17, 21 | `public String handleRequest(Request input, Context context)` |
| .NET | 6, 8 | `public async Task<string> FunctionHandler(string input, ILambdaContext context)` |
| Go | 1.x | `func handler(ctx context.Context, events.Event) (string, error)` |
| Ruby | 3.2 | `def handler(event:, context:)` |

---

## Lambda Limits (Must Know!)

| Limit | Value |
|-------|-------|
| Max memory | **10,240 MB** (10 GB) |
| Max execution timeout | **15 minutes** |
| Max deployment package (zipped) | **50 MB** |
| Max deployment package (unzipped) | **250 MB** |
| Max `/tmp` storage | **10,240 MB** |
| Max environment variables | **4 KB** |
| Max concurrent executions | **1,000** (soft limit, can be increased) |
| Max payload (sync invoke) | **6 MB** |
| Max payload (async invoke) | **256 KB** |

---

## Handler Function

### Python Handler

```python
def lambda_handler(event, context):
    """
    event: The event data that triggered the function (dict)
    context: Runtime information (Context object)
    """
    name = event.get('name', 'World')
    
    # Context properties
    print(f"Function: {context.function_name}")
    print(f"Request ID: {context.aws_request_id}")
    print(f"Remaining time: {context.get_remaining_time_in_millis()} ms")
    
    return {
        'statusCode': 200,
        'body': f'Hello, {name}!'
    }
```

### Node.js Handler

```javascript
export const handler = async (event, context) => {
    // event: The event payload
    // context: Runtime information
    
    console.log(`Function: ${context.functionName}`);
    console.log(`Request ID: ${context.awsRequestId}`);
    console.log(`Remaining time: ${context.getRemainingTimeInMillis()} ms`);
    
    return {
        statusCode: 200,
        body: JSON.stringify({ message: 'Hello, World!' })
    };
};
```

---

## Invocation Types

### 1. Synchronous (RequestResponse)

```
Client ──► Lambda ──► Response
         (waits)
```

```bash
aws lambda invoke --function-name myFunction response.json
```

**Sources:** API Gateway, ALB, CLI, SDK, Amazon Lex

### 2. Asynchronous (Event)

```
Client ──► Lambda Queue ──► Lambda (retries up to 3x)
  │                            │
  ◄──── Acknowledgement ───────┘
```

```bash
aws lambda invoke --function-name myFunction --invocation-type Event response.json
```

**Sources:** S3, SNS, EventBridge, CloudWatch Events

**Retry behavior:** 
- 3 retries total with exponential backoff
- Can configure **Dead Letter Queue (DLQ)** (SQS or SNS) for failed events
- Use `EventInvokeConfig` to customize retry behavior

### 3. Stream-based (Polling)

```
DynamoDB Streams ──► Lambda Polls ──► Processes batch
Kinesis Streams  ──► Lambda Polls ──► Processes batch
```

**Partial batch failure:** Configure `MaximumBatchingWindowInSeconds`, `MaximumRetryAttempts`, and `BisectBatchOnFunctionError`

---

## Event Source Mappings

```python
# Example: DynamoDB Stream event
{
    "Records": [
        {
            "eventID": "1",
            "eventName": "INSERT",
            "dynamodb": {
                "Keys": {"userId": {"S": "123"}},
                "NewImage": {"name": {"S": "John"}}
            }
        }
    ]
}
```

```python
# Example: S3 event
{
    "Records": [
        {
            "s3": {
                "bucket": {"name": "my-bucket"},
                "object": {"key": "uploads/image.jpg"}
            }
        }
    ]
}
```

```python
# Example: API Gateway event
{
    "httpMethod": "POST",
    "path": "/users",
    "queryStringParameters": {"page": "1"},
    "body": "{\"name\": \"John\"}",
    "pathParameters": {"id": "123"},
    "headers": {"Content-Type": "application/json"},
    "requestContext": {
        "requestId": "abc-123",
        "stage": "prod"
    }
}
```

---

## Deployment Packaging

### Zip Package (≤ 50 MB)

```bash
# Python
pip install -r requirements.txt --target ./package
cd package
zip -r ../function.zip .
cd ..
zip -g function.zip lambda_function.py

# Deploy
aws lambda update-function-code --function-name myFunction --zip-file fileb://function.zip
```

### Container Image (≤ 10 GB)

```dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]
```

```bash
# Build and push
docker build -t my-lambda .
docker tag my-lambda:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda:latest

# Deploy
aws lambda update-function-code \
  --function-name myFunction \
  --image-uri 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda:latest
```

---

## Environment Variables

```python
import os

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    stage = os.environ.get('STAGE', 'dev')
    
    # These are automatically available:
    aws_region = os.environ['AWS_REGION']
    function_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    memory_size = os.environ['AWS_LAMBDA_FUNCTION_MEMORY_SIZE']
```

**Encrypting sensitive values:**
- Use KMS to encrypt environment variables at rest
- For secrets, prefer **AWS Secrets Manager** or **SSM Parameter Store**

---

## Lambda Layers

Layers let you separate dependencies from your function code:

```
┌──────────────────────────┐
│   Function Code          │  ← Your handler
├──────────────────────────┤
│   Layer 3 (Custom lib)   │
├──────────────────────────┤
│   Layer 2 (SDK/lib)      │  ← Up to 5 layers
├──────────────────────────┤
│   Layer 1 (Dependencies) │
└──────────────────────────┘
```

- **Max 5 layers** per function
- Total unzipped size (code + layers) ≤ 250 MB
- Layers are **versioned** and can be shared across functions/accounts
- Useful for: shared libraries, custom runtimes, SDK dependencies

---

## Lambda Destinations

Route async invocation results to other services:

```
                ┌─► On Success ──► SQS / SNS / Lambda / EventBridge
Lambda ─────────┤
                └─► On Failure ──► SQS / SNS / Lambda / EventBridge
```

**Note:** Destinations replace DLQs for more flexibility. DLQs still work but are less configurable.

---

## Lambda Versions & Aliases

```
Function: myFunction
  ├── Version 1 (immutable)
  ├── Version 2 (immutable)
  ├── Version 3 ($LATEST - mutable)
  │
  ├── Alias: PROD ──► Version 2
  ├── Alias: STAGING ──► Version 3 ($LATEST)
  └── Alias: CANARY ──► Version 2 (90%) + Version 3 (10%)
```

- **Versions** are immutable snapshots of code + configuration
- **Aliases** are pointers to specific versions
- **Routing config** on aliases enables weighted traffic shifting (canary deployments)

---

## Lambda with VPC

By default, Lambda functions have **no VPC access**. To access VPC resources:

```python
# Required VPC configuration
{
    "VpcConfig": {
        "SubnetIds": ["subnet-abc123", "subnet-def456"],
        "SecurityGroupIds": ["sg-abc123"]
    }
}
```

**Requirements:**
- Lambda needs **ENI** (Elastic Network Interface) in your VPC
- Your VPC needs **NAT Gateway** for internet access
- Lambda needs `AWSLambdaVPCAccessExecutionRole` managed policy

**⚠️ Important:** Lambda in a VPC does NOT have internet access by default! You need a NAT Gateway or VPC endpoints.

---

## Provisioned Concurrency

- Pre-initializes execution environments
- Eliminates cold starts
- Configured per alias/version
- Additional cost (per provisioned concurrent execution)

```bash
aws lambda put-provisioned-concurrency-config \
  --function-name myFunction \
  --qualifier PROD \
  --provisioned-concurrent-executions 10
```

---

## Lambda best practices

1. **Keep handlers small** — Separate business logic from handler
2. **Initialize SDK clients outside handler** — Reuse across warm invocations
3. **Use `/tmp` for caching** — Up to 10 GB ephemeral storage
4. **Minimize deployment package** — Only include needed dependencies
5. **Use environment variables** for configuration
6. **Use layers** for shared code/dependencies
7. **Avoid recursive calls** — Don't create infinite loops (Lambda → S3 → Lambda)
8. **Set appropriate timeout** — Don't use the default 3s for long operations
9. **Use Dead Letter Queues** for async invocations
10. **Monitor with CloudWatch** — Use metrics, logs, and alarms

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Cold start too slow | Use Provisioned Concurrency or SnapStart (Java) |
| Need to process files > 250 MB | Use container images (up to 10 GB) |
| Lambda needs VPC resource access | Configure VPC, subnets, security groups |
| Lambda in VPC needs internet | Add NAT Gateway or VPC endpoints |
| Need shared dependencies | Use Lambda Layers |
| Async function fails silently | Configure DLQ or Destinations |
| Gradual deployment | Use aliases with weighted routing |
| Need to run > 15 min | Use Step Functions or ECS/Fargate |
| Large dependency package | Use Lambda Layers or container images |

---

## Quick Quiz

1. What is the maximum execution timeout for a Lambda function?
2. How does Provisioned Concurrency help with cold starts?
3. What is the difference between synchronous and asynchronous invocation?
4. How do you share code between multiple Lambda functions?
5. What happens if a Lambda function in a VPC needs internet access?

---

[← SDK](01-aws-sdk.md) | [Back to Index](../../README.md) | [Next: API Gateway →](03-api-gateway.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Create doc 01-aws-sdk.md
- [ ] Create remaining Domain 1 study guides (9 files)
- [ ] Create Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>