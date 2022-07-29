from .init import *
from .main import *
from flask_restx import Api, Namespace
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

Compress(app)
api = Api(app, authorizations=authorizations, title='Attandance Documentation API',
    description='swagger always awesome')
ns1 = Namespace('API', description='all of endpoint with prefix /user')
api.add_namespace(ns1, path='/user')

cors   = CORS(app,
              origins=['http://localhost:5000','http://localhost:5001'],
              methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
              allow_headers=['Authorization', 'Keep-Alive'])
cache  = Cache(app)
db     = SQLAlchemy()
ma     = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt    = JWTManager(app)

app.app_context().push()
db.init_app(app)
db.create_all()
