import json
from solution import build_auth_flow, validate_token_claims, build_api_gateway_authorizer

def test_auth_flow():
    flow = build_auth_flow('us-east-1_abc123', 'client-abc', 'https://example.com/callback')
    assert flow['response_type'] == 'code'
    assert 'openid' in flow['scope']

def test_validate_good_claims():
    valid, msg = validate_token_claims({'sub': 'user-123', 'email': 'test@example.com'})
    assert valid == True

def test_validate_missing_sub():
    valid, msg = validate_token_claims({})
    assert valid == False
    assert 'subject' in msg.lower()

def test_validate_group_membership():
    valid, msg = validate_token_claims({'sub': '123', 'cognito:groups': 'admin,dev'}, required_groups=['admin'])
    assert valid == True

def test_validate_missing_group():
    valid, msg = validate_token_claims({'sub': '123', 'cognito:groups': 'viewer'}, required_groups=['admin'])
    assert valid == False

def test_authorizer():
    auth = build_api_gateway_authorizer('arn:aws:cognito-idp:us-east-1:123:userpool/us-east-1_abc')
    assert auth['Type'] == 'COGNITO_USER_POOLS'
