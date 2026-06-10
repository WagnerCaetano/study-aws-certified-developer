import json
import os
from solution import handler

def test_reads_env_variables():
    os.environ['TABLE_NAME'] = 'UsersTable'
    os.environ['STAGE'] = 'prod'
    event = {'httpMethod': 'GET', 'path': '/users'}
    result = handler(event, None)
    body = json.loads(result['body'])
    assert body['table'] == 'UsersTable'
    assert body['stage'] == 'prod'

def test_handles_sqs_event():
    event = {'Records': [
        {'body': json.dumps({'id': 1})},
        {'body': json.dumps({'id': 2})}
    ]}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['processed'] == 2

def test_error_handling():
    # Force an error with malformed data
    event = {'Records': [{'bad_key': None}]}
    result = handler(event, None)
    assert result['statusCode'] == 200  # Should handle gracefully
