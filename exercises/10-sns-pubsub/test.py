"""Live SNS (+ SQS) tests against LocalStack."""

from __future__ import annotations

import importlib
import json
import os
import time
import uuid
from contextlib import contextmanager

from botocore.exceptions import ClientError

_mod = importlib.import_module(os.environ.get("EXERCISE_MODULE", "starter"))
create_topic = _mod.create_topic
publish_json = _mod.publish_json
subscribe_queue = _mod.subscribe_queue
set_filter_policy = _mod.set_filter_policy
parse_sns_event = _mod.parse_sns_event

from common.aws_client import get_client, is_localstack_up


def _require_localstack():
    assert is_localstack_up(), (
        "LocalStack is not reachable at AWS_ENDPOINT_URL. "
        "Run: docker compose up -d"
    )


def _allow_sns_to_sqs(sqs, queue_url: str, queue_arn: str, topic_arn: str) -> None:
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "sns.amazonaws.com"},
                "Action": "sqs:SendMessage",
                "Resource": queue_arn,
                "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}},
            }
        ],
    }
    sqs.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={"Policy": json.dumps(policy)},
    )


@contextmanager
def topic_and_queue():
    _require_localstack()
    sns = get_client("sns")
    sqs = get_client("sqs")
    suffix = uuid.uuid4().hex[:10]
    topic_arn = create_topic(sns, f"ex10-topic-{suffix}")
    q = sqs.create_queue(QueueName=f"ex10-q-{suffix}")
    queue_url = q["QueueUrl"]
    queue_arn = sqs.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]
    _allow_sns_to_sqs(sqs, queue_url, queue_arn, topic_arn)
    try:
        yield sns, sqs, topic_arn, queue_url, queue_arn
    finally:
        try:
            sns.delete_topic(TopicArn=topic_arn)
        except ClientError:
            pass
        try:
            sqs.delete_queue(QueueUrl=queue_url)
        except ClientError:
            pass


def test_create_topic_returns_arn():
    _require_localstack()
    sns = get_client("sns")
    name = f"ex10-solo-{uuid.uuid4().hex[:8]}"
    arn = create_topic(sns, name)
    try:
        assert isinstance(arn, str)
        assert arn.startswith("arn:")
        assert name in arn
    finally:
        sns.delete_topic(TopicArn=arn)


def test_publish_and_subscribe_delivers_to_sqs():
    with topic_and_queue() as (sns, sqs, topic_arn, queue_url, queue_arn):
        sub = subscribe_queue(sns, topic_arn, queue_arn)
        assert isinstance(sub, str)
        mid = publish_json(sns, topic_arn, {"event": "order"}, attributes={"type": "order"})
        assert mid
        # LocalStack delivery can be briefly async
        body = None
        for _ in range(10):
            resp = sqs.receive_message(
                QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1
            )
            msgs = resp.get("Messages", [])
            if msgs:
                body = msgs[0]["Body"]
                sqs.delete_message(
                    QueueUrl=queue_url, ReceiptHandle=msgs[0]["ReceiptHandle"]
                )
                break
            time.sleep(0.3)
        assert body is not None, "expected SNS message on SQS"
        # Body may be SNS envelope JSON
        parsed = json.loads(body)
        if "Message" in parsed:
            inner = json.loads(parsed["Message"]) if isinstance(parsed["Message"], str) else parsed["Message"]
            assert inner.get("event") == "order" or parsed.get("Message")
        else:
            assert parsed.get("event") == "order"


def test_set_filter_policy():
    with topic_and_queue() as (sns, sqs, topic_arn, queue_url, queue_arn):
        sub = subscribe_queue(sns, topic_arn, queue_arn)
        set_filter_policy(sns, sub, {"event_type": ["order", "payment"]})
        attrs = sns.get_subscription_attributes(SubscriptionArn=sub)["Attributes"]
        policy = json.loads(attrs.get("FilterPolicy", "{}"))
        assert "event_type" in policy
        assert "order" in policy["event_type"]


def test_parse_sns_event():
    event = {
        "Records": [
            {
                "Sns": {
                    "Message": json.dumps({"id": 1}),
                    "Subject": "Test",
                    "MessageId": "msg-1",
                }
            }
        ]
    }
    results = parse_sns_event(event)
    assert len(results) == 1
    assert results[0]["subject"] == "Test"
    assert results[0]["message_id"] == "msg-1"
