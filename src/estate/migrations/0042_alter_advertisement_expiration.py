# Generated by Django 3.2.4 on 2021-08-20 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0041_auto_20210820_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 20, 9, 52, 44, 831765)),
        ),
    ]
