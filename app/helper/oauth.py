from app import oauth
import os


google = oauth.remote_app(
    'google',
    consumer_key=str(os.getenv('GOOGLE_CLIENT_ID')),
    consumer_secret=str(os.getenv('GOOGLE_CLIENT_ID_SECRET')),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=str(os.getenv('FACEBOOK_APP_ID')),
    consumer_secret=str(os.getenv('FACEBOOK_APP_SECRET')),
    request_token_params={'scope': 'email'}
)


github = oauth.remote_app(
    'github',
    consumer_key= str(os.getenv('GITHUB_APP_ID')),
    consumer_secret=str(os.getenv('GITHUB_APP_SECRET')),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url= None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)