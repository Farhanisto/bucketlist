
from tests.base import BaseTestCase,app,db
from flask import json
import unittest
from models.models import User


def register_user(self, username, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """Test user registration works correctly."""
        with self.client:
            response = register_user(self, 'joe', '12345')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_register_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(
            username='test',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = register_user(self, 'test', 'test')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='joe',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Try again')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_valid_user_login(self):
        user = User(username='test',
                   password='test')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post('auth/login', data=json.dumps(dict(username='test',
                                                                          password='test')),
                                        content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['auth_token'])


if __name__ == '__main__':
    unittest.main()