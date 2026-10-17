import json
import os


def handler(event, context):
    try:
        table_name = os.environ.get('DYNAMODB_TABLE', 'default-table')
        stage = os.environ.get('ENVIRONMENT', 'dev')

        if 'Records' in event:
            records = event['Records']
            return {
                'statusCode': 200,
                'body': json.dumps({'processed': len(records), 'table': table_name})
            }

        operation = event.get('httpMethod', 'GET')
        path = event.get('path', '/')

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Success',
                'table': table_name,
                'stage': stage,
                'operation': operation
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
