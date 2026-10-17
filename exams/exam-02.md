# Practice Exam 2

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Deployment

Which Elastic Beanstalk deployment strategy has the HIGHEST availability but takes the longest?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 2

**Domain:** Development

What is the primary benefit of DynamoDB DAX?

- A) Multi-region active-active writes
- B) Microsecond in-memory caching for DynamoDB read-heavy workloads
- C) Automatic schema migrations
- D) Replacing GSIs entirely

---

## Question 3

**Domain:** Development

A developer needs temporary access for a client to upload a file directly to S3. What is the BEST approach?

- A) Make the bucket public with PutObject allowed
- B) Generate a pre-signed URL with PutObject permission and a short expiry
- C) Embed IAM user credentials in the mobile app
- D) Use CloudFront signed cookies for uploads only

---

## Question 4

**Domain:** Security

A developer needs to securely store a database connection string for a Lambda function. The string needs to be rotated every 30 days. Which solution is BEST?

- A) Store it in a Lambda environment variable
- B) Store it in AWS Secrets Manager with automatic rotation
- C) Store it in S3 with server-side encryption
- D) Store it in AWS Systems Manager Parameter Store as a String type

---

## Question 5

**Domain:** Security

A developer needs to implement API key-based authentication for a public API. Which approach should they use?

- A) IAM authentication on API Gateway
- B) API Gateway with API keys and usage plans
- C) Cognito User Pools
- D) Lambda authorizer that validates API keys

---

## Question 6

**Domain:** Deployment

Which CloudFormation intrinsic function is used to reference a resource's attribute?

- A) Fn::Ref
- B) Fn::GetAtt
- C) Fn::Sub
- D) Fn::Join

---

## Question 7

**Domain:** Development

A Lambda function processes an SQS batch. One message fails. How can the developer avoid reprocessing successful messages?

- A) Disable the event source mapping
- B) Report failures with ReportBatchItemFailures (partial batch response) so only failed message IDs are retried
- C) Increase memory to 10 GB
- D) Switch to SNS

---

## Question 8

**Domain:** Deployment

Which AWS SAM CLI command validates a SAM template locally?

- A) sam validate
- B) sam deploy --no-execute-changeset
- C) sam build --validate
- D) sam local invoke

---

## Question 9

**Domain:** Development

What is the purpose of an SQS dead-letter queue (DLQ)?

- A) To store messages permanently for archival
- B) To receive messages that fail processing after a configured maximum receive count
- C) To replace the visibility timeout mechanism
- D) To fan out messages to multiple consumers

---

## Question 10

**Domain:** Monitoring

A developer needs to trace requests across multiple Lambda functions and API Gateway. Which service should they enable?

- A) CloudWatch Logs
- B) CloudTrail
- C) AWS X-Ray
- D) CloudWatch Alarms

---

## Question 11

**Domain:** Deployment

Which CloudFormation feature imports existing resources into a stack?

- A) StackSets only
- B) Resource import (create change set with Import)
- C) Drift detection exclusively
- D) Termination protection

---

## Question 12

**Domain:** Security

What is the principle of least privilege in AWS IAM?

- A) Granting all permissions to all users
- B) Granting only the minimum permissions needed to perform a task
- C) Using only managed policies
- D) Denying all access by default and using IAM roles only

---

## Question 13

**Domain:** Security

Which AWS service provides automatic rotation of database credentials?

- A) AWS Systems Manager Parameter Store
- B) AWS Secrets Manager
- C) AWS KMS
- D) AWS IAM

---

## Question 14

**Domain:** Security

A developer wants to use temporary credentials to access AWS resources from an on-premises application. Which STS API should they call?

- A) GetSessionToken
- B) AssumeRole
- C) GetFederationToken
- D) DecodeAuthorizationMessage

---

## Question 15

**Domain:** Deployment

What does the 'Transform: AWS::Serverless-2016-10-31' section in a CloudFormation template indicate?

- A) The template is being converted to JSON
- B) The template uses AWS SAM syntax that needs to be transformed to standard CloudFormation
- C) The template is for a legacy application
- D) The template uses CDK constructs

---

## Question 16

**Domain:** Deployment

CodeBuild project environment variables marked as Parameter Store or Secrets Manager type are useful to:

- A) Commit secrets into buildspec.yml in plaintext
- B) Inject secrets at build time without hardcoding them in the repository
- C) Disable CloudWatch Logs for builds
- D) Skip the install phase

---

## Question 17

**Domain:** Development

Which Elasticache engine feature is commonly used for atomic counters and distributed locks?

- A) Redis INCR / SET with NX and expiry
- B) Memcached flush_all only
- C) DynamoDB PutItem
- D) S3 object lock

---

## Question 18

**Domain:** Deployment

A developer needs to deploy a containerized application without managing any infrastructure. Which combination should they use?

- A) EC2 + Docker
- B) ECS with Fargate launch type
- C) ECS with EC2 launch type
- D) Elastic Beanstalk with Docker platform

---

## Question 19

**Domain:** Security

Which KMS operation should be used to encrypt data that is larger than 4KB?

- A) kms:Encrypt
- B) kms:GenerateDataKey
- C) kms:GenerateRandom
- D) kms:ReEncrypt

---

## Question 20

**Domain:** Monitoring

A developer wants to create a CloudWatch alarm that triggers when Lambda error rate exceeds 5%. Which metric should they use?

- A) Invocations
- B) Duration
- C) Errors (with math expression Errors/Invocations)
- D) Throttles

---

## Question 21

**Domain:** Development

When should a developer choose an SQS FIFO queue over a Standard queue?

- A) When maximum throughput is the only priority
- B) When message order and exactly-once processing within a message group are required
- C) When messages must be larger than 256 KB
- D) When messages must be retained for more than 14 days

---

## Question 22

**Domain:** Security

A developer needs to encrypt data larger than 4KB using KMS. What is the recommended approach?

- A) Call KMS Encrypt repeatedly for each 4KB chunk
- B) Use envelope encryption with GenerateDataKey
- C) Use KMS with a larger key size
- D) Compress the data to under 4KB

---

## Question 23

**Domain:** Monitoring

A developer needs to search through Lambda function logs to find errors. Which tool provides the MOST powerful query capabilities?

- A) CloudWatch Logs console with simple text search
- B) CloudWatch Logs Insights
- C) AWS X-Ray
- D) CloudTrail

---

## Question 24

**Domain:** Development

A developer wants EventBridge to route only OrderCreated events with amount > 1000 to a Lambda target. What should they configure?

- A) An SNS filter policy on the Lambda subscription
- B) An EventBridge rule with an event pattern matching source/detail-type and a content filter on amount
- C) An SQS visibility timeout of 1000 seconds
- D) API Gateway request validation only

---

## Question 25

**Domain:** Development

A developer needs to query DynamoDB items by email address, but the table's partition key is userId. What is the BEST solution?

- A) Scan the table filtering on email
- B) Create a GSI with email as the partition key
- C) Export the table to S3 and query with Athena for every request
- D) Store emails only in ElastiCache

---

## Question 26

**Domain:** Security

Which feature of S3 prevents accidental deletion of objects?

- A) Server-side encryption
- B) Versioning with MFA Delete
- C) CORS configuration
- D) Transfer Acceleration

---

## Question 27

**Domain:** Development

A developer needs to process a large CSV file uploaded to S3. The file is 5GB. What is the MOST efficient approach?

- A) Download the entire file in a Lambda function and process it
- B) Use S3 Select to query only the needed data
- C) Copy the file to EBS and process it with EC2
- D) Use S3 Transfer Acceleration

---

## Question 28

**Domain:** Security

A developer needs to encrypt an S3 bucket with a customer-managed KMS key. Which bucket property should they configure?

- A) Bucket policy
- B) Default encryption with SSE-KMS
- C) CORS configuration
- D) Object lock

---

## Question 29

**Domain:** Security

A developer is reviewing an IAM policy and finds: 'Action': 's3:*', 'Resource': '*'. What security concern does this raise?

- A) The policy syntax is invalid
- B) The policy violates least privilege — it grants full S3 access to all buckets
- C) The policy uses a deprecated format
- D) The policy cannot be attached to a role

---

## Question 30

**Domain:** Development

What does DynamoDB TTL (Time to Live) do?

- A) Automatically encrypts items after a timestamp
- B) Deletes expired items near a Unix epoch attribute without consuming write capacity for the delete in the usual way
- C) Creates a GSI for time-based queries
- D) Extends item retention beyond 365 days

---

## Question 31

**Domain:** Development

A developer needs optimistic concurrency control when updating a DynamoDB item. Which feature should they use?

- A) DynamoDB Streams
- B) Conditional expressions (e.g., attribute_exists / version attribute checks)
- C) Scan with ConsistentRead
- D) On-demand capacity mode

---

## Question 32

**Domain:** Deployment

CodeDeploy blue/green for ECS typically involves:

- A) Replacing Lambda layers only
- B) Shifting traffic from an original task set to a replacement task set using a load balancer listener
- C) Deleting the VPC
- D) Disabling CloudWatch

---

## Question 33

**Domain:** Development

A developer wants to ensure exactly-once processing of SQS messages in a Lambda function. What should they do?

- A) Set the visibility timeout to infinity
- B) Use a FIFO queue with content-based deduplication
- C) Delete the message after processing and use idempotent processing logic
- D) Use SNS instead of SQS

---

## Question 34

**Domain:** Development

Which AWS SDK best practice helps applications recover from transient DynamoDB throttling?

- A) Disable retries and fail immediately
- B) Use exponential backoff with jitter (SDK default retries)
- C) Always Switch to Scan
- D) Hardcode higher timeouts only

---

## Question 35

**Domain:** Security

An application running on ECS needs to access DynamoDB. How should the developer configure permissions?

- A) Store access keys in the container image
- B) Use an IAM task role for the ECS task definition
- C) Use EC2 instance profiles
- D) Create a separate IAM user for each container

---

## Question 36

**Domain:** Deployment

A developer wants to share a Lambda function's ARN from one CloudFormation stack to another. How can they do this?

- A) Use Fn::Ref in the second stack
- B) Use Outputs with Export in the first stack and Fn::ImportValue in the second stack
- C) Hardcode the ARN in both stacks
- D) Use SSM parameters automatically

---

## Question 37

**Domain:** Monitoring

A Step Functions execution fails. Where should the developer look FIRST for the failing state and error cause?

- A) The Step Functions console execution history / event details
- B) Only Amazon Macie findings
- C) ECR image scan results
- D) Route 53 health checks

---

## Question 38

**Domain:** Monitoring

Embedded Metric Format (EMF) in CloudWatch is used to:

- A) Embed IAM policies in logs
- B) Emit custom metrics by writing specially formatted JSON log events
- C) Replace CloudTrail
- D) Disable alarms permanently

---

## Question 39

**Domain:** Monitoring

Which AWS service provides a record of API calls made in an AWS account?

- A) CloudWatch Logs
- B) CloudTrail
- C) X-Ray
- D) VPC Flow Logs

---

## Question 40

**Domain:** Deployment

What is the purpose of a buildspec.yml file in AWS CodeBuild?

- A) It defines the infrastructure resources
- B) It contains the build commands and settings for CodeBuild
- C) It configures CodePipeline stages
- D) It defines IAM policies for the build

---

## Question 41

**Domain:** Monitoring

Which CloudWatch metric is used to monitor Lambda function invocations?

- A) CPUUtilization
- B) Invocations
- C) RequestCount
- D) Throughput

---

## Question 42

**Domain:** Monitoring

Lambda Destinations (on success/failure) for asynchronous invocations can send results to:

- A) Only Amazon RDS
- B) SQS, SNS, EventBridge, or another Lambda function
- C) Only CloudFront
- D) Only IAM

---

## Question 43

**Domain:** Deployment

A developer wants to perform blue/green deployments for a Lambda function. Which deployment preference should they use in SAM?

- A) AllAtOnce
- B) Canary10Percent5Minutes
- C) Linear10PercentEvery3Minutes
- D) Rolling

---

## Question 44

**Domain:** Security

Which API Gateway authorization type uses a Lambda function to validate tokens?

- A) NONE
- B) AWS_IAM
- C) COGNITO_USER_POOLS
- D) CUSTOM (Lambda Authorizer)

---

## Question 45

**Domain:** Monitoring

A Lambda function is timing out when connecting to an RDS database in a VPC. What is the MOST likely cause?

- A) The Lambda function has insufficient memory
- B) The Lambda function's security group doesn't allow outbound traffic to RDS
- C) The Lambda function is not configured to run in the VPC
- D) Both B and C could be causes

---

## Question 46

**Domain:** Deployment

CDK bootstrapping (cdk bootstrap) is required to:

- A) Install Node.js
- B) Provision staging resources (S3, IAM roles, ECR) in an environment for CDK deployments
- C) Create Cognito Identity Pools
- D) Enable MFA on the root user

---

## Question 47

**Domain:** Deployment

In a CI/CD pipeline using AWS CodePipeline, which stage is responsible for transforming source code into a deployable artifact?

- A) Source stage
- B) Build stage
- C) Deploy stage
- D) Approval stage

---

## Question 48

**Domain:** Deployment

In CloudFormation, what happens when a stack update fails?

- A) The stack is deleted
- B) Changes are automatically rolled back to the previous known good state
- C) The stack is paused for manual review
- D) Only the failed resource is deleted

---

## Question 49

**Domain:** Development

Which API Gateway integration type passes the entire request/response to/from Lambda without mapping templates?

- A) AWS integration
- B) HTTP integration
- C) Lambda proxy (AWS_PROXY) integration
- D) MOCK integration

---

## Question 50

**Domain:** Security

Which S3 encryption option requires the customer to provide an encryption key with each request?

- A) SSE-S3
- B) SSE-KMS
- C) SSE-C
- D) Client-side encryption with Encryption SDK managed keys stored only in KMS

---

## Question 51

**Domain:** Development

A Kinesis Data Streams consumer must process records in order per shard and checkpoint progress. Which approach is MOST appropriate with Lambda?

- A) Use SQS Standard as the event source instead
- B) Configure Kinesis as a Lambda event source; Lambda manages shard iterators and checkpoints via event source mapping
- C) Poll Kinesis from EC2 without checkpoints
- D) Publish each record to SNS for unordered fan-out

---

## Question 52

**Domain:** Deployment

A developer is using AWS CDK to define infrastructure. Which command generates the CloudFormation template without deploying?

- A) cdk deploy
- B) cdk synth
- C) cdk init
- D) cdk diff

---

## Question 53

**Domain:** Development

API Gateway WebSocket APIs are MOST appropriate when the application needs:

- A) Only synchronous request/response over HTTP
- B) Persistent bidirectional connections for real-time push to clients
- C) File uploads larger than 10 GB
- D) Batch ETL from S3

---

## Question 54

**Domain:** Development

Which DynamoDB operation should be avoided for large tables when filtering by a non-key attribute without an index?

- A) GetItem
- B) Query
- C) Scan
- D) BatchWriteItem

---

## Question 55

**Domain:** Security

What is the difference between a resource-based policy and an identity-based policy in AWS?

- A) They are the same thing
- B) Resource-based policies are attached to resources (like S3 buckets), identity-based policies are attached to IAM principals
- C) Resource-based policies are only for S3
- D) Identity-based policies are more restrictive

---

## Question 56

**Domain:** Security

A developer wants to add a web-based login page to their application using Cognito. Which Cognito feature provides hosted UI authentication?

- A) Cognito Identity Pools
- B) Cognito User Pool hosted UI (App Integration)
- C) Cognito Sync
- D) Cognito user migration Lambda trigger

---

## Question 57

**Domain:** Development

An application needs strongly consistent reads from DynamoDB. What must the developer do?

- A) Enable DynamoDB Streams
- B) Set ConsistentRead=True on GetItem or Query (not available on GSIs)
- C) Use only Scan operations
- D) Switch the table to eventual consistency mode

---

## Question 58

**Domain:** Monitoring

Which alarm action commonly notifies an operations channel when a metric breaches a threshold?

- A) Publish to an SNS topic subscribed by email/Slack/Lambda
- B) Delete the CloudWatch log group
- C) Disable API Gateway
- D) Rotate Cognito clients

---

## Question 59

**Domain:** Security

A developer needs to grant a Lambda function access to read objects from an S3 bucket. What is the MOST secure approach?

- A) Embed AWS access keys in the Lambda function code
- B) Create an IAM role with S3 read permissions and attach it to the Lambda function
- C) Make the S3 bucket public
- D) Use bucket policies that allow anonymous access

---

## Question 60

**Domain:** Development

A Step Functions Map state is used to process a list of items. What does it do?

- A) Waits for human approval
- B) Runs a set of steps for each item in an array, optionally in parallel with MaxConcurrency
- C) Replaces Choice states entirely
- D) Only works with Express workflows

---

## Question 61

**Domain:** Deployment

A developer wants to deploy infrastructure as code for a serverless application. Which tool is PURPOSE-BUILT for this?

- A) AWS CloudFormation directly
- B) AWS SAM (Serverless Application Model)
- C) AWS Elastic Beanstalk
- D) AWS OpsWorks

---

## Question 62

**Domain:** Development

What is the maximum size of a Lambda deployment package (unzipped, including layers) for a zip upload?

- A) 50 MB
- B) 250 MB
- C) 10 GB
- D) 5 MB

---

## Question 63

**Domain:** Security

A company wants to implement user authentication for a web application without managing passwords. Which service should they use?

- A) AWS IAM
- B) Amazon Cognito
- C) AWS Secrets Manager
- D) AWS WAF

---

## Question 64

**Domain:** Monitoring

DynamoDB Contributor Insights helps identify:

- A) The most accessed keys / items causing hot partitions or heavy traffic
- B) KMS key rotation status only
- C) S3 storage class transitions
- D) Cognito password policies

---

## Question 65

**Domain:** Development

An SNS topic must deliver only messages with attribute orderType=express to a subscribed SQS queue. What should be configured?

- A) SQS redrive policy
- B) SNS subscription filter policy matching orderType=express
- C) Kinesis shard key
- D) API Gateway usage plan

---


---

# Answers & Explanations

---

## Question 1 — Answer: D

**Explanation:** Immutable deployment creates a completely new set of instances, ensuring full availability during deployment. It's the safest but slowest and most expensive option.

---

## Question 2 — Answer: B

**Explanation:** DAX is a write-through cache for DynamoDB that can reduce read latency to microseconds for cache hits.

---

## Question 3 — Answer: B

**Explanation:** Pre-signed URLs grant time-limited permission to perform a specific S3 action without exposing long-lived credentials or opening the bucket publicly.

---

## Question 4 — Answer: B

**Explanation:** Secrets Manager supports automatic rotation (configurable schedule), which meets the 30-day rotation requirement. Parameter Store SecureString can encrypt but doesn't provide automatic rotation.

---

## Question 5 — Answer: B

**Explanation:** API Gateway provides built-in API key management with usage plans for throttling and quotas. This is designed for public APIs where you want to track and control usage.

---

## Question 6 — Answer: B

**Explanation:** Fn::GetAtt returns the value of an attribute from a resource in the template, such as a Lambda function's Arn or an S3 bucket's DomainName.

---

## Question 7 — Answer: B

**Explanation:** Partial batch responses let Lambda tell SQS which message IDs failed; only those become visible again. Successful messages are deleted.

---

## Question 8 — Answer: A

**Explanation:** sam validate checks the SAM template for syntax and structural errors. It can validate both SAM and CloudFormation templates.

---

## Question 9 — Answer: B

**Explanation:** A DLQ captures messages that repeatedly fail processing (after maxReceiveCount), enabling inspection, alerting, and reprocessing without blocking the main queue.

---

## Question 10 — Answer: C

**Explanation:** AWS X-Ray provides distributed tracing, allowing you to trace requests across multiple services, visualize service maps, and identify performance bottlenecks.

---

## Question 11 — Answer: B

**Explanation:** Resource import brings existing resources under CloudFormation management using an import change set and a template that matches current configuration.

---

## Question 12 — Answer: B

**Explanation:** Least privilege means granting only the permissions needed for a specific task. This reduces the blast radius of compromised credentials.

---

## Question 13 — Answer: B

**Explanation:** AWS Secrets Manager provides automatic credential rotation for databases and other services. Parameter Store can store secrets but doesn't provide automatic rotation.

---

## Question 14 — Answer: B

**Explanation:** AssumeRole returns temporary credentials (access key, secret key, session token) that can be used to access AWS resources. It's the standard way to obtain temporary credentials for cross-account or on-premises access.

---

## Question 15 — Answer: B

**Explanation:** The Transform section tells CloudFormation to use the SAM transform, which converts SAM-specific resource types into standard CloudFormation resources.

---

## Question 16 — Answer: B

**Explanation:** CodeBuild can resolve environment variables from SSM or Secrets Manager at runtime so secrets stay out of source control.

---

## Question 17 — Answer: A

**Explanation:** Redis supports atomic operations such as INCR and SET NX EX, which are commonly used for counters and simple distributed locks.

---

## Question 18 — Answer: B

**Explanation:** ECS with Fargate eliminates infrastructure management for containers. Fargate provisions and manages the underlying compute resources automatically.

---

## Question 19 — Answer: B

**Explanation:** GenerateDataKey returns a plaintext data key and an encrypted copy. Use the plaintext key to encrypt data locally (envelope encryption), then store the encrypted key with the data.

---

## Question 20 — Answer: C

**Explanation:** To calculate error rate, use a metric math expression dividing Errors by Invocations, then set the alarm threshold at 0.05 (5%).

---

## Question 21 — Answer: B

**Explanation:** FIFO queues provide ordering and exactly-once processing within a message group ID. Standard queues prioritize higher throughput with at-least-once delivery.

---

## Question 22 — Answer: B

**Explanation:** Envelope encryption uses KMS to generate a data key, which is then used to encrypt the actual data locally. This avoids KMS size limits and reduces KMS API calls.

---

## Question 23 — Answer: B

**Explanation:** CloudWatch Logs Insights provides a powerful query language for searching and analyzing log data, including filtering, aggregation, and sorting.

---

## Question 24 — Answer: B

**Explanation:** EventBridge rules use event patterns (and content filtering) to match specific events and fields before invoking targets like Lambda.

---

## Question 25 — Answer: B

**Explanation:** A GSI with email as partition key enables efficient Query access by email without expensive Scans.

---

## Question 26 — Answer: B

**Explanation:** MFA Delete requires multi-factor authentication to delete objects or disable versioning, providing strong protection against accidental or malicious deletion.

---

## Question 27 — Answer: B

**Explanation:** S3 Select allows you to retrieve only the needed data from a CSV file using SQL expressions, reducing data transfer and processing time significantly.

---

## Question 28 — Answer: B

**Explanation:** S3 default encryption with SSE-KMS uses a customer-managed CMK. This automatically encrypts all new objects with the specified KMS key.

---

## Question 29 — Answer: B

**Explanation:** Using wildcards for both Action and Resource violates least privilege. The policy grants all S3 actions on all buckets, which is overly permissive.

---

## Question 30 — Answer: B

**Explanation:** TTL marks items for expiration based on a numeric epoch attribute; DynamoDB deletes them asynchronously. Ideal for sessions and temporary data.

---

## Question 31 — Answer: B

**Explanation:** Conditional writes (ConditionExpression) implement optimistic locking by failing updates when expected attribute values (like a version) do not match.

---

## Question 32 — Answer: B

**Explanation:** ECS blue/green with CodeDeploy creates a new task set and shifts load balancer traffic gradually or all at once to the replacement set.

---

## Question 33 — Answer: C

**Explanation:** SQS provides at-least-once delivery. For exactly-once semantics, delete messages after successful processing and design idempotent processing logic that can handle duplicate deliveries safely.

---

## Question 34 — Answer: B

**Explanation:** AWS SDKs retry throttling errors with exponential backoff. Applications should also consider on-demand capacity or capacity adjustments for sustained load.

---

## Question 35 — Answer: B

**Explanation:** ECS task roles (taskRoleArn) provide temporary credentials to containers, following the same IAM role pattern as Lambda execution roles.

---

## Question 36 — Answer: B

**Explanation:** CloudFormation cross-stack references use Outputs with Export Name in one stack and Fn::ImportValue in another to share values between stacks.

---

## Question 37 — Answer: A

**Explanation:** Step Functions execution event history shows each state transition, inputs/outputs, and error causes for failed steps.

---

## Question 38 — Answer: B

**Explanation:** EMF lets applications put custom metrics via structured logs that CloudWatch extracts without separate PutMetricData calls.

---

## Question 39 — Answer: B

**Explanation:** CloudTrail records API calls made in your AWS account, including who made the call, when, and what resources were affected.

---

## Question 40 — Answer: B

**Explanation:** The buildspec.yml defines the build phases (install, pre_build, build, post_build), environment variables, and artifacts for CodeBuild.

---

## Question 41 — Answer: B

**Explanation:** CloudWatch publishes Lambda metrics including Invocations, Duration, Errors, Throttles, and ConcurrentExecutions.

---

## Question 42 — Answer: B

**Explanation:** Lambda Destinations route async invocation records to SQS, SNS, EventBridge, or Lambda for success or failure handling.

---

## Question 43 — Answer: B

**Explanation:** Canary10Percent5Minutes shifts 10% of traffic to the new version, waits 5 minutes, then shifts the remaining 90%. This is a blue/green-style canary for Lambda.

---

## Question 44 — Answer: D

**Explanation:** Lambda Authorizers (formerly Custom Authorizers) use a Lambda function to evaluate the authorization token and return an IAM policy.

---

## Question 45 — Answer: D

**Explanation:** Lambda functions need to be configured in the correct VPC/subnets with appropriate security groups to access VPC resources like RDS.

---

## Question 46 — Answer: B

**Explanation:** Bootstrap creates the CDK toolkit stack with assets bucket and deployment roles needed for cdk deploy in that account/region.

---

## Question 47 — Answer: B

**Explanation:** The Build stage (typically using CodeBuild) compiles source code, runs tests, and produces deployable artifacts like Lambda deployment packages or Docker images.

---

## Question 48 — Answer: B

**Explanation:** CloudFormation automatically rolls back changes on failure by default. All changes made during the update are reverted to the previous stable state.

---

## Question 49 — Answer: C

**Explanation:** Lambda proxy integration forwards the full request to Lambda and expects a structured response (statusCode, headers, body), simplifying API wiring.

---

## Question 50 — Answer: C

**Explanation:** SSE-C (customer-provided keys) requires the client to supply the encryption key on each upload/download request.

---

## Question 51 — Answer: B

**Explanation:** Lambda event source mappings for Kinesis poll shards, invoke with batches, and checkpoint on success, preserving per-shard order.

---

## Question 52 — Answer: B

**Explanation:** cdk synth (synthesize) generates the CloudFormation template from CDK code without deploying. This is useful for reviewing changes before deployment.

---

## Question 53 — Answer: B

**Explanation:** WebSocket APIs maintain persistent connections and allow the server to push messages to connected clients for chat, notifications, and similar use cases.

---

## Question 54 — Answer: C

**Explanation:** Scan reads every item and is inefficient/expensive on large tables. Prefer Query with a proper key design or GSI for non-key access patterns.

---

## Question 55 — Answer: B

**Explanation:** Resource-based policies are attached to resources and define who can access them. Identity-based policies are attached to IAM users, groups, or roles and define what they can access.

---

## Question 56 — Answer: B

**Explanation:** Cognito User Pools provide a hosted UI for authentication that can be customized, supporting social providers and SAML, without building your own login page.

---

## Question 57 — Answer: B

**Explanation:** Strongly consistent reads are requested via ConsistentRead=True on GetItem/Query against the base table. GSIs support only eventually consistent reads.

---

## Question 58 — Answer: A

**Explanation:** CloudWatch Alarms typically notify via SNS, which fans out to email, chat integrations, Lambda, and other subscribers.

---

## Question 59 — Answer: B

**Explanation:** IAM roles provide temporary credentials automatically rotated by AWS. This is the secure best practice — never embed credentials in code or make resources public unnecessarily.

---

## Question 60 — Answer: B

**Explanation:** Map iterates over an array and runs a processor state machine for each element, with optional concurrency limits for fan-out processing.

---

## Question 61 — Answer: B

**Explanation:** AWS SAM is a framework for building serverless applications, providing simplified syntax for Lambda functions, API Gateway, and DynamoDB tables.

---

## Question 62 — Answer: B

**Explanation:** The unzipped deployment package size limit (including layers) is 250 MB. Container images support larger packages up to 10 GB.

---

## Question 63 — Answer: B

**Explanation:** Amazon Cognito provides user authentication, sign-up, and sign-in functionality for web and mobile applications, supporting social identity providers and SAML.

---

## Question 64 — Answer: A

**Explanation:** Contributor Insights surfaces frequently accessed keys and traffic patterns useful for diagnosing hot partitions.

---

## Question 65 — Answer: B

**Explanation:** SNS filter policies on subscriptions deliver only messages whose attributes (or payload attributes) match the filter criteria.

---

