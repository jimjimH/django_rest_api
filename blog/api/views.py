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
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from datetime import datetime, timedelta


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def api_detail_blog_view(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = {}

    if request.method == 'GET':
        blog_serializer = QueryBlogSerializer(blog)
        message['blog'] = blog_serializer.data
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


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def api_lastet_blog_view(request):
    try:
        blog = Blog.objects.filter(
            created_at__gte=datetime.now()-timedelta(days=1))
    except Blog.DoesNotExist:
        return Response({'Response': "No latest blogs."}, status=status.HTTP_404_NOT_FOUND)

    message = {}

    if request.method == 'GET':
        blog_serializer = QueryBlogSerializer(blog, many=True)
        message['blog'] = blog_serializer.data
        return Response(message)


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def api_tag_blog_view(request, tag_id):
    try:
        blog = Blog.objects.filter(blog_tag__tag_id=tag_id)
    except Blog.DoesNotExist:
        return Response({'Response': "No latest blogs."}, status=status.HTTP_404_NOT_FOUND)

    message = {}

    if request.method == 'GET':
        blog_serializer = QueryBlogSerializer(blog, many=True)
        message['blog'] = blog_serializer.data
        return Response(message)


class api_search_blog_view(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = QueryBlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title',)
