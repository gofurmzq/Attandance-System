from datetime import datetime
from flask import request, jsonify as flask_jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from flask_restx import Resource, abort
from http import HTTPStatus
from marshmallow import ValidationError
from src.config.utils import encryptBC, checkBC, jsonify, required_body, create_auth_successful_response
from src.config.core import api, login
from sqlalchemy.exc import SQLAlchemyError
from ..config import db, Config
from ..models import UserDB
from ..schema import UserSchema

class UserLogin(Resource):
    @api.doc(body=login, responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'user account is not exist'
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

        # TODO : Check username if exist
        employee = UserDB.find_by_email(email)
        if not employee or not checkBC(employee.password, password):
            abort(HTTPStatus.UNAUTHORIZED, "email or password does not match", status="fail")
        
        schema   = UserSchema()
        
        #TODO : Validation data user
        data = schema.dump(employee)
            
        access_token = create_access_token(
                identity=data.id,
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
    @api.doc(body=login, responses={
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
        if UserDB.find_by_email(email):
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

class UserLogout(Resource):
    """Log out an user and unset an access_token"""
    @api.doc(body=login, responses={
        200: 'OK',
        401: 'Login Failed'
    })
    def post(self):
        response = flask_jsonify({"msg": "logout successful"})
        if unset_jwt_cookies(response):
            return response, 200
        abort(HTTPStatus.UNAUTHORIZED, 'Login Failed', status="fail")
