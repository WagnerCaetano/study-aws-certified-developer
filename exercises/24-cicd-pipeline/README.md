# Exercise 24: CI/CD Pipeline

## Learning goals

- Structure CodeBuild **buildspec** files (`version: 0.2`, install/pre_build/build/post_build phases)
- Configure CodePipeline **Source** actions for CodeCommit
- Pick deployment strategies: Lambda canary, ECS blue/green, and all-at-once

## Problem

Fix the CI/CD configuration helpers in `starter.py`.

Buildspec version must be `0.2`. Source actions use category **Source** (not Build). Deployment strategy logic should return `Canary10Percent5Minutes` for zero-downtime Lambda, `BLUE_GREEN` for ECS, and `ALL_AT_ONCE` when downtime is acceptable.

## Exam tip

**CodePipeline** stages chain actions; artifacts flow between stages. **CodeDeploy** deployment configs for Lambda include canary and linear strategies. CodeBuild runs the buildspec phases in order—tests usually belong in `pre_build` or `build`.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/24-cicd-pipeline
python runner.py exercises/24-cicd-pipeline --solution
```
