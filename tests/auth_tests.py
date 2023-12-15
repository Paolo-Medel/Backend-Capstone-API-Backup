import json
from rest_framework import status
from rest_framework.test import APITestCase

class AuthorizationTests(APITestCase):

    fixtures = ['users', 'tokens']

    def test_login(self):
        url = '/login'

        data = {
            "email": "meg@ducharme.com",
            "password": "ducharme"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["valid"], True)
        self.assertEqual(json_response["token"], "d74b97fbe905134520bb236b0016703f50380dcf")

class RegisterTests(APITestCase):

    fixtures = ['users', 'tokens']

    def test_register_user(self):
        url='/register'

        data = {
            'email': 'me2@me.com',
            'password': 'me2',
            'first_name': 'me',
            'last_name': 'me',
            'bio': 'im me2',
            'profile_image_url': 'here is url',
            'is_business': False,
            'cause_area': []
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(json_response["token"])
