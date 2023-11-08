from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class TestUserViewSet(APITestCase):
    endpoint = '/api/users/'
    data_user = {
        'email': 'testuser@email.com',
        'username': 'testuser',
        'first_name': 'testuserfrname',
        'last_name': 'testuserlsname',
        'password': 'testpass123',
    }

    def setUp(self):
        self.user = get_user_model().objects.create_user(**self.data_user)
        self.client = APIClient()

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint + str(self.user.id) + '/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_update(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'username': 'test_username_updated'
        }
        response = self.client.patch(
            self.endpoint + str(self.user.id) + '/', data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['username'], data['username'])

    def test_me(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.endpoint + 'me/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create(self):
        data = {
            'email': 'testregister@email.com',
            'username': 'register',
            'first_name': 'register name',
            'last_name': 'register last name',
            'password': 'registerpass',
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertIn('id', response.data)

    def test_list_no_auth(self):
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_no_auth(self):
        response = self.client.get(self.endpoint + str(self.user.id) + '/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_update_no_auth(self):
        data = {}
        response = self.client.patch(
            self.endpoint + str(self.user.id) + '/', data
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_me_no_auth(self):
        response = self.client.get(self.endpoint + 'me/')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
