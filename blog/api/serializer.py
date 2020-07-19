from rest_framework import serializers
from blog.models import Blog, Tag, Blog_Tag


class QueryBlogSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField('get_blog_tags_id')

    def get_blog_tags_id(self, blog):
        blog_tag = Blog_Tag.objects.filter(blog=blog)
        return [i.tag.id for i in blog_tag]

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
            'tags',
        )


class CreateUpdateBlogSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField('get_blog_tags_id')

    def get_blog_tags_id(self, blog):
        blog_tag = Blog_Tag.objects.filter(blog=blog)
        return [i.tag.id for i in blog_tag]

    class Meta:
        model = Blog
        fields = (
            'pk',
            'title',
            'body',
            'tags',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'type')


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Tag
        fields = ('tag', 'blog')
