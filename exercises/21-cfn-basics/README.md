# Exercise 21: CloudFormation Basics

## Learning goals

- Build valid CloudFormation templates with `AWSTemplateFormatVersion`, `Resources`, and `Outputs`
- Model `AWS::Lambda::Function` with S3-based deployment packages
- Configure `AWS::S3::Bucket` with versioning enabled

## Problem

Fix the CloudFormation template builders in `starter.py`.

Lambda templates need format version `2010-09-09`, the correct resource type, and a `FunctionArn` output using `Fn::GetAtt`. S3 templates need versioning `Enabled` and a `BucketName` output.

## Exam tip

CloudFormation **Outputs** with `Export` enable cross-stack references via `Fn::ImportValue`. Lambda code in templates usually references **S3** (`Code.S3Bucket` / `S3Key`) or uses SAM/CDK for packaging.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/21-cfn-basics
python runner.py exercises/21-cfn-basics --solution
```
