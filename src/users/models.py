import os

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.phonenumber import to_python as phonenumber_to_python

from config.settings import MEDIA_ROOT
from src.users.services.image_services import UploadToPathAndRename


def validate_international_phonenumber(value):
    phone_number = phonenumber_to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(
            _("Введеный телефонный номер неверен."), code="invalid_phone_number"
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Phone, First_name, Last_name and password are required. Other fields are optional.
    """

    upload_path = os.path.join(MEDIA_ROOT, "images", "users", "avatars")
    NOTIFICATION_TYPE = (
        ("Мне", "Мне"),
        ("Мне и агенту", "Мне и агенту"),
        ("Агенту", "Агенту"),
        ("Отключить", "Отключить"),
    )

    username = models.CharField(
        _("Номер телефона"),
        max_length=150,
        unique=True,
        validators=[validate_international_phonenumber],
    )
    is_verified = models.BooleanField(
        _("Статус верификации номера мобильного телефона"),
        default=True,
        help_text=_("Определяет может ли пользователь входить в систему"),
    )

    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    email = models.EmailField(_("Email"), unique=True)
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

    # favorite_apartments = ManyToManyField(Appartment, related_name)
    # favorite_complex - ManyToManyField(Complex, related_name)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


# Contact PK id user - ForeignKey(User) сontact_type - choice first_name - CharField last_name - CharField phone - PhoneNumber email - EmailField Notary PK id first_name - CharField last_name - CharField phone - PhoneNumber email - EmailField address - CharField Message PK id FK sender - ForeignKey(User) FK recepient - ForeignKey(User) text - CharField created - DateTimeField is_feedback - Boolean File PK id message - ForeignKey file - FileField Subscription PK id OTO user - OneToOne(User) is_active - Boolean created - DateTimeField expiration - DateField auto-renewal - Boolean 1 1..2 Filter PK id name - CharField appartment_type - choices district - CharField microdistrict - CharField rooms_count - IntegerField price_low - Int price_high - Int area_low - Decimal area_high - Decimal purpose - choices payment_options - choices furnish -choices ServiceCenter PK id address - CharField name - CharField map_lat - DecimalField map_lng - DecimalField icon - ImgField Users
