import json

def build_lambda_trust_policy():
    """Build trust policy for Lambda service."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'lambda.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    }

def build_ecs_trust_policy():
    """Build trust policy for ECS tasks."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'ecs-tasks.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    }

def build_assume_role_policy(source_account, role_arn):
    """Build IAM policy allowing a user to assume a role."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': 'sts:AssumeRole',
            'Resource': role_arn
        }]
    }

def extract_temp_credentials(sts_response):
    """Extract credentials from STS assume_role response."""
    creds = sts_response['Credentials']
    return {
        'access_key_id': creds['AccessKeyId'],
        'secret_access_key': creds['SecretAccessKey'],
        'session_token': creds['SessionToken'],
        'expiration': creds['Expiration']
    }
