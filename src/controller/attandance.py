from datetime import datetime
from flask_restx import Resource
from flask_jwt_extended import get_jwt
from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from ..models.activityDB import ActivityDB
from ..schema.activitySchema import ActivitySchema
from ..config.auth import auth_required
from ..config.core import cache, api, ns1
from ..config.utils import jsonify 

class AttandanceHistory(Resource):
    @api.doc(security='apikey', responses={
        200: 'OK',
        502: 'Bad Gateway'
    }) 
    @cache.cached(timeout=5)
    @auth_required(['user'])
    def get(self):
        """Get Attandance History of User"""
        UserID = get_jwt()['sub']        
        try:
            userDetail = ActivityDB.query.filter(ActivityDB.user_id == UserID) \
                .all()
        except SQLAlchemyError as e:
            return jsonify(
                success = False,
                message = str(e),
                code    = 502 
            )
        print(len(userDetail))
        # TODO : Dump query from DB
        schema = ActivitySchema()
        historyAttandance = []
        for i in range(len(userDetail)):
            data = schema.dump(userDetail[i])
            historyAttandance.append({'check_in' : data['check_in'], 'check_out' : data['check_out']})
        
        return jsonify(
            data    = historyAttandance,
            success = True,
            message = 'History Attandace',
            code    = 200
        )