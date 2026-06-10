import json

def build_lambda_s3_policy(bucket_name):
    """Build least-privilege policy for Lambda to read S3 bucket."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': [
                's3:GetObject',
                's3:ListBucket'
            ],
            'Resource': [
                f'arn:aws:s3:::{bucket_name}',
                f'arn:aws:s3:::{bucket_name}/*'
            ]
        }]
    }

def build_lambda_dynamodb_policy(table_arn):
    """Build least-privilege policy for Lambda to access DynamoDB."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Action': [
                'dynamodb:GetItem',
                'dynamodb:PutItem',
                'dynamodb:UpdateItem',
                'dynamodb:Query',
                'dynamodb:Scan'
            ],
            'Resource': table_arn
        }]
    }

def check_least_privilege(policy):
    """Check if a policy follows least privilege (no wildcards in actions)."""
    issues = []
    for stmt in policy.get('Statement', []):
        actions = stmt.get('Action', [])
        if isinstance(actions, str):
            actions = [actions]
        resources = stmt.get('Resource', [])
        if isinstance(resources, str):
            resources = [resources]
        
        for action in actions:
            if action == '*' or action.endswith(':*'):
                issues.append(f'Overly permissive action: {action}')
        for resource in resources:
            if resource == '*':
                issues.append(f'Overly permissive resource: {resource}')
    return issues

def build_cross_account_role_trust(trusted_account_id):
    """Build a trust policy for cross-account access."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'AWS': f'arn:aws:iam::{trusted_account_id}:root'},
            'Action': 'sts:AssumeRole'
        }]
    }
