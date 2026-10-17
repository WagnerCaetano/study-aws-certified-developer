import json


def handler(event, context):
    # BUG: reads name from the event root instead of parsing the JSON body
    name = event.get('name')

    if not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Name is required'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Hello, {name}!'})
    }
