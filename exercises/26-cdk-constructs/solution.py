def classify_construct_level(construct_name, properties):
    if 'Cfn' in construct_name:
        return 'L1'
    elif 'grant' in str(properties.get('methods', [])) or 'from_lookup' in str(properties.get('methods', [])):
        return 'L2'
    elif 'pattern' in construct_name.lower() or 'RestApi' in construct_name:
        return 'L3'
    return 'L2'

def identify_cdk_command(description):
    commands = {
        'Initialize a new CDK project': 'cdk init',
        'Generate CloudFormation template': 'cdk synth',
        'Deploy the stack': 'cdk deploy',
        'Compare with deployed stack': 'cdk diff',
        'Destroy the stack': 'cdk destroy',
        'List all stacks': 'cdk list',
    }
    return commands.get(description, 'Unknown')

def build_construct_props(construct_type, props):
    return {'type': construct_type, 'properties': props, 'level': classify_construct_level(construct_type, props)}
