import json
import os


def handler(event, context):
    try:
        table_name = os.environ.get('TABLE_NAME', 'default-table')
        stage = os.environ.get('STAGE', 'dev')

        if 'Records' in event:
            records = event['Records']
            items = []
            for record in records:
                body = json.loads(record.get('body', record.get('Sns', {}).get('Message', '{}')))
                items.append(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'processed': len(items), 'table': table_name})
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
