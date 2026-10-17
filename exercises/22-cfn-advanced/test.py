import os
import importlib

_mod = importlib.import_module(os.environ.get('EXERCISE_MODULE', 'starter'))
build_sub_arn = _mod.build_sub_arn
build_parameter = _mod.build_parameter
build_output = _mod.build_output
get_intrinsic_function = _mod.get_intrinsic_function

def test_arn_builder():
    arn = build_sub_arn('s3', 'my-bucket')
    assert 's3' in arn
    assert 'my-bucket' in arn

def test_parameter_with_default():
    param = build_parameter('Stage', 'String', default='dev', allowed_values=['dev', 'prod'])
    assert param['Stage']['Default'] == 'dev'
    assert 'prod' in param['Stage']['AllowedValues']

def test_output_with_export():
    output = build_output('BucketName', {'Ref': 'MyBucket'}, export_name='MyApp-Bucket')
    assert 'Export' in output['BucketName']

def test_intrinsic_ref():
    result = get_intrinsic_function('Ref', 'MyBucket')
    assert result == {'Ref': 'MyBucket'}

def test_intrinsic_getatt():
    result = get_intrinsic_function('GetAtt', 'MyFunction', 'Arn')
    assert result == {'Fn::GetAtt': ['MyFunction', 'Arn']}
