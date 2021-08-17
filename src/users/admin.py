from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

# from src.users.forms import UserChangeForm, UserCreationForm
from src.users.models import Message, File, Contact

User = get_user_model()


# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (Message
#         (None, {"fields": ("username", "password")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                     "avatar",
#                 )
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     list_display = ["email", "username", "is_superuser"]
#     search_fields = ["username"]
#

admin.site.register(User)
admin.site.register(Message)
admin.site.register(File)
admin.site.register(Contact)
