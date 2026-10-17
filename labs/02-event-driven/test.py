"""LocalStack tests for lab 02 — event-driven fan-out."""

from __future__ import annotations

import json
import os
import importlib
import time
import uuid

from common.aws_client import get_client, is_localstack_up

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
setup_fanout = _mod.setup_fanout
publish_event = _mod.publish_event
sqs_handler = _mod.sqs_handler


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable. Run: docker compose up -d "
        "and set AWS_ENDPOINT_URL=http://localhost:4566"
    )


def _drain(sqs, url: str, wait: int = 1) -> list:
    messages = []
    # Poll a few times — LocalStack delivery can lag slightly
    for _ in range(5):
        resp = sqs.receive_message(
            QueueUrl=url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=wait,
            MessageAttributeNames=["All"],
        )
        batch = resp.get("Messages", [])
        if not batch:
            if messages:
                break
            continue
        messages.extend(batch)
        for m in batch:
            sqs.delete_message(QueueUrl=url, ReceiptHandle=m["ReceiptHandle"])
    return messages


def test_sqs_handler_parses_records():
    event = {
        "Records": [
            {"body": json.dumps({"event_type": "order_created", "data": {"id": "1"}})},
            {"body": json.dumps({"event_type": "order_created", "data": {"id": "2"}})},
        ]
    }
    result = sqs_handler(event, None)
    assert result["processed"] == 2


def test_fanout_filter_policy():
    _require_localstack()
    sns = get_client("sns")
    sqs = get_client("sqs")
    suffix = uuid.uuid4().hex[:8]
    topic = f"lab02-orders-{suffix}"
    orders_q = f"lab02-orders-q-{suffix}"
    inventory_q = f"lab02-inventory-q-{suffix}"

    config = setup_fanout(
        sns,
        sqs,
        topic,
        [
            {
                "queue_name": orders_q,
                "filter_policy": {"event_type": ["order_created", "order_updated"]},
            },
            {
                "queue_name": inventory_q,
                "filter_policy": {"event_type": ["inventory_updated"]},
            },
        ],
    )
    assert "topic_arn" in config
    assert orders_q in config["queues"]
    assert inventory_q in config["queues"]

    # Give subscriptions a moment
    time.sleep(1)

    publish_event(
        sns,
        config["topic_arn"],
        "order_created",
        {"order_id": "o-1"},
    )
    publish_event(
        sns,
        config["topic_arn"],
        "inventory_updated",
        {"sku": "ABC"},
    )
    time.sleep(1)

    orders_msgs = _drain(sqs, config["queues"][orders_q]["url"])
    inv_msgs = _drain(sqs, config["queues"][inventory_q]["url"])

    assert len(orders_msgs) >= 1, "orders queue should receive order_created"
    assert len(inv_msgs) >= 1, "inventory queue should receive inventory_updated"

    # Orders queue should not get inventory events
    for m in orders_msgs:
        body = json.loads(m["Body"])
        # SNS wraps body sometimes
        if "Message" in body:
            inner = json.loads(body["Message"])
        else:
            inner = body
        assert inner.get("event_type") != "inventory_updated"

    # Cleanup best-effort
    try:
        sns.delete_topic(TopicArn=config["topic_arn"])
        sqs.delete_queue(QueueUrl=config["queues"][orders_q]["url"])
        sqs.delete_queue(QueueUrl=config["queues"][inventory_q]["url"])
    except Exception:
        pass
