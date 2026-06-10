import json

def build_put_object_params(bucket, key, data, content_type='application/json'):
    """Build parameters for S3 put_object."""
    body = json.dumps(data) if isinstance(data, dict) else data
    return {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type
    }

def build_presigned_url_params(bucket, key, expiration=3600):
    """Build parameters for generating a presigned URL."""
    return {
        'Bucket': bucket,
        'Key': key,
        'ExpiresIn': expiration  # Fix: Should be a reasonable duration
    }

def parse_s3_event(event):
    """Parse an S3 event notification."""
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
    """Build parameters for listing S3 objects."""
    params = {'Bucket': bucket}
    if prefix:
        params['Prefix'] = prefix
    return params
