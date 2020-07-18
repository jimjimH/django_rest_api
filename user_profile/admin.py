from django.contrib import admin
from .models import (
    Profile
)
from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display = (
    'pk',
    'username',
    'email',
    'first_name',
    'last_name',
    'last_login',
    'date_joined',
    'is_active',
)

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'age',
        'gender',
        'phone',
        'user_id',
    ]

admin.site.register(Profile, ProfileAdmin)
