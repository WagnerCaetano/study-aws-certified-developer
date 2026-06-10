from solution import build_sampling_rule, identify_trace_component, build_annotation_search, recommend_tracing_config

def test_sampling_rule():
    rule = build_sampling_rule('HighPriority', 1, 1.0, 'payment-service', 'POST', '/api/payments/*', 10)
    assert rule['Priority'] == 1
    assert rule['FixedRate'] == 1.0

def test_identify_trace():
    assert identify_trace_component('x', {'trace_id': 'abc'}) == 'trace'
    assert identify_trace_component('x', {'subsegments': []}) == 'segment'

def test_annotation_search():
    search = build_annotation_search('UserId', 'user-123')
    assert 'UserId' in search['FilterExpression']
    assert 'user-123' in search['FilterExpression']

def test_lambda_tracing():
    config = recommend_tracing_config('lambda')
    assert config['ActiveTracing'] == True
