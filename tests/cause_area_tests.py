import json
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from volunteerapi.models import CauseAreas

class CauseAreaTests(APITestCase):

    fixtures = ['causeAreas', 'users', 'tokens']

    def setUp(self):
        token = Token.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_cause(self):
        cause = CauseAreas()
        cause.label = "Hobbies"
        cause.save()

        response = self.client.get(f"/causeareas/{cause.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Hobbies")
        self.assertEqual(json_response["id"], cause.id)

    def test_get_all_tags(self):
        response = self.client.get("/causeareas")

        json_response = json.loads(response.content)

        self.assertEqual(json_response[0]["label"], "Children")
        self.assertEqual(json_response[1]["label"], "Education")
        self.assertEqual(json_response[2]["label"], "Environment")
        self.assertEqual(json_response[3]["label"], "Healthcare")
        self.assertEqual(json_response[4]["label"], "Seniors")