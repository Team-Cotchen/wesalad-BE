import requests

from django.conf import settings

def google_get_access_token(google_token_api, auth_code):
    client_id     = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    redirect_uri  = settings.GOOGLE_OAUTH2_REDIRECT_URI
    code          = auth_code
    grant_type    = 'authorization_code'
    state         = 'random_string'
    
    google_token_api += \
        f'?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirect_uri}&state={state}'
    
    token = requests.post(google_token_api, timeout=2)
    return token.json()['access_token']

def google_get_user_info(access_token):
    user_info_response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        params = {
            'access_token': access_token
        }
    )
    
    user_info = user_info_response.json()
    return user_info