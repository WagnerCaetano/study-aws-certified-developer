import json
import os
import importlib

_mod = importlib.import_module(os.environ.get('EXERCISE_MODULE', 'starter'))
build_codepipeline_config = _mod.build_codepipeline_config
build_buildspec_advanced = _mod.build_buildspec_advanced
determine_pipeline_stage = _mod.determine_pipeline_stage


def test_pipeline_config():
    config = build_codepipeline_config('my-pipeline', 'my-repo', 'main', 'build-proj', 'my-stack')
    assert config['name'] == 'my-pipeline'
    assert len(config['stages']) == 3


def test_buildspec():
    bs = build_buildspec_advanced(['pytest'], ['sam build'], ['sam package'])
    assert bs['version'] == 0.2
    assert 'pytest' in bs['phases']['pre_build']['commands']


def test_diagnose_build_failure():
    result = determine_pipeline_stage('Build', 'test failed: expected 200 got 400')
    assert 'test' in result.lower()


def test_diagnose_deploy_failure():
    result = determine_pipeline_stage('Deploy', 'permission denied')
    assert 'permission' in result.lower() or 'IAM' in result
