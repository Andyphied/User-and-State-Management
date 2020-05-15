import datetime
import random

from flask import request

from utils.dto import StateDto
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource
from resources.errors import InternalServerError,NoAuthorizationError
from utils.decorator import admin_token_required
from service.state_service import save_new_state


api = StateDto.api
_state = StateDto.state


@admin_token_required
@api.route('/')
class State(Resource):    

    @jwt_required
    @api.response(201, 'State Sucessfully Added')
    @api.doc('Add State')
    @api.expect(_state, validate=True)
    def post(self):
        try:
            data = request.get_json()
            return save_new_state(data)
        except NoAuthorizationError:
            raise NoAuthorizationError
        except Exception as e:
            print(e)
            raise InternalServerError


