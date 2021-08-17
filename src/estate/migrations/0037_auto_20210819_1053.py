# Generated by Django 3.2.4 on 2021-08-19 10:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0036_alter_advertisement_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2021, 9, 19, 10, 53, 33, 139013)),
        ),
        migrations.AlterField(
            model_name='complexbenefits',
            name='complex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complex_benefits', to='estate.complex'),
        ),
    ]
