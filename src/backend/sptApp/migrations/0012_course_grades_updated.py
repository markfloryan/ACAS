# Generated by Django 3.1.5 on 2021-02-25 17:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sptApp', '0011_studenttocourse_lettergrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grades_updated',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]