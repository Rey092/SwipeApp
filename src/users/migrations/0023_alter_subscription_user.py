# Generated by Django 3.2.4 on 2021-08-15 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0022_auto_20210815_0821"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscription",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
