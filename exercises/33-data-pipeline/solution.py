import json

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
