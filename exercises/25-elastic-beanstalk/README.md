# Exercise 25: Elastic Beanstalk

## Learning goals

- Choose EB deployment policies: AllAtOnce, Rolling, RollingWithAdditionalBatch, Immutable
- Structure `.ebextensions` config documents with `option_settings` and `Resources`
- Set load balancer health check options in the correct namespace

## Problem

Fix the Elastic Beanstalk helpers in `starter.py`.

Deployment recommendations must match zero-downtime and capacity constraints. Health checks belong under `aws:elasticbeanstalk:environment:process:default` for path and interval—not the health reporting namespace.

## Exam tip

**Immutable** deployments launch a fresh batch before draining old instances—best for zero downtime without extra capacity. **RollingWithAdditionalBatch** adds capacity during rolling updates. `.ebextensions` files are YAML applied at environment launch/update.

## Run

Edit `starter.py`, then verify your work:

```bash
python runner.py exercises/25-elastic-beanstalk
python runner.py exercises/25-elastic-beanstalk --solution
```
