import json
from solution import build_send_message_params, process_sqs_event, build_queue_attributes, build_dlq_config

def test_send_message_dict():
    result = build_send_message_params('https://sqs.us-east-1.amazonaws.com/123/my-queue', {'key': 'value'})
    assert result['QueueUrl'] == 'https://sqs.us-east-1.amazonaws.com/123/my-queue'
    assert json.loads(result['MessageBody']) == {'key': 'value'}

def test_send_fifo_message():
    result = build_send_message_params('url', {'key': 'value'}, group_id='group-1')
    assert result['MessageGroupId'] == 'group-1'
    assert 'MessageDeduplicationId' in result

def test_process_sqs_event():
    event = {'Records': [
        {'messageId': 'msg-1', 'receiptHandle': 'handle-1', 'body': json.dumps({'id': 1})},
        {'messageId': 'msg-2', 'receiptHandle': 'handle-2', 'body': json.dumps({'id': 2})}
    ]}
    results = process_sqs_event(event)
    assert len(results) == 2
    assert results[0]['body']['id'] == 1

def test_dlq_config():
    result = build_dlq_config('arn:aws:sqs:us-east-1:123:my-dlq', 3)
    policy = json.loads(result['RedrivePolicy'])
    assert policy['deadLetterTargetArn'] == 'arn:aws:sqs:us-east-1:123:my-dlq'
    assert policy['maxReceiveCount'] == '3'
