# AWS Elastic Beanstalk

> **Domain 3: Deployment** | [← CI/CD](03-cicd.md) | [Back to Index](../../README.md) | [Next: AWS CDK →](05-cdk.md)

---

## Overview

Elastic Beanstalk is a **Platform as a Service (PaaS)** that automatically deploys, scales, and manages web applications.

### Supported Platforms
- Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker
- Multi-container Docker (ECS), GlassFish, Tomcat

---

## Architecture

```
┌────────────────────────────────────────────────────┐
│  Elastic Beanstalk Environment                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   ELB    │─►│ Auto     │─►│  EC2 Instances   │ │
│  │(Load     │  │ Scaling  │  │  (with your app) │ │
│  │ Balancer)│  │ Group    │  │                  │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
│       │                              │              │
│       ▼                              ▼              │
│  ┌──────────┐                  ┌──────────────┐    │
│  │Route 53  │                  │  RDS / Elasti │    │
│  │(DNS)     │                  │  Cache (opt)  │    │
│  └──────────┘                  └──────────────┘    │
└────────────────────────────────────────────────────┘
```

---

## Deployment Policies

| Policy | Description | Impact |
|--------|-------------|--------|
| **All at once** | Deploy to all instances simultaneously | **Downtime** possible |
| **Rolling** | Deploy in batches | Reduced capacity during deploy |
| **Rolling with additional batch** | Launch new instances first | Full capacity maintained |
| **Immutable** | Launch new instances in new ASG | **Safest**, zero downtime |
| **Blue/Green** | Swap environment CNAME | Zero downtime, quick rollback |

---

## .ebextensions

```yaml
# .ebextensions/01-loadbalancer.config
option_settings:
  aws:elasticbeanstalk:environment:
    LoadBalancerType: application
  aws:elasticbeanstalk:environment:process:default:
    HealthCheckPath: /health
    Port: 8080

# Custom resources
Resources:
  MyDB:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: postgres
      DBInstanceClass: db.t3.micro
      AllocatedStorage: 20
```

---

## CLI Commands

```bash
# Create application
eb init -p python-3.11 my-app

# Create environment
eb create production --scale 2

# Deploy new version
eb deploy production

# Check status
eb status

# Open in browser
eb open

# Terminate environment
eb terminate production
```

---

## Beanstalk vs Other Deployment Options

| Feature | Elastic Beanstalk | ECS/Fargate | Lambda |
|---------|------------------|-------------|--------|
| Management | PaaS (managed) | Container service | Serverless |
| Use case | Traditional web apps | Containerized apps | Event-driven |
| Scaling | Auto-scaling | Service auto-scaling | Automatic |
| Max timeout | Unlimited | Unlimited | 15 min |
| Cost | EC2 instances | Fargate tasks | Per invocation |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Quick web app deployment | Use Elastic Beanstalk |
| Zero-downtime deployment | Use Immutable or Blue/Green |
| Need to customize environment | Use .ebextensions |
| Traditional web app (Java, PHP) | Use Elastic Beanstalk |
| Container orchestration needed | Use ECS (not Beanstalk) |
| Need full server control | Use EC2 with CloudFormation |

---

[← CI/CD](03-cicd.md) | [Back to Index](../../README.md) | [Next: AWS CDK →](05-cdk.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3: 01-cloudformation.md, 02-sam.md, 03-cicd.md, 04-elastic-beanstalk.md
- [ ] Domain 3: 05-cdk.md
- [ ] Create Domain 4 study guides (4 files)
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>