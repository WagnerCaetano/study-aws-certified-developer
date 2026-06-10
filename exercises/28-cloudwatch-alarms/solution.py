def build_alarm_config(name, metric_name, namespace, threshold, comparison='GreaterThanThreshold',
                         period=300, evaluation_periods=1, statistic='Sum', sns_topic_arn=None):
    config = {
        'AlarmName': name,
        'MetricName': metric_name,
        'Namespace': namespace,
        'Threshold': threshold,
        'ComparisonOperator': comparison,
        'Period': period,
        'EvaluationPeriods': evaluation_periods,
        'Statistic': statistic
    }
    if sns_topic_arn:
        config['AlarmActions'] = [sns_topic_arn]
        config['OKActions'] = [sns_topic_arn]
    return config

def recommend_alarm_action(service, metric, threshold_exceeded):
    if not threshold_exceeded:
        return 'No action needed'
    if metric in ['Errors', '5XXError', 'Throttles']:
        return 'Page on-call immediately'
    elif metric in ['CPUUtilization', 'MemoryUtilization']:
        return 'Auto-scale the service'
    return 'Send notification'

def build_dashboard_metrics(services):
    widgets = []
    for service in services:
        widgets.append({'type': 'metric', 'title': f'{service} Metrics'})
    return {'widgets': widgets}
