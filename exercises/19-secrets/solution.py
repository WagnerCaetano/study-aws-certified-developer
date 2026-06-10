import json

def build_secret_value(username, password, host, port, database):
    """Build a secret value for database credentials."""
    return json.dumps({
        'username': username,
        'password': password,
        'host': host,
        'port': str(port),
        'database': database,
        'engine': 'postgres'
    })

def parse_secret(secret_string):
    """Parse a secret string into a dictionary."""
    return json.loads(secret_string)

def build_ssm_parameter(name, value, param_type='String', description='', kms_key_id=None):
    """Build SSM Parameter Store put_parameter parameters."""
    params = {
        'Name': name,
        'Value': value,
        'Type': param_type,
        'Description': description,
        'Overwrite': True
    }
    if kms_key_id and param_type == 'SecureString':
        params['KeyId'] = kms_key_id
    return params

def recommend_secrets_service(requirements):
    """Recommend Secrets Manager vs Parameter Store based on requirements."""
    if requirements.get('auto_rotation'):
        return 'secrets-manager'
    if requirements.get('is_database'):
        return 'secrets-manager'
    if requirements.get('cost_sensitive'):
        return 'parameter-store'
    if requirements.get('needs_encryption') and not requirements.get('auto_rotation'):
        return 'parameter-store'
    return 'secrets-manager'

def build_ecs_secret_reference(name, secret_arn):
    """Build ECS task definition secret reference."""
    return {'name': name, 'valueFrom': secret_arn}
