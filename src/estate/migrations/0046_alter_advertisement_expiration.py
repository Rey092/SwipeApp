# Generated by Django 3.2.4 on 2021-08-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0045_auto_20210820_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(blank=True),
        ),
    ]
