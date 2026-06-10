from solution import build_task_definition, build_service_config, get_fargate_cpu_memory_options

def test_task_definition():
    td = build_task_definition('my-app', '123456.dkr.ecr.us-east-1.amazonaws.com/my-app:latest', 256, 512, 8080, 'role-arn', 'exec-role-arn')
    assert td['family'] == 'my-app'
    assert td['networkMode'] == 'awsvpc'
    assert 'FARGATE' in td['requiresCompatibilities']
    assert td['cpu'] == '256'
    assert td['memory'] == '512'
    assert len(td['containerDefinitions']) == 1

def test_container_definition():
    td = build_task_definition('my-app', 'image', 256, 512, 8080, 'role', 'exec-role')
    container = td['containerDefinitions'][0]
    assert container['essential'] == True
    assert container['portMappings'][0]['containerPort'] == 8080
    assert container['logConfiguration']['logDriver'] == 'awslogs'

def test_service_config():
    svc = build_service_config('my-cluster', 'my-service', 'my-app:1', 2, ['subnet-1'], ['sg-1'])
    assert svc['launchType'] == 'FARGATE'
    assert svc['desiredCount'] == 2
    assert svc['networkConfiguration']['awsvpcConfiguration']['subnets'] == ['subnet-1']

def test_fargate_options():
    opts = get_fargate_cpu_memory_options()
    assert '256' in opts
    assert '512' in opts['256']
