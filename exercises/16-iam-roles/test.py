import json
from solution import build_lambda_trust_policy, build_ecs_trust_policy, build_assume_role_policy, extract_temp_credentials

def test_lambda_trust():
    trust = build_lambda_trust_policy()
    stmt = trust['Statement'][0]
    assert stmt['Principal']['Service'] == 'lambda.amazonaws.com'

def test_ecs_trust():
    trust = build_ecs_trust_policy()
    stmt = trust['Statement'][0]
    assert stmt['Principal']['Service'] == 'ecs-tasks.amazonaws.com'

def test_assume_role_policy():
    policy = build_assume_role_policy('111111', 'arn:aws:iam::999999:role/Target')
    stmt = policy['Statement'][0]
    assert stmt['Action'] == 'sts:AssumeRole'
    assert stmt['Resource'] == 'arn:aws:iam::999999:role/Target'

def test_extract_credentials():
    response = {'Credentials': {
        'AccessKeyId': 'AKIA...',
        'SecretAccessKey': 'secret',
        'SessionToken': 'token',
        'Expiration': '2024-01-15T12:00:00Z'
    }}
    creds = extract_temp_credentials(response)
    assert creds['access_key_id'] == 'AKIA...'
    assert creds['session_token'] == 'token'
