"""Live SQS tests against LocalStack (create / exercise / teardown)."""

from __future__ import annotations

import importlib
import json
import os
import uuid
from contextlib import contextmanager

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
send_json_message = _mod.send_json_message
receive_messages = _mod.receive_messages
delete_message = _mod.delete_message
build_queue_attributes = _mod.build_queue_attributes
build_dlq_redrive_policy = _mod.build_dlq_redrive_policy
process_sqs_event = _mod.process_sqs_event

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


@contextmanager
def temp_queue(fifo: bool = False):
    _require_localstack()
    sqs = get_client("sqs")
    suffix = uuid.uuid4().hex[:10]
    name = f"ex09-{suffix}.fifo" if fifo else f"ex09-{suffix}"
    attrs = build_queue_attributes(visibility_timeout=30)
    if fifo:
        attrs["FifoQueue"] = "true"
        attrs["ContentBasedDeduplication"] = "true"
    resp = sqs.create_queue(QueueName=name, Attributes=attrs)
    url = resp["QueueUrl"]
    try:
        yield sqs, url
    finally:
        try:
            sqs.delete_queue(QueueUrl=url)
        except ClientError:
            pass


def test_send_receive_delete_json():
    with temp_queue() as (sqs, url):
        mid = send_json_message(sqs, url, {"order_id": 7})
        assert mid
        msgs = receive_messages(sqs, url, max_messages=1, wait_seconds=2)
        assert len(msgs) == 1
        assert msgs[0]["body"]["order_id"] == 7
        delete_message(sqs, url, msgs[0]["receipt_handle"])
        again = receive_messages(sqs, url, max_messages=1, wait_seconds=1)
        assert again == []


def test_fifo_send_with_group():
    with temp_queue(fifo=True) as (sqs, url):
        mid = send_json_message(sqs, url, {"n": 1}, group_id="g1")
        assert mid
        msgs = receive_messages(sqs, url, wait_seconds=2)
        assert len(msgs) == 1
        assert msgs[0]["body"]["n"] == 1
        delete_message(sqs, url, msgs[0]["receipt_handle"])


def test_dlq_redrive_policy_string():
    policy = build_dlq_redrive_policy("arn:aws:sqs:us-east-1:000000000000:dlq", 3)
    assert isinstance(policy, str)
    parsed = json.loads(policy)
    assert parsed["deadLetterTargetArn"].endswith(":dlq")
    assert parsed["maxReceiveCount"] == "3"


def test_queue_with_dlq_attributes():
    _require_localstack()
    sqs = get_client("sqs")
    suffix = uuid.uuid4().hex[:8]
    dlq = sqs.create_queue(QueueName=f"ex09-dlq-{suffix}")
    dlq_url = dlq["QueueUrl"]
    dlq_arn = sqs.get_queue_attributes(QueueUrl=dlq_url, AttributeNames=["QueueArn"])[
        "Attributes"
    ]["QueueArn"]
    main = sqs.create_queue(
        QueueName=f"ex09-main-{suffix}",
        Attributes={
            **build_queue_attributes(),
            "RedrivePolicy": build_dlq_redrive_policy(dlq_arn, 2),
        },
    )
    main_url = main["QueueUrl"]
    try:
        attrs = sqs.get_queue_attributes(
            QueueUrl=main_url, AttributeNames=["RedrivePolicy"]
        )["Attributes"]
        policy = json.loads(attrs["RedrivePolicy"])
        assert policy["maxReceiveCount"] in ("2", 2)
        assert dlq_arn in policy["deadLetterTargetArn"] or policy["deadLetterTargetArn"] == dlq_arn
    finally:
        for u in (main_url, dlq_url):
            try:
                sqs.delete_queue(QueueUrl=u)
            except ClientError:
                pass


def test_process_sqs_event():
    event = {
        "Records": [
            {
                "messageId": "msg-1",
                "receiptHandle": "handle-1",
                "body": json.dumps({"id": 1}),
            }
        ]
    }
    results = process_sqs_event(event)
    assert results[0]["body"]["id"] == 1
