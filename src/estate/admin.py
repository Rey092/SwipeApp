from django.contrib import admin

from src.estate.models import Advertisement, Complex
from src.users.models import Contact

admin.site.register(Advertisement)
admin.site.register(Complex)
