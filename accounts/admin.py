# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    # Define list_display with fields that are part of the CustomUser model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    # Define list_filter with fields that are part of the CustomUser model
    list_filter = ('is_staff', 'is_active')
    # Remove groups and user_permissions from filter_horizontal
    filter_horizontal = ()
    # Define fieldsets to organize the form in the admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'phone_numbers', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Define add_fieldsets to organize the form for adding users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_numbers', 'address', 'profile_picture', 'password1', 'password2'),
        }),
    )
    # Define search_fields to enable search functionality
    search_fields = ('username', 'email')
    # Define ordering of the users
    ordering = ('username',)

admin.site.register(CustomUser, UserAdmin)

