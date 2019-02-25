from app import app, google
from flask import render_template
from flask import session, redirect, url_for
from app.libs import utils
import os

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]

    headers = {'Authorization': 'OAuth '+access_token}
    try:
        req = utils.get_http('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    except Exception as e:
        return str(e)
    else:
        return str(req)


@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(os.getenv('REDIRECT_URI'))
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')