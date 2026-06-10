# AWS X-Ray

> **Domain 4: Monitoring & Troubleshooting** | [← CloudTrail](02-cloudtrail.md) | [Back to Index](../../README.md) | [Next: Troubleshooting →](04-troubleshooting.md)

---

## Overview

AWS X-Ray helps developers **analyze and debug** distributed applications (microservices).

### What X-Ray Does
- Trace requests across multiple services
- Map service dependencies (service map)
- Identify performance bottlenecks
- Debug errors across service boundaries

---

## X-Ray Concepts

```
┌──────────────────────────────────────────────────────┐
│  Request Flow (Trace)                                 │
│                                                      │
│  Client → API Gateway → Lambda → DynamoDB            │
│    │         │            │         │                 │
│    │      Segment     Segment   Subsegment           │
│    │         │            │         │                 │
│    └─────────┴────────────┴─────────┘                │
│                    │                                  │
│              Trace (all segments)                     │
│                    │                                  │
│              Service Map                              │
└──────────────────────────────────────────────────────┘
```

| Concept | Description |
|---------|-------------|
| **Trace** | End-to-end request journey through services |
| **Segment** | Data from one service (Lambda, API Gateway) |
| **Subsegment** | More granular data within a segment |
| **Annotation** | Key-value pairs **indexed** for search (e.g., `Game = "Chess"`) |
| **Metadata** | Key-value pairs **not indexed** (e.g., debug info) |
| **Sampling** | Control how many requests are traced |

---

## Enabling X-Ray

### Lambda
1. Enable **Active Tracing** in Lambda configuration
2. Add `AWSXRayDaemonWriteAccess` policy to execution role
3. Use X-Ray SDK in code

### API Gateway
1. Enable **X-Ray Tracing** in stage settings

### SDK Usage (Python)

```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries
patch_all()

def lambda_handler(event, context):
    # Custom subsegment
    with xray_recorder.capture('process_order') as subsegment:
        order = process_order(event)
        
        # Add annotation (searchable)
        subsegment.put_annotation('OrderId', order['id'])
        
        # Add metadata (not searchable)
        subsegment.put_metadata('debug', {'raw_event': event})
    
    return {'statusCode': 200, 'body': 'OK'}
```

---

## Sampling Rules

```json
{
  "SamplingRules": [
    {
      "RuleName": "BaseRule",
      "Priority": 100,
      "FixedRate": 0.05,
      "ReservoirSize": 1,
      "ServiceName": "*",
      "HTTPMethod": "*",
      "URLPath": "*"
    },
    {
      "RuleName": "HighPriorityRule",
      "Priority": 1,
      "FixedRate": 1.0,
      "ReservoirSize": 10,
      "ServiceName": "payment-service",
      "HTTPMethod": "POST",
      "URLPath": "/api/payments/*"
    }
  ]
}
```

---

## X-Ray Daemon

- Runs alongside your application
- Receives trace data on **UDP port 2000**
- Sends data to X-Ray service
- **Lambda:** Automatically managed
- **ECS/EC2:** Must install and configure

---

## X-Ray vs CloudWatch

| Feature | X-Ray | CloudWatch |
|---------|-------|------------|
| Focus | Request tracing across services | Metrics and logs per service |
| Granularity | Individual requests | Aggregated statistics |
| Service map | **Yes** (visual) | No |
| Best for | Debug distributed systems | Monitor performance |

---

## Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| Debug request across multiple services | Use X-Ray tracing |
| Visualize service dependencies | Use X-Ray Service Map |
| Trace specific requests | Use annotations to filter |
| Reduce tracing overhead | Configure sampling rules |
| Trace Lambda + API Gateway | Enable active tracing on both |
| Search traces by user ID | Add annotation with user ID |

---

[← CloudTrail](02-cloudtrail.md) | [Back to Index](../../README.md) | [Next: Troubleshooting →](04-troubleshooting.md)
</task_progress>
- [x] Create README.md (main index)
- [x] Domain 1 study guides (10 files)
- [x] Domain 2 study guides (5 files)
- [x] Domain 3 study guides (5 files)
- [x] Domain 4: 01-cloudwatch.md, 02-cloudtrail.md, 03-xray.md
- [ ] Domain 4: 04-troubleshooting.md
- [ ] Create quick reference cards (4 files)
- [ ] Create exercises (55 scenarios)
- [ ] Create exercise runner script
- [ ] Create exercises README
- [ ] Create practice exams (5 exams)
</write_to_file>