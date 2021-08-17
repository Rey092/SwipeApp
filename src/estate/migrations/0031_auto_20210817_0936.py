# Generated by Django 3.2.4 on 2021-08-17 09:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0030_auto_20210817_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 17, 9, 36, 50, 872192)),
        ),
        migrations.AlterField(
            model_name='complex',
            name='ceiling_height',
            field=models.DecimalField(decimal_places=1, default=1.5, max_digits=3),
        ),
        migrations.AlterField(
            model_name='complex',
            name='map_lat',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='complex',
            name='map_lng',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
    ]