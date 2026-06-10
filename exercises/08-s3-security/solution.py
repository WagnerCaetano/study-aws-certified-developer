import json

def build_bucket_policy_read_only(bucket_name, account_id):
    """Build a bucket policy that allows public read access."""
    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'PublicReadGetObject',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': 's3:GetObject',
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }]
    }

def build_encryption_config(kms_key_arn=None):
    """Build S3 encryption configuration."""
    if kms_key_arn:
        return {
            'Rules': [{
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'aws:kms',
                    'KMSMasterKeyID': kms_key_arn
                }
            }]
        }
    return {
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
        }]
    }

def build_cors_config(allowed_origins=['*']):
    """Build S3 CORS configuration."""
    return {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST'],
            'AllowedOrigins': allowed_origins,
            'ExposeHeaders': ['ETag'],
            'MaxAgeSeconds': 3600
        }]
    }
