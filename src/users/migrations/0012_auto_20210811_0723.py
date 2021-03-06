# Generated by Django 3.2.4 on 2021-08-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estate", "0006_alter_advertisement_expiration"),
        ("users", "0011_alter_message_recipient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="favorite_apartments",
            field=models.ManyToManyField(null=True, to="estate.Apartment"),
        ),
        migrations.AlterField(
            model_name="user",
            name="favorite_complex",
            field=models.ManyToManyField(null=True, to="estate.Complex"),
        ),
    ]
