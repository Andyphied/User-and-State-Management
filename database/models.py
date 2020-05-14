import datetime


from sqlalchemy.ext.hybrid import  hybrid_property
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import jwt
from app.config import key


mongo = PyMongo()
flask_bcrypt = Bcrypt()
ma = Marshmallow
db = SQLAlchemy()
"""
Defining The Two Database:
    - Database 1: Monodb Database
    - Database 2: Postgre Database
"""

# Database 1
"""
The following codes describe the Table as it is in the Database.
There are a total of two tables in our Database: 
    - Black List Token Table
    - The State Tables
    - The User Table
"""
# Blacklist Token Collection
BlacklistToken_1 = mongo.db.blacklisttoken


# Blacklist Token Collection
State_1 = mongo.db.state


# Blacklist Token Collection
User_1 = mongo.db.user



# Database 2
"""
The following codes describe the Table as it is in the Database and its Schema.
There are a total of two tables in our Database: 
    - Black List Token Table
    - The States Table
    - The User Table
"""

class BlacklistToken_2(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken_2.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class State_2(db.Model):
    __tablename__ = "state"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_by = db.Column(db.String(50), unique=True)
    date_updated = db.Column(db.DateTime, nullable=False,)
    date_created = db.Column(db.DateTime, nullable=False,)
    state = db.Column(db.String(100), unique=True, nullable=False)
    updated_by = db.Column(db.String(50), nullable=False, unique=False)


    def __repr__(self):
        return "<State '{}'>".format(self.state)

class User_2(db.Model):
    __tablename__ = "user"
    
    id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(50), unique=True)
    _password_hash = db.Column('password', db.String(100))
    
    """
    password: ensures password attribute is read only
    hash_password: coverts password to hashs
    check_password: confirms if password matches user password in the database

    """

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext):
        self._password_hash = flask_bcrypt.generate_password_hash(plaintext).decode('utf8')


    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)

    def encode_auth_token(self, user_id):
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
            is_blacklisted_token = BlacklistToken_2.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'                                                                        

    

    def __repr__(self):
        return "<User '{}'>".format(self.user_name)



class StateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = State_2
    
    id = ma.auto_field
    created_by = ma.auto_field
    date_updated = ma.auto_field
    date_created = ma.auto_field
    state = ma.auto_field
    updated_by = ma.auto_field


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User_2
    id = ma.auto_field
    email = ma.auto_field
    registered_on = ma.auto_field
    public_id = ma.auto_field
    user_name = ma.auto_field
    password = ma.auto_field
    
