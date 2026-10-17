# Exercise 23: SAM Templates

## Learning goals

- Define `AWS::Serverless::Function` resources with runtime, handler, and `CodeUri`
- Wire **Api** events for HTTP routes
- Assemble SAM templates with `Transform: AWS::Serverless-2016-10-31` and optional `Globals`

## Problem

Fix the SAM template builders in `starter.py`.

Functions must use type `AWS::Serverless::Function`. API events use type `Api` (not `HttpApi` for this exercise). Full templates must include the SAM transform and merge function resources into `Resources`.

## Exam tip

SAM **Globals** apply defaults to all functions (timeout, memory, environment). `sam build` and `sam deploy` package artifacts and deploy the transformed CloudFormation stack—know the difference from raw CFN templates.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/23-sam-templates
python runner.py exercises/23-sam-templates --solution
```
