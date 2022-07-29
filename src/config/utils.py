import bcrypt as bc
from datetime import datetime as dt
import pytz    
from functools import wraps
from flask import request, make_response, jsonify as flask_jsonify, make_response, current_app
from flask_babel import lazy_gettext as _
import jwt
from werkzeug.exceptions import HTTPException as WerkzeugHttpException
from .core import *
from .init import Config

def encryptBC(key):
    if isinstance(key, str):
        key = bytes(key, 'utf-8')

    return str(bc.hashpw(key, bc.gensalt()), 'utf8')

def checkBC(passwd, check):
    if isinstance(passwd, str) and isinstance(check, str):
        check  = bytes(check, 'utf-8')
        passwd = bytes(passwd, 'UTF-8')

    return bc.hashpw(check, passwd) == passwd

def jsonify(data=None, meta=None, success=False, message=None, code=200):
    if not message:
        message = _('Success')
 
    result = {
        'data': data,
        'meta': meta,
        'success': success,
        'message': message,
        'code': code
    }

    return make_response(flask_jsonify(result),code)


def create_auth_successful_response(token, status_code, message):
    response = flask_jsonify(
        status="success",
        message=message,
        access_token=token,
        token_type="bearer",
        expires_in=_get_token_expire_time(token),
    )
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response

def _get_token_expire_time(token):
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    epochtime =decoded["exp"]
    # return dt.fromtimestamp(epochtime,dt.fromtimestamp(epochtime tz=pytz.timezone('Asia/Jakarta'))
    return dt.fromtimestamp(epochtime).astimezone(pytz.timezone('Asia/Jakarta'))

def required_body(valid):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json()
            if body is None:
                return jsonify(message='Missing body required',code=400)
            if all(key in body for key in valid):
                return func(*args, **kwargs)
            return jsonify(message='Missing body required',code=400)
        return wrapper
    return decorator

class ErrorMessage():
    '''
    An error message gate for Marshmallow and Flask Babel
    '''
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def format(self, **kwargs):
        return [self.code, _(self.message, **kwargs)]


class HttpException(WerkzeugHttpException):  # this is to modify default HttpException
    code = 500  
    description = _('An error occured')
    message_code = None  # specific to this project, NOT HTTP Response Code

    def __init__(self, message=None, message_code=None, status_code=None, response=None):
        super().__init__(description=message, response=None)
        if status_code is not None:
            self.code = status_code
        elif message_code is not None:
            self.message_code = message_code
        else:
            self.message_code = self.code


