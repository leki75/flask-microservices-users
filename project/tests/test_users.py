import datetime
from flask import json
from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='michael',
                        email='michael@realpython.com',
                        )),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@realpython.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict()),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(email='michael@realpython.com')),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        with self.client:
            self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='michael',
                        email='michael@realpython.com',
                        )),
                    content_type='application/json',
                    )
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='michael',
                        email='michael@another.com',
                        )),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('username already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='michael',
                        email='michael@realpython.com',
                        )),
                    content_type='application/json',
                    )
            response = self.client.post(
                    '/users',
                    data=json.dumps(dict(
                        username='mikael',
                        email='michael@realpython.com',
                        )),
                    content_type='application/json',
                    )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        user = add_user('michael', 'michael@realpython.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@realpython.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        created = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user('michael', 'michael@realpython.com', created)
        add_user('fletcher', 'fletcher@realpython.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('michael', data['data']['users'][1]['username'])
            self.assertIn('michael@realpython.com', data['data']['users'][1]['email'])
            self.assertIn('fletcher', data['data']['users'][0]['username'])
            self.assertIn('fletcher@realpython.com', data['data']['users'][0]['email'])
            self.assertIn('success', data['status'])
