from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from blog.models import Blog, Tag, Blog_Tag
from blog.api.serializer import (
    QueryBlogSerializer,
    CreateUpdateBlogSerializer,
    TagSerializer,
    BlogTagSerializer,
)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def api_detail_blog_view(request, id):
    try:
        blog = Blog.objects.get(pk=id)
        blog_tag = Blog_Tag.objects.filter(blog=blog)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = {}

    if request.method == 'GET':
        blog_serializer = QueryBlogSerializer(blog)
        message['blog'] = blog_serializer.data
        message['blog']['tags'] = [i.tag.id for i in blog_tag]
        return Response(message)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])
def api_update_blog_view(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    authenticated_user = request.user
    if blog.user != authenticated_user:
        return Response({'Response': "You don't have permission to edit it."})

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        blog_serializer = CreateUpdateBlogSerializer(blog, data=data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response({"success": "update successful"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
@api_view(['DELETE'])
def api_delete_blog_view(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    authenticated_user = request.user
    if blog.user != authenticated_user:
        return Response({'Response': "You don't have permission to delete it."})

    if request.method == 'DELETE':
        operation = blog.delete()  # 刪除blog會一併刪除blog_tags
        if operation:
            return Response({"success": "delete successful"})
        else:
            return Response({"failure": "delete failed"})


@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def api_create_blog_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        blog = Blog(user=request.user)
        blog_serializer = CreateUpdateBlogSerializer(data=data, instance=blog)
        if blog_serializer.is_valid():
            new_blog = blog_serializer.save()
        else:
            return Response(blog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = {
            'user': blog_serializer.data,
        }
        return Response(message, status=status.HTTP_201_CREATED)
