# Generated by Django 5.0 on 2023-12-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteerapi', '0002_jobposts_interestvolunteers_favorites_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InterestVolunteers',
            new_name='InterestedVolunteers',
        ),
        migrations.AddField(
            model_name='jobposts',
            name='cause_area',
            field=models.ManyToManyField(related_name='posts', through='volunteerapi.PostCause', to='volunteerapi.causeareas'),
        ),
        migrations.AddField(
            model_name='jobposts',
            name='interested_volunteers',
            field=models.ManyToManyField(related_name='posts', through='volunteerapi.InterestedVolunteers', to='volunteerapi.volunteerusers'),
        ),
    ]