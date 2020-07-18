from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from user_profile.models import Profile
from user_profile.api.seriaiizers import ProfileSerializer, UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token


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


@api_view(['PUT'])
def api_update_user_view(request, id):
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=data)
        profile_serializer = ProfileSerializer(profile, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "update successful"}, status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE'])
def api_delete_user_view(request, id):
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = user.delete()  # 會一併刪除profile
        if operation:
            return Response({"success": "delete successful"})
        else:
            return Response({"failure": "delete failed"})


@api_view(['POST'])
def api_create_user_view(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # 先存user
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            new_user = user_serializer.save()
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
        print(user)
        if user is not None:
            token = Token.objects.get(user=user).key
            # print(type(token))
            return Response({"token": token})
        else:
            print(123)
            return Response({"failure": "login failed, wrong username or password"}, status=status.HTTP_400_BAD_REQUEST)