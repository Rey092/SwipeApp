# Generated by Django 3.2.4 on 2021-08-17 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0029_auto_20210817_0900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complex',
            name='contact',
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 17, 9, 8, 58, 23349)),
        ),
    ]