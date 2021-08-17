# Generated by Django 3.2.4 on 2021-08-22 04:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0050_remove_apartment_is_reviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='price_per_square_meter',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='area',
            field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
