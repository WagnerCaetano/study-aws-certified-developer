"""SNS helpers for LocalStack (publish, subscribe SQS, filter policy) + event parsing."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union


def create_topic(client, name: str) -> str:
    """Create a topic and return its ARN."""
    return client.create_topic(Name=name)["TopicArn"]


def publish_json(
    client,
    topic_arn: str,
    message: Union[dict, str],
    subject: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None,
) -> str:
    """Publish a message; return MessageId."""
    params: Dict[str, Any] = {
        "TopicArn": topic_arn,
        "Message": json.dumps(message) if isinstance(message, dict) else message,
    }
    if subject:
        params["Subject"] = subject
    if attributes:
        msg_attrs = {}
        for key, value in attributes.items():
            msg_attrs[key] = {"DataType": "String", "StringValue": str(value)}
        params["MessageAttributes"] = msg_attrs
    return client.publish(**params)["MessageId"]


def subscribe_queue(sns_client, topic_arn: str, queue_arn: str) -> str:
    """Subscribe an SQS queue to an SNS topic; return SubscriptionArn."""
    resp = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="sqs",
        Endpoint=queue_arn,
    )
    return resp["SubscriptionArn"]


def set_filter_policy(sns_client, subscription_arn: str, filter_rules: dict) -> None:
    """Set subscription FilterPolicy from attribute -> list-of-values map."""
    policy = {}
    for attr, values in filter_rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    sns_client.set_subscription_attributes(
        SubscriptionArn=subscription_arn,
        AttributeName="FilterPolicy",
        AttributeValue=json.dumps(policy),
    )


def parse_sns_event(event: dict) -> List[dict]:
    """Parse Lambda SNS event records (key is ``Sns``, not ``SNS``)."""
    results = []
    for record in event.get("Records", []):
        sns = record.get("Sns", {})
        results.append(
            {
                "message": sns.get("Message"),
                "subject": sns.get("Subject"),
                "message_id": sns.get("MessageId"),
            }
        )
    return results
