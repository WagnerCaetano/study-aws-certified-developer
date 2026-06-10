import json
from solution import build_lambda_s3_policy, build_lambda_dynamodb_policy, check_least_privilege, build_cross_account_role_trust

def test_s3_policy_least_privilege():
    policy = build_lambda_s3_policy('my-bucket')
    issues = check_least_privilege(policy)
    assert len(issues) == 0

def test_s3_policy_scopes_to_bucket():
    policy = build_lambda_s3_policy('my-bucket')
    stmt = policy['Statement'][0]
    assert all('my-bucket' in r for r in stmt['Resource'])

def test_dynamodb_policy_least_privilege():
    policy = build_lambda_dynamodb_policy('arn:aws:dynamodb:us-east-1:123:table/MyTable')
    issues = check_least_privilege(policy)
    assert len(issues) == 0

def test_detects_overly_permissive():
    bad_policy = {'Statement': [{'Effect': 'Allow', 'Action': '*', 'Resource': '*'}]}
    issues = check_least_privilege(bad_policy)
    assert len(issues) >= 2

def test_cross_account_trust():
    trust = build_cross_account_role_trust('999999999999')
    stmt = trust['Statement'][0]
    assert '999999999999' in stmt['Principal']['AWS']
    assert stmt['Action'] == 'sts:AssumeRole'
