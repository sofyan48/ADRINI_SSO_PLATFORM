from app import app, redis_store
from flask import request, url_for, request, jsonify
from flask import session, redirect
from app.libs import utils
from app.helper.rest import response
from app.models import model as db
from app import db as dbq
from app.middlewares.auth import get_jwt_identity, login_required
import hashlib, uuid


@app.route("/user/get", methods=['GET'])
@login_required
def user_get():
    id_userdata = get_jwt_identity()
    obj_userdata = list()
    column = db.get_columns('tb_userdata')
    try:
        results = list()
        query = "select * from tb_userdata where id_userdata='"+id_userdata+"' "
        data = db.query(query)
        rows = dbq.fetchall()
        for row in rows:
            print(row)
            results.append(dict(zip(column, row)))
    except Exception as e:
        return response(200, message=str(e))
    else:
        for i in results :
            data = {
                "id_userdata": str(i['id_userdata']),
                "email" : i['email'],
                "first_name" : i['first_name'],
                "last_name" : i['last_name'],
                "location" : i['location']
            }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)

@app.route("/user/delete", methods=['GET'])
@login_required
def delete():
    id_userdata = get_jwt_identity()
    try:
        db.delete(
                table="tb_userdata", 
                field='id_userdata',
                value=id_userdata
            )
    except Exception as e:
        message = {
            "status": False,
            "error": str(e)
        }
    else:
        message = "removing"

    finally:
        return response(200, message=message)

@app.route("/user/update", methods=['POST'])
@login_required
def update():
    id_userdata = get_jwt_identity()
    data = {
        "where":{
            "userdata_id": id_userdata
        },
        "data":{
            "email" : request.form['email'],
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "location" : request.form['location']
        }
    }

    try:
        db.update("tb_userdata", data=data)
    except Exception as e:
        message = {
            "status": False,
            "error": str(e)
        }
    else:
        message = {
            "status": True,
            "data": data
        }
    finally:
        return response(200, message=message)

@app.route('/user/add', methods=['POST'])
def insert_user(self):
    random_string = uuid.uuid4()
    raw_token = '{}{}'.format(random_string, request.form['email'])
    access_token = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    data_insert = {
        "email" : request.form['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "location" : request.form['location'],
        "sso_id" : access_token,
    }
    try:
        result = db.insert(table="tb_userdata", data=data_insert)
    except Exception as e:
        data = {
            "status": False,
            "error": str(e)
        }
        return response(200, message=data)
    else:
        data = {
            "status": True,
            "data": data_insert,
            "id": result
        }
        return response(200, data=data)