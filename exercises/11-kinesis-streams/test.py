import json
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
