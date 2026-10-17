import json


def build_codepipeline_config(name, source_repo, source_branch, build_project, deploy_stack):
    return {
        'name': name,
        'stages': [
            {'name': 'Source', 'provider': 'CodeCommit', 'config': {'repo': source_repo, 'branch': source_branch}},
            {'name': 'Build', 'provider': 'CodeBuild', 'config': {'project': build_project}},
        ],
    }


def build_buildspec_advanced(test_cmds, build_cmds, package_cmds):
    return {
        'version': 0.1,
        'phases': {
            'install': {'runtime-versions': {'python': '3.11'}},
            'pre_build': {'commands': build_cmds},
            'build': {'commands': test_cmds},
            'post_build': {'commands': package_cmds},
        },
        'artifacts': {'files': ['packaged.yaml']},
    }


def determine_pipeline_stage(failed_stage, error_message):
    if failed_stage == 'Source':
        return 'Check pipeline logs'
    elif failed_stage == 'Build':
        return 'Check CloudFormation template for errors'
    elif failed_stage == 'Deploy':
        return 'Fix build errors'
    return 'Check pipeline logs'
