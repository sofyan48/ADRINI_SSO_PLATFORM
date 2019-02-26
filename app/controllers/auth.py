from app import app, redis_store
from flask import request, url_for, request, jsonify
from flask import session, redirect
from app.libs import utils
from app.helper.rest import response
from app.models import model as db
from app import db as dbq
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import hashlib, uuid, dill


@app.route('/login/add', methods=['POST'])
def insert_login():
    password_hash = pbkdf2_sha256.hash(request.form['password'])
    data_insert = {
        "id_userdata" : request.form['userdata_id'],
        "username" : request.form['username'],
        "password" : password_hash,
    }

    try:
        db.insert(table="tb_user", data=data_insert)
    except Exception as e:
        respon = {
            "status": False,
            "error": str(e)
        }
    else:
        data_insert = {
            "userdata_id" : request.form['userdata_id'],
            "username" : request.form['username'],
        }
        respon = {
            "status": True,
            "data": data_insert
        }
    return response(200, message=respon)

@app.route('/login')
def sigin():
    username = request.form['username']
    password = request.form['password']

    user = db.get_by_id(table= "tb_user",field="username",value=username)

    if not user or not pbkdf2_sha256.verify(password, user[0]['password']):
        return response(status_code=401, data="You Not Authorized")
    else:
        random_string = uuid.uuid4()
        raw_token = '{}{}'.format(random_string, username)
        access_token = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

        userdata = db.get_by_id(table= "tb_userdata", field="id_userdata", value=user[0]['id_userdata'])
        stored_data = {
            'id_userdata': user[0]['id_userdata'],
            'email': userdata[0]['email'],
            'username': username
        }
        dill_object = dill.dumps(stored_data)
        redis_store.set(access_token, dill_object)
        redis_store.expire(access_token, 3600)
        data = {
            'email': userdata[0]['email'],
            'Access-Token': access_token,
            'expires': 3600
        }
        return response(200, data=data)