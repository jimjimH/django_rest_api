from django.contrib import admin
from .models import (
    Tag,
    Blog,
    Blog_Tag,
)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
    ]


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title',
        'body',
        'pub_time',
        'created_at',
        'updated_at',
        'user',
    ]

class BlogTagAdmin(admin.ModelAdmin):
    list_display = [
        'tag',
        'blog',
        'created_at',
    ]

admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Blog_Tag, BlogTagAdmin)
