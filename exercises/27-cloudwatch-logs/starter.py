def build_log_insights_query(filter_pattern=None, stats=None, sort_by=None, limit=20):
    parts = []
    if filter_pattern:
        parts.append(f'filter {filter_pattern}')
    if stats:
        parts.append(f'stats {stats}')
    if sort_by:
        parts.append(f'sort {sort_by}')
    parts.append(f'limit {limit}')
    return ' | '.join(parts)


def build_metric_filter(filter_pattern, metric_name, namespace, value='1'):
    return {
        'pattern': filter_pattern,
        'metricTransformations': [{
            'name': metric_name,
            'namespace': namespace,
            'value': value
        }]
    }


def build_log_group_name(service, resource_name):
    return f'/aws/logs/{service}/{resource_name}'
