import unittest
import datetime

from database.collections import User
from test.base import BaseTestCase, test


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user =({
            'email':'test@test.com',
            'password': 'test',
            'registered_on': datetime.datetime.now()
        })
        user = test.insert_one(user)
        auth_token = User.encode_auth_token(user.inserted_id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user =({
            'email':'test@test.com',
            'password': 'test',
            'registered_on': datetime.datetime.now()
        })
        test.insert_one(user)
        item =test.find_one({'email':'test@test.com'})
        auth_token = User.encode_auth_token(item.get('_id'))
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8") ) == user['_id'])


if __name__ == '__main__':
    unittest.main()