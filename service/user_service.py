import uuid
import datetime

from database.models import db, User_2
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError
from database.collections import Blacklist_Token, User
from task.user_task import save_admin, save_blacklist_token, save_state, save_user

""" 
    Handles All Of the User Related Services 

    save_new_user: Helps save the user data to the db

"""


def  save_new_user(data):
    
    user = User.check_user(data)
    if user:
        return EmailAlreadyExistsError
    try:
        save_changes(data)

    except Exception as e:
        print (e)
        raise InternalServerError

    else:
        return generate_token(user)


def get_all_users():
    return User.get_all_user()


def get_a_user(public_id):
    return User.get_a_user(public_id)


def save_changes(data):

    save_user.delay(data)

    new_user = User_2(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            user_name=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.now()
        )
    db.session.add(new_user)
    db.session.commit()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401