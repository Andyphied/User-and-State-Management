import uuid
import datetime

from flask import request
from database.models import db, State_2
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError, StateAlreadyExistsError
from database.collections import Blacklist_Token, State, User
from task.state_task import save_state


""" 
    Handles All Of the State Related Services 

    save_new_user: Helps save the user data to the db

"""

def get_logged_in_user(new_request):
    # get the auth token
    auth_token = new_request.headers.get('Authorization')
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.find_user_with_id(_id=resp)
            return user



def save_changes(data):

    user = get_logged_in_user(request)
    data['created_by'] = user['user_name']
    data['updated_by'] = user['user_name']

    save_state.delay(data)

    new_user = State_2(
            created_by = data['created_by'],
            date_created =datetime.datetime.now(),
            date_updated = datetime.datetime.now(),
            state = data['state'],
            updated_by= data['updated_by']
        )
        
    db.session.add(new_user)
    db.session.commit()


def  save_new_state(data):
    
    user = State.check_state(data)
    if user:
        return StateAlreadyExistsError
    try:
        save_changes(data)

    except Exception as e:
        print (e)
        raise InternalServerError

    else:
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object




