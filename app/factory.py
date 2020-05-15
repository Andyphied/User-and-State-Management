import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.celery_utils import init_celery

# Discover name of package or module and pass to Flask App

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]

def create_app(app_name=PKG_NAME, **kwargs):
    app = Flask(app_name)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    from .app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from database.models import db, flask_bcrypt
    from database.collections import mongo
    # Initiliaze Database 1
    mongo.init_app(app)

    # Initiliaze Database 2
    db.init_app(app)

    flask_bcrypt.init_app(app)

    return app
