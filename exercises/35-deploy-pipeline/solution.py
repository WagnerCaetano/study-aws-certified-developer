import json

def build_codepipeline_config(name, source_repo, source_branch, build_project, deploy_stack):
    return {
        'name': name,
        'stages': [
            {'name': 'Source', 'provider': 'CodeCommit', 'config': {'repo': source_repo, 'branch': source_branch}},
            {'name': 'Build', 'provider': 'CodeBuild', 'config': {'project': build_project}},
            {'name': 'Deploy', 'provider': 'CloudFormation', 'config': {'stack': deploy_stack}}
        ]
    }

def build_buildspec_advanced(test_cmds, build_cmds, package_cmds):
    return {
        'version': 0.2,
        'phases': {
            'install': {'runtime-versions': {'python': '3.11'}},
            'pre_build': {'commands': test_cmds},
            'build': {'commands': build_cmds},
            'post_build': {'commands': package_cmds}
        },
        'artifacts': {'files': ['packaged.yaml']}
    }

def determine_pipeline_stage(failed_stage, error_message):
    if failed_stage == 'Source':
        return 'Check repository and branch configuration'
    elif failed_stage == 'Build':
        if 'test' in error_message.lower():
            return 'Fix failing unit tests'
        return 'Fix build errors'
    elif failed_stage == 'Deploy':
        if 'permission' in error_message.lower():
            return 'Check IAM capabilities and role permissions'
        return 'Check CloudFormation template for errors'
    return 'Check pipeline logs'
