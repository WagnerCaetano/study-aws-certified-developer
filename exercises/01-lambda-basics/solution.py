import json

def handler(event, context):
    # TODO: Fix the event parsing and response format
    # BUG: The body parsing is incorrect
    
    # Fix: Parse the body from the event
    body = json.loads(event.get('body', '{}'))
    
    # Fix: Check for name field properly
    name = body.get('name')
    if not name:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Name is required'})
        }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': f'Hello, {name}!'})
    }
