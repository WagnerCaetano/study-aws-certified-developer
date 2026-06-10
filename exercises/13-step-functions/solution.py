import json

def build_order_workflow(order_function_arn, inventory_function_arn, ship_function_arn):
    """Build an order processing state machine."""
    return {
        'Comment': 'Order processing workflow',
        'StartAt': 'ValidateOrder',
        'States': {
            'ValidateOrder': {
                'Type': 'Task',
                'Resource': order_function_arn,
                'Next': 'CheckInventory'
            },
            'CheckInventory': {
                'Type': 'Task',
                'Resource': inventory_function_arn,
                'Retry': [{
                    'ErrorEquals': ['States.TaskFailed'],
                    'IntervalSeconds': 2,
                    'MaxAttempts': 3,
                    'BackoffRate': 2.0
                }],
                'Catch': [{
                    'ErrorEquals': ['States.ALL'],
                    'Next': 'OrderFailed'
                }],
                'Next': 'InStock?'
            },
            'InStock?': {
                'Type': 'Choice',
                'Choices': [{
                    'Variable': '$.inStock',
                    'BooleanEquals': True,
                    'Next': 'ShipOrder'
                }],
                'Default': 'Backorder'
            },
            'ShipOrder': {
                'Type': 'Task',
                'Resource': ship_function_arn,
                'End': True
            },
            'Backorder': {
                'Type': 'Fail',
                'Error': 'OutOfStock',
                'Cause': 'Item not in stock'
            },
            'OrderFailed': {
                'Type': 'Fail',
                'Error': 'OrderFailed',
                'Cause': 'Could not check inventory'
            }
        }
    }

def validate_state_machine(definition):
    """Validate a state machine definition."""
    errors = []
    
    if 'StartAt' not in definition:
        errors.append('Missing StartAt')
    
    if 'States' not in definition:
        errors.append('Missing States')
        return errors
    
    states = definition['States']
    start = definition.get('StartAt')
    
    if start not in states:
        errors.append(f'StartAt state "{start}" not found in States')
    
    for name, state in states.items():
        if 'Type' not in state:
            errors.append(f'State "{name}" missing Type')
        elif state['Type'] == 'Task' and 'Resource' not in state:
            errors.append(f'Task state "{name}" missing Resource')
        elif state['Type'] == 'Choice' and 'Choices' not in state:
            errors.append(f'Choice state "{name}" missing Choices')
    
    return errors
