import datetime
import jwt
from app.config import key

from database.models import flask_bcrypt
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
InternalServerError, NoDataReceived
from flask_pymongo import PyMongo


mongo = PyMongo()


# Database 1
"""
Description of the Table as it is in the Database.
There are a total of two tables in our Database: 
    - Black List Token Table
    - The State Tables
    - The User Table
"""

class Blacklist_Token():
    def __init__(self):
        pass

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = mongo.db.blacklist_token.find_one({'token': str(auth_token)})
        if res:
            return True
        else:
            return False


    @classmethod
    def store_blacklist_token(cls, token ):
        try:
            users = mongo.db.blacklist_token
            if token is not None:
                users.insert_one({
                    'token': token,
                    'blacklisted_on': datetime.datetime.now()
                })
            else:
                return NoDataRecived
        except:
            return InternalServerError  

class User():

    def __init__(self):
        pass
    

    @classmethod
    def check_user(cls, data):
        users = mongo.db.users
        user = users.find_one({'email': data['email']})
        if user:
            return user
        else:
            return False

    @classmethod
    def get_a_user(cls, public_id):
        try:
            users = mongo.db.users
            user = users.find_one({'email': public_id})
            return user
        except:
            return InternalServerError 

    @classmethod
    def get_all_user(cls):
        try:
            users = mongo.db.users
            all_user = users.find()
            return all_user
        except:
            return InternalServerError  

    
    @classmethod
    def store_user(cls, data=None ):
        try:
            users = mongo.db.users
            if data is not None:
                users.insert_one({
                    'admin': False,
                    'email': data['email'],
                    'registered_on': datetime.datetime.now(),
                    'public_id': str(uuid.uuid4()),
                    'user_name': data['username'],
                    '_password_hash': flask_bcrypt.generate_password_hash(
                                        data['password']
                                    ).decode('utf8')
                })
            else:
                return NoDataRecived
        except:
            return InternalServerError  

    @classmethod
    def store_admin(cls, data=None ):
        try:
            users = mongo.db.users
            if data is not None:
                users.insert_one({
                    'admin': True,
                    'created_by': data['created_by'],
                    'registered_on': datetime.datetime.now(),
                    'public_id': str(uuid.uuid4()),
                    'user_name': data['username'],
                    '_password_hash': flask_bcrypt.generate_password_hash(
                                        data['password']
                                    ) 
                })
            else:
                return NoDataRecived
        except:
            return InternalServerError  

    @classmethod
    def encode_auth_token(cls, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = Blacklist_Token.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        
    @staticmethod
    def check_password(user, password):
        """
        Confirms Password
        :param user:
        :param password:
        :return: Boolean
        """
        return flask_bcrypt.check_password_hash(user.get("_password_hash"), password)

    @classmethod
    def find_user_with_id(cls, _id):
        users = mongo.db.users
        return users.find_one({'_id': id})



class State():
    def __init__(self):
        pass
    
    @classmethod
    def store_state(cls, data=None ):
        try:
            users = mongo.db.states
            if data is not None:
                users.insert_one({
                    'created_by': data['created_by'],
                    'date_created': datetime.datetime.now(),
                    'date_updated': datetime.datetime.now(),
                    'state': data['state'],
                    'updated_by': data['updated_by']
                })
            else:
                return NoDataRecived
        except:
            return InternalServerError 

    @classmethod
    def check_state(cls, data):
        users = mongo.db.users
        user = users.find_one({'state': data['state']})
        if user:
            return True
        else:
            return False


    
