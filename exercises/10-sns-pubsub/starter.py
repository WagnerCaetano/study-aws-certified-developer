"""SNS helpers — fix the bugs so tests pass against LocalStack."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union


def create_topic(client, name: str) -> str:
    """Create a topic and return its ARN."""
    # BUG: returns whole response
    return client.create_topic(Name=name)


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
        # BUG: does not JSON-serialize dicts
        "Message": message if isinstance(message, str) else message,
    }
    if subject:
        params["Subject"] = subject
    if attributes:
        msg_attrs = {}
        for key, value in attributes.items():
            msg_attrs[key] = {"DataType": "String", "StringValue": str(value)}
        # BUG: wrong key MessageAttribute (singular)
        params["MessageAttribute"] = msg_attrs
    return client.publish(**params)["MessageId"]


def subscribe_queue(sns_client, topic_arn: str, queue_arn: str) -> str:
    """Subscribe an SQS queue to an SNS topic; return SubscriptionArn."""
    # BUG: wrong protocol https
    resp = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol="https",
        Endpoint=queue_arn,
    )
    return resp["SubscriptionArn"]


def set_filter_policy(sns_client, subscription_arn: str, filter_rules: dict) -> None:
    """Set subscription FilterPolicy from attribute -> list-of-values map."""
    policy = {}
    for attr, values in filter_rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    # BUG: wrong attribute name FilterPolicies
    sns_client.set_subscription_attributes(
        SubscriptionArn=subscription_arn,
        AttributeName="FilterPolicies",
        AttributeValue=json.dumps(policy),
    )


def parse_sns_event(event: dict) -> List[dict]:
    """Parse Lambda SNS event records (key is ``Sns``, not ``SNS``)."""
    results = []
    for record in event.get("Records", []):
        # BUG: looks for SNS instead of Sns
        sns = record.get("SNS", {})
        results.append(
            {
                "message": sns.get("Message"),
                "subject": sns.get("Subject"),
                "message_id": sns.get("MessageId"),
            }
        )
    return results
