def build_sampling_rule(name, priority, fixed_rate, service_name='*', method='*', path='*', reservoir_size=1):
    return {
        'RuleName': name,
        'Priority': priority,
        'FixedRate': fixed_rate,
        'ReservoirSize': reservoir_size,
        'ServiceName': service_name,
        'HTTPMethod': method,
        'URLPath': path
    }

def identify_trace_component(name, data):
    if 'trace_id' in data or 'TraceId' in data:
        return 'trace'
    elif 'subsegments' in data or 'Subsegments' in data:
        return 'segment'
    elif 'parent_id' in data:
        return 'subsegment'
    return 'unknown'

def build_annotation_search(key, value):
    return {'FilterExpression': f'annotation.{key} = "{value}"'}

def recommend_tracing_config(service_type):
    if service_type == 'lambda':
        return {'ActiveTracing': True, 'SamplingRule': 'default'}
    elif service_type == 'api-gateway':
        return {'TracingEnabled': True}
    elif service_type == 'ecs':
        return {'XRayDaemon': True, 'SamplingRule': 'default'}
    return {'TracingEnabled': True}
