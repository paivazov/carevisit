from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from applications.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('profile_type',)
    list_filter = BaseUserAdmin.list_filter + ('profile_type',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('profile_type',)}),
    )
