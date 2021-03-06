# Generated by Django 3.2.4 on 2021-08-16 15:51

from django.db import migrations, models
import src.users.services.image_services


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notary',
            name='avatar',
            field=models.ImageField(default=1, upload_to=src.users.services.image_services.UploadToPathAndRename('images/service_centers/')),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servicecenter',
            name='icon',
            field=models.ImageField(upload_to=src.users.services.image_services.UploadToPathAndRename('images/service_centers/')),
        ),
    ]
