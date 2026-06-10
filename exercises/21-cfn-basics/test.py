from solution import build_lambda_cfn_template, build_s3_cfn_template

def test_lambda_template():
    template = build_lambda_cfn_template('MyFunction', 'python3.11', 'index.handler', 'my-bucket/code.zip', 'role-arn')
    assert template['AWSTemplateFormatVersion'] == '2010-09-09'
    assert 'MyFunction' in template['Resources']
    assert template['Resources']['MyFunction']['Type'] == 'AWS::Lambda::Function'

def test_lambda_outputs():
    template = build_lambda_cfn_template('MyFunction', 'python3.11', 'index.handler', 'my-bucket/code.zip', 'role-arn')
    assert 'FunctionArn' in template['Outputs']

def test_s3_template():
    template = build_s3_cfn_template('my-unique-bucket')
    assert template['Resources']['MyBucket']['Type'] == 'AWS::S3::Bucket'
    assert template['Resources']['MyBucket']['Properties']['VersioningConfiguration']['Status'] == 'Enabled'

def test_s3_outputs():
    template = build_s3_cfn_template('my-bucket')
    assert 'BucketName' in template['Outputs']
