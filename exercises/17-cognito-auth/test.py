import json
from solution import build_user_pool_config, build_app_client_config, parse_cognito_event, build_identity_pool_config

def test_user_pool_config():
    config = build_user_pool_config('MyAppPool')
    assert config['PoolName'] == 'MyAppPool'
    assert config['Policies']['PasswordPolicy']['MinimumLength'] == 8

def test_app_client_config():
    config = build_app_client_config('pool-1', 'web-client', ['https://example.com/callback'], ['https://example.com/logout'])
    assert config['UserPoolId'] == 'pool-1'
    assert 'code' in config['AllowedOAuthFlows']

def test_parse_cognito_event():
    event = {'requestContext': {'authorizer': {'claims': {
        'sub': 'user-123', 'email': 'test@example.com', 'cognito:groups': 'admin,dev'
    }}}}
    result = parse_cognito_event(event)
    assert result['user_id'] == 'user-123'
    assert result['email'] == 'test@example.com'
    assert 'admin' in result['groups']

def test_identity_pool():
    config = build_identity_pool_config('MyIdPool', 'us-east-1_abc', 'client-123')
    assert config['AllowUnauthenticatedIdentities'] == False
    assert len(config['CognitoIdentityProviders']) == 1
