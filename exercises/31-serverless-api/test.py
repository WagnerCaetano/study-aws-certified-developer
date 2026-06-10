import json
from solution import build_api_handler, build_cors_response

def test_list_items():
    handler = build_api_handler()
    result = handler({'httpMethod': 'GET', 'pathParameters': None}, None)
    assert result['statusCode'] == 200

def test_get_item():
    handler = build_api_handler()
    result = handler({'httpMethod': 'GET', 'pathParameters': {'id': '123'}}, None)
    assert result['statusCode'] == 200
    assert json.loads(result['body'])['id'] == '123'

def test_create_item():
    handler = build_api_handler()
    result = handler({'httpMethod': 'POST', 'body': json.dumps({'name': 'Test'})}, None)
    assert result['statusCode'] == 201

def test_create_item_validation():
    handler = build_api_handler()
    result = handler({'httpMethod': 'POST', 'body': json.dumps({})}, None)
    assert result['statusCode'] == 400

def test_delete_item():
    handler = build_api_handler()
    result = handler({'httpMethod': 'DELETE', 'pathParameters': {'id': '123'}}, None)
    assert result['statusCode'] == 204

def test_cors_response():
    resp = build_cors_response(200, {'ok': True})
    assert resp['headers']['Access-Control-Allow-Origin'] == '*'
