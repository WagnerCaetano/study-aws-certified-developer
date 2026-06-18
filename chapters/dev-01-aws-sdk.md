# AWS SDK & CLI Overview

> **Domain 1: Development with AWS Services** | [← Back to Index](../../README.md) | [Next: Lambda →](02-lambda.md)

---

## Overview

The AWS SDKs (Software Development Kits) and the AWS CLI (Command Line Interface) are the primary tools developers use to interact with AWS services programmatically.

## AWS SDKs

AWS provides SDKs for multiple programming languages:

| SDK | Language | Import |
|-----|----------|--------|
| AWS SDK for Java | Java | `software.amazon.awssdk.*` |
| AWS SDK for JavaScript | Node.js/Browser | `@aws-sdk/client-*` |
| boto3 | Python | `import boto3` |
| AWS SDK for .NET | C# | `Amazon.*` |
| AWS SDK for Go | Go | `github.com/aws/aws-sdk-go-v2` |
| AWS SDK for PHP | PHP | `Aws\Sdk` |

### Key Concepts: Credential Resolution Chain

The SDKs follow a specific order when looking for credentials:

```
1. Environment Variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
2. Shared Credentials File (~/.aws/credentials)
3. EC2 Instance Profile (IAM Role attached to EC2)
4. ECS Task Role (IAM Role for ECS containers)
5. Lambda Execution Role (IAM Role for Lambda functions)
```

### Example: Python (boto3)

```python
import boto3

# Create a client
s3 = boto3.client('s3')

# List all buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# Create a resource (higher-level abstraction)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')
table.put_item(Item={'userId': '123', 'name': 'John'})
```

### Example: JavaScript (Node.js) - v3 SDK

```javascript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const client = new S3Client({ region: 'us-east-1' });

async function uploadFile() {
  const command = new PutObjectCommand({
    Bucket: 'my-bucket',
    Key: 'hello.txt',
    Body: 'Hello World!',
  });
  
  const response = await client.send(command);
  console.log('Upload successful:', response);
}
```

### Example: Using SDK in Lambda

```javascript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  const command = new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: { userId: event.pathParameters.id }
  });
  
  const response = await docClient.send(command);
  return {
    statusCode: 200,
    body: JSON.stringify(response.Item)
  };
};
```

## AWS CLI

### Common CLI Commands for Developers

```bash
# Configure credentials
aws configure
aws configure --profile production

# S3 operations
aws s3 ls
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./local-dir s3://my-bucket/dir/
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# Lambda operations
aws lambda list-functions
aws lambda invoke --function-name myFunction response.json
aws lambda get-function-configuration --function-name myFunction

# DynamoDB operations
aws dynamodb describe-table --table-name Users
aws dynamodb scan --table-name Users
aws dynamodb query --table-name Users --key-condition-expression "userId = :id" --expression-attribute-values '{":id":{"S":"123"}}'

# IAM operations
aws iam list-roles
aws iam get-role --role-name lambda-execution-role

# CloudFormation operations
aws cloudformation deploy --template-file template.yaml --stack-name my-stack
aws cloudformation describe-stacks --stack-name my-stack

# CloudWatch Logs
aws logs tail /aws/lambda/myFunction --follow
```

### Using CLI with different profiles

```bash
# Use a specific profile
aws s3 ls --profile production

# Use a specific region
aws s3 ls --region eu-west-1

# Output format
aws dynamodb scan --table-name Users --output json
aws dynamodb scan --table-name Users --output table
aws dynamodb scan --table-name Users --query 'Items[0]'
```

## AWS CloudShell

- Browser-based shell with pre-installed AWS CLI
- No additional cost
- 1 GB of persistent storage per Region
- Pre-authenticated with your console credentials

## Key SDK Best Practices

1. **Reuse SDK clients** — Don't create new clients for every request
2. **Use environment variables** for configuration (`AWS_REGION`, etc.)
3. **Use IAM roles** instead of hardcoded credentials
4. **Handle pagination** — Use paginators or manual pagination
5. **Implement exponential backoff** for retries
6. **Use the latest SDK version** — v3 for Node.js has tree-shaking support

## SDK Error Handling

```python
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

try:
    response = table.get_item(Key={'userId': '123'})
    item = response.get('Item')
    if item is None:
        print("Item not found")
except ClientError as e:
    print(f"Error: {e.response['Error']['Message']}")
    print(f"Code: {e.response['Error']['Code']}")
```

## Common Exam Topics

- **Credential provider chain** — Know the order of credential resolution
- **SDK versions** — AWS SDK for JavaScript v3 uses modular imports
- **boto3** — Understand resource vs client abstraction
- **IAM roles vs access keys** — Always prefer roles for EC2/Lambda/ECS
- **Region configuration** — How SDKs determine which region to use

---

## Quick Quiz

1. What is the correct order of the credential resolution chain?
2. What's the difference between boto3 `client` and `resource`?
3. How do you specify a profile in the AWS CLI?
4. What is AWS CloudShell?
5. Why should you reuse SDK client instances?

---

[← Back to Index](../../README.md) | [Next: Lambda Deep Dive →](02-lambda.md)
