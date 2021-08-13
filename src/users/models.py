import os

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python as phonenumber_to_python

from config.settings import MEDIA_ROOT
from src.estate.models import (
    Apartment,
    Complex,
    APARTMENT_PURPOSE,
    APARTMENT_FURNISH,
    APARTMENT_PAYMENT,
)
from src.users.services.image_services import UploadToPathAndRename


def validate_international_phonenumber(value):
    phone_number = phonenumber_to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(
            _("Введеный телефонный номер неверен."), code="invalid_phone_number"
        )


class User(AbstractBaseUser, PermissionsMixin):
    """User model with admin-compliant permissions.

    Username, Email and password are required. Other fields are optional.
    """

    # region CHOICES
    upload_path = os.path.join(MEDIA_ROOT, "images", "users", "avatars")
    NOTIFICATION_TYPE = (
        ("Мне", "Мне"),
        ("Мне и агенту", "Мне и агенту"),
        ("Агенту", "Агенту"),
        ("Отключить", "Отключить"),
    )
    # endregion CHOICES

    email = models.EmailField(_("Email"), unique=True)

    is_verified = models.BooleanField(
        _("Статус верификации номера мобильного телефона"),
        default=True,
        help_text=_("Определяет может ли пользователь входить в систему"),
    )
    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    avatar = models.ImageField(
        upload_to=UploadToPathAndRename(upload_path), null=True, blank=True
    )
    is_staff = models.BooleanField(
        _("Статус сотрудника"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Статус пользователя"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_blacklisted = models.BooleanField(
        _("Статус нахождения в черном списке"), default=False
    )
    is_developer = models.BooleanField(
        _("Статус застройщика"),
        default=True,
        help_text=_("Определяет считать ли пользователя Застройщиком. "),
    )
    forward_to_agent = models.BooleanField(
        _("Переключить звонки и сообщения на агента"),
        default=False,
        help_text=_(
            "Определяет необходимо ли переадресовывать звонки и сообщения агенту. "
        ),
    )
    notification_type = models.CharField(
        max_length=12, choices=NOTIFICATION_TYPE, default="Мне"
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    favorite_apartments = models.ManyToManyField(Apartment, blank=True)
    favorite_complex = models.ManyToManyField(Complex, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Contact(models.Model):
    CONTACT_TYPE = (("Отдел продаж", "Отдел продаж"), ("Агент", "Агент"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField()
    email = models.EmailField(_("Email"))


class Notary(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField()
    email = models.EmailField(_("Email"))
    address = models.CharField(max_length=200)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages", blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages", blank=True, null=True)
    text = models.CharField(max_length=4000)
    created = models.DateTimeField(auto_now_add=True)
    is_feedback = models.BooleanField(default=False)


class File(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, "files", "messages")

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to=UploadToPathAndRename(upload_path))


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=None, null=True)
    auto_renewal = models.BooleanField(default=False)


class Filter(models.Model):
    APARTMENT_TYPE = (
        ("Все", "Все"),
        ("Новостройки", "Новостройки"),
        ("Вторичный рынок", "Вторичный рынок"),
        ("Коттеджи", "Коттеджи"),
    )
    name = models.CharField(max_length=30)
    apartment_type = models.CharField(max_length=15, choices=APARTMENT_TYPE)
    district = models.CharField(max_length=200)
    micro_district = models.CharField(max_length=200)

    rooms_count = models.IntegerField(validators=[MinValueValidator(1)])
    price_low = models.PositiveIntegerField()
    price_high = models.PositiveIntegerField()
    area_low = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    area_high = models.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)

    purpose = models.CharField(max_length=22, choices=APARTMENT_PURPOSE)
    payment_options = models.CharField(max_length=9, choices=APARTMENT_PAYMENT)
    furnish = models.CharField(max_length=20, choices=APARTMENT_FURNISH)


class ServiceCenter(models.Model):
    upload_path = os.path.join(MEDIA_ROOT, "images", "service_centers")

    address = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    map_lat = models.DecimalField(max_digits=10, decimal_places=7)
    map_lng = models.DecimalField(max_digits=10, decimal_places=7)
    icon = models.ImageField(upload_to=UploadToPathAndRename(upload_path))
