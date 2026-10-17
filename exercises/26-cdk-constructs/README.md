# Exercise 26: CDK Constructs

## Learning goals

- Distinguish CDK **L1** (CFN resources, `Cfn*`), **L2** (grants, lookups), and **L3** (patterns)
- Map CLI tasks to commands: `cdk synth`, `deploy`, `diff`, `destroy`, `list`, `init`
- Attach construct level metadata when building prop summaries

## Problem

Fix the CDK helpers in `starter.py`.

`Cfn*` constructs are L1; high-level APIs with `grant*` methods are L2; patterns and `RestApi`-style abstractions are L3. Map “Generate CloudFormation template” to `cdk synth` and “Deploy the stack” to `cdk deploy`.

## Exam tip

**cdk synth** produces CloudFormation JSON/YAML without deploying. L2 constructs generate IAM policies and sensible defaults—prefer them over raw L1 unless you need full CFN control.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/26-cdk-constructs
python runner.py exercises/26-cdk-constructs --solution
```
