import json
from solution import build_publish_params, build_sqs_subscription, build_filter_policy, parse_sns_event

def test_publish_with_attributes():
    result = build_publish_params('arn:aws:sns:us-east-1:123:topic', {'event': 'order'}, attributes={'type': 'order'})
    assert result['TopicArn'] == 'arn:aws:sns:us-east-1:123:topic'
    assert result['MessageAttributes']['type']['DataType'] == 'String'

def test_sqs_subscription():
    result = build_sqs_subscription('arn:aws:sns:us-east-1:123:topic', 'arn:aws:sqs:us-east-1:123:queue')
    assert result['Protocol'] == 'sqs'
    assert result['Endpoint'] == 'arn:aws:sqs:us-east-1:123:queue'

def test_filter_policy():
    result = build_filter_policy({'event_type': ['order', 'payment']})
    policy = json.loads(result['FilterPolicy'])
    assert 'event_type' in policy
    assert 'order' in policy['event_type']

def test_parse_sns_event():
    event = {'Records': [{'Sns': {'Message': json.dumps({'id': 1}), 'Subject': 'Test', 'MessageId': 'msg-1'}}]}
    results = parse_sns_event(event)
    assert len(results) == 1
    assert results[0]['subject'] == 'Test'
