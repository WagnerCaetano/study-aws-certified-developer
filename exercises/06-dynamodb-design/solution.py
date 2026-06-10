def design_user_table():
    """Design a table for users accessed by userId."""
    return {
        'TableName': 'Users',
        'KeySchema': [{'AttributeName': 'userId', 'KeyType': 'HASH'}],
        'AttributeDefinitions': [{'AttributeName': 'userId', 'AttributeType': 'S'}],
        'BillingMode': 'PAY_PER_REQUEST'
    }

def design_orders_table():
    """Design a table for orders: query by userId, sort by date."""
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
    """Add a GSI to query orders by status."""
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
