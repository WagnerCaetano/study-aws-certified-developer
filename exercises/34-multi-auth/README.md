# Exercise 34: Multi-Service Authentication

## Learning goals

- Configure Cognito hosted UI / OAuth2 **authorization code** flow settings
- Validate JWT claims (`sub`, `cognito:groups`) for authorization
- Attach a **Cognito User Pool** authorizer to API Gateway

## Problem

Fix the auth helpers in `starter.py`.

1. **`build_auth_flow`**: Use **`response_type`: `code`** and scope including **`openid`** (with email/profile as needed).
2. **`validate_token_claims`**: When `required_groups` is set, succeed only if the user belongs to at least one required group.
3. **`build_api_gateway_authorizer`**: Authorizer **Type** must be **`COGNITO_USER_POOLS`**.

## Exam tip

Implicit flows (`response_type=token`) are discouraged; prefer authorization code with PKCE for SPAs. API Gateway Cognito authorizers validate JWTs from the user pool—group claims appear in `cognito:groups`.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/34-multi-auth
python runner.py exercises/34-multi-auth --solution
```

## Next: multi-service lab

This exercise is an **offline concept check** (Cognito / JWT / API authorizer). For the LocalStack multi-service **security** hands-on (Secrets Manager + SSM + KMS), continue with:

**[labs/04-secure-config](../../labs/04-secure-config/)**
