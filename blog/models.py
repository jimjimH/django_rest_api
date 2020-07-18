from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    TAG_TYPE_CHOICE = [
        ('food', '美食'),
        ('wearing', '衣服'),
    ]
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=TAG_TYPE_CHOICE)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100, blank=True, null=False)
    body = models.TextField(max_length=5000, blank=True, null=False)
    pub_time = models.DateTimeField(
        auto_now=True, verbose_name="published date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {str(self.user.username)}'


class Blog_Tag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tag.name} - {str(self.blog.title)}'
