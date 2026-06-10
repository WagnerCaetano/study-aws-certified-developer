# Amazon API Gateway

> **Domain 1: Development with AWS Services** | [← Lambda](02-lambda.md) | [Back to Index](../../README.md) | [Next: DynamoDB →](04-dynamodb.md)

---

## Overview

Amazon API Gateway is a fully managed service for creating, publishing, maintaining, monitoring, and securing **REST**, **HTTP**, and **WebSocket** APIs at any scale.

```
┌──────────┐     ┌───────────────┐     ┌──────────────┐
│  Client   │────►│  API Gateway  │────►│  Backend     │
│ (Browser) │◄────│  (Endpoint)   │◄────│  (Lambda/ECS)│
└──────────┘     └───────────────┘     └──────────────┘
                       │
                 Rate limiting, auth,
                 caching, transformation
```

---

## API Gateway Types

| Feature | REST API | HTTP API | WebSocket API |
|---------|----------|----------|---------------|
| Purpose | Full-featured APIs | Simple, low-cost APIs | Real-time, bidirectional |
| Cost | Higher | Lower (~70% cheaper) | Per message + connection |
| Features | Request/response mapping, usage plans | Simple routing, JWT auth | Persistent connections |
| Auth | IAM, Cognito, Lambda, Custom | JWT, IAM | IAM, Lambda |
| Cache | Built-in (caching) | No | No |
| Use Case | Complex enterprise APIs | Lambda proxy, simple CRUD | Chat, streaming, IoT |

---

## API Gateway REST API Architecture

```
┌──────────────────────────────────────────────────────┐
│                    REST API                           │
│                                                      │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Resource │──│ Method   │──│Integration│──► Backend│
│  │ /users   │  │ GET/POST │  │  Request  │           │
│  └─────────┘  └──────────┘  └──────────┘           │
│       │                                              │
│  ┌────────────┐                                      │
│  │ /users/{id}│                                      │
│  └────────────┘                                      │
│                                                      │
│  Stages: dev, staging, prod                          │
│  Authorizers: IAM, Cognito, Lambda                  │
└──────────────────────────────────────────────────────┘
```

### Key Components

1. **Resources** — URL paths (e.g., `/users`, `/users/{id}`)
2. **Methods** — HTTP verbs (GET, POST, PUT, DELETE, PATCH, OPTIONS)
3. **Integration** — How API Gateway connects to backend
4. **Stage** — Named deployment snapshot (dev, prod)
5. **Authorizer** — Authentication mechanism

---

## Integration Types

| Integration Type | Description | Use Case |
|-----------------|-------------|----------|
| **Lambda Function** | Direct Lambda invocation | Most common for serverless |
| **HTTP** | HTTP request to backend | Existing web services |
| **AWS Service** | Direct call to AWS service | SNS, SQS, DynamoDB, etc. |
| **Mock** | Returns a response without backend | Testing, static responses |
| **VPC Link** | Connect to private VPC resources | NLB, ALB in VPC |

### Lambda Proxy Integration

```javascript
// Lambda Proxy Integration — Lambda receives full request
export const handler = async (event) => {
    const method = event.httpMethod;        // "GET"
    const path = event.path;                // "/users/123"
    const queryParams = event.queryStringParameters; // {?page: "1"}
    const pathParams = event.pathParameters;  // {id: "123"}
    const body = JSON.parse(event.body || '{}');
    const headers = event.headers;
    
    return {
        statusCode: 200,
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({ message: "Success", data: [] })
    };
};
```

**⚠️ Important:** With Lambda Proxy Integration, you MUST return `statusCode` and `body` (as string).

---

## Authentication & Authorization

```
┌──────────────┐     ┌───────────────┐     ┌──────────┐
│   Request    │────►│  Authorizer   │────►│  Backend │
│   + Token    │     │  (Check)      │     │          │
└──────────────┘     └───────────────┘     └──────────┘
                           │
                    ┌──────┴──────┐
                    │  Allowed?   │
                    │  YES/NO     │
                    └─────────────┘
```

### 1. IAM Authorization

- Signs requests with AWS Sig v4
- Good for internal APIs
- Uses IAM policies for fine-grained access

### 2. Cognito User Pool Authorizer

```javascript
// API Gateway configuration
{
    "AuthorizationType": "COGNITO_USER_POOLS",
    "AuthorizerId": "abc123"
}

// Token comes from: Authorization: Bearer <jwt_token>
```

- Users authenticate via Cognito User Pools
- JWT token validated by API Gateway
- No custom code needed

### 3. Lambda Authorizer (Custom Authorizer)

```javascript
// Lambda Authorizer — custom auth logic
export const handler = async (event) => {
    const token = event.authorizationToken;
    
    // Your custom validation logic
    if (token === 'valid-secret-token') {
        return {
            "principalId": "user123",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event.methodArn
                    }
                ]
            },
            "context": {
                "userId": "user123",
                "role": "admin"
            }
        };
    }
    
    // Deny access
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": "Deny",
                "Resource": event.methodArn
            }]
        }
    };
};
```

**Two types of Lambda Authorizers:**
- **Token-based** — Receives bearer token in `authorizationToken`
- **Request-based** — Receives full request parameters (headers, query, path, body)

**⚠️ Caching:** Authorizer results are cached for **30 minutes** by default. Changes to user permissions may take up to 30 min to take effect!

---

## Request/Response Mapping

### Mapping Templates (Velocity Template Language - VTL)

```velocity
#set($inputRoot = $input.path('$'))
{
  "userId": "$inputRoot.id",
  "name": "$inputRoot.name",
  "timestamp": "$context.requestTime"
}
```

### Common Use Cases
- Transform request body before sending to Lambda
- Transform Lambda response to match expected API format
- Add/remove headers
- Extract path/query parameters

---

## Stage Variables & Deployments

```json
{
    "stageVariables": {
        "lambdaAlias": "prod",
        "bucketName": "my-prod-bucket"
    }
}
```

### Canary Deployments

```
┌──────────────────────────────────────┐
│  Stage: Production                   │
│  ├── Base: Version 1 (90% traffic)  │
│  └── Canary: Version 2 (10% traffic)│
└──────────────────────────────────────┘
```

---

## Caching

- **TTL:** Time-to-live in seconds (0–3600)
- Cache per method + query/header combination
- Cache key includes: method, path, query params, headers
- Max cache size: 0.5 GB to 237 GB
- **Cache invalidation:** `Cache-Control: max-age=0` (requires `invalidateCache` permission)

---

## Usage Plans & API Keys

```
Usage Plan: "Basic"
  ├── Rate limit: 10 requests/second
  ├── Burst: 50 requests
  ├── Quota: 1000 requests/month
  └── API Keys: [key1, key2, ...]
       └── x-api-key header required
```

- **Usage Plans** control who can access, at what rate
- **API Keys** are alphanumeric strings passed via `x-api-key` header
- **⚠️ API Keys are NOT authentication!** They are for rate limiting/quotas only

---

## CORS Configuration

```javascript
// Enable CORS for a resource
// API Gateway adds OPTIONS method with appropriate headers

// Required headers in Lambda response:
return {
    statusCode: 200,
    headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization"
    },
    body: JSON.stringify(data)
};
```

**⚠️ Common exam trap:** CORS errors are caused by missing headers in the Lambda response, NOT browser issues.

---

## WebSocket APIs

```
┌──────────┐     ┌───────────────┐     ┌──────────┐
│  Client   │◄───►│  API Gateway  │◄───►│  Lambda  │
│ (ws://)   │     │  WebSocket    │     │          │
└──────────┘     └───────────────┘     └──────────┘
                       │
                Connection Management:
                $connect, $disconnect,
                $default
```

### Routes
- **$connect** — When client connects
- **$disconnect** — When client disconnects
- **$default** — Unmatched route
- **Custom routes** — Based on message content

### Post to Connection
```python
import boto3
apigw = boto3.client('apigatewaymanagementapi', endpoint_url='https://xxx.execute-api.region.amazonaws.com/prod')

def lambda_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    apigw.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps({'message': 'Hello!'})
    )
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Need to secure API with JWT | Use Cognito User Pool authorizer or Lambda authorizer |
| Need to throttle API per client | Use Usage Plans + API Keys |
| CORS errors in browser | Add CORS headers in Lambda response + enable CORS in API Gateway |
| Need to transform request/response | Use Mapping Templates (VTL) |
| Custom authorization logic | Use Lambda Authorizer |
| Real-time bidirectional communication | Use WebSocket API |
| Cost optimization for simple Lambda APIs | Use HTTP API instead of REST API |
| Cache stale data | Invalidate cache or reduce TTL |
| Auth changes not taking effect | Authorizer result is cached (reduce TTL or clear cache) |

---

## Quick Quiz

1. What's the difference between REST API and HTTP API?
2. How does Lambda Proxy Integration differ from non-proxy?
3. What are the three types of authorizers?
4. Why might CORS errors occur with Lambda + API Gateway?
5. What is a Lambda Authorizer's caching behavior?

---

[← Lambda](02-lambda.md) | [Back to Index](../../README.md) | [Next: DynamoDB →](04-dynamodb.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Create doc 01-aws-sdk.md
- [x] Create doc 02-lambda.md
- [ ] Create doc 03-api-gateway.md (writing now)
- [ ] Create remaining Domain 1 study guides (7 files)
- [ ] Create Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>