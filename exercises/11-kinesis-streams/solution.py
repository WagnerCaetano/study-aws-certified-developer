import json
import base64

def build_put_record_params(stream_name, data, partition_key):
    """Build Kinesis put_record parameters."""
    body = json.dumps(data) if isinstance(data, dict) else data
    return {
        'StreamName': stream_name,
        'Data': body.encode('utf-8') if isinstance(body, str) else body,
        'PartitionKey': partition_key
    }

def parse_kinesis_event(event):
    """Parse Kinesis event from Lambda trigger."""
    results = []
    for record in event.get('Records', []):
        kinesis = record.get('kinesis', {})
        data = kinesis.get('data', '')
        # Fix: Base64 decode the data
        decoded = base64.b64decode(data).decode('utf-8')
        results.append({
            'data': json.loads(decoded),
            'partition_key': kinesis.get('partitionKey'),
            'sequence_number': kinesis.get('sequenceNumber')
        })
    return results

def calculate_shards(throughput_mb_per_sec):
    """Calculate number of shards needed."""
    # Each shard supports 1 MB/s input
    return max(1, int(throughput_mb_per_sec))
