# Generated by Django 3.2.4 on 2021-08-15 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estate", "0018_alter_advertisement_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="expiration",
            field=models.DateField(
                default=datetime.datetime(2021, 9, 15, 8, 21, 38, 390120)
            ),
        ),
    ]
