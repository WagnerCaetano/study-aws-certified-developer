import json

def build_kms_key_policy(account_id, allowed_roles=None):
    """Build a KMS key policy."""
    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'EnableRootAccountAccess',
                'Effect': 'Allow',
                'Principal': {'AWS': f'arn:aws:iam::{account_id}:root'},
                'Action': 'kms:*',
                'Resource': '*'
            }
        ]
    }
    if allowed_roles:
        policy['Statement'].append({
            'Sid': 'AllowRoleAccess',
            'Effect': 'Allow',
            'Principal': {'AWS': allowed_roles},
            'Action': ['kms:Encrypt', 'kms:Decrypt', 'kms:GenerateDataKey'],
            'Resource': '*'
        })
    return policy

def determine_encryption_method(data_size_kb):
    """Determine encryption method based on data size."""
    # KMS direct encryption limit is 4KB
    if data_size_kb <= 4:
        return {
            'method': 'direct',
            'description': 'Use KMS Encrypt/Decrypt directly',
            'api': 'kms.encrypt()'
        }
    else:
        return {
            'method': 'envelope',
            'description': 'Use envelope encryption with GenerateDataKey',
            'api': 'kms.generate_data_key()'
        }

def build_s3_kms_config(kms_key_id):
    """Build S3 encryption configuration with KMS."""
    return {
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'aws:kms',
                'KMSMasterKeyID': kms_key_id
            },
            'BucketKeyEnabled': True
        }]
    }
