#!/usr/bin/env python3
"""Generate practice exams for AWS Developer Certification (DVA-C02)."""

import random
from collections import defaultdict
from pathlib import Path

# Write to repo-root exams/ (not generators/exams)
EXAMS_DIR = Path(__file__).resolve().parent.parent / "exams"

# Domain mix roughly matching DVA-C02 weights (for 65-question exams)
DOMAIN_TARGETS = {
    "Development": 21,  # ~32%
    "Security": 17,  # ~26%
    "Deployment": 16,  # ~24%
    "Monitoring": 11,  # ~18%
}

# ============================================================
# Question Bank - All domains (~150+ unique DVA-C02-style)
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
            "D) Use Kinesis Data Streams to buffer messages before processing",
        ],
        "answer": "B",
        "explanation": "SQS can be configured as an event source for Lambda. Lambda automatically polls the queue and invokes the function with batches of messages. Successfully processed messages are automatically deleted.",
    },
    {
        "id": "q2",
        "domain": "Development",
        "question": "A Lambda function needs to access a DynamoDB table. What is the MOST secure way to grant permissions?",
        "options": [
            "A) Hardcode AWS access keys in the Lambda function code",
            "B) Store access keys in Lambda environment variables",
            "C) Attach an IAM execution role with least-privilege DynamoDB permissions to the Lambda function",
            "D) Use the AWS account root user credentials",
        ],
        "answer": "C",
        "explanation": "IAM execution roles are the secure way to grant Lambda permissions. Never hardcode credentials or use root accounts. Environment variables for secrets should use Secrets Manager instead.",
    },
    {
        "id": "q3",
        "domain": "Development",
        "question": "A developer is building a REST API with API Gateway. The backend Lambda function returns a response, but the client receives a 502 error. What is the MOST likely cause?",
        "options": [
            "A) The API Gateway does not have CORS enabled",
            "B) The Lambda function is not returning a properly formatted proxy response with statusCode, headers, and body",
            "C) The API Gateway is missing request validation",
            "D) The client is sending the wrong Content-Type header",
        ],
        "answer": "B",
        "explanation": "A 502 Bad Gateway error from API Gateway with Lambda proxy integration typically means the Lambda function returned an invalid response format. The response must include statusCode, headers, and body.",
    },
    {
        "id": "q4",
        "domain": "Development",
        "question": "Which DynamoDB operation is MOST efficient for retrieving a single item by its primary key?",
        "options": [
            "A) Scan with a filter expression",
            "B) Query with the partition key",
            "C) GetItem with the full primary key",
            "D) BatchGetItem with a single item",
        ],
        "answer": "C",
        "explanation": "GetItem is the most efficient for retrieving a single item by its full primary key (partition + sort key if applicable). It uses minimal RCUs compared to Scan or Query.",
    },
    {
        "id": "q5",
        "domain": "Development",
        "question": "A developer needs to store user session data with sub-millisecond latency. Which AWS service should be used?",
        "options": [
            "A) Amazon S3",
            "B) Amazon DynamoDB",
            "C) Amazon ElastiCache (Redis)",
            "D) Amazon RDS",
        ],
        "answer": "C",
        "explanation": "ElastiCache (Redis) provides sub-millisecond latency for in-memory data operations, making it ideal for session data. DynamoDB provides single-digit millisecond latency.",
    },
    {
        "id": "q6",
        "domain": "Development",
        "question": "A Lambda function is experiencing cold start latency. Which approach would BEST reduce this?",
        "options": [
            "A) Increase the Lambda memory allocation",
            "B) Use Provisioned Concurrency",
            "C) Add more code to the Lambda function",
            "D) Decrease the timeout setting",
        ],
        "answer": "B",
        "explanation": "Provisioned Concurrency pre-initializes Lambda execution environments, eliminating cold starts. Increasing memory can help but doesn't eliminate cold starts entirely.",
    },
    {
        "id": "q7",
        "domain": "Development",
        "question": "When building a DynamoDB table for an e-commerce application, which access pattern requires a Global Secondary Index (GSI)?",
        "options": [
            "A) Get order by orderId (partition key)",
            "B) Get all orders for a customer sorted by date (composite key)",
            "C) Get all orders with status 'PENDING' regardless of customer",
            "D) Delete an order by orderId",
        ],
        "answer": "C",
        "explanation": "Querying by a non-key attribute (status) requires a GSI. The primary table can only be efficiently queried by the partition key and sort key.",
    },
    {
        "id": "q8",
        "domain": "Development",
        "question": "A developer needs to process a large CSV file uploaded to S3. The file is 5GB. What is the MOST efficient approach?",
        "options": [
            "A) Download the entire file in a Lambda function and process it",
            "B) Use S3 Select to query only the needed data",
            "C) Copy the file to EBS and process it with EC2",
            "D) Use S3 Transfer Acceleration",
        ],
        "answer": "B",
        "explanation": "S3 Select allows you to retrieve only the needed data from a CSV file using SQL expressions, reducing data transfer and processing time significantly.",
    },
    {
        "id": "q9",
        "domain": "Development",
        "question": "A developer wants to ensure exactly-once processing of SQS messages in a Lambda function. What should they do?",
        "options": [
            "A) Set the visibility timeout to infinity",
            "B) Use a FIFO queue with content-based deduplication",
            "C) Delete the message after processing and use idempotent processing logic",
            "D) Use SNS instead of SQS",
        ],
        "answer": "C",
        "explanation": "SQS provides at-least-once delivery. For exactly-once semantics, delete messages after successful processing and design idempotent processing logic that can handle duplicate deliveries safely.",
    },
    {
        "id": "q10",
        "domain": "Development",
        "question": "Which S3 storage class is MOST cost-effective for data that is accessed once a quarter?",
        "options": [
            "A) S3 Standard",
            "B) S3 Intelligent-Tiering",
            "C) S3 Standard-IA (Infrequent Access)",
            "D) S3 Glacier Deep Archive",
        ],
        "answer": "C",
        "explanation": "S3 Standard-IA is designed for data accessed less frequently but requires rapid access when needed (quarterly access). Glacier Deep Archive is for annual access.",
    },
    {
        "id": "q11",
        "domain": "Development",
        "question": "A developer needs to implement a fanout pattern where one event triggers multiple downstream services. Which combination of services is BEST?",
        "options": [
            "A) SQS + Lambda",
            "B) SNS + SQS + Lambda",
            "C) Kinesis + Lambda",
            "D) API Gateway + Lambda",
        ],
        "answer": "B",
        "explanation": "SNS + SQS + Lambda enables the fanout pattern: publish to SNS topic, which fans out to multiple SQS queues (one per service), and Lambda processes each queue independently.",
    },
    {
        "id": "q12",
        "domain": "Development",
        "question": "What is the maximum execution timeout for an AWS Lambda function?",
        "options": [
            "A) 30 seconds",
            "B) 5 minutes",
            "C) 15 minutes",
            "D) 1 hour",
        ],
        "answer": "C",
        "explanation": "The maximum Lambda function timeout is 15 minutes (900 seconds). For longer-running tasks, use Step Functions, ECS, or other compute services.",
    },
    {
        "id": "q13",
        "domain": "Development",
        "question": "A developer needs to implement real-time streaming data processing with ordering guarantees. Which service should they use?",
        "options": [
            "A) Amazon SQS Standard queue",
            "B) Amazon SNS",
            "C) Amazon Kinesis Data Streams",
            "D) Amazon MQ",
        ],
        "answer": "C",
        "explanation": "Kinesis Data Streams provides ordering of records within shards, enabling real-time processing with ordering guarantees. SQS FIFO also provides ordering but is not designed for streaming.",
    },
    {
        "id": "q14",
        "domain": "Development",
        "question": "A Step Functions workflow needs to wait for human approval before proceeding. Which state type should be used?",
        "options": [
            "A) Task state",
            "B) Choice state",
            "C) Wait state with a callback pattern",
            "D) Succeed state",
        ],
        "answer": "C",
        "explanation": "The Wait state with callback pattern (.waitForTaskToken) allows Step Functions to pause execution until an external process (like human approval) completes by returning the task token.",
    },
    {
        "id": "q15",
        "domain": "Development",
        "question": "Which ECS launch type eliminates the need to manage underlying server infrastructure?",
        "options": [
            "A) EC2 launch type",
            "B) Fargate launch type",
            "C) External launch type",
            "D) Lambda launch type",
        ],
        "answer": "B",
        "explanation": "AWS Fargate is a serverless compute engine for containers that works with ECS and EKS, eliminating the need to manage servers or clusters.",
    },
    {
        "id": "q61",
        "domain": "Development",
        "question": "What is the maximum payload size for an SQS message?",
        "options": [
            "A) 64 KB",
            "B) 128 KB",
            "C) 256 KB",
            "D) 1 MB",
        ],
        "answer": "C",
        "explanation": "SQS messages have a maximum size of 256 KB. For larger messages, use S3 to store the payload and pass a reference via SQS.",
    },
    {
        "id": "q62",
        "domain": "Development",
        "question": "Which DynamoDB feature captures item-level modifications in a table?",
        "options": [
            "A) Global Secondary Index",
            "B) DynamoDB Streams",
            "C) Time-to-Live (TTL)",
            "D) Point-in-Time Recovery",
        ],
        "answer": "B",
        "explanation": "DynamoDB Streams captures a time-ordered sequence of item-level changes (insert, update, delete) in a table, enabling event-driven processing.",
    },
    {
        "id": "q63",
        "domain": "Development",
        "question": "A developer needs to implement a state machine that branches based on output from a Lambda function. Which Step Functions state type should be used?",
        "options": [
            "A) Task",
            "B) Pass",
            "C) Choice",
            "D) Wait",
        ],
        "answer": "C",
        "explanation": "The Choice state evaluates conditions and branches to different states based on the input, similar to an if-else statement.",
    },
    {
        "id": "q66",
        "domain": "Development",
        "question": "A developer needs to implement a distributed cache that can be shared across multiple Lambda functions. Which service is BEST?",
        "options": [
            "A) Amazon S3",
            "B) Amazon ElastiCache (Redis)",
            "C) Amazon DynamoDB DAX",
            "D) Both B and C are valid options",
        ],
        "answer": "D",
        "explanation": "Both ElastiCache Redis and DynamoDB DAX can serve as distributed caches. Redis is more general-purpose; DAX is specifically for DynamoDB.",
    },
    {
        "id": "q69",
        "domain": "Development",
        "question": "Which S3 feature allows a Lambda function to be triggered when a new object is created?",
        "options": [
            "A) S3 Lifecycle policies",
            "B) S3 Event Notifications",
            "C) S3 Select",
            "D) S3 Versioning",
        ],
        "answer": "B",
        "explanation": "S3 Event Notifications can trigger Lambda, SNS, or SQS when events like object creation, deletion, or restoration occur in a bucket.",
    },
    {
        "id": "q71",
        "domain": "Development",
        "question": "A Lambda function must share initialization cost across many invocations. Where should expensive SDK clients be created?",
        "options": [
            "A) Inside the handler on every invocation",
            "B) Outside the handler (global/module scope) so warm containers reuse them",
            "C) In a separate Lambda Layer that runs at invoke time",
            "D) In the API Gateway request mapping template",
        ],
        "answer": "B",
        "explanation": "Code outside the handler runs during cold start and is reused for warm invocations. Initialize clients once at module scope for better performance.",
    },
    {
        "id": "q72",
        "domain": "Development",
        "question": "Which DynamoDB operation should be avoided for large tables when filtering by a non-key attribute without an index?",
        "options": [
            "A) GetItem",
            "B) Query",
            "C) Scan",
            "D) BatchWriteItem",
        ],
        "answer": "C",
        "explanation": "Scan reads every item and is inefficient/expensive on large tables. Prefer Query with a proper key design or GSI for non-key access patterns.",
    },
    {
        "id": "q73",
        "domain": "Development",
        "question": "An application needs strongly consistent reads from DynamoDB. What must the developer do?",
        "options": [
            "A) Enable DynamoDB Streams",
            "B) Set ConsistentRead=True on GetItem or Query (not available on GSIs)",
            "C) Use only Scan operations",
            "D) Switch the table to eventual consistency mode",
        ],
        "answer": "B",
        "explanation": "Strongly consistent reads are requested via ConsistentRead=True on GetItem/Query against the base table. GSIs support only eventually consistent reads.",
    },
    {
        "id": "q74",
        "domain": "Development",
        "question": "A developer needs temporary access for a client to upload a file directly to S3. What is the BEST approach?",
        "options": [
            "A) Make the bucket public with PutObject allowed",
            "B) Generate a pre-signed URL with PutObject permission and a short expiry",
            "C) Embed IAM user credentials in the mobile app",
            "D) Use CloudFront signed cookies for uploads only",
        ],
        "answer": "B",
        "explanation": "Pre-signed URLs grant time-limited permission to perform a specific S3 action without exposing long-lived credentials or opening the bucket publicly.",
    },
    {
        "id": "q75",
        "domain": "Development",
        "question": "When should a developer choose an SQS FIFO queue over a Standard queue?",
        "options": [
            "A) When maximum throughput is the only priority",
            "B) When message order and exactly-once processing within a message group are required",
            "C) When messages must be larger than 256 KB",
            "D) When messages must be retained for more than 14 days",
        ],
        "answer": "B",
        "explanation": "FIFO queues provide ordering and exactly-once processing within a message group ID. Standard queues prioritize higher throughput with at-least-once delivery.",
    },
    {
        "id": "q76",
        "domain": "Development",
        "question": "What is the purpose of an SQS dead-letter queue (DLQ)?",
        "options": [
            "A) To store messages permanently for archival",
            "B) To receive messages that fail processing after a configured maximum receive count",
            "C) To replace the visibility timeout mechanism",
            "D) To fan out messages to multiple consumers",
        ],
        "answer": "B",
        "explanation": "A DLQ captures messages that repeatedly fail processing (after maxReceiveCount), enabling inspection, alerting, and reprocessing without blocking the main queue.",
    },
    {
        "id": "q77",
        "domain": "Development",
        "question": "A developer wants EventBridge to route only OrderCreated events with amount > 1000 to a Lambda target. What should they configure?",
        "options": [
            "A) An SNS filter policy on the Lambda subscription",
            "B) An EventBridge rule with an event pattern matching source/detail-type and a content filter on amount",
            "C) An SQS visibility timeout of 1000 seconds",
            "D) API Gateway request validation only",
        ],
        "answer": "B",
        "explanation": "EventBridge rules use event patterns (and content filtering) to match specific events and fields before invoking targets like Lambda.",
    },
    {
        "id": "q78",
        "domain": "Development",
        "question": "Which API Gateway integration type passes the entire request/response to/from Lambda without mapping templates?",
        "options": [
            "A) AWS integration",
            "B) HTTP integration",
            "C) Lambda proxy (AWS_PROXY) integration",
            "D) MOCK integration",
        ],
        "answer": "C",
        "explanation": "Lambda proxy integration forwards the full request to Lambda and expects a structured response (statusCode, headers, body), simplifying API wiring.",
    },
    {
        "id": "q79",
        "domain": "Development",
        "question": "A Kinesis Data Streams consumer must process records in order per shard and checkpoint progress. Which approach is MOST appropriate with Lambda?",
        "options": [
            "A) Use SQS Standard as the event source instead",
            "B) Configure Kinesis as a Lambda event source; Lambda manages shard iterators and checkpoints via event source mapping",
            "C) Poll Kinesis from EC2 without checkpoints",
            "D) Publish each record to SNS for unordered fan-out",
        ],
        "answer": "B",
        "explanation": "Lambda event source mappings for Kinesis poll shards, invoke with batches, and checkpoint on success, preserving per-shard order.",
    },
    {
        "id": "q80",
        "domain": "Development",
        "question": "What does DynamoDB TTL (Time to Live) do?",
        "options": [
            "A) Automatically encrypts items after a timestamp",
            "B) Deletes expired items near a Unix epoch attribute without consuming write capacity for the delete in the usual way",
            "C) Creates a GSI for time-based queries",
            "D) Extends item retention beyond 365 days",
        ],
        "answer": "B",
        "explanation": "TTL marks items for expiration based on a numeric epoch attribute; DynamoDB deletes them asynchronously. Ideal for sessions and temporary data.",
    },
    {
        "id": "q81",
        "domain": "Development",
        "question": "A developer needs optimistic concurrency control when updating a DynamoDB item. Which feature should they use?",
        "options": [
            "A) DynamoDB Streams",
            "B) Conditional expressions (e.g., attribute_exists / version attribute checks)",
            "C) Scan with ConsistentRead",
            "D) On-demand capacity mode",
        ],
        "answer": "B",
        "explanation": "Conditional writes (ConditionExpression) implement optimistic locking by failing updates when expected attribute values (like a version) do not match.",
    },
    {
        "id": "q82",
        "domain": "Development",
        "question": "Which Elasticache engine feature is commonly used for atomic counters and distributed locks?",
        "options": [
            "A) Redis INCR / SET with NX and expiry",
            "B) Memcached flush_all only",
            "C) DynamoDB PutItem",
            "D) S3 object lock",
        ],
        "answer": "A",
        "explanation": "Redis supports atomic operations such as INCR and SET NX EX, which are commonly used for counters and simple distributed locks.",
    },
    {
        "id": "q83",
        "domain": "Development",
        "question": "A Step Functions Map state is used to process a list of items. What does it do?",
        "options": [
            "A) Waits for human approval",
            "B) Runs a set of steps for each item in an array, optionally in parallel with MaxConcurrency",
            "C) Replaces Choice states entirely",
            "D) Only works with Express workflows",
        ],
        "answer": "B",
        "explanation": "Map iterates over an array and runs a processor state machine for each element, with optional concurrency limits for fan-out processing.",
    },
    {
        "id": "q84",
        "domain": "Development",
        "question": "What is the maximum size of a Lambda deployment package (unzipped, including layers) for a zip upload?",
        "options": [
            "A) 50 MB",
            "B) 250 MB",
            "C) 10 GB",
            "D) 5 MB",
        ],
        "answer": "B",
        "explanation": "The unzipped deployment package size limit (including layers) is 250 MB. Container images support larger packages up to 10 GB.",
    },
    {
        "id": "q85",
        "domain": "Development",
        "question": "An SNS topic must deliver only messages with attribute orderType=express to a subscribed SQS queue. What should be configured?",
        "options": [
            "A) SQS redrive policy",
            "B) SNS subscription filter policy matching orderType=express",
            "C) Kinesis shard key",
            "D) API Gateway usage plan",
        ],
        "answer": "B",
        "explanation": "SNS filter policies on subscriptions deliver only messages whose attributes (or payload attributes) match the filter criteria.",
    },
    {
        "id": "q86",
        "domain": "Development",
        "question": "A developer needs to query DynamoDB items by email address, but the table's partition key is userId. What is the BEST solution?",
        "options": [
            "A) Scan the table filtering on email",
            "B) Create a GSI with email as the partition key",
            "C) Export the table to S3 and query with Athena for every request",
            "D) Store emails only in ElastiCache",
        ],
        "answer": "B",
        "explanation": "A GSI with email as partition key enables efficient Query access by email without expensive Scans.",
    },
    {
        "id": "q87",
        "domain": "Development",
        "question": "Which AWS SDK best practice helps applications recover from transient DynamoDB throttling?",
        "options": [
            "A) Disable retries and fail immediately",
            "B) Use exponential backoff with jitter (SDK default retries)",
            "C) Always Switch to Scan",
            "D) Hardcode higher timeouts only",
        ],
        "answer": "B",
        "explanation": "AWS SDKs retry throttling errors with exponential backoff. Applications should also consider on-demand capacity or capacity adjustments for sustained load.",
    },
    {
        "id": "q88",
        "domain": "Development",
        "question": "API Gateway WebSocket APIs are MOST appropriate when the application needs:",
        "options": [
            "A) Only synchronous request/response over HTTP",
            "B) Persistent bidirectional connections for real-time push to clients",
            "C) File uploads larger than 10 GB",
            "D) Batch ETL from S3",
        ],
        "answer": "B",
        "explanation": "WebSocket APIs maintain persistent connections and allow the server to push messages to connected clients for chat, notifications, and similar use cases.",
    },
    {
        "id": "q89",
        "domain": "Development",
        "question": "A Lambda function processes an SQS batch. One message fails. How can the developer avoid reprocessing successful messages?",
        "options": [
            "A) Disable the event source mapping",
            "B) Report failures with ReportBatchItemFailures (partial batch response) so only failed message IDs are retried",
            "C) Increase memory to 10 GB",
            "D) Switch to SNS",
        ],
        "answer": "B",
        "explanation": "Partial batch responses let Lambda tell SQS which message IDs failed; only those become visible again. Successful messages are deleted.",
    },
    {
        "id": "q90",
        "domain": "Development",
        "question": "What is the primary benefit of DynamoDB DAX?",
        "options": [
            "A) Multi-region active-active writes",
            "B) Microsecond in-memory caching for DynamoDB read-heavy workloads",
            "C) Automatic schema migrations",
            "D) Replacing GSIs entirely",
        ],
        "answer": "B",
        "explanation": "DAX is a write-through cache for DynamoDB that can reduce read latency to microseconds for cache hits.",
    },
    {
        "id": "q91",
        "domain": "Development",
        "question": "A developer stores large objects in S3 and metadata in DynamoDB. What is a common pattern for referencing the object?",
        "options": [
            "A) Store the entire object bytes in DynamoDB",
            "B) Store the S3 bucket/key (or URL) in DynamoDB and fetch the object from S3 when needed",
            "C) Use only EBS volumes",
            "D) Embed Base64 objects in SQS messages",
        ],
        "answer": "B",
        "explanation": "The claim-check / metadata pattern stores pointers in DynamoDB and large payloads in S3, staying within DynamoDB item size limits (400 KB).",
    },
    {
        "id": "q92",
        "domain": "Development",
        "question": "Which Lambda concurrency control reserves capacity for a critical function so other functions cannot consume the account limit?",
        "options": [
            "A) Reserved concurrency",
            "B) Provisioned concurrency only",
            "C) Asynchronous invocation",
            "D) Dead-letter queues",
        ],
        "answer": "A",
        "explanation": "Reserved concurrency guarantees a maximum concurrent execution limit for a function and reserves that capacity from the account pool.",
    },
    {
        "id": "q93",
        "domain": "Development",
        "question": "An application must publish events to multiple subscriber types (email, SQS, Lambda) from one producer. Which service is BEST as the fan-out hub?",
        "options": [
            "A) Amazon SNS",
            "B) Amazon SQS alone",
            "C) Amazon S3",
            "D) Amazon ECR",
        ],
        "answer": "A",
        "explanation": "SNS is a pub/sub hub that can deliver to SQS, Lambda, HTTP, email, and other protocols from a single publish.",
    },
    {
        "id": "q94",
        "domain": "Development",
        "question": "What is the maximum item size in DynamoDB?",
        "options": [
            "A) 64 KB",
            "B) 256 KB",
            "C) 400 KB",
            "D) 1 MB",
        ],
        "answer": "C",
        "explanation": "DynamoDB items are limited to 400 KB. Larger payloads should be stored in S3 with a reference in DynamoDB.",
    },
    {
        "id": "q95",
        "domain": "Development",
        "question": "A developer needs to run a long-running workflow with retries, branching, and parallel steps coordinating multiple Lambda functions. Which service fits BEST?",
        "options": [
            "A) A single Lambda with a 15-minute sleep loop",
            "B) AWS Step Functions",
            "C) Amazon SNS only",
            "D) Amazon CloudFront",
        ],
        "answer": "B",
        "explanation": "Step Functions orchestrates multi-step workflows with retries, catchers, Choice, Parallel, and Map states across AWS services.",
    },
    {
        "id": "q96",
        "domain": "Development",
        "question": "When using the AWS SDK, which credential source is preferred for applications running on EC2?",
        "options": [
            "A) Hardcoded access keys in source control",
            "B) Instance profile (IAM role attached to the instance)",
            "C) Root user access keys",
            "D) Credentials emailed to developers",
        ],
        "answer": "B",
        "explanation": "EC2 instance profiles provide temporary credentials via the instance metadata service; the SDK retrieves them automatically.",
    },
    {
        "id": "q97",
        "domain": "Development",
        "question": "API Gateway stage variables are commonly used to:",
        "options": [
            "A) Encrypt Lambda environment variables",
            "B) Parameterize backend endpoints or Lambda aliases per stage (dev/test/prod)",
            "C) Replace IAM policies",
            "D) Increase Lambda memory at runtime",
        ],
        "answer": "B",
        "explanation": "Stage variables let you configure stage-specific values such as Lambda alias ARNs or HTTP endpoints without changing the API definition for each environment.",
    },
    {
        "id": "q98",
        "domain": "Development",
        "question": "A Local Secondary Index (LSI) differs from a GSI because an LSI:",
        "options": [
            "A) Can have a different partition key from the base table",
            "B) Must share the same partition key as the base table and can only be created at table creation",
            "C) Supports only eventually consistent reads",
            "D) Cannot include a sort key",
        ],
        "answer": "B",
        "explanation": "LSIs share the base table partition key, provide an alternate sort key, and must be defined when the table is created. GSIs can use different partition keys.",
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
            "D) Use bucket policies that allow anonymous access",
        ],
        "answer": "B",
        "explanation": "IAM roles provide temporary credentials automatically rotated by AWS. This is the secure best practice — never embed credentials in code or make resources public unnecessarily.",
    },
    {
        "id": "q17",
        "domain": "Security",
        "question": "A company wants to implement user authentication for a web application without managing passwords. Which service should they use?",
        "options": [
            "A) AWS IAM",
            "B) Amazon Cognito",
            "C) AWS Secrets Manager",
            "D) AWS WAF",
        ],
        "answer": "B",
        "explanation": "Amazon Cognito provides user authentication, sign-up, and sign-in functionality for web and mobile applications, supporting social identity providers and SAML.",
    },
    {
        "id": "q18",
        "domain": "Security",
        "question": "A developer needs to encrypt data larger than 4KB using KMS. What is the recommended approach?",
        "options": [
            "A) Call KMS Encrypt repeatedly for each 4KB chunk",
            "B) Use envelope encryption with GenerateDataKey",
            "C) Use KMS with a larger key size",
            "D) Compress the data to under 4KB",
        ],
        "answer": "B",
        "explanation": "Envelope encryption uses KMS to generate a data key, which is then used to encrypt the actual data locally. This avoids KMS size limits and reduces KMS API calls.",
    },
    {
        "id": "q19",
        "domain": "Security",
        "question": "Which AWS service provides automatic rotation of database credentials?",
        "options": [
            "A) AWS Systems Manager Parameter Store",
            "B) AWS Secrets Manager",
            "C) AWS KMS",
            "D) AWS IAM",
        ],
        "answer": "B",
        "explanation": "AWS Secrets Manager provides automatic credential rotation for databases and other services. Parameter Store can store secrets but doesn't provide automatic rotation.",
    },
    {
        "id": "q20",
        "domain": "Security",
        "question": "A developer needs to securely store a database connection string for a Lambda function. The string needs to be rotated every 30 days. Which solution is BEST?",
        "options": [
            "A) Store it in a Lambda environment variable",
            "B) Store it in AWS Secrets Manager with automatic rotation",
            "C) Store it in S3 with server-side encryption",
            "D) Store it in AWS Systems Manager Parameter Store as a String type",
        ],
        "answer": "B",
        "explanation": "Secrets Manager supports automatic rotation (configurable schedule), which meets the 30-day rotation requirement. Parameter Store SecureString can encrypt but doesn't provide automatic rotation.",
    },
    {
        "id": "q21",
        "domain": "Security",
        "question": "What is the principle of least privilege in AWS IAM?",
        "options": [
            "A) Granting all permissions to all users",
            "B) Granting only the minimum permissions needed to perform a task",
            "C) Using only managed policies",
            "D) Denying all access by default and using IAM roles only",
        ],
        "answer": "B",
        "explanation": "Least privilege means granting only the permissions needed for a specific task. This reduces the blast radius of compromised credentials.",
    },
    {
        "id": "q22",
        "domain": "Security",
        "question": "An application running on ECS needs to access DynamoDB. How should the developer configure permissions?",
        "options": [
            "A) Store access keys in the container image",
            "B) Use an IAM task role for the ECS task definition",
            "C) Use EC2 instance profiles",
            "D) Create a separate IAM user for each container",
        ],
        "answer": "B",
        "explanation": "ECS task roles (taskRoleArn) provide temporary credentials to containers, following the same IAM role pattern as Lambda execution roles.",
    },
    {
        "id": "q23",
        "domain": "Security",
        "question": "A developer wants to add a web-based login page to their application using Cognito. Which Cognito feature provides hosted UI authentication?",
        "options": [
            "A) Cognito Identity Pools",
            "B) Cognito User Pool hosted UI (App Integration)",
            "C) Cognito Sync",
            "D) Cognito user migration Lambda trigger",
        ],
        "answer": "B",
        "explanation": "Cognito User Pools provide a hosted UI for authentication that can be customized, supporting social providers and SAML, without building your own login page.",
    },
    {
        "id": "q24",
        "domain": "Security",
        "question": "Which KMS operation should be used to encrypt data that is larger than 4KB?",
        "options": [
            "A) kms:Encrypt",
            "B) kms:GenerateDataKey",
            "C) kms:GenerateRandom",
            "D) kms:ReEncrypt",
        ],
        "answer": "B",
        "explanation": "GenerateDataKey returns a plaintext data key and an encrypted copy. Use the plaintext key to encrypt data locally (envelope encryption), then store the encrypted key with the data.",
    },
    {
        "id": "q25",
        "domain": "Security",
        "question": "A developer is reviewing an IAM policy and finds: 'Action': 's3:*', 'Resource': '*'. What security concern does this raise?",
        "options": [
            "A) The policy syntax is invalid",
            "B) The policy violates least privilege — it grants full S3 access to all buckets",
            "C) The policy uses a deprecated format",
            "D) The policy cannot be attached to a role",
        ],
        "answer": "B",
        "explanation": "Using wildcards for both Action and Resource violates least privilege. The policy grants all S3 actions on all buckets, which is overly permissive.",
    },
    {
        "id": "q26",
        "domain": "Security",
        "question": "A developer needs to implement API key-based authentication for a public API. Which approach should they use?",
        "options": [
            "A) IAM authentication on API Gateway",
            "B) API Gateway with API keys and usage plans",
            "C) Cognito User Pools",
            "D) Lambda authorizer that validates API keys",
        ],
        "answer": "B",
        "explanation": "API Gateway provides built-in API key management with usage plans for throttling and quotas. This is designed for public APIs where you want to track and control usage.",
    },
    {
        "id": "q27",
        "domain": "Security",
        "question": "A developer wants to use temporary credentials to access AWS resources from an on-premises application. Which STS API should they call?",
        "options": [
            "A) GetSessionToken",
            "B) AssumeRole",
            "C) GetFederationToken",
            "D) DecodeAuthorizationMessage",
        ],
        "answer": "B",
        "explanation": "AssumeRole returns temporary credentials (access key, secret key, session token) that can be used to access AWS resources. It's the standard way to obtain temporary credentials for cross-account or on-premises access.",
    },
    {
        "id": "q28",
        "domain": "Security",
        "question": "Which feature of S3 prevents accidental deletion of objects?",
        "options": [
            "A) Server-side encryption",
            "B) Versioning with MFA Delete",
            "C) CORS configuration",
            "D) Transfer Acceleration",
        ],
        "answer": "B",
        "explanation": "MFA Delete requires multi-factor authentication to delete objects or disable versioning, providing strong protection against accidental or malicious deletion.",
    },
    {
        "id": "q29",
        "domain": "Security",
        "question": "What is the difference between a resource-based policy and an identity-based policy in AWS?",
        "options": [
            "A) They are the same thing",
            "B) Resource-based policies are attached to resources (like S3 buckets), identity-based policies are attached to IAM principals",
            "C) Resource-based policies are only for S3",
            "D) Identity-based policies are more restrictive",
        ],
        "answer": "B",
        "explanation": "Resource-based policies are attached to resources and define who can access them. Identity-based policies are attached to IAM users, groups, or roles and define what they can access.",
    },
    {
        "id": "q30",
        "domain": "Security",
        "question": "A developer needs to encrypt an S3 bucket with a customer-managed KMS key. Which bucket property should they configure?",
        "options": [
            "A) Bucket policy",
            "B) Default encryption with SSE-KMS",
            "C) CORS configuration",
            "D) Object lock",
        ],
        "answer": "B",
        "explanation": "S3 default encryption with SSE-KMS uses a customer-managed CMK. This automatically encrypts all new objects with the specified KMS key.",
    },
    {
        "id": "q64",
        "domain": "Security",
        "question": "Which API Gateway authorization type uses a Lambda function to validate tokens?",
        "options": [
            "A) NONE",
            "B) AWS_IAM",
            "C) COGNITO_USER_POOLS",
            "D) CUSTOM (Lambda Authorizer)",
        ],
        "answer": "D",
        "explanation": "Lambda Authorizers (formerly Custom Authorizers) use a Lambda function to evaluate the authorization token and return an IAM policy.",
    },
    {
        "id": "q70",
        "domain": "Security",
        "question": "A developer wants to use Cognito to allow unauthenticated guest access to AWS resources. Which Cognito feature supports this?",
        "options": [
            "A) Cognito User Pools",
            "B) Cognito Identity Pools (Federated Identities)",
            "C) Cognito Sync",
            "D) Cognito user groups",
        ],
        "answer": "B",
        "explanation": "Cognito Identity Pools support both authenticated and unauthenticated (guest) identities, providing temporary AWS credentials for accessing resources.",
    },
    {
        "id": "q99",
        "domain": "Security",
        "question": "Which condition key restricts an IAM policy so that requests must come from a specific VPC endpoint?",
        "options": [
            "A) aws:SourceIp",
            "B) aws:SourceVpce",
            "C) aws:RequestedRegion",
            "D) aws:MultiFactorAuthPresent",
        ],
        "answer": "B",
        "explanation": "aws:SourceVpce (and related VPC endpoint condition keys) can require that API calls originate from a specified VPC endpoint.",
    },
    {
        "id": "q100",
        "domain": "Security",
        "question": "A Lambda environment variable contains a secret. What is the BEST practice?",
        "options": [
            "A) Leave it as plaintext for simplicity",
            "B) Store the secret in Secrets Manager or SSM SecureString and retrieve it at runtime (optionally cache)",
            "C) Commit the secret to Git for team access",
            "D) Put the secret in the function name",
        ],
        "answer": "B",
        "explanation": "Prefer Secrets Manager or SSM Parameter Store (SecureString) over plaintext environment variables for secrets, with IAM-controlled access and optional rotation.",
    },
    {
        "id": "q101",
        "domain": "Security",
        "question": "What does SSE-S3 encryption use for S3 object encryption?",
        "options": [
            "A) Customer-provided keys only (SSE-C)",
            "B) S3-managed encryption keys",
            "C) CloudHSM exclusively",
            "D) Client-side encryption only",
        ],
        "answer": "B",
        "explanation": "SSE-S3 uses encryption keys managed by Amazon S3. SSE-KMS uses KMS keys; SSE-C uses customer-provided keys.",
    },
    {
        "id": "q102",
        "domain": "Security",
        "question": "An IAM policy includes Effect: Deny for s3:DeleteObject. A separate Allow grants s3:*. What is the result for DeleteObject?",
        "options": [
            "A) Allow always wins",
            "B) Explicit Deny overrides Allow — DeleteObject is denied",
            "C) The policies cancel and access is undefined",
            "D) Only resource-based policies apply",
        ],
        "answer": "B",
        "explanation": "In IAM evaluation, an explicit Deny always overrides Allow, regardless of other Allow statements.",
    },
    {
        "id": "q103",
        "domain": "Security",
        "question": "Which Cognito component issues JWT tokens (ID, access, refresh) after user sign-in?",
        "options": [
            "A) Cognito User Pools",
            "B) Cognito Identity Pools only",
            "C) AWS KMS",
            "D) AWS WAF",
        ],
        "answer": "A",
        "explanation": "User Pools authenticate users and issue JWTs. Identity Pools exchange identity for temporary AWS credentials.",
    },
    {
        "id": "q104",
        "domain": "Security",
        "question": "A cross-account S3 access scenario requires Account B to read objects in Account A's bucket. Which combination is commonly required?",
        "options": [
            "A) Only an IAM user in Account B with no bucket policy",
            "B) Bucket policy in Account A allowing Account B's principal, plus permissions in Account B",
            "C) Making the bucket public",
            "D) Disabling encryption",
        ],
        "answer": "B",
        "explanation": "Cross-account S3 access typically needs a resource-based bucket policy granting the external principal and identity-based permissions in the caller's account.",
    },
    {
        "id": "q105",
        "domain": "Security",
        "question": "What is the purpose of an IAM permissions boundary?",
        "options": [
            "A) To replace SCPs in Organizations",
            "B) To set the maximum permissions an IAM identity can be granted, even if policies allow more",
            "C) To encrypt IAM credentials",
            "D) To enable MFA devices",
        ],
        "answer": "B",
        "explanation": "Permissions boundaries define the maximum permissions an identity can have; effective permissions are the intersection of identity policies and the boundary.",
    },
    {
        "id": "q106",
        "domain": "Security",
        "question": "Which Parameter Store parameter type stores encrypted values using KMS?",
        "options": [
            "A) String",
            "B) StringList",
            "C) SecureString",
            "D) HashString",
        ],
        "answer": "C",
        "explanation": "SecureString parameters are encrypted with AWS KMS. String and StringList store plaintext values.",
    },
    {
        "id": "q107",
        "domain": "Security",
        "question": "A developer encrypts Lambda environment variables with a customer-managed KMS key. What additional permission does the Lambda execution role need?",
        "options": [
            "A) kms:CreateKey",
            "B) kms:Decrypt on that CMK",
            "C) iam:PassRole on the KMS key",
            "D) s3:GetObject on all buckets",
        ],
        "answer": "B",
        "explanation": "When environment variables are encrypted with a CMK, the execution role needs kms:Decrypt (and the key policy must allow the role) to decrypt them at runtime.",
    },
    {
        "id": "q108",
        "domain": "Security",
        "question": "API Gateway Cognito User Pool authorizers validate which token by default for REST APIs?",
        "options": [
            "A) Refresh token only",
            "B) ID token (JWT) from the Cognito User Pool",
            "C) AWS access key ID",
            "D) SAML assertion only",
        ],
        "answer": "B",
        "explanation": "Cognito authorizers validate JWTs (typically the ID token) issued by the configured User Pool before allowing the request.",
    },
    {
        "id": "q109",
        "domain": "Security",
        "question": "Which S3 feature can enforce that all uploads use encryption?",
        "options": [
            "A) A bucket policy denying PutObject unless s3:x-amz-server-side-encryption is present",
            "B) CORS only",
            "C) Transfer Acceleration",
            "D) Requester Pays",
        ],
        "answer": "A",
        "explanation": "Bucket policies can deny unencrypted uploads by requiring the encryption header or using default encryption plus Deny for incorrect encryption.",
    },
    {
        "id": "q110",
        "domain": "Security",
        "question": "What does STS GetCallerIdentity return?",
        "options": [
            "A) A new access key pair",
            "B) The Account, UserId, and Arn of the credentials making the call",
            "C) A Cognito JWT",
            "D) A CloudTrail digest",
        ],
        "answer": "B",
        "explanation": "GetCallerIdentity is commonly used to verify which principal the current credentials represent (account, user ID, ARN).",
    },
    {
        "id": "q111",
        "domain": "Security",
        "question": "A mobile app needs temporary AWS credentials after Cognito User Pool login. What should be configured?",
        "options": [
            "A) Only IAM users with long-lived keys in the app",
            "B) Cognito Identity Pool federated with the User Pool to obtain temporary credentials",
            "C) Root account keys",
            "D) CloudFront key pairs only",
        ],
        "answer": "B",
        "explanation": "Identity Pools exchange authenticated User Pool identities (or other IdPs) for temporary AWS credentials via STS.",
    },
    {
        "id": "q112",
        "domain": "Security",
        "question": "Which KMS key policy statement is required for a CMK to be usable by IAM principals in the account?",
        "options": [
            "A) No key policy is needed; IAM alone is always sufficient",
            "B) The key policy must allow the account/root (or specific principals); IAM permissions then further control access",
            "C) Only CloudTrail can use CMKs",
            "D) Key policies only apply to AWS managed keys",
        ],
        "answer": "B",
        "explanation": "KMS requires both key policy and IAM permissions. The key policy is foundational; without it granting the account, IAM alone cannot authorize use.",
    },
    {
        "id": "q113",
        "domain": "Security",
        "question": "What is the safest way to allow a third-party SaaS to write logs into your S3 bucket?",
        "options": [
            "A) Share root credentials",
            "B) Use a bucket policy with a dedicated IAM role/external ID (or assume-role) and least-privilege PutObject on a prefix",
            "C) Make the bucket fully public",
            "D) Disable all encryption",
        ],
        "answer": "B",
        "explanation": "Cross-account least-privilege access via role assumption (often with ExternalId) or tightly scoped bucket policies is the secure pattern for partner writes.",
    },
    {
        "id": "q114",
        "domain": "Security",
        "question": "Which header or mechanism helps protect against confused deputy attacks when using AssumeRole with third parties?",
        "options": [
            "A) External ID in the trust policy Condition",
            "B) Larger session duration",
            "C) Disabling MFA",
            "D) Using * for Principal",
        ],
        "answer": "A",
        "explanation": "ExternalId in the role trust policy Condition helps ensure only the intended third party can assume the role (confused deputy protection).",
    },
    {
        "id": "q115",
        "domain": "Security",
        "question": "SSM Parameter Store hierarchical paths (e.g., /myapp/prod/db) are useful primarily to:",
        "options": [
            "A) Automatically rotate passwords",
            "B) Organize parameters and apply IAM path-based access control with GetParametersByPath",
            "C) Replace KMS entirely",
            "D) Create VPC endpoints",
        ],
        "answer": "B",
        "explanation": "Paths organize configuration and allow IAM policies to grant access to parameter hierarchies via path prefixes and GetParametersByPath.",
    },
    {
        "id": "q116",
        "domain": "Security",
        "question": "A developer needs client-side encryption of objects before uploading to S3. Which approach meets this requirement?",
        "options": [
            "A) Rely only on SSE-S3 after upload",
            "B) Encrypt data in the application (e.g., AWS Encryption SDK) before PutObject",
            "C) Enable Transfer Acceleration",
            "D) Use only CloudWatch Logs encryption",
        ],
        "answer": "B",
        "explanation": "Client-side encryption encrypts data before it leaves the client. Server-side encryption (SSE-*) encrypts after S3 receives the object.",
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
            "D) AWS OpsWorks",
        ],
        "answer": "B",
        "explanation": "AWS SAM is a framework for building serverless applications, providing simplified syntax for Lambda functions, API Gateway, and DynamoDB tables.",
    },
    {
        "id": "q32",
        "domain": "Deployment",
        "question": "In a CI/CD pipeline using AWS CodePipeline, which stage is responsible for transforming source code into a deployable artifact?",
        "options": [
            "A) Source stage",
            "B) Build stage",
            "C) Deploy stage",
            "D) Approval stage",
        ],
        "answer": "B",
        "explanation": "The Build stage (typically using CodeBuild) compiles source code, runs tests, and produces deployable artifacts like Lambda deployment packages or Docker images.",
    },
    {
        "id": "q33",
        "domain": "Deployment",
        "question": "What does the 'Transform: AWS::Serverless-2016-10-31' section in a CloudFormation template indicate?",
        "options": [
            "A) The template is being converted to JSON",
            "B) The template uses AWS SAM syntax that needs to be transformed to standard CloudFormation",
            "C) The template is for a legacy application",
            "D) The template uses CDK constructs",
        ],
        "answer": "B",
        "explanation": "The Transform section tells CloudFormation to use the SAM transform, which converts SAM-specific resource types into standard CloudFormation resources.",
    },
    {
        "id": "q34",
        "domain": "Deployment",
        "question": "A developer wants to perform blue/green deployments for a Lambda function. Which deployment preference should they use in SAM?",
        "options": [
            "A) AllAtOnce",
            "B) Canary10Percent5Minutes",
            "C) Linear10PercentEvery3Minutes",
            "D) Rolling",
        ],
        "answer": "B",
        "explanation": "Canary10Percent5Minutes shifts 10% of traffic to the new version, waits 5 minutes, then shifts the remaining 90%. This is a blue/green-style canary for Lambda.",
    },
    {
        "id": "q35",
        "domain": "Deployment",
        "question": "Which Elastic Beanstalk deployment strategy has the HIGHEST availability but takes the longest?",
        "options": [
            "A) All at once",
            "B) Rolling",
            "C) Rolling with additional batch",
            "D) Immutable",
        ],
        "answer": "D",
        "explanation": "Immutable deployment creates a completely new set of instances, ensuring full availability during deployment. It's the safest but slowest and most expensive option.",
    },
    {
        "id": "q36",
        "domain": "Deployment",
        "question": "A developer is using AWS CDK to define infrastructure. Which command generates the CloudFormation template without deploying?",
        "options": [
            "A) cdk deploy",
            "B) cdk synth",
            "C) cdk init",
            "D) cdk diff",
        ],
        "answer": "B",
        "explanation": "cdk synth (synthesize) generates the CloudFormation template from CDK code without deploying. This is useful for reviewing changes before deployment.",
    },
    {
        "id": "q37",
        "domain": "Deployment",
        "question": "Which CloudFormation intrinsic function is used to reference a resource's attribute?",
        "options": [
            "A) Fn::Ref",
            "B) Fn::GetAtt",
            "C) Fn::Sub",
            "D) Fn::Join",
        ],
        "answer": "B",
        "explanation": "Fn::GetAtt returns the value of an attribute from a resource in the template, such as a Lambda function's Arn or an S3 bucket's DomainName.",
    },
    {
        "id": "q38",
        "domain": "Deployment",
        "question": "A developer wants to share a Lambda function's ARN from one CloudFormation stack to another. How can they do this?",
        "options": [
            "A) Use Fn::Ref in the second stack",
            "B) Use Outputs with Export in the first stack and Fn::ImportValue in the second stack",
            "C) Hardcode the ARN in both stacks",
            "D) Use SSM parameters automatically",
        ],
        "answer": "B",
        "explanation": "CloudFormation cross-stack references use Outputs with Export Name in one stack and Fn::ImportValue in another to share values between stacks.",
    },
    {
        "id": "q39",
        "domain": "Deployment",
        "question": "What is the purpose of a buildspec.yml file in AWS CodeBuild?",
        "options": [
            "A) It defines the infrastructure resources",
            "B) It contains the build commands and settings for CodeBuild",
            "C) It configures CodePipeline stages",
            "D) It defines IAM policies for the build",
        ],
        "answer": "B",
        "explanation": "The buildspec.yml defines the build phases (install, pre_build, build, post_build), environment variables, and artifacts for CodeBuild.",
    },
    {
        "id": "q40",
        "domain": "Deployment",
        "question": "Which AWS SAM CLI command validates a SAM template locally?",
        "options": [
            "A) sam validate",
            "B) sam deploy --no-execute-changeset",
            "C) sam build --validate",
            "D) sam local invoke",
        ],
        "answer": "A",
        "explanation": "sam validate checks the SAM template for syntax and structural errors. It can validate both SAM and CloudFormation templates.",
    },
    {
        "id": "q41",
        "domain": "Deployment",
        "question": "A developer needs to deploy a containerized application without managing any infrastructure. Which combination should they use?",
        "options": [
            "A) EC2 + Docker",
            "B) ECS with Fargate launch type",
            "C) ECS with EC2 launch type",
            "D) Elastic Beanstalk with Docker platform",
        ],
        "answer": "B",
        "explanation": "ECS with Fargate eliminates infrastructure management for containers. Fargate provisions and manages the underlying compute resources automatically.",
    },
    {
        "id": "q42",
        "domain": "Deployment",
        "question": "In CloudFormation, what happens when a stack update fails?",
        "options": [
            "A) The stack is deleted",
            "B) Changes are automatically rolled back to the previous known good state",
            "C) The stack is paused for manual review",
            "D) Only the failed resource is deleted",
        ],
        "answer": "B",
        "explanation": "CloudFormation automatically rolls back changes on failure by default. All changes made during the update are reverted to the previous stable state.",
    },
    {
        "id": "q43",
        "domain": "Deployment",
        "question": "Which AWS CDK construct level provides the highest abstraction with pre-configured patterns?",
        "options": [
            "A) L1 constructs (CfnXxx)",
            "B) L2 constructs",
            "C) L3 constructs (Patterns)",
            "D) L0 constructs",
        ],
        "answer": "C",
        "explanation": "L3 constructs (also called patterns) provide the highest level of abstraction with pre-configured defaults and best practices.",
    },
    {
        "id": "q44",
        "domain": "Deployment",
        "question": "A developer wants to test a SAM application locally before deploying. Which command runs the Lambda function locally?",
        "options": [
            "A) sam validate",
            "B) sam local invoke",
            "C) sam local start-api",
            "D) sam build",
        ],
        "answer": "B",
        "explanation": "sam local invoke runs a Lambda function locally using Docker. sam local start-api starts a local API server instead of invoking directly.",
    },
    {
        "id": "q45",
        "domain": "Deployment",
        "question": "Which Elastic Beanstalk deployment policy is the FASTEST but causes temporary unavailability?",
        "options": [
            "A) All at once",
            "B) Rolling",
            "C) Rolling with additional batch",
            "D) Immutable",
        ],
        "answer": "A",
        "explanation": "All at once deploys to all instances simultaneously, making it the fastest but causes temporary downtime during the deployment.",
    },
    {
        "id": "q65",
        "domain": "Deployment",
        "question": "What is the purpose of 'sam build' command?",
        "options": [
            "A) To deploy the SAM application",
            "B) To create a deployment artifact by building Lambda functions and copying dependencies",
            "C) To delete a SAM application",
            "D) To test the SAM application in production",
        ],
        "answer": "B",
        "explanation": "sam build processes the SAM template, builds Lambda functions (installing dependencies), and creates deployment artifacts in the .aws-sam directory.",
    },
    {
        "id": "q67",
        "domain": "Deployment",
        "question": "A developer wants to use environment-specific configurations in a SAM template. How can they achieve this?",
        "options": [
            "A) Hardcode values in the template",
            "B) Use SAM template parameters with different values per environment",
            "C) Use separate templates for each environment",
            "D) Use environment variables in CloudFormation",
        ],
        "answer": "B",
        "explanation": "SAM templates support CloudFormation parameters, allowing you to pass environment-specific values at deployment time using parameter overrides.",
    },
    {
        "id": "q117",
        "domain": "Deployment",
        "question": "What does CodeDeploy AppSpec (appspec.yml) define for Lambda deployments?",
        "options": [
            "A) Only VPC subnets",
            "B) How traffic is shifted between versions and lifecycle hooks (BeforeAllowTraffic, AfterAllowTraffic)",
            "C) CloudWatch log retention only",
            "D) Cognito user attributes",
        ],
        "answer": "B",
        "explanation": "For Lambda, AppSpec configures alias traffic shifting and optional hooks that run validation Lambda functions during deployment.",
    },
    {
        "id": "q118",
        "domain": "Deployment",
        "question": "Which CodePipeline action provider typically stores source code from a Git repository?",
        "options": [
            "A) AWS CodeCommit, GitHub, or Amazon S3 as Source actions",
            "B) Amazon Athena",
            "C) Amazon Macie",
            "D) AWS Batch only",
        ],
        "answer": "A",
        "explanation": "CodePipeline Source stages commonly pull from CodeCommit, GitHub/GitHub Enterprise, Bitbucket, or S3 artifacts.",
    },
    {
        "id": "q119",
        "domain": "Deployment",
        "question": "CloudFormation nested stacks are used primarily to:",
        "options": [
            "A) Avoid using parameters",
            "B) Modularize large templates by embedding child stacks as AWS::CloudFormation::Stack resources",
            "C) Bypass IAM",
            "D) Replace CodePipeline",
        ],
        "answer": "B",
        "explanation": "Nested stacks break large templates into reusable components managed as a hierarchy of stacks.",
    },
    {
        "id": "q120",
        "domain": "Deployment",
        "question": "What is a CloudFormation change set?",
        "options": [
            "A) A permanent deletion of the stack",
            "B) A preview of proposed stack changes that can be reviewed before execution",
            "C) An automatic CI/CD pipeline",
            "D) A CDK construct library",
        ],
        "answer": "B",
        "explanation": "Change sets show the impact of a proposed update (add/modify/delete resources) before you execute the update.",
    },
    {
        "id": "q121",
        "domain": "Deployment",
        "question": "SAM AutopublishAlias combined with DeploymentPreference enables:",
        "options": [
            "A) Manual zip uploads only",
            "B) Automatic version/alias publishing with gradual CodeDeploy traffic shifting",
            "C) Disabling CloudWatch Logs",
            "D) Creating EC2 instances",
        ],
        "answer": "B",
        "explanation": "AutopublishAlias creates/updates a Lambda alias; DeploymentPreference configures CodeDeploy canary/linear traffic shifting to that alias.",
    },
    {
        "id": "q122",
        "domain": "Deployment",
        "question": "Which Elastic Beanstalk deployment policy launches a temporary set of instances alongside the old ones to avoid capacity reduction?",
        "options": [
            "A) All at once",
            "B) Rolling",
            "C) Rolling with additional batch",
            "D) Traffic splitting only on Lambda",
        ],
        "answer": "C",
        "explanation": "Rolling with additional batch launches new instances first so capacity is not reduced while old instances are updated.",
    },
    {
        "id": "q123",
        "domain": "Deployment",
        "question": "What does cdk diff show?",
        "options": [
            "A) Only TypeScript compile errors",
            "B) Differences between the synthesized template and the deployed stack",
            "C) Git commit history",
            "D) Lambda cold start metrics",
        ],
        "answer": "B",
        "explanation": "cdk diff compares local CDK synth output with the currently deployed CloudFormation stack resources.",
    },
    {
        "id": "q124",
        "domain": "Deployment",
        "question": "In CodeBuild, privileged mode is required primarily when the build needs to:",
        "options": [
            "A) Call DynamoDB",
            "B) Build Docker images (Docker-in-Docker)",
            "C) Write CloudWatch Logs",
            "D) Assume an IAM role",
        ],
        "answer": "B",
        "explanation": "Privileged mode grants elevated permissions needed to run Docker daemon operations for building container images.",
    },
    {
        "id": "q125",
        "domain": "Deployment",
        "question": "CloudFormation Fn::Sub is used to:",
        "options": [
            "A) Delete stacks",
            "B) Perform string substitution with ${Variable} placeholders",
            "C) Create change sets only",
            "D) Import existing resources exclusively",
        ],
        "answer": "B",
        "explanation": "Fn::Sub substitutes variables and resource attributes into strings, commonly for ARNs and configuration values.",
    },
    {
        "id": "q126",
        "domain": "Deployment",
        "question": "A developer needs to update only a Lambda function's code without changing infrastructure. Which approach works?",
        "options": [
            "A) Always recreate the entire CloudFormation stack",
            "B) Use aws lambda update-function-code or deploy via SAM/CFN updating the function resource code",
            "C) Change the DynamoDB table name",
            "D) Disable the API Gateway stage",
        ],
        "answer": "B",
        "explanation": "Lambda code can be updated independently via UpdateFunctionCode or IaC updates that change only the function's code property.",
    },
    {
        "id": "q127",
        "domain": "Deployment",
        "question": "What is the purpose of a CodePipeline manual approval action?",
        "options": [
            "A) To compile source code",
            "B) To pause the pipeline until a reviewer approves before continuing to production deploy",
            "C) To create IAM users",
            "D) To rotate KMS keys",
        ],
        "answer": "B",
        "explanation": "Manual approval actions gate progression (often before prod) until an authorized user approves or rejects.",
    },
    {
        "id": "q128",
        "domain": "Deployment",
        "question": "SAM Globals section is used to:",
        "options": [
            "A) Define account-wide SCPs",
            "B) Set default properties shared by serverless resources (Runtime, Timeout, Environment, etc.)",
            "C) Replace Parameters",
            "D) Configure Organization trails",
        ],
        "answer": "B",
        "explanation": "Globals reduce duplication by applying common Function/Api/SimpleTable properties across SAM resources.",
    },
    {
        "id": "q129",
        "domain": "Deployment",
        "question": "CloudFormation stack policies are used to:",
        "options": [
            "A) Encrypt all parameters automatically",
            "B) Prevent updates to critical resources during stack updates unless explicitly allowed",
            "C) Replace IAM identity policies",
            "D) Speed up rollbacks only",
        ],
        "answer": "B",
        "explanation": "Stack policies protect resources from unintended updates (e.g., databases) during CloudFormation stack operations.",
    },
    {
        "id": "q130",
        "domain": "Deployment",
        "question": "Which artifact store does CodePipeline commonly use between stages?",
        "options": [
            "A) Amazon S3",
            "B) Amazon Neptune",
            "C) Amazon MQ",
            "D) Amazon Lex",
        ],
        "answer": "A",
        "explanation": "CodePipeline uses an S3 artifact bucket to pass build/deploy artifacts between pipeline stages.",
    },
    {
        "id": "q131",
        "domain": "Deployment",
        "question": "Elastic Beanstalk .ebextensions configuration files are used to:",
        "options": [
            "A) Define Lambda layers",
            "B) Customize environment configuration (packages, files, option settings) during deployment",
            "C) Create Cognito User Pools",
            "D) Configure X-Ray sampling only",
        ],
        "answer": "B",
        "explanation": ".ebextensions YAML/JSON files customize Beanstalk environments—software, files, commands, and option settings.",
    },
    {
        "id": "q132",
        "domain": "Deployment",
        "question": "What does AWS::Serverless::Function Events property typically configure?",
        "options": [
            "A) Only CloudTrail events",
            "B) Event sources such as API Gateway, S3, SQS, SNS, DynamoDB Streams, Schedule, etc.",
            "C) VPC Flow Logs exclusively",
            "D) KMS key rotation schedule",
        ],
        "answer": "B",
        "explanation": "SAM Events attach triggers to Lambda (HTTP APIs, queues, topics, schedules, and more) with simplified syntax.",
    },
    {
        "id": "q133",
        "domain": "Deployment",
        "question": "CDK bootstrapping (cdk bootstrap) is required to:",
        "options": [
            "A) Install Node.js",
            "B) Provision staging resources (S3, IAM roles, ECR) in an environment for CDK deployments",
            "C) Create Cognito Identity Pools",
            "D) Enable MFA on the root user",
        ],
        "answer": "B",
        "explanation": "Bootstrap creates the CDK toolkit stack with assets bucket and deployment roles needed for cdk deploy in that account/region.",
    },
    {
        "id": "q134",
        "domain": "Deployment",
        "question": "CodeDeploy blue/green for ECS typically involves:",
        "options": [
            "A) Replacing Lambda layers only",
            "B) Shifting traffic from an original task set to a replacement task set using a load balancer listener",
            "C) Deleting the VPC",
            "D) Disabling CloudWatch",
        ],
        "answer": "B",
        "explanation": "ECS blue/green with CodeDeploy creates a new task set and shifts load balancer traffic gradually or all at once to the replacement set.",
    },
    {
        "id": "q135",
        "domain": "Deployment",
        "question": "Which CloudFormation feature imports existing resources into a stack?",
        "options": [
            "A) StackSets only",
            "B) Resource import (create change set with Import)",
            "C) Drift detection exclusively",
            "D) Termination protection",
        ],
        "answer": "B",
        "explanation": "Resource import brings existing resources under CloudFormation management using an import change set and a template that matches current configuration.",
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
            "D) CloudTrail",
        ],
        "answer": "B",
        "explanation": "CloudWatch Logs Insights provides a powerful query language for searching and analyzing log data, including filtering, aggregation, and sorting.",
    },
    {
        "id": "q47",
        "domain": "Monitoring",
        "question": "Which AWS service provides a record of API calls made in an AWS account?",
        "options": [
            "A) CloudWatch Logs",
            "B) CloudTrail",
            "C) X-Ray",
            "D) VPC Flow Logs",
        ],
        "answer": "B",
        "explanation": "CloudTrail records API calls made in your AWS account, including who made the call, when, and what resources were affected.",
    },
    {
        "id": "q48",
        "domain": "Monitoring",
        "question": "A developer needs to trace requests across multiple Lambda functions and API Gateway. Which service should they enable?",
        "options": [
            "A) CloudWatch Logs",
            "B) CloudTrail",
            "C) AWS X-Ray",
            "D) CloudWatch Alarms",
        ],
        "answer": "C",
        "explanation": "AWS X-Ray provides distributed tracing, allowing you to trace requests across multiple services, visualize service maps, and identify performance bottlenecks.",
    },
    {
        "id": "q49",
        "domain": "Monitoring",
        "question": "A Lambda function is timing out when connecting to an RDS database in a VPC. What is the MOST likely cause?",
        "options": [
            "A) The Lambda function has insufficient memory",
            "B) The Lambda function's security group doesn't allow outbound traffic to RDS",
            "C) The Lambda function is not configured to run in the VPC",
            "D) Both B and C could be causes",
        ],
        "answer": "D",
        "explanation": "Lambda functions need to be configured in the correct VPC/subnets with appropriate security groups to access VPC resources like RDS.",
    },
    {
        "id": "q50",
        "domain": "Monitoring",
        "question": "Which CloudWatch metric is used to monitor Lambda function invocations?",
        "options": [
            "A) CPUUtilization",
            "B) Invocations",
            "C) RequestCount",
            "D) Throughput",
        ],
        "answer": "B",
        "explanation": "CloudWatch publishes Lambda metrics including Invocations, Duration, Errors, Throttles, and ConcurrentExecutions.",
    },
    {
        "id": "q51",
        "domain": "Monitoring",
        "question": "A developer wants to create a CloudWatch alarm that triggers when Lambda error rate exceeds 5%. Which metric should they use?",
        "options": [
            "A) Invocations",
            "B) Duration",
            "C) Errors (with math expression Errors/Invocations)",
            "D) Throttles",
        ],
        "answer": "C",
        "explanation": "To calculate error rate, use a metric math expression dividing Errors by Invocations, then set the alarm threshold at 0.05 (5%).",
    },
    {
        "id": "q52",
        "domain": "Monitoring",
        "question": "What is the purpose of a CloudWatch metric filter?",
        "options": [
            "A) To filter which logs are sent to S3",
            "B) To extract metric values from log events",
            "C) To delete old log entries",
            "D) To encrypt log data",
        ],
        "answer": "B",
        "explanation": "Metric filters define patterns to match in log events and turn them into CloudWatch numeric metrics for alarms and dashboards.",
    },
    {
        "id": "q53",
        "domain": "Monitoring",
        "question": "A developer wants to use X-Ray to trace a Lambda function. What is the MINIMUM configuration needed?",
        "options": [
            "A) Install the X-Ray SDK and modify all code",
            "B) Enable X-Ray active tracing on the Lambda function configuration",
            "C) Create a CloudTrail trail",
            "D) Enable VPC Flow Logs",
        ],
        "answer": "B",
        "explanation": "For Lambda, enabling active tracing in the function configuration provides basic tracing. The X-Ray SDK is needed for custom subsegments and annotations.",
    },
    {
        "id": "q54",
        "domain": "Monitoring",
        "question": "An API Gateway REST API is returning 429 errors. What should the developer do?",
        "options": [
            "A) Increase the Lambda function memory",
            "B) Enable throttling with appropriate rate and burst limits",
            "C) Switch to a regional API endpoint",
            "D) Disable authentication",
        ],
        "answer": "B",
        "explanation": "429 Too Many Requests indicates throttling. Configure appropriate rate/burst limits or request a limit increase from AWS.",
    },
    {
        "id": "q55",
        "domain": "Monitoring",
        "question": "A developer receives a 'ProvisionedThroughputExceededException' from DynamoDB. What is the BEST immediate action?",
        "options": [
            "A) Delete the table and recreate it",
            "B) Switch to on-demand capacity mode or increase provisioned capacity",
            "C) Enable encryption",
            "D) Add a global secondary index",
        ],
        "answer": "B",
        "explanation": "This error means you've exceeded provisioned throughput. Switch to on-demand (PAY_PER_REQUEST) or increase RCUs/WCUs.",
    },
    {
        "id": "q56",
        "domain": "Monitoring",
        "question": "Which X-Ray feature allows searching traces by custom attributes?",
        "options": [
            "A) Annotations",
            "B) Metadata",
            "C) Segments",
            "D) Sampling rules",
        ],
        "answer": "A",
        "explanation": "Annotations are indexed key-value pairs that can be used to filter and search traces. Metadata is not indexed.",
    },
    {
        "id": "q57",
        "domain": "Monitoring",
        "question": "A Lambda function in a VPC cannot reach the internet. What is missing?",
        "options": [
            "A) More memory",
            "B) A NAT Gateway in the VPC's public subnet",
            "C) A larger timeout",
            "D) An Elastic IP address",
        ],
        "answer": "B",
        "explanation": "Lambda in a VPC needs a NAT Gateway (or similar) in a public subnet for internet access; place the function in a private subnet with a route to the NAT.",
    },
    {
        "id": "q58",
        "domain": "Monitoring",
        "question": "What is the default retention period for CloudWatch Logs?",
        "options": [
            "A) 7 days",
            "B) 30 days",
            "C) Never expire (infinite retention)",
            "D) 90 days",
        ],
        "answer": "C",
        "explanation": "By default, CloudWatch Logs never expire. You can configure retention from 1 day to 10 years, or keep data indefinitely.",
    },
    {
        "id": "q59",
        "domain": "Monitoring",
        "question": "Which service should be used to monitor API Gateway REST API access logs?",
        "options": [
            "A) CloudTrail only",
            "B) CloudWatch Logs with API Gateway access logging enabled",
            "C) S3 only",
            "D) X-Ray only",
        ],
        "answer": "B",
        "explanation": "API Gateway can send access logs to CloudWatch Logs with detailed request/response information for monitoring and troubleshooting.",
    },
    {
        "id": "q60",
        "domain": "Monitoring",
        "question": "A developer needs to be notified when a DynamoDB table's consumed capacity exceeds 80%. What should they configure?",
        "options": [
            "A) A CloudWatch Alarm on the ConsumedReadCapacityUnits or ConsumedWriteCapacityUnits metric",
            "B) A DynamoDB Stream",
            "C) A CloudTrail trail",
            "D) An X-Ray sampling rule",
        ],
        "answer": "A",
        "explanation": "CloudWatch Alarms can monitor DynamoDB capacity metrics and trigger notifications via SNS.",
    },
    {
        "id": "q68",
        "domain": "Monitoring",
        "question": "What is the default sampling rate for X-Ray when no sampling rules are configured?",
        "options": [
            "A) 0% (no traces)",
            "B) 100% (all requests)",
            "C) 1 request per second, then 5% of additional requests",
            "D) 10% of all requests",
        ],
        "answer": "C",
        "explanation": "The default X-Ray sampling rule traces the first request each second, then 5% of additional requests.",
    },
    {
        "id": "q136",
        "domain": "Monitoring",
        "question": "A Lambda function shows high Throttles in CloudWatch. What does this indicate?",
        "options": [
            "A) The function code has a syntax error",
            "B) Concurrent executions exceeded reserved or account concurrency limits",
            "C) The DynamoDB table is empty",
            "D) X-Ray is disabled",
        ],
        "answer": "B",
        "explanation": "Throttles occur when Lambda cannot scale further due to reserved concurrency or account concurrency limits being reached.",
    },
    {
        "id": "q137",
        "domain": "Monitoring",
        "question": "Which CloudWatch Logs Insights query finds the 10 slowest Lambda durations from REPORT lines?",
        "options": [
            "A) DELETE FROM log_group",
            "B) A query filtering REPORT lines, parsing Duration, sorting desc, and limiting 10",
            "C) SELECT * FROM dynamodb",
            "D) Only the X-Ray console can do this",
        ],
        "answer": "B",
        "explanation": "Logs Insights can filter REPORT log lines, parse fields like Duration, sort, and limit results for performance analysis.",
    },
    {
        "id": "q138",
        "domain": "Monitoring",
        "question": "What is CloudWatch Logs subscription filter used for?",
        "options": [
            "A) Encrypting log groups with SSE-S3 only",
            "B) Streaming matching log events in near real time to Kinesis, Firehose, or Lambda",
            "C) Deleting empty log streams",
            "D) Replacing metric filters entirely with no metrics",
        ],
        "answer": "B",
        "explanation": "Subscription filters deliver real-time log events matching a filter pattern to streaming or Lambda destinations for processing.",
    },
    {
        "id": "q139",
        "domain": "Monitoring",
        "question": "An X-Ray service map shows a node with a high fault rate. Faults typically indicate:",
        "options": [
            "A) Successful 2xx responses",
            "B) 5xx errors / server-side failures in the traced service",
            "C) Only cold starts",
            "D) Missing IAM roles exclusively",
        ],
        "answer": "B",
        "explanation": "In X-Ray, faults generally correspond to 5xx errors. Errors often map to 4xx client issues; throttles are rate-limit related.",
    },
    {
        "id": "q140",
        "domain": "Monitoring",
        "question": "A developer needs structured logging from Lambda for easier querying. What is a recommended practice?",
        "options": [
            "A) Print unstructured free-form strings only",
            "B) Emit JSON log lines with consistent fields (level, requestId, message) to stdout",
            "C) Disable CloudWatch Logs",
            "D) Log only to local disk",
        ],
        "answer": "B",
        "explanation": "JSON structured logs work well with Logs Insights filters/parses and make correlation by requestId easier.",
    },
    {
        "id": "q141",
        "domain": "Monitoring",
        "question": "Which Lambda metric indicates how long the initialization (cold start) phase took?",
        "options": [
            "A) Init Duration (reported in REPORT / Performance metrics where available)",
            "B) ApproximateNumberOfMessagesVisible",
            "C) BucketSizeBytes",
            "D) HealthyHostCount",
        ],
        "answer": "A",
        "explanation": "Cold start initialization time appears as Init Duration in Lambda REPORT logs and related performance metrics.",
    },
    {
        "id": "q142",
        "domain": "Monitoring",
        "question": "CloudWatch alarm state INSUFFICIENT_DATA usually means:",
        "options": [
            "A) The alarm threshold was breached",
            "B) Not enough data points are available yet for the configured evaluation period",
            "C) The AWS account was suspended",
            "D) X-Ray tracing is mandatory",
        ],
        "answer": "B",
        "explanation": "INSUFFICIENT_DATA occurs when CloudWatch lacks enough datapoints to evaluate the alarm (e.g., new metric or sparse activity).",
    },
    {
        "id": "q143",
        "domain": "Monitoring",
        "question": "To capture failed asynchronous Lambda invocations for later analysis, configure:",
        "options": [
            "A) A dead-letter queue (SQS/SNS) or Lambda destination on failure",
            "B) Only S3 Transfer Acceleration",
            "C) Cognito hosted UI",
            "D) CloudFront signed URLs",
        ],
        "answer": "A",
        "explanation": "Async Lambda failures can be routed to a DLQ or on-failure destination (SQS, SNS, EventBridge, another Lambda) for inspection and retry.",
    },
    {
        "id": "q144",
        "domain": "Monitoring",
        "question": "API Gateway integration latency vs latency metrics differ how?",
        "options": [
            "A) They are identical always",
            "B) Latency includes overhead end-to-end at API Gateway; IntegrationLatency measures time spent calling the backend",
            "C) IntegrationLatency includes client network only",
            "D) Neither is published to CloudWatch",
        ],
        "answer": "B",
        "explanation": "IntegrationLatency is backend call time; Latency is overall API Gateway request time including gateway overhead.",
    },
    {
        "id": "q145",
        "domain": "Monitoring",
        "question": "A developer enables X-Ray tracing on API Gateway. What additional step helps end-to-end traces into Lambda?",
        "options": [
            "A) Disable Lambda logs",
            "B) Enable active tracing on the Lambda function as well",
            "C) Delete the API stage",
            "D) Use only MOCK integrations",
        ],
        "answer": "B",
        "explanation": "For complete traces through API Gateway into Lambda, enable X-Ray on both the API stage and the Lambda function.",
    },
    {
        "id": "q146",
        "domain": "Monitoring",
        "question": "Which tool helps determine if CloudFormation stack resources have drifted from the template?",
        "options": [
            "A) CloudFormation drift detection",
            "B) Amazon Polly",
            "C) AWS Snowball",
            "D) Amazon Rekognition",
        ],
        "answer": "A",
        "explanation": "Drift detection compares actual resource configuration with the stack template and reports differences.",
    },
    {
        "id": "q147",
        "domain": "Monitoring",
        "question": "DynamoDB Contributor Insights helps identify:",
        "options": [
            "A) The most accessed keys / items causing hot partitions or heavy traffic",
            "B) KMS key rotation status only",
            "C) S3 storage class transitions",
            "D) Cognito password policies",
        ],
        "answer": "A",
        "explanation": "Contributor Insights surfaces frequently accessed keys and traffic patterns useful for diagnosing hot partitions.",
    },
    {
        "id": "q148",
        "domain": "Monitoring",
        "question": "A Step Functions execution fails. Where should the developer look FIRST for the failing state and error cause?",
        "options": [
            "A) The Step Functions console execution history / event details",
            "B) Only Amazon Macie findings",
            "C) ECR image scan results",
            "D) Route 53 health checks",
        ],
        "answer": "A",
        "explanation": "Step Functions execution event history shows each state transition, inputs/outputs, and error causes for failed steps.",
    },
    {
        "id": "q149",
        "domain": "Monitoring",
        "question": "Embedded Metric Format (EMF) in CloudWatch is used to:",
        "options": [
            "A) Embed IAM policies in logs",
            "B) Emit custom metrics by writing specially formatted JSON log events",
            "C) Replace CloudTrail",
            "D) Disable alarms permanently",
        ],
        "answer": "B",
        "explanation": "EMF lets applications put custom metrics via structured logs that CloudWatch extracts without separate PutMetricData calls.",
    },
    {
        "id": "q150",
        "domain": "Monitoring",
        "question": "Lambda Destinations (on success/failure) for asynchronous invocations can send results to:",
        "options": [
            "A) Only Amazon RDS",
            "B) SQS, SNS, EventBridge, or another Lambda function",
            "C) Only CloudFront",
            "D) Only IAM",
        ],
        "answer": "B",
        "explanation": "Lambda Destinations route async invocation records to SQS, SNS, EventBridge, or Lambda for success or failure handling.",
    },
    {
        "id": "q151",
        "domain": "Development",
        "question": "A developer needs to process DynamoDB item changes with Lambda near real time. What should they configure?",
        "options": [
            "A) DynamoDB Streams as a Lambda event source",
            "B) S3 inventory reports",
            "C) CloudFront invalidations",
            "D) ECR lifecycle policies",
        ],
        "answer": "A",
        "explanation": "DynamoDB Streams + Lambda event source mapping processes insert/update/delete records shortly after they occur.",
    },
    {
        "id": "q152",
        "domain": "Security",
        "question": "Which S3 encryption option requires the customer to provide an encryption key with each request?",
        "options": [
            "A) SSE-S3",
            "B) SSE-KMS",
            "C) SSE-C",
            "D) Client-side encryption with Encryption SDK managed keys stored only in KMS",
        ],
        "answer": "C",
        "explanation": "SSE-C (customer-provided keys) requires the client to supply the encryption key on each upload/download request.",
    },
    {
        "id": "q153",
        "domain": "Deployment",
        "question": "CodeBuild project environment variables marked as Parameter Store or Secrets Manager type are useful to:",
        "options": [
            "A) Commit secrets into buildspec.yml in plaintext",
            "B) Inject secrets at build time without hardcoding them in the repository",
            "C) Disable CloudWatch Logs for builds",
            "D) Skip the install phase",
        ],
        "answer": "B",
        "explanation": "CodeBuild can resolve environment variables from SSM or Secrets Manager at runtime so secrets stay out of source control.",
    },
    {
        "id": "q154",
        "domain": "Monitoring",
        "question": "Which alarm action commonly notifies an operations channel when a metric breaches a threshold?",
        "options": [
            "A) Publish to an SNS topic subscribed by email/Slack/Lambda",
            "B) Delete the CloudWatch log group",
            "C) Disable API Gateway",
            "D) Rotate Cognito clients",
        ],
        "answer": "A",
        "explanation": "CloudWatch Alarms typically notify via SNS, which fans out to email, chat integrations, Lambda, and other subscribers.",
    },
    {
        "id": "q155",
        "domain": "Development",
        "question": "When designing DynamoDB partition keys, what practice helps avoid hot partitions?",
        "options": [
            "A) Use a single static partition key for all items",
            "B) Choose high-cardinality keys (and consider write sharding) so traffic spreads across partitions",
            "C) Always use Scan instead of Query",
            "D) Disable TTL",
        ],
        "answer": "B",
        "explanation": "High-cardinality partition keys distribute load. Hot keys can be mitigated with sharding suffixes when a natural key is too concentrated.",
    },
]

# ============================================================
# Generate exams (balanced domains, reduced overlap)
# ============================================================


def _by_domain(questions):
    buckets = defaultdict(list)
    for q in questions:
        buckets[q["domain"]].append(q)
    return buckets


def select_exams(questions, num_exams=5, num_questions=65):
    """Select exam question sets with domain balance and minimized reuse."""
    usage = {q["id"]: 0 for q in questions}
    q_by_id = {q["id"]: q for q in questions}
    domain_buckets = _by_domain(questions)

    exams = []
    for exam_num in range(1, num_exams + 1):
        rng = random.Random(exam_num * 42)
        selected = []
        selected_ids = set()

        # Prefer least-used questions within each domain target
        for domain, target in DOMAIN_TARGETS.items():
            pool = list(domain_buckets.get(domain, []))
            rng.shuffle(pool)
            pool.sort(key=lambda q: (usage[q["id"]], q["id"]))
            take = min(target, len(pool))
            for q in pool[:take]:
                if q["id"] not in selected_ids:
                    selected.append(q)
                    selected_ids.add(q["id"])

        # Fill remaining slots from least-used overall
        remaining_needed = num_questions - len(selected)
        if remaining_needed > 0:
            rest = [q for q in questions if q["id"] not in selected_ids]
            rng.shuffle(rest)
            rest.sort(key=lambda q: (usage[q["id"]], q["id"]))
            for q in rest[:remaining_needed]:
                selected.append(q)
                selected_ids.add(q["id"])

        # Final shuffle for exam presentation order
        rng.shuffle(selected)
        selected = selected[:num_questions]

        for q in selected:
            usage[q["id"]] += 1

        exams.append(selected)

    return exams, usage


def generate_exam_markdown(exam_num, selected):
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
        for opt in q["options"]:
            md += f"- {opt}\n"
        md += "\n---\n\n"

    md += "\n---\n\n"
    md += "# Answers & Explanations\n\n"
    md += "---\n\n"

    for i, q in enumerate(selected, 1):
        md += f"## Question {i} — Answer: {q['answer']}\n\n"
        md += f"**Explanation:** {q['explanation']}\n\n"
        md += "---\n\n"

    return md


def generate_all():
    EXAMS_DIR.mkdir(parents=True, exist_ok=True)

    ids = [q["id"] for q in QUESTIONS]
    if len(ids) != len(set(ids)):
        dupes = [i for i in ids if ids.count(i) > 1]
        raise SystemExit(f"Duplicate question ids: {sorted(set(dupes))}")

    print(f"Question bank: {len(QUESTIONS)} unique questions")
    print(f"Output directory: {EXAMS_DIR}")

    exams, usage = select_exams(QUESTIONS, num_exams=5, num_questions=65)

    index = """# Practice Exams

**AWS Certified Developer - Associate (DVA-C02)**

## Available Exams

| Exam | Questions | Topics |
|------|-----------|--------|
"""

    for exam_num, selected in enumerate(exams, 1):
        domains = {}
        for q in selected:
            domains[q["domain"]] = domains.get(q["domain"], 0) + 1

        filename = f"exam-{exam_num:02d}.md"
        (EXAMS_DIR / filename).write_text(generate_exam_markdown(exam_num, selected), encoding="utf-8")

        domain_str = ", ".join(f"{d}: {c}" for d, c in sorted(domains.items()))
        index += f"| [Exam {exam_num}](exam-{exam_num:02d}.md) | {len(selected)} | {domain_str} |\n"
        print(f"  Created: {filename} ({len(selected)} questions) — {domain_str}")

    max_reuse = max(usage.values()) if usage else 0
    never_used = sum(1 for c in usage.values() if c == 0)
    print(f"  Overlap: max times any question reused = {max_reuse}; unused in any exam = {never_used}")

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

- [Study Guide →](../README.md)
- [Hands-on Exercises →](../exercises/)
"""

    (EXAMS_DIR / "README.md").write_text(index, encoding="utf-8")
    print(f"\nDone! Generated 5 practice exams from {len(QUESTIONS)} unique questions.")


if __name__ == "__main__":
    generate_all()
