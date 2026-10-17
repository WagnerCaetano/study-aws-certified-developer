def build_alarm_config(name, metric_name, namespace, threshold, comparison='GreaterThanThreshold',
                         period=300, evaluation_periods=1, statistic='Average', sns_topic_arn=None):
    config = {
        'AlarmName': name,
        'MetricName': metric_name,
        'Namespace': namespace,
        'Threshold': threshold,
        'ComparisonOperator': comparison,
        'Period': 60,
        'EvaluationPeriods': evaluation_periods,
        'Statistic': statistic,
    }
    if sns_topic_arn:
        config['OKActions'] = [sns_topic_arn]
    return config


def recommend_alarm_action(service, metric, threshold_exceeded):
    if not threshold_exceeded:
        return 'No action needed'
    if metric in ['Errors', '5XXError', 'Throttles']:
        return 'Send notification'
    elif metric in ['CPUUtilization', 'MemoryUtilization']:
        return 'Auto-scale the service'
    return 'Send notification'


def build_dashboard_metrics(services):
    return {'widgets': [{'type': 'metric', 'title': 'All Services'}]}
