import json
from solution import build_bucket_policy_read_only, build_encryption_config, build_cors_config

def test_bucket_policy_allows_public_read():
    policy = build_bucket_policy_read_only('my-bucket', '123')
    stmt = policy['Statement'][0]
    assert stmt['Effect'] == 'Allow'
    assert stmt['Principal'] == '*'
    assert stmt['Action'] == 's3:GetObject'
    assert 'my-bucket/*' in stmt['Resource']

def test_sse_kms_encryption():
    config = build_encryption_config('arn:aws:kms:us-east-1:123:key/abc')
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms'
    assert 'KMSMasterKeyID' in rule['ApplyServerSideEncryptionByDefault']

def test_sse_s3_encryption():
    config = build_encryption_config()
    rule = config['Rules'][0]
    assert rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'AES256'

def test_cors_config():
    config = build_cors_config(['https://example.com'])
    rule = config['CORSRules'][0]
    assert 'GET' in rule['AllowedMethods']
    assert rule['AllowedOrigins'] == ['https://example.com']
