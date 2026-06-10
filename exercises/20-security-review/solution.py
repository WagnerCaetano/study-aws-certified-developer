import json

def review_lambda_config(config):
    """Review Lambda configuration for security issues."""
    issues = []
    
    # Check: Should not use access keys
    if config.get('access_key_id'):
        issues.append('CRITICAL: Access key found in config - use IAM roles instead')
    
    # Check: Should not log secrets
    if 'password' in str(config.get('environment_variables', {})).lower():
        issues.append('HIGH: Potential secret in environment variables - use Secrets Manager')
    
    # Check: Memory should be appropriate
    if config.get('memory_size', 128) > 3008:
        issues.append('LOW: Very high memory allocation')
    
    return issues

def review_s3_config(config):
    """Review S3 bucket configuration for security issues."""
    issues = []
    
    # Check: Encryption should be enabled
    if not config.get('encryption'):
        issues.append('HIGH: Encryption not enabled')
    
    # Check: Versioning should be enabled
    if not config.get('versioning'):
        issues.append('MEDIUM: Versioning not enabled')
    
    # Check: Public access should be blocked
    if config.get('public_access'):
        issues.append('HIGH: Public access enabled')
    
    return issues

def review_api_gateway_config(config):
    """Review API Gateway configuration for security issues."""
    issues = []
    
    if not config.get('authorization'):
        issues.append('HIGH: No authorization configured')
    
    if not config.get('throttling'):
        issues.append('MEDIUM: No throttling configured')
    
    if not config.get('waf'):
        issues.append('LOW: WAF not configured')
    
    return issues

def generate_secure_lambda_config():
    """Generate a secure Lambda configuration template."""
    return {
        'runtime': 'python3.11',
        'memory_size': 256,
        'timeout': 30,
        'environment_variables': {'STAGE': 'prod', 'TABLE_NAME': 'my-table'},
        'vpc_config': {'subnetIds': [], 'securityGroupIds': []},
        'tracing_config': {'mode': 'Active'},
        'use_secrets_manager': True,
        'no_access_keys': True
    }
