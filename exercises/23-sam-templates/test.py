from solution import build_sam_function, build_api_event, build_sam_template

def test_sam_function():
    func = build_sam_function('GetItems', 'python3.11', 'app.handler', 'src/')
    assert func['GetItems']['Type'] == 'AWS::Serverless::Function'
    assert func['GetItems']['Properties']['Runtime'] == 'python3.11'

def test_api_event():
    event = build_api_event('/items', 'get')
    assert event['ApiEvent']['Type'] == 'Api'
    assert event['ApiEvent']['Properties']['Method'] == 'get'

def test_full_sam_template():
    func = build_sam_function('GetItems', 'python3.11', 'app.handler', 'src/', 
        events={'GetApi': build_api_event('/items', 'get')})
    template = build_sam_template([func], {'Function': {'Timeout': 30}})
    assert template['Transform'] == 'AWS::Serverless-2016-10-31'
    assert 'Globals' in template
    assert 'GetItems' in template['Resources']
