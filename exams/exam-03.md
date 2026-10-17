# Practice Exam 3

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Security

Which Parameter Store parameter type stores encrypted values using KMS?

- A) String
- B) StringList
- C) SecureString
- D) HashString

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

**Domain:** Security

A cross-account S3 access scenario requires Account B to read objects in Account A's bucket. Which combination is commonly required?

- A) Only an IAM user in Account B with no bucket policy
- B) Bucket policy in Account A allowing Account B's principal, plus permissions in Account B
- C) Making the bucket public
- D) Disabling encryption

---

## Question 4

**Domain:** Deployment

What does CodeDeploy AppSpec (appspec.yml) define for Lambda deployments?

- A) Only VPC subnets
- B) How traffic is shifted between versions and lifecycle hooks (BeforeAllowTraffic, AfterAllowTraffic)
- C) CloudWatch log retention only
- D) Cognito user attributes

---

## Question 5

**Domain:** Deployment

A developer needs to update only a Lambda function's code without changing infrastructure. Which approach works?

- A) Always recreate the entire CloudFormation stack
- B) Use aws lambda update-function-code or deploy via SAM/CFN updating the function resource code
- C) Change the DynamoDB table name
- D) Disable the API Gateway stage

---

## Question 6

**Domain:** Development

When designing DynamoDB partition keys, what practice helps avoid hot partitions?

- A) Use a single static partition key for all items
- B) Choose high-cardinality keys (and consider write sharding) so traffic spreads across partitions
- C) Always use Scan instead of Query
- D) Disable TTL

---

## Question 7

**Domain:** Deployment

Which Elastic Beanstalk deployment policy is the FASTEST but causes temporary unavailability?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 8

**Domain:** Development

A Lambda function needs to access a DynamoDB table. What is the MOST secure way to grant permissions?

- A) Hardcode AWS access keys in the Lambda function code
- B) Store access keys in Lambda environment variables
- C) Attach an IAM execution role with least-privilege DynamoDB permissions to the Lambda function
- D) Use the AWS account root user credentials

---

## Question 9

**Domain:** Security

Which S3 feature can enforce that all uploads use encryption?

- A) A bucket policy denying PutObject unless s3:x-amz-server-side-encryption is present
- B) CORS only
- C) Transfer Acceleration
- D) Requester Pays

---

## Question 10

**Domain:** Development

A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?

- A) Amazon SQS Standard queue
- B) Amazon SNS
- C) Amazon Kinesis Data Streams
- D) Amazon MQ

---

## Question 11

**Domain:** Security

An IAM policy includes Effect: Deny for s3:DeleteObject. A separate Allow grants s3:*. What is the result for DeleteObject?

- A) Allow always wins
- B) Explicit Deny overrides Allow — DeleteObject is denied
- C) The policies cancel and access is undefined
- D) Only resource-based policies apply

---

## Question 12

**Domain:** Security

A developer wants to use Cognito to allow unauthenticated guest access to AWS resources. Which Cognito feature supports this?

- A) Cognito User Pools
- B) Cognito Identity Pools (Federated Identities)
- C) Cognito Sync
- D) Cognito user groups

---

## Question 13

**Domain:** Security

What does SSE-S3 encryption use for S3 object encryption?

- A) Customer-provided keys only (SSE-C)
- B) S3-managed encryption keys
- C) CloudHSM exclusively
- D) Client-side encryption only

---

## Question 14

**Domain:** Development

When using the AWS SDK, which credential source is preferred for applications running on EC2?

- A) Hardcoded access keys in source control
- B) Instance profile (IAM role attached to the instance)
- C) Root user access keys
- D) Credentials emailed to developers

---

## Question 15

**Domain:** Deployment

What is a CloudFormation change set?

- A) A permanent deletion of the stack
- B) A preview of proposed stack changes that can be reviewed before execution
- C) An automatic CI/CD pipeline
- D) A CDK construct library

---

## Question 16

**Domain:** Development

What is the maximum item size in DynamoDB?

- A) 64 KB
- B) 256 KB
- C) 400 KB
- D) 1 MB

---

## Question 17

**Domain:** Monitoring

A Lambda function shows high Throttles in CloudWatch. What does this indicate?

- A) The function code has a syntax error
- B) Concurrent executions exceeded reserved or account concurrency limits
- C) The DynamoDB table is empty
- D) X-Ray is disabled

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

**Domain:** Deployment

A developer wants to use environment-specific configurations in a SAM template. How can they achieve this?

- A) Hardcode values in the template
- B) Use SAM template parameters with different values per environment
- C) Use separate templates for each environment
- D) Use environment variables in CloudFormation

---

## Question 20

**Domain:** Monitoring

Which service should be used to monitor API Gateway REST API access logs?

- A) CloudTrail only
- B) CloudWatch Logs with API Gateway access logging enabled
- C) S3 only
- D) X-Ray only

---

## Question 21

**Domain:** Monitoring

Which X-Ray feature allows searching traces by custom attributes?

- A) Annotations
- B) Metadata
- C) Segments
- D) Sampling rules

---

## Question 22

**Domain:** Deployment

Which AWS CDK construct level provides the highest abstraction with pre-configured patterns?

- A) L1 constructs (CfnXxx)
- B) L2 constructs
- C) L3 constructs (Patterns)
- D) L0 constructs

---

## Question 23

**Domain:** Security

API Gateway Cognito User Pool authorizers validate which token by default for REST APIs?

- A) Refresh token only
- B) ID token (JWT) from the Cognito User Pool
- C) AWS access key ID
- D) SAML assertion only

---

## Question 24

**Domain:** Security

Which KMS key policy statement is required for a CMK to be usable by IAM principals in the account?

- A) No key policy is needed; IAM alone is always sufficient
- B) The key policy must allow the account/root (or specific principals); IAM permissions then further control access
- C) Only CloudTrail can use CMKs
- D) Key policies only apply to AWS managed keys

---

## Question 25

**Domain:** Development

API Gateway stage variables are commonly used to:

- A) Encrypt Lambda environment variables
- B) Parameterize backend endpoints or Lambda aliases per stage (dev/test/prod)
- C) Replace IAM policies
- D) Increase Lambda memory at runtime

---

## Question 26

**Domain:** Development

A developer is building a REST API with API Gateway. The backend Lambda function returns a response, but the client receives a 502 error. What is the MOST likely cause?

- A) The API Gateway does not have CORS enabled
- B) The Lambda function is not returning a properly formatted proxy response with statusCode, headers, and body
- C) The API Gateway is missing request validation
- D) The client is sending the wrong Content-Type header

---

## Question 27

**Domain:** Monitoring

An API Gateway REST API is returning 429 errors. What should the developer do?

- A) Increase the Lambda function memory
- B) Enable throttling with appropriate rate and burst limits
- C) Switch to a regional API endpoint
- D) Disable authentication

---

## Question 28

**Domain:** Security

What is the purpose of an IAM permissions boundary?

- A) To replace SCPs in Organizations
- B) To set the maximum permissions an IAM identity can be granted, even if policies allow more
- C) To encrypt IAM credentials
- D) To enable MFA devices

---

## Question 29

**Domain:** Deployment

Which Elastic Beanstalk deployment policy launches a temporary set of instances alongside the old ones to avoid capacity reduction?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Traffic splitting only on Lambda

---

## Question 30

**Domain:** Development

A developer needs to deploy a Lambda function that processes SQS messages. The function must read messages in batches of 10 and delete them after processing. Which of the following is the BEST approach?

- A) Poll SQS manually using a scheduled Lambda function every minute
- B) Configure SQS as an event source for the Lambda function with a batch size of 10
- C) Use SNS to fan out messages to individual Lambda invocations
- D) Use Kinesis Data Streams to buffer messages before processing

---

## Question 31

**Domain:** Deployment

CloudFormation Fn::Sub is used to:

- A) Delete stacks
- B) Perform string substitution with ${Variable} placeholders
- C) Create change sets only
- D) Import existing resources exclusively

---

## Question 32

**Domain:** Development

A developer needs to run a long-running workflow with retries, branching, and parallel steps coordinating multiple Lambda functions. Which service fits BEST?

- A) A single Lambda with a 15-minute sleep loop
- B) AWS Step Functions
- C) Amazon SNS only
- D) Amazon CloudFront

---

## Question 33

**Domain:** Deployment

In CodeBuild, privileged mode is required primarily when the build needs to:

- A) Call DynamoDB
- B) Build Docker images (Docker-in-Docker)
- C) Write CloudWatch Logs
- D) Assume an IAM role

---

## Question 34

**Domain:** Deployment

SAM AutopublishAlias combined with DeploymentPreference enables:

- A) Manual zip uploads only
- B) Automatic version/alias publishing with gradual CodeDeploy traffic shifting
- C) Disabling CloudWatch Logs
- D) Creating EC2 instances

---

## Question 35

**Domain:** Monitoring

What is the default sampling rate for X-Ray when no sampling rules are configured?

- A) 0% (no traces)
- B) 100% (all requests)
- C) 1 request per second, then 5% of additional requests
- D) 10% of all requests

---

## Question 36

**Domain:** Deployment

What does cdk diff show?

- A) Only TypeScript compile errors
- B) Differences between the synthesized template and the deployed stack
- C) Git commit history
- D) Lambda cold start metrics

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

**Domain:** Monitoring

What is the purpose of a CloudWatch metric filter?

- A) To filter which logs are sent to S3
- B) To extract metric values from log events
- C) To delete old log entries
- D) To encrypt log data

---

## Question 39

**Domain:** Deployment

What is the purpose of 'sam build' command?

- A) To deploy the SAM application
- B) To create a deployment artifact by building Lambda functions and copying dependencies
- C) To delete a SAM application
- D) To test the SAM application in production

---

## Question 40

**Domain:** Security

What does STS GetCallerIdentity return?

- A) A new access key pair
- B) The Account, UserId, and Arn of the credentials making the call
- C) A Cognito JWT
- D) A CloudTrail digest

---

## Question 41

**Domain:** Security

A developer encrypts Lambda environment variables with a customer-managed KMS key. What additional permission does the Lambda execution role need?

- A) kms:CreateKey
- B) kms:Decrypt on that CMK
- C) iam:PassRole on the KMS key
- D) s3:GetObject on all buckets

---

## Question 42

**Domain:** Development

Which DynamoDB operation is MOST efficient for retrieving a single item by its primary key?

- A) Scan with a filter expression
- B) Query with the partition key
- C) GetItem with the full primary key
- D) BatchGetItem with a single item

---

## Question 43

**Domain:** Development

A developer needs to store user session data with sub-millisecond latency. Which AWS service should be used?

- A) Amazon S3
- B) Amazon DynamoDB
- C) Amazon ElastiCache (Redis)
- D) Amazon RDS

---

## Question 44

**Domain:** Development

Which Lambda concurrency control reserves capacity for a critical function so other functions cannot consume the account limit?

- A) Reserved concurrency
- B) Provisioned concurrency only
- C) Asynchronous invocation
- D) Dead-letter queues

---

## Question 45

**Domain:** Security

Which Cognito component issues JWT tokens (ID, access, refresh) after user sign-in?

- A) Cognito User Pools
- B) Cognito Identity Pools only
- C) AWS KMS
- D) AWS WAF

---

## Question 46

**Domain:** Security

Which header or mechanism helps protect against confused deputy attacks when using AssumeRole with third parties?

- A) External ID in the trust policy Condition
- B) Larger session duration
- C) Disabling MFA
- D) Using * for Principal

---

## Question 47

**Domain:** Development

What is the maximum execution timeout for an AWS Lambda function?

- A) 30 seconds
- B) 5 minutes
- C) 15 minutes
- D) 1 hour

---

## Question 48

**Domain:** Development

Which ECS launch type eliminates the need to manage underlying server infrastructure?

- A) EC2 launch type
- B) Fargate launch type
- C) External launch type
- D) Lambda launch type

---

## Question 49

**Domain:** Monitoring

What is the default retention period for CloudWatch Logs?

- A) 7 days
- B) 30 days
- C) Never expire (infinite retention)
- D) 90 days

---

## Question 50

**Domain:** Security

What is the safest way to allow a third-party SaaS to write logs into your S3 bucket?

- A) Share root credentials
- B) Use a bucket policy with a dedicated IAM role/external ID (or assume-role) and least-privilege PutObject on a prefix
- C) Make the bucket fully public
- D) Disable all encryption

---

## Question 51

**Domain:** Deployment

A developer wants to test a SAM application locally before deploying. Which command runs the Lambda function locally?

- A) sam validate
- B) sam local invoke
- C) sam local start-api
- D) sam build

---

## Question 52

**Domain:** Monitoring

A developer receives a 'ProvisionedThroughputExceededException' from DynamoDB. What is the BEST immediate action?

- A) Delete the table and recreate it
- B) Switch to on-demand capacity mode or increase provisioned capacity
- C) Enable encryption
- D) Add a global secondary index

---

## Question 53

**Domain:** Development

A developer needs to process DynamoDB item changes with Lambda near real time. What should they configure?

- A) DynamoDB Streams as a Lambda event source
- B) S3 inventory reports
- C) CloudFront invalidations
- D) ECR lifecycle policies

---

## Question 54

**Domain:** Monitoring

A developer needs to be notified when a DynamoDB table's consumed capacity exceeds 80%. What should they configure?

- A) A CloudWatch Alarm on the ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits metric
- B) A DynamoDB Stream
- C) A CloudTrail trail
- D) An X-Ray sampling rule

---

## Question 55

**Domain:** Monitoring

A Lambda function in a VPC cannot reach the internet. What is missing?

- A) More memory
- B) A NAT Gateway in the VPC's public subnet
- C) A larger timeout
- D) An Elastic IP address

---

## Question 56

**Domain:** Deployment

Which CodePipeline action provider typically stores source code from a Git repository?

- A) AWS CodeCommit, GitHub, or Amazon S3 as Source actions
- B) Amazon Athena
- C) Amazon Macie
- D) AWS Batch only

---

## Question 57

**Domain:** Development

A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?

- A) SQS + Lambda
- B) SNS + SQS + Lambda
- C) Kinesis + Lambda
- D) API Gateway + Lambda

---

## Question 58

**Domain:** Security

Which condition key restricts an IAM policy so that requests must come from a specific VPC endpoint?

- A) aws:SourceIp
- B) aws:SourceVpce
- C) aws:RequestedRegion
- D) aws:MultiFactorAuthPresent

---

## Question 59

**Domain:** Security

A mobile app needs temporary AWS credentials after Cognito User Pool login. What should be configured?

- A) Only IAM users with long-lived keys in the app
- B) Cognito Identity Pool federated with the User Pool to obtain temporary credentials
- C) Root account keys
- D) CloudFront key pairs only

---

## Question 60

**Domain:** Development

A developer stores large objects in S3 and metadata in DynamoDB. What is a common pattern for referencing the object?

- A) Store the entire object bytes in DynamoDB
- B) Store the S3 bucket/key (or URL) in DynamoDB and fetch the object from S3 when needed
- C) Use only EBS volumes
- D) Embed Base64 objects in SQS messages

---

## Question 61

**Domain:** Development

A Local Secondary Index (LSI) differs from a GSI because an LSI:

- A) Can have a different partition key from the base table
- B) Must share the same partition key as the base table and can only be created at table creation
- C) Supports only eventually consistent reads
- D) Cannot include a sort key

---

## Question 62

**Domain:** Development

An application must publish events to multiple subscriber types (email, SQS, Lambda) from one producer. Which service is BEST as the fan-out hub?

- A) Amazon SNS
- B) Amazon SQS alone
- C) Amazon S3
- D) Amazon ECR

---

## Question 63

**Domain:** Deployment

CloudFormation nested stacks are used primarily to:

- A) Avoid using parameters
- B) Modularize large templates by embedding child stacks as AWS::CloudFormation::Stack resources
- C) Bypass IAM
- D) Replace CodePipeline

---

## Question 64

**Domain:** Monitoring

A developer wants to use X-Ray to trace a Lambda function. What is the MINIMUM configuration needed?

- A) Install the X-Ray SDK and modify all code
- B) Enable X-Ray active tracing on the Lambda function configuration
- C) Create a CloudTrail trail
- D) Enable VPC Flow Logs

---

## Question 65

**Domain:** Deployment

What is the purpose of a CodePipeline manual approval action?

- A) To compile source code
- B) To pause the pipeline until a reviewer approves before continuing to production deploy
- C) To create IAM users
- D) To rotate KMS keys

---


---

# Answers & Explanations

---

## Question 1 — Answer: C

**Explanation:** SecureString parameters are encrypted with AWS KMS. String and StringList store plaintext values.

---

## Question 2 — Answer: B

**Explanation:** Prefer Secrets Manager or SSM Parameter Store (SecureString) over plaintext environment variables for secrets, with IAM-controlled access and optional rotation.

---

## Question 3 — Answer: B

**Explanation:** Cross-account S3 access typically needs a resource-based bucket policy granting the external principal and identity-based permissions in the caller's account.

---

## Question 4 — Answer: B

**Explanation:** For Lambda, AppSpec configures alias traffic shifting and optional hooks that run validation Lambda functions during deployment.

---

## Question 5 — Answer: B

**Explanation:** Lambda code can be updated independently via UpdateFunctionCode or IaC updates that change only the function's code property.

---

## Question 6 — Answer: B

**Explanation:** High-cardinality partition keys distribute load. Hot keys can be mitigated with sharding suffixes when a natural key is too concentrated.

---

## Question 7 — Answer: A

**Explanation:** All at once deploys to all instances simultaneously, making it the fastest but causes temporary downtime during the deployment.

---

## Question 8 — Answer: C

**Explanation:** IAM execution roles are the secure way to grant Lambda permissions. Never hardcode credentials or use root accounts. Environment variables for secrets should use Secrets Manager instead.

---

## Question 9 — Answer: A

**Explanation:** Bucket policies can deny unencrypted uploads by requiring the encryption header or using default encryption plus Deny for incorrect encryption.

---

## Question 10 — Answer: C

**Explanation:** Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming.

---

## Question 11 — Answer: B

**Explanation:** In IAM evaluation, an explicit Deny always overrides Allow, regardless of other Allow statements.

---

## Question 12 — Answer: B

**Explanation:** Cognito Identity Pools support both authenticated and unauthenticated (guest) identities, providing temporary AWS credentials for accessing resources.

---

## Question 13 — Answer: B

**Explanation:** SSE-S3 uses encryption keys managed by Amazon S3. SSE-KMS uses KMS keys; SSE-C uses customer-provided keys.

---

## Question 14 — Answer: B

**Explanation:** EC2 instance profiles provide temporary credentials via the instance metadata service; the SDK retrieves them automatically.

---

## Question 15 — Answer: B

**Explanation:** Change sets show the impact of a proposed update (add/modify/delete resources) before you execute the update.

---

## Question 16 — Answer: C

**Explanation:** DynamoDB items are limited to 400 KB. Larger payloads should be stored in S3 with a reference in DynamoDB.

---

## Question 17 — Answer: B

**Explanation:** Throttles occur when Lambda cannot scale further due to reserved concurrency or account concurrency limits being reached.

---

## Question 18 — Answer: C

**Explanation:** The Wait state with callback pattern (.waitForTaskToken) allows Step Functions to pause execution until an external process (like human approval) completes by returning the task token.

---

## Question 19 — Answer: B

**Explanation:** SAM templates support CloudFormation parameters, allowing you to pass environment-specific values at deployment time using parameter overrides.

---

## Question 20 — Answer: B

**Explanation:** API Gateway can send access logs to CloudWatch Logs with detailed request/response information for monitoring and troubleshooting.

---

## Question 21 — Answer: A

**Explanation:** Annotations are indexed key-value pairs that can be used to filter and search traces. Metadata is not indexed.

---

## Question 22 — Answer: C

**Explanation:** L3 constructs (also called patterns) provide the highest level of abstraction with pre-configured defaults and best practices.

---

## Question 23 — Answer: B

**Explanation:** Cognito authorizers validate JWTs (typically the ID token) issued by the configured User Pool before allowing the request.

---

## Question 24 — Answer: B

**Explanation:** KMS requires both key policy and IAM permissions. The key policy is foundational; without it granting the account, IAM alone cannot authorize use.

---

## Question 25 — Answer: B

**Explanation:** Stage variables let you configure stage-specific values such as Lambda alias ARNs or HTTP endpoints without changing the API definition for each environment.

---

## Question 26 — Answer: B

**Explanation:** A 502 Bad Gateway error from API Gateway with Lambda proxy integration typically means the Lambda function returned an invalid response format. The response must include statusCode, headers, and body.

---

## Question 27 — Answer: B

**Explanation:** 429 Too Many Requests indicates throttling. Configure appropriate rate/burst limits or request a limit increase from AWS.

---

## Question 28 — Answer: B

**Explanation:** Permissions boundaries define the maximum permissions an identity can have; effective permissions are the intersection of identity policies and the boundary.

---

## Question 29 — Answer: C

**Explanation:** Rolling with additional batch launches new instances first so capacity is not reduced while old instances are updated.

---

## Question 30 — Answer: B

**Explanation:** SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages. Successfully processed messages are automatically deleted.

---

## Question 31 — Answer: B

**Explanation:** Fn::Sub substitutes variables and resource attributes into strings, commonly for ARNs and configuration values.

---

## Question 32 — Answer: B

**Explanation:** Step Functions orchestrates multi-step workflows with retries, catchers, Choice, Parallel, and Map states across AWS services.

---

## Question 33 — Answer: B

**Explanation:** Privileged mode grants elevated permissions needed to run Docker daemon operations for building container images.

---

## Question 34 — Answer: B

**Explanation:** AutopublishAlias creates/updates a Lambda alias; DeploymentPreference configures CodeDeploy canary/linear traffic shifting to that alias.

---

## Question 35 — Answer: C

**Explanation:** The default X-Ray sampling rule traces the first request each second, then 5% of additional requests.

---

## Question 36 — Answer: B

**Explanation:** cdk diff compares local CDK synth output with the currently deployed CloudFormation stack resources.

---

## Question 37 — Answer: C

**Explanation:** S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access.

---

## Question 38 — Answer: B

**Explanation:** Metric filters define patterns to match in log events and turn them into CloudWatch numeric metrics for alarms and dashboards.

---

## Question 39 — Answer: B

**Explanation:** sam build processes the SAM template, builds Lambda functions (installing dependencies), and creates deployment artifacts in the .aws-sam directory.

---

## Question 40 — Answer: B

**Explanation:** GetCallerIdentity is commonly used to verify which principal the current credentials represent (account, user ID, ARN).

---

## Question 41 — Answer: B

**Explanation:** When environment variables are encrypted with a CMK, the execution role needs kms:Decrypt (and the key policy must allow the role) to decrypt them at runtime.

---

## Question 42 — Answer: C

**Explanation:** GetItem is the most efficient for retrieving a single item by its full primary key (partition + sort key if applicable). It uses minimal RCUs compared to Scan or Query.

---

## Question 43 — Answer: C

**Explanation:** ElastiCache (Redis) provides sub-millisecond latency for in-memory data operations, making it ideal for session data. DynamoDB provides single-digit millisecond latency.

---

## Question 44 — Answer: A

**Explanation:** Reserved concurrency guarantees a maximum concurrent execution limit for a function and reserves that capacity from the account pool.

---

## Question 45 — Answer: A

**Explanation:** User Pools authenticate users and issue JWTs. Identity Pools exchange identity for temporary AWS credentials.

---

## Question 46 — Answer: A

**Explanation:** ExternalId in the role trust policy Condition helps ensure only the intended third party can assume the role (confused deputy protection).

---

## Question 47 — Answer: C

**Explanation:** The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services.

---

## Question 48 — Answer: B

**Explanation:** AWS Fargate is a serverless compute engine for containers that works with ECS and EKS, eliminating the need to manage servers or clusters.

---

## Question 49 — Answer: C

**Explanation:** By default, CloudWatch Logs never expire. You can configure retention from 1 day to 10 years, or keep data indefinitely.

---

## Question 50 — Answer: B

**Explanation:** Cross-account least-privilege access via role assumption (often with ExternalId) or tightly scoped bucket policies is the secure pattern for partner writes.

---

## Question 51 — Answer: B

**Explanation:** sam local invoke runs a Lambda function locally using Docker. sam local start-api starts a local API server instead of invoking directly.

---

## Question 52 — Answer: B

**Explanation:** This error means you've exceeded provisioned throughput. Switch to on-demand (PAY_PER_REQUEST) or increase RCUs/WCUs.

---

## Question 53 — Answer: A

**Explanation:** DynamoDB Streams + Lambda event source mapping processes insert/update/delete records shortly after they occur.

---

## Question 54 — Answer: A

**Explanation:** CloudWatch Alarms can monitor DynamoDB capacity metrics and trigger notifications via SNS.

---

## Question 55 — Answer: B

**Explanation:** Lambda in a VPC needs a NAT Gateway (or similar) in a public subnet for internet access; place the function in a private subnet with a route to the NAT.

---

## Question 56 — Answer: A

**Explanation:** CodePipeline Source stages commonly pull from CodeCommit, GitHub/GitHub Enterprise, Bitbucket, or S3 artifacts.

---

## Question 57 — Answer: B

**Explanation:** SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently.

---

## Question 58 — Answer: B

**Explanation:** aws:SourceVpce (and related VPC endpoint condition keys) can require that API calls originate from a specified VPC endpoint.

---

## Question 59 — Answer: B

**Explanation:** Identity Pools exchange authenticated User Pool identities (or other IdPs) for temporary AWS credentials via STS.

---

## Question 60 — Answer: B

**Explanation:** The claim-check / metadata pattern stores pointers in DynamoDB and large payloads in S3, staying within DynamoDB item size limits (400 KB).

---

## Question 61 — Answer: B

**Explanation:** LSIs share the base table partition key, provide an alternate sort key, and must be defined when the table is created. GSIs can use different partition keys.

---

## Question 62 — Answer: A

**Explanation:** SNS is a pub/sub hub that can deliver to SQS, Lambda, HTTP, email, and other protocols from a single publish.

---

## Question 63 — Answer: B

**Explanation:** Nested stacks break large templates into reusable components managed as a hierarchy of stacks.

---

## Question 64 — Answer: B

**Explanation:** For Lambda, enabling active tracing in the function configuration provides basic tracing. The X-Ray SDK is needed for custom subsegments and annotations.

---

## Question 65 — Answer: B

**Explanation:** Manual approval actions gate progression (often before prod) until an authorized user approves or rejects.

---

