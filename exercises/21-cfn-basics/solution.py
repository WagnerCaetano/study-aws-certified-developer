import json

def build_lambda_cfn_template(function_name, runtime, handler, code_uri, role_arn):
    """Build a CloudFormation template with a Lambda function."""
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': f'Lambda function: {function_name}',
        'Resources': {
            function_name: {
                'Type': 'AWS::Lambda::Function',
                'Properties': {
                    'FunctionName': function_name,
                    'Runtime': runtime,
                    'Handler': handler,
                    'Code': {'S3Bucket': code_uri.split('/')[0], 'S3Key': '/'.join(code_uri.split('/')[1:])},
                    'Role': role_arn,
                    'Timeout': 30,
                    'MemorySize': 256
                }
            }
        },
        'Outputs': {
            'FunctionArn': {
                'Description': 'Lambda Function ARN',
                'Value': {'Fn::GetAtt': [function_name, 'Arn']}
            }
        }
    }

def build_s3_cfn_template(bucket_name):
    """Build a CloudFormation template with an S3 bucket."""
    return {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Resources': {
            'MyBucket': {
                'Type': 'AWS::S3::Bucket',
                'Properties': {
                    'BucketName': bucket_name,
                    'VersioningConfiguration': {'Status': 'Enabled'}
                }
            }
        },
        'Outputs': {
            'BucketName': {'Value': {'Ref': 'MyBucket'}}
        }
    }
