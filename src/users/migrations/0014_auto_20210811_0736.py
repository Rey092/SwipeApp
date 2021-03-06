# Generated by Django 3.2.4 on 2021-08-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estate", "0008_alter_advertisement_expiration"),
        ("users", "0013_auto_20210811_0724"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="favorite_apartments",
            field=models.ManyToManyField(blank=True, to="estate.Apartment"),
        ),
        migrations.AlterField(
            model_name="user",
            name="favorite_complex",
            field=models.ManyToManyField(blank=True, to="estate.Complex"),
        ),
    ]
