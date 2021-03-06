# Generated by Django 3.2.4 on 2021-08-17 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0030_auto_20210817_0908'),
        ('users', '0028_auto_20210816_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='complex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complex_contact', to='estate.complex'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
