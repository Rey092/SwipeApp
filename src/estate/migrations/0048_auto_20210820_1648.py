# Generated by Django 3.2.4 on 2021-08-20 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0047_alter_advertisement_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
