from flask_restplus import Namespace, fields

""" Data Transfer Objects"""

class UserDto:
    api = Namespace('user', description='user realted opertaions')
    user = api.model('user', {
                'email': fields.String(required=True, description='User email address'),
                'username': fields.String(required=True, description='User username'),
                'password': fields.String(required=True, description='User password'),
                'public_id': fields.String(description='User unique identifier')

    })


class AuthDto:
    api = Namespace('auth', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class StateDto:
    api = Namespace('state', description='Creation of States')
    state = api.model('state',{
        'state': fields.String(required=True, description='The name of state')
    })