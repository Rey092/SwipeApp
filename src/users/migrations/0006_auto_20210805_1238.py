# Generated by Django 3.2.4 on 2021-08-05 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0005_alter_user_username")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="last name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="Phone number"
            ),
        ),
    ]
