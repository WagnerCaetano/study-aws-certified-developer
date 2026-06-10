def build_buildspec(install_cmds, pre_build_cmds, build_cmds, post_build_cmds, artifacts):
    return {
        'version': 0.2,
        'phases': {
            'install': {'commands': install_cmds},
            'pre_build': {'commands': pre_build_cmds},
            'build': {'commands': build_cmds},
            'post_build': {'commands': post_build_cmds}
        },
        'artifacts': {'files': artifacts}
    }

def build_pipeline_stage(name, actions):
    return {'Name': name, 'Actions': actions}

def build_source_action(name, provider, repo, branch, output_artifact):
    return {
        'Name': name,
        'ActionTypeId': {'Category': 'Source', 'Owner': 'AWS', 'Provider': provider, 'Version': '1'},
        'Configuration': {'RepositoryName': repo, 'BranchName': branch},
        'OutputArtifacts': [{'Name': output_artifact}]
    }

def determine_deployment_strategy(app_type, zero_downtime_required):
    if zero_downtime_required:
        if app_type == 'lambda':
            return 'Canary10Percent5Minutes'
        elif app_type == 'ecs':
            return 'BLUE_GREEN'
        else:
            return 'IMMUTABLE'
    return 'ALL_AT_ONCE'
