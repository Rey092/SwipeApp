# Generated by Django 3.2.4 on 2021-08-05 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.RenameField(model_name="user", old_name="phone", new_name="username")
    ]