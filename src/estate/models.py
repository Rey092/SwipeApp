import os
from datetime import datetime, timedelta

from django.core.validators import MinValueValidator
from django.db import models

from django.conf import settings
from config.settings import MEDIA_ROOT
from src.users.services.image_services import UploadToPathAndRename

User = settings.AUTH_USER_MODEL


class Complex(models.Model):
    """The Complex model."""

    # region CHOICES
    COMPLEX_STATUS = (
        ("Квартиры", "Квартиры"),
        ("Офисы", "Офисы"),
    )
    COMPLEX_TYPE = (
        ("Многоквартирный", "Многоквартирный"),
        ("Частный", "Частный"),
    )
    COMPLEX_CLASS = (("Элитный", "Элитный"), ("Бюджетный", "Бюджетный"))
    COMPLEX_TECHNOLOGY = (
        (
            "Монолитный каркас с керамзитно-блочным заполнением",
            "Монолитный каркас с керамзитно-блочным заполнением",
        ),
        ("Кирпич", "Кирпич"),
    )
    COMPLEX_TERRITORY = (("Закрытая", "Закрытая"), ("Открытая", "Открытая"))
    COMPLEX_INVOICES = (("Платежи", "Платежи"), ("Автоплатеж", "Автоплатеж"))
    COMPLEX_HEATING = (("Центральное", "Центральное"), ("Личное", "Личное"))
    COMPLEX_ELECTRICITY = (
        ("Подключено", "Подключено"),
        ("Генератор", "Генератор"),
        ("Отсутствует", "Отсутствует"),
    )
    COMPLEX_SEWERAGE = (("Центральная", "Центральная"), ("Отсутствует", "Отсутствует"))
    COMPLEX_WATER = (("Центральное", "Центральное"), ("Отсутствует", "Отсутствует"))
    COMPLEX_PURPOSE = (
        ("Жилое помещение", "Жилое помещение"),
        ("Склад", "Склад"),
    )
    # endregion CHOICES

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complexes")

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    map_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    map_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    is_commissioned = models.BooleanField(default=False)
    commission_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=2000)

    complex_status = models.CharField(
        max_length=10, choices=COMPLEX_STATUS, default="Квартиры"
    )
    complex_type = models.CharField(
        max_length=15, choices=COMPLEX_TYPE, default="Квартиры"
    )
    complex_class = models.CharField(
        max_length=9, choices=COMPLEX_CLASS, default="Элитный"
    )
    technology = models.CharField(
        max_length=50, choices=COMPLEX_TECHNOLOGY, default="Кирпич"
    )
    territory = models.CharField(
        max_length=8, choices=COMPLEX_TERRITORY, default="Закрытая"
    )

    distance_to_sea = models.IntegerField()
    invoice = models.CharField(
        max_length=10, choices=COMPLEX_INVOICES, default="Платежи"
    )
    ceiling_height = models.DecimalField(max_digits=3, decimal_places=1, default=1.5)

    gas = models.BooleanField(default=True)
    heating = models.CharField(
        max_length=11, choices=COMPLEX_HEATING, default="Центральное"
    )
    electricity = models.CharField(
        max_length=11, choices=COMPLEX_ELECTRICITY, default="Подключено"
    )
    sewerage = models.CharField(
        max_length=11, choices=COMPLEX_SEWERAGE, default="Центральная"
    )
    water_supply = models.CharField(
        max_length=11, choices=COMPLEX_WATER, default="Центральное"
    )

    formalization = models.CharField(max_length=50)
    payment_options = models.CharField(max_length=50)
    purpose = models.CharField(
        max_length=15, choices=COMPLEX_PURPOSE, default="Жилое помещение"
    )
    payment_part = models.CharField(max_length=50)


# region APARTMENT_CHOICES
APARTMENT_PURPOSE = (
    ("Квартира в новострое", "Квартира в новострое"),
    ("Вторичная недвижимость", "Квартира в новострое"),
    ("Складское помещение", "Складское помещение"),
    ("Частный дом", "Частный дом"),
    ("Офис", "Офис"),
)
APARTMENT_FURNISH = (
    ("Черновая отделка", "Черновая отделка"),
    ("Евроремонт", "Евроремонт"),
    ("Ремонт от строителей", "Ремонт от строителей"),
)
APARTMENT_PAYMENT = (
    ("Ипотека", "Ипотека"),
    ("Кредит", "Кредит"),
    ("Рассрочка", "Рассрочка"),
    ("Покупка", "Покупка"),
)

# endregion APARTMENT_CHOICES


class Apartment(models.Model):
    upload_path_schema = "images/apartment/schema/"
    upload_path_floor_schema = "images/apartment/floor_schema/"

    address = models.CharField(max_length=50)
    map_lat = models.DecimalField(max_digits=5, decimal_places=2)
    map_lng = models.DecimalField(max_digits=5, decimal_places=2)

    moderation_status = models.CharField(max_length=50)
    is_reviewed = models.BooleanField(default=False)
    foundation = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50, choices=APARTMENT_PURPOSE, default="Квартира в новострое")
    rooms = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    layout = models.CharField(max_length=50)
    furnish = models.CharField(max_length=20, choices=APARTMENT_FURNISH)
    area = models.DecimalField(max_digits=7, decimal_places=2)
    kitchen_area = models.DecimalField(max_digits=7, decimal_places=2)
    has_balcony = models.BooleanField()
    heating_type = models.CharField(max_length=50)

    payment_options = models.CharField(max_length=50, choices=APARTMENT_PAYMENT)
    commission = models.IntegerField()
    communication_type = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    description = models.CharField(max_length=50)
    for_sale = models.BooleanField()
    schema = models.ImageField(upload_to=UploadToPathAndRename(upload_path_schema))
    floor_schema = models.ImageField(
        upload_to=UploadToPathAndRename(upload_path_floor_schema)
    )
    created_date = models.DateField()

    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    corpus = models.IntegerField(validators=[MinValueValidator(1)])
    section = models.IntegerField(validators=[MinValueValidator(1)])
    floor = models.IntegerField(validators=[MinValueValidator(1)])
    riser = models.IntegerField(validators=[MinValueValidator(1)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = [["number", "corpus"]]

    @property
    def get_price_per_square_meter(self):
        return 0


class ComplexGalleryImage(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, "images", "complex")

    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=UploadToPathAndRename(upload_path))


class ComplexNews(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)


class ComplexDocument(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, "files", "complex")

    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=UploadToPathAndRename(upload_path))

    @property
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension


class ApartmentGalleryImage(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, "images", "apartment", "gallery")

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=UploadToPathAndRename(upload_path))


class ComplexBenefits(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    playground = models.BooleanField(default=False)
    school = models.BooleanField(default=False)
    nursery_school = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)


class Advertisement(models.Model):
    # region CHOICES
    ADVERTISEMENT_TEXT = (
        ("Подарок при покупке", "Подарок при покупке"),
        ("Возможен торг", "Возможен торг"),
        ("Квартира у моря", "Квартира у моря"),
        ("В спальном районе", "В спальном районе"),
        ("Вам повезло с ценой!", "Вам повезло с ценой!"),
        ("Для большой семьи", "Для большой семьи"),
        ("Семейное гнездышко", "Семейное гнездышко"),
        ("Отдельная парковка", "Отдельная парковка"),
    )
    ADVERTISEMENT_COLOR = (
        ("Розовый", "FFC0CB"),
        ("Зеленый", "008000"),
        ("Синий", "0000FF"),
    )
    # endregion CHOICES

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    add_text = models.BooleanField(default=False)
    text = models.CharField(max_length=50, choices=ADVERTISEMENT_TEXT)
    add_color = models.BooleanField(default=False)
    color = models.CharField(max_length=50, choices=ADVERTISEMENT_COLOR)
    is_big = models.BooleanField(default=False)
    is_raisable = models.BooleanField(default=False)
    is_turbo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration = models.DateField(default=datetime.now() + timedelta(days=31))
    auto_renewal = models.BooleanField(default=False)


class Complaint(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
