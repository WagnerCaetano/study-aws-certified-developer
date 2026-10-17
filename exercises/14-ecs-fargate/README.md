# Exercise 14: ECS & Fargate

## Learning goals

- Define Fargate-compatible task definitions (`awsvpc`, CPU/memory as strings)
- Configure an ECS service with Fargate launch type and awsvpc networking
- Reference valid Fargate CPU and memory pairings

## Problem

Fix the ECS task definition and service configuration in `starter.py`.

The code should:

1. Use `networkMode: awsvpc`, `requiresCompatibilities: ['FARGATE']`, and string CPU/memory values
2. Set service `launchType` to `FARGATE` (not EC2)
3. Keep awsvpc subnet and security group configuration on the service

## Exam tip

Fargate tasks need an **execution role** (pull images, write logs) and often a **task role** (app AWS API access). CPU and memory must match AWS-documented Fargate combinations.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/14-ecs-fargate
python runner.py exercises/14-ecs-fargate --solution
```
