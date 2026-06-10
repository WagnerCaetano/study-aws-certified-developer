import json

def build_api_response(status_code, body, headers=None):
    """Build a proper API Gateway Lambda proxy response."""
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body) if isinstance(body, dict) else body
    }

def handler(event, context):
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # Fix: Handle CORS preflight
    if http_method == 'OPTIONS':
        return build_api_response(200, '')
    
    # Fix: Route based on method and path
    if http_method == 'GET' and '/items' in path:
        item_id = event.get('pathParameters', {}).get('id') if event.get('pathParameters') else None
        if item_id:
            return build_api_response(200, {'id': item_id, 'name': 'Item ' + item_id})
        return build_api_response(200, {'items': [{'id': '1', 'name': 'Item 1'}]})
    
    if http_method == 'POST' and '/items' in path:
        body = json.loads(event.get('body', '{}'))
        if not body.get('name'):
            return build_api_response(400, {'error': 'name is required'})
        return build_api_response(201, {'id': 'new-1', 'name': body['name']})
    
    return build_api_response(404, {'error': 'Not found'})
