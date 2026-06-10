import json
from solution import handler

def test_get_items():
    event = {'httpMethod': 'GET', 'path': '/items'}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert 'items' in body

def test_get_item_by_id():
    event = {'httpMethod': 'GET', 'path': '/items/123', 'pathParameters': {'id': '123'}}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['id'] == '123'

def test_post_item():
    event = {'httpMethod': 'POST', 'path': '/items', 'body': json.dumps({'name': 'New Item'})}
    result = handler(event, None)
    assert result['statusCode'] == 201

def test_post_item_missing_name():
    event = {'httpMethod': 'POST', 'path': '/items', 'body': json.dumps({})}
    result = handler(event, None)
    assert result['statusCode'] == 400

def test_cors_preflight():
    event = {'httpMethod': 'OPTIONS', 'path': '/items'}
    result = handler(event, None)
    assert result['statusCode'] == 200
    assert 'Access-Control-Allow-Origin' in result['headers']

def test_cors_headers_present():
    event = {'httpMethod': 'GET', 'path': '/items'}
    result = handler(event, None)
    assert result['headers']['Access-Control-Allow-Origin'] == '*'

def test_not_found():
    event = {'httpMethod': 'DELETE', 'path': '/unknown'}
    result = handler(event, None)
    assert result['statusCode'] == 404
