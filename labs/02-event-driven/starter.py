"""Lab 02: Event-driven fan-out — incomplete starter (edit this)."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def setup_fanout(
    sns,
    sqs,
    topic_name: str,
    subscriptions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Create SNS topic + SQS queues with filter-policy subscriptions.

    ``subscriptions`` items: ``{"queue_name": str, "filter_policy": dict}``
    Return ``{"topic_arn": ..., "queues": {name: {"url": ..., "arn": ...}}}``.
    """
    # TODO: create topic, queues, subscribe with FilterPolicy JSON
    raise NotImplementedError("setup_fanout is not implemented")


def publish_event(sns, topic_arn: str, event_type: str, data: Dict[str, Any]) -> str:
    """Publish JSON message with String attribute event_type. Return MessageId."""
    # TODO: MessageAttributes for filter matching
    raise NotImplementedError("publish_event is not implemented")


def sqs_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Lambda handler for SQS events — count and parse records."""
    # TODO: iterate event['Records'], parse body JSON
    return {"processed": 0}
