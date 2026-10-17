import json
import base64

def build_put_record_params(stream_name, data, partition_key):
    """Build Kinesis put_record parameters."""
    body = json.dumps(data) if isinstance(data, dict) else data
    return {
        'StreamName': stream_name,
        'Data': body if isinstance(body, str) else body,
        'Partition': partition_key
    }

def parse_kinesis_event(event):
    """Parse Kinesis event from Lambda trigger."""
    results = []
    for record in event.get('Records', []):
        kinesis = record.get('kinesis', {})
        data = kinesis.get('data', '')
        results.append({
            'data': json.loads(data),
            'partition_key': kinesis.get('partitionKey'),
            'sequence_number': kinesis.get('sequenceNumber')
        })
    return results

def calculate_shards(throughput_mb_per_sec):
    """Calculate number of shards needed."""
    return int(throughput_mb_per_sec)
