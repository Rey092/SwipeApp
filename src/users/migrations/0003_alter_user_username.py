# Generated by Django 3.2.4 on 2021-08-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0002_rename_phone_user_username")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=150, verbose_name="phone"),
        )
    ]