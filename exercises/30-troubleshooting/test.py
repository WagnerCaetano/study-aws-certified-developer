from solution import diagnose_lambda_issue, diagnose_api_gateway_issue, diagnose_dynamodb_issue

def test_lambda_vpc_issue():
    result = diagnose_lambda_issue({'timeout': True, 'vpc_enabled': True, 'nat_gateway': False})
    assert 'NAT' in result

def test_lambda_throttle():
    result = diagnose_lambda_issue({'throttled': True})
    assert 'concurrent' in result.lower() or 'SQS' in result

def test_api_502():
    result = diagnose_api_gateway_issue(502)
    assert 'Lambda' in result

def test_api_cors():
    result = diagnose_api_gateway_issue(403, {'cors': True})
    assert 'CORS' in result

def test_dynamodb_throttle():
    result = diagnose_dynamodb_issue('ProvisionedThroughputExceededException')
    assert 'on-demand' in result.lower() or 'RCU' in result

def test_dynamodb_conditional():
    result = diagnose_dynamodb_issue('ConditionalCheckFailedException')
    assert 'conditional' in result.lower()
