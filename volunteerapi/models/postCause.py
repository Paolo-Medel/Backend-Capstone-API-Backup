from django.db import models

class PostCause(models.Model):
    cause = models.ForeignKey('CauseAreas', on_delete=models.CASCADE)
    posts = models.ForeignKey('JobPosts', on_delete=models.CASCADE)
