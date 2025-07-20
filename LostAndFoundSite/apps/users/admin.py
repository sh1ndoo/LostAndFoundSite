from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fields = ('phone_number', 'first_name', 'is_staff', 'is_active', 'is_superuser', 'vk', 'telegram', 'avatar', 'last_login')
    fieldsets = ()
    list_display = ('phone_number', 'first_name', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('phone_number', 'first_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('phone_number',)
    readonly_fields = ('last_login',)