import json


def build_api_handler():
    def handler(event, context):
        method = event.get('httpMethod', 'GET')
        path_params = event.get('pathParameters') or {}
        body = json.loads(event.get('body') or '{}')

        if method == 'GET' and not path_params.get('id'):
            return {'statusCode': 200, 'body': json.dumps({'items': []})}
        elif method == 'GET' and path_params.get('id'):
            return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}
        elif method == 'POST':
            return {'statusCode': 200, 'body': json.dumps({'id': 'new', 'name': body.get('name')})}
        elif method == 'DELETE' and path_params.get('id'):
            return {'statusCode': 200, 'body': json.dumps({'deleted': path_params['id']})}
        return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}

    return handler


def build_cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body) if isinstance(body, dict) else body,
    }
