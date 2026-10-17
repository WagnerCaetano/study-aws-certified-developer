# Practice Exam 5

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Development

A Local Secondary Index (LSI) differs from a GSI because an LSI:

- A) Can have a different partition key from the base table
- B) Must share the same partition key as the base table and can only be created at table creation
- C) Supports only eventually consistent reads
- D) Cannot include a sort key

---

## Question 2

**Domain:** Security

A Lambda environment variable contains a secret. What is the BEST practice?

- A) Leave it as plaintext for simplicity
- B) Store the secret in Secrets Manager or SSM SecureString and retrieve it at runtime (optionally cache)
- C) Commit the secret to Git for team access
- D) Put the secret in the function name

---

## Question 3

**Domain:** Monitoring

Which CloudWatch metric is used to monitor Lambda function invocations?

- A) CPUUtilization
- B) Invocations
- C) RequestCount
- D) Throughput

---

## Question 4

**Domain:** Development

A developer needs to query DynamoDB items by email address, but the table's partition key is userId. What is the BEST solution?

- A) Scan the table filtering on email
- B) Create a GSI with email as the partition key
- C) Export the table to S3 and query with Athena for every request
- D) Store emails only in ElastiCache

---

## Question 5

**Domain:** Security

A developer encrypts Lambda environment variables with a customer-managed KMS key. What additional permission does the Lambda execution role need?

- A) kms:CreateKey
- B) kms:Decrypt on that CMK
- C) iam:PassRole on the KMS key
- D) s3:GetObject on all buckets

---

## Question 6

**Domain:** Security

Which S3 feature can enforce that all uploads use encryption?

- A) A bucket policy denying PutObject unless s3:x-amz-server-side-encryption is present
- B) CORS only
- C) Transfer Acceleration
- D) Requester Pays

---

## Question 7

**Domain:** Security

Which Cognito component issues JWT tokens (ID, access, refresh) after user sign-in?

- A) Cognito User Pools
- B) Cognito Identity Pools only
- C) AWS KMS
- D) AWS WAF

---

## Question 8

**Domain:** Monitoring

A Step Functions execution fails. Where should the developer look FIRST for the failing state and error cause?

- A) The Step Functions console execution history / event details
- B) Only Amazon Macie findings
- C) ECR image scan results
- D) Route 53 health checks

---

## Question 9

**Domain:** Deployment

A developer wants to use environment-specific configurations in a SAM template. How can they achieve this?

- A) Hardcode values in the template
- B) Use SAM template parameters with different values per environment
- C) Use separate templates for each environment
- D) Use environment variables in CloudFormation

---

## Question 10

**Domain:** Development

What is the maximum execution timeout for an AWS Lambda function?

- A) 30 seconds
- B) 5 minutes
- C) 15 minutes
- D) 1 hour

---

## Question 11

**Domain:** Security

Which API Gateway authorization type uses a Lambda function to validate tokens?

- A) NONE
- B) AWS_IAM
- C) COGNITO_USER_POOLS
- D) CUSTOM (Lambda Authorizer)

---

## Question 12

**Domain:** Development

A Lambda function processes an SQS batch. One message fails. How can the developer avoid reprocessing successful messages?

- A) Disable the event source mapping
- B) Report failures with ReportBatchItemFailures (partial batch response) so only failed message IDs are retried
- C) Increase memory to 10 GB
- D) Switch to SNS

---

## Question 13

**Domain:** Monitoring

A developer needs to trace requests across multiple Lambda functions and API Gateway. Which service should they enable?

- A) CloudWatch Logs
- B) CloudTrail
- C) AWS X-Ray
- D) CloudWatch Alarms

---

## Question 14

**Domain:** Development

An application must publish events to multiple subscriber types (email, SQS, Lambda) from one producer. Which service is BEST as the fan-out hub?

- A) Amazon SNS
- B) Amazon SQS alone
- C) Amazon S3
- D) Amazon ECR

---

## Question 15

**Domain:** Development

Which S3 storage class is MOST cost-effective for data that is accessed once a quarter?

- A) S3 Standard
- B) S3 Intelligent-Tiering
- C) S3 Standard-IA (Infrequent Access)
- D) S3 Glacier Deep Archive

---

## Question 16

**Domain:** Deployment

CloudFormation nested stacks are used primarily to:

- A) Avoid using parameters
- B) Modularize large templates by embedding child stacks as AWS::CloudFormation::Stack resources
- C) Bypass IAM
- D) Replace CodePipeline

---

## Question 17

**Domain:** Monitoring

A developer wants to create a CloudWatch alarm that triggers when Lambda error rate exceeds 5%. Which metric should they use?

- A) Invocations
- B) Duration
- C) Errors (with math expression Errors/Invocations)
- D) Throttles

---

## Question 18

**Domain:** Deployment

Which AWS CDK construct level provides the highest abstraction with pre-configured patterns?

- A) L1 constructs (CfnXxx)
- B) L2 constructs
- C) L3 constructs (Patterns)
- D) L0 constructs

---

## Question 19

**Domain:** Monitoring

Embedded Metric Format (EMF) in CloudWatch is used to:

- A) Embed IAM policies in logs
- B) Emit custom metrics by writing specially formatted JSON log events
- C) Replace CloudTrail
- D) Disable alarms permanently

---

## Question 20

**Domain:** Deployment

Which AWS SAM CLI command validates a SAM template locally?

- A) sam validate
- B) sam deploy --no-execute-changeset
- C) sam build --validate
- D) sam local invoke

---

## Question 21

**Domain:** Development

A developer stores large objects in S3 and metadata in DynamoDB. What is a common pattern for referencing the object?

- A) Store the entire object bytes in DynamoDB
- B) Store the S3 bucket/key (or URL) in DynamoDB and fetch the object from S3 when needed
- C) Use only EBS volumes
- D) Embed Base64 objects in SQS messages

---

## Question 22

**Domain:** Development

A developer wants to ensure exactly-once processing of SQS messages in a Lambda function. What should they do?

- A) Set the visibility timeout to infinity
- B) Use a FIFO queue with content-based deduplication
- C) Delete the message after processing and use idempotent processing logic
- D) Use SNS instead of SQS

---

## Question 23

**Domain:** Security

Which condition key restricts an IAM policy so that requests must come from a specific VPC endpoint?

- A) aws:SourceIp
- B) aws:SourceVpce
- C) aws:RequestedRegion
- D) aws:MultiFactorAuthPresent

---

## Question 24

**Domain:** Development

When using the AWS SDK, which credential source is preferred for applications running on EC2?

- A) Hardcoded access keys in source control
- B) Instance profile (IAM role attached to the instance)
- C) Root user access keys
- D) Credentials emailed to developers

---

## Question 25

**Domain:** Security

A developer needs to encrypt an S3 bucket with a customer-managed KMS key. Which bucket property should they configure?

- A) Bucket policy
- B) Default encryption with SSE-KMS
- C) CORS configuration
- D) Object lock

---

## Question 26

**Domain:** Monitoring

Which AWS service provides a record of API calls made in an AWS account?

- A) CloudWatch Logs
- B) CloudTrail
- C) X-Ray
- D) VPC Flow Logs

---

## Question 27

**Domain:** Development

A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?

- A) SQS + Lambda
- B) SNS + SQS + Lambda
- C) Kinesis + Lambda
- D) API Gateway + Lambda

---

## Question 28

**Domain:** Deployment

What is the purpose of 'sam build' command?

- A) To deploy the SAM application
- B) To create a deployment artifact by building Lambda functions and copying dependencies
- C) To delete a SAM application
- D) To test the SAM application in production

---

## Question 29

**Domain:** Deployment

Which Elastic Beanstalk deployment policy is the FASTEST but causes temporary unavailability?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 30

**Domain:** Security

Which KMS key policy statement is required for a CMK to be usable by IAM principals in the account?

- A) No key policy is needed; IAM alone is always sufficient
- B) The key policy must allow the account/root (or specific principals); IAM permissions then further control access
- C) Only CloudTrail can use CMKs
- D) Key policies only apply to AWS managed keys

---

## Question 31

**Domain:** Security

API Gateway Cognito User Pool authorizers validate which token by default for REST APIs?

- A) Refresh token only
- B) ID token (JWT) from the Cognito User Pool
- C) AWS access key ID
- D) SAML assertion only

---

## Question 32

**Domain:** Development

What is the maximum size of a Lambda deployment package (unzipped, including layers) for a zip upload?

- A) 50 MB
- B) 250 MB
- C) 10 GB
- D) 5 MB

---

## Question 33

**Domain:** Security

What is the purpose of an IAM permissions boundary?

- A) To replace SCPs in Organizations
- B) To set the maximum permissions an IAM identity can be granted, even if policies allow more
- C) To encrypt IAM credentials
- D) To enable MFA devices

---

## Question 34

**Domain:** Security

A developer wants to use Cognito to allow unauthenticated guest access to AWS resources. Which Cognito feature supports this?

- A) Cognito User Pools
- B) Cognito Identity Pools (Federated Identities)
- C) Cognito Sync
- D) Cognito user groups

---

## Question 35

**Domain:** Deployment

SAM AutopublishAlias combined with DeploymentPreference enables:

- A) Manual zip uploads only
- B) Automatic version/alias publishing with gradual CodeDeploy traffic shifting
- C) Disabling CloudWatch Logs
- D) Creating EC2 instances

---

## Question 36

**Domain:** Development

A developer needs to deploy a Lambda function that processes SQS messages. The function must read messages in batches of 10 and delete them after processing. Which of the following is the BEST approach?

- A) Poll SQS manually using a scheduled Lambda function every minute
- B) Configure SQS as an event source for the Lambda function with a batch size of 10
- C) Use SNS to fan out messages to individual Lambda invocations
- D) Use Kinesis Data Streams to buffer messages before processing

---

## Question 37

**Domain:** Deployment

What is the purpose of a buildspec.yml file in AWS CodeBuild?

- A) It defines the infrastructure resources
- B) It contains the build commands and settings for CodeBuild
- C) It configures CodePipeline stages
- D) It defines IAM policies for the build

---

## Question 38

**Domain:** Development

Which AWS SDK best practice helps applications recover from transient DynamoDB throttling?

- A) Disable retries and fail immediately
- B) Use exponential backoff with jitter (SDK default retries)
- C) Always Switch to Scan
- D) Hardcode higher timeouts only

---

## Question 39

**Domain:** Security

What does STS GetCallerIdentity return?

- A) A new access key pair
- B) The Account, UserId, and Arn of the credentials making the call
- C) A Cognito JWT
- D) A CloudTrail digest

---

## Question 40

**Domain:** Security

Which Parameter Store parameter type stores encrypted values using KMS?

- A) String
- B) StringList
- C) SecureString
- D) HashString

---

## Question 41

**Domain:** Deployment

A developer needs to deploy a containerized application without managing any infrastructure. Which combination should they use?

- A) EC2 + Docker
- B) ECS with Fargate launch type
- C) ECS with EC2 launch type
- D) Elastic Beanstalk with Docker platform

---

## Question 42

**Domain:** Security

A mobile app needs temporary AWS credentials after Cognito User Pool login. What should be configured?

- A) Only IAM users with long-lived keys in the app
- B) Cognito Identity Pool federated with the User Pool to obtain temporary credentials
- C) Root account keys
- D) CloudFront key pairs only

---

## Question 43

**Domain:** Development

API Gateway stage variables are commonly used to:

- A) Encrypt Lambda environment variables
- B) Parameterize backend endpoints or Lambda aliases per stage (dev/test/prod)
- C) Replace IAM policies
- D) Increase Lambda memory at runtime

---

## Question 44

**Domain:** Monitoring

A Lambda function is timing out when connecting to an RDS database in a VPC. What is the MOST likely cause?

- A) The Lambda function has insufficient memory
- B) The Lambda function's security group doesn't allow outbound traffic to RDS
- C) The Lambda function is not configured to run in the VPC
- D) Both B and C could be causes

---

## Question 45

**Domain:** Development

What is the maximum item size in DynamoDB?

- A) 64 KB
- B) 256 KB
- C) 400 KB
- D) 1 MB

---

## Question 46

**Domain:** Monitoring

Which alarm action commonly notifies an operations channel when a metric breaches a threshold?

- A) Publish to an SNS topic subscribed by email/Slack/Lambda
- B) Delete the CloudWatch log group
- C) Disable API Gateway
- D) Rotate Cognito clients

---

## Question 47

**Domain:** Deployment

A developer wants to test a SAM application locally before deploying. Which command runs the Lambda function locally?

- A) sam validate
- B) sam local invoke
- C) sam local start-api
- D) sam build

---

## Question 48

**Domain:** Deployment

What is a CloudFormation change set?

- A) A permanent deletion of the stack
- B) A preview of proposed stack changes that can be reviewed before execution
- C) An automatic CI/CD pipeline
- D) A CDK construct library

---

## Question 49

**Domain:** Security

A cross-account S3 access scenario requires Account B to read objects in Account A's bucket. Which combination is commonly required?

- A) Only an IAM user in Account B with no bucket policy
- B) Bucket policy in Account A allowing Account B's principal, plus permissions in Account B
- C) Making the bucket public
- D) Disabling encryption

---

## Question 50

**Domain:** Deployment

A developer wants to share a Lambda function's ARN from one CloudFormation stack to another. How can they do this?

- A) Use Fn::Ref in the second stack
- B) Use Outputs with Export in the first stack and Fn::ImportValue in the second stack
- C) Hardcode the ARN in both stacks
- D) Use SSM parameters automatically

---

## Question 51

**Domain:** Monitoring

What is the purpose of a CloudWatch metric filter?

- A) To filter which logs are sent to S3
- B) To extract metric values from log events
- C) To delete old log entries
- D) To encrypt log data

---

## Question 52

**Domain:** Deployment

Which CodePipeline action provider typically stores source code from a Git repository?

- A) AWS CodeCommit, GitHub, or Amazon S3 as Source actions
- B) Amazon Athena
- C) Amazon Macie
- D) AWS Batch only

---

## Question 53

**Domain:** Deployment

What does CodeDeploy AppSpec (appspec.yml) define for Lambda deployments?

- A) Only VPC subnets
- B) How traffic is shifted between versions and lifecycle hooks (BeforeAllowTraffic, AfterAllowTraffic)
- C) CloudWatch log retention only
- D) Cognito user attributes

---

## Question 54

**Domain:** Deployment

In CloudFormation, what happens when a stack update fails?

- A) The stack is deleted
- B) Changes are automatically rolled back to the previous known good state
- C) The stack is paused for manual review
- D) Only the failed resource is deleted

---

## Question 55

**Domain:** Security

An IAM policy includes Effect: Deny for s3:DeleteObject. A separate Allow grants s3:*. What is the result for DeleteObject?

- A) Allow always wins
- B) Explicit Deny overrides Allow — DeleteObject is denied
- C) The policies cancel and access is undefined
- D) Only resource-based policies apply

---

## Question 56

**Domain:** Development

A developer needs to run a long-running workflow with retries, branching, and parallel steps coordinating multiple Lambda functions. Which service fits BEST?

- A) A single Lambda with a 15-minute sleep loop
- B) AWS Step Functions
- C) Amazon SNS only
- D) Amazon CloudFront

---

## Question 57

**Domain:** Development

A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?

- A) Amazon SQS Standard queue
- B) Amazon SNS
- C) Amazon Kinesis Data Streams
- D) Amazon MQ

---

## Question 58

**Domain:** Monitoring

A developer needs to search through Lambda function logs to find errors. Which tool provides the MOST powerful query capabilities?

- A) CloudWatch Logs console with simple text search
- B) CloudWatch Logs Insights
- C) AWS X-Ray
- D) CloudTrail

---

## Question 59

**Domain:** Development

An SNS topic must deliver only messages with attribute orderType=express to a subscribed SQS queue. What should be configured?

- A) SQS redrive policy
- B) SNS subscription filter policy matching orderType=express
- C) Kinesis shard key
- D) API Gateway usage plan

---

## Question 60

**Domain:** Development

API Gateway WebSocket APIs are MOST appropriate when the application needs:

- A) Only synchronous request/response over HTTP
- B) Persistent bidirectional connections for real-time push to clients
- C) File uploads larger than 10 GB
- D) Batch ETL from S3

---

## Question 61

**Domain:** Development

What is the primary benefit of DynamoDB DAX?

- A) Multi-region active-active writes
- B) Microsecond in-memory caching for DynamoDB read-heavy workloads
- C) Automatic schema migrations
- D) Replacing GSIs entirely

---

## Question 62

**Domain:** Security

What does SSE-S3 encryption use for S3 object encryption?

- A) Customer-provided keys only (SSE-C)
- B) S3-managed encryption keys
- C) CloudHSM exclusively
- D) Client-side encryption only

---

## Question 63

**Domain:** Development

Which Lambda concurrency control reserves capacity for a critical function so other functions cannot consume the account limit?

- A) Reserved concurrency
- B) Provisioned concurrency only
- C) Asynchronous invocation
- D) Dead-letter queues

---

## Question 64

**Domain:** Monitoring

Lambda Destinations (on success/failure) for asynchronous invocations can send results to:

- A) Only Amazon RDS
- B) SQS, SNS, EventBridge, or another Lambda function
- C) Only CloudFront
- D) Only IAM

---

## Question 65

**Domain:** Deployment

Which Elastic Beanstalk deployment policy launches a temporary set of instances alongside the old ones to avoid capacity reduction?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Traffic splitting only on Lambda

---


---

# Answers & Explanations

---

## Question 1 — Answer: B

**Explanation:** LSIs share the base table partition key, provide an alternate sort key, and must be defined when the table is created. GSIs can use different partition keys.

---

## Question 2 — Answer: B

**Explanation:** Prefer Secrets Manager or SSM Parameter Store (SecureString) over plaintext environment variables for secrets, with IAM-controlled access and optional rotation.

---

## Question 3 — Answer: B

**Explanation:** CloudWatch publishes Lambda metrics including Invocations, Duration, Errors, Throttles, and ConcurrentExecutions.

---

## Question 4 — Answer: B

**Explanation:** A GSI with email as partition key enables efficient Query access by email without expensive Scans.

---

## Question 5 — Answer: B

**Explanation:** When environment variables are encrypted with a CMK, the execution role needs kms:Decrypt (and the key policy must allow the role) to decrypt them at runtime.

---

## Question 6 — Answer: A

**Explanation:** Bucket policies can deny unencrypted uploads by requiring the encryption header or using default encryption plus Deny for incorrect encryption.

---

## Question 7 — Answer: A

**Explanation:** User Pools authenticate users and issue JWTs. Identity Pools exchange identity for temporary AWS credentials.

---

## Question 8 — Answer: A

**Explanation:** Step Functions execution event history shows each state transition, inputs/outputs, and error causes for failed steps.

---

## Question 9 — Answer: B

**Explanation:** SAM templates support CloudFormation parameters, allowing you to pass environment-specific values at deployment time using parameter overrides.

---

## Question 10 — Answer: C

**Explanation:** The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services.

---

## Question 11 — Answer: D

**Explanation:** Lambda Authorizers (formerly Custom Authorizers) use a Lambda function to evaluate the authorization token and return an IAM policy.

---

## Question 12 — Answer: B

**Explanation:** Partial batch responses let Lambda tell SQS which message IDs failed; only those become visible again. Successful messages are deleted.

---

## Question 13 — Answer: C

**Explanation:** AWS X-Ray provides distributed tracing, allowing you to trace requests across multiple services, visualize service maps, and identify performance bottlenecks.

---

## Question 14 — Answer: A

**Explanation:** SNS is a pub/sub hub that can deliver to SQS, Lambda, HTTP, email, and other protocols from a single publish.

---

## Question 15 — Answer: C

**Explanation:** S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access.

---

## Question 16 — Answer: B

**Explanation:** Nested stacks break large templates into reusable components managed as a hierarchy of stacks.

---

## Question 17 — Answer: C

**Explanation:** To calculate error rate, use a metric math expression dividing Errors by Invocations, then set the alarm threshold at 0.05 (5%).

---

## Question 18 — Answer: C

**Explanation:** L3 constructs (also called patterns) provide the highest level of abstraction with pre-configured defaults and best practices.

---

## Question 19 — Answer: B

**Explanation:** EMF lets applications put custom metrics via structured logs that CloudWatch extracts without separate PutMetricData calls.

---

## Question 20 — Answer: A

**Explanation:** sam validate checks the SAM template for syntax and structural errors. It can validate both SAM and CloudFormation templates.

---

## Question 21 — Answer: B

**Explanation:** The claim-check / metadata pattern stores pointers in DynamoDB and large payloads in S3, staying within DynamoDB item size limits (400 KB).

---

## Question 22 — Answer: C

**Explanation:** SQS provides at-least-once delivery. For exactly-once semantics, delete messages after successful processing and design idempotent processing logic that can handle duplicate deliveries safely.

---

## Question 23 — Answer: B

**Explanation:** aws:SourceVpce (and related VPC endpoint condition keys) can require that API calls originate from a specified VPC endpoint.

---

## Question 24 — Answer: B

**Explanation:** EC2 instance profiles provide temporary credentials via the instance metadata service; the SDK retrieves them automatically.

---

## Question 25 — Answer: B

**Explanation:** S3 default encryption with SSE-KMS uses a customer-managed CMK. This automatically encrypts all new objects with the specified KMS key.

---

## Question 26 — Answer: B

**Explanation:** CloudTrail records API calls made in your AWS account, including who made the call, when, and what resources were affected.

---

## Question 27 — Answer: B

**Explanation:** SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently.

---

## Question 28 — Answer: B

**Explanation:** sam build processes the SAM template, builds Lambda functions (installing dependencies), and creates deployment artifacts in the .aws-sam directory.

---

## Question 29 — Answer: A

**Explanation:** All at once deploys to all instances simultaneously, making it the fastest but causes temporary downtime during the deployment.

---

## Question 30 — Answer: B

**Explanation:** KMS requires both key policy and IAM permissions. The key policy is foundational; without it granting the account, IAM alone cannot authorize use.

---

## Question 31 — Answer: B

**Explanation:** Cognito authorizers validate JWTs (typically the ID token) issued by the configured User Pool before allowing the request.

---

## Question 32 — Answer: B

**Explanation:** The unzipped deployment package size limit (including layers) is 250 MB. Container images support larger packages up to 10 GB.

---

## Question 33 — Answer: B

**Explanation:** Permissions boundaries define the maximum permissions an identity can have; effective permissions are the intersection of identity policies and the boundary.

---

## Question 34 — Answer: B

**Explanation:** Cognito Identity Pools support both authenticated and unauthenticated (guest) identities, providing temporary AWS credentials for accessing resources.

---

## Question 35 — Answer: B

**Explanation:** AutopublishAlias creates/updates a Lambda alias; DeploymentPreference configures CodeDeploy canary/linear traffic shifting to that alias.

---

## Question 36 — Answer: B

**Explanation:** SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages. Successfully processed messages are automatically deleted.

---

## Question 37 — Answer: B

**Explanation:** The buildspec.yml defines the build phases (install, pre_build, build, post_build), environment variables, and artifacts for CodeBuild.

---

## Question 38 — Answer: B

**Explanation:** AWS SDKs retry throttling errors with exponential backoff. Applications should also consider on-demand capacity or capacity adjustments for sustained load.

---

## Question 39 — Answer: B

**Explanation:** GetCallerIdentity is commonly used to verify which principal the current credentials represent (account, user ID, ARN).

---

## Question 40 — Answer: C

**Explanation:** SecureString parameters are encrypted with AWS KMS. String and StringList store plaintext values.

---

## Question 41 — Answer: B

**Explanation:** ECS with Fargate eliminates infrastructure management for containers. Fargate provisions and manages the underlying compute resources automatically.

---

## Question 42 — Answer: B

**Explanation:** Identity Pools exchange authenticated User Pool identities (or other IdPs) for temporary AWS credentials via STS.

---

## Question 43 — Answer: B

**Explanation:** Stage variables let you configure stage-specific values such as Lambda alias ARNs or HTTP endpoints without changing the API definition for each environment.

---

## Question 44 — Answer: D

**Explanation:** Lambda functions need to be configured in the correct VPC/subnets with appropriate security groups to access VPC resources like RDS.

---

## Question 45 — Answer: C

**Explanation:** DynamoDB items are limited to 400 KB. Larger payloads should be stored in S3 with a reference in DynamoDB.

---

## Question 46 — Answer: A

**Explanation:** CloudWatch Alarms typically notify via SNS, which fans out to email, chat integrations, Lambda, and other subscribers.

---

## Question 47 — Answer: B

**Explanation:** sam local invoke runs a Lambda function locally using Docker. sam local start-api starts a local API server instead of invoking directly.

---

## Question 48 — Answer: B

**Explanation:** Change sets show the impact of a proposed update (add/modify/delete resources) before you execute the update.

---

## Question 49 — Answer: B

**Explanation:** Cross-account S3 access typically needs a resource-based bucket policy granting the external principal and identity-based permissions in the caller's account.

---

## Question 50 — Answer: B

**Explanation:** CloudFormation cross-stack references use Outputs with Export Name in one stack and Fn::ImportValue in another to share values between stacks.

---

## Question 51 — Answer: B

**Explanation:** Metric filters define patterns to match in log events and turn them into CloudWatch numeric metrics for alarms and dashboards.

---

## Question 52 — Answer: A

**Explanation:** CodePipeline Source stages commonly pull from CodeCommit, GitHub/GitHub Enterprise, Bitbucket, or S3 artifacts.

---

## Question 53 — Answer: B

**Explanation:** For Lambda, AppSpec configures alias traffic shifting and optional hooks that run validation Lambda functions during deployment.

---

## Question 54 — Answer: B

**Explanation:** CloudFormation automatically rolls back changes on failure by default. All changes made during the update are reverted to the previous stable state.

---

## Question 55 — Answer: B

**Explanation:** In IAM evaluation, an explicit Deny always overrides Allow, regardless of other Allow statements.

---

## Question 56 — Answer: B

**Explanation:** Step Functions orchestrates multi-step workflows with retries, catchers, Choice, Parallel, and Map states across AWS services.

---

## Question 57 — Answer: C

**Explanation:** Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming.

---

## Question 58 — Answer: B

**Explanation:** CloudWatch Logs Insights provides a powerful query language for searching and analyzing log data, including filtering, aggregation, and sorting.

---

## Question 59 — Answer: B

**Explanation:** SNS filter policies on subscriptions deliver only messages whose attributes (or payload attributes) match the filter criteria.

---

## Question 60 — Answer: B

**Explanation:** WebSocket APIs maintain persistent connections and allow the server to push messages to connected clients for chat, notifications, and similar use cases.

---

## Question 61 — Answer: B

**Explanation:** DAX is a write-through cache for DynamoDB that can reduce read latency to microseconds for cache hits.

---

## Question 62 — Answer: B

**Explanation:** SSE-S3 uses encryption keys managed by Amazon S3. SSE-KMS uses KMS keys; SSE-C uses customer-provided keys.

---

## Question 63 — Answer: A

**Explanation:** Reserved concurrency guarantees a maximum concurrent execution limit for a function and reserves that capacity from the account pool.

---

## Question 64 — Answer: B

**Explanation:** Lambda Destinations route async invocation records to SQS, SNS, EventBridge, or Lambda for success or failure handling.

---

## Question 65 — Answer: C

**Explanation:** Rolling with additional batch launches new instances first so capacity is not reduced while old instances are updated.

---

