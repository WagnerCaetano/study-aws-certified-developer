"""ASL unit checks + LocalStack create/start for a Pass workflow."""

from __future__ import annotations

import importlib
import json
import os
import time
import uuid

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
build_order_workflow = _mod.build_order_workflow
validate_state_machine = _mod.validate_state_machine
build_pass_workflow = _mod.build_pass_workflow
create_state_machine = _mod.create_state_machine
start_execution = _mod.start_execution

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


def _ensure_sfn_role() -> str:
    iam = get_client("iam")
    role_name = "ex13-sfn-role"
    trust = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "states.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
    try:
        resp = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust),
        )
        return resp["Role"]["Arn"]
    except ClientError as e:
        if e.response["Error"]["Code"] not in ("EntityAlreadyExists", "EntityAlreadyExistsException"):
            # LocalStack may use slightly different codes; try get_role
            pass
        try:
            return iam.get_role(RoleName=role_name)["Role"]["Arn"]
        except ClientError:
            # Fallback dummy ARN accepted by many LocalStack builds
            return "arn:aws:iam::000000000000:role/ex13-sfn-role"


def test_workflow_structure():
    wf = build_order_workflow("arn:validate", "arn:inventory", "arn:ship")
    assert wf["StartAt"] == "ValidateOrder"
    assert "States" in wf
    assert len(wf["States"]) == 6


def test_choice_state():
    wf = build_order_workflow("arn:validate", "arn:inventory", "arn:ship")
    choice = wf["States"]["InStock?"]
    assert choice["Type"] == "Choice"
    assert len(choice["Choices"]) == 1


def test_retry_and_catch():
    wf = build_order_workflow("arn:validate", "arn:inventory", "arn:ship")
    check = wf["States"]["CheckInventory"]
    assert "Retry" in check
    assert check["Retry"][0]["MaxAttempts"] == 3
    assert "Catch" in check


def test_fail_states():
    wf = build_order_workflow("arn:validate", "arn:inventory", "arn:ship")
    assert wf["States"]["Backorder"]["Type"] == "Fail"
    assert wf["States"]["OrderFailed"]["Type"] == "Fail"


def test_validate_good_and_bad():
    wf = build_order_workflow("arn:validate", "arn:inventory", "arn:ship")
    assert validate_state_machine(wf) == []
    assert len(validate_state_machine({})) > 0


def test_create_and_run_pass_workflow():
    _require_localstack()
    sfn = get_client("stepfunctions")
    role_arn = _ensure_sfn_role()
    definition = build_pass_workflow({"hello": "world"})
    assert validate_state_machine(definition) == []
    name = f"ex13-{uuid.uuid4().hex[:10]}"
    arn = create_state_machine(sfn, name, definition, role_arn)
    assert isinstance(arn, str) and "stateMachine" in arn
    try:
        exec_arn = start_execution(sfn, arn, {"n": 1})
        assert isinstance(exec_arn, str)
        status = None
        for _ in range(20):
            desc = sfn.describe_execution(executionArn=exec_arn)
            status = desc["status"]
            if status in ("SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"):
                break
            time.sleep(0.25)
        assert status == "SUCCEEDED", f"expected SUCCEEDED, got {status}"
    finally:
        try:
            sfn.delete_state_machine(stateMachineArn=arn)
        except ClientError:
            pass
