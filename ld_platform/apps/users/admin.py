from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ld_platform.apps.users.forms import UserChangeForm, UserCreationForm
from ld_platform.apps.users.models import UserExchangeSetting

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "first_name", "last_name", "is_superuser"]
    search_fields = ["email"]


@admin.register(UserExchangeSetting)
class UserExchangeSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "exchange_name", "user", "api_key", "api_secret"]
    search_fields = ["id", "exchange_name", "user", "api_key", "api_secret"]
