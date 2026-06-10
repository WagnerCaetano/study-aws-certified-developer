from solution import build_alarm_config, recommend_alarm_action, build_dashboard_metrics

def test_alarm_config():
    alarm = build_alarm_config('HighErrors', 'Errors', 'AWS/Lambda', 5, sns_topic_arn='arn:sns:topic')
    assert alarm['Threshold'] == 5
    assert alarm['AlarmActions'] == ['arn:sns:topic']

def test_alarm_no_notification():
    alarm = build_alarm_config('HighCPU', 'CPUUtilization', 'AWS/EC2', 80)
    assert 'AlarmActions' not in alarm

def test_recommend_critical():
    assert recommend_alarm_action('lambda', 'Errors', True) == 'Page on-call immediately'

def test_recommend_no_action():
    assert recommend_alarm_action('lambda', 'Errors', False) == 'No action needed'

def test_dashboard():
    dashboard = build_dashboard_metrics(['Lambda', 'DynamoDB'])
    assert len(dashboard['widgets']) == 2
