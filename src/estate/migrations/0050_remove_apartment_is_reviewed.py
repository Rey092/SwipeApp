# Generated by Django 3.2.4 on 2021-08-21 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0049_auto_20210821_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='is_reviewed',
        ),
    ]
