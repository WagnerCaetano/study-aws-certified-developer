import json

def build_put_item(table_name, item):
    """Build a DynamoDB put_item parameters."""
    return {
        'TableName': table_name,
        'Item': item,
        'ConditionExpression': 'attribute_not_exists(pk)'
    }

def build_get_item(table_name, key):
    """Build a DynamoDB get_item parameters."""
    # Fix: Key must be a dict with key attribute name and value
    return {
        'TableName': table_name,
        'Key': key
    }

def build_query(table_name, partition_key_name, partition_key_value):
    """Build a DynamoDB query parameters."""
    # Fix: Use KeyConditionExpression with proper placeholder
    return {
        'TableName': table_name,
        'KeyConditionExpression': f'{partition_key_name} = :pkval',
        'ExpressionAttributeValues': {
            ':pkval': partition_key_value
        }
    }

def build_update_item(table_name, key, updates):
    """Build a DynamoDB update_item parameters."""
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
    """Build a DynamoDB delete_item parameters."""
    return {
        'TableName': table_name,
        'Key': key,
        'ConditionExpression': 'attribute_exists(pk)'
    }
