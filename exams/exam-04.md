# Practice Exam 4

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Security

What is the difference between a resource-based policy and an identity-based policy in AWS?

- A) They are the same thing
- B) Resource-based policies are attached to resources (like S3 buckets), identity-based policies are attached to IAM principals
- C) Resource-based policies are only for S3
- D) Identity-based policies are more restrictive

---

## Question 2

**Domain:** Security

Which AWS service provides automatic rotation of database credentials?

- A) AWS Systems Manager Parameter Store
- B) AWS Secrets Manager
- C) AWS KMS
- D) AWS IAM

---

## Question 3

**Domain:** Development

An application needs strongly consistent reads from DynamoDB. What must the developer do?

- A) Enable DynamoDB Streams
- B) Set ConsistentRead=True on GetItem or Query (not available on GSIs)
- C) Use only Scan operations
- D) Switch the table to eventual consistency mode

---

## Question 4

**Domain:** Monitoring

DynamoDB Contributor Insights helps identify:

- A) The most accessed keys / items causing hot partitions or heavy traffic
- B) KMS key rotation status only
- C) S3 storage class transitions
- D) Cognito password policies

---

## Question 5

**Domain:** Monitoring

What is CloudWatch Logs subscription filter used for?

- A) Encrypting log groups with SSE-S3 only
- B) Streaming matching log events in near real time to Kinesis, Firehose, or Lambda
- C) Deleting empty log streams
- D) Replacing metric filters entirely with no metrics

---

## Question 6

**Domain:** Security

A developer needs client-side encryption of objects before uploading to S3. Which approach meets this requirement?

- A) Rely only on SSE-S3 after upload
- B) Encrypt data in the application (e.g., AWS Encryption SDK) before PutObject
- C) Enable Transfer Acceleration
- D) Use only CloudWatch Logs encryption

---

## Question 7

**Domain:** Development

A developer needs temporary access for a client to upload a file directly to S3. What is the BEST approach?

- A) Make the bucket public with PutObject allowed
- B) Generate a pre-signed URL with PutObject permission and a short expiry
- C) Embed IAM user credentials in the mobile app
- D) Use CloudFront signed cookies for uploads only

---

## Question 8

**Domain:** Monitoring

A developer needs structured logging from Lambda for easier querying. What is a recommended practice?

- A) Print unstructured free-form strings only
- B) Emit JSON log lines with consistent fields (level, requestId, message) to stdout
- C) Disable CloudWatch Logs
- D) Log only to local disk

---

## Question 9

**Domain:** Development

Which Elasticache engine feature is commonly used for atomic counters and distributed locks?

- A) Redis INCR / SET with NX and expiry
- B) Memcached flush_all only
- C) DynamoDB PutItem
- D) S3 object lock

---

## Question 10

**Domain:** Deployment

SAM Globals section is used to:

- A) Define account-wide SCPs
- B) Set default properties shared by serverless resources (Runtime, Timeout, Environment, etc.)
- C) Replace Parameters
- D) Configure Organization trails

---

## Question 11

**Domain:** Deployment

A developer is using AWS CDK to define infrastructure. Which command generates the CloudFormation template without deploying?

- A) cdk deploy
- B) cdk synth
- C) cdk init
- D) cdk diff

---

## Question 12

**Domain:** Deployment

CodeDeploy blue/green for ECS typically involves:

- A) Replacing Lambda layers only
- B) Shifting traffic from an original task set to a replacement task set using a load balancer listener
- C) Deleting the VPC
- D) Disabling CloudWatch

---

## Question 13

**Domain:** Monitoring

Which tool helps determine if CloudFormation stack resources have drifted from the template?

- A) CloudFormation drift detection
- B) Amazon Polly
- C) AWS Snowball
- D) Amazon Rekognition

---

## Question 14

**Domain:** Deployment

CDK bootstrapping (cdk bootstrap) is required to:

- A) Install Node.js
- B) Provision staging resources (S3, IAM roles, ECR) in an environment for CDK deployments
- C) Create Cognito Identity Pools
- D) Enable MFA on the root user

---

## Question 15

**Domain:** Security

A company wants to implement user authentication for a web application without managing passwords. Which service should they use?

- A) AWS IAM
- B) Amazon Cognito
- C) AWS Secrets Manager
- D) AWS WAF

---

## Question 16

**Domain:** Deployment

A developer wants to deploy infrastructure as code for a serverless application. Which tool is PURPOSE-BUILT for this?

- A) AWS CloudFormation directly
- B) AWS SAM (Serverless Application Model)
- C) AWS Elastic Beanstalk
- D) AWS OpsWorks

---

## Question 17

**Domain:** Monitoring

To capture failed asynchronous Lambda invocations for later analysis, configure:

- A) A dead-letter queue (SQS/SNS) or Lambda destination on failure
- B) Only S3 Transfer Acceleration
- C) Cognito hosted UI
- D) CloudFront signed URLs

---

## Question 18

**Domain:** Development

What does DynamoDB TTL (Time to Live) do?

- A) Automatically encrypts items after a timestamp
- B) Deletes expired items near a Unix epoch attribute without consuming write capacity for the delete in the usual way
- C) Creates a GSI for time-based queries
- D) Extends item retention beyond 365 days

---

## Question 19

**Domain:** Deployment

Which CloudFormation intrinsic function is used to reference a resource's attribute?

- A) Fn::Ref
- B) Fn::GetAtt
- C) Fn::Sub
- D) Fn::Join

---

## Question 20

**Domain:** Deployment

What does AWS::Serverless::Function Events property typically configure?

- A) Only CloudTrail events
- B) Event sources such as API Gateway, S3, SQS, SNS, DynamoDB Streams, Schedule, etc.
- C) VPC Flow Logs exclusively
- D) KMS key rotation schedule

---

## Question 21

**Domain:** Security

A developer needs to securely store a database connection string for a Lambda function. The string needs to be rotated every 30 days. Which solution is BEST?

- A) Store it in a Lambda environment variable
- B) Store it in AWS Secrets Manager with automatic rotation
- C) Store it in S3 with server-side encryption
- D) Store it in AWS Systems Manager Parameter Store as a String type

---

## Question 22

**Domain:** Security

What is the principle of least privilege in AWS IAM?

- A) Granting all permissions to all users
- B) Granting only the minimum permissions needed to perform a task
- C) Using only managed policies
- D) Denying all access by default and using IAM roles only

---

## Question 23

**Domain:** Security

Which S3 encryption option requires the customer to provide an encryption key with each request?

- A) SSE-S3
- B) SSE-KMS
- C) SSE-C
- D) Client-side encryption with Encryption SDK managed keys stored only in KMS

---

## Question 24

**Domain:** Development

A developer needs optimistic concurrency control when updating a DynamoDB item. Which feature should they use?

- A) DynamoDB Streams
- B) Conditional expressions (e.g., attribute_exists / version attribute checks)
- C) Scan with ConsistentRead
- D) On-demand capacity mode

---

## Question 25

**Domain:** Security

An application running on ECS needs to access DynamoDB. How should the developer configure permissions?

- A) Store access keys in the container image
- B) Use an IAM task role for the ECS task definition
- C) Use EC2 instance profiles
- D) Create a separate IAM user for each container

---

## Question 26

**Domain:** Development

A Lambda function must share initialization cost across many invocations. Where should expensive SDK clients be created?

- A) Inside the handler on every invocation
- B) Outside the handler (global/module scope) so warm containers reuse them
- C) In a separate Lambda Layer that runs at invoke time
- D) In the API Gateway request mapping template

---

## Question 27

**Domain:** Deployment

In a CI/CD pipeline using AWS CodePipeline, which stage is responsible for transforming source code into a deployable artifact?

- A) Source stage
- B) Build stage
- C) Deploy stage
- D) Approval stage

---

## Question 28

**Domain:** Monitoring

Which Lambda metric indicates how long the initialization (cold start) phase took?

- A) Init Duration (reported in REPORT / Performance metrics where available)
- B) ApproximateNumberOfMessagesVisible
- C) BucketSizeBytes
- D) HealthyHostCount

---

## Question 29

**Domain:** Security

A developer wants to add a web-based login page to their application using Cognito. Which Cognito feature provides hosted UI authentication?

- A) Cognito Identity Pools
- B) Cognito User Pool hosted UI (App Integration)
- C) Cognito Sync
- D) Cognito user migration Lambda trigger

---

## Question 30

**Domain:** Development

A Lambda function is experiencing cold start latency. Which approach would BEST reduce this?

- A) Increase the Lambda memory allocation
- B) Use Provisioned Concurrency
- C) Add more code to the Lambda function
- D) Decrease the timeout setting

---

## Question 31

**Domain:** Deployment

What does the 'Transform: AWS::Serverless-2016-10-31' section in a CloudFormation template indicate?

- A) The template is being converted to JSON
- B) The template uses AWS SAM syntax that needs to be transformed to standard CloudFormation
- C) The template is for a legacy application
- D) The template uses CDK constructs

---

## Question 32

**Domain:** Development

A Kinesis Data Streams consumer must process records in order per shard and checkpoint progress. Which approach is MOST appropriate with Lambda?

- A) Use SQS Standard as the event source instead
- B) Configure Kinesis as a Lambda event source; Lambda manages shard iterators and checkpoints via event source mapping
- C) Poll Kinesis from EC2 without checkpoints
- D) Publish each record to SNS for unordered fan-out

---

## Question 33

**Domain:** Monitoring

An X-Ray service map shows a node with a high fault rate. Faults typically indicate:

- A) Successful 2xx responses
- B) 5xx errors / server-side failures in the traced service
- C) Only cold starts
- D) Missing IAM roles exclusively

---

## Question 34

**Domain:** Development

What is the maximum payload size for an SQS message?

- A) 64 KB
- B) 128 KB
- C) 256 KB
- D) 1 MB

---

## Question 35

**Domain:** Development

Which API Gateway integration type passes the entire request/response to/from Lambda without mapping templates?

- A) AWS integration
- B) HTTP integration
- C) Lambda proxy (AWS_PROXY) integration
- D) MOCK integration

---

## Question 36

**Domain:** Monitoring

A developer enables X-Ray tracing on API Gateway. What additional step helps end-to-end traces into Lambda?

- A) Disable Lambda logs
- B) Enable active tracing on the Lambda function as well
- C) Delete the API stage
- D) Use only MOCK integrations

---

## Question 37

**Domain:** Deployment

CloudFormation stack policies are used to:

- A) Encrypt all parameters automatically
- B) Prevent updates to critical resources during stack updates unless explicitly allowed
- C) Replace IAM identity policies
- D) Speed up rollbacks only

---

## Question 38

**Domain:** Security

Which feature of S3 prevents accidental deletion of objects?

- A) Server-side encryption
- B) Versioning with MFA Delete
- C) CORS configuration
- D) Transfer Acceleration

---

## Question 39

**Domain:** Monitoring

API Gateway integration latency vs latency metrics differ how?

- A) They are identical always
- B) Latency includes overhead end-to-end at API Gateway; IntegrationLatency measures time spent calling the backend
- C) IntegrationLatency includes client network only
- D) Neither is published to CloudWatch

---

## Question 40

**Domain:** Security

A developer needs to implement API key-based authentication for a public API. Which approach should they use?

- A) IAM authentication on API Gateway
- B) API Gateway with API keys and usage plans
- C) Cognito User Pools
- D) Lambda authorizer that validates API keys

---

## Question 41

**Domain:** Development

Which S3 feature allows a Lambda function to be triggered when a new object is created?

- A) S3 Lifecycle policies
- B) S3 Event Notifications
- C) S3 Select
- D) S3 Versioning

---

## Question 42

**Domain:** Security

A developer needs to grant a Lambda function access to read objects from an S3 bucket. What is the MOST secure approach?

- A) Embed AWS access keys in the Lambda function code
- B) Create an IAM role with S3 read permissions and attach it to the Lambda function
- C) Make the S3 bucket public
- D) Use bucket policies that allow anonymous access

---

## Question 43

**Domain:** Deployment

CodeBuild project environment variables marked as Parameter Store or Secrets Manager type are useful to:

- A) Commit secrets into buildspec.yml in plaintext
- B) Inject secrets at build time without hardcoding them in the repository
- C) Disable CloudWatch Logs for builds
- D) Skip the install phase

---

## Question 44

**Domain:** Development

Which DynamoDB operation should be avoided for large tables when filtering by a non-key attribute without an index?

- A) GetItem
- B) Query
- C) Scan
- D) BatchWriteItem

---

## Question 45

**Domain:** Monitoring

Which CloudWatch Logs Insights query finds the 10 slowest Lambda durations from REPORT lines?

- A) DELETE FROM log_group
- B) A query filtering REPORT lines, parsing Duration, sorting desc, and limiting 10
- C) SELECT * FROM dynamodb
- D) Only the X-Ray console can do this

---

## Question 46

**Domain:** Security

A developer wants to use temporary credentials to access AWS resources from an on-premises application. Which STS API should they call?

- A) GetSessionToken
- B) AssumeRole
- C) GetFederationToken
- D) DecodeAuthorizationMessage

---

## Question 47

**Domain:** Development

When should a developer choose an SQS FIFO queue over a Standard queue?

- A) When maximum throughput is the only priority
- B) When message order and exactly-once processing within a message group are required
- C) When messages must be larger than 256 KB
- D) When messages must be retained for more than 14 days

---

## Question 48

**Domain:** Deployment

Which CloudFormation feature imports existing resources into a stack?

- A) StackSets only
- B) Resource import (create change set with Import)
- C) Drift detection exclusively
- D) Termination protection

---

## Question 49

**Domain:** Development

A developer wants EventBridge to route only OrderCreated events with amount > 1000 to a Lambda target. What should they configure?

- A) An SNS filter policy on the Lambda subscription
- B) An EventBridge rule with an event pattern matching source/detail-type and a content filter on amount
- C) An SQS visibility timeout of 1000 seconds
- D) API Gateway request validation only

---

## Question 50

**Domain:** Deployment

A developer wants to perform blue/green deployments for a Lambda function. Which deployment preference should they use in SAM?

- A) AllAtOnce
- B) Canary10Percent5Minutes
- C) Linear10PercentEvery3Minutes
- D) Rolling

---

## Question 51

**Domain:** Development

A Step Functions Map state is used to process a list of items. What does it do?

- A) Waits for human approval
- B) Runs a set of steps for each item in an array, optionally in parallel with MaxConcurrency
- C) Replaces Choice states entirely
- D) Only works with Express workflows

---

## Question 52

**Domain:** Security

A developer needs to encrypt data larger than 4KB using KMS. What is the recommended approach?

- A) Call KMS Encrypt repeatedly for each 4KB chunk
- B) Use envelope encryption with GenerateDataKey
- C) Use KMS with a larger key size
- D) Compress the data to under 4KB

---

## Question 53

**Domain:** Security

A developer is reviewing an IAM policy and finds: 'Action': 's3:*', 'Resource': '*'. What security concern does this raise?

- A) The policy syntax is invalid
- B) The policy violates least privilege — it grants full S3 access to all buckets
- C) The policy uses a deprecated format
- D) The policy cannot be attached to a role

---

## Question 54

**Domain:** Development

When building a DynamoDB table for an e-commerce application, which access pattern requires a Global Secondary Index (GSI)?

- A) Get order by orderId (partition key)
- B) Get all orders for a customer sorted by date (composite key)
- C) Get all orders with status 'PENDING' regardless of customer
- D) Delete an order by orderId

---

## Question 55

**Domain:** Development

What is the purpose of an SQS dead-letter queue (DLQ)?

- A) To store messages permanently for archival
- B) To receive messages that fail processing after a configured maximum receive count
- C) To replace the visibility timeout mechanism
- D) To fan out messages to multiple consumers

---

## Question 56

**Domain:** Security

SSM Parameter Store hierarchical paths (e.g., /myapp/prod/db) are useful primarily to:

- A) Automatically rotate passwords
- B) Organize parameters and apply IAM path-based access control with GetParametersByPath
- C) Replace KMS entirely
- D) Create VPC endpoints

---

## Question 57

**Domain:** Security

Which KMS operation should be used to encrypt data that is larger than 4KB?

- A) kms:Encrypt
- B) kms:GenerateDataKey
- C) kms:GenerateRandom
- D) kms:ReEncrypt

---

## Question 58

**Domain:** Monitoring

CloudWatch alarm state INSUFFICIENT_DATA usually means:

- A) The alarm threshold was breached
- B) Not enough data points are available yet for the configured evaluation period
- C) The AWS account was suspended
- D) X-Ray tracing is mandatory

---

## Question 59

**Domain:** Deployment

Which Elastic Beanstalk deployment strategy has the HIGHEST availability but takes the longest?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 60

**Domain:** Development

A developer needs to implement a state machine that branches based on output from a Lambda function. Which Step Functions state type should be used?

- A) Task
- B) Pass
- C) Choice
- D) Wait

---

## Question 61

**Domain:** Deployment

Which artifact store does CodePipeline commonly use between stages?

- A) Amazon S3
- B) Amazon Neptune
- C) Amazon MQ
- D) Amazon Lex

---

## Question 62

**Domain:** Development

A developer needs to process a large CSV file uploaded to S3. The file is 5GB. What is the MOST efficient approach?

- A) Download the entire file in a Lambda function and process it
- B) Use S3 Select to query only the needed data
- C) Copy the file to EBS and process it with EC2
- D) Use S3 Transfer Acceleration

---

## Question 63

**Domain:** Development

A developer needs to implement a distributed cache that can be shared across multiple Lambda functions. Which service is BEST?

- A) Amazon S3
- B) Amazon ElastiCache (Redis)
- C) Amazon DynamoDB DAX
- D) Both B and C are valid options

---

## Question 64

**Domain:** Deployment

Elastic Beanstalk .ebextensions configuration files are used to:

- A) Define Lambda layers
- B) Customize environment configuration (packages, files, option settings) during deployment
- C) Create Cognito User Pools
- D) Configure X-Ray sampling only

---

## Question 65

**Domain:** Development

Which DynamoDB feature captures item-level modifications in a table?

- A) Global Secondary Index
- B) DynamoDB Streams
- C) Time-to-Live (TTL)
- D) Point-in-Time Recovery

---


---

# Answers & Explanations

---

## Question 1 — Answer: B

**Explanation:** Resource-based policies are attached to resources and define who can access them. Identity-based policies are attached to IAM users, groups, or roles and define what they can access.

---

## Question 2 — Answer: B

**Explanation:** AWS Secrets Manager provides automatic credential rotation for databases and other services. Parameter Store can store secrets but doesn't provide automatic rotation.

---

## Question 3 — Answer: B

**Explanation:** Strongly consistent reads are requested via ConsistentRead=True on GetItem/Query against the base table. GSIs support only eventually consistent reads.

---

## Question 4 — Answer: A

**Explanation:** Contributor Insights surfaces frequently accessed keys and traffic patterns useful for diagnosing hot partitions.

---

## Question 5 — Answer: B

**Explanation:** Subscription filters deliver real-time log events matching a filter pattern to streaming or Lambda destinations for processing.

---

## Question 6 — Answer: B

**Explanation:** Client-side encryption encrypts data before it leaves the client. Server-side encryption (SSE-*) encrypts after S3 receives the object.

---

## Question 7 — Answer: B

**Explanation:** Pre-signed URLs grant time-limited permission to perform a specific S3 action without exposing long-lived credentials or opening the bucket publicly.

---

## Question 8 — Answer: B

**Explanation:** JSON structured logs work well with Logs Insights filters/parses and make correlation by requestId easier.

---

## Question 9 — Answer: A

**Explanation:** Redis supports atomic operations such as INCR and SET NX EX, which are commonly used for counters and simple distributed locks.

---

## Question 10 — Answer: B

**Explanation:** Globals reduce duplication by applying common Function/Api/SimpleTable properties across SAM resources.

---

## Question 11 — Answer: B

**Explanation:** cdk synth (synthesize) generates the CloudFormation template from CDK code without deploying. This is useful for reviewing changes before deployment.

---

## Question 12 — Answer: B

**Explanation:** ECS blue/green with CodeDeploy creates a new task set and shifts load balancer traffic gradually or all at once to the replacement set.

---

## Question 13 — Answer: A

**Explanation:** Drift detection compares actual resource configuration with the stack template and reports differences.

---

## Question 14 — Answer: B

**Explanation:** Bootstrap creates the CDK toolkit stack with assets bucket and deployment roles needed for cdk deploy in that account/region.

---

## Question 15 — Answer: B

**Explanation:** Amazon Cognito provides user authentication, sign-up, and sign-in functionality for web and mobile applications, supporting social identity providers and SAML.

---

## Question 16 — Answer: B

**Explanation:** AWS SAM is a framework for building serverless applications, providing simplified syntax for Lambda functions, API Gateway, and DynamoDB tables.

---

## Question 17 — Answer: A

**Explanation:** Async Lambda failures can be routed to a DLQ or on-failure destination (SQS, SNS, EventBridge, another Lambda) for inspection and retry.

---

## Question 18 — Answer: B

**Explanation:** TTL marks items for expiration based on a numeric epoch attribute; DynamoDB deletes them asynchronously. Ideal for sessions and temporary data.

---

## Question 19 — Answer: B

**Explanation:** Fn::GetAtt returns the value of an attribute from a resource in the template, such as a Lambda function's Arn or an S3 bucket's DomainName.

---

## Question 20 — Answer: B

**Explanation:** SAM Events attach triggers to Lambda (HTTP APIs, queues, topics, schedules, and more) with simplified syntax.

---

## Question 21 — Answer: B

**Explanation:** Secrets Manager supports automatic rotation (configurable schedule), which meets the 30-day rotation requirement. Parameter Store SecureString can encrypt but doesn't provide automatic rotation.

---

## Question 22 — Answer: B

**Explanation:** Least privilege means granting only the permissions needed for a specific task. This reduces the blast radius of compromised credentials.

---

## Question 23 — Answer: C

**Explanation:** SSE-C (customer-provided keys) requires the client to supply the encryption key on each upload/download request.

---

## Question 24 — Answer: B

**Explanation:** Conditional writes (ConditionExpression) implement optimistic locking by failing updates when expected attribute values (like a version) do not match.

---

## Question 25 — Answer: B

**Explanation:** ECS task roles (taskRoleArn) provide temporary credentials to containers, following the same IAM role pattern as Lambda execution roles.

---

## Question 26 — Answer: B

**Explanation:** Code outside the handler runs during cold start and is reused for warm invocations. Initialize clients once at module scope for better performance.

---

## Question 27 — Answer: B

**Explanation:** The Build stage (typically using CodeBuild) compiles source code, runs tests, and produces deployable artifacts like Lambda deployment packages or Docker images.

---

## Question 28 — Answer: A

**Explanation:** Cold start initialization time appears as Init Duration in Lambda REPORT logs and related performance metrics.

---

## Question 29 — Answer: B

**Explanation:** Cognito User Pools provide a hosted UI for authentication that can be customized, supporting social providers and SAML, without building your own login page.

---

## Question 30 — Answer: B

**Explanation:** Provisioned Concurrency pre-initializes Lambda execution environments, eliminating cold starts. Increasing memory can help but doesn't eliminate cold starts entirely.

---

## Question 31 — Answer: B

**Explanation:** The Transform section tells CloudFormation to use the SAM transform, which converts SAM-specific resource types into standard CloudFormation resources.

---

## Question 32 — Answer: B

**Explanation:** Lambda event source mappings for Kinesis poll shards, invoke with batches, and checkpoint on success, preserving per-shard order.

---

## Question 33 — Answer: B

**Explanation:** In X-Ray, faults generally correspond to 5xx errors. Errors often map to 4xx client issues; throttles are rate-limit related.

---

## Question 34 — Answer: C

**Explanation:** SQS messages have a maximum size of 256 KB. For larger messages, use S3 to store the payload and pass a reference via SQS.

---

## Question 35 — Answer: C

**Explanation:** Lambda proxy integration forwards the full request to Lambda and expects a structured response (statusCode, headers, body), simplifying API wiring.

---

## Question 36 — Answer: B

**Explanation:** For complete traces through API Gateway into Lambda, enable X-Ray on both the API stage and the Lambda function.

---

## Question 37 — Answer: B

**Explanation:** Stack policies protect resources from unintended updates (e.g., databases) during CloudFormation stack operations.

---

## Question 38 — Answer: B

**Explanation:** MFA Delete requires multi-factor authentication to delete objects or disable versioning, providing strong protection against accidental or malicious deletion.

---

## Question 39 — Answer: B

**Explanation:** IntegrationLatency is backend call time; Latency is overall API Gateway request time including gateway overhead.

---

## Question 40 — Answer: B

**Explanation:** API Gateway provides built-in API key management with usage plans for throttling and quotas. This is designed for public APIs where you want to track and control usage.

---

## Question 41 — Answer: B

**Explanation:** S3 Event Notifications can trigger Lambda, SNS, or SQS when events like object creation, deletion, or restoration occur in a bucket.

---

## Question 42 — Answer: B

**Explanation:** IAM roles provide temporary credentials automatically rotated by AWS. This is the secure best practice — never embed credentials in code or make resources public unnecessarily.

---

## Question 43 — Answer: B

**Explanation:** CodeBuild can resolve environment variables from SSM or Secrets Manager at runtime so secrets stay out of source control.

---

## Question 44 — Answer: C

**Explanation:** Scan reads every item and is inefficient/expensive on large tables. Prefer Query with a proper key design or GSI for non-key access patterns.

---

## Question 45 — Answer: B

**Explanation:** Logs Insights can filter REPORT log lines, parse fields like Duration, sort, and limit results for performance analysis.

---

## Question 46 — Answer: B

**Explanation:** AssumeRole returns temporary credentials (access key, secret key, session token) that can be used to access AWS resources. It's the standard way to obtain temporary credentials for cross-account or on-premises access.

---

## Question 47 — Answer: B

**Explanation:** FIFO queues provide ordering and exactly-once processing within a message group ID. Standard queues prioritize higher throughput with at-least-once delivery.

---

## Question 48 — Answer: B

**Explanation:** Resource import brings existing resources under CloudFormation management using an import change set and a template that matches current configuration.

---

## Question 49 — Answer: B

**Explanation:** EventBridge rules use event patterns (and content filtering) to match specific events and fields before invoking targets like Lambda.

---

## Question 50 — Answer: B

**Explanation:** Canary10Percent5Minutes shifts 10% of traffic to the new version, waits 5 minutes, then shifts the remaining 90%. This is a blue/green-style canary for Lambda.

---

## Question 51 — Answer: B

**Explanation:** Map iterates over an array and runs a processor state machine for each element, with optional concurrency limits for fan-out processing.

---

## Question 52 — Answer: B

**Explanation:** Envelope encryption uses KMS to generate a data key, which is then used to encrypt the actual data locally. This avoids KMS size limits and reduces KMS API calls.

---

## Question 53 — Answer: B

**Explanation:** Using wildcards for both Action and Resource violates least privilege. The policy grants all S3 actions on all buckets, which is overly permissive.

---

## Question 54 — Answer: C

**Explanation:** Querying by a non-key attribute (status) requires a GSI. The primary table can only be efficiently queried by the partition key and sort key.

---

## Question 55 — Answer: B

**Explanation:** A DLQ captures messages that repeatedly fail processing (after maxReceiveCount), enabling inspection, alerting, and reprocessing without blocking the main queue.

---

## Question 56 — Answer: B

**Explanation:** Paths organize configuration and allow IAM policies to grant access to parameter hierarchies via path prefixes and GetParametersByPath.

---

## Question 57 — Answer: B

**Explanation:** GenerateDataKey returns a plaintext data key and an encrypted copy. Use the plaintext key to encrypt data locally (envelope encryption), then store the encrypted key with the data.

---

## Question 58 — Answer: B

**Explanation:** INSUFFICIENT_DATA occurs when CloudWatch lacks enough datapoints to evaluate the alarm (e.g., new metric or sparse activity).

---

## Question 59 — Answer: D

**Explanation:** Immutable deployment creates a completely new set of instances, ensuring full availability during deployment. It's the safest but slowest and most expensive option.

---

## Question 60 — Answer: C

**Explanation:** The Choice state evaluates conditions and branches to different states based on the input, similar to an if-else statement.

---

## Question 61 — Answer: A

**Explanation:** CodePipeline uses an S3 artifact bucket to pass build/deploy artifacts between pipeline stages.

---

## Question 62 — Answer: B

**Explanation:** S3 Select allows you to retrieve only the needed data from a CSV file using SQL expressions, reducing data transfer and processing time significantly.

---

## Question 63 — Answer: D

**Explanation:** Both ElastiCache Redis and DynamoDB DAX can serve as distributed caches. Redis is more general-purpose; DAX is specifically for DynamoDB.

---

## Question 64 — Answer: B

**Explanation:** .ebextensions YAML/JSON files customize Beanstalk environments—software, files, commands, and option settings.

---

## Question 65 — Answer: B

**Explanation:** DynamoDB Streams captures a time-ordered sequence of item-level changes (insert, update, delete) in a table, enabling event-driven processing.

---

