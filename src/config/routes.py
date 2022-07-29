from .core import *
from ..controller import *

from flask_restx import Resource



class Alive(Resource):
    @cache.cached(timeout=5)
    def get(self):
        """Check if app is running"""
        return 'alive', 200

# TODO: Check APP alive
ns1.add_resource(Alive, '/alive')

# TODO: Employee Login
ns1.add_resource(UserLogin,'/login')

# TODO: Employee Registration
ns1.add_resource(UserRegistration,'/registration')


# TODO: Employee Activity and Attandance
ns1.add_resource(Activity,'/activity')
ns1.add_resource(Get_Activity,'/activity/date')
ns1.add_resource(AttandanceHistory,'/attandance')

