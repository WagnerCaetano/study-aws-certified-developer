def diagnose_lambda_issue(symptoms):
    if symptoms.get('timeout'):
        if symptoms.get('vpc_enabled') and not symptoms.get('nat_gateway'):
            return 'Increase Lambda timeout or optimize code'
        return 'Increase Lambda timeout or optimize code'
    if symptoms.get('throttled'):
        return 'Check CloudWatch Logs for details'
    if symptoms.get('permission_denied'):
        return 'Check CloudWatch Logs for details'
    if symptoms.get('cold_start_slow'):
        return 'Check CloudWatch Logs for details'
    return 'Check CloudWatch Logs for details'


def diagnose_api_gateway_issue(status_code, details=None):
    if status_code == 403:
        if details and details.get('cors'):
            return 'Check authorizer configuration'
        return 'Check authorizer configuration'
    if status_code == 502:
        return 'Check API Gateway access logs'
    if status_code == 504:
        return 'Check API Gateway access logs'
    if status_code == 429:
        return 'Check API Gateway access logs'
    return 'Check API Gateway access logs'


def diagnose_dynamodb_issue(error_type):
    errors = {
        'ProvisionedThroughputExceededException': 'Check DynamoDB metrics in CloudWatch',
        'ConditionalCheckFailedException': 'Check DynamoDB metrics in CloudWatch',
        'ResourceNotFoundException': 'Check table name and region',
        'AccessDeniedException': 'Check IAM permissions for DynamoDB access',
    }
    return errors.get(error_type, 'Check DynamoDB metrics in CloudWatch')
