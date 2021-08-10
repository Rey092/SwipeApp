# Generated by Django 3.2.4 on 2021-08-10 09:25

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import src.users.services.image_services


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Apartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=50)),
                ("map_lat", models.DecimalField(decimal_places=2, max_digits=5)),
                ("map_lng", models.DecimalField(decimal_places=2, max_digits=5)),
                ("moderation_status", models.CharField(max_length=50)),
                ("is_reviewed", models.BooleanField(default=False)),
                ("foundation", models.CharField(max_length=50)),
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("Квартира в новострое", "Квартира в новострое"),
                            ("Вторичная недвижимость", "Квартира в новострое"),
                            ("Складское помещение", "Складское помещение"),
                            ("Частный дом", "Частный дом"),
                            ("Офис", "Офис"),
                        ],
                        default="Квартира в новострое",
                        max_length=50,
                    ),
                ),
                (
                    "rooms",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("layout", models.CharField(max_length=50)),
                ("furnish", models.CharField(max_length=50)),
                ("area", models.DecimalField(decimal_places=2, max_digits=7)),
                ("kitchen_area", models.DecimalField(decimal_places=2, max_digits=7)),
                ("has_balcony", models.BooleanField()),
                ("heating_type", models.CharField(max_length=50)),
                ("payment_options", models.CharField(max_length=50)),
                ("commission", models.IntegerField()),
                ("communication_type", models.CharField(max_length=50)),
                ("price", models.PositiveIntegerField()),
                ("description", models.CharField(max_length=50)),
                ("for_sale", models.BooleanField()),
                (
                    "schema",
                    models.ImageField(
                        upload_to=src.users.services.image_services.UploadToPathAndRename(
                            "/home/roman/GitHub/SwipeApp/media/images/apartment/schema"
                        )
                    ),
                ),
                (
                    "floor_schema",
                    models.ImageField(
                        upload_to=src.users.services.image_services.UploadToPathAndRename(
                            "/home/roman/GitHub/SwipeApp/media/images/apartment/floor_schema"
                        )
                    ),
                ),
                ("created_date", models.DateField()),
                ("number", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Complex",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("address", models.CharField(max_length=50)),
                ("map_lat", models.DecimalField(decimal_places=7, max_digits=10)),
                ("map_lng", models.DecimalField(decimal_places=7, max_digits=10)),
                ("is_commissioned", models.BooleanField(default=False)),
                ("commission_date", models.DateField()),
                ("created_date", models.DateField(auto_now_add=True)),
                ("description", models.CharField(max_length=2000)),
                (
                    "complex_status",
                    models.CharField(
                        choices=[("Квартиры", "Квартиры"), ("Офисы", "Офисы")],
                        default="Квартиры",
                        max_length=10,
                    ),
                ),
                (
                    "complex_type",
                    models.CharField(
                        choices=[
                            ("Многоквартирный", "Многоквартирный"),
                            ("Частный", "Частный"),
                        ],
                        default="Квартиры",
                        max_length=15,
                    ),
                ),
                (
                    "complex_class",
                    models.CharField(
                        choices=[("Элитный", "Элитный"), ("Бюджетный", "Бюджетный")],
                        default="Элитный",
                        max_length=9,
                    ),
                ),
                (
                    "technology",
                    models.CharField(
                        choices=[
                            (
                                "Монолитный каркас с керамзитно-блочным заполнением",
                                "Монолитный каркас с керамзитно-блочным заполнением",
                            ),
                            ("Кирпич", "Кирпич"),
                        ],
                        default="Кирпич",
                        max_length=50,
                    ),
                ),
                (
                    "territory",
                    models.CharField(
                        choices=[("Закрытая", "Закрытая"), ("Открытая", "Открытая")],
                        default="Закрытая",
                        max_length=8,
                    ),
                ),
                ("distance_to_sea", models.IntegerField()),
                (
                    "invoice",
                    models.CharField(
                        choices=[("Платежи", "Платежи"), ("Автоплатеж", "Автоплатеж")],
                        default="Платежи",
                        max_length=10,
                    ),
                ),
                ("ceiling_height", models.DecimalField(decimal_places=1, max_digits=3)),
                ("gas", models.BooleanField(default=True)),
                (
                    "heating",
                    models.CharField(
                        choices=[("Центральное", "Центральное"), ("Личное", "Личное")],
                        default="Центральное",
                        max_length=11,
                    ),
                ),
                (
                    "electricity",
                    models.CharField(
                        choices=[
                            ("Подключено", "Подключено"),
                            ("Генератор", "Генератор"),
                            ("Отсутствует", "Отсутствует"),
                        ],
                        default="Подключено",
                        max_length=11,
                    ),
                ),
                (
                    "sewerage",
                    models.CharField(
                        choices=[
                            ("Центральная", "Центральная"),
                            ("Отсутствует", "Отсутствует"),
                        ],
                        default="Центральная",
                        max_length=11,
                    ),
                ),
                (
                    "water_supply",
                    models.CharField(
                        choices=[
                            ("Центральное", "Центральное"),
                            ("Отсутствует", "Отсутствует"),
                        ],
                        default="Центральное",
                        max_length=11,
                    ),
                ),
                ("formalization", models.CharField(max_length=50)),
                ("payment_options", models.CharField(max_length=50)),
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("Жилое помещение", "Жилое помещение"),
                            ("Склад", "Склад"),
                        ],
                        default="Жилое помещение",
                        max_length=15,
                    ),
                ),
                ("payment_part", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Corpus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("commissioned_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("floor_count", models.IntegerField()),
                (
                    "corpus",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.corpus"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Riser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.section"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Floor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.section"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplexNews",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                ("title", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=50)),
                (
                    "complex",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.complex"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplexGalleryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=src.users.services.image_services.UploadToPathAndRename(
                            "/home/roman/GitHub/SwipeApp/media/images/complex"
                        )
                    ),
                ),
                (
                    "complex",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.complex"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplexDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "file",
                    models.FileField(
                        upload_to=src.users.services.image_services.UploadToPathAndRename(
                            "/home/roman/GitHub/SwipeApp/media/files/complex"
                        )
                    ),
                ),
                (
                    "complex",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.complex"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ComplexBenefits",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("playground", models.BooleanField(default=False)),
                ("school", models.BooleanField(default=False)),
                ("nursery_school", models.BooleanField(default=False)),
                ("parking", models.BooleanField(default=False)),
                (
                    "complex",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.complex"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Complaint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=2000)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("is_reviewed", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="estate.section"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ApartmentGalleryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=src.users.services.image_services.UploadToPathAndRename(
                            "/home/roman/GitHub/SwipeApp/media/images/apartment/gallery"
                        )
                    ),
                ),
                (
                    "apartment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estate.apartment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="apartment",
            name="complex",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="estate.complex"
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="corpus",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="estate.corpus"
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="floor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="estate.floor"
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="riser",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="estate.riser"
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="estate.section"
            ),
        ),
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("add_text", models.BooleanField(default=False)),
                (
                    "text",
                    models.CharField(
                        choices=[
                            ("Подарок при покупке", "Подарок при покупке"),
                            ("Возможен торг", "Возможен торг"),
                            ("Квартира у моря", "Квартира у моря"),
                            ("В спальном районе", "В спальном районе"),
                            ("Вам повезло с ценой!", "Вам повезло с ценой!"),
                            ("Для большой семьи", "Для большой семьи"),
                            ("Семейное гнездышко", "Семейное гнездышко"),
                            ("Отдельная парковка", "Отдельная парковка"),
                        ],
                        max_length=50,
                    ),
                ),
                ("add_color", models.BooleanField(default=False)),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("Розовый", "FFC0CB"),
                            ("Зеленый", "008000"),
                            ("Синий", "0000FF"),
                        ],
                        max_length=50,
                    ),
                ),
                ("is_big", models.BooleanField(default=False)),
                ("is_raisable", models.BooleanField(default=False)),
                ("is_turbo", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "expiration",
                    models.DateField(
                        default=datetime.datetime(2021, 9, 10, 9, 25, 26, 376253)
                    ),
                ),
                ("auto_renewal", models.BooleanField(default=False)),
                (
                    "apartment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estate.apartment",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="apartment",
            unique_together={("number", "corpus")},
        ),
    ]