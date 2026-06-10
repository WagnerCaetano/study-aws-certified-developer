import json

def build_publish_params(topic_arn, message, subject=None, attributes=None):
    """Build SNS publish parameters."""
    params = {
        'TopicArn': topic_arn,
        'Message': json.dumps(message) if isinstance(message, dict) else message
    }
    if subject:
        params['Subject'] = subject
    if attributes:
        msg_attrs = {}
        for key, value in attributes.items():
            msg_attrs[key] = {
                'DataType': 'String',
                'StringValue': str(value)
            }
        params['MessageAttributes'] = msg_attrs
    return params

def build_sqs_subscription(topic_arn, queue_arn):
    """Build params to subscribe SQS queue to SNS topic."""
    return {
        'TopicArn': topic_arn,
        'Protocol': 'sqs',
        'Endpoint': queue_arn
    }

def build_filter_policy(filter_rules):
    """Build SNS subscription filter policy."""
    policy = {}
    for attr, values in filter_rules.items():
        policy[attr] = values if isinstance(values, list) else [values]
    return {'FilterPolicy': json.dumps(policy)}

def parse_sns_event(event):
    """Parse SNS event from Lambda trigger."""
    results = []
    for record in event.get('Records', []):
        sns = record.get('Sns', {})
        results.append({
            'message': sns.get('Message'),
            'subject': sns.get('Subject'),
            'message_id': sns.get('MessageId')
        })
    return results
