# Generated by Django 3.2.4 on 2021-08-20 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0044_auto_20210820_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 20, 16, 18, 57, 423210)),
        ),
    ]
