# Practice Exam 1

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Security

SSM Parameter Store hierarchical paths (e.g., /myapp/prod/db) are useful primarily to:

- A) Automatically rotate passwords
- B) Organize parameters and apply IAM path-based access control with GetParametersByPath
- C) Replace KMS entirely
- D) Create VPC endpoints

---

## Question 2

**Domain:** Security

A cross-account S3 access scenario requires Account B to read objects in Account A's bucket. Which combination is commonly required?

- A) Only an IAM user in Account B with no bucket policy
- B) Bucket policy in Account A allowing Account B's principal, plus permissions in Account B
- C) Making the bucket public
- D) Disabling encryption

---

## Question 3

**Domain:** Security

Which S3 feature can enforce that all uploads use encryption?

- A) A bucket policy denying PutObject unless s3:x-amz-server-side-encryption is present
- B) CORS only
- C) Transfer Acceleration
- D) Requester Pays

---

## Question 4

**Domain:** Deployment

SAM Globals section is used to:

- A) Define account-wide SCPs
- B) Set default properties shared by serverless resources (Runtime, Timeout, Environment, etc.)
- C) Replace Parameters
- D) Configure Organization trails

---

## Question 5

**Domain:** Deployment

What is a CloudFormation change set?

- A) A permanent deletion of the stack
- B) A preview of proposed stack changes that can be reviewed before execution
- C) An automatic CI/CD pipeline
- D) A CDK construct library

---

## Question 6

**Domain:** Deployment

In CodeBuild, privileged mode is required primarily when the build needs to:

- A) Call DynamoDB
- B) Build Docker images (Docker-in-Docker)
- C) Write CloudWatch Logs
- D) Assume an IAM role

---

## Question 7

**Domain:** Deployment

Which Elastic Beanstalk deployment policy launches a temporary set of instances alongside the old ones to avoid capacity reduction?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Traffic splitting only on Lambda

---

## Question 8

**Domain:** Security

API Gateway Cognito User Pool authorizers validate which token by default for REST APIs?

- A) Refresh token only
- B) ID token (JWT) from the Cognito User Pool
- C) AWS access key ID
- D) SAML assertion only

---

## Question 9

**Domain:** Deployment

Elastic Beanstalk .ebextensions configuration files are used to:

- A) Define Lambda layers
- B) Customize environment configuration (packages, files, option settings) during deployment
- C) Create Cognito User Pools
- D) Configure X-Ray sampling only

---

## Question 10

**Domain:** Deployment

Which CodePipeline action provider typically stores source code from a Git repository?

- A) AWS CodeCommit, GitHub, or Amazon S3 as Source actions
- B) Amazon Athena
- C) Amazon Macie
- D) AWS Batch only

---

## Question 11

**Domain:** Development

What is the maximum payload size for an SQS message?

- A) 64 KB
- B) 128 KB
- C) 256 KB
- D) 1 MB

---

## Question 12

**Domain:** Monitoring

A Lambda function shows high Throttles in CloudWatch. What does this indicate?

- A) The function code has a syntax error
- B) Concurrent executions exceeded reserved or account concurrency limits
- C) The DynamoDB table is empty
- D) X-Ray is disabled

---

## Question 13

**Domain:** Monitoring

A developer enables X-Ray tracing on API Gateway. What additional step helps end-to-end traces into Lambda?

- A) Disable Lambda logs
- B) Enable active tracing on the Lambda function as well
- C) Delete the API stage
- D) Use only MOCK integrations

---

## Question 14

**Domain:** Monitoring

An X-Ray service map shows a node with a high fault rate. Faults typically indicate:

- A) Successful 2xx responses
- B) 5xx errors / server-side failures in the traced service
- C) Only cold starts
- D) Missing IAM roles exclusively

---

## Question 15

**Domain:** Security

A developer needs client-side encryption of objects before uploading to S3. Which approach meets this requirement?

- A) Rely only on SSE-S3 after upload
- B) Encrypt data in the application (e.g., AWS Encryption SDK) before PutObject
- C) Enable Transfer Acceleration
- D) Use only CloudWatch Logs encryption

---

## Question 16

**Domain:** Development

A Lambda function is experiencing cold start latency. Which approach would BEST reduce this?

- A) Increase the Lambda memory allocation
- B) Use Provisioned Concurrency
- C) Add more code to the Lambda function
- D) Decrease the timeout setting

---

## Question 17

**Domain:** Development

When designing DynamoDB partition keys, what practice helps avoid hot partitions?

- A) Use a single static partition key for all items
- B) Choose high-cardinality keys (and consider write sharding) so traffic spreads across partitions
- C) Always use Scan instead of Query
- D) Disable TTL

---

## Question 18

**Domain:** Development

A Step Functions workflow needs to wait for human approval before proceeding. Which state type should be used?

- A) Task state
- B) Choice state
- C) Wait state with a callback pattern
- D) Succeed state

---

## Question 19

**Domain:** Security

What does SSE-S3 encryption use for S3 object encryption?

- A) Customer-provided keys only (SSE-C)
- B) S3-managed encryption keys
- C) CloudHSM exclusively
- D) Client-side encryption only

---

## Question 20

**Domain:** Security

Which Cognito component issues JWT tokens (ID, access, refresh) after user sign-in?

- A) Cognito User Pools
- B) Cognito Identity Pools only
- C) AWS KMS
- D) AWS WAF

---

## Question 21

**Domain:** Security

A Lambda environment variable contains a secret. What is the BEST practice?

- A) Leave it as plaintext for simplicity
- B) Store the secret in Secrets Manager or SSM SecureString and retrieve it at runtime (optionally cache)
- C) Commit the secret to Git for team access
- D) Put the secret in the function name

---

## Question 22

**Domain:** Development

A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?

- A) Amazon SQS Standard queue
- B) Amazon SNS
- C) Amazon Kinesis Data Streams
- D) Amazon MQ

---

## Question 23

**Domain:** Development

A developer needs to implement a distributed cache that can be shared across multiple Lambda functions. Which service is BEST?

- A) Amazon S3
- B) Amazon ElastiCache (Redis)
- C) Amazon DynamoDB DAX
- D) Both B and C are valid options

---

## Question 24

**Domain:** Security

What is the purpose of an IAM permissions boundary?

- A) To replace SCPs in Organizations
- B) To set the maximum permissions an IAM identity can be granted, even if policies allow more
- C) To encrypt IAM credentials
- D) To enable MFA devices

---

## Question 25

**Domain:** Monitoring

Which CloudWatch Logs Insights query finds the 10 slowest Lambda durations from REPORT lines?

- A) DELETE FROM log_group
- B) A query filtering REPORT lines, parsing Duration, sorting desc, and limiting 10
- C) SELECT * FROM dynamodb
- D) Only the X-Ray console can do this

---

## Question 26

**Domain:** Deployment

SAM AutopublishAlias combined with DeploymentPreference enables:

- A) Manual zip uploads only
- B) Automatic version/alias publishing with gradual CodeDeploy traffic shifting
- C) Disabling CloudWatch Logs
- D) Creating EC2 instances

---

## Question 27

**Domain:** Security

Which Parameter Store parameter type stores encrypted values using KMS?

- A) String
- B) StringList
- C) SecureString
- D) HashString

---

## Question 28

**Domain:** Development

A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?

- A) SQS + Lambda
- B) SNS + SQS + Lambda
- C) Kinesis + Lambda
- D) API Gateway + Lambda

---

## Question 29

**Domain:** Development

Which S3 feature allows a Lambda function to be triggered when a new object is created?

- A) S3 Lifecycle policies
- B) S3 Event Notifications
- C) S3 Select
- D) S3 Versioning

---

## Question 30

**Domain:** Security

A developer encrypts Lambda environment variables with a customer-managed KMS key. What additional permission does the Lambda execution role need?

- A) kms:CreateKey
- B) kms:Decrypt on that CMK
- C) iam:PassRole on the KMS key
- D) s3:GetObject on all buckets

---

## Question 31

**Domain:** Security

Which header or mechanism helps protect against confused deputy attacks when using AssumeRole with third parties?

- A) External ID in the trust policy Condition
- B) Larger session duration
- C) Disabling MFA
- D) Using * for Principal

---

## Question 32

**Domain:** Development

What is the maximum execution timeout for an AWS Lambda function?

- A) 30 seconds
- B) 5 minutes
- C) 15 minutes
- D) 1 hour

---

## Question 33

**Domain:** Development

Which DynamoDB feature captures item-level modifications in a table?

- A) Global Secondary Index
- B) DynamoDB Streams
- C) Time-to-Live (TTL)
- D) Point-in-Time Recovery

---

## Question 34

**Domain:** Deployment

CloudFormation stack policies are used to:

- A) Encrypt all parameters automatically
- B) Prevent updates to critical resources during stack updates unless explicitly allowed
- C) Replace IAM identity policies
- D) Speed up rollbacks only

---

## Question 35

**Domain:** Deployment

What does cdk diff show?

- A) Only TypeScript compile errors
- B) Differences between the synthesized template and the deployed stack
- C) Git commit history
- D) Lambda cold start metrics

---

## Question 36

**Domain:** Development

A developer needs to process DynamoDB item changes with Lambda near real time. What should they configure?

- A) DynamoDB Streams as a Lambda event source
- B) S3 inventory reports
- C) CloudFront invalidations
- D) ECR lifecycle policies

---

## Question 37

**Domain:** Development

Which S3 storage class is MOST cost-effective for data that is accessed once a quarter?

- A) S3 Standard
- B) S3 Intelligent-Tiering
- C) S3 Standard-IA (Infrequent Access)
- D) S3 Glacier Deep Archive

---

## Question 38

**Domain:** Security

What does STS GetCallerIdentity return?

- A) A new access key pair
- B) The Account, UserId, and Arn of the credentials making the call
- C) A Cognito JWT
- D) A CloudTrail digest

---

## Question 39

**Domain:** Monitoring

Which tool helps determine if CloudFormation stack resources have drifted from the template?

- A) CloudFormation drift detection
- B) Amazon Polly
- C) AWS Snowball
- D) Amazon Rekognition

---

## Question 40

**Domain:** Deployment

A developer needs to update only a Lambda function's code without changing infrastructure. Which approach works?

- A) Always recreate the entire CloudFormation stack
- B) Use aws lambda update-function-code or deploy via SAM/CFN updating the function resource code
- C) Change the DynamoDB table name
- D) Disable the API Gateway stage

---

## Question 41

**Domain:** Monitoring

API Gateway integration latency vs latency metrics differ how?

- A) They are identical always
- B) Latency includes overhead end-to-end at API Gateway; IntegrationLatency measures time spent calling the backend
- C) IntegrationLatency includes client network only
- D) Neither is published to CloudWatch

---

## Question 42

**Domain:** Security

Which KMS key policy statement is required for a CMK to be usable by IAM principals in the account?

- A) No key policy is needed; IAM alone is always sufficient
- B) The key policy must allow the account/root (or specific principals); IAM permissions then further control access
- C) Only CloudTrail can use CMKs
- D) Key policies only apply to AWS managed keys

---

## Question 43

**Domain:** Security

What is the safest way to allow a third-party SaaS to write logs into your S3 bucket?

- A) Share root credentials
- B) Use a bucket policy with a dedicated IAM role/external ID (or assume-role) and least-privilege PutObject on a prefix
- C) Make the bucket fully public
- D) Disable all encryption

---

## Question 44

**Domain:** Development

A developer is building a REST API with API Gateway. The backend Lambda function returns a response, but the client receives a 502 error. What is the MOST likely cause?

- A) The API Gateway does not have CORS enabled
- B) The Lambda function is not returning a properly formatted proxy response with statusCode, headers, and body
- C) The API Gateway is missing request validation
- D) The client is sending the wrong Content-Type header

---

## Question 45

**Domain:** Security

An IAM policy includes Effect: Deny for s3:DeleteObject. A separate Allow grants s3:*. What is the result for DeleteObject?

- A) Allow always wins
- B) Explicit Deny overrides Allow — DeleteObject is denied
- C) The policies cancel and access is undefined
- D) Only resource-based policies apply

---

## Question 46

**Domain:** Development

A Lambda function needs to access a DynamoDB table. What is the MOST secure way to grant permissions?

- A) Hardcode AWS access keys in the Lambda function code
- B) Store access keys in Lambda environment variables
- C) Attach an IAM execution role with least-privilege DynamoDB permissions to the Lambda function
- D) Use the AWS account root user credentials

---

## Question 47

**Domain:** Development

A developer needs to store user session data with sub-millisecond latency. Which AWS service should be used?

- A) Amazon S3
- B) Amazon DynamoDB
- C) Amazon ElastiCache (Redis)
- D) Amazon RDS

---

## Question 48

**Domain:** Deployment

What does CodeDeploy AppSpec (appspec.yml) define for Lambda deployments?

- A) Only VPC subnets
- B) How traffic is shifted between versions and lifecycle hooks (BeforeAllowTraffic, AfterAllowTraffic)
- C) CloudWatch log retention only
- D) Cognito user attributes

---

## Question 49

**Domain:** Deployment

What does AWS::Serverless::Function Events property typically configure?

- A) Only CloudTrail events
- B) Event sources such as API Gateway, S3, SQS, SNS, DynamoDB Streams, Schedule, etc.
- C) VPC Flow Logs exclusively
- D) KMS key rotation schedule

---

## Question 50

**Domain:** Deployment

Which artifact store does CodePipeline commonly use between stages?

- A) Amazon S3
- B) Amazon Neptune
- C) Amazon MQ
- D) Amazon Lex

---

## Question 51

**Domain:** Development

When building a DynamoDB table for an e-commerce application, which access pattern requires a Global Secondary Index (GSI)?

- A) Get order by orderId (partition key)
- B) Get all orders for a customer sorted by date (composite key)
- C) Get all orders with status 'PENDING' regardless of customer
- D) Delete an order by orderId

---

## Question 52

**Domain:** Deployment

CloudFormation nested stacks are used primarily to:

- A) Avoid using parameters
- B) Modularize large templates by embedding child stacks as AWS::CloudFormation::Stack resources
- C) Bypass IAM
- D) Replace CodePipeline

---

## Question 53

**Domain:** Development

Which ECS launch type eliminates the need to manage underlying server infrastructure?

- A) EC2 launch type
- B) Fargate launch type
- C) External launch type
- D) Lambda launch type

---

## Question 54

**Domain:** Monitoring

Which Lambda metric indicates how long the initialization (cold start) phase took?

- A) Init Duration (reported in REPORT / Performance metrics where available)
- B) ApproximateNumberOfMessagesVisible
- C) BucketSizeBytes
- D) HealthyHostCount

---

## Question 55

**Domain:** Development

Which DynamoDB operation is MOST efficient for retrieving a single item by its primary key?

- A) Scan with a filter expression
- B) Query with the partition key
- C) GetItem with the full primary key
- D) BatchGetItem with a single item

---

## Question 56

**Domain:** Deployment

What is the purpose of a CodePipeline manual approval action?

- A) To compile source code
- B) To pause the pipeline until a reviewer approves before continuing to production deploy
- C) To create IAM users
- D) To rotate KMS keys

---

## Question 57

**Domain:** Security

A mobile app needs temporary AWS credentials after Cognito User Pool login. What should be configured?

- A) Only IAM users with long-lived keys in the app
- B) Cognito Identity Pool federated with the User Pool to obtain temporary credentials
- C) Root account keys
- D) CloudFront key pairs only

---

## Question 58

**Domain:** Development

A developer needs to implement a state machine that branches based on output from a Lambda function. Which Step Functions state type should be used?

- A) Task
- B) Pass
- C) Choice
- D) Wait

---

## Question 59

**Domain:** Monitoring

CloudWatch alarm state INSUFFICIENT_DATA usually means:

- A) The alarm threshold was breached
- B) Not enough data points are available yet for the configured evaluation period
- C) The AWS account was suspended
- D) X-Ray tracing is mandatory

---

## Question 60

**Domain:** Monitoring

What is CloudWatch Logs subscription filter used for?

- A) Encrypting log groups with SSE-S3 only
- B) Streaming matching log events in near real time to Kinesis, Firehose, or Lambda
- C) Deleting empty log streams
- D) Replacing metric filters entirely with no metrics

---

## Question 61

**Domain:** Deployment

CloudFormation Fn::Sub is used to:

- A) Delete stacks
- B) Perform string substitution with ${Variable} placeholders
- C) Create change sets only
- D) Import existing resources exclusively

---

## Question 62

**Domain:** Monitoring

To capture failed asynchronous Lambda invocations for later analysis, configure:

- A) A dead-letter queue (SQS/SNS) or Lambda destination on failure
- B) Only S3 Transfer Acceleration
- C) Cognito hosted UI
- D) CloudFront signed URLs

---

## Question 63

**Domain:** Development

A developer needs to deploy a Lambda function that processes SQS messages. The function must read messages in batches of 10 and delete them after processing. Which of the following is the BEST approach?

- A) Poll SQS manually using a scheduled Lambda function every minute
- B) Configure SQS as an event source for the Lambda function with a batch size of 10
- C) Use SNS to fan out messages to individual Lambda invocations
- D) Use Kinesis Data Streams to buffer messages before processing

---

## Question 64

**Domain:** Monitoring

A developer needs structured logging from Lambda for easier querying. What is a recommended practice?

- A) Print unstructured free-form strings only
- B) Emit JSON log lines with consistent fields (level, requestId, message) to stdout
- C) Disable CloudWatch Logs
- D) Log only to local disk

---

## Question 65

**Domain:** Development

A Lambda function must share initialization cost across many invocations. Where should expensive SDK clients be created?

- A) Inside the handler on every invocation
- B) Outside the handler (global/module scope) so warm containers reuse them
- C) In a separate Lambda Layer that runs at invoke time
- D) In the API Gateway request mapping template

---


---

# Answers & Explanations

---

## Question 1 — Answer: B

**Explanation:** Paths organize configuration and allow IAM policies to grant access to parameter hierarchies via path prefixes and GetParametersByPath.

---

## Question 2 — Answer: B

**Explanation:** Cross-account S3 access typically needs a resource-based bucket policy granting the external principal and identity-based permissions in the caller's account.

---

## Question 3 — Answer: A

**Explanation:** Bucket policies can deny unencrypted uploads by requiring the encryption header or using default encryption plus Deny for incorrect encryption.

---

## Question 4 — Answer: B

**Explanation:** Globals reduce duplication by applying common Function/Api/SimpleTable properties across SAM resources.

---

## Question 5 — Answer: B

**Explanation:** Change sets show the impact of a proposed update (add/modify/delete resources) before you execute the update.

---

## Question 6 — Answer: B

**Explanation:** Privileged mode grants elevated permissions needed to run Docker daemon operations for building container images.

---

## Question 7 — Answer: C

**Explanation:** Rolling with additional batch launches new instances first so capacity is not reduced while old instances are updated.

---

## Question 8 — Answer: B

**Explanation:** Cognito authorizers validate JWTs (typically the ID token) issued by the configured User Pool before allowing the request.

---

## Question 9 — Answer: B

**Explanation:** .ebextensions YAML/JSON files customize Beanstalk environments—software, files, commands, and option settings.

---

## Question 10 — Answer: A

**Explanation:** CodePipeline Source stages commonly pull from CodeCommit, GitHub/GitHub Enterprise, Bitbucket, or S3 artifacts.

---

## Question 11 — Answer: C

**Explanation:** SQS messages have a maximum size of 256 KB. For larger messages, use S3 to store the payload and pass a reference via SQS.

---

## Question 12 — Answer: B

**Explanation:** Throttles occur when Lambda cannot scale further due to reserved concurrency or account concurrency limits being reached.

---

## Question 13 — Answer: B

**Explanation:** For complete traces through API Gateway into Lambda, enable X-Ray on both the API stage and the Lambda function.

---

## Question 14 — Answer: B

**Explanation:** In X-Ray, faults generally correspond to 5xx errors. Errors often map to 4xx client issues; throttles are rate-limit related.

---

## Question 15 — Answer: B

**Explanation:** Client-side encryption encrypts data before it leaves the client. Server-side encryption (SSE-*) encrypts after S3 receives the object.

---

## Question 16 — Answer: B

**Explanation:** Provisioned Concurrency pre-initializes Lambda execution environments, eliminating cold starts. Increasing memory can help but doesn't eliminate cold starts entirely.

---

## Question 17 — Answer: B

**Explanation:** High-cardinality partition keys distribute load. Hot keys can be mitigated with sharding suffixes when a natural key is too concentrated.

---

## Question 18 — Answer: C

**Explanation:** The Wait state with callback pattern (.waitForTaskToken) allows Step Functions to pause execution until an external process (like human approval) completes by returning the task token.

---

## Question 19 — Answer: B

**Explanation:** SSE-S3 uses encryption keys managed by Amazon S3. SSE-KMS uses KMS keys; SSE-C uses customer-provided keys.

---

## Question 20 — Answer: A

**Explanation:** User Pools authenticate users and issue JWTs. Identity Pools exchange identity for temporary AWS credentials.

---

## Question 21 — Answer: B

**Explanation:** Prefer Secrets Manager or SSM Parameter Store (SecureString) over plaintext environment variables for secrets, with IAM-controlled access and optional rotation.

---

## Question 22 — Answer: C

**Explanation:** Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming.

---

## Question 23 — Answer: D

**Explanation:** Both ElastiCache Redis and DynamoDB DAX can serve as distributed caches. Redis is more general-purpose; DAX is specifically for DynamoDB.

---

## Question 24 — Answer: B

**Explanation:** Permissions boundaries define the maximum permissions an identity can have; effective permissions are the intersection of identity policies and the boundary.

---

## Question 25 — Answer: B

**Explanation:** Logs Insights can filter REPORT log lines, parse fields like Duration, sort, and limit results for performance analysis.

---

## Question 26 — Answer: B

**Explanation:** AutopublishAlias creates/updates a Lambda alias; DeploymentPreference configures CodeDeploy canary/linear traffic shifting to that alias.

---

## Question 27 — Answer: C

**Explanation:** SecureString parameters are encrypted with AWS KMS. String and StringList store plaintext values.

---

## Question 28 — Answer: B

**Explanation:** SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently.

---

## Question 29 — Answer: B

**Explanation:** S3 Event Notifications can trigger Lambda, SNS, or SQS when events like object creation, deletion, or restoration occur in a bucket.

---

## Question 30 — Answer: B

**Explanation:** When environment variables are encrypted with a CMK, the execution role needs kms:Decrypt (and the key policy must allow the role) to decrypt them at runtime.

---

## Question 31 — Answer: A

**Explanation:** ExternalId in the role trust policy Condition helps ensure only the intended third party can assume the role (confused deputy protection).

---

## Question 32 — Answer: C

**Explanation:** The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services.

---

## Question 33 — Answer: B

**Explanation:** DynamoDB Streams captures a time-ordered sequence of item-level changes (insert, update, delete) in a table, enabling event-driven processing.

---

## Question 34 — Answer: B

**Explanation:** Stack policies protect resources from unintended updates (e.g., databases) during CloudFormation stack operations.

---

## Question 35 — Answer: B

**Explanation:** cdk diff compares local CDK synth output with the currently deployed CloudFormation stack resources.

---

## Question 36 — Answer: A

**Explanation:** DynamoDB Streams + Lambda event source mapping processes insert/update/delete records shortly after they occur.

---

## Question 37 — Answer: C

**Explanation:** S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access.

---

## Question 38 — Answer: B

**Explanation:** GetCallerIdentity is commonly used to verify which principal the current credentials represent (account, user ID, ARN).

---

## Question 39 — Answer: A

**Explanation:** Drift detection compares actual resource configuration with the stack template and reports differences.

---

## Question 40 — Answer: B

**Explanation:** Lambda code can be updated independently via UpdateFunctionCode or IaC updates that change only the function's code property.

---

## Question 41 — Answer: B

**Explanation:** IntegrationLatency is backend call time; Latency is overall API Gateway request time including gateway overhead.

---

## Question 42 — Answer: B

**Explanation:** KMS requires both key policy and IAM permissions. The key policy is foundational; without it granting the account, IAM alone cannot authorize use.

---

## Question 43 — Answer: B

**Explanation:** Cross-account least-privilege access via role assumption (often with ExternalId) or tightly scoped bucket policies is the secure pattern for partner writes.

---

## Question 44 — Answer: B

**Explanation:** A 502 Bad Gateway error from API Gateway with Lambda proxy integration typically means the Lambda function returned an invalid response format. The response must include statusCode, headers, and body.

---

## Question 45 — Answer: B

**Explanation:** In IAM evaluation, an explicit Deny always overrides Allow, regardless of other Allow statements.

---

## Question 46 — Answer: C

**Explanation:** IAM execution roles are the secure way to grant Lambda permissions. Never hardcode credentials or use root accounts. Environment variables for secrets should use Secrets Manager instead.

---

## Question 47 — Answer: C

**Explanation:** ElastiCache (Redis) provides sub-millisecond latency for in-memory data operations, making it ideal for session data. DynamoDB provides single-digit millisecond latency.

---

## Question 48 — Answer: B

**Explanation:** For Lambda, AppSpec configures alias traffic shifting and optional hooks that run validation Lambda functions during deployment.

---

## Question 49 — Answer: B

**Explanation:** SAM Events attach triggers to Lambda (HTTP APIs, queues, topics, schedules, and more) with simplified syntax.

---

## Question 50 — Answer: A

**Explanation:** CodePipeline uses an S3 artifact bucket to pass build/deploy artifacts between pipeline stages.

---

## Question 51 — Answer: C

**Explanation:** Querying by a non-key attribute (status) requires a GSI. The primary table can only be efficiently queried by the partition key and sort key.

---

## Question 52 — Answer: B

**Explanation:** Nested stacks break large templates into reusable components managed as a hierarchy of stacks.

---

## Question 53 — Answer: B

**Explanation:** AWS Fargate is a serverless compute engine for containers that works with ECS and EKS, eliminating the need to manage servers or clusters.

---

## Question 54 — Answer: A

**Explanation:** Cold start initialization time appears as Init Duration in Lambda REPORT logs and related performance metrics.

---

## Question 55 — Answer: C

**Explanation:** GetItem is the most efficient for retrieving a single item by its full primary key (partition + sort key if applicable). It uses minimal RCUs compared to Scan or Query.

---

## Question 56 — Answer: B

**Explanation:** Manual approval actions gate progression (often before prod) until an authorized user approves or rejects.

---

## Question 57 — Answer: B

**Explanation:** Identity Pools exchange authenticated User Pool identities (or other IdPs) for temporary AWS credentials via STS.

---

## Question 58 — Answer: C

**Explanation:** The Choice state evaluates conditions and branches to different states based on the input, similar to an if-else statement.

---

## Question 59 — Answer: B

**Explanation:** INSUFFICIENT_DATA occurs when CloudWatch lacks enough datapoints to evaluate the alarm (e.g., new metric or sparse activity).

---

## Question 60 — Answer: B

**Explanation:** Subscription filters deliver real-time log events matching a filter pattern to streaming or Lambda destinations for processing.

---

## Question 61 — Answer: B

**Explanation:** Fn::Sub substitutes variables and resource attributes into strings, commonly for ARNs and configuration values.

---

## Question 62 — Answer: A

**Explanation:** Async Lambda failures can be routed to a DLQ or on-failure destination (SQS, SNS, EventBridge, another Lambda) for inspection and retry.

---

## Question 63 — Answer: B

**Explanation:** SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages. Successfully processed messages are automatically deleted.

---

## Question 64 — Answer: B

**Explanation:** JSON structured logs work well with Logs Insights filters/parses and make correlation by requestId easier.

---

## Question 65 — Answer: B

**Explanation:** Code outside the handler runs during cold start and is reused for warm invocations. Initialize clients once at module scope for better performance.

---

