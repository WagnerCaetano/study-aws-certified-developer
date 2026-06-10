import json

def build_fanout_config(topic_arn, queues):
    return {
        'topic': topic_arn,
        'subscriptions': [{'queue_arn': q, 'protocol': 'sqs'} for q in queues]
    }

def build_sns_filter_policy(rules):
    policy = {}
    for attr, values in rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    return json.dumps(policy)

def build_event_payload(event_type, source, data, metadata=None):
    payload = {
        'event_type': event_type,
        'source': source,
        'data': data,
        'timestamp': '2024-01-15T10:00:00Z'
    }
    if metadata:
        payload['metadata'] = metadata
    return payload

def route_event(event_type, handlers):
    return handlers.get(event_type, handlers.get('default'))
