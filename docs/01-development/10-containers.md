# Containers: ECS, ECR & Fargate

> **Domain 1: Development with AWS Services** | [← Step Functions](09-step-functions.md) | [Back to Index](../../README.md) | [Next: IAM →](../02-security/01-iam.md)

---

## Overview

AWS container services let you run containerized applications without managing the underlying infrastructure.

### Service Map

```
┌─────────────────────────────────────────────────────┐
│  Container Services                                  │
│                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐│
│  │   ECR   │  │   ECS   │  │   EKS (Kubernetes)  ││
│  │Registry │  │(Container│  │   (managed K8s)     ││
│  │         │  │ Service) │  │                     ││
│  └─────────┘  └────┬────┘  └─────────────────────┘│
│                    │                                │
│              ┌─────┴─────┐                         │
│              │ Launch    │                         │
│              │ Type      │                         │
│              └─────┬─────┘                         │
│         ┌─────────┴─────────┐                      │
│         ▼                   ▼                      │
│  ┌─────────────┐   ┌─────────────┐                │
│  │   Fargate   │   │   EC2       │                │
│  │ (Serverless)│   │ (Managed)   │                │
│  └─────────────┘   └─────────────┘                │
└─────────────────────────────────────────────────────┘
```

---

## Amazon ECR (Elastic Container Registry)

### Overview
- Fully managed **Docker container registry**
- Store, manage, and deploy container images
- Integrated with ECS and EKS
- Supports image scanning for vulnerabilities

### CLI Operations

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name my-app

# Build, tag, and push
docker build -t my-app .
docker tag my-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest

# List images
aws ecr describe-images --repository-name my-app

# Delete image
aws ecr batch-delete-image \
  --repository-name my-app \
  --image-ids imageTag=latest
```

### ECR Policies
- **Private repositories** — Default, requires authentication
- **Public repositories** — Via ECR Public (gallery.ecr.aws)
- **Lifecycle policies** — Automate image cleanup (e.g., keep last 10 images)
- **Cross-account access** — Via resource-based policies

---

## Amazon ECS (Elastic Container Service)

### Key Concepts

```
┌──────────────────────────────────────────────────────┐
│  ECS Cluster                                         │
│  ┌────────────────────────────────────────────────┐  │
│  │  Service (manages desired count)               │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐      │  │
│  │  │  Task 1  │ │  Task 2  │ │  Task 3  │      │  │
│  │  │(Container│ │(Container│ │(Container│      │  │
│  │  │  s)      │ │  s)      │ │  s)      │      │  │
│  │  └──────────┘ └──────────┘ └──────────┘      │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

| Concept | Description |
|---------|-------------|
| **Cluster** | Logical grouping of resources |
| **Task Definition** | Blueprint for your container (like docker-compose) |
| **Task** | Running instance of a task definition |
| **Service** | Maintains desired number of tasks |
| **Container** | Individual Docker container within a task |

### Task Definition

```json
{
  "family": "my-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:latest",
      "essential": true,
      "portMappings": [
        {"containerPort": 8080, "protocol": "tcp"}
      ],
      "environment": [
        {"name": "STAGE", "value": "production"}
      ],
      "secrets": [
        {"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-password"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/my-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### ECS with Fargate vs EC2

| Feature | Fargate | EC2 |
|---------|---------|-----|
| Management | **Serverless** (no servers) | You manage EC2 instances |
| Scaling | Automatic | Manual or auto-scaling |
| Cost | Pay per task | Pay per EC2 instance |
| SSH access | No | Yes |
| Customization | Limited | Full control |
| Use case | Most workloads | Custom requirements, GPU |

### ECS CLI Commands

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-service \
  --task-definition my-app \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc],securityGroups=[sg-abc],assignPublicIp=ENABLED}"

# Update service (deploy new version)
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --task-definition my-app:2 \
  --force-new-deployment
```

---

## ECS Deployment Types

### Rolling Update (Default)
```
Old: [v1] [v1] [v1]
      ↓
New: [v1] [v1] [v2]  ← 1 new, 2 old
      ↓
New: [v1] [v2] [v2]  ← 2 new, 1 old
      ↓
New: [v2] [v2] [v2]  ← All new
```

### Blue/Green Deployment (with CodeDeploy)
```
Blue (current): [v1] [v1] [v1]  ← Original
Green (new):    [v2] [v2] [v2]  ← New version
                       │
              Traffic switched via LB
```

---

## Fargate Task Sizes

| CPU (vCPU) | Memory (GB) |
|------------|-------------|
| 0.25 | 0.5, 1, 2 |
| 0.5 | 1–4 |
| 1 | 2–8 |
| 2 | 4–16 |
| 4 | 8–30 |

---

## ECS with Application Load Balancer

```
┌──────────┐     ┌───────────────┐     ┌──────────────┐
│  Users   │────►│     ALB       │────►│  ECS Tasks   │
│          │     │  (Target Grp) │     │  (Fargate)   │
└──────────┘     └───────────────┘     └──────────────┘
```

- Use **target groups** to route to ECS tasks
- **Health checks** remove unhealthy tasks
- **Service discovery** via AWS Cloud Map or Route 53

---

## ECS IAM Roles

| Role | Purpose |
|------|---------|
| **Task Execution Role** | Pull images from ECR, write logs to CloudWatch |
| **Task Role** | Permissions for your application code (like Lambda role) |

```json
{
  "family": "my-app",
  "taskRoleArn": "arn:aws:iam::123456789012:role/my-app-task-role",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecs-task-execution-role"
}
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Run containers without managing servers | Use ECS with Fargate |
| Store container images | Use ECR |
| Need to deploy new version gradually | Use rolling update or blue/green |
| Container needs AWS permissions | Use Task Role |
| Pull private images securely | Use Task Execution Role + ECR |
| Need secrets in containers | Use Secrets Manager or SSM Parameter Store |
| Run Docker containers at scale | Use ECS Service with auto-scaling |
| Cost optimization | Use Fargate Spot for non-critical workloads |
| Need persistent storage | Use EFS with ECS |

---

## Quick Quiz

1. What's the difference between ECS Fargate and ECS on EC2?
2. What is the Task Execution Role vs Task Role?
3. How do you store and retrieve secrets in ECS?
4. What deployment strategies are available for ECS?

---

[← Step Functions](09-step-functions.md) | [Back to Index](../../README.md) | [Next: IAM →](../02-security/01-iam.md)
