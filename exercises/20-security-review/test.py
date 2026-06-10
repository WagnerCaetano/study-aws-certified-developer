from solution import review_lambda_config, review_s3_config, review_api_gateway_config, generate_secure_lambda_config

def test_detect_access_keys():
    issues = review_lambda_config({'access_key_id': 'AKIA...'})
    assert any('Access key' in i for i in issues)

def test_detect_secrets_in_env():
    issues = review_lambda_config({'environment_variables': {'password': 'secret'}})
    assert any('secret' in i.lower() for i in issues)

def test_detect_no_encryption():
    issues = review_s3_config({})
    assert any('Encryption' in i for i in issues)

def test_detect_public_access():
    issues = review_s3_config({'public_access': True})
    assert any('Public' in i for i in issues)

def test_detect_no_auth():
    issues = review_api_gateway_config({})
    assert any('authorization' in i.lower() for i in issues)

def test_secure_config_template():
    config = generate_secure_lambda_config()
    assert config['use_secrets_manager'] == True
    assert config['no_access_keys'] == True
    assert 'password' not in str(config['environment_variables']).lower()
