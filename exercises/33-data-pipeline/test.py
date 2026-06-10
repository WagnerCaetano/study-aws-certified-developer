import json
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
