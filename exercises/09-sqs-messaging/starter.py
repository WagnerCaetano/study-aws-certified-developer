"""SQS helpers — fix the bugs so tests pass against LocalStack."""

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
    # BUG: str() instead of json.dumps for dicts; no FIFO dedup id
    params: Dict[str, Any] = {
        "QueueUrl": queue_url,
        "MessageBody": message_body if isinstance(message_body, str) else str(message_body),
        "DelaySeconds": delay_seconds,
    }
    if group_id:
        params["MessageGroupId"] = group_id
    resp = client.send_message(**params)
    return resp["MessageId"]


def receive_messages(client, queue_url: str, max_messages: int = 1, wait_seconds: int = 1) -> List[dict]:
    """Receive messages and return list of {message_id, receipt_handle, body}."""
    resp = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_seconds,
    )
    results = []
    for msg in resp.get("Messages", []):
        # BUG: leaves body as raw string, never json.loads
        results.append(
            {
                "message_id": msg["MessageId"],
                "receipt_handle": msg["ReceiptHandle"],
                "body": msg["Body"],
            }
        )
    return results


def delete_message(client, queue_url: str, receipt_handle: str) -> None:
    """Delete a received message by receipt handle."""
    # BUG: wrong parameter name
    client.delete_message(QueueUrl=queue_url, ReceiptHandleId=receipt_handle)


def build_queue_attributes(visibility_timeout: int = 30, retention_period: int = 1209600) -> Dict[str, str]:
    """Build SQS queue Attributes map (string values)."""
    return {
        "VisibilityTimeout": str(visibility_timeout),
        "MessageRetentionPeriod": str(retention_period),
        "DelaySeconds": "0",
    }


def build_dlq_redrive_policy(dlq_arn: str, max_receive_count: int = 5) -> str:
    """Return RedrivePolicy as a JSON string (SQS attribute value)."""
    # BUG: returns a dict instead of JSON string; maxReceiveCount as int
    return {
        "deadLetterTargetArn": dlq_arn,
        "maxReceiveCount": max_receive_count,
    }


def process_sqs_event(event: dict) -> List[dict]:
    """Parse Lambda SQS event records (exam-style)."""
    results = []
    for record in event.get("Records", []):
        # BUG: does not json.loads body
        results.append(
            {
                "message_id": record["messageId"],
                "receipt_handle": record["receiptHandle"],
                "body": record["body"],
            }
        )
    return results
