from flask_testing import TestCase
from database.collections import mongo
from run import app

test = mongo.db.test

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        mongo.db.test

    def tearDown(self):
        test.remove()
        test.drop()