# Practice Exam 3

**AWS Certified Developer - Associate (DVA-C02)**

- **Questions:** 65
- **Time:** 130 minutes (actual exam is 130 min)
- **Passing Score:** 720/1000

> 💡 **Instructions:** Choose the best answer for each question. Answers and explanations are at the end.

---

## Question 1

**Domain:** Development

A developer needs to implement a state machine that branches based on output from a Lambda function. Which Step Functions state type should be used?

- A) Task
- B) Pass
- C) Choice
- D) Wait

---

## Question 2

**Domain:** Monitoring

A developer wants to use X-Ray to trace a Lambda function. What is the MINIMUM configuration needed?

- A) Install the X-Ray SDK and modify all code
- B) Enable X-Ray active tracing on the Lambda function configuration
- C) Create a CloudTrail trail
- D) Enable VPC Flow Logs

---

## Question 3

**Domain:** Security

An application running on ECS needs to access DynamoDB. How should the developer configure permissions?

- A) Store access keys in the container image
- B) Use an IAM task role for the ECS task definition
- C) Use EC2 instance profiles
- D) Create a separate IAM user for each container

---

## Question 4

**Domain:** Security

A company wants to implement user authentication for a web application without managing passwords. Which service should they use?

- A) AWS IAM
- B) Amazon Cognito
- C) AWS Secrets Manager
- D) AWS WAF

---

## Question 5

**Domain:** Deployment

What is the purpose of 'sam build' command?

- A) To deploy the SAM application
- B) To create a deployment artifact by building Lambda functions and copying dependencies
- C) To delete a SAM application
- D) To test the SAM application in production

---

## Question 6

**Domain:** Monitoring

An API Gateway REST API is returning 429 errors. What should the developer do?

- A) Increase the Lambda function memory
- B) Enable throttling with appropriate rate and burst limits
- C) Switch to a regional API endpoint
- D) Disable authentication

---

## Question 7

**Domain:** Development

Which DynamoDB operation is MOST efficient for retrieving a single item by its primary key?

- A) Scan with a filter expression
- B) Query with the partition key
- C) GetItem with the full primary key
- D) BatchGetItem with a single item

---

## Question 8

**Domain:** Monitoring

Which CloudWatch metric is used to monitor Lambda function invocations?

- A) CPUUtilization
- B) Invocations
- C) RequestCount
- D) Throughput

---

## Question 9

**Domain:** Monitoring

A developer receives a 'ProvisionedThroughputExceededException' from DynamoDB. What is the BEST immediate action?

- A) Delete the table and recreate it
- B) Switch to on-demand capacity mode or increase provisioned capacity
- C) Enable encryption
- D) Add a global secondary index

---

## Question 10

**Domain:** Monitoring

A developer needs to search through Lambda function logs to find errors. Which tool provides the MOST powerful query capabilities?

- A) CloudWatch Logs console with simple text search
- B) CloudWatch Logs Insights
- C) AWS X-Ray
- D) CloudTrail

---

## Question 11

**Domain:** Security

Which feature of S3 prevents accidental deletion of objects?

- A) Server-side encryption
- B) Versioning with MFA Delete
- C) CORS configuration
- D) Transfer Acceleration

---

## Question 12

**Domain:** Monitoring

A Lambda function in a VPC cannot reach the internet. What is missing?

- A) More memory
- B) A NAT Gateway in the VPC's public subnet
- C) A larger timeout
- D) An Elastic IP address

---

## Question 13

**Domain:** Deployment

A developer is using AWS CDK to define infrastructure. Which command generates the CloudFormation template without deploying?

- A) cdk deploy
- B) cdk synth
- C) cdk init
- D) cdk diff

---

## Question 14

**Domain:** Monitoring

What is the purpose of a CloudWatch metric filter?

- A) To filter which logs are sent to S3
- B) To extract metric values from log events
- C) To delete old log entries
- D) To encrypt log data

---

## Question 15

**Domain:** Development

Which ECS launch type eliminates the need to manage underlying server infrastructure?

- A) EC2 launch type
- B) Fargate launch type
- C) External launch type
- D) Lambda launch type

---

## Question 16

**Domain:** Monitoring

A developer wants to create a CloudWatch alarm that triggers when Lambda error rate exceeds 5%. Which metric should they use?

- A) Invocations
- B) Duration
- C) Errors (with math expression Errors/Invocations)
- D) Throttles

---

## Question 17

**Domain:** Deployment

What does the 'Transform: AWS::Serverless-2016-10-31' section in a CloudFormation template indicate?

- A) The template is being converted to JSON
- B) The template uses AWS SAM syntax that needs to be transformed to standard CloudFormation
- C) The template is for a legacy application
- D) The template uses CDK constructs

---

## Question 18

**Domain:** Deployment

Which CloudFormation intrinsic function is used to reference a resource's attribute?

- A) Fn::Ref
- B) Fn::GetAtt
- C) Fn::Sub
- D) Fn::Join

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

**Domain:** Deployment

A developer wants to share a Lambda function's ARN from one CloudFormation stack to another. How can they do this?

- A) Use Fn::Ref in the second stack
- B) Use Outputs with Export in the first stack and Fn::ImportValue in the second stack
- C) Hardcode the ARN in both stacks
- D) Use SSM parameters automatically

---

## Question 21

**Domain:** Security

What is the principle of least privilege in AWS IAM?

- A) Granting all permissions to all users
- B) Granting only the minimum permissions needed to perform a task
- C) Using only managed policies
- D) Denying all access by default and using IAM roles only

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

**Domain:** Deployment

What is the purpose of a buildspec.yml file in AWS CodeBuild?

- A) It defines the infrastructure resources
- B) It contains the build commands and settings for CodeBuild
- C) It configures CodePipeline stages
- D) It defines IAM policies for the build

---

## Question 24

**Domain:** Development

When building a DynamoDB table for an e-commerce application, which access pattern requires a Global Secondary Index (GSI)?

- A) Get order by orderId (partition key)
- B) Get all orders for a customer sorted by date (composite key)
- C) Get all orders with status 'PENDING' regardless of customer
- D) Delete an order by orderId

---

## Question 25

**Domain:** Security

What is the difference between a resource-based policy and an identity-based policy in AWS?

- A) They are the same thing
- B) Resource-based policies are attached to resources (like S3 buckets), identity-based policies are attached to IAM principals
- C) Resource-based policies are only for S3
- D) Identity-based policies are more restrictive

---

## Question 26

**Domain:** Monitoring

A developer needs to be notified when a DynamoDB table's consumed capacity exceeds 80%. What should they configure?

- A) A CloudWatch Alarm on the ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits metric
- B) A DynamoDB Stream
- C) A CloudTrail trail
- D) An X-Ray sampling rule

---

## Question 27

**Domain:** Deployment

In CloudFormation, what happens when a stack update fails?

- A) The stack is deleted
- B) Changes are automatically rolled back to the previous known good state
- C) The stack is paused for manual review
- D) Only the failed resource is deleted

---

## Question 28

**Domain:** Development

A Lambda function needs to access a DynamoDB table. What is the MOST secure way to grant permissions?

- A) Hardcode AWS access keys in the Lambda function code
- B) Store access keys in Lambda environment variables
- C) Attach an IAM execution role with least-privilege DynamoDB permissions to the Lambda function
- D) Use the AWS account root user credentials

---

## Question 29

**Domain:** Deployment

Which AWS SAM CLI command validates a SAM template locally?

- A) sam validate
- B) sam deploy --no-execute-changeset
- C) sam build --validate
- D) sam local invoke

---

## Question 30

**Domain:** Security

Which API Gateway authorization type uses a Lambda function to validate tokens?

- A) NONE
- B) AWS_IAM
- C) COGNITO_USER_POOLS
- D) CUSTOM (Lambda Authorizer)

---

## Question 31

**Domain:** Security

A developer wants to use Cognito to allow unauthenticated guest access to AWS resources. Which Cognito feature supports this?

- A) Cognito User Pools
- B) Cognito Identity Pools (Federated Identities)
- C) Cognito Sync
- D) Cognito user groups

---

## Question 32

**Domain:** Monitoring

Which AWS service provides a record of API calls made in an AWS account?

- A) CloudWatch Logs
- B) CloudTrail
- C) X-Ray
- D) VPC Flow Logs

---

## Question 33

**Domain:** Security

A developer needs to implement API key-based authentication for a public API. Which approach should they use?

- A) IAM authentication on API Gateway
- B) API Gateway with API keys and usage plans
- C) Cognito User Pools
- D) Lambda authorizer that validates API keys

---

## Question 34

**Domain:** Development

A Step Functions workflow needs to wait for human approval before proceeding. Which state type should be used?

- A) Task state
- B) Choice state
- C) Wait state with a callback pattern
- D) Succeed state

---

## Question 35

**Domain:** Security

A developer needs to grant a Lambda function access to read objects from an S3 bucket. What is the MOST secure approach?

- A) Embed AWS access keys in the Lambda function code
- B) Create an IAM role with S3 read permissions and attach it to the Lambda function
- C) Make the S3 bucket public
- D) Use bucket policies that allow anonymous access

---

## Question 36

**Domain:** Development

What is the maximum execution timeout for an AWS Lambda function?

- A) 30 seconds
- B) 5 minutes
- C) 15 minutes
- D) 1 hour

---

## Question 37

**Domain:** Security

A developer needs to securely store a database connection string for a Lambda function. The string needs to be rotated every 30 days. Which solution is BEST?

- A) Store it in a Lambda environment variable
- B) Store it in AWS Secrets Manager with automatic rotation
- C) Store it in S3 with server-side encryption
- D) Store it in AWS Systems Manager Parameter Store as a String type

---

## Question 38

**Domain:** Development

A developer needs to store user session data with sub-millisecond latency. Which AWS service should be used?

- A) Amazon S3
- B) Amazon DynamoDB
- C) Amazon ElastiCache (Redis)
- D) Amazon RDS

---

## Question 39

**Domain:** Development

A developer needs to deploy a Lambda function that processes SQS messages. The function must read messages in batches of 10 and delete them after processing. Which of the following is the BEST approach?

- A) Poll SQS manually using a scheduled Lambda function every minute
- B) Configure SQS as an event source for the Lambda function with a batch size of 10
- C) Use SNS to fan out messages to individual Lambda invocations
- D) Use Kinesis Data Streams to buffer messages before processing

---

## Question 40

**Domain:** Deployment

A developer wants to perform blue/green deployments for a Lambda function. Which deployment preference should they use in SAM?

- A) AllAtOnce
- B) Canary10Percent5Minutes
- C) Linear10PercentEvery3Minutes
- D) Rolling

---

## Question 41

**Domain:** Monitoring

Which X-Ray feature allows searching traces by custom attributes?

- A) Annotations
- B) Metadata
- C) Segments
- D) Sampling rules

---

## Question 42

**Domain:** Deployment

A developer wants to deploy infrastructure as code for a serverless application. Which tool is PURPOSE-BUILT for this?

- A) AWS CloudFormation directly
- B) AWS SAM (Serverless Application Model)
- C) AWS Elastic Beanstalk
- D) AWS OpsWorks

---

## Question 43

**Domain:** Security

A developer needs to encrypt data larger than 4KB using KMS. What is the recommended approach?

- A) Call KMS Encrypt repeatedly for each 4KB chunk
- B) Use envelope encryption with GenerateDataKey
- C) Use KMS with a larger key size
- D) Compress the data to under 4KB

---

## Question 44

**Domain:** Deployment

Which Elastic Beanstalk deployment policy is the FASTEST but causes temporary unavailability?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 45

**Domain:** Security

A developer wants to use temporary credentials to access AWS resources from an on-premises application. Which STS API should they call?

- A) GetSessionToken
- B) AssumeRole
- C) GetFederationToken
- D) DecodeAuthorizationMessage

---

## Question 46

**Domain:** Development

A developer is building a REST API with API Gateway. The backend Lambda function returns a response, but the client receives a 502 error. What is the MOST likely cause?

- A) The API Gateway does not have CORS enabled
- B) The Lambda function is not returning a properly formatted proxy response with statusCode, headers, and body
- C) The API Gateway is missing request validation
- D) The client is sending the wrong Content-Type header

---

## Question 47

**Domain:** Security

A developer is reviewing an IAM policy and finds: 'Action': 's3:*', 'Resource': '*'. What security concern does this raise?

- A) The policy syntax is invalid
- B) The policy violates least privilege — it grants full S3 access to all buckets
- C) The policy uses a deprecated format
- D) The policy cannot be attached to a role

---

## Question 48

**Domain:** Monitoring

What is the default retention period for CloudWatch Logs?

- A) 7 days
- B) 30 days
- C) Never expire (infinite retention)
- D) 90 days

---

## Question 49

**Domain:** Monitoring

A Lambda function is timing out when connecting to an RDS database in a VPC. What is the MOST likely cause?

- A) The Lambda function has insufficient memory
- B) The Lambda function's security group doesn't allow outbound traffic to RDS
- C) The Lambda function is not configured to run in the VPC
- D) Both B and C could be causes

---

## Question 50

**Domain:** Development

A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?

- A) Amazon SQS Standard queue
- B) Amazon SNS
- C) Amazon Kinesis Data Streams
- D) Amazon MQ

---

## Question 51

**Domain:** Deployment

A developer wants to use environment-specific configurations in a SAM template. How can they achieve this?

- A) Hardcode values in the template
- B) Use SAM template parameters with different values per environment
- C) Use separate templates for each environment
- D) Use environment variables in CloudFormation

---

## Question 52

**Domain:** Development

Which S3 storage class is MOST cost-effective for data that is accessed once a quarter?

- A) S3 Standard
- B) S3 Intelligent-Tiering
- C) S3 Standard-IA (Infrequent Access)
- D) S3 Glacier Deep Archive

---

## Question 53

**Domain:** Deployment

Which Elastic Beanstalk deployment strategy has the HIGHEST availability but takes the longest?

- A) All at once
- B) Rolling
- C) Rolling with additional batch
- D) Immutable

---

## Question 54

**Domain:** Security

Which AWS service provides automatic rotation of database credentials?

- A) AWS Systems Manager Parameter Store
- B) AWS Secrets Manager
- C) AWS KMS
- D) AWS IAM

---

## Question 55

**Domain:** Development

Which DynamoDB feature captures item-level modifications in a table?

- A) Global Secondary Index
- B) DynamoDB Streams
- C) Time-to-Live (TTL)
- D) Point-in-Time Recovery

---

## Question 56

**Domain:** Monitoring

A developer needs to trace requests across multiple Lambda functions and API Gateway. Which service should they enable?

- A) CloudWatch Logs
- B) CloudTrail
- C) AWS X-Ray
- D) CloudWatch Alarms

---

## Question 57

**Domain:** Development

A Lambda function is experiencing cold start latency. Which approach would BEST reduce this?

- A) Increase the Lambda memory allocation
- B) Use Provisioned Concurrency
- C) Add more code to the Lambda function
- D) Decrease the timeout setting

---

## Question 58

**Domain:** Monitoring

What is the default sampling rate for X-Ray when no sampling rules are configured?

- A) 0% (no traces)
- B) 100% (all requests)
- C) 1 request per second, then 5% of additional requests
- D) 10% of all requests

---

## Question 59

**Domain:** Deployment

A developer needs to deploy a containerized application without managing any infrastructure. Which combination should they use?

- A) EC2 + Docker
- B) ECS with Fargate launch type
- C) ECS with EC2 launch type
- D) Elastic Beanstalk with Docker platform

---

## Question 60

**Domain:** Development

Which S3 feature allows a Lambda function to be triggered when a new object is created?

- A) S3 Lifecycle policies
- B) S3 Event Notifications
- C) S3 Select
- D) S3 Versioning

---

## Question 61

**Domain:** Development

A developer wants to ensure exactly-once processing of SQS messages in a Lambda function. What should they do?

- A) Set the visibility timeout to infinity
- B) Use a FIFO queue with content-based deduplication
- C) Delete the message after processing and use idempotent processing logic
- D) Use SNS instead of SQS

---

## Question 62

**Domain:** Deployment

A developer wants to test a SAM application locally before deploying. Which command runs the Lambda function locally?

- A) sam validate
- B) sam local invoke
- C) sam local start-api
- D) sam build

---

## Question 63

**Domain:** Development

A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?

- A) SQS + Lambda
- B) SNS + SQS + Lambda
- C) Kinesis + Lambda
- D) API Gateway + Lambda

---

## Question 64

**Domain:** Security

A developer needs to encrypt an S3 bucket with a customer-managed KMS key. Which bucket property should they configure?

- A) Bucket policy
- B) Default encryption with SSE-KMS
- C) CORS configuration
- D) Object lock

---

## Question 65

**Domain:** Development

A developer needs to implement a distributed cache that can be shared across multiple Lambda functions. Which service is BEST?

- A) Amazon S3
- B) Amazon ElastiCache (Redis)
- C) Amazon DynamoDB DAX
- D) Both B and C are valid options

---


---

# Answers & Explanations

---

## Question 1 — Answer: C

**Explanation:** The Choice state evaluates conditions and branches to different states based on the input, similar to an if-else statement.

---

## Question 2 — Answer: B

**Explanation:** For Lambda, simply enabling active tracing in the function configuration provides basic tracing. The X-Ray SDK is needed only for custom subsegments and annotations.

---

## Question 3 — Answer: B

**Explanation:** ECS task roles (taskRoleArn) provide temporary credentials to containers, following the same IAM role pattern as Lambda execution roles.

---

## Question 4 — Answer: B

**Explanation:** Amazon Cognito provides user authentication, sign-up, and sign-in functionality for web and mobile applications, supporting social identity providers and SAML.

---

## Question 5 — Answer: B

**Explanation:** sam build processes the SAM template, builds Lambda functions (installing dependencies), and creates deployment artifacts in the .aws-sam directory.

---

## Question 6 — Answer: B

**Explanation:** 429 Too Many Requests indicates throttling. Configure appropriate rate limits and burst limits, or request a limit increase from AWS.

---

## Question 7 — Answer: C

**Explanation:** GetItem is the most efficient for retrieving a single item by its full primary key (partition + sort key if applicable). It uses minimal RCUs compared to Scan or Query.

---

## Question 8 — Answer: B

**Explanation:** CloudWatch publishes Lambda metrics including Invocations, Duration, Errors, Throttles, and ConcurrentExecutions for monitoring Lambda functions.

---

## Question 9 — Answer: B

**Explanation:** This error means you've exceeded your provisioned throughput. Either switch to on-demand mode (PAY_PER_REQUEST) or increase RCUs/WCUs.

---

## Question 10 — Answer: B

**Explanation:** CloudWatch Logs Insights provides a powerful query language for searching and analyzing log data, including filtering, aggregation, and sorting.

---

## Question 11 — Answer: B

**Explanation:** MFA Delete requires multi-factor authentication to delete objects or disable versioning, providing strong protection against accidental or malicious deletion.

---

## Question 12 — Answer: B

**Explanation:** Lambda functions in a VPC need a NAT Gateway in a public subnet to reach the internet. The function should be placed in a private subnet with a route to the NAT.

---

## Question 13 — Answer: B

**Explanation:** cdk synth (synthesize) generates the CloudFormation template from CDK code without deploying. This is useful for reviewing changes before deployment.

---

## Question 14 — Answer: B

**Explanation:** Metric filters define patterns to match in log events and turn them into CloudWatch numeric metrics, enabling alarms and dashboards based on log data.

---

## Question 15 — Answer: B

**Explanation:** AWS Fargate is a serverless compute engine for containers that works with ECS and EKS, eliminating the need to manage servers or clusters.

---

## Question 16 — Answer: C

**Explanation:** To calculate error rate, use a metric math expression dividing the Errors metric by the Invocations metric, then set the alarm threshold at 0.05 (5%).

---

## Question 17 — Answer: B

**Explanation:** The Transform section tells CloudFormation to use the SAM transform, which converts SAM-specific resource types (like AWS::Serverless::Function) into standard CloudFormation resources.

---

## Question 18 — Answer: B

**Explanation:** Fn::GetAtt returns the value of an attribute from a resource in the template, such as a Lambda function's Arn or an S3 bucket's DomainName.

---

## Question 19 — Answer: B

**Explanation:** GenerateDataKey returns a plaintext data key and an encrypted copy. Use the plaintext key to encrypt data locally (envelope encryption), then store the encrypted key with the data.

---

## Question 20 — Answer: B

**Explanation:** CloudFormation cross-stack references use Outputs with Export Name in one stack and Fn::ImportValue in another to share values between stacks.

---

## Question 21 — Answer: B

**Explanation:** Least privilege means granting only the permissions needed for a specific task. This reduces the blast radius of compromised credentials.

---

## Question 22 — Answer: C

**Explanation:** L3 constructs (also called patterns) provide the highest level of abstraction with pre-configured defaults and best practices, like aws-apigateway.LambdaRestApi.

---

## Question 23 — Answer: B

**Explanation:** The buildspec.yml defines the build phases (install, pre_build, build, post_build), environment variables, and artifacts for CodeBuild.

---

## Question 24 — Answer: C

**Explanation:** Querying by a non-key attribute (status) requires a GSI. The primary table can only be efficiently queried by the partition key and sort key.

---

## Question 25 — Answer: B

**Explanation:** Resource-based policies are attached to resources and define who can access them. Identity-based policies are attached to IAM users, groups, or roles and define what they can access.

---

## Question 26 — Answer: A

**Explanation:** CloudWatch Alarms can monitor DynamoDB capacity metrics (ConsumedReadCapacityUnits, ConsumedWriteCapacityUnits) and trigger notifications via SNS.

---

## Question 27 — Answer: B

**Explanation:** CloudFormation automatically rolls back changes on failure by default. All changes made during the update are reverted to the previous stable state.

---

## Question 28 — Answer: C

**Explanation:** IAM execution roles are the secure way to grant Lambda permissions. Never hardcode credentials or use root accounts. Environment variables for secrets should use Secrets Manager instead.

---

## Question 29 — Answer: A

**Explanation:** sam validate checks the SAM template for syntax and structural errors. It can validate both SAM and CloudFormation templates.

---

## Question 30 — Answer: D

**Explanation:** Lambda Authorizers (formerly Custom Authorizers) use a Lambda function to evaluate the authorization token and return an IAM policy.

---

## Question 31 — Answer: B

**Explanation:** Cognito Identity Pools support both authenticated and unauthenticated (guest) identities, providing temporary AWS credentials for accessing resources.

---

## Question 32 — Answer: B

**Explanation:** CloudTrail records API calls made in your AWS account, including who made the call, when, and what resources were affected.

---

## Question 33 — Answer: B

**Explanation:** API Gateway provides built-in API key management with usage plans for throttling and quotas. This is designed for public APIs where you want to track and control usage.

---

## Question 34 — Answer: C

**Explanation:** The Wait state with callback pattern (.waitForTaskToken) allows Step Functions to pause execution until an external process (like human approval) completes by returning the task token.

---

## Question 35 — Answer: B

**Explanation:** IAM roles provide temporary credentials automatically rotated by AWS. This is the secure best practice — never embed credentials in code or make resources public unnecessarily.

---

## Question 36 — Answer: C

**Explanation:** The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services.

---

## Question 37 — Answer: B

**Explanation:** Secrets Manager supports automatic rotation (configurable schedule), which meets the 30-day rotation requirement. Parameter Store SecureString can encrypt but doesn't provide automatic rotation.

---

## Question 38 — Answer: C

**Explanation:** ElastiCache (Redis) provides sub-millisecond latency for in-memory data operations, making it ideal for session data. DynamoDB provides single-digit millisecond latency.

---

## Question 39 — Answer: B

**Explanation:** SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages (up to 10,000). Successfully processed messages are automatically deleted.

---

## Question 40 — Answer: B

**Explanation:** Canary10Percent5Minutes shifts 10% of traffic to the new version, waits 5 minutes, then shifts the remaining 90%. This is a blue/green deployment strategy for Lambda.

---

## Question 41 — Answer: A

**Explanation:** Annotations are key-value pairs indexed by X-Ray, allowing you to search and filter traces. Metadata is not indexed and cannot be searched.

---

## Question 42 — Answer: B

**Explanation:** AWS SAM is a framework for building serverless applications, providing simplified syntax for Lambda functions, API Gateway, and DynamoDB tables.

---

## Question 43 — Answer: B

**Explanation:** Envelope encryption uses KMS to generate a data key, which is then used to encrypt the actual data locally. This avoids KMS size limits and reduces KMS API calls.

---

## Question 44 — Answer: A

**Explanation:** All at once deploys to all instances simultaneously, making it the fastest but causes temporary downtime during the deployment.

---

## Question 45 — Answer: B

**Explanation:** AssumeRole returns temporary credentials (access key, secret key, session token) that can be used to access AWS resources. It's the standard way to obtain temporary credentials for cross-account or on-premises access.

---

## Question 46 — Answer: B

**Explanation:** A 502 Bad Gateway error from API Gateway with Lambda proxy integration typically means the Lambda function returned an invalid response format. The response must include statusCode, headers, and body as a properly formatted JSON object.

---

## Question 47 — Answer: B

**Explanation:** Using wildcards for both Action and Resource violates least privilege. The policy grants all S3 actions on all buckets, which is overly permissive.

---

## Question 48 — Answer: C

**Explanation:** By default, CloudWatch Logs never expire. You can configure a retention period between 1 day and 10 years, or keep data indefinitely.

---

## Question 49 — Answer: D

**Explanation:** Lambda functions need to be configured in the correct VPC/subnets with appropriate security groups to access VPC resources like RDS. Either missing VPC config or incorrect security groups can cause timeouts.

---

## Question 50 — Answer: C

**Explanation:** Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming.

---

## Question 51 — Answer: B

**Explanation:** SAM templates support CloudFormation parameters, allowing you to pass environment-specific values (like table names, stage names) at deployment time using parameter overrides.

---

## Question 52 — Answer: C

**Explanation:** S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access. Intelligent-Tiering has a monitoring cost.

---

## Question 53 — Answer: D

**Explanation:** Immutable deployment creates a completely new set of instances, ensuring full availability during deployment. It's the safest but slowest and most expensive option.

---

## Question 54 — Answer: B

**Explanation:** AWS Secrets Manager provides automatic credential rotation for databases and other services. Parameter Store can store secrets but doesn't provide automatic rotation.

---

## Question 55 — Answer: B

**Explanation:** DynamoDB Streams captures a time-ordered sequence of item-level changes (insert, update, delete) in a table, enabling event-driven processing.

---

## Question 56 — Answer: C

**Explanation:** AWS X-Ray provides distributed tracing, allowing you to trace requests across multiple services, visualize service maps, and identify performance bottlenecks.

---

## Question 57 — Answer: B

**Explanation:** Provisioned Concurrency pre-initializes Lambda execution environments, eliminating cold starts. Increasing memory can help but doesn't eliminate cold starts entirely.

---

## Question 58 — Answer: C

**Explanation:** The default X-Ray sampling rule traces the first request each second, then 5% of additional requests. This ensures some traces while controlling costs.

---

## Question 59 — Answer: B

**Explanation:** ECS with Fargate eliminates infrastructure management for containers. Fargate provisions and manages the underlying compute resources automatically.

---

## Question 60 — Answer: B

**Explanation:** S3 Event Notifications can trigger Lambda, SNS, or SQS when events like object creation, deletion, or restoration occur in a bucket.

---

## Question 61 — Answer: C

**Explanation:** SQS provides at-least-once delivery. For exactly-once semantics, delete messages after successful processing and design idempotent processing logic that can handle duplicate deliveries safely.

---

## Question 62 — Answer: B

**Explanation:** sam local invoke runs a Lambda function locally using Docker. sam local start-api also works but starts a local API server instead of invoking directly.

---

## Question 63 — Answer: B

**Explanation:** SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently.

---

## Question 64 — Answer: B

**Explanation:** S3 default encryption with SSE-KMS uses a customer-managed CMK. This automatically encrypts all new objects with the specified KMS key.

---

## Question 65 — Answer: D

**Explanation:** Both ElastiCache Redis and DynamoDB DAX can serve as distributed caches. Redis is more general-purpose; DAX is specifically for DynamoDB. Both can be shared across Lambda functions.

---

