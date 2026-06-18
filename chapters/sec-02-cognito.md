# Amazon Cognito

> **Domain 2: Security** | [← IAM](01-iam.md) | [Back to Index](../../README.md) | [Next: KMS →](03-kms.md)

---

## Overview

Amazon Cognito provides **authentication, authorization, and user management** for web and mobile apps.

### Two Main Components

| Component | Purpose |
|-----------|---------|
| **User Pools** | Sign-up, sign-in, user management, JWT tokens |
| **Identity Pools** | Temporary AWS credentials for accessing AWS resources |

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  User Pool   │────►│  JWT Token    │────►│  API Gateway │
│  (Auth)      │     │  (ID/Access)  │     │  (Verify)    │
└──────────────┘     └───────────────┘     └──────────────┘

┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Identity Pool│────►│ STS Temp      │────►│  AWS Services│
│ (Federation) │     │ Credentials   │     │  (S3, etc.)  │
└──────────────┘     └───────────────┘     └──────────────┘
```

---

## User Pools

### Features
- User registration and sign-in
- **JWT tokens** (ID, Access, Refresh)
- Password reset, MFA, account verification
- Social identity providers (Google, Facebook, Apple, Amazon)
- SAML and OIDC federation
- Custom authentication flows (Lambda triggers)

### Sign-In Flow

```
1. User enters credentials
2. Cognito validates
3. Returns JWT tokens:
   ├── ID Token (user attributes)
   ├── Access Token (permissions)
   └── Refresh Token (get new tokens)
```

### Token Types

| Token | Purpose | Lifetime |
|-------|---------|----------|
| **ID Token** | Contains user claims (name, email, etc.) | 1 hour (configurable) |
| **Access Token** | Authorizes API calls | 1 hour (configurable) |
| **Refresh Token** | Get new ID/Access tokens | 30 days (configurable) |

### Lambda Triggers

| Trigger | When |
|---------|------|
| Pre Sign-up | Before registration |
| Post Confirmation | After email/phone verification |
| Pre Authentication | Before sign-in |
| Post Authentication | After successful sign-in |
| Custom Message | Customize verification/welcome emails |
| Token Generation | Modify token claims |
| User Migration | Migrate users from existing system |

### Code Examples

```javascript
// AWS SDK - Sign up
import { CognitoIdentityProviderClient, SignUpCommand } from '@aws-sdk/client-cognito-identity-provider';

const client = new CognitoIdentityProviderClient({});

await client.send(new SignUpCommand({
  ClientId: 'your-client-id',
  Username: 'user@example.com',
  Password: 'SecurePass123!',
  UserAttributes: [
    { Name: 'email', Value: 'user@example.com' }
  ]
}));
```

```python
# Python - Verify JWT from Cognito
import jwt
import requests

def verify_cognito_token(token, user_pool_id):
    # Get public keys
    url = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
    keys = requests.get(url).json()['keys']
    
    # Decode and verify
    header = jwt.get_unverified_header(token)
    kid = header['kid']
    key = next(k for k in keys if k['kid'] == kid)
    
    decoded = jwt.decode(token, key, algorithms=['RS256'])
    return decoded
```

---

## Identity Pools (Federated Identities)

### Features
- Provide temporary AWS credentials
- Support unauthenticated (guest) access
- Federation with: Cognito User Pools, social providers, SAML, OIDC, developer auth

### Flow

```
1. User authenticates (User Pool, Google, Facebook, etc.)
2. Identity Pool exchanges token for AWS credentials
3. User accesses AWS resources with temporary credentials
4. Permissions controlled via IAM roles
```

### Role Mapping

```json
{
  "RulesConfiguration": {
    "Rules": [
      {
        "Claim": "cognito:preferred_role",
        "MatchValue": "Admin",
        "RoleARN": "arn:aws:iam::123456789012:role/AdminRole"
      }
    ]
  }
}
```

---

## Cognito with API Gateway

```javascript
// API Gateway config
{
  "AuthorizationType": "COGNITO_USER_POOLS",
  "AuthorizerId": "abc123"
}

// Client sends: Authorization: Bearer <id_token>
```

**Important:** Use the **ID Token** (not Access Token) for API Gateway Cognito authorization.

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Add user authentication to web app | Use Cognito User Pools |
| Give app users temporary AWS credentials | Use Cognito Identity Pools |
| Customize sign-up flow | Use Lambda triggers |
| Social login (Google/Facebook) | Configure in User Pool |
| Protect API Gateway with Cognito | Use Cognito User Pool authorizer |
| Migrate existing users | Use User Migration Lambda trigger |
| Different roles for different users | Use Identity Pool role mapping |

---

## Quick Quiz

1. What's the difference between User Pools and Identity Pools?
2. What tokens does Cognito issue?
3. Which token do you use with API Gateway?
4. How do you customize the authentication flow?

---

[← IAM](01-iam.md) | [Back to Index](../../README.md) | [Next: KMS →](03-kms.md)
