import json
from solution import build_fanout_config, build_sns_filter_policy, build_event_payload, route_event

def test_fanout_config():
    config = build_fanout_config('arn:sns:topic', ['arn:sqs:q1', 'arn:sqs:q2'])
    assert len(config['subscriptions']) == 2

def test_filter_policy():
    policy = build_sns_filter_policy({'event_type': ['order_created', 'order_updated']})
    parsed = json.loads(policy)
    assert 'order_created' in parsed['event_type']

def test_event_payload():
    payload = build_event_payload('order_created', 'checkout-service', {'order_id': '123'})
    assert payload['event_type'] == 'order_created'
    assert payload['data']['order_id'] == '123'

def test_route_event():
    handlers = {'order_created': 'process_order', 'default': 'log_event'}
    assert route_event('order_created', handlers) == 'process_order'
    assert route_event('unknown', handlers) == 'log_event'
