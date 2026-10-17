"""SQS helpers for LocalStack (send, receive+delete, DLQ config) + event parsing."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union


def send_json_message(
    client,
    queue_url: str,
    message_body: Union[dict, str],
    delay_seconds: int = 0,
    group_id: Optional[str] = None,
) -> str:
    """Send a message; return MessageId. FIFO when ``group_id`` is set."""
    body = json.dumps(message_body) if isinstance(message_body, dict) else message_body
    params: Dict[str, Any] = {
        "QueueUrl": queue_url,
        "MessageBody": body,
        "DelaySeconds": delay_seconds,
    }
    if group_id:
        params["MessageGroupId"] = group_id
        params["MessageDeduplicationId"] = str(
            hash(json.dumps(message_body, sort_keys=True) if isinstance(message_body, dict) else message_body)
        )
    resp = client.send_message(**params)
    return resp["MessageId"]


def receive_messages(client, queue_url: str, max_messages: int = 1, wait_seconds: int = 1) -> List[dict]:
    """Receive messages and return list of {message_id, receipt_handle, body} with body JSON-parsed when possible."""
    resp = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_seconds,
        AttributeNames=["All"],
    )
    results = []
    for msg in resp.get("Messages", []):
        raw = msg["Body"]
        try:
            body = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            body = raw
        results.append(
            {
                "message_id": msg["MessageId"],
                "receipt_handle": msg["ReceiptHandle"],
                "body": body,
            }
        )
    return results


def delete_message(client, queue_url: str, receipt_handle: str) -> None:
    """Delete a received message by receipt handle."""
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)


def build_queue_attributes(visibility_timeout: int = 30, retention_period: int = 1209600) -> Dict[str, str]:
    """Build SQS queue Attributes map (string values)."""
    return {
        "VisibilityTimeout": str(visibility_timeout),
        "MessageRetentionPeriod": str(retention_period),
        "DelaySeconds": "0",
    }


def build_dlq_redrive_policy(dlq_arn: str, max_receive_count: int = 5) -> str:
    """Return RedrivePolicy as a JSON string (SQS attribute value)."""
    return json.dumps(
        {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": str(max_receive_count),
        }
    )


def process_sqs_event(event: dict) -> List[dict]:
    """Parse Lambda SQS event records (exam-style)."""
    results = []
    for record in event.get("Records", []):
        results.append(
            {
                "message_id": record["messageId"],
                "receipt_handle": record["receiptHandle"],
                "body": json.loads(record["body"]),
            }
        )
    return results
