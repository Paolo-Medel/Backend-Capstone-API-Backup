import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from volunteerapi.models import JobPosts, VolunteerUsers

class PostsTests(APITestCase):
    fixtures = ['users', 'jobPosts', 'volunteerUsers', 'tokens', 'causeAreas']

    def setUp(self):
        self.user = User.objects.first()
        self.volunteer_user = VolunteerUsers.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_posts(self):
        response = self.client.get("/posts")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response[0]["id"], 4)
        self.assertEqual(json_response[1]["id"], 3)

    def test_retrieve_post(self):
        post = JobPosts()
        post.title = 'TestPost'
        post.address = '123 way'
        post.image_url = '123.com'
        post.content = 'heloooooo'
        post.user = self.volunteer_user
        post.save()

        response = self.client.get(f"/posts/{post.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "TestPost")
    
    def test_create_post(self):
        url = "/posts"

        data = {
            "title": "test",
            "address": '123',
            "image_url": '1234',
            "content": "werwte",
            "user": self.volunteer_user.id,
            "cause_area": [2, 3],
            "interested_volunteers": [2]
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_post(self):

        post = JobPosts()
        post.title = 'TestPost'
        post.address = '123 way'
        post.image_url = '123.com'
        post.content = 'heloooooo'
        post.user = self.volunteer_user
        post.save()
        post.cause_area.set([2, 3])
        post.interested_volunteers.set([2, 3])


        data = {
            "title": "test",
            "address": '123',
            "image_url": 'https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1356&h=668&fit=crop',
            "content": "werwte",
            "user": self.volunteer_user.id,
            "cause_area": [2, 4],
            "interested_volunteers": [1, 2],
            "approved": False
        }

        response = self.client.put(f"/posts/{post.id}", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/posts/{post.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "test")

    def test_destroy(self):
        post = JobPosts()
        post.title = 'TestPost'
        post.address = '123 way'
        post.image_url = '123.com'
        post.content = 'heloooooo'
        post.user = self.volunteer_user
        post.save()
        post.cause_area.set([2, 3])
        post.interested_volunteers.set([2, 3])

        response = self.client.delete(f"/posts/{post.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/posts/{post.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)