# main/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # поля, которые будут показаны в списке пользователей
    list_display = (
        'email', 'username', 'profile_type', 'is_staff', 'is_active'
    )
    list_filter = (
        'profile_type', 'is_staff', 'is_active'
    )

    # какие поля отображать в форме редактирования пользователя
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Личные данные', {
            'fields': ('username', 'profile_type')
        }),
        ('Права доступа', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # какие поля будут на форме создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'profile_type',
                'password1', 'password2',
                'is_active', 'is_staff'
            ),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
