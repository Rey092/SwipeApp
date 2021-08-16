# Generated by Django 3.2.4 on 2021-08-15 07:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("estate", "0014_alter_advertisement_expiration"),
    ]

    operations = [
        migrations.AddField(
            model_name="complex",
            name="owner",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="users.user"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="advertisement",
            name="expiration",
            field=models.DateField(
                default=datetime.datetime(2021, 9, 15, 7, 41, 26, 449641)
            ),
        ),
    ]
