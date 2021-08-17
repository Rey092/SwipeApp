# Generated by Django 3.2.4 on 2021-08-22 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0052_apartment_is_booked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='complex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complex_apartments', to='estate.complex'),
        ),
    ]
