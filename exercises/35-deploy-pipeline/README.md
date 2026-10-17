# Exercise 35: Deployment Pipeline

## Learning goals

- Structure CodePipeline stages: **Source** (CodeCommit) → **Build** (CodeBuild) → **Deploy** (CloudFormation)
- Author a CodeBuild **buildspec** 0.2 with install, test, build, and package phases
- Diagnose pipeline failures from stage name and error text

## Problem

Fix the CI/CD helpers in `starter.py`.

1. **`build_codepipeline_config`**: Include a third **Deploy** stage using **CloudFormation** and the target stack name.
2. **`build_buildspec_advanced`**: Use version **0.2**; run **tests in `pre_build`**, SAM build in **`build`**, package in **`post_build`**.
3. **`determine_pipeline_stage`**: Map Source/Build/Deploy failures to actionable messages (tests vs IAM vs template errors).

## Exam tip

CodePipeline needs service roles with permissions for each stage action. CloudFormation deploy actions often require `CAPABILITY_IAM` when templates create roles.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/35-deploy-pipeline
python runner.py exercises/35-deploy-pipeline --solution
```
