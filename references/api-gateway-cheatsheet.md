# API Gateway Cheatsheet

Quick reference for Amazon API Gateway (REST / HTTP / WebSocket) on DVA-C02.

## API types

| Type | When to use |
|------|-------------|
| **REST API** | Full features: API keys, usage plans, request validation, WAF, canary |
| **HTTP API** | Lower cost/latency; JWT/Cognito/IAM; simpler |
| **WebSocket API** | Persistent bidirectional (chat, push) |

## Integrations

| Integration | Behavior |
|-------------|----------|
| Lambda proxy | API Gateway passes full request; Lambda returns `statusCode` / `headers` / `body` |
| Lambda non-proxy | Mapping templates transform request/response |
| HTTP / HTTP_PROXY | Forward to HTTP backend |
| AWS service | Direct integrate (e.g. SQS, DynamoDB) via IAM |
| MOCK | No backend; useful for CORS OPTIONS |

## Auth options

| Method | Notes |
|--------|-------|
| Cognito User Pool authorizer | Validate JWT from User Pool |
| IAM (SigV4) | Caller signs with AWS credentials |
| Lambda authorizer | Custom token/request auth; cacheable |
| JWT authorizer (HTTP API) | OIDC/JWT without Cognito-only |
| API keys + usage plans | Quotas/throttling — **not** strong auth alone |
| Resource policy | IP, VPC, account allow/deny |

## Stages, throttling, caching

| Topic | Key point |
|-------|-----------|
| Stage | Deployment snapshot (`dev`, `prod`) |
| Stage variables | Config per stage |
| Throttle | Account/stage/method limits; burst + rate |
| Usage plans | Bind API keys to quotas |
| Cache | REST stage cache; TTL; encryption optional |
| Canary | Shift % of traffic to new deployment |

## CORS & errors

| Topic | Key point |
|-------|-----------|
| CORS | Enable on API; OPTIONS MOCK or gateway response |
| Gateway responses | Customize 4xx/5xx from API Gateway itself |
| Lambda errors | Proxy: map status in Lambda response body |

## Exam tips

- Prefer **Lambda proxy** unless you need mapping templates.
- **HTTP API** ≠ full REST feature set (no usage plans/API keys the same way).
- Protect backends with **least-privilege IAM** on the integration role.
- Know difference between **authorizer failure** (401/403) vs **integration failure** (502/504).

## Related

- Chapter: [dev-03-api-gateway.md](../chapters/dev-03-api-gateway.md)
- Exercises: [04-api-gateway](../exercises/04-api-gateway/), [31-serverless-api](../exercises/31-serverless-api/)
- Lab (when available): [labs/01-serverless-api](../labs/01-serverless-api/)
