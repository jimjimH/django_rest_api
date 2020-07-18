from rest_framework import serializers
from blog.models import Blog, Tag, Blog_Tag


class QueryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'pk',
            'title',
            'body',
            'pub_time',
            'created_at',
            'updated_at',
            'user_id',
        )


class CreateUpdateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'title',
            'body',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'type')


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Tag
        fields = ('tag', 'blog')
