import json

def build_auth_flow(user_pool_id, client_id, callback_url):
    return {
        'auth_url': f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}/oauth2/authorize',
        'token_url': f'https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}/oauth2/token',
        'client_id': client_id,
        'callback_url': callback_url,
        'response_type': 'code',
        'scope': 'openid email profile'
    }

def validate_token_claims(claims, required_groups=None):
    if not claims.get('sub'):
        return False, 'Missing subject claim'
    if required_groups:
        user_groups = claims.get('cognito:groups', '').split(',') if claims.get('cognito:groups') else []
        if not any(g in user_groups for g in required_groups):
            return False, 'User not in required group'
    return True, 'Valid'

def build_api_gateway_authorizer(user_pool_arn):
    return {
        'Type': 'COGNITO_USER_POOLS',
        'ProviderARNs': [user_pool_arn]
    }
