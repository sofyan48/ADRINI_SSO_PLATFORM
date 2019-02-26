from app import app, google, redis_store
from flask import render_template
from flask import session, redirect, url_for, request, jsonify
from app.libs import utils
from app.models import model
import os, dill


@app.route('/google')
def google_login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route(os.getenv('REDIRECT_URI'))
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    headers = {
        'Authorization': 'OAuth '+access_token
    }
    try:
        req = utils.get_http('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    except Exception:
        return redirect(url_for('google'))

    try:
        dt_db = model.get_by_id("tb_userdata","email",req['email'])
    except Exception as e:
        dt_db = None
    if not dt_db:
        data_save = {
            "sso_id": req['id'],
            "first_name": req['given_name'],
            "last_name": req['family_name'],
            "email": req['email'],
            "location": "",
            "picture": req['picture']
        }
        try:
            model.insert("tb_userdata", data_save)
        except Exception as e:
            print(e)
        expires_in = resp['expires_in']
        dill_object = dill.dumps(data_save)
        redis_store.set(access_token, dill_object)
        redis_store.expire(access_token, expires_in)
    else:
        expires_in = resp['expires_in']
        dill_object = dill.dumps(dt_db[0])
        redis_store.set(access_token, dill_object)
        redis_store.expire(access_token, expires_in)

    data_result = {
        "Access-Token": access_token,
        "email": req['email'],
        "expires": expires_in
    }
    result = jsonify(data_result)
    return result