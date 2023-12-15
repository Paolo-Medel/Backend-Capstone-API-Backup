import json
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from volunteerapi.models import VolunteerUsers
from django.contrib.auth.models import User

class VolunteerTests(APITestCase):

    fixtures = ['causeAreas', 'users', 'tokens', 'volunteerUsers', 'jobPosts']

    def setUp(self):
        token = Token.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_rare_user(self):

        response = self.client.get(f"/volunteers/{3}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["bio"], "bio 3")
        self.assertEqual(json_response["profile_image_url"], "https://www.example.com/profile3.jpg")
        self.assertEqual(json_response["created_on"], "2022-12-01T08:30:00Z")
        self.assertEqual(json_response["is_business"], False)
        self.assertEqual(json_response["favorite"], [])
        self.assertEqual(json_response["user"]["full_name"], "Jenna Solis")
        self.assertEqual(json_response["user"]["email"], "jenna@solis.com")
        self.assertEqual(json_response["user"]["username"], "jenna@solis.com")
        self.assertEqual(json_response["cause_area"][0]["id"], 2)
        self.assertEqual(json_response["cause_area"][0]["label"], "Children")

    def test_get_volunteers(self):
        response = self.client.get("/volunteers")

        json_response = json.loads(response.content)

        self.assertIsNotNone(json_response[0])
        self.assertIsNotNone(json_response[1])
        self.assertIsNotNone(json_response[2])
        self.assertIsNotNone(json_response[3])
        self.assertIsNotNone(json_response[4])

    def test_update_volunteer(self):
        user = User.objects.create(username="test_user", email="test@example.com")

        volunteer = VolunteerUsers()
        volunteer.bio = 'test'
        volunteer.profile_image_url = '123'
        volunteer.is_business = False
        volunteer.user = user
        volunteer.save()  # Save the volunteer instance to get an ID
        volunteer.cause_area.set([])  # Use set() for many-to-many field
        volunteer.favorite.set([])

        data = {
            "user": user.id,
            "bio": "update",
            "profile_image_url": "https://ychef.files.bbci.co.uk/1280x720/p0gg3k8j.jpg",
        }

        response = self.client.put(f"/volunteers/{volunteer.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/volunteers/{volunteer.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["bio"], "update")
        self.assertEqual(json_response["profile_image_url"], "https://ychef.files.bbci.co.uk/1280x720/p0gg3k8j.jpg")
