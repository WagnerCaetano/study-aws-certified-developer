import json

def build_api_handler():
    def handler(event, context):
        method = event.get('httpMethod', 'GET')
        path_params = event.get('pathParameters') or {}
        query_params = event.get('queryStringParameters') or {}
        body = json.loads(event.get('body') or '{}')
        
        if method == 'GET' and not path_params.get('id'):
            return {'statusCode': 200, 'body': json.dumps({'items': []})}
        elif method == 'GET' and path_params.get('id'):
            return {'statusCode': 200, 'body': json.dumps({'id': path_params['id']})}
        elif method == 'POST':
            if not body.get('name'):
                return {'statusCode': 400, 'body': json.dumps({'error': 'name required'})}
            return {'statusCode': 201, 'body': json.dumps({'id': 'new', 'name': body['name']})}
        elif method == 'DELETE' and path_params.get('id'):
            return {'statusCode': 204, 'body': ''}
        return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}
    return handler

def build_cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        },
        'body': json.dumps(body) if isinstance(body, dict) else body
    }
