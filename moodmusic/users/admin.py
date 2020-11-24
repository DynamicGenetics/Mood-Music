from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from moodmusic.users.forms import UserChangeForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    fieldsets = (("User", {"fields": ("email",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["email", "is_superuser", "consent_granted", "phone_verified"]
    search_fields = ["email"]
