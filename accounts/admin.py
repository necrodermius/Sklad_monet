from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import BonusTransaction
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


User = get_user_model()

@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'bonuses')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {
            'fields': ('email', 'password'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone_number'),
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
        ('Bonuses', {
            'fields': ('bonuses',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'password1',
                'password2',
            ),
        }),
    )

@admin.register(BonusTransaction)
class BonusTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_amount', 'bonus_awarded', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)