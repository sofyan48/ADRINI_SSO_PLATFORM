from . import configs
from flask import Flask
from flask_oauthlib.client import OAuth, OAuthException
from flask_redis import FlaskRedis
import os, psycopg2


root_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config.from_object(configs.Config)
app.secret_key = os.getenv("SECRET_KEY")

redis_store = FlaskRedis(app)
oauth = OAuth(app)

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


