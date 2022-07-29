__VERSION__     = '1.0.0'
__API_VERSION__ = 'v1'
__APP_NAME__    = 'Attandace System Mitramas'

from datetime import datetime
from datetime import timedelta
import pytz
from flask import Flask, g
from flask_babel import lazy_gettext as _
from flask_jwt_extended import get_jwt, create_access_token, set_access_cookies, get_jwt_identity
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException as WerkzeugHttpException
from .init import *
from .utils import ErrorMessage, HttpException, jsonify
from datetime import timedelta

app = Flask(__APP_NAME__, template_folder=Config.TEMPLATE_FOLDER, static_folder=Config.STATIC_ROOT, static_url_path=Config.STATIC_URL)
app.config.from_object(ProdConfig())
app.app_context().push()


''' TODO: Using an `after_request` callback, we refresh any token that is within 30
minutes of expiring. Change the timedeltas to match the needs of your application.'''
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(pytz.timezone('Asia/Jakarta'))
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

# TODO: auto close connection db when teardown
def close_db(error=None):
    def _close_db(db_name):
        if hasattr(g, db_name):
            getattr(g, db_name).close()

    for db_name in ['hospital_dashboard_db']:
            _close_db(db_name)
    app.teardown_request(close_db)

# TODO: handling marshmallow's ValidationError
def handle_validation_error_exception(exception):
    message = exception.messages
    first_key = list(message.keys())

    if len(first_key):
        first_key = first_key[0]

    message = message[first_key]
    if isinstance(message, ErrorMessage):
        code = message.code
        message = message.message
    else:
        if not isinstance(message, list):
            message = [message]

        if len(message) > 1:
            code, message = message
        else:
            # default error message
            code = 400
            message = f'{first_key}: {message[0]}'

    return jsonify(
        data=None,
        success=False,
        message=message,
        code=code
    ), 400
app.errorhandler(ValidationError)(handle_validation_error_exception)


# TODO: handle HttpException
def handle_http_exception(http_exception):
    if http_exception.code == 400:
        message = _('Please check your input data')
        if http_exception.description:
            message = http_exception.description
    else:
        errors = None
        message = http_exception.description

    return jsonify(
        data=None,
        success=False,
        message=message,
        code=http_exception.message_code
    ), http_exception.code
app.errorhandler(HttpException)(handle_http_exception)

# TODO: handle Werkzeug
def handle_werkzeug_http_exception(http_exception):
    return jsonify(
        data=None,
        success=False,
        message=http_exception.description,
        code=http_exception.code
    ), http_exception.code
app.errorhandler(WerkzeugHttpException)(handle_werkzeug_http_exception)

# TODO: unhadle Exception
def unhandled_exception(error):
    if not app.debug:
        if app.env == 'development':
            raise error

        return jsonify(
            data=None,
            success=False,
            message=_('An error occured'),
            code=500
        ), 500
    
    raise error
app.errorhandler(Exception)(unhandled_exception)

