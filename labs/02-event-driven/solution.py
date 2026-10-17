"""Lab 02: Event-driven fan-out — reference solution."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def setup_fanout(
    sns,
    sqs,
    topic_name: str,
    subscriptions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    topic = sns.create_topic(Name=topic_name)
    topic_arn = topic["TopicArn"]

    queues: Dict[str, Dict[str, str]] = {}
    for sub in subscriptions:
        qname = sub["queue_name"]
        created = sqs.create_queue(QueueName=qname)
        url = created["QueueUrl"]
        attrs = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["QueueArn"])
        qarn = attrs["Attributes"]["QueueArn"]

        # Allow SNS to send (real AWS); LocalStack may not enforce
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "sns.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": qarn,
                    "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}},
                }
            ],
        }
        sqs.set_queue_attributes(
            QueueUrl=url,
            Attributes={"Policy": json.dumps(policy)},
        )

        filter_policy = sub.get("filter_policy") or {}
        sns.subscribe(
            TopicArn=topic_arn,
            Protocol="sqs",
            Endpoint=qarn,
            Attributes={"FilterPolicy": json.dumps(filter_policy)},
        )
        queues[qname] = {"url": url, "arn": qarn}

    return {"topic_arn": topic_arn, "queues": queues}


def publish_event(sns, topic_arn: str, event_type: str, data: Dict[str, Any]) -> str:
    resp = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({"event_type": event_type, "data": data}),
        MessageAttributes={
            "event_type": {"DataType": "String", "StringValue": event_type},
        },
    )
    return resp["MessageId"]


def sqs_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    processed = 0
    for record in event.get("Records", []):
        body = record.get("body", "{}")
        if isinstance(body, str):
            json.loads(body)
        processed += 1
    return {"processed": processed}
