def diagnose_lambda_issue(symptoms):
    if symptoms.get('timeout'):
        if symptoms.get('vpc_enabled') and not symptoms.get('nat_gateway'):
            return 'Lambda in VPC without NAT Gateway cannot reach internet'
        return 'Increase Lambda timeout or optimize code'
    if symptoms.get('throttled'):
        return 'Request concurrent execution limit increase or use SQS buffering'
    if symptoms.get('permission_denied'):
        return 'Check Lambda execution role IAM permissions'
    if symptoms.get('cold_start_slow'):
        return 'Use Provisioned Concurrency or reduce deployment package size'
    return 'Check CloudWatch Logs for details'

def diagnose_api_gateway_issue(status_code, details=None):
    if status_code == 403:
        if details and details.get('cors'):
            return 'Enable CORS in API Gateway and add OPTIONS method'
        return 'Check authorizer configuration'
    if status_code == 502:
        return 'Backend (Lambda) returning error - check Lambda logs'
    if status_code == 504:
        return 'Lambda timeout - increase Lambda timeout (max 30s for API GW REST, 30s for HTTP)'
    if status_code == 429:
        return 'Enable throttling or increase rate limits'
    return 'Check API Gateway access logs'

def diagnose_dynamodb_issue(error_type):
    errors = {
        'ProvisionedThroughputExceededException': 'Switch to on-demand mode or increase RCUs/WCUs',
        'ConditionalCheckFailedException': 'Review your conditional expression logic',
        'ResourceNotFoundException': 'Check table name and region',
        'AccessDeniedException': 'Check IAM permissions for DynamoDB access'
    }
    return errors.get(error_type, 'Check DynamoDB metrics in CloudWatch')
