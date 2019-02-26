from app.models import model as db
from app.helper.rest import response
from app import redis_store
from functools import wraps
from flask import request
import dill


def get_jwt_identity():
    access_token = request.headers['Access-Token']
    stored_data = redis_store.get('{}'.format(access_token))
    stored_data = dill.loads(stored_data)
    try:
        check_data = db.get_by_id("tb_userdata", "email", stored_data['email'])[0]
    except Exception:
        return(response(400, message=str(Exception)))
    return str(check_data['id_userdata'])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Access-Token' not in request.headers:
            return response(400, message=" Invalid access token ")
        else:
            access_token = request.headers['Access-Token']
            stored_data = redis_store.get('{}'.format(access_token))
            if not stored_data:
                return response(400, message=" Invalid access token ")

            stored_data = dill.loads(stored_data)
            try:
                db.get_by_id("tb_userdata", "email", stored_data['email'])[0]
            except Exception:
                return response(400, message="Invalid access token ")
        return f(*args, **kwargs)
    return decorated_function

