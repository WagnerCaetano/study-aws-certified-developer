# Exercise 13: Step Functions

## Learning goals

- Model an order workflow with Task, Choice, Retry, Catch, and Fail states (ASL)
- Validate ASL structure programmatically
- Create and start a simplified Pass-state machine on LocalStack

## LocalStack

**Prerequisite:**

```bash
docker compose up -d
```

See [setup.md](../../setup.md).

**Services used:** `stepfunctions`, `iam` (execution role)

**Cleanup:** tests delete the temporary state machine. Use `docker compose down` to stop LocalStack.

> Live execution uses a **Pass** workflow (no Lambda). The full order ASL is validated offline so you still practice exam-critical Task/Choice/Fail patterns without depending on Lambda packaging in LocalStack.

## Problem

Fix `starter.py`:

1. **build_order_workflow** — six states: ValidateOrder → CheckInventory (Retry+Catch) → `InStock?` Choice → ShipOrder / Backorder / OrderFailed
2. **build_pass_workflow** — valid `StartAt` + Pass state with `End: true`
3. **create_state_machine** — `definition` must be a **JSON string**; return `stateMachineArn`
4. **start_execution** — `input` must be a **JSON string**; return `executionArn`

## Exam tip

Standard workflows support long runs; Express is for high-volume short work. `Retry` uses `ErrorEquals`, `IntervalSeconds`, `MaxAttempts`, and `BackoffRate`.

## Run

```bash
docker compose up -d
python runner.py exercises/13-step-functions
python runner.py exercises/13-step-functions --solution
```
