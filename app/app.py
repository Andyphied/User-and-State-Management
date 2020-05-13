from flask import Blueprint
from flask_restplus import Api

api_bp = Blueprint('api', __name__)

api = Api(
    api_bp,
    title = 'Users and State Management Service',
    version = '0.10',
    description = ("This Service would be responsible for the creation of users,"
                    "authentication mangement using a JWT, and creation of states.")
    

)