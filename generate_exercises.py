#!/usr/bin/env python3
"""Generate all exercise files for AWS Developer Certification study book."""

import os
from pathlib import Path

EXERCISES_DIR = Path(__file__).parent / 'exercises'

# ============================================================
# Exercise definitions: (name, readme, solution, test)
# ============================================================

EXERCISES = []

# ---- Exercise 01: Lambda Basics ----
EXERCISES.append({
    "dir": "01-lambda-basics",
    "readme": """# Exercise 01: Lambda Basics

## Problem
Fix the Lambda handler to properly process API Gateway events.

The function should:
1. Parse the JSON body from the event
2. Extract the `name` field
3. Return a proper response with statusCode 200
4. Handle missing `name` with a 400 error

## Running
```bash
python runner.py exercises/01-lambda-basics
```
""",
    "solution": """import json

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
""",
    "test": """import json
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
""",
})

# ---- Exercise 02: Lambda Advanced ----
EXERCISES.append({
    "dir": "02-lambda-advanced",
    "readme": """# Exercise 02: Lambda Advanced

## Problem
Fix the Lambda function to handle environment variables and proper error handling.

The function should:
1. Read table name from environment variables
2. Handle exceptions gracefully
3. Return proper error responses

## Running
```bash
python runner.py exercises/02-lambda-advanced
```
""",
    "solution": """import json
import os

def handler(event, context):
    try:
        # Fix: Read from environment variables correctly
        table_name = os.environ.get('TABLE_NAME', 'default-table')
        stage = os.environ.get('STAGE', 'dev')
        
        # Fix: Handle different event sources
        if 'Records' in event:
            # SQS/SNS event
            records = event['Records']
            items = []
            for record in records:
                body = json.loads(record.get('body', record.get('Sns', {}).get('Message', '{}')))
                items.append(body)
            return {
                'statusCode': 200,
                'body': json.dumps({'processed': len(items), 'table': table_name})
            }
        
        # API Gateway event
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
        # Fix: Return proper error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
""",
    "test": """import json
import os
from solution import handler

def test_reads_env_variables():
    os.environ['TABLE_NAME'] = 'UsersTable'
    os.environ['STAGE'] = 'prod'
    event = {'httpMethod': 'GET', 'path': '/users'}
    result = handler(event, None)
    body = json.loads(result['body'])
    assert body['table'] == 'UsersTable'
    assert body['stage'] == 'prod'

def test_handles_sqs_event():
    event = {'Records': [
        {'body': json.dumps({'id': 1})},
        {'body': json.dumps({'id': 2})}
    ]}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['processed'] == 2

def test_error_handling():
    # Force an error with malformed data
    event = {'Records': [{'bad_key': None}]}
    result = handler(event, None)
    assert result['statusCode'] == 200  # Should handle gracefully
""",
})

# ---- Exercise 03: Lambda Performance ----
EXERCISES.append({
    "dir": "03-lambda-performance",
    "readme": """# Exercise 03: Lambda Performance

## Problem
Optimize the Lambda function for better cold start performance.

The function should:
1. Initialize AWS SDK clients OUTSIDE the handler
2. Use connection reuse patterns
3. Handle timeouts gracefully

## Running
```bash
python runner.py exercises/03-lambda-performance
```
""",
    "solution": """import json
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Fix: Initialize clients OUTSIDE the handler for connection reuse
# This avoids cold-start re-initialization
CONFIG = {
    'table_name': os.environ.get('TABLE_NAME', 'default'),
    'max_retries': 3,
    'timeout': 28  # Stay under Lambda timeout
}

def process_item(item):
    \"\"\"Process a single item with error handling.\"\"\"
    if not item or 'id' not in item:
        raise ValueError("Item must have an 'id' field")
    return {'id': item['id'], 'processed': True, 'timestamp': int(time.time())}

def handler(event, context):
    # Fix: Check remaining time to avoid timeout
    remaining_ms = context.get_remaining_time_in_millis() if context else 30000
    
    logger.info(f"Processing event, time remaining: {remaining_ms}ms")
    
    try:
        items = event.get('items', [])
        if not items:
            # Fix: Return early for empty batches
            return {'statusCode': 200, 'body': json.dumps({'processed': 0})}
        
        processed = []
        for item in items:
            # Fix: Check if we're running out of time
            if context and context.get_remaining_time_in_millis() < 5000:
                logger.warning("Approaching timeout, returning partial results")
                break
            processed.append(process_item(item))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'processed': len(processed),
                'total': len(items),
                'table': CONFIG['table_name']
            })
        }
    except Exception as e:
        logger.error(f"Error processing: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
""",
    "test": """import json
from solution import handler, CONFIG

def test_config_outside_handler():
    # Config should be initialized at module level
    assert CONFIG['table_name'] is not None
    assert CONFIG['max_retries'] == 3

def test_processes_items():
    event = {'items': [{'id': '1'}, {'id': '2'}, {'id': '3'}]}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['processed'] == 3

def test_handles_empty_batch():
    event = {'items': []}
    result = handler(event, None)
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert body['processed'] == 0

def test_handles_invalid_item():
    event = {'items': [{'wrong': 'field'}]}
    result = handler(event, None)
    assert result['statusCode'] == 500
""",
})

# ---- Exercise 04: API Gateway ----
EXERCISES.append({
    "dir": "04-api-gateway",
    "readme": """# Exercise 04: API Gateway Configuration

## Problem
Fix the API Gateway response mapping and request handling.

## Running
```bash
python runner.py exercises/04-api-gateway
```
""",
    "solution": """import json

def build_api_response(status_code, body, headers=None):
    \"\"\"Build a proper API Gateway Lambda proxy response.\"\"\"
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
""",
    "test": """import json
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
""",
})

# ---- Exercise 05: DynamoDB Operations ----
EXERCISES.append({
    "dir": "05-dynamodb-ops",
    "readme": """# Exercise 05: DynamoDB Operations

## Problem
Fix the DynamoDB helper functions for CRUD operations.

## Running
```bash
python runner.py exercises/05-dynamodb-ops
```
""",
    "solution": """import json

def build_put_item(table_name, item):
    \"\"\"Build a DynamoDB put_item parameters.\"\"\"
    return {
        'TableName': table_name,
        'Item': item,
        'ConditionExpression': 'attribute_not_exists(pk)'
    }

def build_get_item(table_name, key):
    \"\"\"Build a DynamoDB get_item parameters.\"\"\"
    # Fix: Key must be a dict with key attribute name and value
    return {
        'TableName': table_name,
        'Key': key
    }

def build_query(table_name, partition_key_name, partition_key_value):
    \"\"\"Build a DynamoDB query parameters.\"\"\"
    # Fix: Use KeyConditionExpression with proper placeholder
    return {
        'TableName': table_name,
        'KeyConditionExpression': f'{partition_key_name} = :pkval',
        'ExpressionAttributeValues': {
            ':pkval': partition_key_value
        }
    }

def build_update_item(table_name, key, updates):
    \"\"\"Build a DynamoDB update_item parameters.\"\"\"
    # Fix: Build UpdateExpression and ExpressionAttributeValues
    set_parts = []
    attr_values = {}
    for i, (attr, value) in enumerate(updates.items()):
        placeholder = f':val{i}'
        set_parts.append(f'{attr} = {placeholder}')
        attr_values[placeholder] = value
    
    return {
        'TableName': table_name,
        'Key': key,
        'UpdateExpression': 'SET ' + ', '.join(set_parts),
        'ExpressionAttributeValues': attr_values
    }

def build_delete_item(table_name, key):
    \"\"\"Build a DynamoDB delete_item parameters.\"\"\"
    return {
        'TableName': table_name,
        'Key': key,
        'ConditionExpression': 'attribute_exists(pk)'
    }
""",
    "test": """from solution import build_put_item, build_get_item, build_query, build_update_item, build_delete_item

def test_put_item():
    result = build_put_item('Users', {'pk': 'USER#123', 'name': 'Alice'})
    assert result['TableName'] == 'Users'
    assert result['Item']['pk'] == 'USER#123'
    assert 'ConditionExpression' in result

def test_get_item():
    result = build_get_item('Users', {'pk': 'USER#123'})
    assert result['TableName'] == 'Users'
    assert result['Key'] == {'pk': 'USER#123'}

def test_query():
    result = build_query('Users', 'pk', 'USER#123')
    assert result['TableName'] == 'Users'
    assert 'KeyConditionExpression' in result
    assert ':pkval' in result['ExpressionAttributeValues']

def test_update_item():
    result = build_update_item('Users', {'pk': 'USER#123'}, {'name': 'Bob', 'age': 30})
    assert result['TableName'] == 'Users'
    assert 'SET' in result['UpdateExpression']
    assert ':val0' in result['ExpressionAttributeValues']
    assert ':val1' in result['ExpressionAttributeValues']

def test_delete_item():
    result = build_delete_item('Users', {'pk': 'USER#123'})
    assert result['TableName'] == 'Users'
    assert result['Key'] == {'pk': 'USER#123'}
""",
})

# ---- Exercise 06: DynamoDB Design ----
EXERCISES.append({
    "dir": "06-dynamodb-design",
    "readme": """# Exercise 06: DynamoDB Table Design

## Problem
Design proper DynamoDB table schemas for given access patterns.

## Running
```bash
python runner.py exercises/06-dynamodb-design
```
""",
    "solution": """def design_user_table():
    \"\"\"Design a table for users accessed by userId.\"\"\"
    return {
        'TableName': 'Users',
        'KeySchema': [{'AttributeName': 'userId', 'KeyType': 'HASH'}],
        'AttributeDefinitions': [{'AttributeName': 'userId', 'AttributeType': 'S'}],
        'BillingMode': 'PAY_PER_REQUEST'
    }

def design_orders_table():
    \"\"\"Design a table for orders: query by userId, sort by date.\"\"\"
    return {
        'TableName': 'Orders',
        'KeySchema': [
            {'AttributeName': 'userId', 'KeyType': 'HASH'},
            {'AttributeName': 'orderDate', 'KeyType': 'RANGE'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'userId', 'AttributeType': 'S'},
            {'AttributeName': 'orderDate', 'AttributeType': 'S'}
        ],
        'BillingMode': 'PAY_PER_REQUEST'
    }

def design_orders_by_status(orders_table):
    \"\"\"Add a GSI to query orders by status.\"\"\"
    table = orders_table.copy()
    table['GlobalSecondaryIndexes'] = [{
        'IndexName': 'ByStatus',
        'KeySchema': [
            {'AttributeName': 'status', 'KeyType': 'HASH'},
            {'AttributeName': 'orderDate', 'KeyType': 'RANGE'}
        ],
        'Projection': {'ProjectionType': 'ALL'},
    }]
    table['AttributeDefinitions'].append({'AttributeName': 'status', 'AttributeType': 'S'})
    return table
""",
    "test": """from solution import design_user_table, design_orders_table, design_orders_by_status

def test_user_table_has_partition_key():
    table = design_user_table()
    assert table['TableName'] == 'Users'
    keys = table['KeySchema']
    assert any(k['AttributeName'] == 'userId' and k['KeyType'] == 'HASH' for k in keys)

def test_orders_table_has_composite_key():
    table = design_orders_table()
    keys = table['KeySchema']
    hash_keys = [k for k in keys if k['KeyType'] == 'HASH']
    range_keys = [k for k in keys if k['KeyType'] == 'RANGE']
    assert len(hash_keys) == 1
    assert len(range_keys) == 1
    assert hash_keys[0]['AttributeName'] == 'userId'
    assert range_keys[0]['AttributeName'] == 'orderDate'

def test_gsi_for_status():
    base = design_orders_table()
    table = design_orders_by_status(base)
    assert len(table['GlobalSecondaryIndexes']) == 1
    gsi = table['GlobalSecondaryIndexes'][0]
    assert gsi['IndexName'] == 'ByStatus'
    gsi_keys = gsi['KeySchema']
    assert any(k['AttributeName'] == 'status' for k in gsi_keys)

def test_uses_pay_per_request():
    table = design_user_table()
    assert table['BillingMode'] == 'PAY_PER_REQUEST'
""",
})

# ---- Exercise 07: S3 Operations ----
EXERCISES.append({
    "dir": "07-s3-operations",
    "readme": """# Exercise 07: S3 File Operations

## Problem
Fix the S3 helper functions for common file operations.

## Running
```bash
python runner.py exercises/07-s3-operations
```
""",
    "solution": """import json

def build_put_object_params(bucket, key, data, content_type='application/json'):
    \"\"\"Build parameters for S3 put_object.\"\"\"
    body = json.dumps(data) if isinstance(data, dict) else data
    return {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type
    }

def build_presigned_url_params(bucket, key, expiration=3600):
    \"\"\"Build parameters for generating a presigned URL.\"\"\"
    return {
        'Bucket': bucket,
        'Key': key,
        'ExpiresIn': expiration  # Fix: Should be a reasonable duration
    }

def parse_s3_event(event):
    \"\"\"Parse an S3 event notification.\"\"\"
    # Fix: Handle proper S3 event structure
    records = event.get('Records', [])
    if not records:
        return []
    
    results = []
    for record in records:
        s3 = record.get('s3', {})
        bucket = s3.get('bucket', {}).get('name')
        key = s3.get('object', {}).get('key')
        event_name = record.get('eventName', '')
        results.append({
            'bucket': bucket,
            'key': key,
            'event': event_name
        })
    return results

def build_list_objects_params(bucket, prefix=''):
    \"\"\"Build parameters for listing S3 objects.\"\"\"
    params = {'Bucket': bucket}
    if prefix:
        params['Prefix'] = prefix
    return params
""",
    "test": """import json
from solution import build_put_object_params, build_presigned_url_params, parse_s3_event, build_list_objects_params

def test_put_object_dict():
    result = build_put_object_params('my-bucket', 'data.json', {'key': 'value'})
    assert result['Bucket'] == 'my-bucket'
    assert result['Key'] == 'data.json'
    assert json.loads(result['Body']) == {'key': 'value'}

def test_put_object_string():
    result = build_put_object_params('my-bucket', 'file.txt', 'hello')
    assert result['Body'] == 'hello'

def test_presigned_url():
    result = build_presigned_url_params('my-bucket', 'file.pdf', 7200)
    assert result['Bucket'] == 'my-bucket'
    assert result['Key'] == 'file.pdf'
    assert result['ExpiresIn'] == 7200

def test_parse_s3_event():
    event = {'Records': [{
        's3': {'bucket': {'name': 'my-bucket'}, 'object': {'key': 'uploads/file.csv'}},
        'eventName': 'ObjectCreated:Put'
    }]}
    result = parse_s3_event(event)
    assert len(result) == 1
    assert result[0]['bucket'] == 'my-bucket'
    assert result[0]['key'] == 'uploads/file.csv'

def test_parse_empty_event():
    assert parse_s3_event({}) == []

def test_list_with_prefix():
    result = build_list_objects_params('my-bucket', 'uploads/')
    assert result['Prefix'] == 'uploads/'
""",
})

# ---- Exercise 08: S3 Security ----
EXERCISES.append({
    "dir": "08-s3-security",
    "readme": """# Exercise 08: S3 Security

## Problem
Fix the S3 bucket policy and encryption configuration.

## Running
```bash
python runner.py exercises/08-s3-security
```
""",
    "solution": """import json

def build_bucket_policy_read_only(bucket_name, account_id):
    \"\"\"Build a bucket policy that allows public read access.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'PublicReadGetObject',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }]
    }

def build_encryption_config(kms_key_arn=None):
    \"\"\"Build S3 encryption configuration.\"\"\"
    if kms_key_arn:
        return {
            'Rules': [{
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'aws:kms',
                    'KMSMasterKeyID': kms_key_arn
                }
            }]
        }
    return {
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
        }]
    }

def build_cors_config(allowed_origins=['*']):
    \"\"\"Build S3 CORS configuration.\"\"\"
    return {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST'],
            'AllowedOrigins': allowed_origins,
            'ExposeHeaders': ['ETag'],
            'MaxAgeSeconds': 3600
        }]
    }
""",
    "test": """import json
from solution import build_bucket_policy_read_only, build_encryption_config, build_cors_config

def test_bucket_policy_allows_public_read():
    policy = build_bucket_policy_read_only('my-bucket', '123')
    stmt = policy['Statement'][0]
    assert stmt['Effect'] == 'Allow'
    assert stmt['Principal'] == '*'
    assert stmt['Action'] == 's3:GetObject'
    assert 'my-bucket/*' in stmt['Resource']

def test_sse_kms_encryption():
    config = build_encryption_config('arn:aws:kms:us-east-1:123:key/abc')
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms'
    assert 'KMSMasterKeyID' in rule['ApplyServerSideEncryptionByDefault']

def test_sse_s3_encryption():
    config = build_encryption_config()
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'AES256'

def test_cors_config():
    config = build_cors_config(['https://example.com'])
    rule = config['CORSRules'][0]
    assert 'GET' in rule['AllowedMethods']
    assert rule['AllowedOrigins'] == ['https://example.com']
""",
})

# ---- Exercise 09: SQS Messaging ----
EXERCISES.append({
    "dir": "09-sqs-messaging",
    "readme": """# Exercise 09: SQS Messaging

## Problem
Fix the SQS helper functions for sending and receiving messages.

## Running
```bash
python runner.py exercises/09-sqs-messaging
```
""",
    "solution": """import json

def build_send_message_params(queue_url, message_body, delay_seconds=0, group_id=None):
    \"\"\"Build SQS send_message parameters.\"\"\"
    params = {
        'QueueUrl': queue_url,
        'MessageBody': json.dumps(message_body) if isinstance(message_body, dict) else message_body,
        'DelaySeconds': delay_seconds
    }
    # Fix: Add FIFO-specific attributes when group_id provided
    if group_id:
        params['MessageGroupId'] = group_id
        params['MessageDeduplicationId'] = str(hash(json.dumps(message_body, sort_keys=True)))
    return params

def process_sqs_event(event):
    \"\"\"Process SQS event from Lambda trigger.\"\"\"
    results = []
    for record in event.get('Records', []):
        # Fix: Parse the body as JSON
        body = json.loads(record['body'])
        message_id = record['messageId']
        receipt_handle = record['receiptHandle']
        results.append({
            'message_id': message_id,
            'receipt_handle': receipt_handle,
            'body': body
        })
    return results

def build_queue_attributes(visibility_timeout=30, retention_period=1209600):
    \"\"\"Build SQS queue attributes.\"\"\"
    return {
        'VisibilityTimeout': str(visibility_timeout),
        'MessageRetentionPeriod': str(retention_period),
        'DelaySeconds': '0'
    }

def build_dlq_config(dlq_arn, max_receive_count=5):
    \"\"\"Build redrive policy for DLQ.\"\"\"
    return {
        'RedrivePolicy': json.dumps({
            'deadLetterTargetArn': dlq_arn,
            'maxReceiveCount': str(max_receive_count)
        })
    }
""",
    "test": """import json
from solution import build_send_message_params, process_sqs_event, build_queue_attributes, build_dlq_config

def test_send_message_dict():
    result = build_send_message_params('https://sqs.us-east-1.amazonaws.com/123/my-queue', {'key': 'value'})
    assert result['QueueUrl'] == 'https://sqs.us-east-1.amazonaws.com/123/my-queue'
    assert json.loads(result['MessageBody']) == {'key': 'value'}

def test_send_fifo_message():
    result = build_send_message_params('url', {'key': 'value'}, group_id='group-1')
    assert result['MessageGroupId'] == 'group-1'
    assert 'MessageDeduplicationId' in result

def test_process_sqs_event():
    event = {'Records': [
        {'messageId': 'msg-1', 'receiptHandle': 'handle-1', 'body': json.dumps({'id': 1})},
        {'messageId': 'msg-2', 'receiptHandle': 'handle-2', 'body': json.dumps({'id': 2})}
    ]}
    results = process_sqs_event(event)
    assert len(results) == 2
    assert results[0]['body']['id'] == 1

def test_dlq_config():
    result = build_dlq_config('arn:aws:sqs:us-east-1:123:my-dlq', 3)
    policy = json.loads(result['RedrivePolicy'])
    assert policy['deadLetterTargetArn'] == 'arn:aws:sqs:us-east-1:123:my-dlq'
    assert policy['maxReceiveCount'] == '3'
""",
})

# ---- Exercise 10: SNS Pub/Sub ----
EXERCISES.append({
    "dir": "10-sns-pubsub",
    "readme": """# Exercise 10: SNS Pub/Sub

## Problem
Fix the SNS helper functions for publishing and subscribing.

## Running
```bash
python runner.py exercises/10-sns-pubsub
```
""",
    "solution": """import json

def build_publish_params(topic_arn, message, subject=None, attributes=None):
    \"\"\"Build SNS publish parameters.\"\"\"
    params = {
        'TopicArn': topic_arn,
        'Message': json.dumps(message) if isinstance(message, dict) else message
    }
    if subject:
        params['Subject'] = subject
    if attributes:
        msg_attrs = {}
        for key, value in attributes.items():
            msg_attrs[key] = {
                'DataType': 'String',
                'StringValue': str(value)
            }
        params['MessageAttributes'] = msg_attrs
    return params

def build_sqs_subscription(topic_arn, queue_arn):
    \"\"\"Build params to subscribe SQS queue to SNS topic.\"\"\"
    return {
        'TopicArn': topic_arn,
        'Protocol': 'sqs',
        'Endpoint': queue_arn
    }

def build_filter_policy(filter_rules):
    \"\"\"Build SNS subscription filter policy.\"\"\"
    policy = {}
    for attr, values in filter_rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    return {'FilterPolicy': json.dumps(policy)}

def parse_sns_event(event):
    \"\"\"Parse SNS event from Lambda trigger.\"\"\"
    results = []
    for record in event.get('Records', []):
        sns = record.get('Sns', {})
        results.append({
            'message': sns.get('Message'),
            'subject': sns.get('Subject'),
            'message_id': sns.get('MessageId')
        })
    return results
""",
    "test": """import json
from solution import build_publish_params, build_sqs_subscription, build_filter_policy, parse_sns_event

def test_publish_with_attributes():
    result = build_publish_params('arn:aws:sns:us-east-1:123:topic', {'event': 'order'}, attributes={'type': 'order'})
    assert result['TopicArn'] == 'arn:aws:sns:us-east-1:123:topic'
    assert result['MessageAttributes']['type']['DataType'] == 'String'

def test_sqs_subscription():
    result = build_sqs_subscription('arn:aws:sns:us-east-1:123:topic', 'arn:aws:sqs:us-east-1:123:queue')
    assert result['Protocol'] == 'sqs'
    assert result['Endpoint'] == 'arn:aws:sqs:us-east-1:123:queue'

def test_filter_policy():
    result = build_filter_policy({'event_type': ['order', 'payment']})
    policy = json.loads(result['FilterPolicy'])
    assert 'event_type' in policy
    assert 'order' in policy['event_type']

def test_parse_sns_event():
    event = {'Records': [{'Sns': {'Message': json.dumps({'id': 1}), 'Subject': 'Test', 'MessageId': 'msg-1'}}]}
    results = parse_sns_event(event)
    assert len(results) == 1
    assert results[0]['subject'] == 'Test'
""",
})

# ---- Exercise 11: Kinesis ----
EXERCISES.append({
    "dir": "11-kinesis-streams",
    "readme": """# Exercise 11: Kinesis Streams

## Problem
Fix the Kinesis producer and consumer functions.

## Running
```bash
python runner.py exercises/11-kinesis-streams
```
""",
    "solution": """import json
import base64

def build_put_record_params(stream_name, data, partition_key):
    \"\"\"Build Kinesis put_record parameters.\"\"\"
    body = json.dumps(data) if isinstance(data, dict) else data
    return {
        'StreamName': stream_name,
        'Data': body.encode('utf-8') if isinstance(body, str) else body,
        'PartitionKey': partition_key
    }

def parse_kinesis_event(event):
    \"\"\"Parse Kinesis event from Lambda trigger.\"\"\"
    results = []
    for record in event.get('Records', []):
        kinesis = record.get('kinesis', {})
        data = kinesis.get('data', '')
        # Fix: Base64 decode the data
        decoded = base64.b64decode(data).decode('utf-8')
        results.append({
            'data': json.loads(decoded),
            'partition_key': kinesis.get('partitionKey'),
            'sequence_number': kinesis.get('sequenceNumber')
        })
    return results

def calculate_shards(throughput_mb_per_sec):
    \"\"\"Calculate number of shards needed.\"\"\"
    # Each shard supports 1 MB/s input
    return max(1, int(throughput_mb_per_sec))
""",
    "test": """import json
import base64
from solution import build_put_record_params, parse_kinesis_event, calculate_shards

def test_put_record():
    result = build_put_record_params('my-stream', {'event': 'click'}, 'user-123')
    assert result['StreamName'] == 'my-stream'
    assert result['PartitionKey'] == 'user-123'

def test_parse_kinesis_event():
    encoded = base64.b64encode(json.dumps({'id': 1}).encode()).decode()
    event = {'Records': [{
        'kinesis': {
            'data': encoded,
            'partitionKey': 'user-1',
            'sequenceNumber': 'seq-1'
        }
    }]}
    results = parse_kinesis_event(event)
    assert results[0]['data']['id'] == 1
    assert results[0]['partition_key'] == 'user-1'

def test_calculate_shards():
    assert calculate_shards(1) == 1
    assert calculate_shards(5) == 5
    assert calculate_shards(0.5) == 1
""",
})

# ---- Exercise 12: ElastiCache ----
EXERCISES.append({
    "dir": "12-elasticache",
    "readme": """# Exercise 12: ElastiCache Patterns

## Problem
Implement caching patterns (lazy loading, write-through).

## Running
```bash
python runner.py exercises/12-elasticache
```
""",
    "solution": """import json
import time

class SimpleCache:
    \"\"\"Simple in-memory cache simulating ElastiCache.\"\"\"
    
    def __init__(self):
        self._store = {}
        self._ttl = {}
    
    def get(self, key):
        if key in self._store:
            if self._ttl.get(key, float('inf')) > time.time():
                return self._store[key]
            else:
                del self._store[key]
                self._ttl.pop(key, None)
        return None
    
    def set(self, key, value, ttl_seconds=3600):
        self._store[key] = value
        self._ttl[key] = time.time() + ttl_seconds
    
    def delete(self, key):
        self._store.pop(key, None)
        self._ttl.pop(key, None)

# Simulated database
_mock_db = {}

def mock_db_get(user_id):
    \"\"\"Simulate a database read.\"\"\"
    return _mock_db.get(user_id)

def mock_db_set(user_id, data):
    \"\"\"Simulate a database write.\"\"\"
    _mock_db[user_id] = data

cache = SimpleCache()

def get_user_with_cache(user_id):
    \"\"\"Lazy loading pattern: check cache first, then DB.\"\"\"
    # Fix: Check cache first
    cached = cache.get(f'user:{user_id}')
    if cached:
        return cached
    
    # Cache miss - get from DB
    user = mock_db_get(user_id)
    if user:
        cache.set(f'user:{user_id}', user, ttl_seconds=3600)
    return user

def save_user_with_cache(user_id, data):
    \"\"\"Write-through pattern: update both cache and DB.\"\"\"
    # Fix: Write to both cache and DB
    mock_db_set(user_id, data)
    cache.set(f'user:{user_id}', data, ttl_seconds=3600)
    return data
""",
    "test": """from solution import get_user_with_cache, save_user_with_cache, cache, _mock_db

def setup():
    _mock_db.clear()
    cache._store.clear()
    cache._ttl.clear()

def test_lazy_loading():
    setup()
    _mock_db['user-1'] = {'id': 'user-1', 'name': 'Alice'}
    
    # First call - cache miss, reads from DB
    result = get_user_with_cache('user-1')
    assert result['name'] == 'Alice'
    
    # Second call - cache hit
    result2 = get_user_with_cache('user-1')
    assert result2['name'] == 'Alice'

def test_write_through():
    setup()
    save_user_with_cache('user-2', {'id': 'user-2', 'name': 'Bob'})
    
    # Should be in cache
    cached = cache.get('user:user-2')
    assert cached['name'] == 'Bob'
    
    # Should be in DB
    db_result = _mock_db.get('user-2')
    assert db_result['name'] == 'Bob'

def test_cache_miss_returns_none():
    setup()
    result = get_user_with_cache('nonexistent')
    assert result is None
""",
})

# ---- Exercise 13: Step Functions ----
EXERCISES.append({
    "dir": "13-step-functions",
    "readme": """# Exercise 13: Step Functions

## Problem
Build and fix Step Functions state machine definitions (ASL).

## Running
```bash
python runner.py exercises/13-step-functions
```
""",
    "solution": """import json

def build_order_workflow(order_function_arn, inventory_function_arn, ship_function_arn):
    \"\"\"Build an order processing state machine.\"\"\"
    return {
        'Comment': 'Order processing workflow',
        'StartAt': 'ValidateOrder',
        'States': {
            'ValidateOrder': {
                'Type': 'Task',
                'Resource': order_function_arn,
                'Next': 'CheckInventory'
            },
            'CheckInventory': {
                'Type': 'Task',
                'Resource': inventory_function_arn,
                'Retry': [{
                    'ErrorEquals': ['States.TaskFailed'],
                    'IntervalSeconds': 2,
                    'MaxAttempts': 3,
                    'BackoffRate': 2.0
                }],
                'Catch': [{
                    'ErrorEquals': ['States.ALL'],
                    'Next': 'OrderFailed'
                }],
                'Next': 'InStock?'
            },
            'InStock?': {
                'Type': 'Choice',
                'Choices': [{
                    'Variable': '$.inStock',
                    'BooleanEquals': True,
                    'Next': 'ShipOrder'
                }],
                'Default': 'Backorder'
            },
            'ShipOrder': {
                'Type': 'Task',
                'Resource': ship_function_arn,
                'End': True
            },
            'Backorder': {
                'Type': 'Fail',
                'Error': 'OutOfStock',
                'Cause': 'Item not in stock'
            },
            'OrderFailed': {
                'Type': 'Fail',
                'Error': 'OrderFailed',
                'Cause': 'Could not check inventory'
            }
        }
    }

def validate_state_machine(definition):
    \"\"\"Validate a state machine definition.\"\"\"
    errors = []
    
    if 'StartAt' not in definition:
        errors.append('Missing StartAt')
    
    if 'States' not in definition:
        errors.append('Missing States')
        return errors
    
    states = definition['States']
    start = definition.get('StartAt')
    
    if start not in states:
        errors.append(f'StartAt state "{start}" not found in States')
    
    for name, state in states.items():
        if 'Type' not in state:
            errors.append(f'State "{name}" missing Type')
        elif state['Type'] == 'Task' and 'Resource' not in state:
            errors.append(f'Task state "{name}" missing Resource')
        elif state['Type'] == 'Choice' and 'Choices' not in state:
            errors.append(f'Choice state "{name}" missing Choices')
    
    return errors
""",
    "test": """import json
from solution import build_order_workflow, validate_state_machine

def test_workflow_structure():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    assert wf['StartAt'] == 'ValidateOrder'
    assert 'States' in wf
    assert len(wf['States']) == 5

def test_choice_state():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    choice = wf['States']['InStock?']
    assert choice['Type'] == 'Choice'
    assert len(choice['Choices']) == 1

def test_retry_config():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    check = wf['States']['CheckInventory']
    assert 'Retry' in check
    assert check['Retry'][0]['MaxAttempts'] == 3

def test_catch_block():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    check = wf['States']['CheckInventory']
    assert 'Catch' in check

def test_validate_good_definition():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    errors = validate_state_machine(wf)
    assert len(errors) == 0

def test_validate_bad_definition():
    errors = validate_state_machine({})
    assert len(errors) > 0

def test_fail_states():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    assert wf['States']['Backorder']['Type'] == 'Fail'
    assert wf['States']['OrderFailed']['Type'] == 'Fail'
""",
})

# ---- Exercise 14: ECS & Fargate ----
EXERCISES.append({
    "dir": "14-ecs-fargate",
    "readme": """# Exercise 14: ECS & Fargate

## Problem
Fix the ECS task definition and service configuration.

## Running
```bash
python runner.py exercises/14-ecs-fargate
```
""",
    "solution": """import json

def build_task_definition(family, image, cpu, memory, container_port, role_arn, exec_role_arn):
    \"\"\"Build an ECS Fargate task definition.\"\"\"
    return {
        'family': family,
        'networkMode': 'awsvpc',
        'requiresCompatibilities': ['FARGATE'],
        'cpu': str(cpu),
        'memory': str(memory),
        'taskRoleArn': role_arn,
        'executionRoleArn': exec_role_arn,
        'containerDefinitions': [{
            'name': family,
            'image': image,
            'essential': True,
            'portMappings': [{'containerPort': container_port, 'protocol': 'tcp'}],
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': f'/ecs/{family}',
                    'awslogs-region': 'us-east-1',
                    'awslogs-stream-prefix': 'ecs'
                }
            }
        }]
    }

def build_service_config(cluster, service_name, task_def, desired_count, subnet_ids, sg_ids):
    \"\"\"Build ECS service configuration.\"\"\"
    return {
        'cluster': cluster,
        'serviceName': service_name,
        'taskDefinition': task_def,
        'desiredCount': desired_count,
        'launchType': 'FARGATE',
        'networkConfiguration': {
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': sg_ids,
                'assignPublicIp': 'ENABLED'
            }
        }
    }

def get_fargate_cpu_memory_options():
    \"\"\"Return valid Fargate CPU/memory combinations.\"\"\"
    return {
        '256': ['512', '1024', '2048'],
        '512': ['1024', '2048', '3072', '4096'],
        '1024': ['2048', '3072', '4096', '5120', '6144', '7168', '8192'],
        '2048': ['4096', '5120', '6144', '7168', '8192', '9216', '10240', '11264', '12288', '13312', '14336', '15360', '16384'],
    }
""",
    "test": """from solution import build_task_definition, build_service_config, get_fargate_cpu_memory_options

def test_task_definition():
    td = build_task_definition('my-app', '123456.dkr.ecr.us-east-1.amazonaws.com/my-app:latest', 256, 512, 8080, 'role-arn', 'exec-role-arn')
    assert td['family'] == 'my-app'
    assert td['networkMode'] == 'awsvpc'
    assert 'FARGATE' in td['requiresCompatibilities']
    assert td['cpu'] == '256'
    assert td['memory'] == '512'
    assert len(td['containerDefinitions']) == 1

def test_container_definition():
    td = build_task_definition('my-app', 'image', 256, 512, 8080, 'role', 'exec-role')
    container = td['containerDefinitions'][0]
    assert container['essential'] == True
    assert container['portMappings'][0]['containerPort'] == 8080
    assert container['logConfiguration']['logDriver'] == 'awslogs'

def test_service_config():
    svc = build_service_config('my-cluster', 'my-service', 'my-app:1', 2, ['subnet-1'], ['sg-1'])
    assert svc['launchType'] == 'FARGATE'
    assert svc['desiredCount'] == 2
    assert svc['networkConfiguration']['awsvpcConfiguration']['subnets'] == ['subnet-1']

def test_fargate_options():
    opts = get_fargate_cpu_memory_options()
    assert '256' in opts
    assert '512' in opts['256']
""",
})

# ---- Exercise 15: IAM Policies ----
EXERCISES.append({
    "dir": "15-iam-policies",
    "readme": """# Exercise 15: IAM Policies

## Problem
Fix and create IAM policies following least privilege.

## Running
```bash
python runner.py exercises/15-iam-policies
```
""",
    "solution": """import json

def build_lambda_s3_policy(bucket_name):
    \"\"\"Build least-privilege policy for Lambda to read S3 bucket.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': [
                's3:GetObject',
                's3:ListBucket'
            ],
            'Resource': [
                f'arn:aws:s3:::{bucket_name}',
                f'arn:aws:s3:::{bucket_name}/*'
            ]
        }]
    }

def build_lambda_dynamodb_policy(table_arn):
    \"\"\"Build least-privilege policy for Lambda to access DynamoDB.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': [
                'dynamodb:GetItem',
                'dynamodb:PutItem',
                'dynamodb:UpdateItem',
                'dynamodb:Query',
                'dynamodb:Scan'
            ],
            'Resource': table_arn
        }]
    }

def check_least_privilege(policy):
    \"\"\"Check if a policy follows least privilege (no wildcards in actions).\"\"\"
    issues = []
    for stmt in policy.get('Statement', []):
        actions = stmt.get('Action', [])
        if isinstance(actions, str):
            actions = [actions]
        resources = stmt.get('Resource', [])
        if isinstance(resources, str):
            resources = [resources]
        
        for action in actions:
            if action == '*' or action.endswith(':*'):
                issues.append(f'Overly permissive action: {action}')
        for resource in resources:
            if resource == '*':
                issues.append(f'Overly permissive resource: {resource}')
    return issues

def build_cross_account_role_trust(trusted_account_id):
    \"\"\"Build a trust policy for cross-account access.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'AWS': f'arn:aws:iam::{trusted_account_id}:root'},
            'Action': 'sts:AssumeRole'
        }]
    }
""",
    "test": """import json
from solution import build_lambda_s3_policy, build_lambda_dynamodb_policy, check_least_privilege, build_cross_account_role_trust

def test_s3_policy_least_privilege():
    policy = build_lambda_s3_policy('my-bucket')
    issues = check_least_privilege(policy)
    assert len(issues) == 0

def test_s3_policy_scopes_to_bucket():
    policy = build_lambda_s3_policy('my-bucket')
    stmt = policy['Statement'][0]
    assert all('my-bucket' in r for r in stmt['Resource'])

def test_dynamodb_policy_least_privilege():
    policy = build_lambda_dynamodb_policy('arn:aws:dynamodb:us-east-1:123:table/MyTable')
    issues = check_least_privilege(policy)
    assert len(issues) == 0

def test_detects_overly_permissive():
    bad_policy = {'Statement': [{'Effect': 'Allow', 'Action': '*', 'Resource': '*'}]}
    issues = check_least_privilege(bad_policy)
    assert len(issues) >= 2

def test_cross_account_trust():
    trust = build_cross_account_role_trust('999999999999')
    stmt = trust['Statement'][0]
    assert '999999999999' in stmt['Principal']['AWS']
    assert stmt['Action'] == 'sts:AssumeRole'
""",
})

# ---- Exercise 16: IAM Roles & STS ----
EXERCISES.append({
    "dir": "16-iam-roles",
    "readme": """# Exercise 16: IAM Roles & STS

## Problem
Fix the STS AssumeRole and role configuration.

## Running
```bash
python runner.py exercises/16-iam-roles
```
""",
    "solution": """import json

def build_lambda_trust_policy():
    \"\"\"Build trust policy for Lambda service.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'lambda.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    }

def build_ecs_trust_policy():
    \"\"\"Build trust policy for ECS tasks.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'ecs-tasks.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    }

def build_assume_role_policy(source_account, role_arn):
    \"\"\"Build IAM policy allowing a user to assume a role.\"\"\"
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': 'sts:AssumeRole',
            'Resource': role_arn
        }]
    }

def extract_temp_credentials(sts_response):
    \"\"\"Extract credentials from STS assume_role response.\"\"\"
    creds = sts_response['Credentials']
    return {
        'access_key_id': creds['AccessKeyId'],
        'secret_access_key': creds['SecretAccessKey'],
        'session_token': creds['SessionToken'],
        'expiration': creds['Expiration']
    }
""",
    "test": """import json
from solution import build_lambda_trust_policy, build_ecs_trust_policy, build_assume_role_policy, extract_temp_credentials

def test_lambda_trust():
    trust = build_lambda_trust_policy()
    stmt = trust['Statement'][0]
    assert stmt['Principal']['Service'] == 'lambda.amazonaws.com'

def test_ecs_trust():
    trust = build_ecs_trust_policy()
    stmt = trust['Statement'][0]
    assert stmt['Principal']['Service'] == 'ecs-tasks.amazonaws.com'

def test_assume_role_policy():
    policy = build_assume_role_policy('111111', 'arn:aws:iam::999999:role/Target')
    stmt = policy['Statement'][0]
    assert stmt['Action'] == 'sts:AssumeRole'
    assert stmt['Resource'] == 'arn:aws:iam::999999:role/Target'

def test_extract_credentials():
    response = {'Credentials': {
        'AccessKeyId': 'AKIA...',
        'SecretAccessKey': 'secret',
        'SessionToken': 'token',
        'Expiration': '2024-01-15T12:00:00Z'
    }}
    creds = extract_temp_credentials(response)
    assert creds['access_key_id'] == 'AKIA...'
    assert creds['session_token'] == 'token'
""",
})

# ---- Exercise 17: Cognito Auth ----
EXERCISES.append({
    "dir": "17-cognito-auth",
    "readme": """# Exercise 17: Cognito Authentication

## Problem
Fix the Cognito authentication flow helpers.

## Running
```bash
python runner.py exercises/17-cognito-auth
```
""",
    "solution": """import json

def build_user_pool_config(pool_name, password_policy=None):
    \"\"\"Build Cognito User Pool configuration.\"\"\"
    config = {
        'PoolName': pool_name,
        'Policies': {
            'PasswordPolicy': password_policy or {
                'MinimumLength': 8,
                'RequireUppercase': True,
                'RequireLowercase': True,
                'RequireNumbers': True,
                'RequireSymbols': True
            }
        },
        'AutoVerifiedAttributes': ['email']
    }
    return config

def build_app_client_config(pool_id, client_name, callback_urls, logout_urls):
    \"\"\"Build Cognito User Pool Client configuration.\"\"\"
    return {
        'UserPoolId': pool_id,
        'ClientName': client_name,
        'CallbackURLs': callback_urls,
        'LogoutURLs': logout_urls,
        'AllowedOAuthFlows': ['code'],
        'AllowedOAuthScopes': ['openid', 'email', 'profile'],
        'SupportedIdentityProviders': ['COGNITO']
    }

def parse_cognito_event(event):
    \"\"\"Parse Cognito authorizer event from API Gateway.\"\"\"
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    return {
        'user_id': claims.get('sub'),
        'email': claims.get('email'),
        'groups': claims.get('cognito:groups', '').split(',') if claims.get('cognito:groups') else []
    }

def build_identity_pool_config(pool_name, user_pool_id, app_client_id):
    \"\"\"Build Cognito Identity Pool configuration.\"\"\"
    return {
        'IdentityPoolName': pool_name,
        'AllowUnauthenticatedIdentities': False,
        'CognitoIdentityProviders': [{
            'ProviderName': f'cognito-idp.us-east-1.amazonaws.com/{user_pool_id}',
            'ClientId': app_client_id
        }]
    }
""",
    "test": """import json
from solution import build_user_pool_config, build_app_client_config, parse_cognito_event, build_identity_pool_config

def test_user_pool_config():
    config = build_user_pool_config('MyAppPool')
    assert config['PoolName'] == 'MyAppPool'
    assert config['Policies']['PasswordPolicy']['MinimumLength'] == 8

def test_app_client_config():
    config = build_app_client_config('pool-1', 'web-client', ['https://example.com/callback'], ['https://example.com/logout'])
    assert config['UserPoolId'] == 'pool-1'
    assert 'code' in config['AllowedOAuthFlows']

def test_parse_cognito_event():
    event = {'requestContext': {'authorizer': {'claims': {
        'sub': 'user-123', 'email': 'test@example.com', 'cognito:groups': 'admin,dev'
    }}}}
    result = parse_cognito_event(event)
    assert result['user_id'] == 'user-123'
    assert result['email'] == 'test@example.com'
    assert 'admin' in result['groups']

def test_identity_pool():
    config = build_identity_pool_config('MyIdPool', 'us-east-1_abc', 'client-123')
    assert config['AllowUnauthenticatedIdentities'] == False
    assert len(config['CognitoIdentityProviders']) == 1
""",
})

# ---- Exercise 18: KMS Encryption ----
EXERCISES.append({
    "dir": "18-kms-encryption",
    "readme": """# Exercise 18: KMS Encryption

## Problem
Fix the KMS encryption and key management functions.

## Running
```bash
python runner.py exercises/18-kms-encryption
```
""",
    "solution": """import json

def build_kms_key_policy(account_id, allowed_roles=None):
    \"\"\"Build a KMS key policy.\"\"\"
    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'EnableRootAccountAccess',
                'Effect': 'Allow',
                'Principal': {'AWS': f'arn:aws:iam::{account_id}:root'},
                'Action': 'kms:*',
                'Resource': '*'
            }
        ]
    }
    if allowed_roles:
        policy['Statement'].append({
            'Sid': 'AllowRoleAccess',
            'Effect': 'Allow',
            'Principal': {'AWS': allowed_roles},
            'Action': ['kms:Encrypt', 'kms:Decrypt', 'kms:GenerateDataKey'],
            'Resource': '*'
        })
    return policy

def determine_encryption_method(data_size_kb):
    \"\"\"Determine encryption method based on data size.\"\"\"
    # KMS direct encryption limit is 4KB
    if data_size_kb <= 4:
        return {
            'method': 'direct',
            'description': 'Use KMS Encrypt/Decrypt directly',
            'api': 'kms.encrypt()'
        }
    else:
        return {
            'method': 'envelope',
            'description': 'Use envelope encryption with GenerateDataKey',
            'api': 'kms.generate_data_key()'
        }

def build_s3_kms_config(kms_key_id):
    \"\"\"Build S3 encryption configuration with KMS.\"\"\"
    return {
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'aws:kms',
                'KMSMasterKeyID': kms_key_id
            },
            'BucketKeyEnabled': True
        }]
    }
""",
    "test": """import json
from solution import build_kms_key_policy, determine_encryption_method, build_s3_kms_config

def test_key_policy_has_root():
    policy = build_kms_key_policy('123456789012')
    assert len(policy['Statement']) >= 1
    assert '123456789012' in policy['Statement'][0]['Principal']['AWS']

def test_key_policy_with_roles():
    policy = build_kms_key_policy('123', ['arn:aws:iam::123:role/LambdaRole'])
    assert len(policy['Statement']) == 2
    role_stmt = policy['Statement'][1]
    assert 'kms:Encrypt' in role_stmt['Action']

def test_direct_encryption_for_small_data():
    result = determine_encryption_method(2)
    assert result['method'] == 'direct'

def test_envelope_for_large_data():
    result = determine_encryption_method(100)
    assert result['method'] == 'envelope'

def test_s3_kms_config():
    config = build_s3_kms_config('alias/my-key')
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms'
    assert rule['BucketKeyEnabled'] == True
""",
})

# ---- Exercise 19: Secrets Management ----
EXERCISES.append({
    "dir": "19-secrets",
    "readme": """# Exercise 19: Secrets Management

## Problem
Fix the secrets management helper functions.

## Running
```bash
python runner.py exercises/19-secrets
```
""",
    "solution": """import json

def build_secret_value(username, password, host, port, database):
    \"\"\"Build a secret value for database credentials.\"\"\"
    return json.dumps({
        'username': username,
        'password': password,
        'host': host,
        'port': str(port),
        'database': database,
        'engine': 'postgres'
    })

def parse_secret(secret_string):
    \"\"\"Parse a secret string into a dictionary.\"\"\"
    return json.loads(secret_string)

def build_ssm_parameter(name, value, param_type='String', description='', kms_key_id=None):
    \"\"\"Build SSM Parameter Store put_parameter parameters.\"\"\"
    params = {
        'Name': name,
        'Value': value,
        'Type': param_type,
        'Description': description,
        'Overwrite': True
    }
    if kms_key_id and param_type == 'SecureString':
        params['KeyId'] = kms_key_id
    return params

def recommend_secrets_service(requirements):
    \"\"\"Recommend Secrets Manager vs Parameter Store based on requirements.\"\"\"
    if requirements.get('auto_rotation'):
        return 'secrets-manager'
    if requirements.get('is_database'):
        return 'secrets-manager'
    if requirements.get('cost_sensitive'):
        return 'parameter-store'
    if requirements.get('needs_encryption') and not requirements.get('auto_rotation'):
        return 'parameter-store'
    return 'secrets-manager'

def build_ecs_secret_reference(name, secret_arn):
    \"\"\"Build ECS task definition secret reference.\"\"\"
    return {'name': name, 'valueFrom': secret_arn}
""",
    "test": """import json
from solution import build_secret_value, parse_secret, build_ssm_parameter, recommend_secrets_service, build_ecs_secret_reference

def test_build_and_parse_secret():
    secret = build_secret_value('admin', 'password123', 'db.example.com', 5432, 'mydb')
    parsed = parse_secret(secret)
    assert parsed['username'] == 'admin'
    assert parsed['host'] == 'db.example.com'

def test_ssm_secure_string():
    params = build_ssm_parameter('/app/db-password', 'secret123', 'SecureString', 'DB Password', 'alias/my-key')
    assert params['Type'] == 'SecureString'
    assert params['KeyId'] == 'alias/my-key'

def test_ssm_plain_string():
    params = build_ssm_parameter('/app/config', 'value', 'String', 'Config')
    assert params['Type'] == 'String'
    assert 'KeyId' not in params

def test_recommend_secrets_manager():
    assert recommend_secrets_service({'auto_rotation': True}) == 'secrets-manager'
    assert recommend_secrets_service({'is_database': True}) == 'secrets-manager'

def test_recommend_parameter_store():
    assert recommend_secrets_service({'cost_sensitive': True}) == 'parameter-store'

def test_ecs_secret_ref():
    ref = build_ecs_secret_reference('DB_PASSWORD', 'arn:aws:secretsmanager:us-east-1:123:secret:my-secret')
    assert ref['name'] == 'DB_PASSWORD'
    assert ref['valueFrom'] == 'arn:aws:secretsmanager:us-east-1:123:secret:my-secret'
""",
})

# ---- Exercise 20: Security Review ----
EXERCISES.append({
    "dir": "20-security-review",
    "readme": """# Exercise 20: Security Review

## Problem
Identify and fix security issues in the given configurations.

## Running
```bash
python runner.py exercises/20-security-review
```
""",
    "solution": """import json

def review_lambda_config(config):
    \"\"\"Review Lambda configuration for security issues.\"\"\"
    issues = []
    
    # Check: Should not use access keys
    if config.get('access_key_id'):
        issues.append('CRITICAL: Access key found in config - use IAM roles instead')
    
    # Check: Should not log secrets
    if 'password' in str(config.get('environment_variables', {})).lower():
        issues.append('HIGH: Potential secret in environment variables - use Secrets Manager')
    
    # Check: Memory should be appropriate
    if config.get('memory_size', 128) > 3008:
        issues.append('LOW: Very high memory allocation')
    
    return issues

def review_s3_config(config):
    \"\"\"Review S3 bucket configuration for security issues.\"\"\"
    issues = []
    
    # Check: Encryption should be enabled
    if not config.get('encryption'):
        issues.append('HIGH: Encryption not enabled')
    
    # Check: Versioning should be enabled
    if not config.get('versioning'):
        issues.append('MEDIUM: Versioning not enabled')
    
    # Check: Public access should be blocked
    if config.get('public_access'):
        issues.append('HIGH: Public access enabled')
    
    return issues

def review_api_gateway_config(config):
    \"\"\"Review API Gateway configuration for security issues.\"\"\"
    issues = []
    
    if not config.get('authorization'):
        issues.append('HIGH: No authorization configured')
    
    if not config.get('throttling'):
        issues.append('MEDIUM: No throttling configured')
    
    if not config.get('waf'):
        issues.append('LOW: WAF not configured')
    
    return issues

def generate_secure_lambda_config():
    \"\"\"Generate a secure Lambda configuration template.\"\"\"
    return {
        'runtime': 'python3.11',
        'memory_size': 256,
        'timeout': 30,
        'environment_variables': {'STAGE': 'prod', 'TABLE_NAME': 'my-table'},
        'vpc_config': {'subnetIds': [], 'securityGroupIds': []},
        'tracing_config': {'mode': 'Active'},
        'use_secrets_manager': True,
        'no_access_keys': True
    }
""",
    "test": """from solution import review_lambda_config, review_s3_config, review_api_gateway_config, generate_secure_lambda_config

def test_detect_access_keys():
    issues = review_lambda_config({'access_key_id': 'AKIA...'})
    assert any('Access key' in i for i in issues)

def test_detect_secrets_in_env():
    issues = review_lambda_config({'environment_variables': {'password': 'secret'}})
    assert any('secret' in i.lower() for i in issues)

def test_detect_no_encryption():
    issues = review_s3_config({})
    assert any('Encryption' in i for i in issues)

def test_detect_public_access():
    issues = review_s3_config({'public_access': True})
    assert any('Public' in i for i in issues)

def test_detect_no_auth():
    issues = review_api_gateway_config({})
    assert any('authorization' in i.lower() for i in issues)

def test_secure_config_template():
    config = generate_secure_lambda_config()
    assert config['use_secrets_manager'] == True
    assert config['no_access_keys'] == True
    assert 'password' not in str(config['environment_variables']).lower()
""",
})

# ---- Exercise 21: CloudFormation Basics ----
EXERCISES.append({
    "dir": "21-cfn-basics",
    "readme": """# Exercise 21: CloudFormation Basics

## Problem
Fix the CloudFormation template for a serverless application.

## Running
```bash
python runner.py exercises/21-cfn-basics
```
""",
    "solution": """import json

def build_lambda_cfn_template(function_name, runtime, handler, code_uri, role_arn):
    \"\"\"Build a CloudFormation template with a Lambda function.\"\"\"
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': f'Lambda function: {function_name}',
        'Resources': {
            function_name: {
                'Type': 'AWS::Lambda::Function',
                'Properties': {
                    'FunctionName': function_name,
                    'Runtime': runtime,
                    'Handler': handler,
                    'Code': {'S3Bucket': code_uri.split('/')[0], 'S3Key': '/'.join(code_uri.split('/')[1:])},
                    'Role': role_arn,
                    'Timeout': 30,
                    'MemorySize': 256
                }
            }
        },
        'Outputs': {
            'FunctionArn': {
                'Description': 'Lambda Function ARN',
                'Value': {'Fn::GetAtt': [function_name, 'Arn']}
            }
        }
    }

def build_s3_cfn_template(bucket_name):
    \"\"\"Build a CloudFormation template with an S3 bucket.\"\"\"
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Resources': {
            'MyBucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {
                    'BucketName': bucket_name,
                    'VersioningConfiguration': {'Status': 'Enabled'}
                }
            }
        },
        'Outputs': {
            'BucketName': {'Value': {'Ref': 'MyBucket'}}
        }
    }
""",
    "test": """from solution import build_lambda_cfn_template, build_s3_cfn_template

def test_lambda_template():
    template = build_lambda_cfn_template('MyFunction', 'python3.11', 'index.handler', 'my-bucket/code.zip', 'role-arn')
    assert template['AWSTemplateFormatVersion'] == '2010-09-09'
    assert 'MyFunction' in template['Resources']
    assert template['Resources']['MyFunction']['Type'] == 'AWS::Lambda::Function'

def test_lambda_outputs():
    template = build_lambda_cfn_template('MyFunction', 'python3.11', 'index.handler', 'my-bucket/code.zip', 'role-arn')
    assert 'FunctionArn' in template['Outputs']

def test_s3_template():
    template = build_s3_cfn_template('my-unique-bucket')
    assert template['Resources']['MyBucket']['Type'] == 'AWS::S3::Bucket'
    assert template['Resources']['MyBucket']['Properties']['VersioningConfiguration']['Status'] == 'Enabled'

def test_s3_outputs():
    template = build_s3_cfn_template('my-bucket')
    assert 'BucketName' in template['Outputs']
""",
})

# ---- Exercise 22-35: Continue with remaining exercises ----
# These are compressed for brevity

# ---- Exercise 22: CloudFormation Advanced ----
EXERCISES.append({
    "dir": "22-cfn-advanced",
    "readme": """# Exercise 22: CloudFormation Advanced

## Problem
Use intrinsic functions and cross-stack references.

## Running
```bash
python runner.py exercises/22-cfn-advanced
```
""",
    "solution": """def build_sub_arn(service, resource, account='123456789012', region='us-east-1'):
    return f'arn:aws:{service}:{region}:{account}:{resource}'

def build_parameter(name, param_type, default=None, allowed_values=None):
    param = {'Type': param_type}
    if default:
        param['Default'] = default
    if allowed_values:
        param['AllowedValues'] = allowed_values
    return {name: param}

def build_output(name, value, export_name=None):
    output = {'Value': value}
    if export_name:
        output['Export'] = {'Name': export_name}
    return {name: output}

def get_intrinsic_function(fn_name, *args):
    functions = {
        'Ref': lambda x: {'Ref': x},
        'GetAtt': lambda x, y: {'Fn::GetAtt': [x, y]},
        'Sub': lambda x: {'Fn::Sub': x},
        'Join': lambda x, y: {'Fn::Join': [x, y]},
        'ImportValue': lambda x: {'Fn::ImportValue': x},
    }
    return functions[fn_name](*args)
""",
    "test": """from solution import build_sub_arn, build_parameter, build_output, get_intrinsic_function

def test_arn_builder():
    arn = build_sub_arn('s3', 'my-bucket')
    assert 's3' in arn
    assert 'my-bucket' in arn

def test_parameter_with_default():
    param = build_parameter('Stage', 'String', default='dev', allowed_values=['dev', 'prod'])
    assert param['Stage']['Default'] == 'dev'
    assert 'prod' in param['Stage']['AllowedValues']

def test_output_with_export():
    output = build_output('BucketName', {'Ref': 'MyBucket'}, export_name='MyApp-Bucket')
    assert 'Export' in output['BucketName']

def test_intrinsic_ref():
    result = get_intrinsic_function('Ref', 'MyBucket')
    assert result == {'Ref': 'MyBucket'}

def test_intrinsic_getatt():
    result = get_intrinsic_function('GetAtt', 'MyFunction', 'Arn')
    assert result == {'Fn::GetAtt': ['MyFunction', 'Arn']}
""",
})

# ---- Exercise 23: SAM Templates ----
EXERCISES.append({
    "dir": "23-sam-templates",
    "readme": """# Exercise 23: SAM Templates

## Problem
Build a SAM template for a serverless application.

## Running
```bash
python runner.py exercises/23-sam-templates
```
""",
    "solution": """def build_sam_function(function_name, runtime, handler, code_uri, events=None, policies=None):
    func = {
        function_name: {
            'Type': 'AWS::Serverless::Function',
            'Properties': {
                'Runtime': runtime,
                'Handler': handler,
                'CodeUri': code_uri
            }
        }
    }
    if events:
        func[function_name]['Properties']['Events'] = events
    if policies:
        func[function_name]['Properties']['Policies'] = policies
    return func

def build_api_event(path, method):
    return {'ApiEvent': {'Type': 'Api', 'Properties': {'Path': path, 'Method': method}}}

def build_sam_template(functions, globals_config=None):
    template = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31',
        'Resources': {}
    }
    if globals_config:
        template['Globals'] = globals_config
    for func in functions:
        template['Resources'].update(func)
    return template
""",
    "test": """from solution import build_sam_function, build_api_event, build_sam_template

def test_sam_function():
    func = build_sam_function('GetItems', 'python3.11', 'app.handler', 'src/')
    assert func['GetItems']['Type'] == 'AWS::Serverless::Function'
    assert func['GetItems']['Properties']['Runtime'] == 'python3.11'

def test_api_event():
    event = build_api_event('/items', 'get')
    assert event['ApiEvent']['Type'] == 'Api'
    assert event['ApiEvent']['Properties']['Method'] == 'get'

def test_full_sam_template():
    func = build_sam_function('GetItems', 'python3.11', 'app.handler', 'src/', 
        events={'GetApi': build_api_event('/items', 'get')})
    template = build_sam_template([func], {'Function': {'Timeout': 30}})
    assert template['Transform'] == 'AWS::Serverless-2016-10-31'
    assert 'Globals' in template
    assert 'GetItems' in template['Resources']
""",
})

# ---- Exercise 24: CI/CD Pipeline ----
EXERCISES.append({
    "dir": "24-cicd-pipeline",
    "readme": """# Exercise 24: CI/CD Pipeline

## Problem
Build a CI/CD pipeline configuration.

## Running
```bash
python runner.py exercises/24-cicd-pipeline
```
""",
    "solution": """def build_buildspec(install_cmds, pre_build_cmds, build_cmds, post_build_cmds, artifacts):
    return {
        'version': 0.2,
        'phases': {
            'install': {'commands': install_cmds},
            'pre_build': {'commands': pre_build_cmds},
            'build': {'commands': build_cmds},
            'post_build': {'commands': post_build_cmds}
        },
        'artifacts': {'files': artifacts}
    }

def build_pipeline_stage(name, actions):
    return {'Name': name, 'Actions': actions}

def build_source_action(name, provider, repo, branch, output_artifact):
    return {
        'Name': name,
        'ActionTypeId': {'Category': 'Source', 'Owner': 'AWS', 'Provider': provider, 'Version': '1'},
        'Configuration': {'RepositoryName': repo, 'BranchName': branch},
        'OutputArtifacts': [{'Name': output_artifact}]
    }

def determine_deployment_strategy(app_type, zero_downtime_required):
    if zero_downtime_required:
        if app_type == 'lambda':
            return 'Canary10Percent5Minutes'
        elif app_type == 'ecs':
            return 'BLUE_GREEN'
        else:
            return 'IMMUTABLE'
    return 'ALL_AT_ONCE'
""",
    "test": """from solution import build_buildspec, build_pipeline_stage, build_source_action, determine_deployment_strategy

def test_buildspec():
    bs = build_buildspec(['pip install -r requirements.txt'], ['pytest'], ['sam build'], ['echo done'], ['packaged.yaml'])
    assert bs['version'] == 0.2
    assert len(bs['phases']['build']['commands']) == 1

def test_source_action():
    action = build_source_action('Source', 'CodeCommit', 'my-repo', 'main', 'SourceCode')
    assert action['ActionTypeId']['Category'] == 'Source'
    assert action['ActionTypeId']['Provider'] == 'CodeCommit'

def test_deployment_strategy():
    assert determine_deployment_strategy('lambda', True) == 'Canary10Percent5Minutes'
    assert determine_deployment_strategy('ecs', True) == 'BLUE_GREEN'
    assert determine_deployment_strategy('lambda', False) == 'ALL_AT_ONCE'
""",
})

# ---- Exercise 25: Elastic Beanstalk ----
EXERCISES.append({
    "dir": "25-elastic-beanstalk",
    "readme": """# Exercise 25: Elastic Beanstalk

## Problem
Configure Elastic Beanstalk deployment settings.

## Running
```bash
python runner.py exercises/25-elastic-beanstalk
```
""",
    "solution": """def recommend_deployment_policy(zero_downtime, capacity_constraint):
    if not zero_downtime:
        return 'AllAtOnce'
    elif capacity_constraint:
        return 'RollingWithAdditionalBatch'
    elif zero_downtime and not capacity_constraint:
        return 'Immutable'
    return 'Rolling'

def build_ebextensions(filename, option_settings=None, resources=None):
    config = {}
    if option_settings:
        config['option_settings'] = option_settings
    if resources:
        config['Resources'] = resources
    return config

def build_health_check_config(path='/health', interval=30):
    return [
        {'namespace': 'aws:elasticbeanstalk:environment:process:default', 'option_name': 'HealthCheckPath', 'value': path},
        {'namespace': 'aws:elasticbeanstalk:environment:process:default', 'option_name': 'HealthCheckInterval', 'value': str(interval)}
    ]
""",
    "test": """from solution import recommend_deployment_policy, build_ebextensions, build_health_check_config

def test_deployment_policy():
    assert recommend_deployment_policy(False, False) == 'AllAtOnce'
    assert recommend_deployment_policy(True, True) == 'RollingWithAdditionalBatch'
    assert recommend_deployment_policy(True, False) == 'Immutable'

def test_ebextensions():
    config = build_ebextensions('01-loadbalancer', option_settings=[{'key': 'value'}])
    assert 'option_settings' in config

def test_health_check():
    hc = build_health_check_config('/api/health', 15)
    assert any('/api/health' in str(s) for s in hc)
""",
})

# ---- Exercise 26: CDK Constructs ----
EXERCISES.append({
    "dir": "26-cdk-constructs",
    "readme": """# Exercise 26: CDK Constructs

## Problem
Build CDK construct definitions.

## Running
```bash
python runner.py exercises/26-cdk-constructs
```
""",
    "solution": """def classify_construct_level(construct_name, properties):
    if 'Cfn' in construct_name:
        return 'L1'
    elif 'grant' in str(properties.get('methods', [])) or 'from_lookup' in str(properties.get('methods', [])):
        return 'L2'
    elif 'pattern' in construct_name.lower() or 'RestApi' in construct_name:
        return 'L3'
    return 'L2'

def identify_cdk_command(description):
    commands = {
        'Initialize a new CDK project': 'cdk init',
        'Generate CloudFormation template': 'cdk synth',
        'Deploy the stack': 'cdk deploy',
        'Compare with deployed stack': 'cdk diff',
        'Destroy the stack': 'cdk destroy',
        'List all stacks': 'cdk list',
    }
    return commands.get(description, 'Unknown')

def build_construct_props(construct_type, props):
    return {'type': construct_type, 'properties': props, 'level': classify_construct_level(construct_type, props)}
""",
    "test": """from solution import classify_construct_level, identify_cdk_command, build_construct_props

def test_l1_construct():
    assert classify_construct_level('CfnBucket', {}) == 'L1'

def test_l2_construct():
    assert classify_construct_level('Bucket', {'methods': ['grantRead']}) == 'L2'

def test_cdk_commands():
    assert identify_cdk_command('Generate CloudFormation template') == 'cdk synth'
    assert identify_cdk_command('Deploy the stack') == 'cdk deploy'

def test_construct_props():
    props = build_construct_props('Function', {'runtime': 'python3.11'})
    assert props['level'] in ['L1', 'L2', 'L3']
""",
})

# ---- Exercise 27: CloudWatch Logs ----
EXERCISES.append({
    "dir": "27-cloudwatch-logs",
    "readme": """# Exercise 27: CloudWatch Logs

## Problem
Build CloudWatch Logs insights queries and metric filters.

## Running
```bash
python runner.py exercises/27-cloudwatch-logs
```
""",
    "solution": """def build_log_insights_query(filter_pattern=None, stats=None, sort_by=None, limit=20):
    parts = []
    if filter_pattern:
        parts.append(f'filter {filter_pattern}')
    if stats:
        parts.append(f'stats {stats}')
    if sort_by:
        parts.append(f'sort {sort_by}')
    parts.append(f'limit {limit}')
    return '\\n| '.join(parts)

def build_metric_filter(filter_pattern, metric_name, namespace, value='1'):
    return {
        'filterPattern': filter_pattern,
        'metricTransformations': [{
            'metricName': metric_name,
            'metricNamespace': namespace,
            'metricValue': value
        }]
    }

def build_log_group_name(service, resource_name):
    return f'/aws/{service}/{resource_name}'
""",
    "test": """from solution import build_log_insights_query, build_metric_filter, build_log_group_name

def test_error_query():
    query = build_log_insights_query('@message like /ERROR/', 'count(*) as errorCount', '@timestamp desc')
    assert 'ERROR' in query
    assert 'count' in query

def test_metric_filter():
    mf = build_metric_filter('ERROR', 'ErrorCount', 'MyApp')
    assert mf['filterPattern'] == 'ERROR'
    assert mf['metricTransformations'][0]['metricName'] == 'ErrorCount'

def test_log_group_name():
    assert build_log_group_name('lambda', 'my-function') == '/aws/lambda/my-function'
""",
})

# ---- Exercise 28: CloudWatch Alarms ----
EXERCISES.append({
    "dir": "28-cloudwatch-alarms",
    "readme": """# Exercise 28: CloudWatch Alarms

## Problem
Configure CloudWatch alarms and metrics.

## Running
```bash
python runner.py exercises/28-cloudwatch-alarms
```
""",
    "solution": """def build_alarm_config(name, metric_name, namespace, threshold, comparison='GreaterThanThreshold',
                         period=300, evaluation_periods=1, statistic='Sum', sns_topic_arn=None):
    config = {
        'AlarmName': name,
        'MetricName': metric_name,
        'Namespace': namespace,
        'Threshold': threshold,
        'ComparisonOperator': comparison,
        'Period': period,
        'EvaluationPeriods': evaluation_periods,
        'Statistic': statistic
    }
    if sns_topic_arn:
        config['AlarmActions'] = [sns_topic_arn]
        config['OKActions'] = [sns_topic_arn]
    return config

def recommend_alarm_action(service, metric, threshold_exceeded):
    if not threshold_exceeded:
        return 'No action needed'
    if metric in ['Errors', '5XXError', 'Throttles']:
        return 'Page on-call immediately'
    elif metric in ['CPUUtilization', 'MemoryUtilization']:
        return 'Auto-scale the service'
    return 'Send notification'

def build_dashboard_metrics(services):
    widgets = []
    for service in services:
        widgets.append({'type': 'metric', 'title': f'{service} Metrics'})
    return {'widgets': widgets}
""",
    "test": """from solution import build_alarm_config, recommend_alarm_action, build_dashboard_metrics

def test_alarm_config():
    alarm = build_alarm_config('HighErrors', 'Errors', 'AWS/Lambda', 5, sns_topic_arn='arn:sns:topic')
    assert alarm['Threshold'] == 5
    assert alarm['AlarmActions'] == ['arn:sns:topic']

def test_alarm_no_notification():
    alarm = build_alarm_config('HighCPU', 'CPUUtilization', 'AWS/EC2', 80)
    assert 'AlarmActions' not in alarm

def test_recommend_critical():
    assert recommend_alarm_action('lambda', 'Errors', True) == 'Page on-call immediately'

def test_recommend_no_action():
    assert recommend_alarm_action('lambda', 'Errors', False) == 'No action needed'

def test_dashboard():
    dashboard = build_dashboard_metrics(['Lambda', 'DynamoDB'])
    assert len(dashboard['widgets']) == 2
""",
})

# ---- Exercise 29: X-Ray Tracing ----
EXERCISES.append({
    "dir": "29-xray-tracing",
    "readme": """# Exercise 29: X-Ray Tracing

## Problem
Configure X-Ray tracing and sampling.

## Running
```bash
python runner.py exercises/29-xray-tracing
```
""",
    "solution": """def build_sampling_rule(name, priority, fixed_rate, service_name='*', method='*', path='*', reservoir_size=1):
    return {
        'RuleName': name,
        'Priority': priority,
        'FixedRate': fixed_rate,
        'ReservoirSize': reservoir_size,
        'ServiceName': service_name,
        'HTTPMethod': method,
        'URLPath': path
    }

def identify_trace_component(name, data):
    if 'trace_id' in data or 'TraceId' in data:
        return 'trace'
    elif 'subsegments' in data or 'Subsegments' in data:
        return 'segment'
    elif 'parent_id' in data:
        return 'subsegment'
    return 'unknown'

def build_annotation_search(key, value):
    return {'FilterExpression': f'annotation.{key} = "{value}"'}

def recommend_tracing_config(service_type):
    if service_type == 'lambda':
        return {'ActiveTracing': True, 'SamplingRule': 'default'}
    elif service_type == 'api-gateway':
        return {'TracingEnabled': True}
    elif service_type == 'ecs':
        return {'XRayDaemon': True, 'SamplingRule': 'default'}
    return {'TracingEnabled': True}
""",
    "test": """from solution import build_sampling_rule, identify_trace_component, build_annotation_search, recommend_tracing_config

def test_sampling_rule():
    rule = build_sampling_rule('HighPriority', 1, 1.0, 'payment-service', 'POST', '/api/payments/*', 10)
    assert rule['Priority'] == 1
    assert rule['FixedRate'] == 1.0

def test_identify_trace():
    assert identify_trace_component('x', {'trace_id': 'abc'}) == 'trace'
    assert identify_trace_component('x', {'subsegments': []}) == 'segment'

def test_annotation_search():
    search = build_annotation_search('UserId', 'user-123')
    assert 'UserId' in search['FilterExpression']
    assert 'user-123' in search['FilterExpression']

def test_lambda_tracing():
    config = recommend_tracing_config('lambda')
    assert config['ActiveTracing'] == True
""",
})

# ---- Exercise 30: Troubleshooting ----
EXERCISES.append({
    "dir": "30-troubleshooting",
    "readme": """# Exercise 30: Troubleshooting

## Problem
Diagnose and fix common AWS issues.

## Running
```bash
python runner.py exercises/30-troubleshooting
```
""",
    "solution": """def diagnose_lambda_issue(symptoms):
    if symptoms.get('timeout'):
        if symptoms.get('vpc_enabled') and not symptoms.get('nat_gateway'):
            return 'Lambda in VPC without NAT Gateway cannot reach internet'
        return 'Increase Lambda timeout or optimize code'
    if symptoms.get('throttled'):
        return 'Request concurrent execution limit increase or use SQS buffering'
    if symptoms.get('permission_denied'):
        return 'Check Lambda execution role IAM permissions'
    if symptoms.get('cold_start_slow'):
        return 'Use Provisioned Concurrency or reduce deployment package size'
    return 'Check CloudWatch Logs for details'

def diagnose_api_gateway_issue(status_code, details=None):
    if status_code == 403:
        if details and details.get('cors'):
            return 'Enable CORS in API Gateway and add OPTIONS method'
        return 'Check authorizer configuration'
    if status_code == 502:
        return 'Backend (Lambda) returning error - check Lambda logs'
    if status_code == 504:
        return 'Lambda timeout - increase Lambda timeout (max 30s for API GW REST, 30s for HTTP)'
    if status_code == 429:
        return 'Enable throttling or increase rate limits'
    return 'Check API Gateway access logs'

def diagnose_dynamodb_issue(error_type):
    errors = {
        'ProvisionedThroughputExceededException': 'Switch to on-demand mode or increase RCUs/WCUs',
        'ConditionalCheckFailedException': 'Review your conditional expression logic',
        'ResourceNotFoundException': 'Check table name and region',
        'AccessDeniedException': 'Check IAM permissions for DynamoDB access'
    }
    return errors.get(error_type, 'Check DynamoDB metrics in CloudWatch')
""",
    "test": """from solution import diagnose_lambda_issue, diagnose_api_gateway_issue, diagnose_dynamodb_issue

def test_lambda_vpc_issue():
    result = diagnose_lambda_issue({'timeout': True, 'vpc_enabled': True, 'nat_gateway': False})
    assert 'NAT' in result

def test_lambda_throttle():
    result = diagnose_lambda_issue({'throttled': True})
    assert 'concurrent' in result.lower() or 'SQS' in result

def test_api_502():
    result = diagnose_api_gateway_issue(502)
    assert 'Lambda' in result

def test_api_cors():
    result = diagnose_api_gateway_issue(403, {'cors': True})
    assert 'CORS' in result

def test_dynamodb_throttle():
    result = diagnose_dynamodb_issue('ProvisionedThroughputExceededException')
    assert 'on-demand' in result.lower() or 'RCU' in result

def test_dynamodb_conditional():
    result = diagnose_dynamodb_issue('ConditionalCheckFailedException')
    assert 'conditional' in result.lower()
""",
})

# ---- Exercise 31: Serverless API (Advanced) ----
EXERCISES.append({
    "dir": "31-serverless-api",
    "readme": """# Exercise 31: Serverless API

## Problem
Build a complete serverless API with Lambda, DynamoDB, and API Gateway patterns.

## Running
```bash
python runner.py exercises/31-serverless-api
```
""",
    "solution": """import json

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
""",
    "test": """import json
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
""",
})

# ---- Exercise 32: Event-Driven Architecture ----
EXERCISES.append({
    "dir": "32-event-driven",
    "readme": """# Exercise 32: Event-Driven Architecture

## Problem
Build an event-driven architecture with SNS, SQS, and Lambda.

## Running
```bash
python runner.py exercises/32-event-driven
```
""",
    "solution": """import json

def build_fanout_config(topic_arn, queues):
    return {
        'topic': topic_arn,
        'subscriptions': [{'queue_arn': q, 'protocol': 'sqs'} for q in queues]
    }

def build_sns_filter_policy(rules):
    policy = {}
    for attr, values in rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    return json.dumps(policy)

def build_event_payload(event_type, source, data, metadata=None):
    payload = {
        'event_type': event_type,
        'source': source,
        'data': data,
        'timestamp': '2024-01-15T10:00:00Z'
    }
    if metadata:
        payload['metadata'] = metadata
    return payload

def route_event(event_type, handlers):
    return handlers.get(event_type, handlers.get('default'))
""",
    "test": """import json
from solution import build_fanout_config, build_sns_filter_policy, build_event_payload, route_event

def test_fanout_config():
    config = build_fanout_config('arn:sns:topic', ['arn:sqs:q1', 'arn:sqs:q2'])
    assert len(config['subscriptions']) == 2

def test_filter_policy():
    policy = build_sns_filter_policy({'event_type': ['order_created', 'order_updated']})
    parsed = json.loads(policy)
    assert 'order_created' in parsed['event_type']

def test_event_payload():
    payload = build_event_payload('order_created', 'checkout-service', {'order_id': '123'})
    assert payload['event_type'] == 'order_created'
    assert payload['data']['order_id'] == '123'

def test_route_event():
    handlers = {'order_created': 'process_order', 'default': 'log_event'}
    assert route_event('order_created', handlers) == 'process_order'
    assert route_event('unknown', handlers) == 'log_event'
""",
})

# ---- Exercise 33: Data Pipeline ----
EXERCISES.append({
    "dir": "33-data-pipeline",
    "readme": """# Exercise 33: Data Pipeline

## Problem
Build a data pipeline: S3 -> Lambda -> DynamoDB.

## Running
```bash
python runner.py exercises/33-data-pipeline
```
""",
    "solution": """import json

def parse_csv_line(line):
    return line.strip().split(',')

def transform_record(raw_record):
    return {
        'pk': f'RECORD#{raw_record[0]}',
        'sk': f'DATA#{raw_record[1]}',
        'value': raw_record[2] if len(raw_record) > 2 else '',
        'status': 'processed'
    }

def batch_records(records, batch_size=25):
    return [records[i:i+batch_size] for i in range(0, len(records), batch_size)]

def build_pipeline_processor():
    def processor(event, context):
        results = []
        for record in event.get('Records', []):
            s3 = record.get('s3', {})
            bucket = s3.get('bucket', {}).get('name')
            key = s3.get('object', {}).get('key')
            results.append({'bucket': bucket, 'key': key, 'status': 'queued'})
        return {'statusCode': 200, 'body': json.dumps({'processed': len(results)})}
    return processor
""",
    "test": """import json
from solution import parse_csv_line, transform_record, batch_records, build_pipeline_processor

def test_parse_csv():
    result = parse_csv_line('1,Alice,30')
    assert result == ['1', 'Alice', '30']

def test_transform():
    result = transform_record(['123', 'data', 'value'])
    assert result['pk'] == 'RECORD#123'
    assert result['status'] == 'processed'

def test_batch():
    records = list(range(30))
    batches = batch_records(records, 10)
    assert len(batches) == 3
    assert len(batches[0]) == 10

def test_pipeline_processor():
    processor = build_pipeline_processor()
    event = {'Records': [{'s3': {'bucket': {'name': 'my-bucket'}, 'object': {'key': 'data.csv'}}}]}
    result = processor(event, None)
    assert result['statusCode'] == 200
""",
})

# ---- Exercise 34: Multi-Service Auth ----
EXERCISES.append({
    "dir": "34-multi-auth",
    "readme": """# Exercise 34: Multi-Service Authentication

## Problem
Build authentication flow with Cognito + API Gateway + Lambda.

## Running
```bash
python runner.py exercises/34-multi-auth
```
""",
    "solution": """import json

def build_auth_flow(user_pool_id, client_id, callback_url):
    return {
        'auth_url': f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}/oauth2/authorize',
        'token_url': f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}/oauth2/token',
        'client_id': client_id,
        'callback_url': callback_url,
        'response_type': 'code',
        'scope': 'openid email profile'
    }

def validate_token_claims(claims, required_groups=None):
    if not claims.get('sub'):
        return False, 'Missing subject claim'
    if required_groups:
        user_groups = claims.get('cognito:groups', '').split(',') if claims.get('cognito:groups') else []
        if not any(g in user_groups for g in required_groups):
            return False, 'User not in required group'
    return True, 'Valid'

def build_api_gateway_authorizer(user_pool_arn):
    return {
        'Type': 'COGNITO_USER_POOLS',
        'ProviderARNs': [user_pool_arn]
    }
""",
    "test": """import json
from solution import build_auth_flow, validate_token_claims, build_api_gateway_authorizer

def test_auth_flow():
    flow = build_auth_flow('us-east-1_abc123', 'client-abc', 'https://example.com/callback')
    assert flow['response_type'] == 'code'
    assert 'openid' in flow['scope']

def test_validate_good_claims():
    valid, msg = validate_token_claims({'sub': 'user-123', 'email': 'test@example.com'})
    assert valid == True

def test_validate_missing_sub():
    valid, msg = validate_token_claims({})
    assert valid == False
    assert 'subject' in msg.lower()

def test_validate_group_membership():
    valid, msg = validate_token_claims({'sub': '123', 'cognito:groups': 'admin,dev'}, required_groups=['admin'])
    assert valid == True

def test_validate_missing_group():
    valid, msg = validate_token_claims({'sub': '123', 'cognito:groups': 'viewer'}, required_groups=['admin'])
    assert valid == False

def test_authorizer():
    auth = build_api_gateway_authorizer('arn:aws:cognito-idp:us-east-1:123:userpool/us-east-1_abc')
    assert auth['Type'] == 'COGNITO_USER_POOLS'
""",
})

# ---- Exercise 35: Deployment Pipeline ----
EXERCISES.append({
    "dir": "35-deploy-pipeline",
    "readme": """# Exercise 35: Deployment Pipeline

## Problem
Build a complete deployment pipeline configuration.

## Running
```bash
python runner.py exercises/35-deploy-pipeline
```
""",
    "solution": """import json

def build_codepipeline_config(name, source_repo, source_branch, build_project, deploy_stack):
    return {
        'name': name,
        'stages': [
            {'name': 'Source', 'provider': 'CodeCommit', 'config': {'repo': source_repo, 'branch': source_branch}},
            {'name': 'Build', 'provider': 'CodeBuild', 'config': {'project': build_project}},
            {'name': 'Deploy', 'provider': 'CloudFormation', 'config': {'stack': deploy_stack}}
        ]
    }

def build_buildspec_advanced(test_cmds, build_cmds, package_cmds):
    return {
        'version': 0.2,
        'phases': {
            'install': {'runtime-versions': {'python': '3.11'}},
            'pre_build': {'commands': test_cmds},
            'build': {'commands': build_cmds},
            'post_build': {'commands': package_cmds}
        },
        'artifacts': {'files': ['packaged.yaml']}
    }

def determine_pipeline_stage(failed_stage, error_message):
    if failed_stage == 'Source':
        return 'Check repository and branch configuration'
    elif failed_stage == 'Build':
        if 'test' in error_message.lower():
            return 'Fix failing unit tests'
        return 'Fix build errors'
    elif failed_stage == 'Deploy':
        if 'permission' in error_message.lower():
            return 'Check IAM capabilities and role permissions'
        return 'Check CloudFormation template for errors'
    return 'Check pipeline logs'
""",
    "test": """import json
from solution import build_codepipeline_config, build_buildspec_advanced, determine_pipeline_stage

def test_pipeline_config():
    config = build_codepipeline_config('my-pipeline', 'my-repo', 'main', 'build-proj', 'my-stack')
    assert config['name'] == 'my-pipeline'
    assert len(config['stages']) == 3

def test_buildspec():
    bs = build_buildspec_advanced(['pytest'], ['sam build'], ['sam package'])
    assert bs['version'] == 0.2
    assert 'pytest' in bs['phases']['pre_build']['commands']

def test_diagnose_build_failure():
    result = determine_pipeline_stage('Build', 'test failed: expected 200 got 400')
    assert 'test' in result.lower()

def test_diagnose_deploy_failure():
    result = determine_pipeline_stage('Deploy', 'permission denied')
    assert 'permission' in result.lower() or 'IAM' in result
""",
})


# ============================================================
# Generator
# ============================================================

def generate_all():
    print("Generating exercises...")
    for ex in EXERCISES:
        dir_path = EXERCISES_DIR / ex['dir']
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Write README
        (dir_path / 'README.md').write_text(ex['readme'])
        
        # Write solution
        (dir_path / 'solution.py').write_text(ex['solution'])
        
        # Write test
        (dir_path / 'test.py').write_text(ex['test'])
        
        print(f"  Created: {ex['dir']}")
    
    print(f"\nDone! Generated {len(EXERCISES)} exercises.")

if __name__ == '__main__':
    generate_all()
