from django.db import models

class CauseAreas(models.Model):
    label = models.CharField(max_length=64)
