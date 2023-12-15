from django.db import models

class Favorites(models.Model):
    volunteer = models.ForeignKey('VolunteerUsers', on_delete=models.CASCADE)
    posts = models.ForeignKey('JobPosts', on_delete=models.CASCADE)
