# Exercise 19: Secrets Management

## Learning goals

- Structure JSON secrets and choose Secrets Manager vs Parameter Store
- Store/retrieve secrets and SSM parameters on LocalStack
- Reference secrets in ECS task definitions with `valueFrom`

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `secretsmanager`, `ssm`

**Cleanup:** tests force-delete secrets and delete parameters. Use `docker compose down` to stop LocalStack.

## Problem

Fix `starter.py`:

1. Serialize DB credentials with `port` as a **string**
2. Honor `SecureString` + `KeyId` in `build_ssm_parameter`
3. Recommend Secrets Manager for rotation/DB; Parameter Store when cost-sensitive
4. ECS refs use `valueFrom`
5. **store_secret** / **get_secret_string** — return ARN / SecretString
6. **put_parameter** / **get_parameter_value** — real SSM calls with `WithDecryption`

## Exam tip

Secrets Manager supports **automatic rotation** (especially RDS). Parameter Store Standard params are cheaper. Never hardcode credentials in Lambda/ECS — pull at runtime via IAM.

## Run

```bash
docker compose up -d
python runner.py exercises/19-secrets
python runner.py exercises/19-secrets --solution
```
