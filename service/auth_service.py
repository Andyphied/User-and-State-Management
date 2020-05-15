import datetime

from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError
from flask_jwt_extended import create_access_token
from service.blacklist_service import save_token
from database.collections import User


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.check_user(data)
            authorized = User.check_password(user, data.get('password'))
            if not authorized:
                return UnauthorizedError

            auth_token = User.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                                'status': 'success',
                                'message': 'Successfully logged in.',
                                'Authorization': auth_token.decode()
                }
                return response_object, 200
        
        except Exception as e:
            print(e)
            return InternalServerError


    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.find_user_with_id(_id=resp)
                response_object = {
                    'status': 'success',
                    'data': {
                        'public_id': user['public_id'],
                        'email': user['email'],
                        'admin': user['admin'],
                        'registered_on': str(user['registered_on'])
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
