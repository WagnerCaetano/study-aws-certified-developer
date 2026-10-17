# Exercise 08: S3 Security

## Learning goals

- Author bucket policies for anonymous read of objects (not the bucket itself)
- Configure default bucket encryption with SSE-S3 vs SSE-KMS
- Define CORS rules for browser uploads and downloads

## Problem

Fix the S3 security helpers in `starter.py`.

The helpers should:

1. **Public read policy** — `Principal: "*"`, action `s3:GetObject`, resource `arn:aws:s3:::bucket-name/*`
2. **Encryption** — default SSE-S3 (`AES256`) when no KMS ARN; with a KMS ARN use `aws:kms` and `KMSMasterKeyID`
3. **CORS** — allow `GET`, `PUT`, and `POST`, plus `ExposeHeaders` including `ETag` and `MaxAgeSeconds` of 3600

## Exam tip

**Block Public Access** settings override bucket policies—exam questions often ask whether a policy alone is enough to expose objects (usually you must adjust BPA or use CloudFront OAC instead).

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/08-s3-security
python runner.py exercises/08-s3-security --solution
```
