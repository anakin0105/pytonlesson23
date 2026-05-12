from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Улучшенная админка для CustomUser"""

    list_display = ('email', 'username', 'phone_number', 'country',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined')

    list_filter = ('is_active', 'is_staff', 'is_superuser', 'country')
    search_fields = ('email', 'username', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {
            'fields': ('username', 'avatar', 'phone_number', 'country')
        }),
        ('Права и статус', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'country', 'password1', 'password2'),
        }),
    )

    ordering = ('-date_joined',)