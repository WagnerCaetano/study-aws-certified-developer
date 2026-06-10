import json

def build_user_pool_config(pool_name, password_policy=None):
    """Build Cognito User Pool configuration."""
    config = {
        'PoolName': pool_name,
        'Policies': {
            'PasswordPolicy': password_policy or {
                'MinimumLength': 8,
                'RequireUppercase': True,
                'RequireLowercase': True,
                'RequireNumbers': True,
                'RequireSymbols': True
            }
        },
        'AutoVerifiedAttributes': ['email']
    }
    return config

def build_app_client_config(pool_id, client_name, callback_urls, logout_urls):
    """Build Cognito User Pool Client configuration."""
    return {
        'UserPoolId': pool_id,
        'ClientName': client_name,
        'CallbackURLs': callback_urls,
        'LogoutURLs': logout_urls,
        'AllowedOAuthFlows': ['code'],
        'AllowedOAuthScopes': ['openid', 'email', 'profile'],
        'SupportedIdentityProviders': ['COGNITO']
    }

def parse_cognito_event(event):
    """Parse Cognito authorizer event from API Gateway."""
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    return {
        'user_id': claims.get('sub'),
        'email': claims.get('email'),
        'groups': claims.get('cognito:groups', '').split(',') if claims.get('cognito:groups') else []
    }

def build_identity_pool_config(pool_name, user_pool_id, app_client_id):
    """Build Cognito Identity Pool configuration."""
    return {
        'IdentityPoolName': pool_name,
        'AllowUnauthenticatedIdentities': False,
        'CognitoIdentityProviders': [{
            'ProviderName': f'cognito-idp.us-east-1.amazonaws.com/{user_pool_id}',
            'ClientId': app_client_id
        }]
    }
