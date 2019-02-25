from . import configs
from flask import Flask
from flask_oauthlib.client import OAuth
import os, psycopg2


root_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object(configs.Config)
app.secret_key = os.getenv("SECRET_KEY")

oauth = OAuth(app)
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


conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    sslmode=os.getenv('DB_SSL'),
    port=os.getenv('DB_PORT'),
    host=os.getenv('DB_HOST')
)

conn.set_session(autocommit=True)
db = conn.cursor()

# registering controllers
from app.controllers import *


