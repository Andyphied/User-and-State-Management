from flask import Blueprint
from flask_restplus import Api
from resources.user_resources import api as user_ns
from resources.auth_resource import api_auth as auth_ns
from resources.state_resource import api as state_ns
api_bp = Blueprint('api', __name__)

api = Api(api_bp,
    title = 'Users and State Management Service',
    version = '0.10',
    description = ("This Service would be responsible for the creation of users,"
                    "authentication mangement using a JWT, and creation of states.")
    

)

api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(state_ns, path='/me/state')