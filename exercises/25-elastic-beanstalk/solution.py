def recommend_deployment_policy(zero_downtime, capacity_constraint):
    if not zero_downtime:
        return 'AllAtOnce'
    elif capacity_constraint:
        return 'RollingWithAdditionalBatch'
    elif zero_downtime and not capacity_constraint:
        return 'Immutable'
    return 'Rolling'

def build_ebextensions(filename, option_settings=None, resources=None):
    config = {}
    if option_settings:
        config['option_settings'] = option_settings
    if resources:
        config['Resources'] = resources
    return config

def build_health_check_config(path='/health', interval=30):
    return [
        {'namespace': 'aws:elasticbeanstalk:environment:process:default', 'option_name': 'HealthCheckPath', 'value': path},
        {'namespace': 'aws:elasticbeanstalk:environment:process:default', 'option_name': 'HealthCheckInterval', 'value': str(interval)}
    ]
