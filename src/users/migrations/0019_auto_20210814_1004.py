# Generated by Django 3.2.4 on 2021-08-14 10:04

from django.db import migrations, models
import django.db.models.deletion
import src.users.services.image_services


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_remove_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(
                upload_to=src.users.services.image_services.UploadToPathAndRename(
                    "media/files/messages/"
                )
            ),
        ),
        migrations.AlterField(
            model_name="file",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="message_files",
                to="users.message",
            ),
        ),
    ]
