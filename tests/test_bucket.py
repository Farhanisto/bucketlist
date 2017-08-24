from tests.base import BaseTestCase,app,db
from flask import json
import unittest
from models.models import User


def login(self):
    user = User(username='test',
                password='test')
    db.session.add(user)
    db.session.commit()
    with self.client:
        response = self.client.post('auth/login', data=json.dumps(dict(username='test',
                                                                       password='test')),
                                    content_type='application/json')
        return response


class Test_bucket(BaseTestCase):
    def test_bucket_creation(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')

    def test_bucket_creation_loged_out_user(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')
            res_logout = self.client.post(
                '/auth/logout',
                headers={'content-type': 'application/json',
                         'Authorization': access_token})
            self.assertEqual(res_logout.status_code, 200)
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            self.assertEqual(res.status_code, 401)

    def test_bucket_get(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res_post = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))

            res_get = self.client.get(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token})
            data = json.loads(res_get.data.decode())
            self.assertEqual(res_post.status_code, 201)

    def test_bucket_rename(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            resp=self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(resp.data.decode())
            self.assertTrue(resp.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')

            bucket_update = {'name': 'Go to heaven instead'}
            res = self.client.put(
                '/bucket/1',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_update))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 200)

    def test_get_by_id(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')
            resp = self.client.get(
                '/bucket/1',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            self.assertTrue(resp.status_code == 200)

    def test_delete_bucket(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            resp = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(resp.data.decode())
            self.assertTrue(resp.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')

            res = self.client.delete(
                '/bucket/1',
                headers={'content-type': 'application/json',
                         'Authorization': access_token})
            self.assertTrue(res.status_code == 200)


class Test_bucket_items(BaseTestCase):
    def test_bucket_item_creation(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')
            item_content ={'name': 'test item'}
            res = self.client.post(
                '/bucket/1/items',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(item_content))
            self.assertEqual(res.status_code, 201)

    def test_bucket_get_item(self):
        pass
    def test_bucket_rename_item(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')
            item_content = {'name': 'test item'}
            res = self.client.post(
                '/bucket/1/items',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(item_content))
            self.assertEqual(res.status_code, 201)
            item_update = {'name': 'test item'}
            res_get = self.client.put(
                '/bucket/1/items/1',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(item_update))
            self.assertEqual(res_get.status_code, 200)

    def test_delete_bucket_item(self):
        response = login(self)
        with self.client:
            access_token = json.loads(response.data)['auth_token']
            bucket_details = {'name': 'Go to school'}
            res = self.client.post(
                '/bucket/',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(bucket_details))
            data = json.loads(res.data.decode())
            self.assertTrue(res.status_code == 201)
            self.assertTrue(data['name'] == 'Go to school')
            item_content = {'name': 'test item'}
            res = self.client.post(
                '/bucket/1/items',
                headers={'content-type': 'application/json',
                         'Authorization': access_token}, data=json.dumps(item_content))
            self.assertEqual(res.status_code, 201)
            res_get = self.client.delete(
                '/bucket/1/items/1',
                headers={'content-type': 'application/json',
                         'Authorization': access_token})
            self.assertEqual(res_get.status_code, 200)