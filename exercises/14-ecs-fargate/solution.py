import json

def build_task_definition(family, image, cpu, memory, container_port, role_arn, exec_role_arn):
    """Build an ECS Fargate task definition."""
    return {
        'family': family,
        'networkMode': 'awsvpc',
        'requiresCompatibilities': ['FARGATE'],
        'cpu': str(cpu),
        'memory': str(memory),
        'taskRoleArn': role_arn,
        'executionRoleArn': exec_role_arn,
        'containerDefinitions': [{
            'name': family,
            'image': image,
            'essential': True,
            'portMappings': [{'containerPort': container_port, 'protocol': 'tcp'}],
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': f'/ecs/{family}',
                    'awslogs-region': 'us-east-1',
                    'awslogs-stream-prefix': 'ecs'
                }
            }
        }]
    }

def build_service_config(cluster, service_name, task_def, desired_count, subnet_ids, sg_ids):
    """Build ECS service configuration."""
    return {
        'cluster': cluster,
        'serviceName': service_name,
        'taskDefinition': task_def,
        'desiredCount': desired_count,
        'launchType': 'FARGATE',
        'networkConfiguration': {
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': sg_ids,
                'assignPublicIp': 'ENABLED'
            }
        }
    }

def get_fargate_cpu_memory_options():
    """Return valid Fargate CPU/memory combinations."""
    return {
        '256': ['512', '1024', '2048'],
        '512': ['1024', '2048', '3072', '4096'],
        '1024': ['2048', '3072', '4096', '5120', '6144', '7168', '8192'],
        '2048': ['4096', '5120', '6144', '7168', '8192', '9216', '10240', '11264', '12288', '13312', '14336', '15360', '16384'],
    }
