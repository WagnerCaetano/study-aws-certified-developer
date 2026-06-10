import json
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
