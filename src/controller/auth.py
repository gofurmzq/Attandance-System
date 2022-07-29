from datetime import datetime
from flask import request, jsonify as flask_jsonify, session
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_restx import Resource, abort, fields
from http import HTTPStatus
from marshmallow import ValidationError
from src.config.utils import encryptBC, checkBC, jsonify, required_body, create_auth_successful_response
from src.config.core import api
from sqlalchemy.exc import SQLAlchemyError
from ..config import db, Config, ns1
from ..models import UserDB
from ..schema import UserSchema

login_fields = ns1.model('login', {
    'email': fields.String,
    'password':fields.String
})

registration_fields = ns1.model('registration', {
    'name'      : fields.String,
    'email'     : fields.String,
    'password'  : fields.String,
    'gender'    : fields.String,
    'birthdate' : fields.Date
})

class UserLogin(Resource):
    @api.doc(body=login_fields,responses={
        200: 'OK',
        401: 'Unauthorized',
        403: 'Forbidden'
    })
    @required_body([
        'email',
        'password',
    ])
    def post(self):
        """Authenticate an existing user and return an access token."""
        body = request.get_json()

        email = body['email']
        password = body['password']
        
        # TODO: Validating body received
        try:
            UserSchema().load(body)
        except ValidationError as err:
            return jsonify(
                success = False,
                message = err.messages,
                code    = 403
            )
        # TODO : Check username if exist
        employee = UserDB.query.filter(UserDB.email == email)
        if not employee.count() or not checkBC(employee.first().password, password):
            abort(HTTPStatus.UNAUTHORIZED, "email or password does not match", status="fail")
        
        schema   = UserSchema()
        
        #TODO : Dump data user
        data = schema.dump(employee.first())
        
        access_token = create_access_token(
                identity=data['id'],
                additional_claims={
                    'admin' : False,
                    'user'  : True
                }
            )
        return create_auth_successful_response(
            token=access_token,
            status_code=HTTPStatus.OK,
            message="successfully logged in",
        )
     

class UserRegistration(Resource):
    @api.doc(body=registration_fields, responses={
        200: 'OK',
        401: 'Unauthorized',
        409: 'Conflict',
        502: 'Bad Gateway'
    })
       
    @required_body([
        'name',
        'email',
        'password',
        'gender',
        'birthdate'
    ])
    def post(self):
        """Register a new user and return an access_token"""
        body = request.get_json()
  
        # TODO: Validating body received
        try:
            body['birthdate'] = datetime.strptime(body['birthdate'], Config.DATEFORMAT).date().isoformat()
            employee_data = UserSchema().load(body)
        except ValidationError as err:
            return jsonify(
                success = False,
                message = err.messages,
                code    = 403
            )
            
        email = employee_data['email']      
        # TODO: Checking email uniqueness
        if UserDB.query.filter(UserDB == email).count():
            abort(HTTPStatus.CONFLICT, f"{email} is already registered", status="fail")
        
        employee_data['password'] = encryptBC(employee_data['password'])
        
        # TODO : Insert to database
        try:
            new_user = UserDB(**employee_data)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
                return jsonify(
                    success = False,
                    message = str(e),
                    code    = 502
                )
        
        access_token = create_access_token(
                identity=new_user.id,
                additional_claims={
                    'admin' : False,
                    'user'  : True
                }
            )

        return create_auth_successful_response(
            token=access_token,
            status_code=HTTPStatus.CREATED,
            message="successfully registered",
        )
