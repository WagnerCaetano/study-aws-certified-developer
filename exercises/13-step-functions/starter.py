"""Step Functions helpers — fix ASL + LocalStack create/start bugs."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def build_order_workflow(
    order_function_arn: str,
    inventory_function_arn: str,
    ship_function_arn: str,
) -> dict:
    """Build an order-processing ASL definition (exam-shaped)."""
    # BUG: missing Choice/Retry/Catch; wrong transitions; Backorder is Pass not Fail
    return {
        "Comment": "Order processing workflow",
        "StartAt": "ValidateOrder",
        "States": {
            "ValidateOrder": {
                "Type": "Task",
                "Resource": order_function_arn,
                "Next": "CheckInventory",
            },
            "CheckInventory": {
                "Type": "Task",
                "Resource": inventory_function_arn,
                "Next": "ShipOrder",
            },
            "ShipOrder": {
                "Type": "Task",
                "Resource": ship_function_arn,
                "Next": "Backorder",
            },
            "Backorder": {
                "Type": "Pass",
                "End": True,
            },
        },
    }


def validate_state_machine(definition: dict) -> List[str]:
    """Validate required ASL fields; return a list of error strings."""
    errors: List[str] = []
    if "StartAt" not in definition:
        errors.append("Missing StartAt")
    if "States" not in definition:
        errors.append("Missing States")
        return errors

    states = definition["States"]
    start = definition.get("StartAt")
    if start not in states:
        errors.append(f'StartAt state "{start}" not found in States')

    for name, state in states.items():
        if "Type" not in state:
            errors.append(f'State "{name}" missing Type')
        elif state["Type"] == "Task" and "Resource" not in state:
            errors.append(f'Task state "{name}" missing Resource')
        elif state["Type"] == "Choice" and "Choices" not in state:
            errors.append(f'Choice state "{name}" missing Choices')
    return errors


def build_pass_workflow(result: dict | None = None) -> dict:
    """Minimal Pass-state machine safe to run on LocalStack without Lambda."""
    # BUG: missing End / wrong StartAt
    return {
        "Comment": "LocalStack-friendly pass workflow",
        "StartAt": "Missing",
        "States": {
            "Done": {
                "Type": "Pass",
                "Result": result or {"ok": True},
            }
        },
    }


def create_state_machine(sfn_client, name: str, definition: dict, role_arn: str) -> str:
    """Create a state machine; return its ARN."""
    # BUG: passes dict instead of JSON string; returns whole response
    return sfn_client.create_state_machine(
        name=name,
        definition=definition,
        roleArn=role_arn,
        type="STANDARD",
    )


def start_execution(sfn_client, state_machine_arn: str, input_data: dict | None = None) -> str:
    """Start an execution; return execution ARN."""
    params: Dict[str, Any] = {"stateMachineArn": state_machine_arn}
    if input_data is not None:
        # BUG: passes dict instead of JSON string
        params["input"] = input_data
    return sfn_client.start_execution(**params)["executionArn"]
