# Generated by Django 3.2.7 on 2022-03-16 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sptApp', '0016_section_studenttosection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='published',
        ),
    ]
