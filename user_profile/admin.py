from django.contrib import admin
from .models import (
    Profile
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
