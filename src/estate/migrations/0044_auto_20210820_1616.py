# Generated by Django 3.2.4 on 2021-08-20 16:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
import src.users.services.image_services


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0043_alter_advertisement_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='apartment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='estate.apartment'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 20, 16, 16, 48, 934573)),
        ),
        migrations.AlterField(
            model_name='apartmentgalleryimage',
            name='image',
            field=models.ImageField(upload_to=src.users.services.image_services.UploadToPathAndRename('images/apartment/gallery/')),
        ),
    ]
