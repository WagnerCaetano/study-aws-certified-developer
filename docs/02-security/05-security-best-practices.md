# Security Best Practices

> **Domain 2: Security** | [← Secrets](04-secrets.md) | [Back to Index](../../README.md) | [Next: CloudFormation →](../03-deployment/01-cloudformation.md)

---

## Security Checklist for AWS Developers

### 1. IAM Security
- ✅ Use **least privilege** — Grant minimum permissions needed
- ✅ Use **roles** instead of access keys for services (Lambda, EC2, ECS)
- ✅ Enable **MFA** for all IAM users
- ✅ **Rotate access keys** regularly (every 90 days)
- ✅ Use **IAM Access Analyzer** to find overly permissive policies
- ✅ Never embed credentials in code or environment variables (use Secrets Manager)

### 2. Data Protection
- ✅ **Encrypt data at rest** — S3 (SSE-KMS), DynamoDB, EBS, RDS
- ✅ **Encrypt data in transit** — Use HTTPS/TLS for all communications
- ✅ Use **customer-managed KMS keys** when you need key policy control
- ✅ Store secrets in **Secrets Manager** (with rotation) or **SSM Parameter Store**
- ✅ Use **envelope encryption** for large data encryption

### 3. Network Security
- ✅ Use **VPC** for resources that need network isolation
- ✅ Use **Security Groups** (stateful) and **NACLs** (stateless) for access control
- ✅ Use **VPC endpoints** for private AWS service access
- ✅ **Lambda in VPC** needs NAT Gateway for internet access
- ✅ Use **WAF** for web application protection

### 4. Application Security
- ✅ Validate all **input** to prevent injection attacks
- ✅ Use **Cognito** for user authentication in web/mobile apps
- ✅ Implement **CORS** properly
- ✅ Use **API Gateway** with authorization (Cognito, Lambda, IAM)
- ✅ **Never log sensitive data** (passwords, tokens, PII)

### 5. Monitoring & Auditing
- ✅ Use **CloudTrail** to log all API calls
- ✅ Use **CloudWatch** for monitoring and alerting
- ✅ Use **X-Ray** for distributed tracing
- ✅ Use **AWS Config** for resource compliance
- ✅ Enable **GuardDuty** for threat detection

---

## Security in the SDLC

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   Code   │──►│  Build   │──►│  Deploy  │──►│  Runtime │
│          │   │          │   │          │   │          │
│ • Scan   │   │ • Secrets│   │ • IAM    │   │ • Monitor│
│   code   │   │   scan   │   │   least  │   │ • GuardDuty│
│ • Dep    │   │ • SAST   │   │   priv.  │   │ • WAF    │
│   check  │   │ • Sign   │   │ • Enc.   │   │ • Logging│
│          │   │   artifacts│  │          │   │ • Patch  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

---

## Common Exam Security Topics

| Topic | Key Point |
|-------|-----------|
| **Shared Responsibility** | AWS secures infrastructure; you secure your data and access |
| **IAM vs Resource policies** | IAM = identity permissions; Resource = who can access resource |
| **KMS key policies** | Must explicitly grant access; default gives root only |
| **S3 encryption** | SSE-S3 (default), SSE-KMS (audit/control), SSE-C (customer keys) |
| **Secrets Manager vs Parameter Store** | Auto-rotation vs cost-free |
| **Cognito User vs Identity Pools** | Auth/user management vs AWS credentials |
| **Lambda security** | Execution role + resource-based policies |
| **API Gateway auth** | Cognito, IAM, Lambda authorizer, JWT |
| **VPC security** | Security groups + NACLs |
| **CloudTrail** | Logs all API calls for audit |

---

## Quick Quiz

1. What is the principle of least privilege?
2. How do you securely provide database credentials to Lambda?
3. What's the difference between Security Groups and NACLs?
4. How does CloudTrail help with security auditing?

---

[← Secrets](04-secrets.md) | [Back to Index](../../README.md) | [Next: CloudFormation →](../03-deployment/01-cloudformation.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [ ] Create Domain 3 study guides (6 files)
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>