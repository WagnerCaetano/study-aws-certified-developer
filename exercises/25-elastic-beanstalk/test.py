from solution import recommend_deployment_policy, build_ebextensions, build_health_check_config

def test_deployment_policy():
    assert recommend_deployment_policy(False, False) == 'AllAtOnce'
    assert recommend_deployment_policy(True, True) == 'RollingWithAdditionalBatch'
    assert recommend_deployment_policy(True, False) == 'Immutable'

def test_ebextensions():
    config = build_ebextensions('01-loadbalancer', option_settings=[{'key': 'value'}])
    assert 'option_settings' in config

def test_health_check():
    hc = build_health_check_config('/api/health', 15)
    assert any('/api/health' in str(s) for s in hc)
