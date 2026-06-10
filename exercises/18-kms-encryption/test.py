import json
from solution import build_kms_key_policy, determine_encryption_method, build_s3_kms_config

def test_key_policy_has_root():
    policy = build_kms_key_policy('123456789012')
    assert len(policy['Statement']) >= 1
    assert '123456789012' in policy['Statement'][0]['Principal']['AWS']

def test_key_policy_with_roles():
    policy = build_kms_key_policy('123', ['arn:aws:iam::123:role/LambdaRole'])
    assert len(policy['Statement']) == 2
    role_stmt = policy['Statement'][1]
    assert 'kms:Encrypt' in role_stmt['Action']

def test_direct_encryption_for_small_data():
    result = determine_encryption_method(2)
    assert result['method'] == 'direct'

def test_envelope_for_large_data():
    result = determine_encryption_method(100)
    assert result['method'] == 'envelope'

def test_s3_kms_config():
    config = build_s3_kms_config('alias/my-key')
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms'
    assert rule['BucketKeyEnabled'] == True
