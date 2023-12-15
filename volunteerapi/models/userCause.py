from django.db import models

class UserCause(models.Model):
    user = models.ForeignKey('VolunteerUsers', on_delete=models.CASCADE)
    cause_area = models.ForeignKey('CauseAreas', on_delete=models.CASCADE)
