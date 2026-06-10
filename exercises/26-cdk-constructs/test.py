from solution import classify_construct_level, identify_cdk_command, build_construct_props

def test_l1_construct():
    assert classify_construct_level('CfnBucket', {}) == 'L1'

def test_l2_construct():
    assert classify_construct_level('Bucket', {'methods': ['grantRead']}) == 'L2'

def test_cdk_commands():
    assert identify_cdk_command('Generate CloudFormation template') == 'cdk synth'
    assert identify_cdk_command('Deploy the stack') == 'cdk deploy'

def test_construct_props():
    props = build_construct_props('Function', {'runtime': 'python3.11'})
    assert props['level'] in ['L1', 'L2', 'L3']
