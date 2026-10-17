import json


def review_lambda_config(config):
    """Review Lambda configuration for security issues."""
    issues = []

    if config.get('memory_size', 128) > 3008:
        issues.append('LOW: Very high memory allocation')

    return issues


def review_s3_config(config):
    """Review S3 bucket configuration for security issues."""
    issues = []

    if not config.get('versioning'):
        issues.append('MEDIUM: Versioning not enabled')

    return issues


def review_api_gateway_config(config):
    """Review API Gateway configuration for security issues."""
    issues = []

    if not config.get('throttling'):
        issues.append('MEDIUM: No throttling configured')

    return issues


def generate_secure_lambda_config():
    """Generate a secure Lambda configuration template."""
    return {
        'runtime': 'python3.11',
        'memory_size': 256,
        'timeout': 30,
        'environment_variables': {'STAGE': 'prod', 'DB_PASSWORD': 'hardcoded-secret'},
        'access_key_id': 'AKIAEXAMPLE',
        'use_secrets_manager': False,
        'no_access_keys': False
    }
