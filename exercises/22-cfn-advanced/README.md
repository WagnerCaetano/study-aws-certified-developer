# Exercise 22: CloudFormation Advanced

## Learning goals

- Construct ARNs with the correct segment order (service, region, account, resource)
- Define template **Parameters** with `Default` and `AllowedValues`
- Build **Outputs** with `Export.Name` for cross-stack sharing
- Use intrinsic functions: `Ref`, `Fn::GetAtt`, `Fn::Sub`, `Fn::Join`, `Fn::ImportValue`

## Problem

Fix the CloudFormation helper functions in `starter.py`.

Parameters must use CloudFormation’s capitalized `Default` key. Outputs must nest exports under `Export.Name`. Intrinsic helpers must return the canonical JSON forms (`Ref`, `Fn::GetAtt`, etc.).

## Exam tip

**Fn::ImportValue** reads exported output names from other stacks—exports cannot be renamed without updating dependents. **Fn::GetAtt** returns resource attributes (for example Lambda `Arn`); **Ref** returns the logical ID or physical name depending on the resource type.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/22-cfn-advanced
python runner.py exercises/22-cfn-advanced --solution
```
