from solution import design_user_table, design_orders_table, design_orders_by_status

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
