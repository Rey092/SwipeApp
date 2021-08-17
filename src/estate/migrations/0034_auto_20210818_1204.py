# Generated by Django 3.2.4 on 2021-08-18 12:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import src.users.services.image_services


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0033_auto_20210817_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 18, 12, 4, 31, 852172)),
        ),
        migrations.AlterField(
            model_name='complexdocument',
            name='file',
            field=models.FileField(upload_to=src.users.services.image_services.UploadToPathAndRename('files/complex/')),
        ),
        migrations.AlterField(
            model_name='complexgalleryimage',
            name='complex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complex_gallery', to='estate.complex'),
        ),
        migrations.AlterField(
            model_name='complexgalleryimage',
            name='image',
            field=models.ImageField(upload_to=src.users.services.image_services.UploadToPathAndRename('images/complex/')),
        ),
    ]
