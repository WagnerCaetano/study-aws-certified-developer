# AWS CloudFormation

> **Domain 3: Deployment** | [← Security Best Practices](../02-security/05-security-best-practices.md) | [Back to Index](../../README.md) | [Next: SAM →](02-sam.md)

---

## Overview

AWS CloudFormation provisions AWS infrastructure using **declarative templates** (YAML/JSON).

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Template** | YAML/JSON file describing resources |
| **Stack** | Instantiated template (running resources) |
| **Stack Set** | Stacks across multiple accounts/regions |
| **Change Set** | Preview of changes before applying |
| **Drift Detection** | Detect manual changes outside CloudFormation |

---

## Template Anatomy

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'My Serverless Application'

Parameters:
  Stage:
    Type: String
    Default: dev
    AllowedValues: [dev, prod]

Mappings:
  RegionMap:
    us-east-1:
      AMI: ami-0abcdef1234567890
    us-west-2:
      AMI: ami-0fedcba0987654321

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'my-app-${Stage}-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled

  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub 'my-function-${Stage}'
      Runtime: python3.11
      Handler: index.handler
      Code:
        ZipFile: |
          def handler(event, context):
              return {'statusCode': 200, 'body': 'Hello!'}
      Role: !GetAtt FunctionRole.Arn

  FunctionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

Outputs:
  BucketName:
    Value: !Ref MyBucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'
  FunctionArn:
    Value: !GetAtt MyFunction.Arn
```

---

## Intrinsic Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `!Ref` | Reference a resource/parameter | `!Ref MyBucket` |
| `!GetAtt` | Get attribute of a resource | `!GetAtt MyFunction.Arn` |
| `!Sub` | Substitute variables | `!Sub 'arn:aws:s3:::${BucketName}'` |
| `!Join` | Join values with delimiter | `!Join [':', ['a', 'b']]` |
| `!Select` | Select from list by index | `!Select [0, !Ref List]` |
| `!Split` | Split string into list | `!Split [',', 'a,b,c']` |
| `!If` | Conditional | `!If [Condition, TrueVal, FalseVal]` |
| `!Equals` | Compare values | `!Equals [!Ref Stage, 'prod']` |
| `!ImportValue` | Reference exported output | `!ImportValue OtherStack-BucketName` |

---

## CloudFormation CLI

```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Create stack
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=Stage,ParameterValue=prod \
  --capabilities CAPABILITY_IAM

# Update stack
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# Create change set (preview changes)
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name my-changes \
  --template-body file://template.yaml

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# Check drift
aws cloudformation detect-stack-drift --stack-name my-stack
```

---

## Nested Stacks & Cross-Stack References

### Nested Stacks
```yaml
Resources:
  NetworkStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/network.yaml
      Parameters:
        VpcCidr: 10.0.0.0/16
```

### Cross-Stack References
```yaml
# Stack A - Output
Outputs:
  BucketName:
    Value: !Ref MyBucket
    Export:
      Name: MyApp-BucketName

# Stack B - Import
Resources:
  MyFunction:
    Properties:
      Environment:
        Variables:
          BUCKET: !ImportValue MyApp-BucketName
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Infrastructure as Code | Use CloudFormation templates |
| Preview changes before applying | Use Change Sets |
| Reuse templates across environments | Use Parameters |
| Cross-stack resource reference | Use Outputs + ImportValue |
| Detect manual configuration changes | Use Drift Detection |
| Deploy to multiple accounts | Use StackSets |
| Need custom resource logic | Use Custom Resources with Lambda |

---

[← Security Best Practices](../02-security/05-security-best-practices.md) | [Back to Index](../../README.md) | [Next: SAM →](02-sam.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3: 01-cloudformation.md
- [ ] Domain 3: 02-sam.md, 03-cicd.md, 04-elastic-beanstalk.md, 05-codedeploy.md, 06-cdk.md
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>