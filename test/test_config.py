import os
import unittest

from flask import current_app
from flask_testing import TestCase

from run import app
from app.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
            self.assertFalse(app.config['SECRET_KEY'] is '9cf900f4302a746d8da38e0d555fa14a')
            self.assertTrue(app.config['DEBUG'] == True)
            self.assertFalse(current_app == None)
            self.assertTrue(
                app.config['SQLALCHEMY_DATABASE_URI'] == ('postgresql://andyphied:Ericphilip5@localhost/tutdb')
            )
            self.assertTrue(
            app.config['MONGO_URI'] == ('mongodb://localhost:27017/service')
        )



class TestTestingConfig(TestCase):

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is '9cf900f4302a746d8da38e0d555fa14a')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == ('postgresql://andyphied:Ericphilip5@localhost/tutdb')
        )
        self.assertTrue(
            app.config['MONGO_URI'] == ('mongodb://localhost:27017/service')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)



if __name__ == '__main__':
    unittest.main()