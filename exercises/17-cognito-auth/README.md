# Exercise 17: Cognito Authentication

## Learning goals

- Configure a Cognito User Pool with password policy and email verification
- Set up an app client for OAuth authorization code flow
- Parse JWT claims from API Gateway Cognito authorizers
- Link a User Pool to a Cognito Identity Pool for AWS credentials

## Problem

Fix the Cognito authentication flow helpers in `starter.py`.

The code should:

1. Auto-verify **email** on the user pool
2. Use OAuth flow `code` (authorization code) on the app client
3. Read claims from `event['requestContext']['authorizer']['claims']`
4. Disallow unauthenticated identities on the identity pool

## Exam tip

User Pools authenticate users; Identity Pools exchange tokens for temporary AWS credentials. Hosted UI and authorization code flow are preferred over implicit flow for web apps.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/17-cognito-auth
python runner.py exercises/17-cognito-auth --solution
```
