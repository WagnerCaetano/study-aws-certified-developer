import json
from solution import handler

def test_returns_greeting_with_name():
    event = {'body': json.dumps({'name': 'Alice'})}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['message'] == 'Hello, Alice!'

def test_returns_400_without_name():
    event = {'body': json.dumps({})}
    result = handler(event, None)
    assert result['statusCode'] == 400

def test_handles_missing_body():
    event = {}
    result = handler(event, None)
    assert result['statusCode'] == 400

def test_response_has_headers():
    event = {'body': json.dumps({'name': 'Bob'})}
    result = handler(event, None)
    assert 'headers' in result
    assert result['headers']['Content-Type'] == 'application/json'
