from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from .core import jwt
from .utils import jsonify
from ..models import UserDB

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserDB.query.filter_by(id=identity).one_or_none()

def auth_required(types):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
            except Exception:
                return jsonify(
                    message = "Token is invalid",
                    code    = 403
                )  
            for i in types:
                if claims[i]:
                    return fn(*args, **kwargs)
                
                return jsonify(
                    message = "Access denied!!!",
                    code    = 403
                )
        return decorator
    return wrapper