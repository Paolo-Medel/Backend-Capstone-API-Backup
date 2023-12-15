from django.db import models

class JobPosts(models.Model):
    title = models.CharField(max_length=250)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    approved = models.BooleanField(default=True)
    user = models.ForeignKey("VolunteerUsers", on_delete=models.CASCADE)
    content = models.CharField(max_length=3000)
    address = models.CharField(max_length=3000)
    cause_area = models.ManyToManyField('CauseAreas', through='PostCause', related_name='posts')
    interested_volunteers = models.ManyToManyField('VolunteerUsers', through='InterestedVolunteers', related_name='posts')
