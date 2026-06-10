def build_sam_function(function_name, runtime, handler, code_uri, events=None, policies=None):
    func = {
        function_name: {
            'Type': 'AWS::Serverless::Function',
            'Properties': {
                'Runtime': runtime,
                'Handler': handler,
                'CodeUri': code_uri
            }
        }
    }
    if events:
        func[function_name]['Properties']['Events'] = events
    if policies:
        func[function_name]['Properties']['Policies'] = policies
    return func

def build_api_event(path, method):
    return {'ApiEvent': {'Type': 'Api', 'Properties': {'Path': path, 'Method': method}}}

def build_sam_template(functions, globals_config=None):
    template = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Transform': 'AWS::Serverless-2016-10-31',
        'Resources': {}
    }
    if globals_config:
        template['Globals'] = globals_config
    for func in functions:
        template['Resources'].update(func)
    return template
