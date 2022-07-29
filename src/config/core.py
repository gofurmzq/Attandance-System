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
api = Api(app, authorizations=authorizations, title='Hospital Documentation API',
    description='swagger always awesome')
api.add_namespace(Namespace('API', description='swagger always awesome', ordered=True))
cors   = CORS(app,
              origins=['http://localhost:5000','http://localhost:5001'],
              methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
              allow_headers=['Authorization', 'Keep-Alive'])
cache  = Cache(app)
db     = SQLAlchemy()
ma     = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt    = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()
