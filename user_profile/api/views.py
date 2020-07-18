from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from user_profile.models import Profile
from user_profile.api.serializers import ProfileSerializer, UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def api_detail_user_view(request, id):
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile)
        message = {
            'user': user_serializer.data,
            'profile': profile_serializer.data
        }
        return Response(message)


@permission_classes((IsAuthenticated,))
@api_view(['PUT'])
def api_update_user_view(request, id):
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    authenticated_user = request.user
    if user != authenticated_user:
        return Response({'Response': "You don't have permission to edit it."})

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=data)
        profile_serializer = ProfileSerializer(profile, data=data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            if data['password']:
                user.set_password(data.get('password'))
                user.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "update successful"}, status=status.HTTP_202_ACCEPTED)


@permission_classes((IsAuthenticated,))
@api_view(['DELETE'])
def api_delete_user_view(request, id):
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    authenticated_user = request.user
    if user != authenticated_user:
        return Response({'Response': "You don't have permission to delete it."})

    if request.method == 'DELETE':
        operation = user.delete()  # 刪除user會一併刪除profile
        if operation:
            return Response({"success": "delete successful"})
        else:
            return Response({"failure": "delete failed"})


@permission_classes((AllowAny,))
@api_view(['POST'])
def api_create_user_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # 先存user
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            new_user = user_serializer.save()
            new_user.set_password(data.get('password'))
            new_user.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 再存profile
        if new_user is not None:
            profile = Profile(user=new_user)
            profile_serializer = ProfileSerializer(data=data, instance=profile)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                new_user.delete()  # 驗證失敗時，把已經儲存的user刪掉
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = Token.objects.get(user=new_user).key
        message = {
            'user': user_serializer.data,
            'profile': profile_serializer.data,
            'token': token
        }
        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def obtain_auth_token(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
        if user is not None:
            token = Token.objects.get(user=user).key
            return Response({"token": token})
        else:
            return Response({"failure": "login failed, wrong username or password"}, status=status.HTTP_400_BAD_REQUEST)
