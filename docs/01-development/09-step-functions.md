# AWS Step Functions

> **Domain 1: Development with AWS Services** | [← ElastiCache](08-elasticache.md) | [Back to Index](../../README.md) | [Next: Containers →](10-containers.md)

---

## Overview

AWS Step Functions is a **serverless orchestration** service that lets you coordinate multiple AWS services into serverless workflows using **state machines**.

### Why Step Functions?
- Orchestrate Lambda functions in complex workflows
- Built-in error handling and retry logic
- Visual workflow editor
- Long-running workflows (up to 1 year)
- Replaces complex Lambda chains

---

## State Machine Types

| Type | Description | Duration |
|------|-------------|----------|
| **Standard** | Long-running, exactly-once execution | Up to 1 year |
| **Express** | High-throughput, short-duration | Up to 5 minutes |

| Feature | Standard | Express |
|---------|----------|---------|
| Execution rate | 2,000/second | 100,000+/second |
| Exactly-once | **Yes** | At-least-once |
| Visual execution | **Yes** | Limited |
| Cost | Per state transition | Per execution + duration |
| Use case | Long workflows, orchestration | High-volume, event processing |

---

## State Types

```
┌─────────────────────────────────────────────────────┐
│                  State Machine                       │
│                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│  │  Start  │───►│  Task   │───►│ Choice  │        │
│  └─────────┘    │(Lambda) │    │  (If)   │        │
│                 └─────────┘    └────┬────┘        │
│                                    │               │
│                              ┌─────┴─────┐        │
│                              ▼           ▼        │
│                        ┌─────────┐ ┌─────────┐   │
│                        │  Pass   │ │  Fail   │   │
│                        └─────────┘ └─────────┘   │
│                              │                     │
│                              ▼                     │
│                        ┌─────────┐                │
│                        │   End   │                │
│                        └─────────┘                │
└─────────────────────────────────────────────────────┘
```

| State Type | Description |
|-----------|-------------|
| **Task** | Execute work (Lambda, ECS, SNS, SQS, etc.) |
| **Choice** | Branch based on input (if/else) |
| **Pass** | Pass input to output (transform) |
| **Wait** | Delay for a specified time |
| **Succeed** | End execution successfully |
| **Fail** | End execution with error |
| **Parallel** | Execute branches in parallel |
| **Map** | Process array items in parallel |

---

## ASL (Amazon States Language) Example

```json
{
  "Comment": "Order Processing Workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:validateOrder",
      "Next": "CheckInventory"
    },
    "CheckInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:checkInventory",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2.0
      }],
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "OrderFailed"
      }],
      "Next": "InventoryChoice"
    },
    "InventoryChoice": {
      "Type": "Choice",
      "Choices": [{
        "Variable": "$.inStock",
        "BooleanEquals": true,
        "Next": "ProcessPayment"
      }],
      "Default": "BackorderItem"
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:processPayment",
      "Next": "ShipOrder"
    },
    "ShipOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:shipOrder",
      "End": true
    },
    "BackorderItem": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:backorder",
      "End": true
    },
    "OrderFailed": {
      "Type": "Fail",
      "Error": "OrderFailed",
      "Cause": "Could not check inventory"
    }
  }
}
```

---

## Error Handling & Retries

```json
{
  "Type": "Task",
  "Resource": "arn:aws:lambda:region:account:function:myFunction",
  "Retry": [
    {
      "ErrorEquals": ["States.Timeout", "States.TaskFailed"],
      "IntervalSeconds": 3,
      "MaxAttempts": 3,
      "BackoffRate": 2.0,
      "JitterStrategy": "FULL"
    },
    {
      "ErrorEquals": ["States.ALL"],
      "IntervalSeconds": 5,
      "MaxAttempts": 2,
      "BackoffRate": 1.5
    }
  ],
  "Catch": [
    {
      "ErrorEquals": ["CustomError"],
      "Next": "HandleCustomError"
    },
    {
      "ErrorEquals": ["States.ALL"],
      "Next": "CatchAllFallback"
    }
  ],
  "Next": "SuccessState"
}
```

### Retry Parameters
- **IntervalSeconds** — Initial wait before first retry
- **MaxAttempts** — Maximum number of retries (0 = no retry)
- **BackoffRate** — Multiplier for each subsequent retry
- **JitterStrategy** — Add randomness to avoid thundering herd

---

## Parallel State

```json
{
  "Type": "Parallel",
  "Branches": [
    {
      "StartAt": "SendEmail",
      "States": {
        "SendEmail": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:region:account:function:sendEmail",
          "End": true
        }
      }
    },
    {
      "StartAt": "UpdateDatabase",
      "States": {
        "UpdateDatabase": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:region:account:function:updateDB",
          "End": true
        }
      }
    }
  ],
  "Next": "Finalize"
}
```

---

## Map State (Distributed Processing)

```json
{
  "Type": "Map",
  "ItemsPath": "$.orders",
  "MaxConcurrency": 5,
  "Iterator": {
    "StartAt": "ProcessOrder",
    "States": {
      "ProcessOrder": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:region:account:function:processOrder",
        "End": true
      }
    }
  },
  "Next": "AllOrdersComplete"
}
```

---

## Synchronous Express Workflows

```json
{
  "Type": "Task",
  "Resource": "arn:aws:states:us-east-1:123456789012:express:MyStateMachine",
  "ResourceType": "workflow",
  "End": true
}
```

- Can be started synchronously (wait for completion)
- Useful from Lambda, API Gateway, Step Functions

---

## Step Functions with SAM

```yaml
MyStateMachine:
  Type: AWS::Serverless::StateMachine
  Properties:
    DefinitionUri: statemachine/definition.asl.json
    Role: !GetAtt StateMachineRole.Arn
    Events:
      ApiEvent:
        Type: Api
        Properties:
          Path: /start-workflow
          Method: post
```

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Orchestrate Lambda functions | Use Step Functions |
| Need retry with backoff | Configure Retry in state machine |
| Branch based on conditions | Use Choice state |
| Process items in parallel | Use Map or Parallel state |
| Long-running workflow (> 15 min) | Use Standard Step Functions |
| High-volume short workflows | Use Express Step Functions |
| Workflow exceeds Lambda timeout | Use Step Functions |
| Need visual monitoring | Use Step Functions (Standard) |
| Coordinate 10+ microservices | Use Step Functions |

---

## Quick Quiz

1. What's the difference between Standard and Express workflows?
2. What state types are available in Step Functions?
3. How does retry with exponential backoff work?
4. When would you use a Map state?

---

[← ElastiCache](08-elasticache.md) | [Back to Index](../../README.md) | [Next: Containers →](10-containers.md)
