# Generated by Django 3.2.4 on 2021-08-11 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estate", "0005_alter_advertisement_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="advertisement",
            name="expiration",
            field=models.DateField(
                default=datetime.datetime(2021, 9, 11, 7, 23, 15, 494100)
            ),
        ),
    ]
