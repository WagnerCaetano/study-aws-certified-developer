# CI/CD on AWS

> **Domain 3: Deployment** | [← SAM](02-sam.md) | [Back to Index](../../README.md) | [Next: Elastic Beanstalk →](04-elastic-beanstalk.md)

---

## Overview

AWS provides several services for building **continuous integration and continuous deployment** pipelines.

### Service Overview

| Service | Purpose |
|---------|---------|
| **CodeCommit** | Source code repository (Git) |
| **CodeBuild** | Build and test service |
| **CodeDeploy** | Deploy to EC2, Lambda, ECS |
| **CodePipeline** | Orchestrate CI/CD pipelines |
| **CodeArtifact** | Package repository (npm, Maven, PyPI) |
| **CodeStar** | Quick project setup |

---

## CodePipeline Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Source     │──►│   Build      │──►│   Test       │──►│   Deploy     │
│  (CodeCommit │   │  (CodeBuild) │   │  (CodeBuild) │   │ (CodeDeploy/ │
│   GitHub,    │   │              │   │              │   │  CloudForm.) │
│   S3)        │   │              │   │              │   │              │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

### Pipeline Definition (CloudFormation)

```yaml
MyPipeline:
  Type: AWS::CodePipeline::Pipeline
  Properties:
    RoleArn: !GetAtt PipelineRole.Arn
    ArtifactStore:
      Type: S3
      Location: !Ref ArtifactBucket
    Stages:
      - Name: Source
        Actions:
          - Name: SourceAction
            ActionTypeId:
              Category: Source
              Owner: AWS
              Provider: CodeCommit
              Version: '1'
            Configuration:
              RepositoryName: my-repo
              BranchName: main
            OutputArtifacts:
              - Name: SourceCode

      - Name: Build
        Actions:
          - Name: BuildAction
            ActionTypeId:
              Category: Build
              Owner: AWS
              Provider: CodeBuild
              Version: '1'
            InputArtifacts:
              - Name: SourceCode
            OutputArtifacts:
              - Name: BuiltCode
            Configuration:
              ProjectName: !Ref BuildProject

      - Name: Deploy
        Actions:
          - Name: DeployAction
            ActionTypeId:
              Category: Deploy
              Owner: AWS
              Provider: CloudFormation
              Version: '1'
            InputArtifacts:
              - Name: BuiltCode
            Configuration:
              ActionMode: REPLACE_ON_FAILURE
              StackName: my-app
              TemplatePath: BuiltCode::packaged.yaml
              Capabilities: CAPABILITY_IAM
```

---

## CodeBuild

### buildspec.yml

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - pip install -r requirements.txt
  pre_build:
    commands:
      - python -m pytest tests/
  build:
    commands:
      - sam build
      - sam package --s3-bucket $ARTIFACT_BUCKET --output-template-file packaged.yaml
  post_build:
    commands:
      - echo "Build complete!"
artifacts:
  type: zip
  files:
    - packaged.yaml
```

---

## CodeDeploy for Lambda

### Deployment Configurations

| Config | Description |
|--------|-------------|
| **Canary10PercentXMinutes** | Shift 10% traffic, wait X minutes, then 100% |
| **Linear10PercentXMinutes** | Shift 10% every X minutes |
| **AllAtOnce** | Shift all traffic immediately |

### AppSpec for Lambda

```yaml
version: 0.0
Resources:
  - MyFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: my-function
        Alias: live
        CurrentVersion: 1
        TargetVersion: 2
```

### Traffic Shifting with Pre/Post Hooks

```yaml
Hooks:
  BeforeAllowTraffic: !Ref PreTrafficHook
  AfterAllowTraffic: !Ref PostTrafficHook
```

---

## CodeDeploy for ECS

### Deployment Types
- **Blue/Green** — New tasks created, traffic switched via LB
- Uses **CodeDeploy** with ECS integration

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Build CI/CD pipeline | Use CodePipeline + CodeBuild + CodeDeploy |
| Run tests in pipeline | Use CodeBuild with buildspec.yml |
| Canary deployment for Lambda | Use CodeDeploy with Canary10Percent |
| Blue/Green for ECS | Use CodeDeploy with ECS |
| Deploy SAM application | Use CodePipeline with CloudFormation deploy action |
| Source code management | Use CodeCommit or GitHub |
| Store build artifacts | Use S3 as artifact store |

---

[← SAM](02-sam.md) | [Back to Index](../../README.md) | [Next: Elastic Beanstalk →](04-elastic-beanstalk.md)
