# Generated by Django 5.0 on 2023-12-15 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteerapi', '0004_remove_volunteerusers_volunteer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposts',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
