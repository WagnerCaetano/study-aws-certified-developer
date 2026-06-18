#!/usr/bin/env python3
"""Generate practice exams for AWS Developer Certification."""

import random
import json
from pathlib import Path

EXAMS_DIR = Path(__file__).parent / 'exams'

# ============================================================
# Question Bank - All domains
# ============================================================

QUESTIONS = [
    # ---- Domain 1: Development ----
    {
        "id": "q1",
        "domain": "Development",
        "question": "A developer needs to deploy a Lambda function that processes SQS messages. The function must read messages in batches of 10 and delete them after processing. Which of the following is the BEST approach?",
        "options": [
            "A) Poll SQS manually using a scheduled Lambda function every minute",
            "B) Configure SQS as an event source for the Lambda function with a batch size of 10",
            "C) Use SNS to fan out messages to individual Lambda invocations",
            "D) Use Kinesis Data Streams to buffer messages before processing"
        ],
        "answer": "B",
        "explanation": "SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages (up to 10,000). Successfully processed messages are automatically deleted."
    },
    {
        "id": "q2",
        "domain": "Development",
        "question": "A Lambda function needs to access a DynamoDB table. What is the MOST secure way to grant permissions?",
        "options": [
            "A) Hardcode AWS access keys in the Lambda function code",
            "B) Store access keys in Lambda environment variables",
            "C) Attach an IAM execution role with least-privilege DynamoDB permissions to the Lambda function",
            "D) Use the AWS account root user credentials"
        ],
        "answer": "C",
        "explanation": "IAM execution roles are the secure way to grant Lambda permissions. Never hardcode credentials or use root accounts. Environment variables for secrets should use Secrets Manager instead."
    },
    {
        "id": "q3",
        "domain": "Development",
        "question": "A developer is building a REST API with API Gateway. The backend Lambda function returns a response, but the client receives a 502 error. What is the MOST likely cause?",
        "options": [
            "A) The API Gateway does not have CORS enabled",
            "B) The Lambda function is not returning a properly formatted proxy response with statusCode, headers, and body",
            "C) The API Gateway is missing request validation",
            "D) The client is sending the wrong Content-Type header"
        ],
        "answer": "B",
        "explanation": "A 502 Bad Gateway error from API Gateway with Lambda proxy integration typically means the Lambda function returned an invalid response format. The response must include statusCode, headers, and body as a properly formatted JSON object."
    },
    {
        "id": "q4",
        "domain": "Development",
        "question": "Which DynamoDB operation is MOST efficient for retrieving a single item by its primary key?",
        "options": [
            "A) Scan with a filter expression",
            "B) Query with the partition key",
            "C) GetItem with the full primary key",
            "D) BatchGetItem with a single item"
        ],
        "answer": "C",
        "explanation": "GetItem is the most efficient for retrieving a single item by its full primary key (partition + sort key if applicable). It uses minimal RCUs compared to Scan or Query."
    },
    {
        "id": "q5",
        "domain": "Development",
        "question": "A developer needs to store user session data with sub-millisecond latency. Which AWS service should be used?",
        "options": [
            "A) Amazon S3",
            "B) Amazon DynamoDB",
            "C) Amazon ElastiCache (Redis)",
            "D) Amazon RDS"
        ],
        "answer": "C",
        "explanation": "ElastiCache (Redis) provides sub-millisecond latency for in-memory data operations, making it ideal for session data. DynamoDB provides single-digit millisecond latency."
    },
    {
        "id": "q6",
        "domain": "Development",
        "question": "A Lambda function is experiencing cold start latency. Which approach would BEST reduce this?",
        "options": [
            "A) Increase the Lambda memory allocation",
            "B) Use Provisioned Concurrency",
            "C) Add more code to the Lambda function",
            "D) Decrease the timeout setting"
        ],
        "answer": "B",
        "explanation": "Provisioned Concurrency pre-initializes Lambda execution environments, eliminating cold starts. Increasing memory can help but doesn't eliminate cold starts entirely."
    },
    {
        "id": "q7",
        "domain": "Development",
        "question": "When building a DynamoDB table for an e-commerce application, which access pattern requires a Global Secondary Index (GSI)?",
        "options": [
            "A) Get order by orderId (partition key)",
            "B) Get all orders for a customer sorted by date (composite key)",
            "C) Get all orders with status 'PENDING' regardless of customer",
            "D) Delete an order by orderId"
        ],
        "answer": "C",
        "explanation": "Querying by a non-key attribute (status) requires a GSI. The primary table can only be efficiently queried by the partition key and sort key."
    },
    {
        "id": "q8",
        "domain": "Development",
        "question": "A developer needs to process a large CSV file uploaded to S3. The file is 5GB. What is the MOST efficient approach?",
        "options": [
            "A) Download the entire file in a Lambda function and process it",
            "B) Use S3 Select to query only the needed data",
            "C) Copy the file to EBS and process it with EC2",
            "D) Use S3 Transfer Acceleration"
        ],
        "answer": "B",
        "explanation": "S3 Select allows you to retrieve only the needed data from a CSV file using SQL expressions, reducing data transfer and processing time significantly."
    },
    {
        "id": "q9",
        "domain": "Development",
        "question": "A developer wants to ensure exactly-once processing of SQS messages in a Lambda function. What should they do?",
        "options": [
            "A) Set the visibility timeout to infinity",
            "B) Use a FIFO queue with content-based deduplication",
            "C) Delete the message after processing and use idempotent processing logic",
            "D) Use SNS instead of SQS"
        ],
        "answer": "C",
        "explanation": "SQS provides at-least-once delivery. For exactly-once semantics, delete messages after successful processing and design idempotent processing logic that can handle duplicate deliveries safely."
    },
    {
        "id": "q10",
        "domain": "Development",
        "question": "Which S3 storage class is MOST cost-effective for data that is accessed once a quarter?",
        "options": [
            "A) S3 Standard",
            "B) S3 Intelligent-Tiering",
            "C) S3 Standard-IA (Infrequent Access)",
            "D) S3 Glacier Deep Archive"
        ],
        "answer": "C",
        "explanation": "S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access. Intelligent-Tiering has a monitoring cost."
    },
    {
        "id": "q11",
        "domain": "Development",
        "question": "A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?",
        "options": [
            "A) SQS + Lambda",
            "B) SNS + SQS + Lambda",
            "C) Kinesis + Lambda",
            "D) API Gateway + Lambda"
        ],
        "answer": "B",
        "explanation": "SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently."
    },
    {
        "id": "q12",
        "domain": "Development",
        "question": "What is the maximum execution timeout for an AWS Lambda function?",
        "options": [
            "A) 30 seconds",
            "B) 5 minutes",
            "C) 15 minutes",
            "D) 1 hour"
        ],
        "answer": "C",
        "explanation": "The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services."
    },
    {
        "id": "q13",
        "domain": "Development",
        "question": "A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?",
        "options": [
            "A) Amazon SQS Standard queue",
            "B) Amazon SNS",
            "C) Amazon Kinesis Data Streams",
            "D) Amazon MQ"
        ],
        "answer": "C",
        "explanation": "Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming."
    },
    {
        "id": "q14",
        "domain": "Development",
        "question": "A Step Functions workflow needs to wait for human approval before proceeding. Which state type should be used?",
        "options": [
            "A) Task state",
            "B) Choice state",
            "C) Wait state with a callback pattern",
            "D) Succeed state"
        ],
        "answer": "C",
        "explanation": "The Wait state with callback pattern (.waitForTaskToken) allows Step Functions to pause execution until an external process (like human approval) completes by returning the task token."
    },
    {
        "id": "q15",
        "domain": "Development",
        "question": "Which ECS launch type eliminates the need to manage underlying server infrastructure?",
        "options": [
            "A) EC2 launch type",
            "B) Fargate launch type",
            "C) External launch type",
            "D) Lambda launch type"
        ],
        "answer": "B",
        "explanation": "AWS Fargate is a serverless compute engine for containers that works with ECS and EKS, eliminating the need to manage servers or clusters."
    },
    # ---- Domain 2: Security ----
    {
        "id": "q16",
        "domain": "Security",
        "question": "A developer needs to grant a Lambda function access to read objects from an S3 bucket. What is the MOST secure approach?",
        "options": [
            "A) Embed AWS access keys in the Lambda function code",
            "B) Create an IAM role with S3 read permissions and attach it to the Lambda function",
            "C) Make the S3 bucket public",
            "D) Use bucket policies that allow anonymous access"
        ],
        "answer": "B",
        "explanation": "IAM roles provide temporary credentials automatically rotated by AWS. This is the secure best practice — never embed credentials in code or make resources public unnecessarily."
    },
    {
        "id": "q17",
        "domain": "Security",
        "question": "A company wants to implement user authentication for a web application without managing passwords. Which service should they use?",
        "options": [
            "A) AWS IAM",
            "B) Amazon Cognito",
            "C) AWS Secrets Manager",
            "D) AWS WAF"
        ],
        "answer": "B",
        "explanation": "Amazon Cognito provides user authentication, sign-up, and sign-in functionality for web and mobile applications, supporting social identity providers and SAML."
    },
    {
        "id": "q18",
        "domain": "Security",
        "question": "A developer needs to encrypt data larger than 4KB using KMS. What is the recommended approach?",
        "options": [
            "A) Call KMS Encrypt repeatedly for each 4KB chunk",
            "B) Use envelope encryption with GenerateDataKey",
            "C) Use KMS with a larger key size",
            "D) Compress the data to under 4KB"
        ],
        "answer": "B",
        "explanation": "Envelope encryption uses KMS to generate a data key, which is then used to encrypt the actual data locally. This avoids KMS size limits and reduces KMS API calls."
    },
    {
        "id": "q19",
        "domain": "Security",
        "question": "Which AWS service provides automatic rotation of database credentials?",
        "options": [
            "A) AWS Systems Manager Parameter Store",
            "B) AWS Secrets Manager",
            "C) AWS KMS",
            "D) AWS IAM"
        ],
        "answer": "B",
        "explanation": "AWS Secrets Manager provides automatic credential rotation for databases and other services. Parameter Store can store secrets but doesn't provide automatic rotation."
    },
    {
        "id": "q20",
        "domain": "Security",
        "question": "A developer needs to securely store a database connection string for a Lambda function. The string needs to be rotated every 30 days. Which solution is BEST?",
        "options": [
            "A) Store it in a Lambda environment variable",
            "B) Store it in AWS Secrets Manager with automatic rotation",
            "C) Store it in S3 with server-side encryption",
            "D) Store it in AWS Systems Manager Parameter Store as a String type"
        ],
        "answer": "B",
        "explanation": "Secrets Manager supports automatic rotation (configurable schedule), which meets the 30-day rotation requirement. Parameter Store SecureString can encrypt but doesn't provide automatic rotation."
    },
    {
        "id": "q21",
        "domain": "Security",
        "question": "What is the principle of least privilege in AWS IAM?",
        "options": [
            "A) Granting all permissions to all users",
            "B) Granting only the minimum permissions needed to perform a task",
            "C) Using only managed policies",
            "D) Denying all access by default and using IAM roles only"
        ],
        "answer": "B",
        "explanation": "Least privilege means granting only the permissions needed for a specific task. This reduces the blast radius of compromised credentials."
    },
    {
        "id": "q22",
        "domain": "Security",
        "question": "An application running on ECS needs to access DynamoDB. How should the developer configure permissions?",
        "options": [
            "A) Store access keys in the container image",
            "B) Use an IAM task role for the ECS task definition",
            "C) Use EC2 instance profiles",
            "D) Create a separate IAM user for each container"
        ],
        "answer": "B",
        "explanation": "ECS task roles (taskRoleArn) provide temporary credentials to containers, following the same IAM role pattern as Lambda execution roles."
    },
    {
        "id": "q23",
        "domain": "Security",
        "question": "A developer wants to add a web-based login page to their application using Cognito. Which Cognito feature provides hosted UI authentication?",
        "options": [
            "A) Cognito Identity Pools",
            "B) Cognito User Pool hosted UI (App Integration)",
            "C) Cognito Sync",
            "D) Cognito user migration Lambda trigger"
        ],
        "answer": "B",
        "explanation": "Cognito User Pools provide a hosted UI for authentication that can be customized, supporting social providers and SAML, without building your own login page."
    },
    {
        "id": "q24",
        "domain": "Security",
        "question": "Which KMS operation should be used to encrypt data that is larger than 4KB?",
        "options": [
            "A) kms:Encrypt",
            "B) kms:GenerateDataKey",
            "C) kms:GenerateRandom",
            "D) kms:ReEncrypt"
        ],
        "answer": "B",
        "explanation": "GenerateDataKey returns a plaintext data key and an encrypted copy. Use the plaintext key to encrypt data locally (envelope encryption), then store the encrypted key with the data."
    },
    {
        "id": "q25",
        "domain": "Security",
        "question": "A developer is reviewing an IAM policy and finds: 'Action': 's3:*', 'Resource': '*'. What security concern does this raise?",
        "options": [
            "A) The policy syntax is invalid",
            "B) The policy violates least privilege — it grants full S3 access to all buckets",
            "C) The policy uses a deprecated format",
            "D) The policy cannot be attached to a role"
        ],
        "answer": "B",
        "explanation": "Using wildcards for both Action and Resource violates least privilege. The policy grants all S3 actions on all buckets, which is overly permissive."
    },
    {
        "id": "q26",
        "domain": "Security",
        "question": "A developer needs to implement API key-based authentication for a public API. Which approach should they use?",
        "options": [
            "A) IAM authentication on API Gateway",
            "B) API Gateway with API keys and usage plans",
            "C) Cognito User Pools",
            "D) Lambda authorizer that validates API keys"
        ],
        "answer": "B",
        "explanation": "API Gateway provides built-in API key management with usage plans for throttling and quotas. This is designed for public APIs where you want to track and control usage."
    },
    {
        "id": "q27",
        "domain": "Security",
        "question": "A developer wants to use temporary credentials to access AWS resources from an on-premises application. Which STS API should they call?",
        "options": [
            "A) GetSessionToken",
            "B) AssumeRole",
            "C) GetFederationToken",
            "D) DecodeAuthorizationMessage"
        ],
        "answer": "B",
        "explanation": "AssumeRole returns temporary credentials (access key, secret key, session token) that can be used to access AWS resources. It's the standard way to obtain temporary credentials for cross-account or on-premises access."
    },
    {
        "id": "q28",
        "domain": "Security",
        "question": "Which feature of S3 prevents accidental deletion of objects?",
        "options": [
            "A) Server-side encryption",
            "B) Versioning with MFA Delete",
            "C) CORS configuration",
            "D) Transfer Acceleration"
        ],
        "answer": "B",
        "explanation": "MFA Delete requires multi-factor authentication to delete objects or disable versioning, providing strong protection against accidental or malicious deletion."
    },
    {
        "id": "q29",
        "domain": "Security",
        "question": "What is the difference between a resource-based policy and an identity-based policy in AWS?",
        "options": [
            "A) They are the same thing",
            "B) Resource-based policies are attached to resources (like S3 buckets), identity-based policies are attached to IAM principals",
            "C) Resource-based policies are only for S3",
            "D) Identity-based policies are more restrictive"
        ],
        "answer": "B",
        "explanation": "Resource-based policies are attached to resources and define who can access them. Identity-based policies are attached to IAM users, groups, or roles and define what they can access."
    },
    {
        "id": "q30",
        "domain": "Security",
        "question": "A developer needs to encrypt an S3 bucket with a customer-managed KMS key. Which bucket property should they configure?",
        "options": [
            "A) Bucket policy",
            "B) Default encryption with SSE-KMS",
            "C) CORS configuration",
            "D) Object lock"
        ],
        "answer": "B",
        "explanation": "S3 default encryption with SSE-KMS uses a customer-managed CMK. This automatically encrypts all new objects with the specified KMS key."
    },
    # ---- Domain 3: Deployment ----
    {
        "id": "q31",
        "domain": "Deployment",
        "question": "A developer wants to deploy infrastructure as code for a serverless application. Which tool is PURPOSE-BUILT for this?",
        "options": [
            "A) AWS CloudFormation directly",
            "B) AWS SAM (Serverless Application Model)",
            "C) AWS Elastic Beanstalk",
            "D) AWS OpsWorks"
        ],
        "answer": "B",
        "explanation": "AWS SAM is a framework for building serverless applications, providing simplified syntax for Lambda functions, API Gateway, and DynamoDB tables."
    },
    {
        "id": "q32",
        "domain": "Deployment",
        "question": "In a CI/CD pipeline using AWS CodePipeline, which stage is responsible for transforming source code into a deployable artifact?",
        "options": [
            "A) Source stage",
            "B) Build stage",
            "C) Deploy stage",
            "D) Approval stage"
        ],
        "answer": "B",
        "explanation": "The Build stage (typically using CodeBuild) compiles source code, runs tests, and produces deployable artifacts like Lambda deployment packages or Docker images."
    },
    {
        "id": "q33",
        "domain": "Deployment",
        "question": "What does the 'Transform: AWS::Serverless-2016-10-31' section in a CloudFormation template indicate?",
        "options": [
            "A) The template is being converted to JSON",
            "B) The template uses AWS SAM syntax that needs to be transformed to standard CloudFormation",
            "C) The template is for a legacy application",
            "D) The template uses CDK constructs"
        ],
        "answer": "B",
        "explanation": "The Transform section tells CloudFormation to use the SAM transform, which converts SAM-specific resource types (like AWS::Serverless::Function) into standard CloudFormation resources."
    },
    {
        "id": "q34",
        "domain": "Deployment",
        "question": "A developer wants to perform blue/green deployments for a Lambda function. Which deployment preference should they use in SAM?",
        "options": [
            "A) AllAtOnce",
            "B) Canary10Percent5Minutes",
            "C) Linear10PercentEvery3Minutes",
            "D) Rolling"
        ],
        "answer": "B",
        "explanation": "Canary10Percent5Minutes shifts 10% of traffic to the new version, waits 5 minutes, then shifts the remaining 90%. This is a blue/green deployment strategy for Lambda."
    },
    {
        "id": "q35",
        "domain": "Deployment",
        "question": "Which Elastic Beanstalk deployment strategy has the HIGHEST availability but takes the longest?",
        "options": [
            "A) All at once",
            "B) Rolling",
            "C) Rolling with additional batch",
            "D) Immutable"
        ],
        "answer": "D",
        "explanation": "Immutable deployment creates a completely new set of instances, ensuring full availability during deployment. It's the safest but slowest and most expensive option."
    },
    {
        "id": "q36",
        "domain": "Deployment",
        "question": "A developer is using AWS CDK to define infrastructure. Which command generates the CloudFormation template without deploying?",
        "options": [
            "A) cdk deploy",
            "B) cdk synth",
            "C) cdk init",
            "D) cdk diff"
        ],
        "answer": "B",
        "explanation": "cdk synth (synthesize) generates the CloudFormation template from CDK code without deploying. This is useful for reviewing changes before deployment."
    },
    {
        "id": "q37",
        "domain": "Deployment",
        "question": "Which CloudFormation intrinsic function is used to reference a resource's attribute?",
        "options": [
            "A) Fn::Ref",
            "B) Fn::GetAtt",
            "C) Fn::Sub",
            "D) Fn::Join"
        ],
        "answer": "B",
        "explanation": "Fn::GetAtt returns the value of an attribute from a resource in the template, such as a Lambda function's Arn or an S3 bucket's DomainName."
    },
    {
        "id": "q38",
        "domain": "Deployment",
        "question": "A developer wants to share a Lambda function's ARN from one CloudFormation stack to another. How can they do this?",
        "options": [
            "A) Use Fn::Ref in the second stack",
            "B) Use Outputs with Export in the first stack and Fn::ImportValue in the second stack",
            "C) Hardcode the ARN in both stacks",
            "D) Use SSM parameters automatically"
        ],
        "answer": "B",
        "explanation": "CloudFormation cross-stack references use Outputs with Export Name in one stack and Fn::ImportValue in another to share values between stacks."
    },
    {
        "id": "q39",
        "domain": "Deployment",
        "question": "What is the purpose of a buildspec.yml file in AWS CodeBuild?",
        "options": [
            "A) It defines the infrastructure resources",
            "B) It contains the build commands and settings for CodeBuild",
            "C) It configures CodePipeline stages",
            "D) It defines IAM policies for the build"
        ],
        "answer": "B",
        "explanation": "The buildspec.yml defines the build phases (install, pre_build, build, post_build), environment variables, and artifacts for CodeBuild."
    },
    {
        "id": "q40",
        "domain": "Deployment",
        "question": "Which AWS SAM CLI command validates a SAM template locally?",
        "options": [
            "A) sam validate",
            "B) sam deploy --no-execute-changeset",
            "C) sam build --validate",
            "D) sam local invoke"
        ],
        "answer": "A",
        "explanation": "sam validate checks the SAM template for syntax and structural errors. It can validate both SAM and CloudFormation templates."
    },
    {
        "id": "q41",
        "domain": "Deployment",
        "question": "A developer needs to deploy a containerized application without managing any infrastructure. Which combination should they use?",
        "options": [
            "A) EC2 + Docker",
            "B) ECS with Fargate launch type",
            "C) ECS with EC2 launch type",
            "D) Elastic Beanstalk with Docker platform"
        ],
        "answer": "B",
        "explanation": "ECS with Fargate eliminates infrastructure management for containers. Fargate provisions and manages the underlying compute resources automatically."
    },
    {
        "id": "q42",
        "domain": "Deployment",
        "question": "In CloudFormation, what happens when a stack update fails?",
        "options": [
            "A) The stack is deleted",
            "B) Changes are automatically rolled back to the previous known good state",
            "C) The stack is paused for manual review",
            "D) Only the failed resource is deleted"
        ],
        "answer": "B",
        "explanation": "CloudFormation automatically rolls back changes on failure by default. All changes made during the update are reverted to the previous stable state."
    },
    {
        "id": "q43",
        "domain": "Deployment",
        "question": "Which AWS CDK construct level provides the highest abstraction with pre-configured patterns?",
        "options": [
            "A) L1 constructs (CfnXxx)",
            "B) L2 constructs",
            "C) L3 constructs (Patterns)",
            "D) L0 constructs"
        ],
        "answer": "C",
        "explanation": "L3 constructs (also called patterns) provide the highest level of abstraction with pre-configured defaults and best practices, like aws-apigateway.LambdaRestApi."
    },
    {
        "id": "q44",
        "domain": "Deployment",
        "question": "A developer wants to test a SAM application locally before deploying. Which command runs the Lambda function locally?",
        "options": [
            "A) sam validate",
            "B) sam local invoke",
            "C) sam local start-api",
            "D) sam build"
        ],
        "answer": "B",
        "explanation": "sam local invoke runs a Lambda function locally using Docker. sam local start-api also works but starts a local API server instead of invoking directly."
    },
    {
        "id": "q45",
        "domain": "Deployment",
        "question": "Which Elastic Beanstalk deployment policy is the FASTEST but causes temporary unavailability?",
        "options": [
            "A) All at once",
            "B) Rolling",
            "C) Rolling with additional batch",
            "D) Immutable"
        ],
        "answer": "A",
        "explanation": "All at once deploys to all instances simultaneously, making it the fastest but causes temporary downtime during the deployment."
    },
    # ---- Domain 4: Monitoring & Troubleshooting ----
    {
        "id": "q46",
        "domain": "Monitoring",
        "question": "A developer needs to search through Lambda function logs to find errors. Which tool provides the MOST powerful query capabilities?",
        "options": [
            "A) CloudWatch Logs console with simple text search",
            "B) CloudWatch Logs Insights",
            "C) AWS X-Ray",
            "D) CloudTrail"
        ],
        "answer": "B",
        "explanation": "CloudWatch Logs Insights provides a powerful query language for searching and analyzing log data, including filtering, aggregation, and sorting."
    },
    {
        "id": "q47",
        "domain": "Monitoring",
        "question": "Which AWS service provides a record of API calls made in an AWS account?",
        "options": [
            "A) CloudWatch Logs",
            "B) CloudTrail",
            "C) X-Ray",
            "D) VPC Flow Logs"
        ],
        "answer": "B",
        "explanation": "CloudTrail records API calls made in your AWS account, including who made the call, when, and what resources were affected."
    },
    {
        "id": "q48",
        "domain": "Monitoring",
        "question": "A developer needs to trace requests across multiple Lambda functions and API Gateway. Which service should they enable?",
        "options": [
            "A) CloudWatch Logs",
            "B) CloudTrail",
            "C) AWS X-Ray",
            "D) CloudWatch Alarms"
        ],
        "answer": "C",
        "explanation": "AWS X-Ray provides distributed tracing, allowing you to trace requests across multiple services, visualize service maps, and identify performance bottlenecks."
    },
    {
        "id": "q49",
        "domain": "Monitoring",
        "question": "A Lambda function is timing out when connecting to an RDS database in a VPC. What is the MOST likely cause?",
        "options": [
            "A) The Lambda function has insufficient memory",
            "B) The Lambda function's security group doesn't allow outbound traffic to RDS",
            "C) The Lambda function is not configured to run in the VPC",
            "D) Both B and C could be causes"
        ],
        "answer": "D",
        "explanation": "Lambda functions need to be configured in the correct VPC/subnets with appropriate security groups to access VPC resources like RDS. Either missing VPC config or incorrect security groups can cause timeouts."
    },
    {
        "id": "q50",
        "domain": "Monitoring",
        "question": "Which CloudWatch metric is used to monitor Lambda function invocations?",
        "options": [
            "A) CPUUtilization",
            "B) Invocations",
            "C) RequestCount",
            "D) Throughput"
        ],
        "answer": "B",
        "explanation": "CloudWatch publishes Lambda metrics including Invocations, Duration, Errors, Throttles, and ConcurrentExecutions for monitoring Lambda functions."
    },
    {
        "id": "q51",
        "domain": "Monitoring",
        "question": "A developer wants to create a CloudWatch alarm that triggers when Lambda error rate exceeds 5%. Which metric should they use?",
        "options": [
            "A) Invocations",
            "B) Duration",
            "C) Errors (with math expression Errors/Invocations)",
            "D) Throttles"
        ],
        "answer": "C",
        "explanation": "To calculate error rate, use a metric math expression dividing the Errors metric by the Invocations metric, then set the alarm threshold at 0.05 (5%)."
    },
    {
        "id": "q52",
        "domain": "Monitoring",
        "question": "What is the purpose of a CloudWatch metric filter?",
        "options": [
            "A) To filter which logs are sent to S3",
            "B) To extract metric values from log events",
            "C) To delete old log entries",
            "D) To encrypt log data"
        ],
        "answer": "B",
        "explanation": "Metric filters define patterns to match in log events and turn them into CloudWatch numeric metrics, enabling alarms and dashboards based on log data."
    },
    {
        "id": "q53",
        "domain": "Monitoring",
        "question": "A developer wants to use X-Ray to trace a Lambda function. What is the MINIMUM configuration needed?",
        "options": [
            "A) Install the X-Ray SDK and modify all code",
            "B) Enable X-Ray active tracing on the Lambda function configuration",
            "C) Create a CloudTrail trail",
            "D) Enable VPC Flow Logs"
        ],
        "answer": "B",
        "explanation": "For Lambda, simply enabling active tracing in the function configuration provides basic tracing. The X-Ray SDK is needed only for custom subsegments and annotations."
    },
    {
        "id": "q54",
        "domain": "Monitoring",
        "question": "An API Gateway REST API is returning 429 errors. What should the developer do?",
        "options": [
            "A) Increase the Lambda function memory",
            "B) Enable throttling with appropriate rate and burst limits",
            "C) Switch to a regional API endpoint",
            "D) Disable authentication"
        ],
        "answer": "B",
        "explanation": "429 Too Many Requests indicates throttling. Configure appropriate rate limits and burst limits, or request a limit increase from AWS."
    },
    {
        "id": "q55",
        "domain": "Monitoring",
        "question": "A developer receives a 'ProvisionedThroughputExceededException' from DynamoDB. What is the BEST immediate action?",
        "options": [
            "A) Delete the table and recreate it",
            "B) Switch to on-demand capacity mode or increase provisioned capacity",
            "C) Enable encryption",
            "D) Add a global secondary index"
        ],
        "answer": "B",
        "explanation": "This error means you've exceeded your provisioned throughput. Either switch to on-demand mode (PAY_PER_REQUEST) or increase RCUs/WCUs."
    },
    {
        "id": "q56",
        "domain": "Monitoring",
        "question": "Which X-Ray feature allows searching traces by custom attributes?",
        "options": [
            "A) Annotations",
            "B) Metadata",
            "C) Segments",
            "D) Sampling rules"
        ],
        "answer": "A",
        "explanation": "Annotations are key-value pairs indexed by X-Ray, allowing you to search and filter traces. Metadata is not indexed and cannot be searched."
    },
    {
        "id": "q57",
        "domain": "Monitoring",
        "question": "A Lambda function in a VPC cannot reach the internet. What is missing?",
        "options": [
            "A) More memory",
            "B) A NAT Gateway in the VPC's public subnet",
            "C) A larger timeout",
            "D) An Elastic IP address"
        ],
        "answer": "B",
        "explanation": "Lambda functions in a VPC need a NAT Gateway in a public subnet to reach the internet. The function should be placed in a private subnet with a route to the NAT."
    },
    {
        "id": "q58",
        "domain": "Monitoring",
        "question": "What is the default retention period for CloudWatch Logs?",
        "options": [
            "A) 7 days",
            "B) 30 days",
            "C) Never expire (infinite retention)",
            "D) 90 days"
        ],
        "answer": "C",
        "explanation": "By default, CloudWatch Logs never expire. You can configure a retention period between 1 day and 10 years, or keep data indefinitely."
    },
    {
        "id": "q59",
        "domain": "Monitoring",
        "question": "Which service should be used to monitor API Gateway REST API access logs?",
        "options": [
            "A) CloudTrail only",
            "B) CloudWatch Logs with API Gateway access logging enabled",
            "C) S3 only",
            "D) X-Ray only"
        ],
        "answer": "B",
        "explanation": "API Gateway can be configured to send access logs to CloudWatch Logs, providing detailed request/response information for monitoring and troubleshooting."
    },
    {
        "id": "q60",
        "domain": "Monitoring",
        "question": "A developer needs to be notified when a DynamoDB table's consumed capacity exceeds 80%. What should they configure?",
        "options": [
            "A) A CloudWatch Alarm on the ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits metric",
            "B) A DynamoDB Stream",
            "C) A CloudTrail trail",
            "D) An X-Ray sampling rule"
        ],
        "answer": "A",
        "explanation": "CloudWatch Alarms can monitor DynamoDB capacity metrics (ConsumedReadCapacityUnits, ConsumedWriteCapacityUnits) and trigger notifications via SNS."
    },
    # ---- Additional questions for variety ----
    {
        "id": "q61",
        "domain": "Development",
        "question": "What is the maximum payload size for an SQS message?",
        "options": [
            "A) 64 KB",
            "B) 128 KB",
            "C) 256 KB",
            "D) 1 MB"
        ],
        "answer": "C",
        "explanation": "SQS messages have a maximum size of 256 KB. For larger messages, use S3 to store the payload and pass a reference via SQS."
    },
    {
        "id": "q62",
        "domain": "Development",
        "question": "Which DynamoDB feature captures item-level modifications in a table?",
        "options": [
            "A) Global Secondary Index",
            "B) DynamoDB Streams",
            "C) Time-to-Live (TTL)",
            "D) Point-in-Time Recovery"
        ],
        "answer": "B",
        "explanation": "DynamoDB Streams captures a time-ordered sequence of item-level changes (insert, update, delete) in a table, enabling event-driven processing."
    },
    {
        "id": "q63",
        "domain": "Development",
        "question": "A developer needs to implement a state machine that branches based on output from a Lambda function. Which Step Functions state type should be used?",
        "options": [
            "A) Task",
            "B) Pass",
            "C) Choice",
            "D) Wait"
        ],
        "answer": "C",
        "explanation": "The Choice state evaluates conditions and branches to different states based on the input, similar to an if-else statement."
    },
    {
        "id": "q64",
        "domain": "Security",
        "question": "Which API Gateway authorization type uses a Lambda function to validate tokens?",
        "options": [
            "A) NONE",
            "B) AWS_IAM",
            "C) COGNITO_USER_POOLS",
            "D) CUSTOM (Lambda Authorizer)"
        ],
        "answer": "D",
        "explanation": "Lambda Authorizers (formerly Custom Authorizers) use a Lambda function to evaluate the authorization token and return an IAM policy."
    },
    {
        "id": "q65",
        "domain": "Deployment",
        "question": "What is the purpose of 'sam build' command?",
        "options": [
            "A) To deploy the SAM application",
            "B) To create a deployment artifact by building Lambda functions and copying dependencies",
            "C) To delete a SAM application",
            "D) To test the SAM application in production"
        ],
        "answer": "B",
        "explanation": "sam build processes the SAM template, builds Lambda functions (installing dependencies), and creates deployment artifacts in the .aws-sam directory."
    },
    {
        "id": "q66",
        "domain": "Development",
        "question": "A developer needs to implement a distributed cache that can be shared across multiple Lambda functions. Which service is BEST?",
        "options": [
            "A) Amazon S3",
            "B) Amazon ElastiCache (Redis)",
            "C) Amazon DynamoDB DAX",
            "D) Both B and C are valid options"
        ],
        "answer": "D",
        "explanation": "Both ElastiCache Redis and DynamoDB DAX can serve as distributed caches. Redis is more general-purpose; DAX is specifically for DynamoDB. Both can be shared across Lambda functions."
    },
    {
        "id": "q67",
        "domain": "Deployment",
        "question": "A developer wants to use environment-specific configurations in a SAM template. How can they achieve this?",
        "options": [
            "A) Hardcode values in the template",
            "B) Use SAM template parameters with different values per environment",
            "C) Use separate templates for each environment",
            "D) Use environment variables in CloudFormation"
        ],
        "answer": "B",
        "explanation": "SAM templates support CloudFormation parameters, allowing you to pass environment-specific values (like table names, stage names) at deployment time using parameter overrides."
    },
    {
        "id": "q68",
        "domain": "Monitoring",
        "question": "What is the default sampling rate for X-Ray when no sampling rules are configured?",
        "options": [
            "A) 0% (no traces)",
            "B) 100% (all requests)",
            "C) 1 request per second, then 5% of additional requests",
            "D) 10% of all requests"
        ],
        "answer": "C",
        "explanation": "The default X-Ray sampling rule traces the first request each second, then 5% of additional requests. This ensures some traces while controlling costs."
    },
    {
        "id": "q69",
        "domain": "Development",
        "question": "Which S3 feature allows a Lambda function to be triggered when a new object is created?",
        "options": [
            "A) S3 Lifecycle policies",
            "B) S3 Event Notifications",
            "C) S3 Select",
            "D) S3 Versioning"
        ],
        "answer": "B",
        "explanation": "S3 Event Notifications can trigger Lambda, SNS, or SQS when events like object creation, deletion, or restoration occur in a bucket."
    },
    {
        "id": "q70",
        "domain": "Security",
        "question": "A developer wants to use Cognito to allow unauthenticated guest access to AWS resources. Which Cognito feature supports this?",
        "options": [
            "A) Cognito User Pools",
            "B) Cognito Identity Pools (Federated Identities)",
            "C) Cognito Sync",
            "D) Cognito user groups"
        ],
        "answer": "B",
        "explanation": "Cognito Identity Pools support both authenticated and unauthenticated (guest) identities, providing temporary AWS credentials for accessing resources."
    },
]

# ============================================================
# Generate exams
# ============================================================

def generate_exam(exam_num, questions, num_questions=65):
    """Generate a practice exam from the question bank."""
    # Shuffle questions
    random.seed(exam_num * 42)  # Deterministic per exam number
    shuffled = list(questions)
    random.shuffle(shuffled)
    
    # Select questions
    selected = shuffled[:num_questions]
    
    # Generate markdown
    md = f"""# Practice Exam {exam_num}

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** {len(selected)}
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

"""
    
    for i, q in enumerate(selected, 1):
        md += f"## Question {i}\n\n"
        md += f"**Domain:** {q['domain']}\n\n"
        md += f"{q['question']}\n\n"
        for opt in q['options']:
            md += f"- {opt}\n"
        md += "\n---\n\n"
    
    # Answers section
    md += "\n---\n\n"
    md += "# Answers & Explanations\n\n"
    md += "---\n\n"
    
    for i, q in enumerate(selected, 1):
        md += f"## Question {i} — Answer: {q['answer']}\n\n"
        md += f"**Explanation:** {q['explanation']}\n\n"
        md += "---\n\n"
    
    return md, selected


def generate_all():
    EXAMS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating practice exams...")
    
    # Create an index
    index = """# Practice Exams

**AWS Certified Developer - Associate (DVA-C02)**

## Available Exams

| Exam | Questions | Topics |
|------|-----------|--------|
"""
    
    for exam_num in range(1, 6):
        md, selected = generate_exam(exam_num, QUESTIONS, 65)
        
        # Count by domain
        domains = {}
        for q in selected:
            domains[q['domain']] = domains.get(q['domain'], 0) + 1
        
        filename = f'exam-{exam_num:02d}.md'
        (EXAMS_DIR / filename).write_text(md)
        
        domain_str = ', '.join(f'{d}: {c}' for d, c in sorted(domains.items()))
        index += f"| [Exam {exam_num}](exam-{exam_num:02d}.md) | {len(selected)} | {domain_str} |\n"
        
        print(f"  Created: {filename} ({len(selected)} questions)")
    
    index += """
## How to Use

1. Take each exam under timed conditions (130 minutes)
2. Score yourself using the answer key at the end
3. Review explanations for incorrect answers
4. Focus study on domains where you scored lowest
5. Retake exams after additional study

## Scoring

- Each question is worth equal points
- **Passing Score:** ~72% (720/1000 on the actual exam)
- The actual exam uses scaled scoring

## Domain Weights (Actual Exam)

| Domain | Weight |
|--------|--------|
| Development with AWS Services | 32% |
| Security | 26% |
| Deployment | 24% |
| Monitoring and Troubleshooting | 18% |

## Study Resources

- [Study Guide →](../docs/README.md)
- [Hands-on Exercises →](../exercises/README.md)
"""
    
    (EXAMS_DIR / 'README.md').write_text(index)
    print(f"\nDone! Generated 5 practice exams with {len(QUESTIONS)} unique questions in the bank.")


if __name__ == '__main__':
    generate_all()