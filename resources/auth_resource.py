from flask import request

from flask_restplus import Resource
from utils.dto import AuthDto
from marshmallow import ValidationError

from service.auth_service import Auth

api_auth = AuthDto.api
_user_auth = AuthDto.user_auth


        
@api_auth.route('/login')
class LoginApi(Resource):

    @api_auth.doc('user login')
    @api_auth.expect(_user_auth, validate=True)
    def post(self):
        data = request.get_json()
        return Auth.login_user(data=data)


@api_auth.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api_auth.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)