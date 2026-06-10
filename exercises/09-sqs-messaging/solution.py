import json

def build_send_message_params(queue_url, message_body, delay_seconds=0, group_id=None):
    """Build SQS send_message parameters."""
    params = {
        'QueueUrl': queue_url,
        'MessageBody': json.dumps(message_body) if isinstance(message_body, dict) else message_body,
        'DelaySeconds': delay_seconds
    }
    # Fix: Add FIFO-specific attributes when group_id provided
    if group_id:
        params['MessageGroupId'] = group_id
        params['MessageDeduplicationId'] = str(hash(json.dumps(message_body, sort_keys=True)))
    return params

def process_sqs_event(event):
    """Process SQS event from Lambda trigger."""
    results = []
    for record in event.get('Records', []):
        # Fix: Parse the body as JSON
        body = json.loads(record['body'])
        message_id = record['messageId']
        receipt_handle = record['receiptHandle']
        results.append({
            'message_id': message_id,
            'receipt_handle': receipt_handle,
            'body': body
        })
    return results

def build_queue_attributes(visibility_timeout=30, retention_period=1209600):
    """Build SQS queue attributes."""
    return {
        'VisibilityTimeout': str(visibility_timeout),
        'MessageRetentionPeriod': str(retention_period),
        'DelaySeconds': '0'
    }

def build_dlq_config(dlq_arn, max_receive_count=5):
    """Build redrive policy for DLQ."""
    return {
        'RedrivePolicy': json.dumps({
            'deadLetterTargetArn': dlq_arn,
            'maxReceiveCount': str(max_receive_count)
        })
    }
