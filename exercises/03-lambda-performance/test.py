import json
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
