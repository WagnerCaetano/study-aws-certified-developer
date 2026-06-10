import json
from solution import build_secret_value, parse_secret, build_ssm_parameter, recommend_secrets_service, build_ecs_secret_reference

def test_build_and_parse_secret():
    secret = build_secret_value('admin', 'password123', 'db.example.com', 5432, 'mydb')
    parsed = parse_secret(secret)
    assert parsed['username'] == 'admin'
    assert parsed['host'] == 'db.example.com'

def test_ssm_secure_string():
    params = build_ssm_parameter('/app/db-password', 'secret123', 'SecureString', 'DB Password', 'alias/my-key')
    assert params['Type'] == 'SecureString'
    assert params['KeyId'] == 'alias/my-key'

def test_ssm_plain_string():
    params = build_ssm_parameter('/app/config', 'value', 'String', 'Config')
    assert params['Type'] == 'String'
    assert 'KeyId' not in params

def test_recommend_secrets_manager():
    assert recommend_secrets_service({'auto_rotation': True}) == 'secrets-manager'
    assert recommend_secrets_service({'is_database': True}) == 'secrets-manager'

def test_recommend_parameter_store():
    assert recommend_secrets_service({'cost_sensitive': True}) == 'parameter-store'

def test_ecs_secret_ref():
    ref = build_ecs_secret_reference('DB_PASSWORD', 'arn:aws:secretsmanager:us-east-1:123:secret:my-secret')
    assert ref['name'] == 'DB_PASSWORD'
    assert ref['valueFrom'] == 'arn:aws:secretsmanager:us-east-1:123:secret:my-secret'
