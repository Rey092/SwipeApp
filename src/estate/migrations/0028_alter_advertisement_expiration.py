# Generated by Django 3.2.4 on 2021-08-17 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0027_auto_20210816_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 17, 8, 55, 13, 484373)),
        ),
    ]
