from email.quoprimime import body_check
from flask_jwt_extended import get_jwt
from flask_restx import Resource, fields
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from ..models.activityDB import ActivityDB
from ..schema.activitySchema import ActivitySchema
from ..config.auth import auth_required
from ..config.core import cache, db, api, ns1
from ..config.utils import required_body, jsonify 

insert_fields = ns1.model('insert', {
    'date'      : fields.Date,
    'check_in'  : fields.String,
    'activity'  : fields.String,
    'status'    : fields.String,
    'check_out' : fields.String
})

delete_fields = ns1.model('delete', {
    'date': fields.Date
})

class Activity(Resource):
    @api.doc(body=insert_fields, security='apikey', responses={
        200: 'OK',
        403: 'Forbidden',
        412: 'Precondition Failed',
        502: 'Bad Gateway'
    })
    @auth_required(['user'])
    @required_body([
        'date',
        'check_in',
        'activity',
        'status',
        'check_out'
    ])
    def post(self):
        """Insert User's activity"""
        body = request.get_json()
        print(get_jwt()['sub'])
        userID = get_jwt()['sub']
        body['user_id'] = userID 
        
        # TODO : Validation schema user
        try:
            userData = ActivitySchema().load(body)
        except ValidationError as err:
            return jsonify(
                success = False,
                message = err.messages,
                code    = 403
            )
        # TODO: Checking Date uniqueness
        date = ActivityDB.query \
            .filter(ActivityDB.date == userData['date'], ActivityDB.user_id == userID)

        if date.count():
            return jsonify(
                success = False,
                message = 'Date is already exist',
                code    = 412
                
            )
            
        # TODO : Insert received data request
        try:
            user = ActivityDB(**userData)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(
                success = False,
                message = str(e),
                code    = 502
            )
        
        return jsonify(
            data    = userData,
            success = True,
            message = 'Insert activity success',
            code    = 200
        )

    @api.doc(body=insert_fields, security='apikey', responses={
        200: 'OK',
        403: 'Forbidden',
        412: 'Precondition Failed',
        502: 'Bad Gateway'
    })
    @auth_required(['user'])
    @required_body([
        'date',
        'check_in',
        'activity',
        'status',
        'check_out'
    ])
    def put(self):
        """Update User's activity"""
        body = request.get_json()
        userID = get_jwt()['sub']
        body['user_id'] = userID 
        
        # TODO : Validation schema user
        try:
            userData = ActivitySchema().load(body)
        except ValidationError as err:
            return jsonify(
                success = False,
                message = err.messages,
                code    = 403
            )
        # TODO: Checking Date uniqueness
        date = ActivityDB.query \
            .filter(ActivityDB.date == userData['date'], ActivityDB.user_id == userID)

        if not date.count():
            return jsonify(
                success = False,
                message = "Date doesn't exist",
                code    = 412
                
            )

        activityData = date.first()
        if not body['check_in']:
            body['check_in'] = activityData.check_in
        
        if not body['activity']:
            body['activity'] = activityData.activity
        
        if not body['status']:
            body['status'] = activityData.status
        
        if not body['check_out']:
            body['check_out'] = activityData.check_out

        # TODO : Validation schema activity
        try:
          activityRow = ActivitySchema().load(body)
        except ValidationError as err:
            return jsonify(
                success = False,
                message = err.messages,
                code    = 403
            )
        
        
        # TODO : Update activity
        try:
            date.update(activityRow)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(
                success = False,
                message = str(e),
                code    = 502
            )
        
        return jsonify(
            data    = userData,
            success = True,
            message = 'Update activity success',
            code    = 200
        )

    @api.doc(body=delete_fields, security='apikey', responses={
        200: 'OK',
        502: 'Bad Gateway'
    })
    @auth_required(['user'])
    @required_body([
        'date'
    ])
    def delete(self):
        """Remove User's activity"""
        body = request.get_json()
        date = body['date']            
        # TODO : Remove detail doctor
        try:
            data = ActivityDB.query \
                .filter(ActivityDB.user_id == get_jwt()['sub'], ActivityDB.date == date).first()    
            db.session.delete(data)
            db.session.commit()
        except SQLAlchemyError as e:
            return jsonify(
                success = False,
                message = str(e),
                code    = 502
            )

        return jsonify(
            success = True,
            message = 'Remove activity success',
            code    = 200
        )

class Get_Activity(Resource):
    @api.doc(body=delete_fields, security='apikey', responses={
        200: 'OK',
        502: 'Bad Gateway'
    }) 
    @cache.cached(timeout=5)
    @auth_required(['user'])
    @required_body([
        'date'
    ])
    def post(self):
        """Get User's activity based on date"""
        body = request.get_json()
        date = body['date']
        # TODO : Get Activity based on date
        userID = get_jwt()['sub']        
        try:
            activityDetail = ActivityDB.query.filter(ActivityDB.date == date, ActivityDB.user_id == userID) \
                .first()
        except SQLAlchemyError as e:
            return jsonify(
                success = False,
                message = str(e),
                code    = 502 
            )

        # TODO : Dump query from DB
        schema = ActivitySchema() 
        
        data = schema.dump(activityDetail)
        activity = data['activity']
        
        return jsonify(
            data    = {"activity-detail": activity},
            success = True,
            message = 'success',
            code    = 200
        )