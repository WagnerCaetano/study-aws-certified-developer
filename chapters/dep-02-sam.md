# AWS SAM (Serverless Application Model)

> **Domain 3: Deployment** | [← CloudFormation](01-cloudformation.md) | [Back to Index](../../README.md) | [Next: CI/CD →](03-cicd.md)

---

## Overview

AWS SAM is an extension of CloudFormation **simplified for serverless applications**.

### SAM vs CloudFormation

| Feature | CloudFormation | SAM |
|---------|---------------|-----|
| Lambda definition | Verbose (50+ lines) | Simplified (10 lines) |
| API Gateway | Manual resource | Implicit HTTP events |
| Local testing | No | **Yes** (sam local) |
| Build & package | Manual | `sam build` / `sam package` |

---

## SAM Template Example

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: My Serverless Application

Globals:
  Function:
    Runtime: python3.11
    Timeout: 30
    Environment:
      Variables:
        STAGE: !Ref Stage

Parameters:
  Stage:
    Type: String
    Default: dev

Resources:
  # Lambda Function
  GetItemsFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/get_items/
      Handler: app.handler
      Events:
        GetItems:
          Type: HttpApi
          Properties:
            Path: /items
            Method: get
            ApiId: !Ref MyApi
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref ItemsTable

  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/create_item/
      Handler: app.handler
      Events:
        CreateItem:
          Type: HttpApi
          Properties:
            Path: /items
            Method: post
            ApiId: !Ref MyApi
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable

  # HTTP API Gateway
  MyApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: !Ref Stage
      Auth:
        DefaultAuthorizer: MyCognitoAuth
        Authorizers:
          MyCognitoAuth:
            UserPoolArn: !GetAtt MyUserPool.Arn

  # DynamoDB Table
  ItemsTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      PrimaryKey:
        Name: itemId
        Type: String
      TableName: !Sub 'items-${Stage}'

  # Cognito User Pool
  MyUserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !Sub 'my-app-${Stage}'

Outputs:
  ApiEndpoint:
    Value: !Sub 'https://${MyApi}.execute-api.${AWS::Region}.amazonaws.com/${Stage}'
```

---

## SAM Resource Types

| SAM Type | Replaces |
|----------|----------|
| `AWS::Serverless::Function` | Lambda + IAM Role + Events |
| `AWS::Serverless::Api` | API Gateway (REST) |
| `AWS::Serverless::HttpApi` | API Gateway (HTTP) |
| `AWS::Serverless::SimpleTable` | DynamoDB Table |
| `AWS::Serverless::LayerVersion` | Lambda Layer |

---

## SAM Policy Templates

```yaml
Policies:
  - DynamoDBCrudPolicy:
      TableName: !Ref MyTable
  - S3ReadPolicy:
      BucketName: !Ref MyBucket
  - SQSPollerPolicy:
      QueueName: !Ref MyQueue
  - CloudWatchPutMetricPolicy: {}
```

---

## SAM CLI Commands

```bash
# Initialize a new project
sam init --runtime python3.11 --name my-app

# Build (install dependencies)
sam build

# Local invoke
sam local invoke GetItemsFunction

# Local API testing
sam local start-api

# Package (upload code to S3)
sam package --s3-bucket my-deployment-bucket --output-template-file packaged.yaml

# Deploy
sam deploy --guided  # First time (interactive)
sam deploy            # Subsequent deploys

# One-line deploy
sam deploy --capabilities CAPABILITY_IAM
```

---

## SAM with Layers

```yaml
MyLayer:
  Type: AWS::Serverless::LayerVersion
  Properties:
    LayerName: my-shared-layer
    ContentUri: layers/shared/
    CompatibleRuntimes:
      - python3.11

MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    CodeUri: src/
    Handler: app.handler
    Layers:
      - !Ref MyLayer
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Deploy serverless app quickly | Use SAM |
| Test Lambda locally | Use `sam local invoke` |
| Simplify Lambda + API Gateway | Use SAM `Events` property |
| Share code between functions | Use SAM Layers |
| Package for deployment | `sam package` uploads to S3 |
| Need DynamoDB policy | Use SAM Policy Templates |

---

[← CloudFormation](01-cloudformation.md) | [Back to Index](../../README.md) | [Next: CI/CD →](03-cicd.md)
