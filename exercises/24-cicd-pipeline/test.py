from solution import build_buildspec, build_pipeline_stage, build_source_action, determine_deployment_strategy

def test_buildspec():
    bs = build_buildspec(['pip install -r requirements.txt'], ['pytest'], ['sam build'], ['echo done'], ['packaged.yaml'])
    assert bs['version'] == 0.2
    assert len(bs['phases']['build']['commands']) == 1

def test_source_action():
    action = build_source_action('Source', 'CodeCommit', 'my-repo', 'main', 'SourceCode')
    assert action['ActionTypeId']['Category'] == 'Source'
    assert action['ActionTypeId']['Provider'] == 'CodeCommit'

def test_deployment_strategy():
    assert determine_deployment_strategy('lambda', True) == 'Canary10Percent5Minutes'
    assert determine_deployment_strategy('ecs', True) == 'BLUE_GREEN'
    assert determine_deployment_strategy('lambda', False) == 'ALL_AT_ONCE'
