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










"""
The following codes describe the Table as it is in the Database and its Schema.
There are a total of two tables in our Database: 
    - The Car Service Table
    - The User Table
    - Black List Token Table
"""