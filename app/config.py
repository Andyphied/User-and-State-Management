import os


basedir = os.path.abspath(os.path.dirname(__file__))

"""
This Module contains the various configurations required for our
diffrent enviroments:

Development
Testing
Production 
Staging

"""

class Config(object):
    DEBUG = False
    TESTING =False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
    MONGO_URI =  os.environ.get('MONGO_URI')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING =True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False



key = Config.SECRET_KEY