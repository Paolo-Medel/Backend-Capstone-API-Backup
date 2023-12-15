from django.db import models

class InterestedVolunteers(models.Model):
    user = models.ForeignKey('VolunteerUsers', on_delete=models.CASCADE)
    posts = models.ForeignKey('JobPosts', on_delete=models.CASCADE)
