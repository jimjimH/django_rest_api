
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt

# Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# 登入後(輸入帳密後)，回傳該user token
# 1. 
# from rest_framework.authtoken.models import Token
# token = Token.objects.get(user=...)去取得token
# print(token.key)
# 2.
# 用現成的api
# from rest_framework.authtoken.views import obtain_auth_token
# path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


# Token Auth後的get, post動作
class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


'''
# 一般序列化後回傳JSON方法
import json
from django.http import JsonResponse
from django.core import serializers

def index(request):
    users = User.objects.all().select_related('profile')
    print(list(users.values()))
    # print(users[0].profile.gender)
    # return render(request, 'index.html', locals())

    return JsonResponse({'result': list(users.values())})

    user_json = serializers.serialize('json', users)
    return HttpResponse(user_json, content_type='application/json')
'''
