from solution import build_log_insights_query, build_metric_filter, build_log_group_name

def test_error_query():
    query = build_log_insights_query('@message like /ERROR/', 'count(*) as errorCount', '@timestamp desc')
    assert 'ERROR' in query
    assert 'count' in query

def test_metric_filter():
    mf = build_metric_filter('ERROR', 'ErrorCount', 'MyApp')
    assert mf['filterPattern'] == 'ERROR'
    assert mf['metricTransformations'][0]['metricName'] == 'ErrorCount'

def test_log_group_name():
    assert build_log_group_name('lambda', 'my-function') == '/aws/lambda/my-function'
