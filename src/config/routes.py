from .core import *
from ..controller import *

from flask_restx import Resource



class Alive(Resource):
    @cache.cached(timeout=50)
    def get(self):
        alive = ['hello world' for _ in range(1000)]
        return alive, 200

# TODO: Check APP alive
api.add_resource(Alive, '/alive')

# TODO: Employee Login
api.add_resource(UserLogin,'/login')

# TODO: Employee Registration
api.add_resource(UserRegistration,'/registration')

# TODO: Employees Logout
api.add_resource(UserLogout,'/logout')

# TODO: Employee Activity and Attandance
api.add_resource(Activity,'/activity')
api.add_resource(AttandanceHistory,'/attandance')
