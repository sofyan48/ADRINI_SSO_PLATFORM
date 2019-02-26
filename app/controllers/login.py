from app import app, redis_store, OAuthException
from flask import render_template, g
from flask import session, redirect, url_for, request, jsonify
from app.libs import utils
from app.models import model
from app.helper import oauth
import os, dill


@app.route('/google')
def google_login():
    callback = url_for('authorized', _external=True)
    return oauth.google.authorize(callback=callback)

@app.route(os.getenv('REDIRECT_URI'))
@oauth.google.authorized_handler
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


@app.route('/facebook')
def facebook():
    callback = url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return oauth.facebook.authorize(callback=callback)



@app.route(str(os.getenv('REDIRECT_URI_FB')))
@oauth.facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    # session['oauth_token'] = (resp['access_token'], '')
    # me = facebook.get('/me')
    # return str(me)

@app.route('/github')
def login():
    return oauth.github.authorize(callback=url_for('github_authorized', _external=True))

@app.route(os.getenv('REDIRECT_URI_GITHUB'))
def github_authorized():
    resp = oauth.github.authorized_response()
    token = None
    for i in resp:
        if i == 'access_token':
            token = resp[i]
    req = utils.get_http('https://api.github.com/user?access_token='+token,
                  None, None)
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
        dill_object = dill.dumps(data_save)
        redis_store.set(token, dill_object)
        redis_store.expire(token, 3600)
    else:
        dill_object = dill.dumps(dt_db[0])
        redis_store.set(token, dill_object)
        redis_store.expire(token, 3600)

    data_result = {
        "Access-Token": token,
        "email": req['email'],
        "expires": 3600
    }
    result = jsonify(data_result)
    return result

@oauth.github.tokengetter
def get_github_oauth_token():
    return ""

@app.route('/twitter')
def tweet():
    callback_url = url_for('tweet_oauthorized', next=request.args.get('next'))
    return oauth.twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route(str(os.getenv('REDIRECT_URI_TWITTER')))
def tweet_oauthorized():
    g.access_token = None
    resp = oauth.twitter.authorized_response()
    access_token = resp['oauth_token']
    g.access_token = access_token
    a = oauth.twitter.get("lists/show.json")
    return str(a)

@oauth.twitter.tokengetter
def get_twitter_token():
    return g.access_token
