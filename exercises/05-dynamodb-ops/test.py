from solution import build_put_item, build_get_item, build_query, build_update_item, build_delete_item

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
