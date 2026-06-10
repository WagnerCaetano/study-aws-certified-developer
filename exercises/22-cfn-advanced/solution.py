def build_sub_arn(service, resource, account='123456789012', region='us-east-1'):
    return f'arn:aws:{service}:{region}:{account}:{resource}'

def build_parameter(name, param_type, default=None, allowed_values=None):
    param = {'Type': param_type}
    if default:
        param['Default'] = default
    if allowed_values:
        param['AllowedValues'] = allowed_values
    return {name: param}

def build_output(name, value, export_name=None):
    output = {'Value': value}
    if export_name:
        output['Export'] = {'Name': export_name}
    return {name: output}

def get_intrinsic_function(fn_name, *args):
    functions = {
        'Ref': lambda x: {'Ref': x},
        'GetAtt': lambda x, y: {'Fn::GetAtt': [x, y]},
        'Sub': lambda x: {'Fn::Sub': x},
        'Join': lambda x, y: {'Fn::Join': [x, y]},
        'ImportValue': lambda x: {'Fn::ImportValue': x},
    }
    return functions[fn_name](*args)
