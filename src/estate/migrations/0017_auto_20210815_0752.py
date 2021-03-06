# Generated by Django 3.2.4 on 2021-08-15 07:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0021_alter_contact_user"),
        ("estate", "0016_alter_advertisement_expiration"),
    ]

    operations = [
        migrations.AddField(
            model_name="complex",
            name="contact",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="users.contact",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="advertisement",
            name="expiration",
            field=models.DateField(
                default=datetime.datetime(2021, 9, 15, 7, 52, 18, 200529)
            ),
        ),
    ]
