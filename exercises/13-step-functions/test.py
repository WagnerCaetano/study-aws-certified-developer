import json
from solution import build_order_workflow, validate_state_machine

def test_workflow_structure():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    assert wf['StartAt'] == 'ValidateOrder'
    assert 'States' in wf
    assert len(wf['States']) == 6

def test_choice_state():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    choice = wf['States']['InStock?']
    assert choice['Type'] == 'Choice'
    assert len(choice['Choices']) == 1

def test_retry_config():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    check = wf['States']['CheckInventory']
    assert 'Retry' in check
    assert check['Retry'][0]['MaxAttempts'] == 3

def test_catch_block():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    check = wf['States']['CheckInventory']
    assert 'Catch' in check

def test_validate_good_definition():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    errors = validate_state_machine(wf)
    assert len(errors) == 0

def test_validate_bad_definition():
    errors = validate_state_machine({})
    assert len(errors) > 0

def test_fail_states():
    wf = build_order_workflow('arn:validate', 'arn:inventory', 'arn:ship')
    assert wf['States']['Backorder']['Type'] == 'Fail'
    assert wf['States']['OrderFailed']['Type'] == 'Fail'
